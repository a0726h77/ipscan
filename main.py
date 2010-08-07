#!/usr/bin/python
# coding:utf-8
#
# A tool for ip test and scan


import sys
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

class View:
    def __init__(self):
        # 載入 glade 檔
        self.gladefile = "main.glade"
        self.UI = gtk.glade.XML(self.gladefile)
        # 載入視窗
        self.window = self.UI.get_widget("window1")
        # 載入元件
        self.btn1 = self.UI.get_widget("button1")
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
        print "hello"

def main():
    gtk.main()

if __name__ == "__main__":
    tvexample = View()
    main()
