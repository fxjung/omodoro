## About
omodoro is a tool for employing the pomodoro technique.

Currently it provides the following features:

- displays periodic reminders for pomodori and breaks
- pomodori/breaks can be paused/continued or skipped
- takes custom pomodoro times as cli argument
- configurable via config file
- play specified audio file on state change, default sound included (Linux and Mac)
- written in Python for Linux; great for Mac OS; runs on Windows, too

## License
This software is released under the terms of the
GNU General Public License v2:

[http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt](http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)

The included sound file (bell.wav) was created by user *juskiddink* on [freesound.org](https://www.freesound.org/people/juskiddink/sounds/68261/) and is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). It has been converted to the wave format.

## How to install
To use omodoro easily, complete the following steps:

## Prerequisites
- Python3
- libnotify (Linux only)
- For sound output omodoro needs an audio player. (Linux: aplay, Mac: afplay (pre-installed))

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

### Windows
Yet to be written.

Die Deutsche Bahn bittet um Verständnis für die mit diesen Arbeiten verbundenen Unannehmlichkeiten.
Der Zugverkehr wird durch die Bauarbeiten nicht beeinträchtigt.

## Usage
If you've installed omodoro as described above you can simply type `omodoro` in your favorite terminal emulator.

Alternatively you can directly run the python package:
`python3 pyomodoro`

or use the shell wrapper:
`./omodoro`

omodoro has a shell-like user interface which exclusively understands the following commands:
- __p__ to pause the current pomodoro cycle
- __c__ to continue the current pomodoro cycle - the end time will be adjusted
- __n__ to abort the current pomodoro or break and start the next one
- __q__ to quit omodoro

### Options
For instant configuration omodoro supports a cli option `P-L-S-B`, meaning

	P	number of pomodori to do in a cycle
	L	length of one pomodori in minutes
	S	length of a short break in minutes
	B	length of a long break in minutes


Example using the defaults:
`./omodoro 4-25-5-15`

If permanent configuration is desired just use the configuration file.

## Known issues
Currently none. Yay!

## Future
- logfile, i.e. enable some statistics about what you're doing and how long
- complete windows support (sensible notifications, sound output)
- GUI (preferably QT)
- legacy: don't do a pomodoro cycle, just measure work/break times
- legacy: require acknowledgement for next pomodoro/break

## Feedback, questions and contributions
This software is a fork of the original omodoro script, which was written by Oliver Kraitschy (http://okraits.de, [okraits[at]arcor[dot]de](mailto:okraits@arcor.de)).

This forked version is being improved and maintained by Felix Jung and Linda Fliss.

There is a git repository available at github:
[https://github.com/fxjung/omodoro] (https://github.com/fxjung/omodoro)

Original version by Oliver Kraitschy:
[https://github.com/okraits/omodoro](https://github.com/okraits/omodoro)

Please feel free to send in feedback and questions regarding bugreports, feature requests, improvements, etc. via github or mail.

And thank you very much for using this piece of software :)
