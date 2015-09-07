#!/usr/bin/python
'''
Author: bernhard.denner@gmail.com
Date: 16. Feb 2014
'''
import sys, os
import os.path
import json
import easyBankcsv2qif
from gi.repository import Gtk


DEFAULT_ENC_FROM = 'iso-8859-1'
DEFAULT_ENC_TO   = 'utf-8'

DEFAULT_CONFIG_FILE = os.path.expanduser(
    '~/.config/easyBankcsv2qifFrontend.conf')

CONF_DIR_ACCOUNTS = 'accountnames'


class Frontend(object):

    def __init__(self):
        object.__init__(self)
        self._config = None
        self.readConfigFile()
        
        self.account = None
        self.newFilename = None
        

    def saveDialog(self, filename):
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(filename)
        dialog.props.title = "save file in QIF format, choose a name..."

        # add a ComboBoxText to specify the Name of the Account 
        # to be specified in the QIF file        
        box = dialog.get_content_area()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box.add(hbox)
        
        label = Gtk.Label("Select Account name:")
        combo = Gtk.ComboBoxText.new_with_entry()
        hbox.pack_start(label, True, True, 10)
        hbox.pack_start(combo, True, True, 10)
        
        # add known account names to the combobox
        for i in self._config[CONF_DIR_ACCOUNTS]:
            combo.append_text(i)
            
        # select the first one
        if self._config[CONF_DIR_ACCOUNTS]:
            combo.set_active(0)
                
        dialog.show_all()

        # show the dialog and wait for user response
        response = dialog.run()
        self.newFilename = None
        
        if response == Gtk.ResponseType.OK:
            self.newFilename = dialog.get_filename()

        self.account = combo.get_active_text()
        
        # write new account to the config file
        if len(self.account) > 0 \
           and self.account not in self._config[CONF_DIR_ACCOUNTS]:
            self._config[CONF_DIR_ACCOUNTS].append(self.account)
            self.writeConfigFile()
        
        dialog.destroy()
        return self.newFilename


    def processedDialog(self, message):
        dialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK)
        dialog.props.title = "EasyBank CSV to QIF finished"
        dialog.props.text = "CSV 2 QIF converstion finished"
        dialog.format_secondary_text(message)

        dialog.run()
        dialog.destroy()
        

    def errorMessage(self, headline, message):
        dialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK)
        dialog.props.title = "Error"
        dialog.props.text = headline
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
        
        
    def readConfigFile(self):
        conf = None
        try:
            confFile = open(DEFAULT_CONFIG_FILE, 'r')
            conf = json.load(confFile)
            confFile.close()
        except IOError as detail:
            print detail
        
        # check/initialize configuration
        if type(conf) != dict:
            conf = {}
            
        if CONF_DIR_ACCOUNTS not in conf:
            conf[CONF_DIR_ACCOUNTS] = []

        self._config = conf
        return conf


    def writeConfigFile(self, conf = None):
        if conf == None:
            conf = self._config
            
        try:
            confFile = open(DEFAULT_CONFIG_FILE, 'w')
            json.dump(conf, confFile)
            confFile.close()
        except IOError as detail:
            print detail
            
            
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " <filename>"
        sys.exit(1)
    
    f = Frontend()

    csvFilename = sys.argv[1]
    instream = None
    try:
        instream = open(csvFilename, 'r')
    except IOError as detail:
        f.errorMessage("could not open input file '" + csvFilename + "'",
            str(detail))    
        sys.exit(1)

    newFilename = os.path.basename(csvFilename)
    newFilename += ".qif"

    f.saveDialog(newFilename)
    newFilename = f.newFilename
    account = f.account or ''
    
    if newFilename == None:
        instream.close()
        sys.exit(0)

    outstream = None
    try:
        outstream = open(newFilename, 'w')
    except IOError as detail:
        f.errorMessage("could not open output file", str(detail))
        instream.close()
        sys.exit(1)

    # do processing here
    converter = easyBankcsv2qif.EasyCSV2QIFconverter(instream, outstream, account)
    converter.setEncoding(DEFAULT_ENC_FROM, DEFAULT_ENC_TO)
    converter.convert()

    instream.close()
    outstream.close()

    # show summary dialog
    f.processedDialog(converter.getSummary())

    # remove the csv file
    # os.unlink(csvFilename) better keep them
