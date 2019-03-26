# CO2 Logger

A simple utility to log CO2 sensor readings to a Google Sheets spreadsheet.
For use with COZIR sensors.

## Quick start
```
$ python setup.py build
$ python setup.py install

$ co2_logger --help
usage: co2_logger [-h] [-v] --device DEVICE --sheetid SHEETID --range RANGE
                   --service-acct SERVICE_ACCT [--poll-interval POLL_INTERVAL]

CO2 Google Sheets Logger

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  --device DEVICE       Serial device for sensor
  --sheetid SHEETID     Google Sheets spreadsheets id.
  --range RANGE         Target sheet range. E.g "Sheet1!A1:C"
  --service-acct SERVICE_ACCT
                        Google service account JSON file
  --poll-interval POLL_INTERVAL
                        sensor poll interval in seconds (default=300)
```
