"""
.----------------------------------------------------------------------------------.
|                                                                                  |
|  Copyright (C) 2010  Cam Farnell                                                 |
|                                                                                  |
|  This program is free software; you can redistribute it and/or                   |
|  modify it under the terms of the GNU General Public License                     |
|  as published by the Free Software Foundation; either version 2                  |
|  of the License, or (at your option) any later version.                          |
|                                                                                  |
|  This program is distributed in the hope that it will be useful,                 |
|  but WITHOUT ANY WARRANTY; without even the implied warranty of                  |
|  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   |
|  GNU General Public License for more details.                                    |
|                                                                                  |
|  You should have received a copy of the GNU General Public License               |
|  along with this program; if not, write to the Free Software                     |
|  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA. |
|                                                                                  |
`----------------------------------------------------------------------------------'


This code demonstrates a real-world drag and drop.
"""

#Set Verbosity to control the display of information messages:
#    2 Displays all messages
#    1 Displays all but dnd_accept and dnd_motion messages
#    0 Displays no messages
Verbosity = 1

#When you drag an existing object on a canvas, we normally make the original
#    label into an invisible phantom, and what you are ACTUALLY dragging is
#    a clone of the objects label. If you set "LeavePhantomVisible" then you
#    will be able to see the phantom which persists until the object is
#    dropped. In real life you don't want the user to see the phantom, but
#    for demonstrating what is going on it is useful to see it. This topic
#    beaten to death in the comment string for Dragged.Press, below.
LeavePhantomVisible = 0

from Tkinter import *
import Tkdnd
import ttk

# Keeps track of where the mouse cursor is 
def MouseInWidget(Widget,Canvas,Event,Xlate=1):
    """
    Figure out where the cursor is with respect to a Widget on a Canvas.
    
    Both "Widget" and the widget which precipitated "Event" must be
        in the same root window for this routine to work.
        
    We call this routine as part of drawing a DraggedObject inside a
        TargetWidget, eg our Canvas. Since all the routines which need
        to draw a DraggedObject (dnd_motion and it's friends) receive
        an Event, and since an event object contain e.x and e.y values which say
        where the cursor is with respect to the widget you might wonder what all
        the fuss is about; why not just use e.x and e.y? Well it's never
        that simple. The event that gets passed to dnd_motion et al was an
        event against the InitiatingObject and hence what e.x and e.y say is 
        where the mouse is WITH RESPECT TO THE INITIATINGOBJECT. Since we want
        to know where the mouse is with respect to some other object, like the
        Canvas, e.x and e.y do us little good. You can find out where the cursor
        is with respect to the screen (w.winfo_pointerxy) and you can find out
        where it is with respect to an event's root window (e.*_root). So we
        have three locations for the cursor, none of which are what we want.
        Great. We solve this by using w.winfo_root* to find the upper left
        corner of "Widget" with respect to it's root window. Thus we now know
        where both "Widget" and the cursor (e.*_root) are with respect to their
        common root window (hence the restriction that they MUST share a root
        window). Subtracting the two gives us the position of the cursor within
        the widget. 
    """
    x = Event.x_root - Widget.winfo_rootx()
    y = Event.y_root - Widget.winfo_rooty()
    #So far, so good. We now know where the mouse is in the window in which
    #    the canvas resided. BUT, canvas coordinates will be different from window
    #    coordinates if the canvas can scroll and sometimes they are different
    #    just because they are. Ask me how I know. In any case we now translate
    #    from window to canvas coordinates which is a Good Thing.
    if Xlate:
        x = int(round(Canvas.canvasx(x)))
        y = int(round(Canvas.canvasy(y)))
    return (x,y)

# Not needed, displays information
def Blab(Level,Message):
    """
    Display Message if Verbosity says to.
    """
    if Verbosity >= Level:
        print Message
    
