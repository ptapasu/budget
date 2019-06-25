import csv
import sqlite3
import shutil
import datetime
import logging



'''This looks throug the coding csv file, and for each (BUDGET) category, looks for items (payees) which are on the db. From there it assigns them that particular code'''


def logger():
    """A tool for logging events in the program to alter the log reporting change the level: logging.INFO, logging.DEBUG, logging.ERROR"""
    logging.basicConfig(filename='./app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.ERROR)
    logging.debug('code_entries: running module assign_code_to_db_entries')


def backup():
        logging.debug('code_entries: running module assign_code_to_db_entries.backup')
        try:
                todays_date = datetime.datetime.now().strftime('%H%M%S.%d-%m-%y')
                shutil.copy('mydata.sqlite3',f'./archive/{todays_date}.backup.mydata.sqlite3')
        except FileNotFoundError:
                logging.error(f'code_entries: Could not find the database or the archive folder to backup the database')


def coder():
        logging.debug('code_entries: running module assign_code_to_db_entries.coder')
        try:
                conn = sqlite3.connect('mydata.sqlite3')
                c = conn.cursor()
                with open ('./configuration/coding.csv') as csvfile:
                        logging.debug('code_entries: Checking configuration file "coding.csv"')
                        csv_reader = csv.reader(csvfile, delimiter=',')
                        for row in csv_reader:
                                label = row[0]
                                for item in row:
                                        if len(item) != 0:
                                                data = (label, item)
                                                c.execute('UPDATE bankdata SET CODE = ? WHERE payee LIKE ? AND code IS NULL AND edited IS NULL', (data))
                conn.commit()
                conn.close()
        except FileNotFoundError:
                logging.error(f'code_entries: Could not find the path or file "/configuration/coding.csv')


if __name__ == "__main__":
        logger()
        backup()
        coder()
        
