from tkinter import *

import threading
import time
from PIL import ImageTk, Image  
import datetime

import json

'''
class ResizingCanvas(Canvas):
    
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)
'''


class FrontendGUI:

    def __init__(self, net_client):

        self.width = 1920
        self.height = 1080

        self.root = Tk()
        self.root.geometry(str(self.width)+"x"+str(self.height))
        self.root.title("90sNet")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=YES)

        # Base canvas
        self.canvas = Canvas(self.main_frame, 
                    width=self.width, 
                    height=self.height, 
                    bg="#202225",
                    bd=0, 
                    highlightthickness=0, 
                    relief='ridge')
        self.canvas.pack(fill=BOTH, expand=YES)

        # Score Display

        self.scoreboard = Text(self.canvas, height = 44,
                    width = 60,
                    highlightbackground="#36393f",
                    relief="flat",
                    bg = "blue",
                    fg="white",
                    highlightthickness = 0,
                    font=("Free Mono Bold", 10),
                    state=DISABLED)
        self.scoreboard.grid(row=0, column=0, sticky='w')

        # Console user input
        self.console = Text(self.canvas,
                    width = 240,
                    height = 15,
                    highlightbackground="#36393f",
                    relief="flat",
                    bg = "#000000",
                    fg="white",
                    highlightthickness = 0,
                    font=("Free Mono Bold", 10,))
        self.console.grid(row=1, column=0, columnspan = 3, sticky='s')

        # canvas that displays map and nodes
        self.map_canvas = Canvas(self.canvas,
                    width=750,
                    height=750,
                    bg="red")
        self.map_canvas.grid(row=0, column=1, sticky='n')

        # Map image
        image = Image.open("FrontendCore/uc_map.png")
        image = image.resize((750,750), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(image)
        self.map_canvas.create_image(0,0,image=pic, anchor="nw")

        # Nodes
        with open("FrontendCore/nodes.json") as json_file:
            self.node_data = json.load(json_file)
        print(self.node_data)
        for name, data in self.node_data.items():
            r = 7
            x0 = data['location'][0] - r
            y0 = data['location'][1] - r
            x1 = data['location'][0] + r
            y1 = data['location'][1] + r
            o = self.map_canvas.create_oval(x0, y0, x1, y1, fill="blue")
            #self.map_canvas.tag_raise(o, self.image_item)

        # Event stream
        ## Canvas
        self.event_stream_container = Canvas(self.canvas,
                    height = 750,
                    width = 500,
                    bg = "green",
                    relief=SUNKEN,
                    scrollregion=(0, 0, 400, 9000))
        self.event_stream_container.grid(row=0, column=2, sticky='e')
        self.event_stream_container.grid_propagate(0)
        

        
        ## Scroll bar
        yscrollbar = Scrollbar(self.canvas, orient="vertical", command=self.event_stream_container.yview)
        yscrollbar.grid(row=0, column=3, sticky="ns")
        self.event_stream_container.configure(yscrollcommand=yscrollbar.set)

        self.event_stream_container.bind_all('<4>', lambda event: self.event_stream_container.yview_scroll(-1, "units"))
        self.event_stream_container.bind_all('<5>', lambda event: self.event_stream_container.yview_scroll(1, "units"))
        
        ## Frame
        self.event_stream_frame = Frame(self.event_stream_container,
                    bg='purple')
        self.event_stream_container.create_window((0,0), window=self.event_stream_frame, anchor="nw")
        
        # Net thread
        self.net_client = net_client
        self.event_stream_thread = threading.Thread(target=self.update_gui, args=[])
        self.event_stream_thread.start()

        mainloop()
    
    def write_to(self,tk_object, text):
        tk_object.config(state=NORMAL)
        tk_object.insert(END, text + "\n")
        tk_object.see("end")
        tk_object.config(state=DISABLED)

    def display_event(self, time_stamp, event):
        event_text = "{}: {}\nDetail: {}\n{}".format(str(datetime.datetime.fromtimestamp(float(time_stamp)))[-15:-7], event, "text", " "*60)
        new_event = Message(self.event_stream_frame,
                    fg="white",
                    bg="blue",
                    font=("Free Mono", 10, "bold"),
                    width=470,
                    text=event_text)
        last_row = self.event_stream_frame.grid_size()[1]
        new_event.grid(row=last_row, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='n')
        self.event_stream_container.config(scrollregion= self.event_stream_container.bbox("all"))
        self.event_stream_container.yview_moveto(1)
        


    def update_gui(self):
        time_last_event = 0
        while True:
            # get updated events from server
            new_events, time_last_event = self.net_client.getEventsSince(time_last_event)
            # for each event, update display as needed
            for time_stamp, event in new_events.items():
                # update event stream
                self.display_event(time_stamp, event)
                # TODO: update map dots
                # TODO: update scoreboard
            time.sleep(5)
    




    '''
    # Function is run as own thread to get information and update gui. Should be its own file to be honest, or diff functions
    def update_event_stream(self):
        last_time = 0 # default to get all events since start of server
        while True:
            # command json that is sent to the server
            event_command = {
                "command":"getEventsSince",
                "args":[float(last_time)]
            }
            # send command and get events
            new_events = self.net_client.send_and_receive(json.dumps(event_command))

            # Not great, new_events is received as json string. Empty json is "{}" with len of 2. Only run this if not empty
            if len(new_events) > 2:
                new_events_dict = json.loads(new_events)
                last_time = list(new_events_dict)[-1] # gets the time of the last event
                self.net_client.event_list += [new_events_dict] # loads events into event manager. also not the best way of doing this. Fix to have better separation of duty between classes
                {self.write_to(self.event_stream, "{}: {}".format(t,e)) for (t,e) in new_events_dict.items()} # using dict comprehension as a loop. Funny, but not great practice. This just adds thing to the tk textbox

            time.sleep(10)
    '''