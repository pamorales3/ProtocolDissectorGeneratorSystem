import Tkinter as tk
import ttk
import tkFileDialog
#import AppKit

class dissector_script_window(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("Dissector Script")
        self.master.resizable(False,False)
        self.master.tk_setPalette("#ececec")

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="Generate a custom dissector script from a selected project.",
                   font="System 14 bold", justify="left", aspect=800)
        window_prompt.pack(pady=(15,0))

        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=20, pady=15, anchor='w')

        project_label = tk.Label(dialog_frame, text="Project:",font='System 14 bold')
        project_label.grid(row=0, column=0,sticky='w')

        project_name_entry = tk.Entry(dialog_frame, background="white", width=24)
        project_name_entry.grid(row=0,column=1,sticky='w')
        #highlight frame around the project_name entry when selected
        project_name_entry.focus_set()

        browse_project_button = tk.Button(dialog_frame,text="Browse", command=self.file_picker)
        browse_project_button.grid(row=0,column=2,sticky='w')

        dissector_format_label = tk.Label(dialog_frame,text="Dissector Format:", font='System 14 bold')
        dissector_format_label.grid(row=1,column=0,sticky='w')

        dissectorFormats = ['Lua','C']
        combo = ttk.Combobox(dialog_frame,values=dissectorFormats,state='readonly')
        combo.current(0)
        combo.grid(row=1,column=1,sticky='w')

        save_location_label = tk.Label(dialog_frame,text='Save Location',font='System 14 bold')
        save_location_label.grid(row=2,column=0,sticky='w')

        location = tk.Entry(dialog_frame,background='white',width=24,)
        location.grid(row=2,column=1,sticky='w')

        browse_location_button = tk.Button(dialog_frame,text='Browse', command=self.directory_picker)
        browse_location_button.grid(row=2,column=2,sticky='w')

        button_frame = tk.Frame(self)
        button_frame.pack(padx=15,pady=(0,15),anchor='e')

        cancel_button = tk.Button(button_frame, text='Cancel',height=1,width=6,command=self.click_cancel)
        cancel_button.pack(side='right')

        generate_button = tk.Button(button_frame,text='Generate', height=1,width=6,default='active',command=self.click_generate)
        generate_button.pack(side='right')

    def click_generate(self, event=None):
        print("the user clicked 'Generate")
        self.master.destroy()

    def click_cancel(self,event=None):
        print("The user clicked 'Cancel'")
        self.master.destroy()

    def directory_picker(self):
        self.selected_directory = tkFileDialog.askdirectory(parent=self,initialdir = "/",title = "Select directory")
        print("You selected directory: " + self.selected_directory)

    def file_picker(self):
        self.selected_file = tkFileDialog.askopenfilename(parent=self,initialdir = "/",title = "Select file")
        print("You selected file: " + self.selected_file)

if __name__ == '__main__':
    #info = AppKit.NSBundle.mainBundle().infoDictionary()
    #info['LSUIElement']=True
    root = tk.Tk()
    app = dissector_script_window(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()