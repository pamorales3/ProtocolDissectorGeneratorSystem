import Tkinter as tk

class App(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pack()
        self.master.title("Raw Data Area")
        self.master.resizable(True,True)
        self.master.tk_setPalette('#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight())/3
        #center the frame on the screen
        self.master.geometry("+{}+{}".format(x,y))

        self.master.config(menu=tk.Menu(self))

        window_prompt = tk.Message(self, text="[+] User Datagram Protocol, Src Port: domain (53), Dst Port: 62872 (62872)\n"
                                              "[-] Domain Name System (response)\n"
                                              "        [Request In: 831]\n"
                                              "        [Time: 0.025771000 seconds]\n"
                                              "        Transaction ID: 0xcf1f\n"
                                              "    [+] Flags: 0x8180 (Standard query response, No error)\n"
                                              "        Questions: 1\n"
                                              "        Answer RRs: 6\n"
                                              "        Authority RRs: 0\n"
                                              "        Additional RRs: 0\n"
                                              "    [-] Queries\n"
                                              "        [-] www.cnn.com: type A, class IN\n"
                                              "               Name: www.ccn.com\n"
                                              "               Type: A (Host address)\n"
                                              "               Class: IN (0x0001)"

                                   , font="System 14", justify='left',aspect=1200)
        window_prompt.pack(pady=(50, 50))


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()