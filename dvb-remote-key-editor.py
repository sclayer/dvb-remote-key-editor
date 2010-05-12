#!/usr/bin/env python
#Copyright (C) by Hagen Fritsch, 2007
#Released under the terms of the GPLv3 or later
#TODO i18n, menu accels, menu icons
#     a console only version

import struct, re, os
import pygtk
pygtk.require('2.0')
import gtk
class KeyEditor:
    "Generic KeyEditor Class Interface"
    def __init__(self, file=None, ver=None):
        if file is None:
            if ver is None: ver = os.popen("uname -r").read().strip()
            file = self.filename % ver
        self.filename = file
        self.file = open(file)
        #self.read_file()
        #self.file = open(file)
        self.find_offset()
        self.read_table()
        self.file.close()

    def read_file(self):
        try:
            self.log=open("/media/Donnee/telcommande/log.txt","w")
            self.essai=struct.unpack('@I', self.file.read(4))[0]
            while self.essai != 123456: 
                #print self.essai
                self.log.write(str(self.essai) + "\n")
                self.essai=struct.unpack('@I', self.file.read(4))[0]
            self.log.close()
        except:
            raise Exception("file could not be read")

    def find_offset(self):
        try:
            while struct.unpack('@I', self.file.read(4))[0] != self.pattern: pass
            self.start = self.file.tell()+self.offset
        except:
            raise Exception("offset could not be found")

    def read_table(self):
        self.file.seek(self.start, 0)
        self.table = {}
        self.data = []
        for i in range(len(self.std_keys)):
            x = struct.unpack(self.struct, self.file.read(self.len))
            #print x
            self.data.append(x)
            self.table[x[self.key]] = x[self.keycode]

    def save(self, file=None):
        if file is None: file = self.filename
        #file = "/tmp/%s" % os.path.basename(self.filename)
        file = open(file, "r+")
        file.seek(self.start, 0)
        for x in self.data:
            x = list(x)
            x[self.keycode] = self.table[x[self.key]]
            file.write(struct.pack(self.struct, *x))
        file.close()

###############################################
### Descriptions for common DVB-USB drivers ###
###############################################

class EditorNovaT(KeyEditor):
    std_keys = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'KPASTERISK', 11: 'RED', 12: 'RADIO', 13: 'MENU', 14: 'GRAVE', 15: 'MUTE', 16: 'VOLUMEUP', 17: 'VOLUMEDOWN', 18: 'CHANNEL', 20: 'UP', 21: 'DOWN', 22: 'LEFT', 23: 'RIGHT', 24: 'VIDEO', 25: 'AUDIO', 26: 'MEDIA', 27: 'EPG', 28: 'TV', 30: 'NEXT', 31: 'BACK', 32: 'CHANNELUP', 33: 'CHANNELDOWN', 36: 'LAST', 37: 'OK', 41: 'BLUE', 46: 'GREEN', 48: 'PAUSE', 50: 'REWIND', 52: 'FASTFORWARD', 53: 'PLAY', 54: 'STOP', 55: 'RECORD', 56: 'YELLOW', 59: 'GOTO', 61: 'POWER'}
    pattern = 0x1e
    offset  = -4
    name = "Hauppauge Win-TV Nova-T USB2"
    struct = '@BBI'
    len = 8
    filename = "/lib/modules/%s/kernel/drivers/media/dvb/dvb-usb/dvb-usb-nova-t-usb2.ko" 
    key, keycode = 1, 2
    
class EditorA800(KeyEditor):#ok
    std_keys = {543: 'VOLUMEUP', 771: 'CHANNELUP', 539: 'STOP', 537: 'RECORD', 521: '4', 536: 'PLAY', 522: '5', 770: 'CHANNELDOWN', 517: '1', 523: '6', 524: 'ZOOM', 541: 'BACK', 535: 'PROG2', 542: 'VOLUMEDOWN', 527: '9', 528: 'PROG3', 531: 'RIGHT', 513: 'PROG1', 512: 'POWER', 530: 'LEFT', 525: '7', 515: 'TEXT', 768: 'LAST', 538: 'PLAYPAUSE', 532: 'MUTE', 769: 'FIRST', 533: 'MENU', 516: 'EPG', 529: '0', 518: '2', 520: 'AUDIO', 519: '3', 540: 'FORWARD', 526: '8'}
    pattern = 0xa801
    offset  = +64
    name = "AVerMedia AverTV DVB-T A800"
    struct = '@HI'
    len = 8
    filename = "/lib/modules/%s/kernel/drivers/media/dvb/dvb-usb/dvb-usb-a800.ko" 
    key, keycode = 0,1

