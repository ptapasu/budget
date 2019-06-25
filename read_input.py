import os
import csv
import sqlite3
import datetime
import logging


'''This reads csv files in the input folder named "mastercard"," bnz" and "visa". Then...'''


def logger():
    """A tool for logging events in the program to alter the log reporting change the level: logging.INFO, logging.DEBUG, logging.ERROR"""
    logging.basicConfig(filename='./app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.ERROR)
    logging.debug('input_reader: running module read_bank_input')

    
def get_max_pk(c):
    logging.debug('input_reader: running module read_bank_input.get_max_pk')
    try:
        c.execute('SELECT max(primary_key) FROM bankdata')
        output = c.fetchone()[0]
        return output
    except TypeError:
        return 0


def checkforexistence():
    #check for a matching entry but one that is not entered today??? maybe... lets try it. 
    c.execute("SELECT rowid FROM table WHERE data = ? AND AMOUNT = ? AND PAYEE = ? AND PARTICULAR = ? AND trans type = ? and reference = ?")
    output = cursor.fetchone()[0]
    if data==0:
        print('no duplicate found')
    else:
        print('duplicate found')


def first_date(filename):
    logging.debug('input_reader: running module read_bank_input.first_date')
    try:
        with open (filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count =0
            for row in csv_reader:
                if line_count==0:
                    line_count +=1
                else:
                    return datetime.datetime.strptime(row[0], '%d/%m/%y').strftime('%d-%m-%Y')
    except FileNotFoundError:
        logging.error('input_reader: cannot find the path or file')

        
def csvreader(filename,name,c):
    logging.debug('input_reader: running module read_bank_input.csvreader')
    max_pk = 0
    max_pk = get_max_pk(c)
    first_entrydate = first_date(filename)
    with open (filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count==0:
                line_count +=1
            else:
                #check for a matching entry but one that is not entered today??? maybe... lets try it. 
                format_date = datetime.datetime.strptime(row[0], '%d/%m/%y')
                output_date = format_date.strftime('%d/%m/%Y')
                todays_date = datetime.date.today().strftime('%d/%m/%y')
                max_pk+=1
                if name == 'bnz':
                    data=(max_pk,todays_date,output_date,abs(float(row[1])),row[2],row[3],row[6],row[5],row[13],'bnz_everyday')#13
                    c.execute('INSERT INTO bankdata VALUES(?,?,?,?,?,?,?,?,NULL,NULL,?,NULL,?)', data)#8
                    line_count +=1
                else:
                    data=(max_pk,todays_date,output_date,abs(float(row[1])),row[2],row[3],row[6],row[5],row[7],'mastercard')#13
                    c.execute('INSERT INTO bankdata VALUES(?,?,?,?,?,?,?,?,NULL,NULL,?,NULL,?)', data)#8
                    line_count +=1
        logging.debug(f'input_reader: Processed {line_count} lines.')
        return first_entrydate #this is a timestamp that will be added to the archive file created as a copy of the .csv


def check_file(file_name,name,c):
    logging.debug('input_reader: running module read_bank_input.check_file')
    if os.path.isfile(file_name)==True:
        arc_date = csvreader(file_name,name,c)
        try:
            os.rename(file_name, f'./archive/period_{arc_date}.arc_{name}.added_{datetime.date.today().strftime("%d-%m-%y")}.csv')
        except FileNotFoundError:
            logging.error('input_reader: cannot find the path or file')


def read_input():
    conn = sqlite3.connect('mydata.sqlite3')
    c = conn.cursor()
    for x in ['mastercard','bnz','visa']:
        check_file(f'./input/{x}.csv',x,c)
    conn.commit()
    conn.close()


if __name__=='__main__':
    logger()
    read_input()

'''
                data=(max_pk,todays_date,output_date,row[1],row[2],row[3],row[6],row[5],row[13],'bnz_everyday')#13
                c.execute('INSERT INTO bankdata VALUES(?,?,?,?,?,?,?,?,NULL,NULL,?,NULL,?)', data)#8
                line_count +=1
'''

