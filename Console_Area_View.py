import Tkinter as tk
# Tutorial Video Link - https://www.youtube.com/watch?v=Wb1YFgHqUZ8
class App(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("Console Area")
        self.master.resizable(True,True)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="No error message to show.", font="System 14", justify='left',aspect=800)
        window_prompt.pack(pady=(50, 50))





if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()