class Dragged:
    """
    This is a prototype thing to be dragged and dropped.
    
    Derive from (or mixin) this class to create real draggable objects.
    
    If you derive from this class and want something nicer to represent the
        object on the screen (like an image), you can do so easily by
        overriding the methods WidgetShow and WidgetHide with nethods which
        display whatever you want.
    """
    #We use this to assign a unique number to each instance of Dragged.
    #    This isn't a necessity; we do it so that during the demo you can
    #    tell one instance from another.
    NextNumber = 0
    
    def __init__(self,name,Type='Generic'):
        """
        Create the dragged object.
        
        By default we are a draggable object of drag-type "Generic".
            Pass in a different type if you want. Creating draggable objects of
            different types allows dnd enabled target widgets to be selective
            about which dragged objects they will and won't accept.
        """
        Blab(1, "An instance of Dragged has been created")
        # assert type(Type) == type('')
        self.DragType = Type
        # When created we are not on any canvas
        self.Canvas = None
        self.OriginalCanvas = None
        # This sets where the mouse cursor will be with respect to our label
        self.OffsetX = 0
        self.OffsetY = 0
        # Assign ourselves a unique number
        self.Number = Dragged.NextNumber
        Dragged.NextNumber += 1
        # Use the number to build our name
        self.Name = 'DragObj-%s'%self.Number
        # We don't yet know the nominal size of the label representing us
        self.NominalLabelWidth = None
        self.NominalLabelHeight = None
        # The name of the window to be created
        self.WindowName = name

    def PlaceOnCanvas(self,Canvas,XY):
        """
        Call this method to place us on an arbitrary canvas at location XY.
        
        If we are already on a canvas, then we remove ourselves from that canvas
            before installing ourself on the specified canvas. Probably best not
            to call this method while we are in mid-drag.
            
        This method is handy if you want to place a newly minted draggable object
            directly on a canvas without the user having to drag it there. It 
            will also work if you simply want to move an existing draggable object
            from one canvas to another.    
        """
        #if we are on an existing canvas, then get off of it.
        self.Vanish()
        #draw ourself on the new canvas. Since we are being placed arbitrarily,
        #    we zero the offset.
        self.OffsetX = 0
        self.OffsetY = 0
        self.Appear(Canvas,XY)
        #bind to ButtonPress so user can drag us around
        self.Label.bind('<ButtonPress>',self.Press)
        
    def dnd_end(self,Target,Event):
        """
        This gets called when we are dropped.
        """
        Blab(1, "%s has been dropped; Target=%s"%(self.Name,`Target`))
        if self.Canvas==None and self.OriginalCanvas==None:
            #We were created and then dropped in the middle of nowhere, or
            #    we have been told to self destruct. In either case
            #    nothing needs to be done and we will evaporate shortly.
            return
        if self.Canvas==None and self.OriginalCanvas<>None:
            #We previously lived on OriginalCanvas and the user has
            #   dragged and dropped us in the middle of nowhere. What you do
            #   here rather depends on your own personal taste. There are 2 choices:
            #   1) Do nothing. The dragged object will simply evaporate. In effect
            #      you are saying "dropping an existing object in the middle
            #      of nowhere deletes it".  Personally I don't like this option because
            #      it means that if the user, while dragging an important object, 
            #      twitches their mouse finger as the object is in the middle of
            #      nowhere then the object gets immediately deleted. Oops.
            #   2) Resurrect the original label (which has been there but invisible)
            #      thus saying "dropping an existing dragged object in the middle of
            #      nowhere is as if no drag had taken place". Thats what the code that
            #      follows does.
            self.Canvas = self.OriginalCanvas
            self.ID = self.OriginalID
            self.Label = self.OriginalLabel
            self.WidgetShow(self.Label)
            #If the canvas has an ObjectDict to track dragged objects, make sure we are
            #    listed in it. Since we were dragged off the canvas, we will not be
            #    currently listed, and since we are now popping back up on the canvas,
            #    we should be listed.
            if hasattr(self.Canvas,'ObjectDict') and type(self.Canvas.ObjectDict) == type({}):
                self.Canvas.ObjectDict[self.Name] = self
            return
        #At this point we know that self.Canvas is not None, which means we have an
        #    label of ourself on that canvas. Bind <ButtonPress> to that label so the
        #    the user can pick us up again if and when desired.            
        self.Label.bind('<ButtonPress>',self.Press)
        #If self.OriginalCanvas exists then we were an existing object and our
        #    original label is still around although hidden. We no longer need
        #    it so we delete it.
        if self.OriginalCanvas:
            self.OriginalCanvas.delete(self.OriginalID)
            self.OriginalCanvas = None
            self.OriginalID = None
            self.OriginalLabel = None

    def WidgetShow(self, Widget, Parent=None):
        """
        Arrange for a Widget to represent this instance of dragged.
        
        If Widget is None, then create one, on Parent, and return it as
            the result. 
        
        If Widget is not None it will be a widget, previously created by
            this method, which should be set so it displays our proper
            representation. In this case, Parent need not be given.
            
        To display something fancier than a simple label, override this
            method with your own method which creates however fancy a
            representing widget as you want. You should also override
            method "WidgetHide" below.    
        """
        if self.WindowName == 'field':
            print("Field Window was created and dropped")
            Result = Canvas(Parent,height=270,width=290,bg='white')
            fieldWindow = FieldWindow(Parent)
            Result.create_window(150,140,window=fieldWindow,anchor='center')
        elif self.WindowName == 'startField':
            print("Start Field Window was created and dropped")
            Result = Canvas(Parent,height=130,width=300,bg='white')
            startFieldWindow = StartFieldWindow(Parent)
            Result.create_window(155,70,window=startFieldWindow,anchor='center')
        elif self.WindowName == 'end':
            print("End Window was created and dropped")
            Result = Canvas(Parent, height=35,width=80,bg='white')
            endWindow = EndFieldWindow(Parent)
            Result.create_window(45,25,window=endWindow,anchor='center')
        elif self.WindowName == 'packetInfo':
            print("Packet Information Window was created and dropped")
            Result = Canvas(Parent,height=110,width=350,bg='white')
            packetInfoWindow = PacketInformationWindow(Parent)
            Result.create_window(180,60,window=packetInfoWindow,anchor='center')
        elif self.WindowName == 'referenceList':
            print("Reference List Window was created and dropped")
            Result = Canvas(Parent,height=130,width=350,bg='white')
            referenceListWindow = ReferenceListWindow(Parent)
            Result.create_window(180,70,window=referenceListWindow,anchor='center')
        else:   
            Result = Widget    
        #set it's attributes appropriately    
        #Result['text'] = '%s '%self.Name
        Result['relief'] = RAISED
        Result['borderwidth'] = 2
        return Result
        
    def WidgetHide(self, Widget):    
        """
        Arrange for Widget to be invisible.
        
        Widget will have been previously created by method WidgetShow. On
            exit from this method Widget should still exist on the canvas
            but it should be invisible, ie, no text, no image, no border.
            
        Purely for demonstration purposes, this method pays attention to
            "LeavePhonatoVisible".     
        """
        if LeavePhantomVisible:
            Widget['text'] = '<phantom>'
            Widget['relief']=RAISED
        else:
            Widget['text'] = ''
            Widget['relief']=FLAT
        
    def Appear(self, Canvas, XY):
        """
        Put a label representing this Dragged instance on Canvas.
        
        XY says where the mouse pointer is. We don't, however, necessarily want
            to draw our upper left corner at XY. Why not? Because if the user
            pressed over an existing label AND the mouse wasn't exactly over the
            upper left of the label (which is pretty likely) then we would like
            to keep the mouse pointer at the same relative position inside the
            label. We therefore adjust X and Y by self.OffsetX and self.OffseY
            thus moving our upper left corner up and/or left by the specified
            amounts. These offsets are set to a nominal value when an instance
            of Dragged is created (where it matters rather less), and to a useful
            value by our "Press" routine when the user clicks on an existing
            instance of us.
        """
        if self.Canvas:
            #we are already on a canvas
            self.Vanish()
        self.X, self.Y = XY    
        self.X -= self.OffsetX
        self.Y -= self.OffsetY

        #Note the canvas on which we will draw the label.
        self.Canvas = Canvas
        
        #Create a label which identifies us, including our unique number
        self.Label = self.WidgetShow(None,Canvas)
        #Adjust position, if needed, so our label doesn't fall partly off the canvas
        self.LabelContain()
        #Display the label on a window on the canvas. We need the ID returned by
        #    the canvas so we can move the label around as the mouse moves.
        self.ID = Canvas.create_window(self.X, self.Y, window=self.Label, anchor="nw")
    
        #If canvas has an ObjectDict, then make sure we are listed in it
        if hasattr(self.Canvas,'ObjectDict') and type(self.Canvas.ObjectDict) == type({}):
            self.Canvas.ObjectDict[self.Name] = self

    def Vanish(self,All=0):
        """
        If there is a label representing us on a canvas, make it go away.
        
        if self.Canvas is not None, that implies that "Appear" had prevously
            put a label representing us on the canvas and we delete it.
        
        if "All" is true then we check self.OriginalCanvas and if it not None
            we delete from it the label which represents us.
        """
        if self.Canvas:
            #we have a label on a canvas; delete it
            self.Canvas.delete(self.ID)
            #If canvas has an ObjectDict, then make sure we are not listed in it
            if hasattr(self.Canvas,'ObjectDict') and type(self.Canvas.ObjectDict) == type({}):
                del self.Canvas.ObjectDict[self.Name] 
            #flag that we are not represented on the canvas
            self.Canvas = None
            #Since ID and Label are no longer meaningful, get rid of them lest they
            #confuse the situation later on. Not necessary, but tidy.
            del self.ID
            del self.Label
        
        if All and self.OriginalCanvas:
            #Delete label representing us from self.OriginalCanvas
            self.OriginalCanvas.delete(self.OriginalID)
            self.OriginalCanvas = None
            del self.OriginalID
            del self.OriginalLabel
            #If canvas has an ObjectDict, then make sure we are not listed in it
            if hasattr(self.OriginalCanvas,'ObjectDict') and type(self.OriginalCanvas.ObjectDict) == type({}):
                del self.OriginalCanvas.ObjectDict[self.Name] 

    def Move(self,XY):
        """
        If we have a label on a canvas, then move it to the specified location. 
        
        XY is with respect to the upper left corner of the canvas
        """    
        assert self.Canvas, "Can't move because we are not on a canvas"
        self.X, self.Y = XY
        self.X -= self.OffsetX
        self.Y -= self.OffsetY
        #Adjust position, if needed, so our label doesn't fall partly off the canvas
        self.LabelContain()
        #We've decided where we want the label to be; put it there.    
        self.Canvas.coords(self.ID, self.X, self.Y)

    def LabelContain(self):
        """
        Do adjustment to make sure our label stays fully within the canvas.
        
        Here we do some calculations concerned with what happens when the label which
            represents this dragged object bumps into the edge of the canvas. Note that
            if the mouse is off the canvas then we not called. However, just because the
            mouse is on the canvas doesn't mean that our entire label would be on the 
            canvas if drawn at our current XY coordinates.
        
        If any part of the label would be moved off the canvas, then we move the
            label just enough in the necessary direction so the entire label is on the
            canvas. If such an adjustment is necessary, we also set the offset in the
            corresponding direction to be half the size of the label; this has the effect,
            when the label bumps into the edge (eg when moving from one canvas to another)
            of centering the mouse on the label in that direction.
        """
        #Attempt to get the actual size of our label
        W = self.Label.winfo_width()
        H = self.Label.winfo_height()
        if (W,H) == (1,1):
            #Apparently we don't know the actual size of the label yet.
            if (self.NominalLabelWidth,self.NominalLabelHeight) <> (None,None):
                #But we had a size previously; use that value now
                W = self.NominalLabelWidth
                H = self.NominalLabelHeight
        else:
            #We know the actual size of the label; save it for future use
            self.NominalLabelWidth = W
            self.NominalLabelHeight = H
        CW = self.Canvas.winfo_width()
        CH = self.Canvas.winfo_height()
        #If the canvas is larger than the window, then use the actual size
        T = self.Canvas.bbox('all')
        if T <> None:
            CW = max(T[2] - T[0], CW)
            CH = max(T[3] - T[1], CH)
        #We know the size of the label and the canvas; do the computation.
        if self.X < 0:
            self.X = 0
            self.OffsetX = W/2
        elif self.X+W > CW:
            self.X = CW - W
            self.OffsetX = W/2
        if self.Y < 0:
            self.Y = 0
            self.OffsetY = H/2
        elif self.Y+H> CH:
            self.Y = CH - H
            self.OffsetY = H/2

    def Press(self,Event):
        """
        User has clicked on a label representing us. Initiate drag and drop.
        
        There is a problem, er, opportunity here. In this case we would like to
            act as both the InitiationObject (because the user clicked on us
            and it't up to us to start the drag and drop) but we also want to
            act as the dragged object (because it's us the user wants to drag
            around). If we simply pass ourself to "Tkdnd" as the dragged object
            it won't work because the entire drag and drop process is moved
            along by <motion> events as a result of a binding by the widget
            on which the user clicked. That widget is the label which represents
            us and it get moved around by our "move" method. It also gets
            DELETED by our "vanish" method if the user moves it off the current
            canvas, which is a perfectly legal thing from them to do. If the
            widget which is driving the process gets deleted, the whole drag and
            drop grinds to a real quick halt. We use a little sleight of hand to
            get around this:
            
            o  We take the label which is currently representing us (self.Label)
               and we make it into an invisible phantom by setting its text to ''
               and settings its relief to FLAT. It is now, so to speak, a polar
               bear in a snowstorm. It's still there, but it blends in with the
               rest of then canvas on which it sits. 
            o  We move all the information about the phantom label (Canvas, ID
               and Label) into variables which store information about the 
               previous label (PreviousCanvas, PreviousID and PreviousLabel)
            o  We set self.Canvas and friends to None, which indicates that we 
               don't have a label representing us on the canvas. This is a bit
               of a lie (the phantom is technically on the canvas) but it does no
               harm.
            o  We call "self.Appear" which, noting that don't have a label
               representing us on the canvas, promptly draws one for us, which
               gets saved as self.Canvas etc.
               
        We went to all this trouble so that:
        
            o  The original widget on which the user clicked (now the phantom)
               could hang around driving the drag and drop until it is done, and
            o  The user has a label (the one just created by Appear) which they 
               can drag around, from canvas to canvas as desired, until they 
               drop it. THIS one can get deleted from the current canvas and
               redrawn on another canvas without Anything Bad happening.           

        From the users viewpoint the whole thing is seamless: they think
            the ARE dragging around the original label, but they are not. To 
            make it really clear what is happening, go to the top of the
            code and set "LeavePhantomVisible" to 1. Then when you drag an 
            existing object, you will see the phantom.

        The phantom is resolved by routine "dnd_end" above. If the user 
            drops us on a canvas, then we take up residence on the canvas and
            the phantom label, no longer needed, is deleted. If the user tries
            to drop us in the middle of nowhere, then there will be no
            'current' label for us (because we are in the middle of nowhere)
            and thus we resurrect the phantom label which in this case
            continues to represent us.    

        Note that this whole deal happens ONLY when the user clicks on an
            EXISTING instance of us. In the case where the user clicks over
            the button marked "InitiationObject" then it it that button that
            IS the initiation object, it creates a copy of us and the whole
            opportunity never happens, since the "InitiationObject" button 
            is never in any danger of being deleted.
        """
        Blab(1, "Dragged.press")
        #Save our current label as the Original label
        self.OriginalID = self.ID
        self.OriginalLabel = self.Label
        self.OriginalCanvas = self.Canvas
        #Make the phantom invisible (unless the user asked to see it)
        self.WidgetHide(self.OriginalLabel)
        #Say we have no current label    
        self.ID = None
        self.Canvas = None
        self.Label = None
        #Ask Tkdnd to start the drag operation
        if Tkdnd.dnd_start(self,Event):
            #Save where the mouse pointer was in the label so it stays in the
            #    same relative position as we drag it around
            self.OffsetX, self.OffsetY = MouseInWidget(self.OriginalLabel,self.OriginalCanvas,Event,Xlate=0)
            #Draw a label of ourself for the user to drag around
            XY = MouseInWidget(self.OriginalCanvas,self.OriginalCanvas,Event)
            self.Appear(self.OriginalCanvas,XY)

