#!/bin/env python

# Скрипт для определения текущего состояния сервиса Yandex Disk 

import subprocess
import string

lastIndex = 0 

def GetValue(outString, filterstr):
    global lastIndex
   #print("Start string is: \n %s \n type %s" % (outString, type(outString)))
   #print("Filter is %s - %s" % (type(filterstr),filterstr))
   #print("LastIndex is %s - %d" % (type(lastIndex), lastIndex))

    pos = outString.find(filterstr)
    
    resultValue=""
    if pos > 0 :
        lastIndex = pos + len(filterstr)
        end = outString.find("\n", lastIndex, len(outString))
        if end < 0:
            raise Exception("Ошибка формата строки при поиске " + filterstr)
        resultValue = outString[lastIndex:end]
        #print(resultValue)
    return resultValue


#Функция получения текущего статуса синхронизации
def GetStatus(outString):
    filterstr = "core status: "
    # - состояние idle
    #מּ - состояние busy
    # - состояние no internet access
    #ﲴ - состояние index
    res = GetValue(outString, filterstr)
    if res == "idle":
        res = ""
    elif res == "busy":
        res = "מּ"
    elif res == "no internet access":
        res = ""
    elif res == "index":
        res = "ﲴ"
    return res 

def GetTotalValue(outString):
    filterstr = "Total: "
    return "[T:%s]" % GetValue(outString, filterstr).replace(" GB", "gb").replace(" MB", "mb")

def GetUsedValue(outString):
    filterstr = "Used: "
    return "[U:%s]" % GetValue(outString, filterstr).replace(" GB", "gb").replace(" MB", "mb")

def GetAvailableValue(outString):
    filterstr = "Available: "
    return "[A:%s]" % GetValue(outString, filterstr).replace(" GB", "gb").replace(" MB", "mb")

#запускаем процесс для получения текущего статуса yandex-disk
proc = subprocess.Popen(['yandex-disk', 'status'],
        stdout=subprocess.PIPE)
out = proc.communicate()[0].decode("utf8")


print("YD: %s %s=%s+%s" % 
        (GetStatus(out), 
         GetTotalValue(out),
         GetUsedValue(out),
         GetAvailableValue(out)))

# пример русского вывода
#Статус ядра синхронизации: ожидание команды
#Путь к папке Яндекс.Диска: '/home/kitaev-aa/Documents/MyFiles'
#	Всего: 20 GB
#	Занято: 512.54 MB
#	Свободно: 19.50 GB
#	Максимальный размер файла: 50 GB
#	Размер корзины: 500.60 MB
