#!/usr/bin/python
'''
Author: bernhard.denner@gmail.com
Date: 16. Feb 2014
'''
import sys, os
import easyBankcsv2qif
from gi.repository import Gtk


DEFAULT_ENC_FROM = 'iso-8859-1'
DEFAULT_ENC_TO   = 'utf-8'

class Frontend(object):

    def __init__(self):
        object.__init__(self)

    def saveDialog(self, filename):
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_do_overwrite_confirmation(True)
        #dialog.set_filename(filename)
        dialog.set_current_name(filename)
        dialog.props.title = "save file in QIF format, choose a name..."

        response = dialog.run()
        newFilename = None
        if response == Gtk.ResponseType.OK:
            newFilename = dialog.get_filename()
#            print dialog.get_uri()
        #elif response == Gtk.ResponseType.CANCEL:

        dialog.destroy()
        return newFilename


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

    newFilename = f.saveDialog(newFilename)
    #print newFilename
    
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
    converter = easyBankcsv2qif.EasyCSV2QIFconverter(instream, outstream, '')
    converter.setEncoding(DEFAULT_ENC_FROM, DEFAULT_ENC_TO)
    converter.convert()

    instream.close()
    outstream.close()

    # show summary dialog
    f.processedDialog(converter.getSummary())

    # remove the csv file
    os.unlink(csvFilename)
