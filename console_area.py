import Tkinter as tk
import AppKit

class ConsoleApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(fill='both',expand=True)

        main_frame = tk.Frame(self)
        main_frame.grid(row=0,sticky="nsew")

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0,sticky="nsew")

        self.listbox_frame = tk.Frame(main_frame)
        self.listbox_frame.grid(row=1,sticky="nsew")

        error_list = ['No error message to show.']

        self.listbox = tk.Listbox(self.listbox_frame, selectmode='extended', bg='white')
        self.listbox.pack(fill='x',expand=True)

        # Window min, max,close button, and title
        title = tk.Label(button_frame, text="Console Area", font='System 14 bold', background='lightblue')
        title.grid(row=0,column=0,sticky="nsew")

        minimize = tk.Button(button_frame, text="_", command=self.minimize_button_clicked)
        minimize.grid(row=0,column=1,sticky="nsew")

        maximize = tk.Button(button_frame, text="[ ]",command=self.maximize_button_clicked)
        maximize.grid(row=0,column=2,sticky="nsew")

        close = tk.Button(button_frame, text="X",command=self.close_button_clicked)
        close.grid(row=0,column=3,sticky="nsew")

        for error in error_list:
            self.listbox.insert('end', error)

    def close_button_clicked(self,event=None):
        self.grid_forget()

    def minimize_button_clicked(self, event=None):
        self.listbox_frame.grid_forget()

    def maximize_button_clicked(self,event=None):
        self.listbox_frame.grid(row=1,sticky="nsew")


if __name__ == '__main__':
    root = tk.Tk()
    app=ConsoleApp(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()