class CanvasDnd(Canvas):
    """
    A dnd enabled canvas.
    
    A canvas to which we have added those methods necessary so it can
        act as both a TargetWidget and a TargetObject. 
        
    Use (or derive from) this drag-and-drop enabled canvas to create anything
        that needs to be able to receive a dragged object.    
    """    
    def __init__(self, Master, cnf={}, **kw):
        """
        Create the canvas
        
        DropTypes is an optional keyword argument which defaults to ['Generic'].
            It is a tuple or list of drag-object types that this canvas is
            willing to have dropped on it. We default to allowing only draggable
            objects of drag-type "Generic" but pass in your own list to modify
            this behavior. See also the "__init__" routine for Class "Dragged".
        """    
        self.DropTypes = ['Generic']
        if cnf:
            kw.update(cnf)
        if kw.has_key('DropTypes'):
            self.DropTypes = kw['DropTypes']    
            del kw['DropTypes']
        assert type(self.DropTypes) == type([])    
        Canvas.__init__(self, Master, kw)
        #ObjectDict is a dictionary of dragable object which are currently on
        #    this canvas, either because they have been dropped there or because
        #    they are in mid-drag and are over this canvas.
        self.ObjectDict = {}

    #----- TargetWidget functionality -----
    
    def dnd_accept(self,Source,Event):
        """
        Are we willing to accept a dragged object?
        
        Tkdnd is asking us (the TargetWidget) if we want to tell it about a
            TargetObject. Since CanvasDnd is also acting as TargetObject we
            return 'self', saying that we are willing to be the TargetObject.
        """    
        Blab(2, "CanvasDnd: dnd_accept")
        if Source.DragType in self.DropTypes:
            #the Source dragged object is of a type we will accept
            return self
        else:
            #or not
            return None    

    #----- TargetObject functionality -----

    def dnd_enter(self,Source,Event):
        """
        The mouse pointer has entered our canvas.
        
        This is called when the mouse pointer goes from outside the
           Target Widget to inside the Target Widget.
        """
        Blab(1, "CanvasDnd: dnd_enter")
        #Figure out where the mouse is with respect to this widget
        XY = MouseInWidget(self,self,Event)
        #Since the mouse pointer is just now moving over us (the TargetWidget),
        #    we ask the DraggedObject to represent itself on us.
        #    "Source" is the DraggedObject.
        #    "self" is us, the CanvasDnd on which we want the DraggedObject to draw itself.
        #    "XY" is where (on CanvasDnd) that we want the DraggedObject to draw itself.
        Source.Appear(self,XY)
        
    def dnd_leave(self,Source,Event):
        """
        The mouse pointer has left our canvas.
        
        This is called when the mouse pointer goes from inside the
            Target Widget to outside the Target Widget.
        """
        Blab(1, "CanvasDnd: dnd_leave")
        #Since the mouse pointer is just now leaving us (the TargetWidget), we
        #    ask the DraggedObject to remove the representation of itself that it
        #    had previously drawn on us.
        Source.Vanish()
        
    def dnd_motion(self,Source,Event):
        """
        The mouse pointer moved while over our canvas.
        
        This is called when the mouse pointer moves withing the TargetWidget.
        """
        Blab(2, "CanvasDnd: dnd_motion")
        #Figure out where the mouse is with respect to this widget
        XY = MouseInWidget(self,self,Event)
        #Ask the DraggedObject to move it's representation of itself to the
        #    new mouse pointer location.
        Source.Move(XY)
        
    def dnd_commit(self,Source,Event):
        """
        A dragged object is being dropped on us.
        
        This is called if the DraggedObject is being dropped on us.
        
        This demo doesn't need to do anything here (the DraggedObject is
            already in self.ObjectDict) but a real application would
            likely want to do stuff here.
        """
        Blab(1, "CanvasDnd: dnd_commit; Object received= %s"%`Source`)

    #----- code added for demo purposes -----

    def ShowObjectDict(self,Comment):
        """
        Print Comment and then print the present content of our ObjectDict.
        """
        print Comment
        if len(self.ObjectDict) > 0:
            for Name,Object in self.ObjectDict.items():
                print '    %s %s'%(Name,Object)
        else:
            print "    <empty>"    

