import Tkinter as tk
import tkFileDialog
import AppKit

class project_import_window(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("Project Import")
        self.master.resizable(False,False)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="Import a project into the current workspace.", font="System 14 bold", justify='left',aspect=800)
        window_prompt.pack(pady=(15,0))

        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=20,pady=15,anchor='w')

        project_label = tk.Label(dialog_frame,text="Project",font='System 14 bold')
        project_label.grid(row=0,column=0,sticky='w')

        project_name_entry = tk.Entry(dialog_frame,background="white",width=24)
        project_name_entry.grid(row=0,column=1,sticky='w')

        browse_project_button = tk.Button(dialog_frame,text='Browse', command=self.directory_picker)
        browse_project_button.grid(row=0,column=2,sticky='w')

        #frame for Import and Cancel Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=15,pady=(0,15),anchor='e')

        cancel_button = tk.Button(button_frame,text='Cancel', command=self.cancel_clicked)
        cancel_button.pack(side='right')

        import_button = tk.Button(button_frame,text='Import',height = 1,width=6,command=self.import_clicked,default='active')
        import_button.pack(side='right')

    def cancel_clicked(self, event=None):
        print('Cancel was clicked!')
        self.master.destroy()

    def import_clicked(self,event=None):
        print('Import was clicked!')
        self.master.destroy()

    def directory_picker(self):
        self.selected_directory = tkFileDialog.askdirectory(parent=self,initialdir = "/",title = "Select directory")
        print("You selected directory: " + self.selected_directory)


if __name__ == '__main__':
    root = tk.Tk()
    app = project_import_window(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()