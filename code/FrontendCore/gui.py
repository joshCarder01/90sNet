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

        self.colors = {
            'darkest':"#181818",
            'top_bar':"#222222",
            'main_text':"#202020",
            'light_tb':"#313131"
        }

        # Base canvas
        self.canvas = Canvas(self.main_frame, 
                    width=self.width, 
                    height=self.height, 
                    bg=self.colors['darkest'],
                    #bg='green',
                    bd=0, 
                    highlightthickness=0, 
                    relief='ridge')
        self.canvas.pack(fill=BOTH, expand=YES)

        # Score Display
        self.scoreboard = Canvas(self.canvas,
                    height = 750,
                    width = 550,
                    bg = self.colors['darkest'],
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0)
        self.scoreboard.grid(row=0, column=0, sticky='w', padx=20)
        self.scoreboard.grid_propagate(0)
        self.user_scores = {}

        # Console user input
        self.console = Text(self.canvas,
                    width = 94,
                    height = 17,
                    highlightbackground="#36393f",
                    relief="flat",
                    bg = "#111111",
                    fg="white",
                    highlightthickness = 0,
                    font=("Free Mono", 10,"bold"))
        self.console.grid(row=1, column=1, sticky='s', pady=0)

        # canvas that displays map and nodes
        self.map_canvas = Canvas(self.canvas,
                    width=750,
                    height=750,
                    bg="red")
        self.map_canvas.grid(row=0, column=1, sticky='n', pady=20)

        # Map image
        image = Image.open("FrontendCore/uc_map.png")
        image = image.resize((750,750), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(image)
        self.map_canvas.create_image(0,0,image=pic, anchor="nw")

        # Nodes on map
        with open("FrontendCore/nodes.json") as json_file:
            self.node_data = json.load(json_file)
        print(self.node_data)
        for name, data in self.node_data.items():
            r = 7
            x0 = data['location'][0] - r
            y0 = data['location'][1] - r
            x1 = data['location'][0] + r
            y1 = data['location'][1] + r
            o = self.map_canvas.create_oval(x0, y0, x1, y1, fill="#e13038")
            #self.map_canvas.tag_raise(o, self.image_item)

        # Event stream
        ## Canvas
        self.event_stream_container = Canvas(self.canvas,
                    height = 750,
                    width = 550,
                    bg = self.colors['darkest'],
                    relief="flat",
                    borderwidth=0,
                    scrollregion=(0, 0, 400, 9000),
                    highlightthickness=0)
        self.event_stream_container.grid(row=0, column=2, sticky='w',padx=20)
        self.event_stream_container.grid_propagate(0)
        
        ## Scrolling
        self.event_stream_container.bind_all('<4>', lambda event: self.event_stream_container.yview_scroll(-1, "units"))
        self.event_stream_container.bind_all('<5>', lambda event: self.event_stream_container.yview_scroll(1, "units"))
        
        ## Frame where all the events go
        self.event_stream_frame = Frame(self.event_stream_container,
                    bg=self.colors['darkest'],
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0)
        self.event_stream_container.create_window((0,0), window=self.event_stream_frame, anchor="nw")
        
        # Net thread
        self.net_client = net_client
        self.run_thread = True
        self.event_stream_thread = threading.Thread(target=self.update_gui, args=[])
        self.event_stream_thread.start()

        mainloop()
        self.run_thread = False
    
    def write_to(self,tk_object, text):
        tk_object.config(state=NORMAL)
        tk_object.insert(END, text + "\n")
        tk_object.see("end")
        tk_object.config(state=DISABLED)

    def display_event(self, time_stamp, event):
        event_type = list(event.keys())[0]
        details = ", ".join(["{}: {}".format(k,v) for k,v in event[event_type].items()])
        event_text = "{}: {}\n{}\n{}".format(str(datetime.datetime.fromtimestamp(float(time_stamp)))[-15:-7], event_type, details, " "*75)
        new_event = Message(self.event_stream_frame,
                    fg="#94d6fe",
                    bg=self.colors['main_text'],
                    font=("Free Mono", 10, "bold"),
                    width=510,
                    relief=SUNKEN,
                    text=event_text)
        last_row = self.event_stream_frame.grid_size()[1]
        new_event.grid(row=last_row, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='n')
        self.event_stream_container.config(scrollregion= self.event_stream_container.bbox("all"))
        self.event_stream_container.yview_moveto(1)

    def update_score_db(self, time_stamp, event):
        event_type = list(event.keys())[0]
        # If it is not a score related event, return
        if event_type != "addScore" and event_type != "setScore":
            return
        # if malformed, return
        if "user" not in event[event_type] or "value" not in event[event_type]:
            print("malformed score event. should have user and value keys")
            return
        # assign score
        user = event[event_type]['user']
        value = event[event_type]['value']
        if event_type == "setScore" or user not in self.user_scores:
            self.user_scores[user] = value
            print(self.user_scores)
        elif event_type == 'addScore':
            self.user_scores[user] += value

    def display_scores(self):
        self.scoreboard.delete('all')
        num_players = len(self.user_scores.keys())
        for i, kv in enumerate(self.user_scores.items()):
            user, value = kv
            event_text = "{}:\n{}\n{}".format(user, value, " "*10)
            new_event = Message(self.scoreboard,
                        fg="#579753",
                        bg=self.colors['main_text'],
                        font=("Free Mono", 13, "bold"),
                        width=510,
                        relief=SUNKEN,
                        text=event_text)
            
            new_event.grid(row=i//4, column=i%4, padx=5, pady=5, ipadx=5, ipady=5, sticky='n')


        
            
        


    def update_gui(self):
        time_last_event = 0
        while self.run_thread:
            # get updated events from server
            new_events, time_last_event = self.net_client.getEventsSince(time_last_event)
            # for each event, update display as needed
            for time_stamp, event in new_events.items():
                # update event stream
                self.display_event(time_stamp, event)
                # update scoreboard
                self.update_score_db(time_stamp, event)
                # TODO: update map
            self.display_scores()
            time.sleep(5)
    


