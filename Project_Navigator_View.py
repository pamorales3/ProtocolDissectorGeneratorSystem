import Tkinter as tk
# Tutorial Video Link - https://www.youtube.com/watch?v=Wb1YFgHqUZ8
class App(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("Project Navigator")
        self.master.resizable(True,True)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3

        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))


        # Workspace
        workspace = tk.Message(self, text="Workspace X", font="System 14", justify='left',aspect=800).grid(row=0, columnspan=2)

        # Project A
        img1 = tk.PhotoImage(file="open_folder_icon.gif")
        img1.zoom(10,10)
        project1 = tk.Label(self, text="Project A", image=img1, compound="left")
        project1.photo = img1
        project1.grid(row=1, columnspan=2)


        # Project B
'''        img2 = tk.PhotoImage(file="close_folder_icon.gif")
        img2.subsample(10, 10)
        project2 = tk.Label(self, text="Project B", image=img2, compound="left")
        project2.photo = img2
        project2.grid(row=1, columnspan=2)
        '''



if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()