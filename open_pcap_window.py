import Tkinter as tk
import tkFileDialog
import AppKit

class App(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("PCAP")
        self.master.resizable(False,False)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="Open a PCAP file", font="System 14 bold", justify='left',aspect=800)
        window_prompt.pack(pady=(15,0))
        
        # PCAP Frame
        pcap_frame = tk.Frame(self)
        pcap_frame.pack(padx=20,pady=15,anchor='w')

        pcap_label = tk.Label(pcap_frame,text="PCAP Name",font='System 14 bold', anchor="n")
        pcap_label.grid(row=0,column=0,sticky='w')

        pcap_entry = tk.Entry(pcap_frame,background="white",width=24)
        pcap_entry.grid(row=0,column=1,sticky='w')

        browse_project_button = tk.Button(pcap_frame,text='Browse', command=self.file_picker)
        browse_project_button.grid(row=0,column=2,sticky='w')

        # Open and Cancel Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=15,pady=(0,15),anchor='e')

        cancel_button = tk.Button(button_frame,text='Cancel', command=self.cancel_clicked)
        cancel_button.pack(side='right')

        open_button = tk.Button(button_frame,text='Open',height = 1,width=6,command=self.open_clicked, default='active')
        open_button.pack(side='right')

    def cancel_clicked(self, event=None):
        print('Cancel was clicked!')
        self.master.destroy()

    def open_clicked(self,event=None):
        print('Open was clicked!')
        self.master.destroy()

    def file_picker(self):
        self.selected_file = tkFileDialog.askopenfilename(parent=self,initialdir = "/",title = "Select PCAP file")
        print("You selected file: " + self.selected_file)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()