class TrashBin(CanvasDnd):
    """
    A canvas specifically for deleting dragged objects.
    """
    def __init__(self,Master,**kw):
        """`
        Create the trash bin.
        """
        #Set default height/width if user didn't specify.
        if not kw.has_key('width'):
            kw['width'] =150
        if not kw.has_key('height'):
            kw['height'] = 25    
        CanvasDnd.__init__(self, Master, kw)
        #Put the text "trash" in the middle of the canvas
        X = kw['width'] / 2
        Y = kw['height'] /2
        self.create_text(X,Y,text='TRASH')
    
    def dnd_commit(self,Source,Event):
        """
        Accept an object dropped in the trash.
        
        Note that the dragged object's 'dnd_end' method is called AFTER this
            routine has returned. We call the dragged objects "Vanish(All=1)"
            routine to get rid of any labels it has on any canvas. Having done
            so, it will, at 'dnd_end' time, allow itself to evaporate. If you
            DON'T call "Vanish(All=1)" AND there is a phantom label of the dragged
            object on an OriginalCanvas then the dragged object will think it 
            has been erroniously dropped in the middle of nowhere and it will 
            resurrect itself from the OriginalCanvas label. Since we are trying 
            to trash it, we don't want this to happen.
        """
        Blab(1, "TrashBin: dnd_commit")
        #tell the dropped object to remove ALL labels of itself.
        Source.Vanish(All=1)
        #were a trash bin; don't keep objects dropped on us.
        self.ObjectDict.clear()    

