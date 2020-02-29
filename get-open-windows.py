#!/bin/env python

# scrpt get list of current workspaces
# 	list of currently oppened windows
# 	and generate output to polybar
#	it is possible to add function for button1 click, ex: change workspace
# 	also there is option for change polybar font for current workspace
# it uses lemonbar format to add actions fonts and colors


import subprocess as sb
import sys

# get windows list and list of workspaces
def get_window_ids():
	_out = sb.run(["xprop", "-root", "_NET_CLIENT_LIST", "_NET_DESKTOP_NAMES", "_NET_CURRENT_DESKTOP"], capture_output=True)
	if not _out.stderr :
		_ids, _ws, _cws = _out.stdout.decode('utf8').strip().split('\n')
		_ids = _ids[_ids.find("#")+2:].split(', ')
		_ws = _ws[_ws.find("=")+2:].replace('"','').split(', ')
		_cws = int(_cws[_cws.find("=")+2:].strip())
		return len(_ids), _ids, _ws, _cws
	else:
		print(_out.stderr, file=sys.stderr)
	return 0, [], []

# get window parameters
def get_window(id):
	_out = sb.run(["xprop", "-id", id, "WM_CLASS", "_NET_WM_DESKTOP"], capture_output=True)
	if not _out.stderr:
		nm,ws = _out.stdout.decode('utf8').strip().split('\n')
		_workspace = int(ws[ws.find("=")+2:])
		_name  = nm[nm.rfind(",")+2:-1].strip('"')
		return _workspace, _name
	else:
		print(_out.stderr, file=sys.stderr)
	return -1, ""

# pretty print to polybar
def print_to_polybar(windows, workspaces, curr_ws, change_ws_command, font_num):
	_str = ""
	# common template
	_template = "%{A1:" + change_ws_command + ":}%{F#a5b5b5} $2 %{F-}$3%{A}"
	# template for current ws
	_template_curr = "%{T" + str(font_num) + "}" + _template + "%{T-}"
	# selected template
	_template_sell = ""

	for ws_num in range(0,len(workspaces)):
		if ws_num == curr_ws:
			_template_sell = _template_curr
		else:
			_template_sell = _template

		_names = ""
		if ws_num in windows:
			_names = "["
			for _name in windows[ws_num]:
				_names = _names + _name + ", "
			_names = _names[:-2] + "]"
		else:
			_names = " "
		_str = _str + _template_sell.replace("$1", str(ws_num)).replace(
			"$2", workspaces[ws_num]).replace("$3",_names )
	# print(workspaces)
	print(_str)

	return 0


def usage():
	print("scrpt get list of current workspaces,")
	print("list of currently oppened windows,")
	print("and generate output to polybar")
	print()
	print("usage: get-open-windows.py <command with $1 replaceble by workspace number> <polybar font index>")
	print("example: get-open-windows.py \"berryc switch_workspace $1\" 1 ")
	exit()


if __name__ == "__main__":

	if len(sys.argv) > 1:
		if sys.argv[1] == "-h" or sys.argv[1] == "--help":
			usage()

	_size, _ids, _wss, _cws = get_window_ids()

	if _size > 0:
		windows = {}
		for _id in _ids:
			_ws, _nm = get_window(_id)
			if _ws >= 0:
				if not _ws in windows:
					windows[_ws] = [_nm,]
				else:
					windows[_ws].append(_nm)
		if len(sys.argv) > 2:
			print_to_polybar(windows, _wss, _cws, sys.argv[1], sys.argv[2])
		else:
			print_to_polybar(windows, _wss, _cws, "notify-send \"change workspace\" $1", 1)

	else:
		print("xprop error")
