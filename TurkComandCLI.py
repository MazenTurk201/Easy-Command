from os import path,getcwd,system,name
from sys import argv
from winreg import OpenKey,HKEY_LOCAL_MACHINE,KEY_WRITE,SetValueEx,REG_SZ,CloseKey

def windowso(command, arg):
    cmd_file_path = path.expanduser("~\\aliass.bat")
    
    if path.isfile(cmd_file_path):
        with open(cmd_file_path, "a") as file:
            file.write(f"doskey {command}={arg} $*\n")
    else:
        with open(cmd_file_path, "a") as file:
            file.write(f"@echo off\ndoskey {command}={arg} $*\n")
        try:
            reg_key = OpenKey(HKEY_LOCAL_MACHINE,"Software\\Microsoft\\Command Processor",0,KEY_WRITE,)
            SetValueEx(reg_key, "AutoRun", 0, REG_SZ, cmd_file_path)
            CloseKey(reg_key)
            print(f"Successfully made doskey macros permanent. File created at: {cmd_file_path}")
        except Exception as e:print(f"Failed to modify the registry: {e}")  

def filedef(filee):
    import fileinput
    file = fileinput.input(filee)
    cmdlist = []
    arglist = []
    for i,line in enumerate(file, start=1):
        if i % 2 == 0:
            arglist.append(line.strip())
        else:
            cmdlist.append(line.strip())
    try:
        for i in range(len(cmdlist)):
            if name == "nt":
                windowso(cmdlist[i],arglist[i])
            elif name == "posix":
                system(f"echo 'alias {cmdlist[i]}={arglist[i]}' >> ~/.bashrc")   # or ~/.zshrc for Zsh users
                system("source ~/.bashrc")
    except:pass

def helpp():
    print(f'''
 Help Menu
Usage:
  python TurkComandCLI.py                         Loop.
  python TurkComandCLI.py -h                      Help Menu (This Page).
  python TurkComandCLI.py "command" "argument"    Run a command with an argument.
  python TurkComandCLI.py argument.txt            Run a list with an argument.
Example:
  python TurkComandCLI.py lnk "python 'TurkComandCLI.py'"
''')

def loopp():
    while True:
        try:
            print("Enter Command (or 'exit' to quit): ", end="")
            command = input()
            print("Enter Arg (or 'exit' to quit): ", end="")
            arg = input()
            if command == 'exit' or arg == 'exit':
                break
            elif command:
                if name == "nt":
                    # system(f"doskey {command}={arg}")
                    windowso(command, arg)
                elif name == "posix":
                    system(f"echo 'alias {command}={arg}' >> ~/.bashrc")   # or ~/.zshrc for Zsh users
                    system("source ~/.bashrc")
            print("--------------")
        except:pass

try:
    if path.isfile(path.join(getcwd(),argv[1])):
        filedef(argv[1])
    elif argv[1] == '--help' or argv[1] == '-h':
        helpp()
    elif argv[1] and argv[2] is not None:
        if name == "nt":
            # system(f"doskey {argv[1]}={argv[2]}")
            windowso(argv[1], argv[2])
        elif name == "posix":
            system(f"echo 'alias {argv[1]}={argv[2]}' >> ~/.bashrc")   # or ~/.zshrc for Zsh users
            system("source ~/.bashrc")
    else:helpp()
except:loopp()
