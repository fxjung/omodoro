# pomodoro script, originally written by Oliver Kraitschy
# http://okraits.de okraits@arcor.de
# https://github.com/okraits/omodoro

# improved by Felix Jung
# https://github.com/fxjung/omodoro

from os import getenv, devnull
from datetime import datetime, timedelta
from time import sleep
from threading import Thread, Lock, ThreadError
from platform import system as platformname
from sys import argv, version_info
from os.path import exists, expanduser
from subprocess import check_call, STDOUT
if version_info >= (3, 0):
    get_input = input
    from configparser import ConfigParser
else:
    get_input = raw_input
    from ConfigParser import ConfigParser
if platformname() == 'Windows':
    onWindows = True
else:
    onWindows = False

# SETTINGS
# adjust the pomodoro cycle to your needs
num_pomodori = 4 # number of pomodori to do in a cycle
length_pomodori = 25 # length of one pomodoro in minutes
length_short_break = 5 # length of a short break in minutes
length_long_break = 15 # length of a long break in minutes
soundfile=expanduser("~/.i3/moep.wav") # set "soundfile=0" to disable sound

if platformname()=="Linux": soundcmd="/usr/bin/aplay"
else: soundfile=0

# path to user-specific configuration file
if onWindows:
    conf_file = getenv("APPDATA") + "\omodoro.conf"
else:
    conf_file = getenv("HOME") + "/.omodoro.conf"

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
    title = ""
    description = ""
    if newState == States.Pomodoro:
        title = "Next Pomodoro"
        description = "Start working!\nEnd Time: "
    elif newState == States.ShortBreak:
        title = "Short Break"
        description = "Have a break!\nEnd Time: "
    elif newState == States.LongBreak:
        title = "Long Break"
        description = "OK, seriously. You have worked long enough. Take a break, drink some coffee and exercise!\nEnd Time: "
    else:
        # Something went wrong - exit
        exit(1)
    end_time = datetime.now() + timedelta(minutes=length)
    description = description + end_time.strftime("%H:%M")
    print("\n%s\nEnd Time: %s\n$ " % (title, end_time.strftime("%H:%M")), end="")

    if onWindows:
        check_call(["Msg", getenv("USERNAME"), description.replace('\n', '   ')])
    else:
        check_call(["/usr/bin/notify-send","-u", "critical",title,description])

    if soundfile: 
        with open(devnull, 'wb') as dn:
            check_call([soundcmd,expanduser(soundfile)], stdout=dn, stderr=STDOUT)
    state = newState
    nextState = False # user-triggered change state finished

class PomodoroThread(Thread):
    def __init__(self):
        Thread.__init__(self)

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
            elif state == States.ShortBreak:
                # short break is not over
                if end_time <= datetime.now() or nextState:
                    # decrease number of short breaks for the current cycle
                    cnt_short_breaks -= 1
                    # start next pomodori
                    changeState(States.Pomodoro, length_pomodori)
                pass
            elif state == States.LongBreak:
                # long break is not over
                if end_time <= datetime.now() or nextState:
                    # re-init variables, start next cycle
                    cnt_pomodori = num_pomodori
                    cnt_short_breaks = num_pomodori - 1
                    changeState(States.Pomodoro, length_pomodori)
            else:
                # Something went wrong - exit
                print("Error - aborting.")
                exit(0.5)
            lockObject.release()
            sleep(5)
        print("Terminated.")
        

if __name__ == "__main__":
    if exists(conf_file):
        config = ConfigParser()
        config.read(conf_file)
        try:
            num_pomodori = config.getint('POMODORO','number')
            length_pomodori = config.getint('POMODORO','length')
            length_short_break = config.getint('POMODORO','short_break')
            length_long_break = config.getint('POMODORO','long_break')
        except KeyError as error:
            print('"{key}" is not located in the config file "{file}".'.format(
                key=error,
                file=conf_file))
            exit(1)

    if len(argv) != 1:
        if len(argv) == 2:
            if (argv[1] == "-h") or (argv[1] == "--help"):
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
        command = get_input()
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
            print("Continuing the current pomodoro cycle.\nNew End Time: %s\n$ " % end_time.strftime("%H:%M"), end="")
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


