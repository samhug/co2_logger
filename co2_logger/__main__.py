import argparse
import logging
import sys

from time import sleep
from datetime import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account

from cozir import Cozir

LOGGER = logging.getLogger()


def get_google_sheets_service(service_account_file):
    '''Connects and authenticates with the Google Sheets API and returns a
    service object.
    '''
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)

    return service


def append_data(service, sheet_id, sheet_range, values):
    '''appends a set of values to the given spreadsheet range
    '''
    sheet = service.spreadsheets()

    request = sheet.values().append(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption='USER_ENTERED',
        body={'values': values})
    response = request.execute()

    # TODO: check response


def get_co2_sensor(device):
    return Cozir(device)


def read_sensor_value(sensor):
    '''reads the current value from the given sensor
    '''
    multi = sensor.read_CO2_multiplier()
    return multi * sensor.read_CO2()


def main(args=None):
    '''The main routine'''
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='CO2 Google Sheets Logger')
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    parser.add_argument(
        '--device', type=str, required=True, help='Serial device for sensor')
    parser.add_argument(
        '--sheetid',
        type=str,
        required=True,
        help='Google Sheets spreadsheets id.')
    parser.add_argument(
        '--range',
        type=str,
        required=True,
        help='Target sheet range. E.g "Sheet1!A1:C"')
    parser.add_argument(
        '--service-acct',
        type=str,
        required=True,
        help='Google service account JSON file')
    parser.add_argument(
        '--poll-interval',
        type=int,
        default=300,
        help='sensor poll interval in seconds (default=300)')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    LOGGER.info(
        'initializing CO2 logger with device=%s, sheetid=%s, range=%s, \
poll-interval=%d',
        args.device,
        args.sheetid,
        args.range,
        args.poll_interval,
    )

    service = get_google_sheets_service(args.service_acct)

    sensor = get_co2_sensor(args.device)

    while True:
        sensor_value = read_sensor_value(sensor)
        row = [str(datetime.now()), sensor_value]
        append_data(service, args.sheetid, args.range, [row])

        sleep(args.poll_interval)


if __name__ == '__main__':
    main()
