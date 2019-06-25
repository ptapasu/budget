import sqlite3
import csv
import logging



''' What this does is looks at through the coding file, then returns from that a list
of all the payees that do not have a default code assigned to them.
For example KFC would normally go under the code takeaways, but maybe an individual
store like KFC-12 would not have been added to the coding file, so just copy the name
from payees and add it to coding to have it categorised correctly.
It also identifies any payee in the DB which is not assigned to payees or coding
and adds it to payees'''


def logger():
    """A tool for logging events in the program to alter the log reporting change the level: logging.INFO, logging.DEBUG, logging.ERROR"""
    logging.basicConfig(filename='./app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.ERROR)
    logging.debug('unassigned_payees: running module unassigned_payee_update')
    

def payee_scraper():
    logging.debug('unassigned_payees: running module unassigned_payee_update function payee_scraper')
    conn = sqlite3.connect('mydata.sqlite3')
    c = conn.cursor()
    c.execute(f"SELECT DISTINCT(payee) FROM bankdata;")
    data = c.fetchall()
    return data


def existing_codes():
    logging.debug('unassigned_payees: running module unassigned_payee_update function existing_codes')
    current_codes = []
    try:
        with open('./configuration/coding.csv') as coding:
            csv_reader = csv.reader(coding, delimiter=',')
            for row in csv_reader:
                for i in row:
                    if i != '':
                        current_codes.append(i)
        current_codes = set(current_codes)
        return current_codes
    except FileNotFoundError:
            logging.error(f'unassigned_payees: Could not find the path or file "/configuration/coding.csv')


def write_unassigned(data, current_codes):
    logging.debug('unassigned_payees: running module unassigned_payee_update function write_unassigned')
    try:
        with open(f'./configuration/payees.csv', 'w', newline='') as csv_file:
            data_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in data:
                if i[0] not in current_codes:
                    data_writer.writerow(i)
    except FileNotFoundError:
            logging.error(f'unassigned_payees: Could not find the path or file "/configuration/payee.csv')
            

if __name__=="__main__":
    logger()
    data = payee_scraper()
    current_codes = existing_codes()
    write_unassigned(data, current_codes)
    
