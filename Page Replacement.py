from tkinter import *
from tkinter import messagebox
import re
import copy

root = Tk()
root.resizable(False,False)
root.title('Page Replacement Simulator')
root.geometry("1000x450")
faultlabel = Label()
faultnum = Label()
pages = [' ']
page = 0
faultpages = 0
comparative = [["FIFO",' '],["LRU",' '],["Optimal",' ']]
fiforun = 0
lrurun = 0
oprun = 0
c = 0
 
#----------------------FUNCTIONS PART ----------------------------------#

def showtable(data,ref):
	for z in range(len(pages)):
		Label(frame3,text=pages[z],width=9,font=("Century Gothic",9,"bold"),bg="#2A425A",fg="white").grid(row=z,column=0)
	for i in range(len(ref)-1):
		Label(frame3,text=ref[i],width=5,font=("Century Gothic",12,"bold"),bg="#2A425A",fg="white",pady=7).grid(row=0,column=i+1)
	Label(frame3,text=ref[len(ref)-1],width=8,font=("Century Gothic",12,"bold"),bg="#2A425A",fg="white").grid(row=0,column=len(ref))
	for x in range(page+1):
		for y in range(len(ref)):
			Label(frame3,text=data[x][y],width=5,font=("Century Gothic",10),bg="#2A425A",fg="white").grid(row=x+1,column=y+1)

def FIFO(referencestring):
	global faultpages,fiforun
	data = []
	finalqueue = []
	queue= []
	current = 0
	isPageFault = []
	count = 0
	for y in range(page):
		queue.append(' ')

	for i in range(len(referencestring)):
		if (referencestring[i] not in queue):						
			isPageFault.append("PF")								
			if (count<page):
				queue[count] = referencestring[i]
				count+=1
			else:
				queue[current] = referencestring[i]
				current+=1
				if(current==page):
					current=0
			faultpages+=1
		else:
			isPageFault.append("✓")
		q = copy.deepcopy(queue)
		finalqueue.append(q)
	for q in range(len(finalqueue)):
		finalqueue[q].append(isPageFault[q])
	for a in range(page+1):
		data.append([])
		for x in range(len(referencestring)):
			data[a].append(finalqueue[x][a])
	for b in range(page):
		data[b].append(" ")
	data[page].append(faultpages)
	spareref = copy.deepcopy(referencestring)
	spareref.append("Total PF")
	showtable(data,spareref)
	if(fiforun==0):
		comparative[0][1] = faultpages
	fiforun = 1
			
def LRU(referencestring):
	global faultpages,lrurun
	data = []
	finalqueue = []
	queue= []
	current = 0
	toChange = []
	isPageFault = []
	spare = []
	count = 0
	for y in range(page):
		queue.append(' ')
		spare.append(' ')
	for i in range(len(referencestring)):
		if (referencestring[i] not in queue):						
			isPageFault.append("PF")								
			if (count<page):
				queue[count] = referencestring[i]
				spare[count] = referencestring[i]
				count+=1
			else:
				toChange = spare.pop(0)
				spare.append(referencestring[i])
				queue[queue.index(toChange)] = referencestring[i]
			faultpages+=1
		else:
			isPageFault.append("✓")
			spare.remove(referencestring[i])
			spare.append(referencestring[i])

		q = copy.deepcopy(queue)
		finalqueue.append(q)
	for q in range(len(finalqueue)):
		finalqueue[q].append(isPageFault[q])
	for a in range(page+1):
		data.append([])
		for x in range(len(referencestring)):
			data[a].append(finalqueue[x][a])
	for b in range(page):
		data[b].append(" ")
	data[page].append(faultpages)
	spareref = copy.deepcopy(referencestring)
	spareref.append("Total PF")
	showtable(data,spareref)
	if(lrurun==0):
		comparative[1][1] = faultpages
	lrurun	= 1	

def Optimal(referencestring):
	global faultpages,oprun
	data = []
	finalqueue = []
	queue= []
	current = 0
	toChange = []
	sortedHigher = []
	isPageFault = []
	spare = []
	count = 0
	for y in range(page):
		queue.append(' ')
	occurance = [None for i in range(page)]
	for i in range(len(referencestring)):
		if (referencestring[i] not in queue):						
			isPageFault.append("PF")								
			if (count<page):
				queue[count] = referencestring[i]
				count+=1
			else:
				for x in range(len(queue)):
					if(queue[x] not in referencestring[i+1:]):
						queue[x] = referencestring[i]
						break
					else:
						occurance[x] = referencestring[i+1:].index(queue[x])
				else:
					queue[occurance.index(max(occurance))] = referencestring[i]
			faultpages+=1
		else:
			isPageFault.append("✓")

		q = copy.deepcopy(queue)
		finalqueue.append(q)
	for q in range(len(finalqueue)):
		finalqueue[q].append(isPageFault[q])
	for a in range(page+1):
		data.append([])
		for x in range(len(referencestring)):
			data[a].append(finalqueue[x][a])
	for b in range(page):
		data[b].append(" ")
	data[page].append(faultpages)
	spareref = copy.deepcopy(referencestring)
	spareref.append("Total PF")
	showtable(data,spareref)
	if(oprun==0):
		comparative[2][1] = faultpages
	oprun = 1

