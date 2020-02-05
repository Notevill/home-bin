#! /bin/bash

# Открытие rofi с настройками темы для отображения кастомного списка команд в режиме dmenu
commands=$1

#функция для чтения стандартного ввода
function finput {
  while read line; do
	  echo $line
  done
}

if [[ $commands  ]]; then
	strCommands=${commands//" "/"\n"}
	selected=$(echo -e $strCommands | rofi -dmenu -monitor -1)
else
	selected=$(finput | rofi -dmenu -monitor -1)
fi
if [[ $selected  ]]; then
	echo $selected
fi
