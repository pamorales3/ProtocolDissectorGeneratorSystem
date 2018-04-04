import Tkinter as tk
import packet_stream_area as ps
import dissected_stream_area as dsa
import AppKit
import ttk

class OutputView(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.master.title("Console Views")
        notebook = ttk.Notebook(self.master)

        notebook.pack()

        #Tab for Packet Stream Area
        packet_stream_tab = ps.PacketStreamArea(notebook)
        notebook.add(packet_stream_tab, text="Packet Stream Area")

        #Tab for Dissected Stream Area
        dissected_stream_tab = ttk.Frame(notebook)
        notebook.add(dissected_stream_tab, text="Dissected Stream Area")

        #Test button inside the tab
        tk.Button(dissected_stream_tab, text="click me").pack()

        #Tab for Raw Data Area
        raw_data_tab = ttk.Frame(notebook)
        notebook.add(raw_data_tab, text="Raw Data Area")

        #Tab for Console Area

        console_area_tab = ttk.Frame(notebook)
        notebook.add(console_area_tab,text="Console Area")

    def create_packet_stream_area(self):
        root = tk.Tk()
        stream_area = ps.PacketStreamArea(root)
        stream_area.mainloop()


    def create_dissected_stream_area(self):
        root = tk.Tk()
        stream_area = dsa.DissectedStreamArea(root)
        stream_area.mainloop()



if __name__ == '__main__':
    root = tk.Tk()
    OutputView = OutputView(root)
    AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    OutputView.mainloop()