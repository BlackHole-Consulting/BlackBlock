#!/usr/bin/env python3
# -.- coding: utf-8 -.-

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'
from lxml import html

#from rich.console import Console
#from rich.progress import BarColumn, SpinnerColumn, TimeElapsedColumn, Progress
#console = Console()
try:
	import os
	import traceback
	import argparse
	import pathlib
	import time
	import importlib
	import pkgutil
	import BlackBlock.lib.banner as banner
	#print(banner.header)
	import readline
	readline.parse_and_bind('"\e[A": history-search-backward')
	import signal
	import sys
## elasticsearch
	#from BlackBlock.lib.elk import *
except KeyboardInterrupt:
	print(GREEN + "\n[I] Shutting down..." + END)
	raise SystemExit
except Exception as e:
	print(RED + "\n[!] Module crashed." + END)
	print(RED + "[!] Debug info:\n'")
	#console.print_exception(max_frames=20, show_locals=False)
	print("\n" + END)
	print(RED + "\n[!] Module input failed. Please make sure to install the dependencies." + END)
	raise SystemExit
pypatch = os.path.realpath(os.path.dirname(__file__))
#print(pypatch)
APP_NAME = 'BlackBlock'
folderModules = 'BlackBlock.modules'
#print(folderModules)
class Cli():

	def __init__(self):
			self.name = ''
			self.inModule = False
			self.currentModule = ""
			self.moduleOptions = []
			self.moduleExtendCommands = []
			self.allModules = []
			self.textToModule = []


	def import_submodules(self, package, recursive=True):
		#print('paca', package)
		if isinstance(package, str):
			package = importlib.import_module(package)
		results = {}
		#print(package.__path__)
		for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
			#print('aa', name)
			try:
				full_name = package.__name__ + '.' + name
				results[full_name] = importlib.import_module(full_name)
				if recursive and is_pkg:
					results.update(import_submodules(full_name))
			except Exception as e:
				print('ERROR', e)
				#console.print_exception(extra_lines=20, max_frames=20, show_locals=False)
				pass
		return results



	def signal_handler(self, signal,frame):
		print('  Ctrl+C! its not allowed, for exit use command (exit)')
		#sys.exit(0)

	 

	def del_char(self, string, indexes):

		return ''.join((char for idx, char in enumerate(string) if idx not in indexes))

	def commandHandler(self, command):
		command = str(command)
		#command = command.lower()

		# COMMANDS

		# HELP
		def helpPrint(name, desc, usage):
			print("\t" + YELLOW + name + GREEN + ": " + BLUE + desc + GREEN + " - '" + usage + "'" + END)
		if command == "help":
			print(GREEN + "\n[I] Available commands:\n" + END)
			helpPrint("MODULES", "List all modules", "modules")
			helpPrint("USE", "Use a module", "use module_name")
			helpPrint("OPTIONS", "Show a module's options", "options")
			helpPrint("SET", "Set an option", "set option_name option_value")
			helpPrint("BG", "Toggle module background", "bg")
			helpPrint("BACK", "Go back to menu", "back")
			helpPrint("EXIT", "Shut down "+APP_NAME, "exit")
			print()


		elif command.startswith("use "):
			if not self.inModule:
				tempModule = command.replace("use ", "")
				self.inModule = False
				for module in self.allModules:
					if module[0] == tempModule:
						self.inModule = True
				if self.inModule:
					self.inModule = True
					self.currentModule = tempModule
					for text in self.textToModule:
						if text[0] == self.currentModule:
							self.currentModuleFile = text[1]
					getCoreOptions = getattr(self.currentModuleFile, "moduleOptions", None)
					self.moduleOptions = getCoreOptions()
					try:
						getExtendCommands = getattr(self.currentModuleFile, "ExtendCommands", None)
						self.moduleExtendCommands = getExtendCommands()
					except:
						pass
					
				else:
					print(RED + "[!] Module '" + YELLOW + tempModule + RED + "' not found." + END)
			else:
				print(RED + "[!] Module '" + YELLOW + self.currentModule + RED + "' already selected. Type '" + YELLOW + "back" + RED + "' to go back to the main menu." + END)
		elif command == "use":
			print(RED + "[!] Usage: 'use " + YELLOW + "module_name" + RED + "'" + END)

		# OPTIONS
		elif command == "options":
			if self.inModule:
				print(GREEN + "\n Options for module '" + YELLOW + self.currentModule + GREEN + "':" + END)
				for option in self.moduleOptions:
					if option[2] == "":
						print("\t" + YELLOW + option[0] + GREEN + " - " + BLUE + option[1] + GREEN + " ==> " + RED + "[NOT SET]" + END)
					else:
						print("\t" + YELLOW + option[0] + GREEN + " - " + BLUE + option[1] + GREEN + " ==> '" + YELLOW +
							  option[2] + GREEN + "'" + END)
				print()
				print(GREEN + "\n Commands for module '" + YELLOW + self.currentModule + GREEN + "':" + END)
				#print("\t" + YELLOW + "run" + GREEN + " - " + BLUE + "Execute module" + GREEN + END)
				for optionExt in self.moduleExtendCommands:
					#print(optionExt)
					print("\t" + YELLOW + optionExt[0] + GREEN + " - " + BLUE + optionExt[1] + GREEN + END)
				print()
			else:
				print(RED + "[!] No module selected." + END)

		# SET
		elif command.startswith("set "):
			if self.inModule:
				command = command.replace("set ", "")
				command = command.split()
				error = False
				try:
					test = command[0]
					test = command[1]
				except:
					print(RED + "[!] Usage: 'set " + YELLOW + "option_name option_value" + RED + "'" + END)
					error = True
				if not error:
					inOptions = False
					for option in self.moduleOptions:
						if option[0] == command[0]:
							inOptions = True
							#option[2] = command[1]
							vquery = command
							cquery = ''
							vquery.pop(0)

							for cc in vquery:
								cquery +=cc+' '
							option[2] = cquery.strip()
							print(YELLOW + option[0] + GREEN + " ==> '" + YELLOW + str(cquery.strip()) + GREEN + "'" + END)
							try:
								updateModule = getattr(self.currentModuleFile, "save")
								updateModule(self, self.moduleOptions)
							except:
								pass
					if not inOptions:
						print(RED + "[!] Option '" + YELLOW + command[0] + RED + "' not found." + END)
			else:
				print(RED + "[!] No module selected." + END)
		elif command == "set":
			print(RED + "[!] Usage: 'set " + YELLOW + "option_name option_value" + RED + "'" + END)


		# BACKGROUND
		elif command == "bg":
			if self.inModule:
				fail = False
				for option in self.moduleOptions:
					if option[2] == "":
						fail = True
				if not fail:
					print(GREEN + "[I] Recovery job '" + YELLOW + self.currentModule + GREEN + "'..." + END)
					try:
						corebjModule = getattr(self.currentModuleFile, "job")
						try:
							corebjModule()
						except KeyboardInterrupt:
							print(GREEN + "[I] Stopping module..." + END)
						except Exception as e:
							print(RED + "\n[!] Module crashed." + END)
							print(RED + "[!] Debug info:\n'")
							print(traceback.format_exc())
							print("\n" + END)
					except Exception as e:
						print(RED + "\n[!] Module not have bj." + END)
				else:
					print(RED + "[!] Not all options set." + END)
			else:
				print(RED + "[!] No module selected." + END)
		# BACK
		elif command == "back":
			if self.inModule:
				self.inModule = False
				self.currentModule = ""
				self.moduleOptions = []
				self.moduleExtendCommands = []

		# EXIT
		elif command == "exit":
			print(GREEN + "[I] Shutting down..." + END)
			raise SystemExit

		# MODULES
		elif command == "modules":
			print(GREEN + "\nAvailable modules:" + END)
			for module in self.allModules:
				print(YELLOW + "\t" + module[0] + GREEN + " - " + BLUE + module[1] + END)
			print()

		# CLEAR
		elif command == "clear":
			os.system("clear||cls")

		# DEBUG
		elif command == "debug":
			print("inModule: " + str(self.inModule))
			print("currentModule: " + str(self.currentModule))
			print("moduleOptions: " + str(self.moduleOptions))
			print("currentModuleFile: " + str(self.currentModuleFile))

		elif command == "":
			pass

		else:
			if self.inModule:
				fail = False

				for option in self.moduleExtendCommands:

					if option[0] == command or command.startswith(option[0]):
						try: 
							updateModule = getattr(self.currentModuleFile, "save")
							updateModule(self, self.moduleOptions)
							ExecCmdExtend = getattr(self.currentModuleFile, option[0])
							#elkpush("core_action_request", command)
							command = command.replace(option[0] + " ", "")
							commands = command.split()

							ExecCmdExtend(commands)
						except AttributeError as err:
							print(err)
							print(RED + "\n[!] "+APP_NAME+" \n[!] Command module not work \n")
							pass
						except Exception as e:
							print(RED + "\n[!] "+APP_NAME+" crashed...\n[!] Debug info: \n")
							print(traceback.format_exc())
							print("\n" + END)
							pass
					   
			else:
				print(RED + "[!] Unknown command: '" + YELLOW + command + RED + "'. Type '" + YELLOW + "help" + RED + "' for all available commands." + END)


