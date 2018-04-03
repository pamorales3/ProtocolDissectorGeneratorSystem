import Tkinter as tk
import ttk
import AppKit

class ConsoleApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title('Console Area')
        self.pack(fill='both',expand=True)
        self.master.minsize(800,200)

        #tk.Label(self, text="This is a listbox").pack()

        error_list = ['No error message to show.']

        self.listbox = tk.Listbox(self, selectmode='extended', bg='white')
        self.listbox.pack(fill='both',expand=True)

        for error in error_list:
            self.listbox.insert('end', error)


if __name__ == '__main__':
    #info = AppKit.NSBundle.mainBundle().infoDictionary()
    root = tk.Tk()
    app=ConsoleApp(root)
    AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()