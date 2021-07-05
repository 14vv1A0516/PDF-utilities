from tkinter import *
import easygui,os
#import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter import messagebox
import tkinter as tk
ifile = ""

def select_PDF():
 global ifile
 ifile = easygui.fileopenbox()
 if(ifile.endswith(".pdf")):
  messagebox.showinfo("File selected","PDF file is '{0}'".format(ifile))
  T1.insert(tk.END,ifile)
  global inp_dir
  inp_dir = os.path.dirname(ifile)
  with open(ifile,mode="rb") as f:
    r = PyPDF2.PdfFileReader(f).isEncrypted
    if r == True:
      messagebox.showerror("Error","PDF is already password protected\nPlease select another PDF")
 else:
   messagebox.showerror("File Error-> Not PDF","Please select only PDF file")

def retrieve():
 if ifile == "":
  messagebox.showerror("Error", "Please select PDF first ")
 else:
  global user_pwd, owner_pwd
  owner_pwd=textBox1.get("1.0","end-1c")
  user_pwd=textBox2.get("1.0","end-1c")
  if owner_pwd == "" or user_pwd == "":
   messagebox.showerror("Warning","Please enter both passwords")
  else:
   encrypt_pdf(ifile,owner_pwd,user_pwd)

def encrypt_pdf(input_file, owner_pass, user_pass):  # encrypts selected PDF and no new file created
    output = PyPDF2.PdfFileWriter()
    input_stream = PyPDF2.PdfFileReader(open(input_file, "rb"))
    for i in range(0, input_stream.getNumPages()):
        output.addPage(input_stream.getPage(i))
    output_file = os.path.join(inp_dir,"temp.pdf")
    outputStream = open(output_file, "wb")   # Set user and owner password to pdf file
    output.encrypt(user_pass, owner_pass, use_128bit=True)
    output.write(outputStream)
    outputStream.close()
    os.rename(output_file, input_file)
    messagebox.showinfo("Encryption Done","Encrypted PDF file is '{0}'".format(input_file))
     
root=Tk()
root.title("Assign Owner and User passwords to a PDF")
def close_window():
 root.destroy()
l1 = Label(root,text="PDF file")
l1.place(x=20,y=30)
T1 = Entry(root, width = 30)
T1.place(x=130,y=25)
T1.insert(tk.END,ifile)
button1 = Button(root, text="Select PDF",fg="Red",font="Times", command=select_PDF)
button1.place(x=360,y=23)

l1 = Label(root,text="Enter Owner password")
l1.place(x=20,y=70)
textBox1=Text(root , height=2, width=20)
textBox1.place(x=180,y=70)

l2 = Label(root,text="Enter User password")
l2.place(x=20,y=110)
textBox2=Text(root ,height=2, width=20)
textBox2.place(x=180,y=110)

buttonok=Button(root, height=1, width=10, text="Encrypt PDF",fg="green",font="Verdana 15 bold",command=lambda: retrieve())
buttonok.place(x=350,y=240)
buttonclose = Button(root, text="Close",fg="red",font="Times", command=close_window)
buttonclose.pack(side = "bottom") # to close application
root.geometry("500x500")
mainloop()
