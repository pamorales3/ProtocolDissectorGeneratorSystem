import Tkinter as tk
import AppKit

class App(tk.Frame):
    def __init__(self,master):

        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("Organize Views")
        self.master.resizable(False,False)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="Customize the views", font="System 14 bold", justify='left',aspect=800)
        window_prompt.pack(pady=(15,0))

        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=20,pady=15,anchor='w')

        # Hide and Show Labels
        hide_label = tk.Label(dialog_frame,text="Hide",font='System 14', anchor='n')
        hide_label.grid(row=0,column=1,sticky='w', padx=(20,10))

        show_label = tk.Label(dialog_frame, text="Show",font="System 14", anchor='n')
        show_label.grid(row=0,column=2,sticky='w', padx=(15,10))

        # Project Navigation 
        self.var_1 = tk.IntVar()

        project_nav_label = tk.Label(dialog_frame, text="Project Navigation", font='System 14 bold')
        project_nav_label.grid(row=1,column=0,sticky='w', padx=(10,10), pady=(10,10))

        project_nav_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_1, value=1,
                  command=self.project_nav_clicked)
        project_nav_hide.grid(row=1,column=1,sticky='w', padx=(20,10))

        project_nav_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_1, value=2,
                  command=self.project_nav_clicked)
        project_nav_show.grid(row=1,column=2,sticky='w', padx=(20,10))

        # Dissector Building Area
        self.var_2 = tk.IntVar()

        dissector_building_label = tk.Label(dialog_frame, text="Dissector Builidng Area", font='System 14 bold')
        dissector_building_label.grid(row=2,column=0,sticky='w', padx=(10,10), pady=(10,10))

        dissector_building_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_2, value=1,
                    command=self.dissector_building_clicked)
        dissector_building_hide.grid(row=2,column=1,sticky='w', padx=(20,10))

        dissector_building_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_2, value=2,
                    command=self.dissector_building_clicked)
        dissector_building_show.grid(row=2,column=2,sticky='w', padx=(20,10))

        # Palette 
        self.var_3 = tk.IntVar()

        palette_label = tk.Label(dialog_frame, text="Palette", font='System 14 bold')
        palette_label.grid(row=3,column=0,sticky='w', padx=(10,10), pady=(10,10))

        palette_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_3, value=1,
                    command=self.palette_clicked)
        palette_hide.grid(row=3,column=1,sticky='w', padx=(20,10))

        palette_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_3, value=2,
                    command=self.palette_clicked)
        palette_show.grid(row=3,column=2,sticky='w', padx=(20,10))

        # Packet Stream Area
        self.var_4 = tk.IntVar()

        packet_stream_label = tk.Label(dialog_frame, text="Packet Stream Area", font='System 14 bold')
        packet_stream_label.grid(row=4,column=0,sticky='w', padx=(10,10), pady=(10,10))

        packet_stream_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_4, value=1,
                    command=self.packet_stream_clicked)
        packet_stream_hide.grid(row=4,column=1,sticky='w', padx=(20,10))

        packet_stream_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_4, value=2,
                    command=self.packet_stream_clicked)
        packet_stream_show.grid(row=4,column=2,sticky='w', padx=(20,10))

        # Dissected Stream Area
        self.var_5 = tk.IntVar()

        dissected_stream_label = tk.Label(dialog_frame, text="Dissected Stream Area", font='System 14 bold')
        dissected_stream_label.grid(row=5,column=0,sticky='w', padx=(10,10), pady=(10,10))

        dissected_stream_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_5, value=1,
                    command=self.dissected_stream_clicked)
        dissected_stream_hide.grid(row=5,column=1,sticky='w', padx=(20,10))

        dissected_stream_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_5, value=2,
                    command=self.dissected_stream_clicked)
        dissected_stream_show.grid(row=5,column=2,sticky='w', padx=(20,10))

        # Raw Data Area
        self.var_6 = tk.IntVar()

        raw_data_label = tk.Label(dialog_frame, text="Raw Data Area", font='System 14 bold')
        raw_data_label.grid(row=6,column=0,sticky='w', padx=(10,10), pady=(10,10))

        raw_data_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_6, value=1,
                    command=self.raw_data_clicked)
        raw_data_hide.grid(row=6,column=1,sticky='w', padx=(20,10))

        raw_data_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_6, value=2,
                    command=self.raw_data_clicked)
        raw_data_show.grid(row=6,column=2,sticky='w', padx=(20,10))

        # Console Area
        self.var_7 = tk.IntVar()

        console_label = tk.Label(dialog_frame, text="Console Area", font='System 14 bold')
        console_label.grid(row=7,column=0,sticky='w', padx=(10,10), pady=(10,10))

        console_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_7, value=1,
                    command=self.console_area_clicked)
        console_hide.grid(row=7,column=1,sticky='w', padx=(20,10))

        console_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_7, value=2,
                    command=self.console_area_clicked)
        console_show.select()
        console_show.grid(row=7,column=2,sticky='w', padx=(20,10))


        # Frame to hold buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=15,pady=(0,15),anchor='e')

        cancel_button = tk.Button(button_frame,text='Cancel', command=self.cancel_clicked)
        cancel_button.pack(side='right')

        import_button = tk.Button(button_frame,text='Confirm',height = 1,width=6,command=self.confirm_clicked,default='active')
        import_button.pack(side='right')

        default_button = tk.Button(button_frame, text="Restore to Default", command=self.default_clicked)
        default_button.pack(side='right')

    def default_clicked(self,event=None):
        print('Default was clicked!')
        self.master.destroy()

    def confirm_clicked(self,event=None):
        print('Confirm was clicked!')
        self.master.destroy()

    def cancel_clicked(self, event=None):
        print('Cancel was clicked!')
        self.master.destroy()

    def project_nav_clicked(self, event=None):
        print("Project Navigation was selected")
        selection = "You selected the option " + str(self.var_1.get())
        print(selection)

    def dissector_building_clicked(self, event=None):
        print("Dissector Building Area was selected")
        selection = "You selected the option " + str(self.var_2.get())
        print(selection)

    def palette_clicked(self, event=None):
        print("Palette was selected")
        selection = "You selected the option" + str(self.var_3.get())
        print(selection)

    def packet_stream_clicked(self, event=None):
        print("Packet Stream Area selected")
        selection = "You selected the option" + str(self.var_4.get())
        print(selection)

    def dissected_stream_clicked(self, event=None):
        print("Dissected Stream Area selected")
        selection = "You selected the option" + str(self.var_5.get())
        print(selection)

    def raw_data_clicked(self, event=None):
        print("Raw Data Area selected")
        selection = "You selected the option" + str(self.var_6.get())
        print(selection)

    def console_area_clicked(self, event=None):
        print("Console Area selected")
        selection = "You selected the option" + str(self.var_7.get())
        print(selection)
        


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()