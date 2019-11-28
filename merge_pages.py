from tkinter.filedialog import  * 
from tkinter import *
import easygui,os
from tkinter import filedialog,messagebox
import PyPDF2,sys
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
ifile=""
inp_dir=""
def select_dir():       # to select a directory to save output PDF file

 global inp_dir
 inp_dir = filedialog.askdirectory()
 T2.insert(tk.END,inp_dir)
 messagebox.showinfo("Directory selected","Selected folder is '{0}'".format(inp_dir))

def select_PDF():  # to select input PDF from which we extract required page nos

 global ifile
 ifile = easygui.fileopenbox()
 with open(ifile,mode="rb") as f:
    r = PyPDF2.PdfFileReader(f).isEncrypted
 if r == True:
      messagebox.showerror("Error","PDF is already password protected\nYou cannot select encrypted PDF \nPlease decrypt it first")
 else:
  if(ifile.endswith(".pdf")):
   inp_file = open(ifile, 'rb') 
   pdfreader = PdfFileReader(inp_file)
   numpages = pdfreader.numPages
   T1.insert(tk.END,ifile)
   messagebox.showinfo("File selected","PDF file is '{0}' with '{1}' pages".format(ifile,numpages))
  else:
   messagebox.showerror("File Error-> Not PDF","Please select only PDF file")

def split_pdf(): # actual code to create new PDF with required pages
 flag = 0
 if ifile == "" or inp_dir=="":
  messagebox.showerror("ERROR","Please select PDF file and folder first")
 else:
  text = textBox1.get("1.0", 'end-1c')
  output_file = textBox2.get("1.0",'end-1c')  # extract name of output file
  print("page no text is '{0}'\noutput file name is '{1}'".format(text,output_file))
  if text == "" or output_file == "":
   messagebox.showerror("ERROR","Please enter page nos or output PDF name properly")
  else:
   nos = text.split(",")
   page_nos = []

   for i in range(len(nos)):   # if pages are entered in (a-b) format
    if re.search(r'-',nos[i]):
      x = nos[i].split('-')
      if int(x[0]) >= int(x[1]):  # in (a-b) format if b>a
        flag=1                    # to ensure if page nos are entered properly
        break
      else:
       for j in range(int(x[0]),int(x[1])+1): # get pages from a to b in (a-b) format
         page_nos.append(j)
    else:
      page_nos.append(int(nos[i]))   # append single pages

   print("page_nos are " ,len(page_nos))
   if os.path.exists(os.path.join(inp_dir,output_file)): # if output file already exists
    messagebox.showerror("ERROR","'{0}' already exists in '{1}'\nPlease change file name".format(output_file,inp_dir))

   else:               # if output PDF doesn't exist
    if flag == 0 and output_file.endswith(".pdf"):
     with open(ifile, 'rb') as inp_file, open(os.path.join(inp_dir,output_file), 'wb') as out_file:
      print("out file is ", out_file)
      reader = PdfFileReader(inp_file)
      writer = PdfFileWriter()

      for i in page_nos:      # adding each page to new output PDF
        if i in range(0,reader.getNumPages()):
          writer.addPage(reader.getPage(i))
      writer.write(out_file)

     inp_file.close()
     out_file.close()
     messagebox.showinfo("PDF created","PDF file is '{0}' with '{1}' pages".format(out_file,len(page_nos)))
    else:
     messagebox.showerror("ERROR","Please enter pages range properly (or) End your file with '.pdf'")

root=Tk()
root.title("Merge Selected pages of a PDF to create a new PDF")
def close_window():
 root.destroy()
l1 = Label(root,text="PDF file")
l1.place(x=20,y=30)
T1 = Entry(root, width = 30)
T1.place(x=100,y=25)
T1.insert(tk.END,ifile)
button1 = Button(root, text="Select PDF",fg="Red",font="Times", command=select_PDF)
button1.place(x=360,y=23)   # to select input PDF file(.pdf only)

l2 = Label(root,text="Choose output directory for PDF file to be saved")
l2.place(x=20,y=70)         # to choose a directory
T2 = Entry(root, width = 30)
T2.place(x=20,y=90)
T2.insert(tk.END,inp_dir)
button2 = Button(root, text="Select folder",fg="Red",font="Times", command=select_dir)
button2.place(x=360,y=90)

l1 = Label(root,text="Enter page nos to extract (12,23 (or) 34-65) format and page no starts from 0 in input PDF")
l1.place(x=20,y=130)

textBox1=Text(root ,height=2, width=30)
textBox1.place(x=20,y=160)  # to enter page nos

l2 = Label(root,text="Type a new PDF file name to be saved(.pdf only)")
l2.place(x=20,y=210)

textBox2=Text(root ,height=2, width=25)
textBox2.place(x=20,y=240)   # to enter output file name (only .PDF file)
global out_file

buttonok=Button(root, height=1, width=10, text="proceed",fg="green",font="Verdana 15 bold",command=lambda: split_pdf())   # to create a new PDF with required pages
buttonok.place(x=360,y=260)

buttonclose = Button(root, text="Close",fg="red", command=close_window)
buttonclose.pack(side = "bottom") # to close application

root.geometry("660x500")
root.mainloop()
