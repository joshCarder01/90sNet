from FrontendCore import gui
from FrontendCore import netclient


net_client = netclient.NetClient('127.0.0.1', 5000)
frontend_gui = gui.FrontendGUI(net_client)