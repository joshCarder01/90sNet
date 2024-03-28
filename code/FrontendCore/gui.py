from tkinter import *

import threading
import time
from PIL import ImageTk, Image  
import datetime
from FrontendCore import netclient

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
        self.root.bind('<Return>', lambda event:self.update_user_input())
        self.root.bind("<Button-1>", lambda event:self.console.mark_set("insert", END))
        #self.root.bind("<Button-1>", lambda event:print("foo"))
        self.write_to_stream(self.console, "Admin> ")

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
    
    def write_to_stream(self, tk_object, text):
        tk_object.insert(END, text)
        tk_object.see("end")

    def display_event(self, time_stamp, event):
        event_type = event['type']
        details = ", ".join(["{}: {}".format(k,v) for k,v in event.items()])
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
        #event_type = event['type']
        if event["type"] == 'score':
            username, val = event['description'].split(',')
            val = int(val)
            self.user_scores[username] += val
        
        '''
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
        '''

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
            for event in new_events:
                time_stamp = event['time']
                # update event stream
                self.display_event(time_stamp, event)
                # update scoreboard
                self.update_score_db(time_stamp, event)
                # TODO: update map
            self.display_scores()
            time.sleep(5)

    def update_user_input(self):
        stream = self.console.get("1.0", "end-1c")
        prompt = "Admin> "
        last_cmd = stream.rfind(prompt)

        cmd_str = stream[last_cmd+len(prompt):-1]

        cmd_dict = netclient.cmd_to_dict(cmd_str)
        if cmd_dict['cmd'] == "docker":
            m_cmd_dict = cmd_dict
            m_cmd_dict['cmd'] = 'cli'
            request_id = json.loads(self.net_client.http_command(netclient.cmd_dict_to_str(m_cmd_dict)))
            while True:
                cmd_result = self.net_client.send_and_receive_http('command/results', request_id)
                if str(request_id['id']) in cmd_result:
                    cmd_result = json.loads(cmd_result)
                    if cmd_result['id'] == request_id['id']:
                        break

            self.write_to_stream(self.console, "{}\n{}".format(cmd_result['result'], prompt))
            '''
            request_id = json.loads(self.net_client.http_command(" ".join(['cli'] + cmd_str.split(" ")[1:])))
            self.write_to_stream(self.console, "{}\n{}".format(request_id, prompt))
            while True:
                cmd_result = json.loads(self.net_client.send_and_receive_http('command/result', request_id))
                print(cmd_result)
                print(request_id)
                if cmd_result['id'] == request_id['id']:
                    break

            self.write_to_stream(self.console, "{}\n{}".format(cmd_result, prompt))
            '''
            self.write_to_stream(self.console, "{}\n{}".format("", prompt))
        elif cmd_dict['cmd'] == "addUser":
            response = self.net_client.post_and_receive_http("users/add", {"name":cmd_dict['args'][0], "username":cmd_dict['args'][1]})
            self.write_to_stream(self.console, "{}\n{}".format(response, prompt))
            self.user_scores[cmd_dict['args'][1]] = 0

        # uncomment this block once chad gets his db stuff working and returning single cmd info
        '''
        while True:
            cmd_result = self.net_client.send_and_receive_http('command', request_id)
            if cmd_result['id'] == request_id['id']:
                break

        self.write_to_stream(self.console, "{}\n{}".format(cmd_result, prompt))
        '''

    


