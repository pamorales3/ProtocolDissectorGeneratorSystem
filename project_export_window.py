import Tkinter as tk
import tkFileDialog
import AppKit

class App(tk.Frame):

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("Project Export")
        self.master.resizable(False,False)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="Export a project to the local file system.", font="System 14 bold", justify='left',aspect=800)
        window_prompt.pack(pady=(15,0))
        
        # Project Frame
        project_frame = tk.Frame(self)
        project_frame.pack(padx=20,pady=15,anchor='w')

        project_label = tk.Label(project_frame,text="Project",font='System 14 bold', anchor="n")
        project_label.grid(row=0,column=0,sticky='w')

        project_name_entry = tk.Entry(project_frame,background="white",width=24)
        project_name_entry.grid(row=0,column=1,sticky='w')

        browse_project_button = tk.Button(project_frame,text='Browse', command=self.file_picker)
        browse_project_button.grid(row=0,column=2,sticky='w')

        export_label = tk.Label(project_frame, text="To export file", font='System 14 bold')
        export_label.grid(row=1,column=0,sticky='w')

        export_label_entry = tk.Entry(project_frame, background="white", width=24)
        export_label_entry.grid(row=1,column=1,sticky='w')

        browse_project_button = tk.Button(project_frame,text='Browse', command=self.directory_picker)
        browse_project_button.grid(row=1,column=2,sticky='w')

        # Frame for Export and Cancel Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=15,pady=(0,15),anchor='e')

        cancel_button = tk.Button(button_frame,text='Cancel', command=self.cancel_clicked)
        cancel_button.pack(side='right')

        export_button = tk.Button(button_frame,text='Export',height = 1,width=6,command=self.export_clicked,default='active')
        export_button.pack(side='right')

    def cancel_clicked(self, event=None):
        print('Cancel was clicked!')
        self.master.destroy()

    def export_clicked(self,event=None):
        print('Export was clicked!')
        self.master.destroy()

    def file_picker(self):
        self.selected_file = tkFileDialog.askopenfilename(parent=self,initialdir = "/",title = "Select file")
        print("You selected file: " + self.selected_file)

    def directory_picker(self):
        self.selected_directory = tkFileDialog.askdirectory(parent=self,initialdir = "/",title = "Select directory")
        print("You selected directory: " + self.selected_directory)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()