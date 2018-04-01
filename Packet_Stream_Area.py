import Tkinter as tk


class Example(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.master.title("Packet Stream Area")
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")

        # Vertical Scrollbar
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")

        # Horizontal Scrollbar
        self.vsb2 = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.vsb2.set)
        self.vsb2.pack(side="bottom", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):

        numButton = tk.Button(self.frame, text="No.").grid(row=0, column=0)

        timeButton = tk.Button(self.frame, text="Time", width=10).grid(row=0, column=1)

        sourceButton = tk.Button(self.frame, text="Source", width=10).grid(row=0, column=2)

        destinationButton = tk.Button(self.frame, text="Destination", width=10).grid(row=0, column=3)

        protocolButton = tk.Button(self.frame, text="Protocol").grid(row=0, column=4)

        infoButton = tk.Button(self.frame, text="Info", width=50).grid(row=0, column=5)

        numData = tk.Message(self.frame, text="366\n"
                                         "367\n"
                                         "369\n"
                                         "384\n"
                                         "385\n"
                                         "386\n"
                                         "387",
                             font="System 14", justify='left', aspect=1000).grid(row=1, column=0)

        timeData = tk.Message(self.frame, text="11.767290\n"
                                          "11.768865\n"
                                          "11.775952\n"
                                          "12.286091\n"
                                          "12.312727\n"
                                          "12.361495\n"
                                          "12.361583",
                              font="System 14", justify='left', aspect=1000).grid(row=1, column=1)

        sourceData = tk.Message(self.frame, text="192.168.0.31\n"
                                            "192.168.0.28\n"
                                            "192.168.0.31\n"
                                            "192.168.0.28\n"
                                            "192.168.0.1\n"
                                            "192.168.0.28\n"
                                            "64.236.91.21",
                                font="System 14", justify='left', aspect=1000).grid(row=1, column=2)

        destinationData = tk.Message(self.frame, text="192.168.0.28\n"
                                                 "192.168.0.31\n"
                                                 "192.168.0.28\n"
                                                 "192.168.0.1\n"
                                                 "192.168.0.28\n"
                                                 "64.23691.21\n"
                                                 "192.168.0.28",
                                     font="System 14", justify='left', aspect=1000).grid(row=1, column=3)

        protocolData = tk.Message(self.frame, text="SNMP\n"
                                              "SNMP\n"
                                              "SNMP\n"
                                              "DNS\n"
                                              "DNS\n"
                                              "TCP\n"
                                              "TCP",
                                  font="System 14", justify='left', aspect=1000).grid(row=1, column=4)

        infoData = tk.Message(self.frame, text="get-response SNMPv2-SMI::enterprises.11.2.3.9.4.2.1.4.1.3.7.1\n"
                                          "get-request SNMPv2-SMI::enterprises.11.2.3.9.4.2.1.4.1.5.8.1\n"
                                          "get-response SNMPv2-SMI::enterprises.11.2.3.9.4.2.1.4.1.5.8.1\n"
                                          "Standard query A www.cnn.com\n"
                                          "Standard query response A 64.236.91.21 A 64.236.91.23 A 64.23\n"
                                          "56606 > http [SYN] Seq=0 win=8192 Len=0 MSS=1460 WS=2\n"
                                          "http> 56606 [SYN, ACK] Seq=1 Ack=1 Win=17520 Len=0",
                              font="System 14", justify='left', aspect=1000).grid(row=1, column=5)



    def onFrameConfigure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

