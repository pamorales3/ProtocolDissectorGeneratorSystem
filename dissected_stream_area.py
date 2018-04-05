import Tkinter as tk
import ttk


class DissectedStreamArea(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        treeview = ttk.Treeview(self)
        treeview.pack(fill='both', expand=True);

        # Top level ' ' (no name) root node
        # parent, index in the tree, id for item
        treeview.insert('', '0', 'UDP', text='User Datagram Protocol, src Port: domain(53), Dst Port: 62872 (62872)')
        treeview.insert('', '1', 'DNS', text='Domain Name System (response)')
        # end adds it to the end of all the items in the same heirarchy (' ' in this case)
        treeview.insert('', 'end', 'item3', text='Third Item')

        # A child of item1
        treeview.insert('UDP', '0', 'sampleData', text='Sample Data')

        treeview.insert('DNS', '0', 'requestIn', text='[Request In: 381]')
        treeview.insert('DNS', '1', 'time', text='[Time: 0.025771000 seconds]')
        treeview.insert('DNS', '2', 'transactionID', text='Transaction ID: 0xcf1f')
        treeview.insert('DNS', '3', 'flags', text='Flags: 0x8180 (Standard query response, No error')
        treeview.insert('flags', '1', 'sampleData2', text="Sample Data")

        treeview.insert('DNS', '4', 'questions', text='Questions: 1')
        treeview.insert('DNS', '5', 'answer', text='Answer RRs: 1')
        treeview.insert('DNS', '6', 'authority', text='Authority RRs: 0')
        treeview.insert('DNS', '7', 'additional', text='Additional RRs: 0')

        treeview.insert('DNS', '8', 'queries', text='Queries')
        treeview.insert('queries', '0', 'cnn', text='www.cnn.com: type A, class IN')
        treeview.insert('cnn', '0', 'name', text='Name: www.cnn.com')
        treeview.insert('cnn', '1', 'type', text='Type: A (Host address)')
        treeview.insert('cnn', '2', 'class', text='Class: IN (0x0001)')


if __name__ == '__main__':
    root = tk.Tk()
    dissected_area = DissectedStreamArea(root)
    dissected_area.mainloop()
