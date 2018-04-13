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

class Main(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("")
        self.master.resizable(True,True)
        self.master.tk_setPalette('#ececec')
        self.master.protocol("WM_DELETE_WINDOW", self.callback)

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3

        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_title = tk.Message(self, text="Protocol Dissector Generator System", font=("System 14 bold", 20), justify='left',aspect=1000)
        window_title.config(foreground="orange")
        window_title.pack(pady=(5,0))

        # Menu Section Frame
        menu_section_frame = tk.Frame(self,relief='raised', borderwidth=10)
        menu_section_frame.pack(padx=5,pady=5,anchor='w',expand=True)

        '''
        ////////////////////////////////////////////////////////////////////////////////////
        /                                  MENU SECTION                                    /
        ////////////////////////////////////////////////////////////////////////////////////
        '''   

        # Create Project Button
        createProjectButton = tk.Button(menu_section_frame, text='Create Project', command=self.create_project_clicked)
        createProjectButton.pack(side='left')

        # Save Project Button
        saveProjectButton = tk.Button(menu_section_frame, text='Save Project', command=self.save_project_clicked)
        saveProjectButton.pack(side='left')

        # Close Project Button
        closeProjectButton = tk.Button(menu_section_frame, text='Close Project', command=self.close_project_clicked)
        closeProjectButton.pack(side='left')

        # Switch Workspace Button
        switchWorkspaceButton = tk.Button(menu_section_frame, text='Switch Workspace', command=self.switch_workspace_clicked)
        switchWorkspaceButton.pack(side='left')

        # Import Project Button
        importProjectButton = tk.Button(menu_section_frame, text='Import Project', command=self.import_project_clicked)
        importProjectButton.pack(side='left')
        
        # Export Project Button
        exportProjectButton = tk.Button(menu_section_frame, text='Export Project', command=self.export_project_clicked)
        exportProjectButton.pack(side='left')
        
        # Generate Dissector Script Button
        generateDSButton = tk.Button(menu_section_frame, text='Generate Dissector Script', command=self.generate_dissector_clicked)
        generateDSButton.pack(side='left')

        # Organize Views Button
        organizeViewsButton = tk.Button(menu_section_frame, text='Organize Views', command=self.organize_views_clicked)
        organizeViewsButton.pack(side='left')

        # Open PCAP Button
        openPCAPButton = tk.Button(menu_section_frame, text='Open PCAP', command=self.open_pcap_clicked)
        openPCAPButton.pack(side='left')

        '''
        ////////////////////////////////////////////////////////////////////////////////////
        /                                  MAIN SECTION                                    /
        ////////////////////////////////////////////////////////////////////////////////////
        ''' 

        # Main Area Frame
        self.main_area_frame = tk.Frame(self,relief='raised', borderwidth=5)
        self.main_area_frame.pack(padx=5,pady=5,anchor='w')

        self.project_nav = pnv.Project_Navigator_View(self.main_area_frame)
        self.project_nav.pack(side='left')

        #self.dissector_builder = dba.dissector_builder_area(self.main_area_frame)
        #self.dissector_builder.pack(side='right')

        self.views_frame = tk.Frame(self,relief='raised', borderwidth=1)
        self.views_frame.pack(padx=5,pady=5,anchor='w')

        self.views = psa.PacketStreamArea(self.views_frame)
        self.views.pack(side='left')

        self.dissected_stream = dsa.DissectedStreamArea(self.views_frame)
        self.dissected_stream.pack(side='left')

        self.main_area_frame.update()
        print("Main Frame X Size " , self.main_area_frame.winfo_width())
        print("Main Frame Y Size " , self.main_area_frame.winfo_height())

    def callback(self):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.master.destroy()

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None
        #app.mainloop
        
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

    def organize_views_clicked(self,event=None):
        root = tk.Tk()
        app = ovw.organzie_views_window(root)
        app.mainloop()

    def open_pcap_clicked(self,event=None):
        root = tk.Tk()
        app = opw.open_pcap_window(root)
        app.mainloop()
    
if __name__ == '__main__':
    root = tk.Tk()         
    app = Main(root)
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    app.mainloop()