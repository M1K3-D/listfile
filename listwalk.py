import os
import shutil
import tkinter as tk
from tkinter import filedialog

from tkinter.filedialog import askdirectory
import unidecode

#import tkinter
#from tkinter import filedialog as fd
import tkinter.filedialog

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
        lb.pack()
        root.update()
        if dirname != newdirname:
            if not os.path.exists(newdirname):
                lb.insert('end', 'copy and delete ->' + newdirname)
                lb.pack()
                root.update()
#               print(dirname)
#               print('-', newdirname)
                shutil.copytree(dirname, newdirname, dirs_exist_ok=True)
                shutil.rmtree(dirname, ignore_errors=True)
            else:
                lb.insert('end', 'delete ->' + newdirname)
                shutil.rmtree(dirname, ignore_errors=True)







for path, dirs, files in os.walk(current_directory):
#    for dir in dirs:
        for file in files:
            filename = os.path.join(path, file)
            newfile = unidecode.unidecode(file)
            newfilename = os.path.join(path, newfile)
            lb.insert('end', filename)
            root.update()
            lb.pack()
            if filename != newfilename:
                lb.insert('end', 'rename->' + newfilename)
                lb.pack()
                root.update()
#               print(filename)
#               print('-', newfilename)
                try:
                    os.replace(filename, newfilename)
                except Exception as e:
                    lb.insert('end', str(e))
                
lb.insert('end', 'TERMINE')

root.mainloop()
