from FrontendCore import testGUI
from FrontendCore import testNetClient


net_client = testNetClient.NetClient('127.0.0.1', 9000)
frontend_gui = testGUI.FrontendGUI(net_client)