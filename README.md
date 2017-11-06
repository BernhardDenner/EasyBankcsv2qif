## _easyBankcsv2qif.py_

This is a little python script to convert a CSV file from the online bank platform Easybank (or BAWAG PSK works also) into QIF format. This format can be read by many accounting applications like [Homebank](http://homebank.free.fr/) or [GnuCash](http://www.gnucash.org/). 

The script extracts the following fields for each transaction:
* account number
* transaction date
* amount
* currency (default is fixed to EUR)
* transaction description: since this information is often very cryptic, the conversion tries to rebuild a suitable description. Additionally, other useful information is some how encoded in this field. Therefor some heuristics try to extract this info, like:
  * transaction type: like transfer, payment, withdraw...
  * payee
  * memo

Additionally, the script is able to change the character encoding of the input data. 

For usage details, see `./easyBankcsv2qif.py -h`

Currently I'm using this script for converting Easybank and BAWAG-PSK CSV file into QIF, which I import in Homebank to manage my transactions. 

## _easyBankcsv2qifFrontend.py_

This script is a small GTK3 frontend for easyBankcsv2qif.py. It takes the input file's filename as parameter, asks the user for the output filename, does the csv 2 qif conversion and after a short summary the input file is deleted. This script is designed to open the downloaded CSV file from the ebanking Webapp directly with the browser, thus avoiding the need of the command line.
Additionally an account name can be specified, which will be added to the QIF file. This information can be used to directly refer to a Homebanks account name, thus having selected the correct import target account. Already entered account names are stored in `~/.config/easyBankcsv2qifFrontend.conf` and don't need to be typed again.

Note: the Frontend script uses a fixed enconding, from iso-8859-1 to utf-8

Note: this is my first python script. Any comments on it are welcome ;)