class ToggledFrame(Frame):
    
    def __init__(self, parent, text="", *args, **options):
        Frame.__init__(self, parent, *args, **options)

        self.show = IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=5)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')   

class dissector_builder_area(Frame):
    def __init__(self,master):

        Frame.__init__(self,master)
        #self.title('Python Drag&Drop')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #main_frame = Frame(self, bg='red')
        #main_frame.grid(row=0)

        button_frame = Frame(self, bg='cyan')
        button_frame.grid(row=0,sticky='nsew')

        self.builder_frame = Frame(self, bg='yellow')
        self.builder_frame.grid(row=1, sticky='nsew')

        # Window min, max, close button, and title
        title = Label(button_frame, text="Dissector Builder Area", font='System 14 bold', background='lightblue')
        title.grid(row=0,column=0)

        minimize = Button(button_frame, text="_", command=self.minimize_button_clicked, bg="lightblue")
        minimize.grid(row=0,column=1)

        maximize = Button(button_frame, text="[ ]",bg='lightblue',command=self.maximize_button_clicked)
        maximize.grid(row=0,column=2)

        close = Button(button_frame, text="X", bg='lightblue',command=self.close_button_clicked)
        close.grid(row=0,column=3)

        '''
        ////////////////////////////////////////////////////////////////////////////////////
        /                                  PALETTE SECTION                                 /
        ////////////////////////////////////////////////////////////////////////////////////
        ''' 

         # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self.builder_frame, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self.builder_frame, bd=0, highlightthickness=0,yscrollcommand=vscrollbar.set, bg='green')
        canvas.pack(side=RIGHT, fill=BOTH, expand=FALSE)
        vscrollbar.config(command=canvas.yview)        


        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas, bg='purple')
        interior_id = canvas.create_window(0, 0, window=interior,anchor=NW)


        # Palette min, max, close button, and title
        '''
        palette_title = Label(self.interior, text="Palette", font='System 14 bold', background='lightblue')
        palette_title.grid(row=0,column=0)
        
        palette_minimize = Button(self.interior, text="_")
        palette_minimize.grid(row=0,column=1)

        palette_maximize = Button(self.interior, text="[ ]")
        palette_maximize.grid(row=0,column=2)
        
        palette_close = Button(self.interior, text="X", command=self.palette_close_button)
        palette_close.grid(row=0,column=3)
        '''
        t2 = ToggledFrame(self.interior, text='Field', relief="raised", borderwidth=1)
        t2.grid(row=2,sticky='ns')
        
        construct = ToggledFrame(self.interior, text='Construct', relief="raised", borderwidth=1)
        construct.grid(row=3,sticky='ns')
    
        
        # Field Draggables 
        # You must keep your own reference to the image object or else the image won't always appear
        start = PhotoImage(file="start.gif") 
        InitiationObjectStart = Button(t2.sub_frame,image=start)
        InitiationObjectStart.image = start         # Keep a reference!
        InitiationObjectStart.grid(row=0,column=0)
        InitiationObjectStart.bind('<ButtonPress>', lambda event, n='startField':self.on_dnd_start(event,n))
        
        fieldOne = PhotoImage(file="field1.gif")
        InitiationObjectFieldOne = Button(t2.sub_frame,image=fieldOne)
        InitiationObjectFieldOne.image = fieldOne
        InitiationObjectFieldOne.grid(row=1,column=0)
        InitiationObjectFieldOne.bind('<ButtonPress>',lambda event, n='field':self.on_dnd_start(event,n))
        
        fieldTwo = PhotoImage(file="field2.gif")
        InitiationObjectFieldTwo = Button(t2.sub_frame,image=fieldTwo)
        InitiationObjectFieldTwo.image = fieldTwo
        InitiationObjectFieldTwo.grid(row=2,column=0)
        InitiationObjectFieldTwo.bind('<ButtonPress>',lambda event, n='field':self.on_dnd_start(event,n))

        fieldFour = PhotoImage(file="field4.gif")
        InitiationObjectFieldFour = Button(t2.sub_frame,image=fieldFour)
        InitiationObjectFieldFour.image = fieldFour
        InitiationObjectFieldFour.grid(row=3,column=0)
        InitiationObjectFieldFour.bind('<ButtonPress>',lambda event, n='field':self.on_dnd_start(event,n))

        fieldSixteen = PhotoImage(file="field16.gif")
        InitiationObjectFieldSixteen = Button(t2.sub_frame,image=fieldSixteen)
        InitiationObjectFieldSixteen.image = fieldSixteen
        InitiationObjectFieldSixteen.grid(row=4,column=0)
        InitiationObjectFieldSixteen.bind('<ButtonPress>',lambda event, n='field':self.on_dnd_start(event,n))

        fieldVar = PhotoImage(file="fieldVar.gif")
        InitiationObjectFieldVar = Button(t2.sub_frame,image=fieldVar)
        InitiationObjectFieldVar.image = fieldVar
        InitiationObjectFieldVar.grid(row=0,column=1)
        InitiationObjectFieldVar.bind('<ButtonPress>',lambda event, n='field':self.on_dnd_start(event,n))

        packet = PhotoImage(file="packet.gif")
        InitiationObjectPacket = Button(t2.sub_frame,image=packet)
        InitiationObjectPacket.image = packet
        InitiationObjectPacket.grid(row=1,column=1)
        InitiationObjectPacket.bind('<ButtonPress>',lambda event, n='packetInfo':self.on_dnd_start(event,n))

        reference = PhotoImage(file="Reference.gif")
        InitiationObjectReference = Button(t2.sub_frame,image=reference)
        InitiationObjectReference.image = reference
        InitiationObjectReference.grid(row=2,column=1)
        InitiationObjectReference.bind('<ButtonPress>',lambda event, n='referenceList':self.on_dnd_start(event,n))

        end = PhotoImage(file="end.gif")
        InitiationObjectEnd = Button(t2.sub_frame,image=end)
        InitiationObjectEnd.image = end
        InitiationObjectEnd.grid(row=3,column=1)
        InitiationObjectEnd.bind('<ButtonPress>',lambda event, n='end':self.on_dnd_start(event,n))

        # Construct Draggables 
        
        expression = PhotoImage(file="expression.gif") 
        expression = expression.subsample(3,3)
        InitiationObjectExpression = Button(construct.sub_frame,image=expression)
        InitiationObjectExpression.image = expression
        InitiationObjectExpression.grid(row=0)
        InitiationObjectExpression.bind('<ButtonPress>',self.on_dnd_start)

        connector = PhotoImage(file="connector.gif")
        connector = connector.subsample(3,3) 
        InitiationObjectConnector = Button(construct.sub_frame,image=connector)
        InitiationObjectConnector.image = connector
        InitiationObjectConnector.grid(row=1)
        InitiationObjectConnector.bind('<ButtonPress>',self.on_dnd_start)

        InitiationObjectRelational = Label(construct.sub_frame,text="Relational: ")
        InitiationObjectRelational.grid(row=2)
        
        less = PhotoImage(file="less.gif") 
        less = less.subsample(4,4)
        InitiationObjectLess = Button(construct.sub_frame,image=less)
        InitiationObjectLess.image = less
        InitiationObjectLess.grid(row=3,column=0)
        InitiationObjectLess.bind('<ButtonPress>',self.on_dnd_start)

        gtr = PhotoImage(file="greater.gif") 
        gtr = gtr.subsample(4,4)
        InitiationObjectGtr = Button(construct.sub_frame,image=gtr)
        InitiationObjectGtr.image = gtr
        InitiationObjectGtr.grid(row=3,column=1)
        InitiationObjectGtr.bind('<ButtonPress>',self.on_dnd_start)

        lessEqual = PhotoImage(file="greater.gif") 
        lessEqual = lessEqual.subsample(4,4)
        InitiationObjectLessEqual = Button(construct.sub_frame,image=lessEqual)
        InitiationObjectLessEqual.image = lessEqual
        InitiationObjectLessEqual.grid(row=3,column=2)
        InitiationObjectLessEqual.bind('<ButtonPress>',self.on_dnd_start)

        greaterEqual = PhotoImage(file="greaterequal.gif") 
        greaterEqual = greaterEqual.subsample(4,4)
        InitiationObjectGreaterEqual = Button(construct.sub_frame,image=greaterEqual)
        InitiationObjectGreaterEqual.image = greaterEqual
        InitiationObjectGreaterEqual.grid(row=4,column=0)
        InitiationObjectGreaterEqual.bind('<ButtonPress>',self.on_dnd_start)

        equal = PhotoImage(file="equal.gif") 
        equal = equal.subsample(4,4)
        InitiationObjectEqual = Button(construct.sub_frame,image=equal)
        InitiationObjectEqual.image = equal
        InitiationObjectEqual.grid(row=4,column=1)
        InitiationObjectEqual.bind('<ButtonPress>',self.on_dnd_start)

        nand = PhotoImage(file="nand.gif") 
        nand = nand.subsample(4,4)
        InitiationObjectNand = Button(construct.sub_frame,image=nand)
        InitiationObjectNand.image = nand
        InitiationObjectNand.grid(row=4,column=2)
        InitiationObjectNand.bind('<ButtonPress>',self.on_dnd_start)

        InitiationObjectLogical = Label(construct.sub_frame,text="Logical: ")
        InitiationObjectLogical.grid(row=5)

        andop = PhotoImage(file="and.gif") 
        andop = andop.subsample(4,4)
        InitiationObjectAndop = Button(construct.sub_frame,image=andop)
        InitiationObjectAndop.image = andop
        InitiationObjectAndop.grid(row=6,column=0)
        InitiationObjectAndop.bind('<ButtonPress>',self.on_dnd_start)

        orop = PhotoImage(file="or.gif") 
        orop = orop.subsample(4,4)
        InitiationObjectOrop = Button(construct.sub_frame,image=orop)
        InitiationObjectOrop.image = orop
        InitiationObjectOrop.grid(row=6,column=1)
        InitiationObjectOrop.bind('<ButtonPress>',self.on_dnd_start)

        notop = PhotoImage(file="not.gif") 
        notop = notop.subsample(4,4)
        InitiationObjectNotop = Button(construct.sub_frame,image=notop)
        InitiationObjectNotop.image = notop
        InitiationObjectNotop.grid(row=6,column=2)
        InitiationObjectNotop.bind('<ButtonPress>',self.on_dnd_start)

        oper = PhotoImage(file="oper.gif") 
        oper = oper.subsample(4,4)
        InitiationObjectOper = Button(construct.sub_frame,image=oper)
        InitiationObjectOper.image = oper
        InitiationObjectOper.grid(row=7,)
        InitiationObjectOper.bind('<ButtonPress>',self.on_dnd_start)
        
        '''
        Trash = TrashBin(self, relief=RAISED,bd=2)
        Trash.pack(expand=NO)
        '''

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        TargetWidget_TargetObject = CanvasDnd(self.builder_frame,relief=RAISED,bd=2,height=380,width=780)
        TargetWidget_TargetObject.pack(side=LEFT)

        hbar=Scrollbar(self.builder_frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=TargetWidget_TargetObject.xview)

        vbar=Scrollbar(self.builder_frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=TargetWidget_TargetObject.yview)

        TargetWidget_TargetObject.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        
        #T = Dragged('field')
        #T.PlaceOnCanvas(TargetWidget_TargetObject,(100,100))
        
        #self.master.mainloop()

    def on_dnd_start(self,Event,name):
        """
        This is invoked by InitiationObject to start the drag and drop process.
        """
        #Create an object to be dragged
        ThingToDrag = Dragged(name)
        #Pass the object to be dragged and the event to Tkdnd
        Tkdnd.dnd_start(ThingToDrag,Event)

    def ShowObjectDicts():
        """
        Some demo code to let the user see what ojects we think are
            on each of the three canvases.
        
        The only reason we display the content of the trash bin is to show that it
            has no objects, even after some have been dropped on it.
        """
        TargetWidget_TargetObject.ShowObjectDict('UpperCanvas')
        TargetWidget_TargetObject2.ShowObjectDict('LowerCanvas')
        Trash.ShowObjectDict('Trash bin')
        print '----------'


    def close_button_clicked(self,event=None):
        self.master.grid_forget()

    def maximize_button_clicked(self,event=None):
        self.builder_frame.grid()

    def minimize_button_clicked(self, event=None):
        self.builder_frame.grid_forget()