class EditorDIBUSB(KeyEditor):
    std_keys = {5632: 'POWER', 4096: 'MUTE', 6534: 'FORWARD', 2304: '4', 4742: 'POWER', 1414: '5', 256: '2', 1536: '3', 19456: 'PAUSE', 512: 'CHANNELDOWN', 7302: 'UNKNOWN', 3206: 'UNKNOWN', 0: 'TAB', 7680: 'VOLUMEUP', 768: '1', 7168: 'EPG', 2438: '9', 5510: 'ESC', 5120: 'PLAY', 3328: '7', 5766: 'PLAY', 7814: 'DOWN', 16384: 'REWIND', 2560: 'VOLUMEDOWN', 4998: 'UNKNOWN', 6656: 'STOP', 3974: 'SELECT', 19712: 'SCREEN', 4230: 'MUTE', 5888: 'FAVORITES', 134: 'UNDO', 1024: 'LIST', 3462: 'STOP', 18432: 'INFO', 2694: '0', 4352: 'RECORD', 6790: 'UP', 646: '2', 3584: 'PREVIOUS', 21504: 'AUDIO', 902: '3', 1158: '4', 390: '1', 6912: '9', 5254: 'UNKNOWN', 7558: 'RECORD', 4486: 'BACK', 3072: 'CANCEL', 7424: '5', 1280: 'CHANNELUP', 3718: 'PAUSE', 5376: '0', 1670: '6', 8070: 'LEFT', 2950: 'EPG', 4608: 'FASTFORWARD', 7046: 'RIGHT', 1926: '7', 7936: '6', 6400: '8', 3840: 'TEXT', 6278: 'ZOOM', 2182: '8'}
    pattern = 0x1600
    offset  = -4
    name = "Generic dib-usb Driver"
    struct = '@HI'
    len = 8
    filename = "/lib/modules/%s/kernel/drivers/media/dvb/dvb-usb/dvb-usb-dibusb-common.ko"
    key, keycode = 0,1

class EditorDTT200U(KeyEditor):
    std_keys = {384: 'MUTE', 640: 'CHANNELDOWN', 896: 'VOLUMEDOWN', 1664: '3', 3712: 'SELECT', 4736: 'POWER', 6784: 'CHANNELUP', 1152: '1', 1920: '4', 7040: '8', 1408: '2', 7808: 'VOLUMEUP', 2176: '5', 3200: 'ZOOM', 2688: '7', 8064: '9', 2432: '6', 3456: '0'}
    pattern = 0x180
    offset  = -4
    name = "WideView/Yakumo/Hama/Typhoon/Yuan DVB-T USB2"
    struct = '@HI'
    len = 8
    filename = "/lib/modules/%s/kernel/drivers/media/dvb/dvb-usb/dvb-usb-dtt200u.ko"
    key, keycode = 0,1

class EditorVP7045(KeyEditor):
    std_keys = {5632: 'POWER', 4096: 'MUTE', 16384: 'REWIND', 6400: '8', 256: '2', 19456: 'PAUSE', 512: 'CHANNELDOWN', 0: 'TAB', 768: '1', 7168: 'EPG', 1024: 'LIST', 1280: 'CHANNELUP', 7680: 'VOLUMEUP', 2560: 'VOLUMEDOWN', 1536: '3', 19712: 'SCREEN', 5888: 'FAVORITES', 5120: 'PLAY', 18432: 'INFO', 4352: 'RECORD', 2304: '4', 21504: 'AUDIO', 6656: 'STOP', 6912: '9', 3072: 'CANCEL', 7424: '5', 5376: '0', 3328: '7', 4608: 'FASTFORWARD', 3584: 'PREVIOUS', 7936: '6', 3840: 'TEXT'}
    pattern = 0x1600
    offset  = -4
    name = "TwinhanDTV Alpha/MagicBoxII USB2"
    struct = '@HI'
    len = 8
    filename = "/lib/modules/%s/kernel/drivers/media/dvb/dvb-usb/dvb-usb-vp7045.ko"
    key, keycode = 0,1

class EditorCinergyT2(KeyEditor):#ok
    std_keys = std_keys = {1041: 'LEFT', 1042: 'OK', 1053: 'MUTE', 1055: 'CHANNELDOWN', 1096:'STOP', 1026: '1', 1028: '3', 1034: '9', 1030: '5', 1032: '7', 1036: '0', 1051: 'CHANNELUP', 1038: 'SELECT', 1037: 'REFRESH', 1040: 'UP', 1112: 'RECORD', 1044: 'DOWN', 1046: 'INFO', 1048: 'GREEN', 1050: 'BLUE', 1052: 'VOLUMEUP', 1108: 'PREVIOUS', 1054: 'VOLUMEDOWN', 1116: 'NEXT', 1025: 'POWER', 1027: '2', 1088: 'PAUSE', 1029: '4', 1031: '6', 1033: '8', 1043: 'RIGHT', 1100: 'PLAY', 1039: 'EPG', 1049: 'YELLOW', 1035: 'VIDEO', 1045: 'TEXT', 1047: 'RED'}
    pattern = 0xccd0003 #260
    offset = +60
    name = "Cinergy T2"
    struct = '@HI'
    len = 8
    filename = "/lib/modules/%s/kernel/drivers/media/dvb/dvb-usb/dvb-usb-cinergyT2.ko"
    key, keycode = 0, 1