def onClick():
	global pages,page,frame3,faultpages,refstring,numpage,algoFIFO,algoLRU,comparative,title,c
	s = str(faultpages)


	ref = refstring.get()
	hold = numpage.get()
	if(ref == '' and hold == ''):
		messagebox.showinfo("Error","Data must be not null")
		resetButton()
		return
	if(ref ==''):
		messagebox.showinfo("Error","Reference string must be not null")
		resetButton()
		return
	else:
		ref = re.split(',| ',ref)
		for i in range(len(ref)):
			ref[i] = int(ref[i])
		if(len(ref)<10 or len(ref)>15):
			messagebox.showinfo("Error","Reference string must be 10-15")
			resetButton()
			return
	if(hold ==''):
		messagebox.showinfo("Error","Page number must be not null")
		resetButton()
		return
	else:
		page = int(hold)
		if (page<2 or page>4):
			messagebox.showinfo("Error","Page number must be 2-4")
			resetButton()
			return

	frame3.destroy()
	frame3 = Frame(mainframe,height=35, width=950,bg="#2A425A",highlightbackground="white", highlightthickness=1)
	frame3.place(x=30,y=250)
		
	if(c == 0):
		for i in range(page):
			pages.append('Frame '+str((i+1)))
		c = 1

	if(clicked.get()=="FIFO"):
		FIFO(ref)
		title.config(font=("Century Gothic",12,"bold"),text="First In, First Out simulation result: ",bg="#2A425A",fg="white")
	elif(clicked.get()=="LRU"):
		LRU(ref)
		title.config(font=("Century Gothic",12,"bold"),text="Least Recently Used simulation result: ",bg="#2A425A",fg="white")
	elif(clicked.get()=="Optimal"):
		Optimal(ref)
		title.config(font=("Century Gothic",12,"bold"),text="Optimal Page Replacement simulation result: ",bg="#2A425A",fg="white")

	title.place(x=39,y=235)
	showComparativetable()
	faultpages = 0
	refstring.config(state='disabled')
	numpage.config(state='disabled')

def resetButton():
	global refstring,numpage,frame3,faultlabel,faultnum,frame4,fifofault,lrufault,comparative,lrurun,fiforun,title,c,pages,oprun
	comparative = [["FIFO",' '],["LRU",' '],["Optimal",' ']]
	faultnum.destroy()
	frame3.destroy()
	c = 0
	pages = [' ']
	fifofault.config(font=("Century Gothic",12),text=comparative[0][1],bg="#2A425A",fg="white")
	fifofault.grid(row=1,column=1)
	lrufault.config(font=("Century Gothic",12),text=comparative[1][1],bg="#2A425A",fg="white")
	lrufault.grid(row=2,column=1)
	opfault.config(font=("Century Gothic",12),text=comparative[2][1],bg="#2A425A",fg="white")
	opfault.grid(row=3,column=1)
	refstring.config(state='normal')
	numpage.config(state='normal')
	refstring.delete(0,END)
	numpage.delete(0,END)
	algoFIFO.config(font=("Century Gothic",12),text=comparative[0][0])
	algoFIFO.grid(row=1,column=0)
	algoLRU .config(font=("Century Gothic",12),text=comparative[1][0])
	algoLRU .grid(row=2,column=0)
	algoOp .config(font=("Century Gothic",12),text=comparative[2][0])
	algoOp .grid(row=3,column=0)

	title.config(font=("Century Gothic",12,"bold"),text=" ",bg="#2A425A",fg="white")
	title.place(x=39,y=190)
	lrurun = 0
	fiforun = 0
	oprun = 0


def showComparativetable():
	if (comparative[0][1] != ' ' and comparative[1][1] != ' ' and comparative[2][1] != ' '):
		comparative.sort(key=lambda x:x[1])

	fifofault.config(font=("Century Gothic",12),text=comparative[0][1])
	fifofault.grid(row=1,column=1)
	lrufault.config(font=("Century Gothic",12),text=comparative[1][1])
	lrufault.grid(row=2,column=1)
	opfault.config(font=("Century Gothic",12),text=comparative[2][1])
	opfault.grid(row=3,column=1)

	algoFIFO.config(font=("Century Gothic",12),text=comparative[0][0])
	algoFIFO.grid(row=1,column=0)

	algoLRU .config(font=("Century Gothic",12),text=comparative[1][0])
	algoLRU .grid(row=2,column=0)

	algoOp .config(font=("Century Gothic",12),text=comparative[2][0])
	algoOp .grid(row=3,column=0)

