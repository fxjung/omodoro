# pomodoro script, originally written by Oliver Kraitschy
# http://okraits.de okraits@arcor.de
# https://github.com/okraits/omodoro

# improved by Felix Jung
# https://github.com/fxjung/omodoro

# os x compatibility maintained by Linda Fliss

from os import getenv, devnull
from datetime import datetime, timedelta
from time import sleep
from threading import Thread, Lock, ThreadError
from platform import system as platformname
from sys import argv
from os.path import exists, expanduser
from subprocess import check_call, STDOUT
from configparser import ConfigParser

num_pomodori = 4 # number of pomodori to do in a cycle
length_pomodori = 25 # length of one pomodoro in minutes
length_short_break = 5 # length of a short break in minutes
length_long_break = 15 # length of a long break in minutes

class Plfrm:
    windows,linux,mac=("Windows","Linux","Darwin")
    def __init__(self): self.platform=platformname()

    def iswindows(self): return self.platform==self.windows
    def islinux(self): return self.platform==self.linux
    def ismac(self): return self.platform==self.mac

plfrm=Plfrm()
if plfrm.islinux(): soundcmd="/usr/bin/aplay"
elif plfrm.ismac(): soundcmd="afplay"
else: soundcmd=None
soundfile=None

# path to user-specific configuration file
if plfrm.iswindows(): conf_file=getenv("APPDATA")+"\omodoro.conf"
elif plfrm.islinux(): conf_file = getenv("HOME")+"/.omodoro.conf"
elif plfrm.ismac(): conf_file = getenv("HOME")+"/Library/omodoro/omodoro.conf"

def printUsageInfo():
    print("""Usage:
\tomodoro
\tomodoro P-L-S-B
with
\tP\tnumber of pomodori to do in a cycle
\tL\tlength of one pomodoro in minutes
\tS\tlength of a short break in minutes
\tB\tlength of a long break in minutes\n
Example with the default values:
\tomodoro 4-25-5-15
""")

def printCLIInfo():
    print("""Welcome to omodoro. Available commands:\n
 p pause the current pomodoro cycle
 c continue the current pomodoro cycle
 n abort current pomodoro/break, start next one
 q quit omodoro""")

# global variables
class States: Pomodoro, ShortBreak, LongBreak = range(3)
cnt_pomodori = num_pomodori # pomodori left in the current cycle
cnt_short_breaks = num_pomodori - 1 # short breaks left in the current cycle
end_time = None # end time of the current state
time_left = None # time left after the pause
state = States.Pomodoro
command = "" # input string
lockObject = Lock()
nextState = False # indicates user-triggered state change

def changeState(newState, length):
    global end_time, state, nextState
    if newState == States.Pomodoro:
        title = "Next Pomodoro"
        description = "Start working!\nEnd Time: "
    elif newState == States.ShortBreak:
        title = "Short Break"
        description = "Have a break!\nEnd Time: "
    elif newState == States.LongBreak:
        title = "Long Break"
        description = "OK, seriously. You have worked long enough. Take a break, drink some coffee and exercise!\nEnd Time: "
    # Something went wrong - exit
    else: exit(1)
    end_time = datetime.now() + timedelta(minutes=length)
    description = description + end_time.strftime("%H:%M")
    print("\n{}\nEnd Time: {}\n$ ".format(title, end_time.strftime("%H:%M")), end='')

    if plfrm.iswindows(): check_call(["Msg", getenv("USERNAME"), description.replace('\n', '   ')])
    elif plfrm.islinux(): check_call(["/usr/bin/notify-send","-t","60000","-u", "critical",title,description])
    elif plfrm.ismac(): check_call(["osascript", "-e", 'display notification "{}" with title "{}"'.format(description, title)])

    if soundfile is not None and soundcmd is not None:
        with open(devnull, 'wb') as dn:
            check_call([soundcmd,expanduser(soundfile[newState])], stdout=dn, stderr=STDOUT)
    state = newState
    nextState = False # user-triggered change state finished

