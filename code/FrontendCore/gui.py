from tkinter import *

import threading
import time

import json

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


class FrontendGUI:

    def __init__(self, net_client):

        self.width = 960
        self.height = 540

        self.root = Tk()
        self.root.geometry(str(self.width)+"x"+str(self.height))
        self.root.title("Map")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=YES)

        self.canvas = ResizingCanvas(self.main_frame, 
                    width=self.width, 
                    height=self.height, 
                    bg="#202225",
                    bd=0, 
                    highlightthickness=0, 
                    relief='ridge')
        self.canvas.pack(fill=BOTH, expand=YES)

        self.event_stream = Text(self.canvas, height = 28,
                    width = 95,
                    highlightbackground="#36393f",
                    relief="flat",
                    bg = "#202225",
                    fg="white",
                    highlightthickness = 0,
                    font=("Uni Sans", 10),
                    state=DISABLED)
        self.event_stream.pack(fill=BOTH, expand=YES)

        self.canvas.addtag_all("all")

        self.net_client = net_client
        self.event_stream_thread = threading.Thread(target=self.update_event_stream, args=[])
        self.event_stream_thread.start()

        mainloop()
    
    def write_to(self,tk_object, text):
        tk_object.config(state=NORMAL)
        tk_object.insert(END, text + "\n")
        tk_object.see("end")
        tk_object.config(state=DISABLED)

    def update_event_stream(self):
        
        last_time = 0
        while True:
            event_command = {
                "command":"getEventsSince",
                "args":[float(last_time)]
            }
            new_events = self.net_client.send_and_receive(json.dumps(event_command))
            if len(new_events) > 2:
                new_events_dict = json.loads(new_events)
                last_time = list(new_events_dict)[-1]
                self.net_client.event_list += [new_events_dict]
                {self.write_to(self.event_stream, "{}: {}".format(t,e)) for (t,e) in new_events_dict.items()}

            time.sleep(10)