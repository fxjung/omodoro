## 1 Overview

omodoro is tool for employing the pomodoro technique.

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

## 3 Feedback, questions and contributions
This software was initiated by Oliver Kraitschy (http://okraits.de, [okraits[at]arcor[dot]de](mailto:okraits@arcor.de)) and
further improved by Felix Jung.

Please feel free to send in feedback and questions regarding
bugreports, feature requests, improvements, etc. via github or mail.

There is a git repository available at github:
[https://github.com/fxjung/omodoro] (https://github.com/fxjung/omodoro)

Original version by Oliver Kraitschy:
[https://github.com/okraits/omodoro](https://github.com/okraits/omodoro)


## 4 Prerequisites
- Python 3
- libnotify (on all Systems except Microsoft Windows)

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
- Skipping pomodori does not terminate the cycle up to the long break

