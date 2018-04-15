import Tkinter as tk
import ttk

class Project_Navigator_View(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack(fill='both',expand=True)
        #self.master.title("Project Navigator")
        #self.master.resizable(True,True)
        #self.master.tk_setPalette('#ececec')

        main_frame = tk.Frame(self)
        main_frame.pack(anchor='w',expand=True,fill='x')

        button_frame = tk.Frame(main_frame)
        button_frame.pack(padx=0,pady=0,anchor='w',expand=True,fill='x')

        self.title = tk.Label(button_frame, text="Project Navigator", font='System 14 bold', background='lightblue')
        self.title.pack(side='left',fill='x')

        self.title.bind("<ButtonPress-1>", self.StartMove)
        self.title.bind("<ButtonRelease-1>", self.StopMove)
        self.title.bind("<B1-Motion>", self.OnMotion)

        minimize = tk.Button(button_frame, text="_", command=self.minimize_button_clicked, bg="lightblue")
        minimize.pack(side='left')

        maximize = tk.Button(button_frame, text="[ ]",bg='lightblue')
        maximize.pack(side='left')

        close = tk.Button(button_frame, text="X", bg='lightblue',command=self.close_button_clicked)
        close.pack(side='left')

        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(anchor='w',expand=True,fill='x')


        # Create Treeview 
        self.tree = ttk.Treeview(tree_frame, selectmode='none',height=190)
        self.tree.pack(fill='both',expand=True)
        self.tree.bind("<Double-1>", self.OnDoubleClick)

        # Setup column heading   #0  is 0 column
        self.tree.heading('#0', text='Workspace X', anchor='center')

        # Insert image to #0 
        self.img_1 = tk.PhotoImage(file="open_folder_icon.gif") #change to your file path
        self.img_1 = self.img_1.subsample(10,10)

        self.img_2 = tk.PhotoImage(file="close_folder_icon.gif")
        self.img_2 = self.img_2.subsample(40,40)

        projA = self.tree.insert('', 'end', text="Project A", image=self.img_1)
        self.tree.insert(projA, 'end', text="Dissector A")

        projB = self.tree.insert('', 'end', text="Project B", image=self.img_1)
        self.tree.insert(projB, 'end', text="Dissector B")

        projC = self.tree.insert('', 'end', text="Project C", image=self.img_2)
        self.tree.insert(projC, 'end', text="Dissector C")

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y
        print("Start X Position ", self.x)
        print("Start Y Position ", self.y)

    def StopMove(self, event):
        self.x = event.x
        self.y = event.y
        print("End X Position ", self.x)
        print("End Y Position ", self.y)

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        if (x > 0 and y > 0):
            self.master.place(x=x)
            self.master.place(y=y) 
            self.master.update()

    def OnDoubleClick(self, event):
        item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(item,"text"))

    def close_button_clicked(self,event=None):
        self.grid_forget()

    def minimize_button_clicked(self, event=None):
        self.master.iconify()


if __name__ == '__main__':
    root = tk.Tk()
    app = Project_Navigator_View(root)
    app.mainloop()