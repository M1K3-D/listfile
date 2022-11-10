import os
import sys
import unidecode
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from pathlib import Path
from functools import partial

#from tabulate import tabulate

win = tk.Tk()
win.title("Suppression caracteres accentues".upper())
win.geometry("1000x1000")
Lsize = 0
cpt_lu = 0
cpt_tr = 0
# Universal Home
home_folder = os.path.expanduser('~')
homedrive = home_folder
rep_source = home_folder
selection = ""
r_record = []
#p_record = []
# Selection fichier et affichage nom dans la3

# print (sys.getfilesystemencoding())
def openfile(evt):
    #    pass
    w = evt.widget
# Pour ListBox    
#    index = int(w.curselection()[0])
#    value = w.get(index)
# Pour TreeView
    index = w.selection()[0]
    value = tr.set(index, column="c1")
    selection = value
    v_sel.set(selection)

# curItem = self.tree.item(self.tree.focus())
#     col = self.tree.identify_column(event.x)
#     print ('curItem = ', curItem)
#     print ('col = ', col)

#     if col == '#0':
#         cell_value = curItem['text']
#     elif col == '#1':
#         cell_value = curItem['values'][0]
#     elif col == '#2':
#         cell_value = curItem['values'][1]
#     elif col == '#3':
#         cell_value = curItem['values'][2]
#     print ('cell_value = ', cell_value)

def ask_question():
    global rep_source
    global cpt_lu
    global cpt_tr    
    v_go = True
    rep_source = tk.filedialog.askdirectory(
        parent=win, initialdir=rep_source, title="Selectionnez le dossier SOURCE")
    try:
        os.listdir(rep_source)
    except Exception as e:
        tk.messagebox.showinfo('Return', 'Traitement annulé', parent=win)
        v_go = False
    if v_go == True:
        v_trait = 'N'

        read_files()
        v_cpt.set(str(cpt_lu)+"/"+str(cpt_tr))
        win.update()
        if cpt_tr != 0:
            do_job()

def read_files():
    global rep_source
    global cpt_lu
    global cpt_tr
    lb.delete(0, tk.END)
    tr.delete(*tr.get_children())
    win.update()
    cpt_lu = 0
    cpt_tr = 0
    r_record.clear()

    for file in os.listdir(rep_source):
        fileDec = file
        fileDec = unidecode.unidecode(file)
        cpt_lu = cpt_lu + 1
        v_cpt.set(str(cpt_lu)+"/"+str(cpt_tr))
#       la1.config(text=str(cpt_lu)+"/"+str(cpt_tr))

        filePath = Path(rep_source)
        newFile = os.path.join(filePath , fileDec)
        oldFile = os.path.join(filePath , file)
        if os.path.isfile(oldFile) is True:
            v_type = 'F'
        if os.path.isdir(oldFile) is True:
            v_type = 'D'
        v_exist = 'N'
        if os.path.isfile(newFile) is True:
            v_exist = 'Y'
        if os.path.isdir(newFile) is True:
            v_exist = 'Y'
#        os.stat(newFile)    
#        v_trait = "N"

        if file == fileDec:
            v_trait = 'N'
            v_exist = ''
            fileDec=""
        else:
            # Si le repertoire existe, on traite ?
            if (v_type == "D" and v_exist == "Y"):
                    v_trait = '?'
            # Si le fichier existe, on traite 
            elif (v_type == "F" and v_exist == "Y"):
                v_trait = 'Y'
                    # lb.insert(1, "  "+"\t" + fileDec + "  " +
                    #   "\t" + v_type+"\t" + v_exist)
            else:
                v_trait = 'Y'
        r_record.append([file, fileDec, oldFile, newFile, v_type, v_exist, v_trait])

    for [file, fileDec, oldFile, newFile, v_type, v_exist,v_trait] in r_record:
        if (v_trait == 'Y' or v_trait == '?'):
            cpt_tr = cpt_tr+1
        tr.insert('', 'end', text="1", values=(file,fileDec ,v_type, v_exist,v_trait))

    win.update()
#   nb d'enreg dans la lb
    Lsize = lb.size()

def do_job():
    global rep_source
    msg_box = tk.messagebox.askquestion('Return', 'Validation des modifications ?',
                                        icon='warning', parent=win)
    if msg_box == 'yes':
        #       pass
        rename_files()
        tk.messagebox.showinfo('Return', 'Traitement terminé', parent=win)
    else:
        tk.messagebox.showinfo(
            'Return', 'Modifications non effectuées', parent=win)

def rename_files():
    global rep_source
    global cpt_lu
    global cpt_tr
    cpt_lu = 0
    cpt_tr = 0
    for [file, fileDec, oldFile, newFile, v_type, v_exist, v_trait] in r_record:
        # print(file, oldFile)
        cpt_lu = cpt_lu+1
        if (v_trait == 'Y'):
            pass
            # filePath = Path(rep_source)
            # newFile = filePath / fileDec
            # oldFile = filePath / file
            try:
                os.replace(oldFile, newFile)
#                shutil.move(oldFile, newFile)
                cpt_tr = cpt_tr+1
            except Exception as e:
                cpt_tr = cpt_tr-1
#                print(str(e))
                tk.messagebox.showinfo('Return', str(e), parent=win)
        if v_trait == '?':
            try:
#                os.copy(oldFile, newFile)
#                newFile = newFile+"zz" 
#                shutil.copy2(oldFile, newFile)
                shutil.copytree(oldFile, newFile, dirs_exist_ok=True)
                cpt_tr = cpt_tr+1
            except Exception as e:
                cpt_tr = cpt_tr-1
#                print(str(e))
                tk.messagebox.showinfo('Return', str(e), parent=win)

#   refresh
    read_files()
    v_cpt.set(str(cpt_lu)+"/"+str(cpt_tr))
#   la1.config(text=str(cpt_lu)+"/"+str(cpt_tr))


v_cpt = tk.StringVar(win, value=str(cpt_lu)+"/"+str(cpt_tr))
v_sel = tk.StringVar(win, value=selection)

# action_with_arg = partial(ask_question, rep_source)
# bt1 = tk.Button(win, text="Open a Directory", command=action_with_arg)
bt1 = tk.Button(win, text="Open a Directory", command = ask_question)
bt1.pack()
lb = tk.Listbox(win)
#lb.pack()
# expand=tk.YES, fill=tk.BOTH)
lb.bind("<<ListboxSelect>>", openfile)
tr = ttk.Treeview(win, column=("c1", "c2", "c3","c4","c5"), show='headings', height=20)
tr.heading('c1', text='Fichier')
tr.column('c1', minwidth=0, width=300)
tr.heading('c2', text='Nouveau Fichier')
tr.column('c2', minwidth=0, width=300)
tr.heading('c3', text='F/D')
tr.column('c3', minwidth=0, width=50)
tr.heading('c4', text='Exist')
tr.column('c4', minwidth=0, width=50)
tr.heading('c5', text='Traitement')
tr.column('c5', minwidth=0, width=50)
tr.pack(expand=tk.YES, fill=tk.BOTH)
tr.bind("<<TreeviewSelect>>", openfile)

# Utilisation de variable
#la1 = tk.Label(win,text=str(cpt_lu)+"/"+str(cpt_tr))
# la1.pack()
# Utilisation de tk.StringVar
la2 = tk.Label(win, textvariable=v_cpt)
la2.pack()
# Affichage de selection
la3 = tk.Label(win, textvariable=v_sel)
la3.pack()

win.mainloop()
