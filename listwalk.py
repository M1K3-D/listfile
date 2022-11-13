import os
import shutil
import tkinter as tk
from tkinter import filedialog
#from tkinter.filedialog import askdirectory
import unidecode
#import tkinter
#from tkinter import filedialog as fd
#import tkinter.filedialog

root = tk.Tk()
root.title("SUPPRESSION ACCENTS RECURSIF")
root.geometry('1000x800')
# root.withdraw()
lb = tk.Listbox(root)
lb.pack(expand=tk.YES, fill=tk.BOTH)
current_directory = tk.filedialog.askdirectory(parent=root)


# file_path = os.path.join(current_directory,file_name)
# print(file_path)

# home_folder = os.path.expanduser('~')
for path, dirs, files in os.walk(current_directory):
    for dir in dirs:
        dirname = os.path.join(path, dir)
        newdir = unidecode.unidecode(dir)
        newdirname = os.path.join(path, newdir)
        lb.insert('end', dirname)
        if dirname != newdirname:
            if not os.path.exists(newdirname):
                lb.insert('end', '->' + newdirname)
#               print(dirname)
#               print('-', newdirname)
                shutil.copytree(dirname, newdirname, dirs_exist_ok=True)

for path, dirs, files in os.walk(current_directory):
    for file in files:
        filename = os.path.join(path, file)
        newfile = unidecode.unidecode(file)
        newfilename = os.path.join(path, newfile)
        lb.insert('end', filename)
        if filename != newfilename:
            lb.insert('end', '->' + newfilename)
#           print(filename)
#           print('-', newfilename)
            os.replace(filename, newfilename)
root.mainloop()
