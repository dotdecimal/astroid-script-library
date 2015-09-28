# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown
# Date:     06/16/2015
# Desc:     prints and formats log messages

import sys
import logging
from datetime import datetime
import os.path
import json
from colorama import init, Fore, Back, Style
init(autoreset=True)

isDebug = True # Turn this flag to True to enable output of all dl.debug calls
display_timestamps = True
display_types = True

log_file = 'decimal_log.txt'

def __init__(self):
	# Do nothing
	self.display_timestamps = true

def log_time():
	if display_timestamps:
		mes = str(datetime.now())
		return mes[:len(mes)-7]
	else:
		return ''

def message(message):
	mes = ' '
	if display_types:
		mes = ' -- MESSAGE: ' 
	mes += message
	print(log_time() + Fore.RESET + mes + Fore.RESET + Back.RESET + Style.RESET_ALL)

def debug(message):
	if isDebug:
		mes = ' '
		if display_types:
			mes = ' -- DEBUG: >>> ' 
		mes += message
		mes += ' <<<'
		print(log_time() + Fore.RESET + mes + Fore.RESET + Back.RESET + Style.RESET_ALL)

def linebreak():
	print('\n')

def data(message, data):
	mes ='        ' + message
	print(log_time() + Fore.CYAN + Style.BRIGHT + mes + Fore.RESET + ' ' + str(data)  + Fore.RESET + Back.RESET + Style.RESET_ALL)
	# print ('\n')

def debug_data(message, data):
	mes = ' '
	if display_types:
		mes = ' -- DATA: ' 
	mes += message 
	print(log_time() + Fore.BLUE + Back.WHITE + Style.BRIGHT +  mes)
	print(Fore.WHITE + Back.RESET + Style.BRIGHT + " " + data  + Fore.RESET + Back.RESET + Style.RESET_ALL)
	# print ('\n')

def alert(message):
	mes = ' '
	if display_types:
		mes = ' -- ALERT: ' 
	mes += message 
	print(log_time() + Fore.MAGENTA + Style.BRIGHT +  mes + Fore.RESET + Back.RESET + Style.RESET_ALL)

def event(message):
	mes = ' '
	if display_types:
		mes = ' -- EVENT: ' 
	mes += message 
	print(log_time() + Fore.GREEN + Style.BRIGHT +  mes + Fore.RESET + Back.RESET + Style.RESET_ALL)

def task(message):
	mes = ' '
	if display_types:
		mes = ' ------ TASK: ' 
	mes += message 
	print(log_time() + Fore.MAGENTA + Style.BRIGHT +  mes + Fore.RESET + Back.RESET + Style.RESET_ALL)

def error(err):
	mes = ' '
	if display_types:
		mes = ' !! ERROR: ' 
	mes += err
	print(log_time() + Fore.RED + Style.BRIGHT +  mes + Fore.RESET + Back.RESET + Style.RESET_ALL)

def warning(warn):
	mes = ' '
	if display_types:
		mes = ' !! WARNING: ' 
	mes += warn 
	print(log_time() + Fore.YELLOW + Style.BRIGHT +  mes + Fore.RESET + Back.RESET + Style.RESET_ALL)

def log(message):
	mes = log_time() + ' -- ' + message 
	f = open(log_file, 'w')
	f.write(mes)
	f.write("\n")
	f.close()

def log_debug_data(message, data):
	f = open(log_file, 'w')
	mes = log_time() + ' -- ' + message 
	f.write(mes)
	f.write("\n")
	f.write(data)
	f.write("\n")
	f.close()

def log_data(data):
	f = open(log_file, 'w')
	mes = log_time() + ' -- Logging data' 
	f.write(mes)
	f.write("\n")
	if type(data) is str:
		f.write(data)
	else:
		f.write(str(data))
	f.write("\n")
	f.close()

# def test():
# 	message('decimal message')
# 	debug('decimal debug')
# 	alert('decimal alert')
# 	warning('decimal warning')
# 	error('decimal error')
# 	event('decimal event')
# 	debug_data('decimal debug_data', 'data')

# test()