from tkinter import *
from tkinter import ttk

class todo:
    def __init__(self,  root):
        self.root = root
        self.root.title('To-do-list')
        self.root.geometry('650x410+300+150') #size of the application

        #===to create a label as to do list which fill total in the application==#

        self.label = Label(self.root ,text='To-Do-List-App' ,font='ariel, 25 bold',width = 10 ,bd=5, bg='yellow',fg='black')
        self.label.pack(side='top' , fill=BOTH)  #pack() is used to Tkinter literally packs all the widgets one after the other in a window.  We can use options like fill, expand, and side to control this geometry manager.
        
        #===to create a label as add tasks in the application==#

        self.label2 = Label(self.root ,text='Add Tasks' ,font='ariel, 15 bold',width = 10 ,bd=5, bg='yellow',fg='black')
        self.label2.place(x=40, y=54)

        #===to create a label as  tasks in the application==#
        
        self.label3 = Label(self.root ,text='Tasks' ,font='ariel, 15 bold',width = 10 ,bd=5, bg='yellow',fg='black')
        self.label3.place(x=320, y=54)

        #===to create text box below the tasks where we can see the tasks in the application==#

        self.main_text=Listbox(self.root, height=9, bd=5, width=23, font="ariel, 20 italic bold")
        self.main_text.place(x=280, y=100)

        #===to create text box below the add tasks where we can text or enter the tasks in the application==#

        self.text = Text(self.root, bd=5, height=2, width=30, font='ariel, 10 bold')
        self.text.place(x=20, y=120)


        #=====add task=====#

        def add():
            content = self.text.get(1.0, END) #1.0 is the beginning index
            self.main_text.insert(END, content) #getting content from our text box and then inserting into list box
            with open('data.txt','a') as file:  #creating and opening a file data.txt and in this we will save data that getting from our text box
                file.write(content)  # and then getting the content which inserted into list box now we are writing it to text file
                file.seek(0)
                file.close()
            self.text.delete(1.0, END) #when we frst write the content in the text box after adding it to the list box it should be delete on the text box so that we can add other items

        #====Delete Task =====#
        def delete():
            delete_ = self.main_text.curselection() # when we click on item and then on delete then the item should be deleted in that way instead of deleting manually we can delete whatever we want on clicking on item which is in list box
            look = self.main_text.get(delete_) #passing the item delete_ variable to the look 
            with open('data.txt', 'r+') as f:
                new_f= f.readlines() #for reading each line in txt file
                f.seek(0)
                for line in new_f:
                    item = str(look) #changing the variable of look into string 
                    if item not in line:  
                        f.write(line)
                f.truncate()   #this with method will delete the item on our text file so that it wont be in the text file
            self.main_text.delete(delete_) #this line delete the item that we selected in our listbox

        #==Reading data from a file==#
        with open('data.txt', 'r') as file:
            read = file.readlines() 
            for i in read:  #by this loop we get the each item in seperate line
                ready = i.split() #split everything
                self.main_text.insert(END, ready) #here we pass the ready so each line will be on a separate line on out list box
            file.close()

        #==To create a button for adding and deleting the items ===#
        self.button = Button(self.root, text="ADD", font='sarif, 20 bold italic',width=10,bd=5,bg='yellow',fg='black', command=add) #here command is the pass the button to the add function
        self.button.place(x=30,y=180)

        self.button2 = Button(self.root, text="Delete", font='sarif, 20 bold italic',width=10,bd=5,bg='yellow',fg='black', command=delete)
        self.button2.place(x=30,y=280)


def main():
    root = Tk()  #root variable to instantiate the Tkinter window and run the application.
    ui = todo(root)  
    root.mainloop()

if __name__ == "__main__":
    main()