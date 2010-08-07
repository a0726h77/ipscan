#!/usr/bin/python
# coding:utf-8
#
# A tool for ip test and scan

import sys
from threading import Thread
import re
import os
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class Main_Window:
    def __init__(self):
        # 載入 glade 檔
        self.gladefile = "main.glade"
        self.UI = gtk.glade.XML(self.gladefile)
        # 載入視窗
        self.window = self.UI.get_widget("window1")
        # 載入元件
        self.btn1 = self.UI.get_widget("button1")
        self.entry1 = self.UI.get_widget("entry1")
        self.entry2 = self.UI.get_widget("entry2")
        self.entry3 = self.UI.get_widget("entry3")
        self.clist = self.UI.get_widget("clist1")
        # 顯示視窗畫面
        self.window.show_all()

        # 設定事件
	#dic = {"on_window1_destory" : gtk.main_quit,
	#	"on_btn1_button_press_event" : self.on_btn1_button_press_event,
	#	}
        # 連結事件
	#self.UI.signal_autoconnect(dic)

	self.window.connect('destroy', gtk.main_quit) 
        self.btn1.connect('clicked', self.on_btn1_button_press_event, None)

    def on_btn1_button_press_event(self, widget, event):
	if '' == self.entry1.get_text():
            Dialog("tttttttttttt..........")
	else:
            print self.entry1.get_text()
	    print self.entry2.get_text()
	    print self.entry3.get_text()

	    # test icmp_scan function
	    ip_list = []
	    ip_list.append(self.entry1.get_text())
	    self.icmp_scan(ip_list)

    def icmp_scan(self, ip_list):
        pinglist = []
        for ip in ip_list:
            current = ping(ip)
            pinglist.append(current)
            current.start()

        ping.lifeline = re.compile(r"(\d) received")
        report = ("No response","Partial Response","Alive")
    
        for pingle in pinglist:
            pingle.join()
            print "Status from ",pingle.ip,"is",report[pingle.status]
	
class Dialog:
    def __init__(self, message):
        self.gladefile = "main.glade"
        self.UI = gtk.glade.XML(self.gladefile)
        self.warning_dialog = self.UI.get_widget("window2")
        self.message_label = self.UI.get_widget("label4")
        self.btn2 = self.UI.get_widget("button2")

        self.warning_dialog.connect('destroy', self.widget_close, None) 
        self.btn2.connect('clicked', self.widget_close, None) 
	
	self.message_label.set_text(message)

        self.warning_dialog.show_all()

    def widget_close(self, widget, event):
        gtk.Window.destroy(self.warning_dialog)

class ping(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
    def run(self):
        pingaling = os.popen("ping -q -c2 "+self.ip,"r")
        while 1:
            line = pingaling.readline()
            if not line: break
            igot = re.findall(ping.lifeline,line)
            if igot:
                self.status = int(igot[0])

def main():
    gtk.main()

if __name__ == "__main__":
    tvexample = Main_Window()
    main()
