import Tkinter as tk
import ttk
import tkMessageBox
import create_project_window as cP
import workspace_launcher as wL
import project_import_window as piw
import project_export_window as pew
import dissector_script_window as dsw
import organize_views_windows as ovw
import open_pcap_window as opw
import Project_Navigator_View as pnv
import output_views as ov
import dissector_builder_area as dba
import packet_stream_area as psa
import dissected_stream_area as dsa 
import raw_data_area as rda
import console_area as ca

class Main2(tk.Frame):

    root = tk.Tk()
    app = wL.workspace_launcher(root)
    app.mainloop()
    
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("")
        self.master.resizable(True,True)
        self.master.tk_setPalette('#ececec')

        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad)) 

        # create all of the main containers
        top_frame = tk.Frame(self, bg='cyan', width=450, height=50, pady=3)
        center = tk.Frame(self, bg='red', width=450, height=45, padx=3, pady=3)
        btm_frame = tk.Frame(self, bg='purple', width=250, height=45, pady=3)
        #btm_frame2 = tk.Frame(self, bg='lavender', width=450, height=60, pady=3)

        # layout all of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top_frame.grid(row=0, sticky="ew")
        center.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")
        #btm_frame2.grid(row=4, sticky="ew")

        # create the widgets for the top frame

        # Title
        window_title = tk.Message(top_frame, text="Protocol Dissector Generator System", font=("System 14 bold", 20), justify='left',aspect=1000)
        window_title.config(foreground="orange")


        # Create Project Button
        createProjectButton = tk.Button(top_frame, text='Create Project', command=self.create_project_clicked)

        # Save Project Button
        saveProjectButton = tk.Button(top_frame, text='Save Project', command=self.save_project_clicked)

        # Close Project Button
        closeProjectButton = tk.Button(top_frame, text='Close Project', command=self.close_project_clicked)

        # Switch Workspace Button
        switchWorkspaceButton = tk.Button(top_frame, text='Switch Workspace', command=self.switch_workspace_clicked)

        # Import Project Button
        importProjectButton = tk.Button(top_frame, text='Import Project', command=self.import_project_clicked)
        
        # Export Project Button
        exportProjectButton = tk.Button(top_frame, text='Export Project', command=self.export_project_clicked)
        
        # Generate Dissector Script Button
        generateDSButton = tk.Button(top_frame, text='Generate Dissector Script', command=self.generate_dissector_clicked)

        # Organize Views Button
        organizeViewsButton = tk.Button(top_frame, text='Organize Views',command=self.call_organize_views)

        # Open PCAP Button
        openPCAPButton = tk.Button(top_frame, text='Open PCAP', command=self.open_pcap_clicked)

        # layout the widgets in the top frame
        window_title.grid(row=0,columnspan=8)
        createProjectButton.grid(row=1, column=0)
        saveProjectButton.grid(row=1, column=1)
        closeProjectButton.grid(row=1, column=2)
        switchWorkspaceButton.grid(row=1, column=3)
        importProjectButton.grid(row=1, column=4)
        exportProjectButton.grid(row=1,column=5)
        generateDSButton.grid(row=1,column=6)
        organizeViewsButton.grid(row=1,column=7)
        openPCAPButton.grid(row=1,column=8)

        # create the center widgets
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        ctr_left = tk.Frame(center, bg='blue', width=150, height=190)
        ctr_mid = tk.Frame(center, bg='yellow', width=300, height=210, padx=3, pady=3)
        #ctr_right = tk.Frame(center, bg='green', width=100, height=190, padx=3, pady=3)

        ctr_left.grid(row=0, column=0, sticky="ns")
        ctr_mid.grid(row=0, column=1, sticky="nsew")
        #ctr_right.grid(row=0, column=2, sticky="ns")

        '''
        ////////////////////////////////////////////////////////////////////////////////////
        /                                  MAIN SECTION                                    /
        ////////////////////////////////////////////////////////////////////////////////////
        ''' 

        self.project_nav = pnv.Project_Navigator_View(ctr_left)
        self.project_nav.grid(row=0,column=0,rowspan=2,sticky="nsew")

        self.dissector_builder = dba.dissector_builder_area(ctr_mid)
        self.dissector_builder.grid(row=0,column=1,sticky="nsew")
        
        self.views = psa.PacketStreamArea(btm_frame)
        self.views.grid(row=0,column=1,padx=1,pady=1,sticky="nsew")

        self.dissected_stream = dsa.DissectedStreamArea(btm_frame)
        self.dissected_stream.grid(row=0,column=2,padx=1,pady=1,sticky="nsew")

        self.raw_data = rda.RawData(btm_frame)
        self.raw_data.grid(row=0,column=3,padx=1,pady=1,sticky="nsew")

        self.console_area = ca.ConsoleApp(btm_frame)
        self.console_area.grid(row=0,column=4,padx=1,pady=1,sticky="nsew")

    def call_organize_views(self):
        r = tk.Toplevel()
        organizeViews = OrganizeViews(r)
        organizeViews.mainloop()

    def create_project_clicked(self,event=None):
        root = tk.Tk()
        app = cP.create_project_window(root)
        app.mainloop()

    def save_project_clicked(self,event=None):
        #start progress bar
        saveBar = range(75)
        popup = tk.Toplevel()
        tk.Label(popup, text="Project is being saved.").grid(row=0,column=0)

        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0)
        popup.pack_slaves()

        progress_step = float(100.0/len(saveBar))
        for s in saveBar:
            popup.update()
            progress += progress_step
            progress_var.set(progress)

        popup.destroy()

    def close_project_clicked(self,event=None):
        popup = tk.Toplevel()
        tk.Label(popup, text="Are you sure you want to close project?").grid(row=0,column=0)

        yes = tk.Button(popup, text="YES")
        yes.grid(row=1,column=0,columnspan=2,sticky='w')

        no = tk.Button(popup, text="NO")
        no.grid(row=1,column=4,columnspan=2)

    def switch_workspace_clicked(self,event=None):
        root = tk.Tk()
        app = wL.workspace_launcher(root)
        app.mainloop()

    def import_project_clicked(self,event=None):
        root = tk.Tk()
        app = piw.project_import_window(root)
        app.mainloop()

    def export_project_clicked(self,event=None):
        root = tk.Tk()
        app = pew.project_export_window(root)
        app.mainloop()

    def generate_dissector_clicked(self,event=None):
        root = tk.Tk()
        app = dsw.dissector_script_window(root)
        app.mainloop()

    def open_pcap_clicked(self,event=None):
        root = tk.Tk()
        app = opw.open_pcap_window(root)
        app.mainloop()

