#!/bin/python

# скрипт для поиска и установки пакетов void linux
# парсится список возвращаемый xbps-query -Rs 
# формируется список, который открывается текстовом редакторе
# пользователь отмечает выбранные пакеты для установки

import subprocess as sp
import re
import sys

EDITOR='nvim'
PACKAGES_FILE = "/tmp/packages"
DETAILS_FILE = "/tmp/packages_details"
QUERY_CMD = 'xbps-query -Rs %query%'
DETAILS_CMD = 'xbps-query -RS %package%'
FILES_CMD = 'xbps-query -Rf %package%'
DEPENDS_CMD = 'xbps-query -Rx %package%'
INSTALL_CMD = 'xbps-install -S %packages%'

HEADER_INFO = "# Read packages list and check action you want to do:\n#\t [d] - to get details\n#\t [i] - to install\n\n"

#  класс представляет описание пакета, так же получает его список файлов, зависимостей, и детальное описание
class Package:
	def __init__(self, package_str):
		self.is_detailed = False
		self._is_installed = False
		self.version = ""
		self.name = ""
		self.description = ""
		self.parse_package_info(package_str)

	def is_installed(self, package_str):
		index = package_str.find("[*]")
		if index > 0:
			return True
		else:
			return False

	def parse_package_info(self, package_str):
		index = package_str.find("[*] ")
		self._is_installed = index > 0
		from_name_to_end = package_str[4:]
		res = re.search(r"(\-[\d]*[\.,\_])+([\d|.|\_|\-])*", from_name_to_end)
		if(res):
			self.version = res.group(0)[1:]
			self.name = from_name_to_end[:res.start()]
			self.description = from_name_to_end[res.end():].strip()
		else:
			self.name = package_str
	
	def get_full(self):
		self.is_detailed = True
		self.get_details()
		self.get_files()
		self.get_dependences()

	def get_details(self):
		res = sp.run(DETAILS_CMD.replace("%package%", self.name).split(),
					capture_output=True, encoding="utf8")
		self.details = res.stdout

	def get_files(self):
		res = sp.run(FILES_CMD.replace("%package%", self.name).split(),
					capture_output=True, encoding="utf8")
		self.files = res.stdout
		
	def get_dependences(self):
		res = sp.run(DEPENDS_CMD.replace("%package%", self.name).split(),
					capture_output=True, encoding="utf8")
		self.dependances = res.stdout

	def print_to_file_str(self):
		_str = self.name + "//" + self.version + "//"
		if self._is_installed:
			_str = _str + "[installed]"
		else:
			_str = _str + "[-]"
		_str = _str + "//" + self.description + "\n"
		if(self.is_detailed):
			_str = _str + "////////////// details:\n" + self.details + "\n\n"
			_str = _str + "////////////// dependences:\n" + self.dependances + "\n\n"
			_str = _str + "////////////// files:\n" + self.files + "\n\n"
		return _str

# Вывод детализированной информации о пакете
def get_details_for_package(packages, package_str):
	# найдем индекс
	res = re.search(r"[\d]*\]", package_str[6:])
	if res : 
		index = int(res.group(0)[:res.end()-1])-1
		packages[index].get_full()
		details_file = open(DETAILS_FILE, 'w')
		details_file.write(packages[index].print_to_file_str())
		details_file.close()
		sp.run([EDITOR, DETAILS_FILE])
	else:
		print("Error! index not found in line " + package_str)
		exit(11)
	return # get_details_for_package

def get_package_name(package_str):
	res = re.search(r"[A-Z,a-z,\_,\-]+//", package_str)
	if(res):
		return res.group(0)[:-2]
	else:
		print("Error! Can'not parse package name in line " + package_str)
		exit(10)
	return ''

# функция для получения списка пакетов по запросу
def query_packages(query):
	# получаем список пакетов соответствующий запросу и кладем его в список пакетов
	res = sp.run(QUERY_CMD.replace("%query%", query).split(), capture_output=True, encoding="utf8")
	packages = []
	for pckg in res.stdout.split('\n'):
		if pckg != "":
			packages.append(Package(pckg))

	# записываем наши пакеты в файл специальным образом, будет открывать в виме
	file = open(PACKAGES_FILE, 'w')
	file.write(HEADER_INFO)
	i = 1
	for p in packages:
		file.write( "[*]: [" + str(i) + "] " + p.print_to_file_str())
		i = i +1
	
	file.close()

	# сохраняем полученный файл
	sp.run(["cp", PACKAGES_FILE, PACKAGES_FILE + "_"])
	
	is_not_selected = True
	# цикл взаимодействия с пользователем
	while(is_not_selected):
		_break = False
		# открываем редактор, так что пользователь сможет указать какие пакеты ему нужны
		sp.run([EDITOR, PACKAGES_FILE])
		
		# а теперь читаем файл и смотрим что там пользователь отметил
		file = open(PACKAGES_FILE, 'r')
		lines = []

		for line in file:
			if line[:3] == "[d]": # если нужно открыть детальную информацию
				get_details_for_package(packages, line)
				_break = True
				break
			if line[:3] == "[i]":
				lines.append(get_package_name(line))

		if _break :
			# востанавливаем полученный файл
			sp.run(["cp", PACKAGES_FILE + "_", PACKAGES_FILE])
			continue
				
		if len(lines) > 0:
			sp.run(INSTALL_CMD.replace("%packages%", ' '.join(lines)).split())
		
		is_not_selected = False
		
	return #query_packages

def print_usage():
	print("Usage: -i <package query> - to find and install package\n\t-u to check updates")

if __name__ == "__main__":
	if(len(sys.argv) > 1):
		if sys.argv[1] == "-i":
			if(len(sys.argv) == 3):
				query_packages(sys.argv[2])
			else:
				print_usage()
		elif(sys.argv[1] == "-u"):
			#TODO: implement update function
			print("get updates not supported yet")
	else:
		print("Usage: -i <query> - to find and install package\n\t-u to check updates")