#####################
### GUI INTERFACE ###
#####################
class KeyEditorGui:
    ui='''<ui>
        <menubar name="BarreMenu">
            <menu action="KeymapMenuAction">
                <menuitem action="LoadAction"/>
                <menuitem action="SaveAction"/>
                <separator/>
                <menuitem action="QuitAction"/>
            </menu>
            <menu action="LoadMenuAction">
            </menu>
            <menu action="HelpMenuAction">
                <menuitem action="InfoAction"/>
            </menu>

        </menubar>

    </ui>'''

    def __init__(self, ke):
        self.name = "DVB Remote Editor"
        self.version = "0.2.7-beta2"
        self.ke = None #ke[0]()
        self.editors = ke
        self.read_linux_keys()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.set_title()
        self.window.set_default_size(350,600)
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(1)
	
        self.box1 = gtk.VBox(False, 1)
        self.table = gtk.Table(len(ke), 1)
        
        #use of UIManager
        self.gestionui=gtk.UIManager()
        
        
        self.grouperacc = self.gestionui.get_accel_group()
        self.window.add_accel_group(self.grouperacc)
        
        #action group
        groupeactions = gtk.ActionGroup('ExempleUIGestion')
        self.groupeactions = groupeactions
        
        groupeactions.add_actions([('KeymapMenuAction',None,'Keymap',None,None,None),                
                ('LoadAction',None,'Load from file',None,None,self.load),
                ('SaveAction',None,'Save to file',None,None,self.save),
                ('QuitAction',None,'Quit',None,None,self.quit),
                ('LoadMenuAction',None,'Load',None,None,None),
                ('HelpMenuAction',None,'Help',None,None,None),
                ('InfoAction',None,'Info',None,None,self.info)])
        
        #instert the actions in the UI manager
        self.gestionui.insert_action_group(groupeactions, 0)
        
        #add interface description (xml)
        self.gestionui.add_ui_from_string(self.ui)
        
        #add ui for the modules
        ui1='''<menubar name="BarreMenu">
                <menu action="LoadMenuAction"> 
                '''
        for x in range(len(ke)):
            ui1=ui1+'''<menuitem action="%s'''% ke[x].name+'''" position="bottom"/>
                        '''
            groupeactions.add_actions([(ke[x].name,None,ke[x].name,None,None,self.load_kernel)],x)
        ui1=ui1+'''</menu>
                    </menubar>'''
        self.gestionui.add_ui_from_string(ui1)

        for x in range(len(ke)):
            but = gtk.Button(ke[x].name)
            but.connect("clicked", self.load_kernel, x)
            but.show()
            self.table.attach(but, 0, 1, x, x+1, yoptions=0)

        
        #Menu Bar (use UI widget)
        self.barremenus = self.gestionui.get_widget('/BarreMenu')
        self.box1.pack_start(self.barremenus, False)
        
        self.scroll = gtk.ScrolledWindow()
        
        self.scroll.add_with_viewport(self.table)
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.box1.add(self.scroll)
        self.window.add(self.box1)
        
        self.button1 = gtk.Button("Save changes to kernel module")
        self.button1.connect("clicked", self.save_button)
        self.box1.pack_start(self.button1, False, False, 0)
        self.button1.show()
        self.boxes = {}
        self.table.show()
        self.scroll.show()
        self.box1.show()
        self.window.show()
        
    def set_title(self, msg=None):
        title = self.name
        if msg is None and self.ke is not None: msg = self.ke.name
        if msg is not None: title = "%s: %s" % (title, msg)
        self.window.set_title(title)
    
    def load(self, w, data=None):
        if self.ke is None: return
        fc = gtk.FileChooserDialog(title="Select a file to open", buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK) )
        fc.set_default_response(gtk.RESPONSE_OK)
        res = fc.run()
        file = fc.get_filename()
        fc.destroy()
        if res != gtk.RESPONSE_OK: return
        file = open(file)
        d = {}
        self.i=0
        for line in file:
            try:
                key, value = line[:-1].split("\t")
                d[key] = value
            except:
                if not line[0] == '#': print "mismatch for \"%s\"" % line[:-1]
        for key,box in self.boxes.iteritems():
            if key in self.ke.std_keys:
                k = self.ke.std_keys[key]
                index=self.get_index(d[k])
                if k in d: box.set_active(index)
        
    def save(self, w, data=None):
        if self.ke is None: return
        fc = gtk.FileChooserDialog(title="Select a file to save", action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        fc.set_do_overwrite_confirmation(True)
        fc.set_default_response(gtk.RESPONSE_OK)
        res = fc.run()
        file = fc.get_filename()
        fc.destroy()
        if res != gtk.RESPONSE_OK: return
        file = open(file, "w")
        file.write("#Keymap for \"%s\"\n#Generated by %s (v%s)\n" % (self.ke.name, self.name, self.version))
        for key,box in self.boxes.iteritems():
            file.write("%s\t%s\n" % (self.ke.std_keys[key], box.get_active_text()))
            
        file.close()
        
    def load_kernel(self, w, data=None):
        if isinstance(w, int): data, w = w, data
        for i in self.table: self.table.remove(i)
        self.ke = self.editors[data]()
        self.set_title("Loading...")
        self.table.resize(len(self.ke.std_keys), 2)
        self.boxes = {}
        c = 0
        #for name,key in self.ke.std_keys.iteritems(): 
        for x in self.ke.data:
            key = x[self.ke.key]
            name = self.ke.std_keys[key]
            lab = gtk.Label(name)
            lab.show()
            combo=gtk.combo_box_entry_new_text()
            for i in range(len(self.linux_keys.values())):
                combo.append_text(self.linux_keys.values()[i])
            test=False
            j=-1
            while test==False & j<len(self.linux_keys.values()):
                j+=1
                if self.linux_keys.values()[j]==self.linux_keys[self.ke.table[key]]:test=True
            
            combo.set_active(j)

            combo.show()
            self.table.attach(lab, 0, 1, c, c+1)
            self.table.attach(combo, 1, 2, c, c+1)
            self.boxes[key] = combo
            c += 1 
        self.table.show()
        self.set_title()
      # print self.boxes

    def get_index (self,data):
        index=-1
        j=-1
        l=len(self.linux_keys.values())
        test=False
        while test==False & j<l:
            j+=1
            if self.linux_keys.values()[j]==data:test=True
        index=j
        return index
        
    def delete_event(self, widget,event, data=None):
        gtk.main_quit()
        return False

    def quit (self, widget,data=None):
        gtk.main_quit()

    def info(self, widget, data=None):
        dlg = gtk.MessageDialog(self.window, buttons=gtk.BUTTONS_CLOSE)
        dlg.set_markup("""<b>%s v%s</b> by Hagen Fritsch  
		<span foreground='purple'>Updated by Sylvain Clayer</span>

Designed to make changing keycodes for DVB-T Remotes easier.
Works by patching the appropriate kernel-modules.

Needs to be run as root for patching kernel-modules.""" % (self.name, self.version))
        dlg.set_title("About %s" % self.name)
        if dlg.run() == gtk.RESPONSE_CLOSE: dlg.destroy()

    def save_button(self, widget):
        if self.ke is None: return
        lkeys = {}
        for key,val in self.linux_keys.iteritems(): lkeys[val] = key
        for key,box in self.boxes.iteritems():
            self.ke.table[key] = lkeys[box.get_active_text()]
        try:
            self.ke.save()
            mod = os.path.basename(self.ke.filename)[:-3].replace("-", "_")
            dlg = gtk.MessageDialog(self.window, buttons=gtk.BUTTONS_CLOSE, message_format="To enable the new keycodes, you have to reload the kernel-module:\n\nsudo rmmod %s\nsudo modprobe %s" % (mod, mod))
            dlg.set_title("Saved")
            if dlg.run() == gtk.RESPONSE_CLOSE: dlg.destroy()
        except Exception, e:
            dlg = gtk.MessageDialog(self.window, buttons=gtk.BUTTONS_CLOSE, message_format=str(e))
            dlg.set_title("Saving failed")
            if dlg.run() == gtk.RESPONSE_CLOSE: dlg.destroy()

    def read_linux_keys(self):
        "Reads key codes and names from input.h"
        self.linux_keys = {}
        self.linux_key_table = {}
        linux = open("input.h")
        keyline = re.compile('^#define KEY_([^\s]+?)\s+(.+)$')
        d = 0
        for line in linux:
            match = keyline.match(line)
            if match:
                i = match.group(2)
                try:
                    if len(i) > 2 and i[1] == 'x': i = int(i, 16)
                    else: i = int(i)
                    self.linux_keys[i] = match.group(1) #touche clavier
                    self.linux_key_table[d] = i #clees
                    d+=1
                except:
                    print match.group(0), "failed"
if __name__=='__main__':
    ke=[EditorNovaT, EditorCinergyT2, EditorA800, EditorDIBUSB, EditorDTT200U, EditorVP7045]
    KeyEditorGui(ke)
    gtk.main()
