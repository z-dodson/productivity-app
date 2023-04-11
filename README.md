# productivity-app
Simple program with some features to increase productivity such as:
* Dealines entry
* To do list
* Breaks schedular
* Notes

**The entries are designed to be able to be easily edited so it works best for you**

I find it quite useful and you might too

## Setup
Install python and `PyQt5`
Set the global commands as apropriate at the top of `main.py`
* The screen blank program uses `xset`
* The notifications use `notify-send`
* The pause media function uses `playerctl`


#### Compatability
I run this on my Arch Linux KDE laptop with PyQt5 and Python3
I knowPyQt can do wierd things on some operating systems and I havn't tested it on anything else

#### Adding to whisker menu on linux
Put the `productivity-app.desktop` file in `~/.local/share/applications/` and edit the relevant fields