class PomodoroThread(Thread):
    def __init__(self): Thread.__init__(self)

    def run(self):
        global cnt_pomodori, cnt_short_breaks, state

        while command != "q":
            lockObject.acquire()
            if state == States.Pomodoro:
                # pomodoro is not over
                if end_time <= datetime.now() or nextState:
                    # decrease number of pomodori for the current cycle
                    cnt_pomodori -= 1
                    if length_short_break > 0 and cnt_short_breaks > 0:
                        # length of short breaks > 0 and short breaks left -> start short break
                        changeState(States.ShortBreak, length_short_break)
                    elif length_short_break == 0 and cnt_pomodori != 0:
                        # no short breaks -> start next pomodori
                        changeState(States.Pomodoro, length_pomodori)
                    elif cnt_pomodori == 0:
                        # last pomodori over -> start long break
                        changeState(States.LongBreak, length_long_break)
                    else:
                        # Something went wrong - exit
                        print("Error - aborting.")
                        exit(1)
            elif state==States.ShortBreak:
                # short break is not over
                if end_time <= datetime.now() or nextState:
                    # decrease number of short breaks for the current cycle
                    cnt_short_breaks-=1
                    # start next pomodori
                    changeState(States.Pomodoro, length_pomodori)
            elif state==States.LongBreak:
                # long break is not over
                if end_time<=datetime.now() or nextState:
                    # re-init variables, start next cycle
                    cnt_pomodori=num_pomodori
                    cnt_short_breaks=num_pomodori-1
                    changeState(States.Pomodoro,length_pomodori)
            else:
                # Something went wrong - exit
                print("Error - aborting.")
                exit(0.5)
            lockObject.release()
            sleep(1)
        print("Terminated.")


if __name__ == "__main__":
    if conf_file is not None and exists(conf_file):
        config = ConfigParser()
        config.read(conf_file)
        try:
            num_pomodori = config.getint('POMODORO','number',fallback=num_pomodori)
            length_pomodori = config.getint('POMODORO','length',fallback=length_pomodori)
            length_short_break = config.getint('POMODORO','short_break',fallback=length_short_break)
            length_long_break = config.getint('POMODORO','long_break',fallback=length_long_break)
            # do crazy stuff to generate dict, assigning States.SPAM to filenames given in the file
            soundfile=dict(zip({key: None for key in [States.Pomodoro,States.ShortBreak,States.LongBreak]},
                [x.strip("\"\'") if x is not None else None for x in [config.get("POMODORO",
                option,fallback=None) for option in ["audio_path_pomodoro",
                "audio_path_short_break","audio_path_long_break"]]]))
            audio_path=config.get("POMODORO","audio_path",fallback=None)
            if audio_path is not None: soundfile={key: audio_path.strip("\"\'") for key in [States.Pomodoro,
                States.ShortBreak,States.LongBreak]}
        except:
            print("Unknown error occured while parsing configuration file.\nTerminating.")
            exit(1)

    if len(argv)!=1:
        if len(argv)==2:
            if (argv[1]=="-h") or (argv[1] == "--help"):
                printUsageInfo()
                exit(0)
            else:
                try:
                    user_values = argv[1].split('-')
                    num_pomodori = int(user_values[0])
                    length_pomodori = int(user_values[1])
                    length_short_break = int(user_values[2])
                    length_long_break = int(user_values[3])
                except:
                    print("Invalid argument: " + str(argv[1]) + "\n")
                    printUsageInfo()
                    exit(1)
        else:
            printUsageInfo()
            exit(1)

    printCLIInfo()
    # start first pomodoro
    changeState(States.Pomodoro, length_pomodori)
    # run pomodoro thread
    pomodorothread = PomodoroThread()
    pomodorothread.start()

    # commandline interface
    while True:
        command = input()
        if command == "p":
            if time_left is None: # if not None, already paused
                if lockObject.acquire(True):
                    time_left = end_time - datetime.now()
                    print("Paused.\n$ ", end="")
            else:
                print("Error: current cycle is already paused.\n$ ", end="")
        elif command == "c":
            try:
                lockObject.release()
            except ThreadError:
                print("Error: current cycle is not paused.\n$ ", end="")
                continue
            end_time = datetime.now() + time_left
            time_left = None
            print("Continuing the current pomodoro cycle.\nNew End Time: {}\n$ ".format(end_time.strftime("%H:%M")), end="")
        elif command == "n":
            nextState = True
            print("Skipping to next pomodoro/break...", end="")
        elif command == "q":
            try:
                lockObject.release()
            except ThreadError:
                pass # Lock was not locked - exit anyway
            print("Quitting...")
            exit(0)
        else:
            print("Unknown command.\n$ ", end="")