#----------------------FRAME WIDGETS----------------------------------#
mainframe = Frame(root,height=450, width=1000,bg="#2A425A")
mainframe.pack()
frame1 = Frame(mainframe,padx=5,pady=5,height=100, width=360,highlightbackground="white", highlightthickness=1,bg="#2A425A")
frame1.place(x=79,y=69)

frame2 = Frame(mainframe,padx=5,pady=5,height=130, width=237,highlightbackground="white", highlightthickness=1,bg="#2A425A")
frame2.place(x=470,y=54)

frame3 = Frame(mainframe,height=35, width=850,bg="#2A425A")
frame3.place(x=30,y=240)

frame4 = Frame(mainframe,padx=5,pady=5,height=154, width=200,highlightbackground="white", highlightthickness=1,bg="#2A425A")
frame4.place(x=740,y=48)
#----------------------LABEL WIDGETS----------------------------------#

numpagelabel = Label(mainframe,text="Comparative table",bg="#2A425A",fg="white")
numpagelabel.config(font=("Century Gothic",13,"bold"))
numpagelabel.place(x=752,y=33)

datalabel = Label(mainframe,text="Data Entry",bg="#2A425A",fg="white")
datalabel.config(font=("Century Gothic",13,"bold"))
datalabel.place(x=100,y=55)

note = Label(mainframe,text="Note: Reference string must be separated by space or comma only",bg="#2A425A",fg="white")
note.config(font=("Century Gothic",8))
note.place(x=75,y=170)

refstringlabel = Label(frame1,text="Reference string:",bg="#2A425A",fg="white")
refstringlabel.config(font=("Century Gothic",10,"bold"))
refstringlabel.place(x=8,y=16)

numpagelabel = Label(frame1,text="Number of frames:",bg="#2A425A",fg="white")
numpagelabel.config(font=("Century Gothic",10,"bold"))
numpagelabel.place(x=8,y=50)

numpagelabel = Label(frame2,text="Choose an Algorithm",bg="#2A425A",fg="white")
numpagelabel.config(font=("Century Gothic",12,"bold"))
numpagelabel.place(x=30,y=0)

faultlabel = Label(frame4,bg="#2A425A",fg="white")
faultnum = Label(frame4,bg="#2A425A",fg="white")

whitespace = Label(frame4, font=("Century Gothic",12,"bold"),text = "Algo",pady=10,bg="#2A425A",fg="white")
whitespace.grid(row=0,column=0)	

algoFIFO = Label(frame4,padx=18,bg="#2A425A",fg="white")
algoFIFO.config(font=("Century Gothic",12),text=comparative[0][0],bg="#2A425A",fg="white")
algoFIFO.grid(row=1,column=0)

algoLRU = Label(frame4,bg="#2A425A",fg="white")
algoLRU .config(font=("Century Gothic",12),text=comparative[1][0],bg="#2A425A",fg="white")
algoLRU .grid(row=2,column=0)

algoOp = Label(frame4,bg="#2A425A",fg="white")
algoOp .config(font=("Century Gothic",12),text=comparative[2][0],bg="#2A425A",fg="white")
algoOp.grid(row=3,column=0)

faultlabel = Label(frame4,bg="#2A425A",fg="white")
faultlabel.config(font=("Century Gothic",12,"bold"),text="Page Faults",bg="#2A425A",fg="white")
faultlabel.grid(row=0,column=1)	

fifofault = Label(frame4,bg="#2A425A",fg="white")
lrufault = Label(frame4,bg="#2A425A",fg="white")
opfault = Label(frame4,bg="#2A425A",fg="white")
title = Label(root)
#----------------------BUTTON WIDGETS----------------------------------#
options = ["FIFO","LRU","Optimal"]
clicked = StringVar()
clicked.set("FIFO")
choices = OptionMenu(frame2,clicked,*options)
choices.config(width=7,highlightbackground="black",highlightthickness=1)
choices.place(x=70,y=32)


Displaybutton = Button(frame2, text="Simulate", command=lambda:[onClick()],fg="white",bg="#29B44A")
Displaybutton.config(font=("Century Gothic",9))
Displaybutton.place(x=55,y=70)


reset = Button(frame2, text="Reset", command=lambda:[resetButton()],fg="white",bg="#C24242")
reset.config(font=("Century Gothic",9))
reset.place(x=123,y=70)


#----------------------ENTRY WIDGETS----------------------------------#
refstring = Entry(frame1,width=30)
refstring.place(x=133, y=20)
numpage = Entry(frame1,width=5,justify='center')
numpage.place(x=140, y=52)

root.mainloop()