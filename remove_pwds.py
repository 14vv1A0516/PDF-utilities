from tkinter import *
import easygui,os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter import messagebox
import tkinter as tk
ifile=""

def select_PDF():
 global ifile 
 ifile = easygui.fileopenbox()
 if ifile.endswith(".pdf"):
  messagebox.showinfo("File selected","PDF file is '{0}'".format(ifile))
  T1.insert(tk.END,ifile)
  global inp_dir
  inp_dir = os.path.dirname(ifile)
  with open(ifile,mode="rb") as f:
    r = PyPDF2.PdfFileReader(f).isEncrypted
    if r == False:
      messagebox.showerror("Error","PDF has no password to be removed")
 else:
   messagebox.showerror("File Error => Not PDF","Please select only PDF file")

def retrieve():
 if ifile == "":
  messagebox.showerror("Error", "Please select PDF first ")
 else: 
  global old_pwd
  old_pwd=textBox1.get("1.0","end-1c")
  decrypt_pdf(ifile, os.path.join(inp_dir,"temp.pdf"), old_pwd)

def decrypt_pdf(input_file, output_file, old_pwd):
  with open(input_file, 'rb') as inp_file, open(output_file, 'wb') as out_file:
    reader = PdfFileReader(inp_file)
    st = reader.decrypt(old_pwd)
    if st == 0:
     messagebox.showerror("Error","Entered PDF password is incorrect\nPlease enter correct password")
    else:
     writer = PdfFileWriter()
     for i in range(reader.getNumPages()):
       writer.addPage(reader.getPage(i))
     writer.write(out_file)
     inp_file.close()
     out_file.close()
     os.rename(output_file,input_file)
     messagebox.showinfo("Password Removed","Decrypted PDF file is '{0}'".format(input_file))

root=Tk()
root.title("Remove password from a PDF")
def close_window():
 root.destroy()
l1 = Label(root,text="PDF file")
l1.place(x=20,y=30)
T1 = Entry(root, width = 30)
T1.place(x=120,y=25)
T1.insert(tk.END,ifile)
button1 = Button(root, text="Select PDF",fg="Red",font="Times", command=select_PDF)
button1.place(x=370,y=23)

l1 = Label(root,text="Enter PDF password")
l1.place(x=20,y=70)
textBox1=Text(root , height=2, width=20)
textBox1.place(x=180,y=70)

buttonok=Button(root, height=1, width=10, text="Proceed",fg="green",font="Verdana 15 bold",command=lambda: retrieve())
buttonok.place(x=320,y=240)
buttonclose = Button(root, text="Close",fg="red",font="Times", command=close_window)
buttonclose.pack(side = "bottom") # to close application
root.geometry("500x400")
mainloop()
