'''1  # !/usr/bin/env python
2
3  # example table.py
4
5
import pygtk

6
pygtk.require('2.0')
7
import gtk

8
9


class Table:


    10  # Our callback.
11  # The data passed to this method is printed to stdout
12


def callback(self, widget, data=None):
    13
    print "Hello again - %s was pressed" % data


14
15  # This callback quits the program
16


def delete_event(self, widget, event, data=None):
    17
    gtk.main_quit()


18
return False
19
20


def __init__(self):
    21  # Create a new window


22
self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
23
24  # Set the window title
25
self.window.set_title("Table")
26
27  # Set a handler for delete_event that immediately
28  # exits GTK.
29
self.window.connect("delete_event", self.delete_event)
30
31  # Sets the border width of the window.
32
self.window.set_border_width(20)
33
34  # Create a 2x2 table
35
table = gtk.Table(2, 2, True)
36
37  # Put the table in the main window
38
self.window.add(table)
39
40  # Create first button
41
button = gtk.Button("button 1")
42
43  # When the button is clicked, we call the "callback" method
44  # with a pointer to "button 1" as its argument
45
button.connect("clicked", self.callback, "button 1")
46
47
48  # Insert button 1 into the upper left quadrant of the table
49
table.attach(button, 0, 1, 0, 1)
50
51
button.show()
52
53  # Create second button
54
55
button = gtk.Button("button 2")
56
57  # When the button is clicked, we call the "callback" method
58  # with a pointer to "button 2" as its argument
59
button.connect("clicked", self.callback, "button 2")
60  # Insert button 2 into the upper right quadrant of the table
61
table.attach(button, 1, 2, 0, 1)
62
63
button.show()
64
65  # Create "Quit" button
66
button = gtk.Button("Quit")
67
68  # When the button is clicked, we call the main_quit function
69  # and the program exits
70
button.connect("clicked", lambda w: gtk.main_quit())
71
72  # Insert the quit button into the both lower quadrants of the table
73
table.attach(button, 0, 2, 1, 2)
74
75
button.show()
76
77
table.show()
78
self.window.show()
79
80


def main():
    81
    gtk.main()


82
return 0
83
84
if __name__ == "__main__":
    85
    Table()
86
main()'''