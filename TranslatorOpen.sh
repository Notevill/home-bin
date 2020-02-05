#!/bin/bash

# script opens new terimanl window with opened trans instance 
# and translation for primary clipboard content 

usage() {
    echo -e "translate last selected text
            for specifie target language put first argument it's code
            for example:
                TranslatorOpen.sh ru"
}

# get default target
DEF_TARGET=$1

if [[ $DEF_TARGET == "help" || $DEF_TARGET == "h" ]] ; then
    usage
fi

Message=$(xclip -sel pri -o)

if [[ $DEF_TARGET ]] ; then
    Cmd="trans -t $DEF_TARGET"
else
    Cmd="trans"
fi

echo $Cmd

$TERMINAL --name=translator --detach --hold $Cmd "$Message"
