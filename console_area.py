import Tkinter as tk
import AppKit

class ConsoleApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(fill='both',expand=True)

        main_frame = tk.Frame(self)
        main_frame.grid(row=0)

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0)

        listbox_frame = tk.Frame(main_frame)
        listbox_frame.grid(row=1)

        error_list = ['No error message to show.']

        self.listbox = tk.Listbox(listbox_frame, selectmode='extended', bg='white')
        self.listbox.pack(fill='both',expand=True)

        # Window min, max,close button, and title
        title = tk.Label(button_frame, text="Raw Data Area", font='System 14 bold', background='lightblue')
        title.grid(row=0,column=0)

        minimize = tk.Button(button_frame, text="_", command=self.minimize_button_clicked)
        minimize.grid(row=0,column=1)

        maximize = tk.Button(button_frame, text="[ ]")
        maximize.grid(row=0,column=2)

        close = tk.Button(button_frame, text="X",command=self.close_button_clicked)
        close.grid(row=0,column=3)

        for error in error_list:
            self.listbox.insert('end', error)

    def close_button_clicked(self,event=None):
        self.grid_forget()

    def minimize_button_clicked(self, event=None):
        print("Minimize was press!")


if __name__ == '__main__':
    root = tk.Tk()
    app=ConsoleApp(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()