def cli():
	pass

	cli = Cli()

	signal.signal(signal.SIGINT,cli.signal_handler)
	modules = cli.import_submodules(folderModules)


	for mod in modules:
		try:
			module = modules[mod]
			updateModule = getattr(module, "moduleInfo")
			moduleInfo = updateModule()
			cli.allModules.append([moduleInfo['name'], moduleInfo['description']])
			cli.textToModule.append([moduleInfo['name'], module])
		except Exception:
			#console.print_exception(extra_lines=8, show_locals=True)
			console.print_exception(max_frames=20, show_locals=False)




	parser = argparse.ArgumentParser(description=""+APP_NAME+" CLI")
	parser.add_argument("--run", action='store_true')
	parser.add_argument("--test", action='store_true')
	parser.add_argument('--module', action='store', type=str, required=False)
	parser.add_argument('--options', action='store', type=str, required=False)
	#args, leftovers = parser.parse_known_args()
	args = parser.parse_args()



	print(BLUE + banner.header + "                        \n" + END)


	moduleList = ""
	i = 0
	for module in cli.allModules:
		i += 1
		##if i%7 == 0:
		#	moduleList += "\n"
		moduleList = moduleList + YELLOW + module[0] +"  " + BLUE + module[1]+"\n "

	moduleList = moduleList[:-2]
	print(GREEN + "Loaded modules: " + "\n "+moduleList + "\n")

	if args.test:
		print("Test build detected. Exiting...")
		exit()
	if args.module:
		print(args.module)
		cli.commandHandler('use '+args.module)
	if args.options:

		for op in args.options.split(';'):
			time.sleep(0.1)
			cli.commandHandler(op)

	if args.run:
		cli.commandHandler('run')

	while True:
		if cli.inModule:
			inputHeader = BLUE + APP_NAME + RED + "/" + cli.currentModule + BLUE + " $> " + END
		else:
			inputHeader = BLUE + APP_NAME+" $> " + END

		try:
			cli.commandHandler(input(inputHeader))
		except KeyboardInterrupt:
			print(GREEN + "\n[I] Shutting down..." + END)
			raise SystemExit
		except Exception as e:
			print(RED + "\n[!] "+APP_NAME+" crashed...\n[!] Debug info: \n")
			#print(traceback.format_exc())
			console.print_exception(max_frames=20, show_locals=False)
			print("\n" + END)
			exit()

cli()