class FieldWindow(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        REF_OPTIONS = ["Reference List 1", 'Reference List 2', 'Reference List 3']
        BASE_OPTIONS = ['1', '2', '4', '8', '16', '32', '64', '128', '256', '1024']
        DATA_TYPE_OPTIONS = ["Int", 'Str', 'Double']

        self.fieldWindow = Frame(self, bg='lightblue')
        self.fieldWindow.pack()
        titleFrame = Frame(self.fieldWindow,bg='lightblue')
        self.infoFrame = Frame(self.fieldWindow, bg='white')

        titleFrame.grid(row=0)
        self.infoFrame.grid(row=1)

        # Window Title and Buttons
        title = Label(titleFrame,text='Field',font='System 14 bold',bg='lightblue')
        title.grid(row=0,column=0,sticky='w')
        
        titleMin = Button(titleFrame,text='_',font='System 12 bold',bg='lightblue',command=self.close_window)
        titleMin.grid(row=0,column=1,sticky='w')

        titleMax = Button(titleFrame,text='[ ]',font='System 12 bold',bg='lightblue',command=self.expand_window)
        titleMax.grid(row=0,column=2,sticky='w')

        # Field Name Label
        name = Label(self.infoFrame,text='Name',font='System 10 bold',bg='white')
        name.grid(row=0,column=0)
        # Field Name Entry 
        nameEntry = Entry(self.infoFrame,font='System 10',bg='white')
        nameEntry.grid(row=0,column=1,sticky='ew')

        # Field Abbreviation Label
        abbreviation = Label(self.infoFrame, text='Abbreviation',font='System 10 bold',bg='white')
        abbreviation.grid(row=1,column=0)
        # Field Abbreviation Entry 
        abbreviationEntry = Entry(self.infoFrame,font='System 10',bg='white')
        abbreviationEntry.grid(row=1,column=1,sticky='ew',)

        # Field Description Label
        description = Label(self.infoFrame, text='Description',font='System 10 bold',bg='white')
        description.grid(row=2,column=0)
        # Field Description Entry
        descriptionEntry = Entry(self.infoFrame,font='System 10', width=30,bg='white')
        descriptionEntry.grid(row=2,column=1)

        # Field Reference List Label
        referenceList = Label(self.infoFrame, text='Reference List',font='System 10 bold',bg='white')
        referenceList.grid(row=3,column=0)
        # Field Reference List Option Menu
        ref = StringVar(self.infoFrame)
        ref.set(REF_OPTIONS[0]) # default value
        referenceListMenu = OptionMenu(self.infoFrame, ref, *REF_OPTIONS)
        referenceListMenu.grid(row=3,column=1,sticky='ew')

        # Field Data Type Label
        dataType = Label(self.infoFrame, text='Data Type',font='System 10 bold',bg='white')
        dataType.grid(row=4,column=0)
        # Field Data Type Option Menu
        data = StringVar(self.infoFrame)
        data.set(DATA_TYPE_OPTIONS[0]) # default value
        dataTypeMenu = OptionMenu(self.infoFrame, data, *DATA_TYPE_OPTIONS)
        dataTypeMenu.grid(row=4,column=1,sticky='ew')

        # Field Base Type Label
        baseType = Label(self.infoFrame, text='Base Type',font='System 10 bold',bg='white')
        baseType.grid(row=5,column=0)
        # Field Base Type Option Menu
        base = StringVar(self.infoFrame)
        base.set(BASE_OPTIONS[0]) # default value
        baseType = OptionMenu(self.infoFrame, base, *BASE_OPTIONS)
        baseType.grid(row=5,column=1,sticky='ew')

        # Field Mask Label
        mask = Label(self.infoFrame, text='Mask',font='System 10 bold',bg='white')
        mask.grid(row=6,column=0)
        # Field Mask Entry 
        maskEntry = Entry(self.infoFrame,font='System 10',bg='white')
        maskEntry.grid(row=6,column=1)

        # Field Value Constraint
        valueConstraint = Label(self.infoFrame, text='Value Constraint',font='System 10 bold',bg='white')
        valueConstraint.grid(row=7,column=0)
        # Field Value Constraint Entry
        valueConstraintEntry = Entry(self.infoFrame,font='System 10',bg='white')
        valueConstraintEntry.grid(row=7,column=1)

        # Field Required
        required = Label(self.infoFrame, text='Required',font='System 10 bold',bg='white')
        required.grid(row=8,column=0)
        # Field Required Checkbox
        requiredCheckBox = Checkbutton(self.infoFrame)
        requiredCheckBox.grid(row=8,column=1)

    def close_window(self):
        self.infoFrame.grid_forget()

    def expand_window(self):
        self.infoFrame.grid()

class StartFieldWindow(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        startFieldWindow = Frame(self,bg='lightblue')
        titleFrame = Frame(startFieldWindow,bg='lightblue')
        self.infoFrame = Frame(startFieldWindow, bg='white')

        startFieldWindow.pack()
        titleFrame.grid(row=0)
        self.infoFrame.grid(row=1)

        # Window Title and Buttons
        title = Label(titleFrame,text='Start Field',font='System 14 bold',bg='lightblue')
        title.grid(row=0,column=0,sticky='w')
        
        titleMin = Button(titleFrame,text='_',font='System 12 bold',bg='lightblue',command=self.close_window)
        titleMin.grid(row=0,column=1,sticky='w')

        titleMax = Button(titleFrame,text='[ ]',font='System 12 bold',bg='lightblue',command=self.expand_window)
        titleMax.grid(row=0,column=2,sticky='w')

        # Start Field - Protocol Name Label
        protocolName = Label(self.infoFrame,text='Protocol Name',font='System 10 bold',bg='white')
        protocolName.grid(row=1,column=0)
        # Start Field - Protocol Name Entry 
        protocolNameEntry = Entry(self.infoFrame,font='System 10',bg='white')
        protocolNameEntry.grid(row=1,column=1,sticky='ew')

        # Start Field - Protocol Description Label
        protocolDescription = Label(self.infoFrame, text='Protocol Description',font='System 10 bold',bg='white')
        protocolDescription.grid(row=2,column=0)
        # Start Field - Protocol Description Entry 
        protocolDescriptionEntry = Entry(self.infoFrame,font='System 10',bg='white')
        protocolDescriptionEntry.grid(row=2,column=1,sticky='ew',)

        # Start Field - Dependent Protocol Name Label
        dependentProtocolName = Label(self.infoFrame, text='Dependent Protocol Name',font='System 10 bold',bg='white')
        dependentProtocolName.grid(row=3,column=0)
        # Start Field - Dependent Protocol Name Entry
        dependentProtocolNameEntry = Entry(self.infoFrame,font='System 10',bg='white')
        dependentProtocolNameEntry.grid(row=3,column=1)

        # Start Field - Dependency Pattern Label
        dependencyPattern = Label(self.infoFrame, text='Dependency Pattern',font='System 10 bold',bg='white')
        dependencyPattern.grid(row=4,column=0)
        # Start Field - Dependency Pattern Entry
        dependencyPatternEntry = Entry(self.infoFrame,font='System 10',bg='white')
        dependencyPatternEntry.grid(row=4,column=1)

    def close_window(self):
        self.infoFrame.grid_forget()

    def expand_window(self):
        self.infoFrame.grid()

class EndFieldWindow(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        endFieldWindow = Frame(self,bg='lightblue')
        endFieldWindow.pack()
        title = Label(endFieldWindow,text='End Field',font='System 14 bold',bg='lightblue')
        title.grid(row=0)

class PacketInformationWindow(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        self.r = 3
        
        main = Frame(self,bg='lightblue')
        title = Frame(main,bg='lightblue')
        self.packetInfo = Frame(main,bg='white')
        
        main.pack()
        title.grid(row=0)
        self.packetInfo.grid(row=1)

        titleLabel = Label(title,text='Packet Information',font='System 14 bold',bg='lightblue')
        titleLabel.grid(row=0,column=0,sticky='w')

        titleMin = Button(title,text='_',font='System 12 bold',bg='lightblue',command=self.close_window)
        titleMin.grid(row=0,column=1,sticky='w')

        titleMax = Button(title,text='[ ]',font='System 12 bold',bg='lightblue',command=self.expand_window)
        titleMax.grid(row=0,column=2,sticky='w')
        
        # Value Label
        valueLabel = Label(self.packetInfo, text="Value",font='System 12 bold',bg='white')
        valueLabel.grid(row=0,column=0,sticky='nesw')
        
        # Text Description Label
        textDescription = Label(self.packetInfo, text='Text Description',font='System 12 bold',bg='white')
        textDescription.grid(row=0,column=1,sticky='nesw')      
        
        # Value and Text Description Entry 
        Entry(self.packetInfo,font='System 12',bg='white').grid(row=1, column=0)        
        Entry(self.packetInfo,font='System 12',bg='white').grid(row=1, column=1)
        
        Button(self.packetInfo, text='+', bg='white',command=self.addInfo).grid(row=10, column=1, sticky='e')

    def close_window(self):
        self.packetInfo.grid_forget()

    def expand_window(self):
        self.packetInfo.grid()

    def addInfo(self):
        Entry(self.packetInfo,font='System 12',bg='white').grid(row=self.r,column=0)
        Entry(self.packetInfo,font='System 12',bg='white').grid(row=self.r,column=1)
        self.r += 1

class ReferenceListWindow(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        self.x = 3
        
        referenceList = Frame(self,bg='lightblue')
        title = Frame(referenceList,bg='lightblue')
        self.infoFrame = Frame(referenceList,bg='white')
        
        referenceList.pack()
        title.grid(row=0)
        self.infoFrame.grid(row=2)

        # Window Title and Buttons
        
        titleLabel = Label(title,text='Reference List',font='System 14 bold',bg='lightblue')
        titleLabel.grid(row=0,column=0,sticky='w')
        
        titleMin = Button(title,text='_',font='System 12 bold',bg='lightblue',command=self.close_window)
        titleMin.grid(row=0,column=1,sticky='w')

        titleMax = Button(title,text='[ ]',font='System 12 bold',bg='lightblue',command=self.expand_window)
        titleMax.grid(row=0,column=2,sticky='w')
        
        
        referenceLabel = Label(self.infoFrame, text="Reference List Name",font='System 12 bold',bg='white')
        referenceLabel.grid(row=0,column=0,sticky='nesw')
        
        referenceEntry = Entry(self.infoFrame,bg='white',font='System 10')
        referenceEntry.grid(row=0,column=1,sticky='we')     
        
         # Value Label
        valueLabel = Label(self.infoFrame, text="Value",font='System 12 bold',bg='white')
        valueLabel.grid(row=1,column=0,sticky='nesw')

        # Text Description Label
        textDescription = Label(self.infoFrame, text='Text Description',font='System 12 bold',bg='white')
        textDescription.grid(row=1,column=1,sticky='nesw')    
        
        Entry(self.infoFrame,bg='white',font='System 12').grid(row=2, column=0)        
        Entry(self.infoFrame,bg='white',font='System 12').grid(row=2, column=1)
        
        Button(self.infoFrame, text='+', command=self.add).grid(row=10, column=1, sticky='e')

    def add(self):
        Entry(self.infoFrame,bg='white',font='System 12').grid(row=self.x, column=0) 
        Entry(self.infoFrame,bg='white',font='System 12').grid(row=self.x, column=1) 
        self.x+=1

    def close_window(self):
        self.infoFrame.grid_forget()

    def expand_window(self):
        self.infoFrame.grid()


if __name__ == "__main__":

    root = Tk()
    app = dissector_builder_area(root)
    app.mainloop()