from tkinter import *
import easygui,os
from tkinter import messagebox
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk

ifile=""
def select_PDF():
 global ifile,inp_dir
 ifile = easygui.fileopenbox()
 if ifile.endswith(".pdf"):
  inp_dir = os.path.dirname(ifile)
  T1.insert(tk.END,ifile)
  messagebox.showinfo("File selected","PDF file is '{0}'".format(ifile))
  with open(ifile,mode="rb") as f:
   r = PyPDF2.PdfFileReader(f).isEncrypted
   if r == False:
      messagebox.showerror("Error","PDF has no password")
 else:
   messagebox.showerror("File Error-> Not PDF","Please select only PDF file")

def change_pwd():
 if ifile == "":
  messagebox.showerror("Error", "Please select PDF first ")
 else:
  print("Inp_File is '{0}'".format(ifile))
  global old_pwd
  old_pwd = textBox1.get("1.0","end-1c")
  global new_pwd1
  new_pwd1 = textBox2.get("1.0","end-1c")
  global new_pwd2
  new_pwd2 = textBox3.get("1.0","end-1c")
  if new_pwd1 != new_pwd2:
    messagebox.showerror("Error","New passwords don't match")
  else:
   with open(ifile, 'rb') as inp_file:   
     reader = PdfFileReader(inp_file)
     st = reader.decrypt(old_pwd)
     if st == 0:
       messagebox.showerror("Error","Old PDF's password is incorrect")
     else:
       writer = PdfFileWriter()
       for i in range(reader.getNumPages()):
          writer.addPage(reader.getPage(i))
       outputstream = open(os.path.join(inp_dir,"temp.pdf"),'wb')
       writer.encrypt(new_pwd2, use_128bit=True)
       writer.write(outputstream)
       outputstream.close()
       os.rename(os.path.join(inp_dir,"temp.pdf"), ifile)
       messagebox.showinfo("Password Changed","Password has been changed for '{0}'".format(ifile))

root=Tk()
root.title("Change password of a PDF")
def close_window():
 root.destroy()
l1 = Label(root,text="PDF file")
l1.place(x=20,y=30)
T1 = Entry(root, width = 30)
T1.place(x=130,y=25)
T1.insert(tk.END,ifile)
button1 = Button(root, text="Select PDF",fg="Red",font="Times", command=select_PDF)
button1.place(x=360,y=23)

l1 = Label(root,text="Enter Old password")
l1.place(x=20,y=75)
textBox1=Text(root , height=2, width=20)
textBox1.place(x=180,y=70)

l2 = Label(root,text="Enter New password")
l2.place(x=20,y=115)
textBox2=Text(root ,height=2, width=20)
textBox2.place(x=180,y=110)

l3 = Label(root,text="Re-enter New password again")
l3.place(x=20,y=155)
textBox3=Text(root ,height=2, width=20)
textBox3.place(x=180,y=150)
buttonok=Button(root, height=1, width=10, text="Proceed",fg="green",font="Verdana 15 bold",command=lambda: change_pwd())
buttonok.place(x=350,y=240)
buttonclose = Button(root, text="Close",fg="red",font="Times", command=close_window)
buttonclose.pack(side = "bottom") # to close application
root.geometry("500x500")
mainloop()
