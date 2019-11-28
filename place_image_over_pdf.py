import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import messagebox
import easygui,os,io
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

ifile = ""
img=""
inp_dir=""

def select_file():
 global ifile,T1,inp_dir
 ifile = easygui.fileopenbox()
 if ifile.endswith(".pdf"):
  inp_dir = os.path.dirname(ifile)
  T1.insert(tk.END,ifile)
  messagebox.showinfo("File created", "File selected is '{0}'".format(ifile))
 else:
  ifile=""
  messagebox.showerror("File Error => Not PDF", "Please select only PDF file")  

def select_image():
 global img,T2
 img = easygui.fileopenbox()
 if img.endswith(".png") or img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith(".gif"):
  T2.insert(tk.END,img)
  messagebox.showinfo("File selected", "File selected is '{0}'".format(img))
 else:
  img=""
  messagebox.showerror("File Error => Not Image", "Please select only Image file")  

def place_img():
 if ifile=="" or img=="":
  messagebox.showerror("Error", "Please select PDF and image file first")  
 else:
  x = textbox1.get("1.0","end-1c")
  y = textbox2.get("1.0","end-1c")
  height = textbox3.get("1.0","end-1c")
  width = textbox4.get("1.0","end-1c")
  ofile = textbox5.get("1.0","end-1c")
   
  if x == "" or y == "" or height == "" or width == "":
    messagebox.showerror("Error", "Please enter all dimensions properly")
  else:
   if ofile.endswith(".pdf"):
    imgsign = BytesIO()
    imgDoc = canvas.Canvas(imgsign)
    imgDoc.drawImage(img,int(x),int(y),int(width),int(height))
    imgDoc.save()

    packet  = io.BytesIO()
    can = canvas.Canvas(packet,pagesize=letter)
    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open(ifile,"rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    overlay1 = PdfFileReader(BytesIO(imgsign.getvalue())).getPage(0)
    page.mergePage(overlay1)
    output.addPage(page)
    ofile = os.path.join(inp_dir,ofile)
    outputstream = open(os.path.join(inp_dir,ofile),"wb")
    output.write(outputstream)
    outputstream.close()
    messagebox.showinfo("Image placed", "Image placed over file '{0}' successfully".format(ofile))
   else:
    messagebox.showerror("File Error => Not PDF", "Please add extension '.pdf'")  

root = Tk()
def close_window():
    root.destroy()
l1 = Label(root, text = "Input PDF ")
l1.place(x=20,y=30)
T1 = Entry(root, width = 30)
T1.place(x=130,y=30)
T1.insert(tk.END, ifile)
button1 = Button(root, text="Select PDF", fg="Red", command=select_file)
button1.place(x=420,y=23)

l2 = Label(root, text = "Input Image ")
l2.place(x=20,y=70)
T2 = Entry(root, width = 30)
T2.place(x=130,y=70)
T2.insert(tk.END, img)
button2 = Button(root, text="Select Image",fg="Red", command=select_image)
button2.place(x=420,y=63)

l2 = Label(root, text = "(jpg,png,jpeg,gif) ")
l2.place(x=20,y=90)

x = Label(root, text = "Enter PDF Coordinates: X")
x.place(x=20,y=110)
textbox1 = Text(root, height=2, width=6)
textbox1.place(x=200,y=105)

y = Label(root, text ="Y")
y.place(x=255,y=110)
textbox2 = Text(root, height=2, width=6)
textbox2.place(x=280,y=105)

height = Label(root, text = "Enter Image Coordinates: Height")
height.place(x=20,y=150)
textbox3 = Text(root, height=2, width=6)
textbox3.place(x=250,y=150)

width= Label(root, text = "Width")
width.place(x=310,y=150)
textbox4 = Text(root, height=2, width=6)
textbox4.place(x=350,y=150)

proceed = Button(root,height=1, width=10,text = “Proceed",fg="green",command=lambda:place_img())
proceed.place(x=420,y=240)

oufile = Label(root, text = "Enter Output PDF file name:")
oufile.place(x=20,y=200)
textbox5 = Text(root, height=2, width=20)
textbox5.place(x=215,y=200)
close = Button(root,height=1, width=10,text = "Close",fg="red",command=lambda:close_window())
close.pack(side = "bottom",padx=10,pady=20)
root.geometry("550x600")
root.mainloop()
