from os import path,system,name
from flet import *
from winreg import OpenKey,HKEY_LOCAL_MACHINE,KEY_WRITE,SetValueEx,REG_SZ,CloseKey
import ctypes
import sys
from functools import wraps





import requests
from webbrowser import open_new_tab as lnk
def check_update():
    with open('version.txt', 'r') as file:
        localVersion = file.read()

    url = "https://raw.githubusercontent.com/MazenTurk201/Easy-Command/refs/heads/main/version.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        text_content = response.text
        update = text_content.replace("\n", "")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the file: {e}")
    if localVersion < update:
    # if float(localVersion) < 1.2:
        print(f"New version available: {update}v. Please update your software.")
        lnk(f"https://github.com/MazenTurk201/Turk-Py-Converter/releases")
        # system(f"powershell -Command \"Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::MsgBox('New {update}v.', 'OkOnly,Information', 'Update Easy Command')\" ;; start https://github.com/MazenTurk201/Easy-Command/releases")
        exit()

def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
if check_internet_connection():
    check_update()
# input()














def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
run_as_admin()

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

def filedef(fileen):
    from fileinput import input as finput
    filee = finput(fileen)
    # print(filee)
    cmdlist = []
    arglist = []
    for i,line in enumerate(filee, start=1):
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


def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

    
# GUI part

@memoize
def main(page: Page):
    # Set the title of the app
    page.title = "Turk Commands"
    page.window.maximized = True

    # Add a text control to the page
    # page.add(txt)
    

    arg_input = TextField(label="Write Command")
    cmd_input = TextField(label="Write Argument")


    def dropdown_changed(e):
        selected_value = dropdownn.value
        if selected_value == "Inputs":
            page.clean()
            page.add(inputtss,)
        if selected_value == "File":
            page.clean()
            page.overlay.append(file_picker)
            txt.value = "Hello, User!"
            page.add(fileess)
        if selected_value == "Test Results":
            page.clean()
            txt.value = "THX for using PLZ Rate Us <3\""
            page.add(testresult,)
        page.update()

    dropdownn = Dropdown(
        label="Choose an option",
        options=[
            dropdown.Option("Inputs"),
            dropdown.Option("File"),
            dropdown.Option("Test Results"),
        ],
        on_change=dropdown_changed,
    )
    
    txt = Text(value="Hello, User!", color="blue", size=40,font_family="Consolas")

    def btnn(e):
        cmd = cmd_input.value
        arg = arg_input.value
        if "" in (arg,cmd):
            txt.value = "Type Commands PLZ!"
            page.update()
        else:
            txt.value = "Hello, User!"
            if name == "nt":
                windowso(cmd,arg)
            elif name == "posix":
                system(f"echo 'alias {cmd}={arg}' >> ~/.bashrc")   # or ~/.zshrc for Zsh users
                system("source ~/.bashrc")
            cmd_input.value = ""
            arg_input.value = ""
            page.update()
        
        
    btn = ElevatedButton(text="Click Me", on_click=btnn)

    def run_command(e):
        if name == "nt":
            system("start cmd")
        elif name == "posix":
            system("source ~/.bashrc")
    def about(e):
        from webbrowser import open_new_tab as lnk
        lnk("https://bit.ly/m/MazenTURK")

    run_button = ElevatedButton("Test Commands?", on_click=run_command)
    about_button = ElevatedButton("Us <3\"", on_click=about)

    # file_content = Text("No file selected", selectable=True)
    file_content = TextField(
        multiline=True, 
        read_only=True,
        width=600, 
        height=300,
        visible=False,
        label="No file selected",
    )
    listcommands=None
    btnfile = ElevatedButton(
        "Yes", 
        # on_click=filedef,
        on_click=lambda e: filedef(listcommands),
        # on_click=filedef(listcommands),
        visible=False,
    )
    # File picker instance
    file_picker = FilePicker(
        on_result=lambda e: read_file(e.files[0].path if e.files else None)
    )


    # Function to read and display file content
    def read_file(file_path):
        nonlocal listcommands
        listcommands=file_path
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content.value = f.read()
                file_content.label = "This List?"
                file_content.visible = True
                btnfile.visible = True
        else:
            file_content.value = "No file selected"
        page.update()

    # Button to open file picker (restrict to .txt files)
    browse_button = ElevatedButton(
        "Browse TXT File", 
        on_click=lambda e: file_picker.pick_files(allowed_extensions=["txt"])
    )

    inputtss = Row(
        [
            Column(
                [
                    txt,
                    Text(value="\n"),
                    Text(value="\n"),
                    dropdownn,
                    arg_input,
                    cmd_input,
                    btn,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        ],
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=CrossAxisAlignment.CENTER,
    )

    fileess = Row(
        [
            Column(
                [
                    txt,
                    Text(value="\n"),
                    Text(value="\n"),
                    dropdownn,
                    browse_button,
                    file_picker,
                    Row(controls=[file_content, btnfile]),
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        ],
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=CrossAxisAlignment.CENTER,
    )
    
    testresult = Row(
        [
            Column(
                [
                    txt,
                    Text(value="\n"),
                    dropdownn,
                    run_button,
                    about_button,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        ],
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=CrossAxisAlignment.CENTER,
    )


    page.add(inputtss,)


if __name__ == "__main__":
    # app(target=main, view=WEB_BROWSER, port=80,)
    app(target=main)