import Tkinter as tk
import ttk
# Tutorial Video Link - https://www.youtube.com/watch?v=Wb1YFgHqUZ8
class Project_Navigator_View(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        #self.master.title("Project Navigator")
        #self.master.resizable(True,True)
        #self.master.tk_setPalette('#ececec')

        # Create Treeview 
        self.tree = ttk.Treeview(self, selectmode='none', height=7)
        self.tree.grid(row=0, column=0, sticky='nsew')
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

    def change_image(self):
        return tk.PhotoImage(file="open_folder_icon.gif")

    def OnDoubleClick(self, event):
        item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(item,"text"))


if __name__ == '__main__':
    root = tk.Tk()
    app = Project_Navigator_View(root)
    app.mainloop()

