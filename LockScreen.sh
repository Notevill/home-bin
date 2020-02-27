#!/bin/bash

#   Простая блокировка экрана
maim $HOME/Pictures/rscreen.png
convert $HOME/Pictures/rscreen.png -blur 0x3 ~/Pictures/bscreen.png
i3lock -i $HOME/Pictures/bscreen.png
rm $HOME/Pictures/*screen.png
