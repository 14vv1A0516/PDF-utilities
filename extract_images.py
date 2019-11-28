import PyPDF2,fitz,datetime,os,sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import messagebox
import tkinter as tk,easygui

ifile = ""
out_dir=""
pfile = ""

def select_dir():       # to select output directory to save png images
 global out_dir
 out_dir = filedialog.askdirectory()
 T2.insert(tk.END,out_dir)
 messagebox.showinfo("Directory selected","Selected folder is '{0}'".format(out_dir))

def select_PDF():     # select PDF file
 global ifile,T1
 ifile = easygui.fileopenbox()
 print("ifile is '{0}'".format(ifile))
 if ifile.endswith(".pdf"):
  T1.insert(tk.END,ifile)
 else:
  messagebox.showerror("File Error => Not PDF","Please select only PDF file")

def retrieve_images():
  if ifile == "" or out_dir == "":
    messagebox.showerror("Error","Please select PDF and output directory to save png files")
  else:
   pdfile = fitz.open(ifile)
   ct = 0
   for i in range(len(pdfile)):
    for image in pdfile.getPageImageList(i):
     j=0
     print(image)
     customxref = image[0]
     pic = fitz.Pixmap(pdfile,customxref)
     finalpic = fitz.Pixmap(fitz.csRGB,pic)
     finalpic.writePNG(str(os.path.join(out_dir,str(datetime.datetime.now()))+".png"))
     pic = None
     finalpic = None
     j = j + 1
     ct = ct + 1
   messagebox.showinfo("Images retrieved","No of images created are '{0}'".format(ct))

def select_PDF_for_img_in_PDF():
 global pfile,T3
 pfile = easygui.fileopenbox()
 print("Input PDF is '{0}'".format(pfile))
 if pfile.endswith(".pdf"):
  T3.insert(tk.END,pfile)
 else:
  messagebox.showerror("File Error-> Not PDF","Please select only PDF file")

def retrieve_images_into_pdf():
 if pfile == "": # or pfile.endswith(".pdf"):
  messagebox.showerror("File Error-> Not PDF","Please select PDF file")
 else:
  from pdfrw import PdfReader, PdfWriter
  from pdfrw.findobjs import page_per_xobj
  ofile = 'extract.' + os.path.basename(pfile)
  pages = list(page_per_xobj(PdfReader(pfile).pages, margin=0.5*72))
  if not pages:
     raise IndexError("No XObjects found")
  writer = PdfWriter(ofile)
  writer.addpages(pages)
  writer.write()
  messagebox.showinfo("Images retrieved","All images saved in '{0}'".format(ofile))
 
root = Tk()
root.title("Retrieve images as pngs")
def close_window():
    root.destroy()
l = Label(root, font="Verdana 15 bold",text = "To retrieve images as png files ")
l.place(x=20,y=20)
l1 = Label(root, text = "Input PDF ")
l1.place(x=20,y=60)
T1 = Entry(root, width = 30)
T1.place(x=130,y=60)
T1.insert(tk.END,ifile)
button1 = Button(root, text="Select PDF",fg="Red",font="Times", command=select_PDF)
button1.place(x=390,y=53)

l2 = Label(root, text = "Output folder ")
l2.place(x=20,y=100)
T2 = Entry(root, width = 30)
T2.place(x=130,y=100)
T2.insert(tk.END,out_dir)
button2 = Button(root, text="Select folder",fg="Red",font="Times", command=select_dir)
button2.place(x=390,y=93)

proceed = Button(root,height=1, width=10,text = "Proceed",fg="green",font="Verdana 15 bold",command=lambda:retrieve_images())
proceed.place(x=390,y=140)

l3 = Label(root, font="Verdana 15 bold", text = "To create a new PDF with all images of input PDF  ")
l3.place(x=20,y=200)

l4 = Label(root, text = "Input PDF ")
l4.place(x=20,y=250)
T3 = Entry(root, width = 30)
T3.place(x=130,y=250)
T3.insert(tk.END,pfile)
button1 = Button(root, text="Select PDF",fg="Red",font="Times", command=select_PDF_for_img_in_PDF)
button1.place(x=390,y=250)

proceed2 = Button(root,height=1, width=10,text = "Proceed",fg="green",font="Verdana 15 bold",command=lambda:retrieve_images_into_pdf())
proceed2.place(x=390,y=300)

close = Button(root,height=1, width=10,text = "Close",fg="red",font="Verdana 15 bold",command=lambda:close_window())
close.pack(side = "bottom",padx=10,pady=20)
root.geometry("610x500")
root.mainloop()
