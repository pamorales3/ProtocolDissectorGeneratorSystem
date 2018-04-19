import Tkinter as tk

class RawData(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(fill='both',expand=True)

        main_frame = tk.Frame(self)
        main_frame.grid(row=0,sticky="nsew")

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0,sticky="nsew")

        self.listbox_frame = tk.Frame(main_frame)
        self.listbox_frame.grid(row=1,sticky="nsew")

        # Window min, max,close button, and title
        title = tk.Label(button_frame, text="Raw Data Area", font='System 14 bold', background='lightblue')
        title.grid(row=0,column=0,sticky="nsew")

        minimize = tk.Button(button_frame, text="_", command=self.minimize_button_clicked)
        minimize.grid(row=0,column=1,sticky="nsew")

        maximize = tk.Button(button_frame, text="[ ]",command=self.maximize_button_clicked)
        maximize.grid(row=0,column=2,sticky="nsew")

        close = tk.Button(button_frame, text="X",command=self.close_button_clicked)
        close.grid(row=0,column=3,sticky="nsew")


        packet_data = ["0000   00 1c 26 26 66 a2 00 0e  8e 04 d0 9e 08 00 45 00    ..&&f... ......E.",
                      '0010   00 99 00 00 40 00 40 11  b8 e6 c0 a8 00 01 c0 a8    ....@.@. ........',
                      '0020   00 1c 00 35 f5 98 00 85  98 5a cf 1f 81 80 00 01    ...5.... .Z......',
                      '0030   00 06 00 00 00 00 03 77  77 77 03 63 6e 6e 03 63    .......w ww.cnn.c',
                      '0040   6f 6d 00 00 01 00 01 c0  0c 00 01 00 01 00 00 00    om...... ........']

        self.listbox = tk.Listbox(self.listbox_frame, selectmode='extended', bg='white')
        self.listbox.pack(fill='x',expand=True)

        for data in packet_data:
            self.listbox.insert('end', data)


    def close_button_clicked(self,event=None):
        self.grid_forget()

    def minimize_button_clicked(self, event=None):
        self.listbox_frame.grid_forget()

    def maximize_button_clicked(self,event=None):
        self.listbox_frame.grid(row=1,sticky="nsew")


if __name__ == '__main__':
    root = tk.Tk()
    app=RawData(root)
    app.mainloop()