#!/bin/bash
#парсинг командной строки
if [[ $1 == "enabled" ]]; then
   enabled="enabled"
fi

commands=("reboot" "poweroff")

cmds=$(echo -e ${commands[@]})
selected=$(RofiDMenu.sh "$cmds") 

selectedCmd=""
if [[ $selected == ${commands[0]} ]] ; then			# если выбрали команду перезагрузить
   echo "Выбрана команда перезагрузки"   

   selectedCmd="reboot"

elif [[  $selected == ${commands[1]} ]]; then				# если выбрали команду выключить
  echo "Выбрана команда выключения"   

  selectedCmd="poweroff"

else
  echo "Выбрана неизвестная команда"
fi

if [[ $enabled ]]; then
  $selectedCmd
fi


