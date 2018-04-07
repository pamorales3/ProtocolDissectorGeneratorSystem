import Tkinter as tk
import packet_stream_area as ps
import dissected_stream_area as ds
import raw_data_area as raw
import console_area as console
import AppKit
import ttk

class OutputView(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #self.master.title("Console Views")
        #Create a notebook with tabs to hold all views belos
        notebook = ttk.Notebook(self.master,width=200, height=100)
        #make the notebook visible
        notebook.pack()

        # Tab for Packet Stream Area
        packet_stream_tab = ps.PacketStreamArea(notebook)
        notebook.add(packet_stream_tab, text="Packet Stream Area")

        # Tab for Dissected Stream Area
        dissected_stream_tab = ds.DissectedStreamArea(notebook)
        notebook.add(dissected_stream_tab, text="Dissected Stream Area")

        #Tab for Raw Data Area
        raw_data_tab = raw.RawData(notebook)
        notebook.add(raw_data_tab, text="Raw Data Area")

        # Tab for Console Area
        console_area_tab = console.ConsoleApp(notebook)
        notebook.add(console_area_tab, text="Console Area")

if __name__ == '__main__':
    root = tk.Tk()
    OutputView = OutputView(root)
    #Bring this window on top of all other windows
    #Might need to remove later on
    #AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    OutputView.mainloop()