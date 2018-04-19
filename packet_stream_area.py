import Tkinter as tk
import ttk

class PacketStreamArea(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        main_frame = tk.Frame(self, width=100,height=100)
        main_frame.grid(row=0)
        
        button_frame = tk.Frame(main_frame, width=100,height=100)
        button_frame.grid(row=0,sticky='nsew')

        self.treeview_frame = tk.Frame(main_frame, width=100,height=100)
        self.treeview_frame.grid(row=1, sticky='nsew')

        self.treeview = ttk.Treeview(self.treeview_frame)
        self.treeview.bind("<Double-1>", self.OnDoubleClick)
        self.treeview.pack(fill='both',expand=True)

        # List of tuples for each packet stream, containing the number, time, source, destination, protocol, and info
        packets_list = [("366", "11.767290", "192.168.0.31", "192.168.0.28", "SNMP", "get-response SNMPv2-SMI::enterprises.11.2.3.9.4.2.1.4.1.5.7.1"),
                ("367", "11.768865", "192.168.0.28", "192.168.0.31", "SNMP", "get-request SNMPv2-SMI::enterprises.11.2.3.9.4.2.1.4.1.5.8.1"),
                ("369", "11.775952", "192.168.0.31", "192.168.0.28", "SNMP", "get-response SNMPv2-SMI::enterprises.11.2.3.9.4.2.1.4.1.5.8.1"),
                ("381", "12.286091", "192.168.0.1", "192.168.0.1", "DNS", "Standard query A www.cnn.com"),
                ("384", "12.311862", "192.168.0.1", "192.168.0.28", "DNS", "Standard query response A 64.236.91.21 A 64.236.91.23 A 64.23"),
                ("385", "12.312727", "192.168.0.28", "64.236.91.21", "TCP", "56606 > http [SYN] Seq=0 Win=8192 Len=0 MSS=1460 WS=2"),
                ("386", "12.361495", "64.236.91.21", "192.168.0.28", "TCP", "http > 56606 [SYN, ACK] Seq=0 Ack=1 Win=8192 Len=0 MSS=1460"),
                ("387", "12.361583", "192.168.0.28", "64.236.91.21", "TCP", "56606 > http [ACK] Seq=1 Ack=1 Win=17520 Len=0"),
                ("388", "12.361805", "192.168.0.28", "64.236.91.21", "HTTP", "GET / HTTP/1.1"),
                ("389", "12.413166", "64.236.91.21", "192.168.0.28", "TCP", "http > 56606 [ACK] Seq=1 Ack=845 Win=6960 Len=0"),
                ("390", "12.413611", "64.236.91.21", "192.168.0.28", "TCP", "[TCP segment of a reassembled PDU]"),
                ("391", "12.414386", "64.236.91.21", "192.168.0.28", "TCP", "[TCP segment of a reassembled PDU]")]

        self.treeview['columns'] = ('No.','Time','Source','Destination','Protocol','Info')

        # Window min, max, close button, and title
        title = tk.Label(button_frame, text="Packet Stream Area", font='System 14 bold', background='lightblue')
        title.grid(row=0,column=0)

        minimize = tk.Button(button_frame, text="_", bg="lightblue",command=self.minimize_button_clicked)
        minimize.grid(row=0,column=1)

        maximize = tk.Button(button_frame, text="[ ]",bg='lightblue',command=self.maximize_button_clicked)
        maximize.grid(row=0,column=2)

        close = tk.Button(button_frame, text="X", bg='lightblue',command=self.close_button_clicked)
        close.grid(row=0,column=3)

        #supress the unused identifier column (first column) and keep it out of view
        self.treeview['show'] = 'headings'

        #set up heading and column for the parent tree view: No.
        self.treeview.heading('No.',text='No.',anchor='w')
        self.treeview.column('No.',anchor='w', width=75)

        #set up heading and column for 'Time'
        self.treeview.heading('Time', text='Time')
        self.treeview.column('Time',anchor='w',width=100)

        #set up heading and column for 'Source'
        self.treeview.heading('Source', text='Source')
        self.treeview.column('Source',anchor='w',width=100)

        #set up heading and column for 'Destination'
        self.treeview.heading('Destination', text='Destination')
        self.treeview.column('Destination',anchor='w',width=100)

        #set up heading and column for 'Protocol'
        self.treeview.heading('Protocol', text='Protocol')
        self.treeview.column('Protocol',anchor='w',width=50)

        #set up heading and column for 'Info'
        self.treeview.heading('Info', text='Info')
        self.treeview.column('Info',anchor='w',width=100)

        #populate table
        for packet in packets_list:
            self.treeview.insert('','end',values=((packet[0]),(packet[1]),(packet[2]),(packet[3]),(packet[4]),(packet[5])))

        #Test index access in the tree view
        if(packets_list[0][4] == 'SNMP'):
            print ('SNMP in first packet')

    def close_button_clicked(self,event=None):
        self.grid_forget()

    def minimize_button_clicked(self, event=None):
        self.treeview_frame.grid_forget()

    def maximize_button_clicked(self, event=None):
        self.treeview_frame.grid()

    def OnDoubleClick(self, event):
        item = self.treeview.identify('item',event.x,event.y)
        print("you clicked on", self.treeview.item(item,"text"))

if __name__ == '__main__':
    root = tk.Tk()
    packet_stream_area = PacketStreamArea(root)
    packet_stream_area.mainloop()