class OrganizeViews(tk.Frame):
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

        window_prompt = tk.Message(self.master, text="Customize the views", font="System 14 bold", justify='left',aspect=800)
        window_prompt.pack(pady=(15,0))

        dialog_frame = tk.Frame(self.master)
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

        self.project_nav_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_1, value=2,
                  command=self.project_nav_clicked)
        self.project_nav_show.grid(row=1,column=2,sticky='w', padx=(20,10))
        self.project_nav_show.select() # Turns on the project navigation show radio button

        # Dissector Building Area
        self.var_2 = tk.IntVar()

        dissector_building_label = tk.Label(dialog_frame, text="Dissector Builidng Area", font='System 14 bold')
        dissector_building_label.grid(row=2,column=0,sticky='w', padx=(10,10), pady=(10,10))

        dissector_building_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_2, value=1,
                    command=self.dissector_building_clicked)
        dissector_building_hide.grid(row=2,column=1,sticky='w', padx=(20,10))

        self.dissector_building_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_2, value=2,
                    command=self.dissector_building_clicked)
        self.dissector_building_show.grid(row=2,column=2,sticky='w', padx=(20,10))
        self.dissector_building_show.select() # Turns on the dissector building show radio button

        # Palette 
        self.var_3 = tk.IntVar()

        palette_label = tk.Label(dialog_frame, text="Palette", font='System 14 bold')
        palette_label.grid(row=3,column=0,sticky='w', padx=(10,10), pady=(10,10))

        palette_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_3, value=1,
                    command=self.palette_clicked)
        palette_hide.grid(row=3,column=1,sticky='w', padx=(20,10))

        self.palette_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_3, value=2,
                    command=self.palette_clicked)
        self.palette_show.grid(row=3,column=2,sticky='w', padx=(20,10))
        self.palette_show.select() # Turns on the palette show radio button

        # Packet Stream Area
        self.var_4 = tk.IntVar()

        packet_stream_label = tk.Label(dialog_frame, text="Packet Stream Area", font='System 14 bold')
        packet_stream_label.grid(row=4,column=0,sticky='w', padx=(10,10), pady=(10,10))

        packet_stream_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_4, value=1,
                    command=self.packet_stream_clicked)
        packet_stream_hide.grid(row=4,column=1,sticky='w', padx=(20,10))

        self.packet_stream_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_4, value=2,
                    command=self.packet_stream_clicked)
        self.packet_stream_show.grid(row=4,column=2,sticky='w', padx=(20,10))
        self.packet_stream_show.select() # Turns on the packet stream show radio button

        # Dissected Stream Area
        self.var_5 = tk.IntVar()

        dissected_stream_label = tk.Label(dialog_frame, text="Dissected Stream Area", font='System 14 bold')
        dissected_stream_label.grid(row=5,column=0,sticky='w', padx=(10,10), pady=(10,10))

        dissected_stream_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_5, value=1,
                    command=self.dissected_stream_clicked)
        dissected_stream_hide.grid(row=5,column=1,sticky='w', padx=(20,10))

        self.dissected_stream_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_5, value=2,
                    command=self.dissected_stream_clicked)
        self.dissected_stream_show.grid(row=5,column=2,sticky='w', padx=(20,10))
        self.dissected_stream_show.select() # Turns on the dissected stream show radio button

        # Raw Data Area
        self.var_6 = tk.IntVar()

        raw_data_label = tk.Label(dialog_frame, text="Raw Data Area", font='System 14 bold')
        raw_data_label.grid(row=6,column=0,sticky='w', padx=(10,10), pady=(10,10))

        raw_data_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_6, value=1,
                    command=self.raw_data_clicked)
        raw_data_hide.grid(row=6,column=1,sticky='w', padx=(20,10))

        self.raw_data_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_6, value=2,
                    command=self.raw_data_clicked)
        self.raw_data_show.grid(row=6,column=2,sticky='w', padx=(20,10))
        self.raw_data_show.select() # Turns on the raw data show radio button 

        # Console Area
        self.var_7 = tk.IntVar()

        console_label = tk.Label(dialog_frame, text="Console Area", font='System 14 bold')
        console_label.grid(row=7,column=0,sticky='w', padx=(10,10), pady=(10,10))

        console_hide = tk.Radiobutton(dialog_frame, text="", variable=self.var_7, value=1,
                    command=self.console_area_clicked)
        console_hide.grid(row=7,column=1,sticky='w', padx=(20,10))

        self.console_show = tk.Radiobutton(dialog_frame, text="", variable=self.var_7, value=2,
                    command=self.console_area_clicked)
        self.console_show.grid(row=7,column=2,sticky='w', padx=(20,10))
        self.console_show.select()  # Turns on the console show radio button


        # Frame to hold buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(padx=15,pady=(0,15),anchor='e')

        cancel_button = tk.Button(button_frame,text='Cancel', command=self.cancel_clicked)
        cancel_button.pack(side='right')

        import_button = tk.Button(button_frame,text='Confirm',height = 1,width=6,command=self.confirm_clicked,default='active')
        import_button.pack(side='right')

        default_button = tk.Button(button_frame, text="Restore to Default", command=self.default_clicked)
        default_button.pack(side='right')

    def default_clicked(self,event=None):
        print('Default was clicked!')
        self.project_nav_show.select()
        self.dissector_building_show.select()
        self.palette_show.select()
        self.packet_stream_show.select()
        self.dissected_stream_show.select()
        self.raw_data_show.select()
        self.console_show.select()

    def confirm_clicked(self,event=None):
        print('Confirm was clicked!')
        self.master.destroy()

    def cancel_clicked(self, event=None):
        print('Cancel was clicked!')
        self.master.destroy()

    def project_nav_clicked(self, event=None):
        selection = self.var_1.get()
        if selection == 1:
            print("Project Navigation: Hide was clicked")
        else:
            print("Project Navigation: Show was clicked")

    def dissector_building_clicked(self, event=None):
        selection = self.var_2.get()
        if selection == 1:
            print("Dissector Building Area: Hide was clicked")
        else:
            print("Dissector Building Area: Show was clicked")

    def palette_clicked(self, event=None):
        selection = self.var_3.get()
        if selection == 1:
            print("Palette: Hide was clicked")
        else:
            print("Palette: Show was clicked")

    def packet_stream_clicked(self, event=None):
        selection = self.var_4.get()
        if selection == 1:
            print("Packet Stream: Hide was clicked")
        else:
            print("Packet Stream: Show was clicked")

    def dissected_stream_clicked(self, event=None):
        selection = self.var_5.get()
        if selection == 1:
            print("Dissected Stream Area: Hide was clicked")
        else:
            print("Dissected Stream Area: Show was clicked")

    def raw_data_clicked(self, event=None):
        selection = self.var_6.get()
        if selection == 1:
            print("Raw Data Area: Hide was clicked")
        else:
            print("Raw Data Area: Show was clicked")

    def console_area_clicked(self, event=None):
        selection = self.var_7.get()
        if selection == 1:
            print("Console Area: Hide was clicked")
        else:
            print("Console Area: Show was clicked")


if __name__ == '__main__':
    root = tk.Tk()         
    app = Main2(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()