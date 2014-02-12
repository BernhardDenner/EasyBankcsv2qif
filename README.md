## _easyBankcsv2qif.py_

This is a little python script to convert a CSV file from the online bank platform Easybank (or Bawak PSK works also) into QIF format. This format can be read by many accounting applications like [Homebank](http://homebank.free.fr/) or [GnuCash](http://www.gnucash.org/). 

The script extracts the following fields for each transaction:
* account number
* transaction date
* amount
* currency (default is fixed to EUR)
* transaction description: since this information is often very cryptic, the conversion tries to rebuild a suitable description. Additionally, other useful information is some how encoded in this field. Therefor some heuristics try to extract this info, like:
  * transaction type: like transfer, payment, withdraw...
  * payee
  * memo

Currently I'm using this script for converting Easybank and Bawag-PSK CSV file into QIF, which I import in Homebank to manage my transactions. 

