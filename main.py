from asyncio.windows_events import NULL
from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import END,font as tkfont
from tkinter import messagebox,PhotoImage
from getpass import getpass
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
    )
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE Security")
mydb.connect(database = "Security")
mycursor.execute("CREATE TABLE Security(NAME VARCHAR(50), DATE_JOINING DATE, DEPARTMENT VARCHAR(50));")

names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
                
        self.title_font = tkfont.Font(family='Helvetica', size=33, weight="bold")
        self.title("Auth")
        self.resizable(False, False)
        self.geometry("535x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None

        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=2)
        container.grid_columnconfigure(0, weight=2)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Rendering image on frame
        render = PhotoImage(file="homepagepic.png")
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=1, column=2, rowspan=4, sticky="nsew")

        label = tk.Label(self, text="       Security System", font=self.controller.title_font, fg="#263942")
        label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        #Adding buttons to perform specific operation
        button1 = tk.Button(self, text="   Verify a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
        button4 = tk.Button(self, text="  Details of a User ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageFive"))
        button3 = tk.Button(self, text="Quit", fg="#fc0808", bg="#ffffff", command=self.on_closing)
        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=1, column=4, ipady=3, ipadx=2)
        button4.grid(row=3, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=4, ipady=3, ipadx=25)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        render = PhotoImage(file="homepagepic.png")
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=1, column=2, rowspan=4, sticky="nsew")

        #Selecting user for verification
        tk.Label(self, text="Select user :", fg="#263942", font='Helvetica 15 bold',).grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)

        #Button to proceed with verifiaction
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        #To check if valid name is entered and showing frame "PageFour"
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")
    
    #function to refresh name in the drop down menu 
    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

#"Pagetwo" frame to add detail of user and capture their picture for further face recognition
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Enter the name :", fg="#263942", font='Helvetica 15 bold').grid(row=1, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetic 12')
        self.user_name.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(self, text="Date of joining(YYYY-MM-DD) :", fg="#263942", font='Helvetica 15 bold').grid(row=2, column=0, pady=10, padx=5)
        self.user_date = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 12')
        self.user_date.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(self, text="Department :", fg="#263942", font='Helvetica 15 bold').grid(row=3, column=0, pady=10, padx=5)
        self.user_dep = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 12')
        self.user_dep.grid(row=3, column=1, pady=10, padx=10)

        self.buttoncanc = tk.Button(self, text="Homepage", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.capturebutton = tk.Button(self, text="Capture", fg="#ffffff", bg="#263942", command=self.start_training)
        
        self.buttoncanc.grid(row=4, column=0, pady=10, ipadx=5, ipady=4)
        self.capturebutton.grid(row=4, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        
    #to add detail of user to database and proceed for face recognition
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        dojo = self.user_date.get()
        depp = self.user_dep.get()
        self.controller.active_name = name
        #refreshing the name in the dropdown of pageone
        self.controller.frames["PageOne"].refresh_names() 
        self.controller.show_frame("PageThree")
        #adding details to database
        mycursor.execute("insert into Security values(%s,%s,%s)",(name,dojo,depp))
        mydb.commit()
        self.clear_text()

    #function to refresh name in the drop down menu
    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

    #function to refresh pagetwo to add new details
    def clear_text(self):
        self.user_name.delete(0,END)
        self.user_date.delete(0,END)
        self.user_dep.delete(0,END)

#To capture imge and train the face recognition model
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        self.back = tk.Button(self, text="Back", fg="#ffffff", bg="#263942", command=lambda: controller.show_frame("PageTwo"))
        self.back.grid(row=1, column=2, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "),bg='#fccb17')
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.back_null()

    def back_null(self):
        self.controller.num_of_images = 0
        self.controller.active_name = NULL
        self.controller.show_frame("PageTwo")

#PageFour will intiate the face verification process
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button2 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        #calling main_app to detect faces
        main_app(self.controller.active_name)

#print all the details of current user
class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file="homepagepic.png")
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=1, column=2, rowspan=4, sticky="nsew")
        tk.Label(self, text="Details of the users :", fg="#263942", font='Helvetica 15 bold').grid(row=0, column=0, padx=10, pady=10)

        #Printing all the records in the database
        mycursor.execute("SELECT * FROM security")
        i=1
        x=0
        for record in mycursor: 
            for j in range(len(record)):
                e = tk.Entry(self, width=10, fg='black') 
                e.grid(row=i, column=j) 
                e.insert(END, record[j])
                x=j
            i=i+1
        
        button = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button.grid(row=i,column=x)



app = MainUI()
photo = PhotoImage(file ="icon.png")
app.iconphoto(False, photo)
app.mainloop()