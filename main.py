#!/usr/bin/python
# coding:utf-8
#
# A tool for ip test and scan

import sys
from threading import Thread
import re
import os
import time
import socket
from netaddr import *
import fcntl
import struct
import array
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
        global clist
        # 載入 glade 檔
        self.gladefile = "main.glade"
        self.UI = gtk.glade.XML(self.gladefile)
        # 載入視窗
        self.window = self.UI.get_widget("window1")
        # 載入元件
        self.btn1 = self.UI.get_widget("button1")
        self.entry1 = self.UI.get_widget("combo1")
        self.entry2 = self.UI.get_widget("entry2")
        self.entry3 = self.UI.get_widget("entry3")
        self.clist = self.UI.get_widget("clist1")
        clist = self.clist

        interface_ip_list = [""] + (get_all_network_interfaces_ip())
        self.entry1.set_popdown_strings(interface_ip_list)

        self.clist.column_titles_show()
        self.clist.set_column_title(0, 'IP')
        self.clist.set_column_title(1, 'Status')
        self.clist.set_column_title(2, 'Hostname')
        self.clist.set_column_width(0, len(' 888.888.888.888 ')*8)
        self.clist.set_column_width(1, len('Status')*8)
        self.clist.set_column_width(2, len('Hostname')*8)
        self.clist.set_column_justification(0, 'center')
        self.clist.set_column_justification(1, 'center')
        self.clist.set_column_justification(2, 'center')

        # 顯示視窗畫面
        self.window.show_all()

        # 設定事件
        dic = { "on_btn1_button_press_event" : self.on_btn1_button_press_event,
                "on_window1_destory" : gtk.main_quit,
        }
        # 連結事件
        self.UI.signal_autoconnect(dic)
        #self.window.connect('destroy', gtk.main_quit)
        #self.btn1.connect('clicked', self.on_btn1_button_press_event, None)

    def on_btn1_button_press_event(self, widget):
        print time.ctime()
        self.clist.clear()
        ip_list = gen_ip_list(self.entry1.entry.get_text(), self.entry2.get_text())
        # test icmp_scan and lookup_hostname function
        icmp_scan(ip_list)
        lookup_hostname(ip_list)
        print time.ctime()


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

# generate ip list from input entry
# Not complete !!
def gen_ip_list(ip_start, ip_end):
    global clist
    ip_list = []
    if '' == ip_start:
        Dialog("Start IP cannot be empty.")
    elif ('' != ip_start) and ('' == ip_end) and (True == is_valid_ip(ip_start)):
        ip_list.append(ip_start)
        clist.append([ip_start, '', ''])
    elif ('' != ip_start) and ('' != ip_end) and (True == is_valid_ip(ip_start)) and (True == is_valid_ip(ip_end)):
        try:
            iprange = IPRange(ip_start, ip_end)
            for ip in iprange:
                # strip subnet ip and broadcast ip
                if None == re.match(".*\.(255|0)$", str(ip)):
                    print str(ip)
                    ip_list.append(str(ip))
                    clist.append([str(ip), '', ''])
        except AddrFormatError:
            Dialog("lower bound IP greater than upper bound!")

#        ip_list.append(ip_start)
#        ip_list.append(ip_end)
#        clist.append([ip_start, '', ''])
#        clist.append([ip_end, '', ''])
    return ip_list

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
    except socket.error:
        print 'illegal ip'
        return False
    return True

def get_all_network_interfaces_ip():
    platform = sys.platform
    if "win" in platform:
        pass
    elif "linux" in platform:
        def get_ip_address(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])

        max_possible = 128  # arbitrary. raise if needed.
        bytes = max_possible * 32
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        names = array.array('B', '\0' * bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        namestr = names.tostring()
        #return [namestr[i:i+32].split('\0', 1)[0] for i in range(0, outbytes, 32)]

        iface_list = [namestr[i:i+32].split('\0', 1)[0] for i in range(0, outbytes, 32)]
	iface_ip_list = []
        for iface in iface_list:
            iface_ip_list.append(get_ip_address(iface))
	return iface_ip_list
    else:
        return ['', '192.168.0.1']

def icmp_scan(ip_list):
    global clist
    pinglist = []
    for ip in ip_list:
        current = ping(ip)
        pinglist.append(current)
        current.start()

    ping.lifeline = re.compile(r"(\d) received")
    report = ("No response","Partial Response","Alive")

    for pingle in pinglist:
        pingle.join()
        #print "Status from ",pingle.ip,"is",report[pingle.status]
        if 'Alive' == report[pingle.status]:
            clist.set_text(ip_list.index(pingle.ip), 1, '●')

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

def lookup_hostname(ip_list):
    print "In lookup_hostname function.."
    pass

class nmblookup(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
    def run(self):
        pingaling = os.popen("nmblookup -A "+self.ip,"r")
        while 1:
            line = pingaling.readline()
            if not line: break
            print line
            #igot = re.findall(ping.lifeline,line)
            #if igot:
            #    self.status = int(igot[0])

def main():
    gtk.main()

if __name__ == "__main__":
    tvexample = Main_Window()
    main()
