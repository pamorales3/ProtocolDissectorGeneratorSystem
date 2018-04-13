import Tkinter as tk
import ttk


class DissectedStreamArea(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        main_frame = tk.Frame(self)
        main_frame.grid(row=0)

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0)

        treeview_frame = tk.Frame(main_frame)
        treeview_frame.grid(row=1)

        self.treeview = ttk.Treeview(treeview_frame)
        self.treeview.grid(row=0)

        # Window min, max,close button, and title
        title = tk.Label(button_frame, text="Dissected Stream Area", font='System 14 bold', background='lightblue')
        title.grid(row=0,column=0)

        minimize = tk.Button(button_frame, text="_", command=self.minimize_button_clicked, bg="lightblue")
        minimize.grid(row=0,column=1)

        maximize = tk.Button(button_frame, text="[ ]",bg='lightblue')
        maximize.grid(row=0,column=2)

        close = tk.Button(button_frame, text="X", bg='lightblue',command=self.close_button_clicked)
        close.grid(row=0,column=3)

        # Top level ' ' (no name) root node
        # parent, index in the tree, id for item
        self.treeview.insert('', '0', 'UDP', text='User Datagram Protocol, src Port: domain(53), Dst Port: 62872 (62872)')
        self.treeview.insert('', '1', 'DNS', text='Domain Name System (response)')
        # end adds it to the end of all the items in the same heirarchy (' ' in this case)
        self.treeview.insert('', 'end', 'item3', text='Third Item')

        # A child of item1
        self.treeview.insert('UDP', '0', 'sampleData', text='Sample Data')

        self.treeview.insert('DNS', '0', 'requestIn', text='[Request In: 381]')
        self.treeview.insert('DNS', '1', 'time', text='[Time: 0.025771000 seconds]')
        self.treeview.insert('DNS', '2', 'transactionID', text='Transaction ID: 0xcf1f')
        self.treeview.insert('DNS', '3', 'flags', text='Flags: 0x8180 (Standard query response, No error')
        self.treeview.insert('flags', '1', 'sampleData2', text="Sample Data")

        self.treeview.insert('DNS', '4', 'questions', text='Questions: 1')
        self.treeview.insert('DNS', '5', 'answer', text='Answer RRs: 1')
        self.treeview.insert('DNS', '6', 'authority', text='Authority RRs: 0')
        self.treeview.insert('DNS', '7', 'additional', text='Additional RRs: 0')

        self.treeview.insert('DNS', '8', 'queries', text='Queries')
        self.treeview.insert('queries', '0', 'cnn', text='www.cnn.com: type A, class IN')
        self.treeview.insert('cnn', '0', 'name', text='Name: www.cnn.com')
        self.treeview.insert('cnn', '1', 'type', text='Type: A (Host address)')
        self.treeview.insert('cnn', '2', 'class', text='Class: IN (0x0001)')

    def close_button_clicked(self,event=None):
        self.grid_forget()

    def minimize_button_clicked(self, event=None):
        print("Minimize was press!")


if __name__ == '__main__':
    root = tk.Tk()
    dissected_area = DissectedStreamArea(root)
    dissected_area.mainloop()
