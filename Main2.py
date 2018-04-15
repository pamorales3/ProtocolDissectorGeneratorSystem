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
        createProjectButton = tk.Button(top_frame, text='Create Project')

        # Save Project Button
        saveProjectButton = tk.Button(top_frame, text='Save Project')

        # Close Project Button
        closeProjectButton = tk.Button(top_frame, text='Close Project')

        # Switch Workspace Button
        switchWorkspaceButton = tk.Button(top_frame, text='Switch Workspace')

        # Import Project Button
        importProjectButton = tk.Button(top_frame, text='Import Project')
        
        # Export Project Button
        exportProjectButton = tk.Button(top_frame, text='Export Project')
        
        # Generate Dissector Script Button
        generateDSButton = tk.Button(top_frame, text='Generate Dissector Script')

        # Organize Views Button
        organizeViewsButton = tk.Button(top_frame, text='Organize Views')

        # Open PCAP Button
        openPCAPButton = tk.Button(top_frame, text='Open PCAP')

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


if __name__ == '__main__':
    root = tk.Tk()         
    app = Main2(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()