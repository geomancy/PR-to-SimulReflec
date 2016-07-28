from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
from os import path
from tkinter import messagebox
import csv

def About () :
	messagebox.showinfo("About", "Written by Daniel Hey - drh981@uowmail.edu.au")
	return

def BrowseFile1 () :
	Tk().withdraw()
	file = (askopenfilename(filetypes=[('DAT files', '.DAT')]))
	reflec_plus.delete(0,END)
	reflec_plus.insert(0, file)
	ReadyCheck()
	return

	
def BrowseFile2 () :
	Tk().withdraw() 
	file = (askopenfilename(filetypes=[('DAT files', '.DAT')]))
	reflec_minus.delete(0,END)
	reflec_minus.insert(0, file)
	ReadyCheck()
	return
	
def ReadyCheck () :
	if ('.dat' in reflec_minus.get()) and ('.dat' in reflec_plus.get()):
		mergeb.configure(bg="green")
		Comment.delete(0,END)
		Comment.insert(0,'R+: ' + path.split(reflec_plus.get())[1] + ', R-: ' + path.split(reflec_minus.get())[1])
	else:
		mergeb.configure(bg="red")
	return

	
def mergeFiles () :
	if (y in reflec_minus.get()) and (y in reflec_plus.get()):
		Tk().withdraw()
		file_out = asksaveasfilename(defaultextension=".txt", filetypes=[('Text files', '.txt')])
		#FILE 1
		Q = []
		R_plus = []
		with open(reflec_plus.get()) as f:
			reader = csv.reader(f, delimiter='\t')
			next(f)
			for row in reader:
				Q.append(round(float(row[0])*10, (no_dp.get())))
				R_plus.append(float(row[1]))
		f.close()
		
		#FILE 2
		R_minus = []
		with open(reflec_minus.get()) as f:
			reader = csv.reader(f, delimiter='\t')
			next(f)
			for row in reader:
				R_minus.append(float(row[1]))
		f.close()
		test = zip(Q,R_plus,R_minus)

		#write
		with open(file_out, 'w') as output:
			writing = csv.writer(output, delimiter='\t')
			writing.writerow(['# Comment = ' + Comment.get()])
			writing.writerow([PART.get()])
			writing.writerow([POL.get()])
			writing.writerow([ABS.get()])
			writing.writerow([TOF.get()])
			for row in test:
				writing.writerow(row) 
		output.close()
		messagebox.showinfo("Completed!", "Jolly good")
	else:
		messagebox.showwarning("Error", "Select files for merging")
	return
	
'''
	GUI SETUP
'''
y = '.dat'
window = Tk()
window.wm_title("PR to SimulReflec")
window.resizable(width=False, height=False)

menubar = Menu(window)
menubar.add_command(label="About", command=About)
menubar.add_command(label="Quit", command=window.quit)

window.config(menu=menubar)

''' FRAME 1 '''
frame1 = Frame(window)
frame1.pack(fill=BOTH)


Label(frame1, text="+Refl.").grid(row=0, column=0)
reflec_plus = Entry(frame1)
reflec_plus.grid(row=0, column=1)


Label(frame1, text="-Refl.").grid(row=1, column=0)
file2Var= StringVar()
reflec_minus= Entry(frame1)
reflec_minus.grid(row=1, column=1)

b1 = Button(frame1,text="Browse",command=BrowseFile1, padx=5, pady=5).grid(row=0, column=2)
b2 = Button(frame1,text="Browse",command=BrowseFile2, padx=5, pady=5).grid(row=1, column=2)


''' FRAME 2 '''
frame2 = Frame(window)
frame2.pack()

#comments
v = StringVar()
Label(frame2, text="Comment:").grid(row=0, column=0, sticky=W)
Comment = Entry(frame2)
Comment.grid(row=0, column=1, sticky=N+E+S+W, columnspan=2)

#particles
Label(frame2, text="Particles:").grid(row=1, column=0, sticky=W)
PART = StringVar()
PART.set('# Particles = neutrons')
Radiobutton(frame2, text="Neutrons", variable=PART, value='# Particles = neutrons').grid(row=1,column=1, sticky=W)
Radiobutton(frame2, text="X-Rays", variable=PART, value='# Particles = x-rays').grid(row=1,column=2, sticky=W)

#polarisation
Label(frame2, text="Polarised?").grid(row=2, column=0, sticky=W)
POL = StringVar()
POL.set('# Polarisation = polarised')
Radiobutton(frame2, text="True", variable=POL, value='# Polarisation = polarised').grid(row=2,column=1, sticky=W)
Radiobutton(frame2, text="False", variable=POL, value='# Polarisation = non polarised').grid(row=2,column=2, sticky=W)

#abscisses
Label(frame2, text="Abscisses:").grid(row=3, column=0, sticky=W)
ABS = StringVar()
ABS.set('# Abscisses = nm-1')
Radiobutton(frame2, text="Degrees", variable=ABS, value='# Abscisses = deg').grid(row=3,column=1, sticky=W)
Radiobutton(frame2, text="nm^-1", variable=ABS, value='# Abscisses = nm-1').grid(row=3,column=2, sticky=W)

#TOF
Label(frame2, text="Time of flight:").grid(row=4, column=0, sticky=W)
TOF = StringVar()
TOF.set('# TimeOfFlight = False')
Radiobutton(frame2, text="True", variable=TOF, value='# TimeOfFlight = True').grid(row=4,column=1, sticky=W)
Radiobutton(frame2, text="False", variable=TOF, value='# TimeOfFlight = False').grid(row=4,column=2, sticky=W)

#Truncation
frame3 = Frame(window)
frame3.pack(fill=BOTH)
Label(frame3, text="Decimal places (Q)").grid(row=0, column=0, sticky=W)
no_dp = IntVar()
no_dp.set(5)
drop = OptionMenu(frame3,no_dp,1,2,3,4,5,6,7,8,9,10)
drop.grid(row=0, column=1, columnspan=2)

''' FRAME 3 '''
frame4 = Frame(window)
frame4.pack(fill=BOTH)
mergeb = Button(frame4,text="Merge",command=mergeFiles,bg='red')
mergeb.pack(fill=BOTH,expand=5, padx=5, pady=5)

window.protocol("WM_DELETE_WINDOW", window.quit)
window.mainloop() 
