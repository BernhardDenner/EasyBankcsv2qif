import unittest
from easyBankcsv2qif import Transaction

# some globals
defaultAccount = "OPSKATWW AT120000120340560780"


class TestTransaction(unittest.TestCase):
    
    def setUp(self):
        pass
        
    
    def gTdesc(self, desc):
        """ get_Transaction_set_Description
            is a shortcut function to init a Transaction
            with default values and a custom description since we mostly test
            parsing the description
        """
        v = ["AT1234",       # account
             desc,           # description
             "01.08.2013",   # date
             "02.08.2013",   # valutadate
             "+1200,00",     # amount
             "EUR"]          # currency
             
        t = Transaction()
        t.setTransaction(v[0],  # account
                         v[1],  # description
                         v[2],  # date
                         v[3],  # valutadate
                         v[4],  # amount
                         v[5])  # currency
        return t
        
        
    def testBasics(self):
        """ test the basic value setting
        """
        t = Transaction()
        t = self.gTdesc("some description")
        self.assertEqual(t.account, "AT1234")
        self.assertEqual(t.description, "some description")
        self.assertEqual(t.date, "01.08.2013")
        self.assertEqual(t.valutadate, "02.08.2013")
        self.assertEqual(t.amount, "+1200,00")
        self.assertEqual(t.currency, "EUR")
        
        
    def testUeberweisung1(self):
        t = self.gTdesc("Startkapital fuer Haushaltskonto von          BG/000000002 {} Denner Bernhard Bernhard".format(defaultAccount))
        self.assertEqual(t.type, "BG")
        self.assertEqual(t.htype, "transfer")
        self.assertEqual(t.memo, "Startkapital fuer Haushaltskonto von Bernhard")
        self.assertEqual(t.payee, "Denner Bernhard ({})".format(defaultAccount))
        
        
    def testUeberweisung2(self):
        t = self.gTdesc("Gutschrift Onlinebanking                     BG/000000036 {} Denner Bernhard Linux Magazin via Kreditkarte Linux New Media AG".format(defaultAccount))
        self.assertEqual(t.type, "BG")
        self.assertEqual(t.htype, "transfer")
        self.assertEqual(t.memo, "Gutschrift Onlinebanking Linux Magazin via Kreditkarte Linux New Media AG")
        self.assertEqual(t.payee, "Denner Bernhard ({})".format(defaultAccount))
        
        
    def testUeberweisung2(self):
        t = self.gTdesc("monatliches Budget                           BG/000000093 {} Denner Bernhard".format(defaultAccount))
        self.assertEqual(t.type, "BG")
        self.assertEqual(t.htype, "transfer")
        self.assertEqual(t.memo, "monatliches Budget")
        self.assertEqual(t.payee, "Denner Bernhard ({})".format(defaultAccount))
        
        
    def testAuszahlung1(self):
        t = self.gTdesc("Auszahlung Maestro             4 20:26K1     MC/000000151 25 00000100 MAESTRO ATM 14.07.14 20:26K1 SOCIETE GENERALE\\\\ARLE S\\132000         2500340   ")
        self.assertEqual(t.type, "MC")
        self.assertEqual(t.htype, "withdraw")
        self.assertEqual(t.memo, "Auszahlung Maestro (4 20:26K1) 25 00000100 MAESTRO ATM 14.07.14 20:26K1 SOCIETE GENERALE\\\\ARLE S\\132000         2500340")
        self.assertEqual(t.payee, None)
        

    def testAuszahlung1(self):
        t = self.gTdesc("Auszahlung Maestro             18.39         MC/000000007 AUTOMAT   S6EE0160 K1 29.08.UM 18.39    ")
        self.assertEqual(t.type, "MC")
        self.assertEqual(t.htype, "withdraw")
        self.assertEqual(t.memo, "Auszahlung Maestro (18.39) AUTOMAT S6EE0160 K1 29.08.UM 18.39")
        self.assertEqual(t.payee, None)
        

    def testZahlung1(self):
        t = self.gTdesc("Bezahlung Maestro              16.35         MC/000000005 LUTZ DANKT   8834  K1 22.08.UM 16.35 XXXLUTZ 8834\\\\LAA AN D ER TH\\21             040   ")
        self.assertEqual(t.type, "MC")
        self.assertEqual(t.htype, "payment")
        self.assertEqual(t.memo, "Bezahlung Maestro (16.35) LUTZ DANKT 8834 K1 22.08.UM 16.35 XXXLUTZ 8834\\\\LAA AN D ER TH\\21 040")
        self.assertEqual(t.payee, None)
        

    def testZahlung2(self):
        t = self.gTdesc("MERKUR DANKT 3750P K1 03.09.    UM 19.06     VD/000000009     ")
        self.assertEqual(t.type, "VD")
        self.assertEqual(t.htype, "payment")
        self.assertEqual(t.memo, "MERKUR DANKT 3750P K1 03.09. UM 19.06")
        self.assertEqual(t.payee, None)
        

    def testZahlung3(self):
        t = self.gTdesc("MERKUR DANKT 3750P K1 03.09.    UM 19.06     VD/000000009     ")
        self.assertEqual(t.type, "VD")
        self.assertEqual(t.htype, "payment")
        self.assertEqual(t.memo, "MERKUR DANKT 3750P K1 03.09. UM 19.06")
        self.assertEqual(t.payee, None)
        

    def testZahlung4(self):
        t = self.gTdesc("www.hochkar.com   /1228           AE120932   OG/000000049 35000 00000069682 HOBEX AG    ")
        self.assertEqual(t.type, "OG")
        self.assertEqual(t.htype, "payment")
        self.assertEqual(t.memo, "www.hochkar.com /1228 AE120932 35000 00000069682 HOBEX AG")
        self.assertEqual(t.payee, None)
        

    def testZahlung5(self):
        t = self.gTdesc("Vorschreibung 09/14-10/14 + Nachverr. 08/14-08/14 (Betrag enthaelt 10%U                                   St: EUR 4 ,85), 2153, Patzenthal 7                     OG/000000186 RZBAATWWXXX AT673100000404011011 GIS Gebuehren Info Service GmbH (FN ")
        self.assertEqual(t.type, "OG")
        self.assertEqual(t.htype, "payment")
        self.assertEqual(t.memo, "Vorschreibung 09/14-10/14 + Nachverr. 08/14-08/14 (Betrag enthaelt 10%U St: EUR 4 ,85), 2153, Patzenthal 7 RZBAATWWXXX AT673100000404011011 GIS Gebuehren Info Service GmbH (FN")
        self.assertEqual(t.payee, None)
        
        
    # also known as financial institute fee (FI fee)
    def testBankFee1(self):
        t = self.gTdesc("Kontoeroeffnung                               BG/000000001     ")
        self.assertEqual(t.type, "BG")
        self.assertEqual(t.htype, "bankfee")
        self.assertEqual(t.memo, "Kontoeroeffnung")
        self.assertEqual(t.payee, None)
        

    def testBankFee2(self):
        t = self.gTdesc("BG/000000052 Entgelt fuer Kontofuehrung    ")
        self.assertEqual(t.type, "BG")
        self.assertEqual(t.htype, "bankfee")
        self.assertEqual(t.memo, "Entgelt fuer Kontofuehrung")
        self.assertEqual(t.payee, None)
        

    def testBankFee3(self):
        t = self.gTdesc("RI/000000121 Entgelt fuer Mahnung    ")
        self.assertEqual(t.type, "RI")
        self.assertEqual(t.htype, "bankfee")
        self.assertEqual(t.memo, "Entgelt fuer Mahnung")
        self.assertEqual(t.payee, None)
        
    def testCreditCardBill1(self):
        t = self.gTdesc("easy kreditkarte VISA                        MC/000000338 Abrechnung Nr. 000000020")
        self.assertEqual(t.type, "MC")
        self.assertEqual(t.htype, "credit card bill")
        self.assertEqual(t.memo, "easy kreditkarte VISA Abrechnung Nr. 000000020")
        self.assertEqual(t.payee, None)

        
if __name__ == '__main__':
    unittest.main()
            
