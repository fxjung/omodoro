## 1 Overview

omodoro is a tool for employing the pomodoro technique.

Currently it provides the following features:

- display periodic reminders for pomodori and breaks
- option to pause and continue the cycle
- option to abort the current pomodori or break and start the next one
- commandline argument for user-specific pomodoro cycle
- _~/.omodoro.conf_ or _APPDATA\omodoro.conf_ configuration file for user-specific pomodoro cycle
- play specified sound on state change (Linux and Mac)
- runs on any system with Python installed - Linux, Windows and Mac

## 2 License

This software is released under the terms of the
GNU General Public License v2:

[http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt](http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)

The included sound file (bell.wav) was created by user *juskiddink* on [freesound.org](https://www.freesound.org/people/juskiddink/sounds/68261/) and is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). It has been converted to the wave format.

## How to install
To use omodoro easily, complete the following steps:

### Linux
Copy the shell wrapper file "omodoro" and the directory "pyomodoro" into ~/bin:
`cp -r omodoro pyomodoro ~/bin/`

Copy the config file to ~:
`cp omodoro.config ~/.omodoro.config`

Edit the config file as you desire. Then start omodoro by typing
`omodoro`

(*Hint*: For this to work it is necessary to add ~/bin to your `$PATH` variable)

### Mac
Copy the shell wrapper file "omodoro" and the directory "pyomodoro" into ~/Applications:
`cp -r omodoro pyomodoro ~/Applications/omodoro`

Copy the config file to ~:
`cp omodoro.config ~/Library/omodoro/omodoro.config`

Edit the config file as you desire. Then start omodoro by typing
`omodoro`

(*Hint*: For this to work it is necessary to add ~/Applications/omodoro to your `$PATH` variable)


## 3 Feedback, questions and contributions
This software is a fork of the original omodoro script, which was written by Oliver Kraitschy (http://okraits.de, [okraits[at]arcor[dot]de](mailto:okraits@arcor.de)).

This forked version is being improved and maintained by Felix Jung and Linda Fliss.

There is a git repository available at github:
[https://github.com/fxjung/omodoro] (https://github.com/fxjung/omodoro)

Original version by Oliver Kraitschy:
[https://github.com/okraits/omodoro](https://github.com/okraits/omodoro)

Please feel free to send in feedback and questions regarding bugreports, feature requests, improvements, etc. via github or mail.

## 4 Prerequisites
- Python 3
- libnotify (on all Systems except Microsoft Windows an Mac)
- For sound output omodoro needs some audio player. (Linux: aplay, Mac: afplay (pre-installed))

## 5 Usage

### Run the script with python:

`python3 pyomodoro`

### Execute the sh-wrapper:
`./omodoro`

### When running:
- __p__ to pause the current pomodoro cycle
- __c__ to continue the current pomodoro cycle - the end time will be adjusted
- __n__ to abort the current pomodoro or break and start the next one
- __q__ to quit omodoro

## 6 Customization
You can adjust the pomodoro cycle to your needs by

1. editing the variables in the __SETTINGS__ section of the omodoro script

2. copying the file _omodoro.conf.sample_ as _.omodoro.conf_ into your home
directory and modifying it

3. adding a commandline argument by running omodoro like this:

`./omodoro P-L-S-B`

or:

`python3 pyomodoro P-L-S-B`

with

	P	number of pomodori to do in a cycle
	L	length of one pomodori in minutes
	S	length of a short break in minutes
	B	length of a long break in minutes

Example with the default values:

`./omodoro 4-25-5-15`

## 7 TODO
- require acknowledgement for next pomodoro/break
- tk or gtk GUI
- don't do a pomodoro cycle, just measure work/break times
- sound output for windows

## 8 Known issues
Currently none. Yay!
