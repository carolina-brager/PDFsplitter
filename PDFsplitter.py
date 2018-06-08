#!/usr/local/bin/python
#
# PDFsplitter.py
#
# Carolina Brager
# 06/06/18
#


from Tkinter import *
from os.path import basename, abspath
import tkFileDialog
from PyPDF2 import PdfFileReader, PdfFileWriter

pdf_path = None #path for the pdf
pdf_filename = None #filename for the pdf

outdir = "" #stores the output directory of the pdf files

# Stores the filenames and pathnames into pathnames and filenames to be used when the run
# button is pressed.
def getFiles():
	global pdf_filename
	global pdf_path
	file = tkFileDialog.askopenfilename(parent=app,title='Choose a file',filetypes=[('pdf file','*.pdf')])

	pdf_path = abspath(file)
	pdf_filename = basename(abspath(file))

	print(pdf_filename)

def run():
	print("run")

	if(pdf_path is None):
		quantErr()
		return

	inputpdf = PdfFileReader(open(pdf_path, "rb"))
	temp = None
	splitted = None
	output = PdfFileWriter()

	for i in xrange(inputpdf.numPages):
		pageObj = inputpdf.getPage(i)
		text = pageObj.extractText()
		decoded = text.encode('ascii','replace')
		temp = splitted
		splitted = decoded.split('\n', 1)[0]

		print(splitted)
		if (splitted != temp and temp != None):
			with open("%s/%s.pdf" % (outdir, temp), "wb") as outputStream:
				output.write(outputStream)
				output = PdfFileWriter()

		output.addPage(inputpdf.getPage(i))


	with open("%s/%s.pdf" % (outdir, splitted), "wb") as outputStream:
		output.write(outputStream)
		output = PdfFileWriter()

	success()

#stores the otuput location of the svm.asconf file. If none is chosen, creates the svm.asconf file in the curretn directory.
def col():
	global outdir
	outdir = tkFileDialog.askdirectory(parent = app, title = 'Choose a location')
	print("Output location = " + outdir)

#clears the files from the listbox and from the filenames and pathnames lists
def clear():
	pdf_filename = None;
	pdf_path = None;
	errMsg.config(fg = "red")
	quote = "file cleared"
	errMsg.config(text = quote)
	errMsg.pack()


#Runs when not enough or too many files has been uploaded. Tells the user how many files they need
#to add or delete to get to the right number of files.
def quantErr():
	errMsg.config(fg = "red")
	quote = "You must upload a file"
	errMsg.config(text = quote)
	errMsg.pack()

# Runs when the program has run successfully. Prints "Command Executed" in green at the bottom
# and creates a message box that tells the user where the output file is.
def success():
	errMsg.config(fg = "forest green")
	quote = "Command Executed"
	errMsg.config(text = quote)
	errMsg.pack()



### Everything below this comment is layout information for the GUI of the program ###

app = Tk()
app.title("Terminal Program")
app.resizable(0,0)

w = 300
h = 230

ws = app.winfo_screenwidth()
hs = app.winfo_screenheight()

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

app.geometry('%dx%d+%d+%d' % (w, h , x, y))

frame1 = Frame(app)
frame2 = Frame(app, bg = 'snow2')
frame3 = Frame(app, bg = 'snow2')
frame5 = Frame(app)
miniframe = Frame(frame1)

getFiles = Button(master = frame2, text = "Select PDF", highlightbackground = 'snow2', command = getFiles)
COL = Button(master = frame5, text = "Choose Output Location", command = col)
RUN = Button(master = frame5, text = "RUN", command = run)
CLEAR = Button(master = frame5, text = "Clear File", command = clear)

errMsg = Message(frame3, text = "", bg = 'snow2', width = 500)
title = Label(miniframe, text = "PDF Splitter", font ="-size 30" )

frame1.pack(side = TOP, fill = X)
miniframe.pack(fill = Y)
title.pack(side = LEFT, padx = 10)

frame2.pack(fill = X, expand = True)
getFiles.pack(padx = 30, pady = 5)

frame3.pack(side = BOTTOM, fill = BOTH)
errMsg.pack()

frame5.pack(padx = 10)
CLEAR.pack(pady = 6)
COL.pack(pady = 6)
RUN.pack(pady = 6)

app.mainloop()
