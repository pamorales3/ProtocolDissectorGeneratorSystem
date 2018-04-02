import Tkinter as tk
#import AppKit

class create_project_window(tk.Frame):  # Frame is a type of container for Tkinter
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("New Project")
        self.master.resizable(False,False)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="Create a new project.", font="System 14 bold", justify='left',aspect=800)
        window_prompt.pack(pady=(15,0))

        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=20,pady=15,anchor='w')

        project_label = tk.Label(dialog_frame,text="Project Name",font='System 14 bold')
        project_label.grid(row=0,column=0,sticky='w')

        project_name_entry = tk.Entry(dialog_frame,background="white",width=24)
        project_name_entry.grid(row=0,column=1,sticky='w')

        project_description_label = tk.Label(dialog_frame, text="Description", font='System 14 bold')
        project_description_label.grid(row=1,column=0,sticky='w')

        project_description_entry = tk.Text(dialog_frame, background="white", width=32, height=7)
        project_description_entry.grid(row=1,column=1,sticky='w')

        # Frame for Create and Cancel Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=15,pady=(0,15),anchor='e')

        cancel_button = tk.Button(button_frame,text='Cancel')
        cancel_button.pack(side='right')

        import_button = tk.Button(button_frame,text='Create',height = 1,width=6,command=self.create_clicked,default='active')
        import_button.pack(side='right')

    def create_clicked(self,event=None):
        print('Create was clicked!')
        self.master.destroy()

    def cancel_clicked(self, event=None):
        print('Cancel was clicked!')
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = create_project_window(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()