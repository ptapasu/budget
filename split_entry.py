import csv
import sqlite3
import datetime
import os
import logging



'''This will take a primary key number from the db and allow you to split it into
multiple smaller entries, hiding the original and stopping it from being re-categorized.'''


def logger():
    """A tool for logging events in the program to alter the log reporting change the level: logging.INFO, logging.DEBUG, logging.ERROR"""
    logging.basicConfig(filename='./app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.ERROR)
    logging.debug('code_entries: running module assign_code_to_db_entries')


def n_validator(text):
    while True:
        print(text)
        n = input('')
        try:
            n = int(n)
            return n
        except ValueError:
            input('Not a number | Press enter to continue')
            os.system('cls')
            
            
def entry(n):
    conn = sqlite3.connect('mydata.sqlite3')
    c = conn.cursor()
    c.execute(f'SELECT * FROM bankdata WHERE primary_key = {n}')
    entry = c.fetchone()
    return (entry)


def make_code_list():
    codings = []
    with open ('./configuration/coding.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
                label = row[0]
                codings.append(label)
    codings = codings[1::]
    return codings


def code_text(codings):
    text = ''
    for counter, value in enumerate(codings):
        text += f'{counter}-{value}\n'
    return text


def less_than(text,x):
    while True:
        print(text)
        n = input('')
        try:
            n = int(n)
            if n<=x:
                return n
            else:
                input('This number is bigger than the original entry | Press enter to continue')
                os.system('cls')
        except ValueError:
            input('Not a number | Press enter to continue')
            os.system('cls')

            
def choose_code():
    while True:
        answer = less_than(f'{code_command}Please enter your choice of code for the entry',len(code_list))
        os.system('cls')
        return code_list[answer]


def get_max_pk():
    c.execute('SELECT max(primary_key) FROM bankdata')
    output = c.fetchone()[0]
    return output


def true_false(text):
    while True:
        print(text)
        response = input('')
        try:
            if response[0].lower() in ['y','n']:
                return response[0].lower()
        except IndexError:
            continue

        
def confirm_record():
    while True:
        pk = n_validator('Please enter the primary key of the entry you wish to split')
        prime_shard = entry(int(pk))
        if prime_shard != None:
            print(f'The record which you have selected to split is:\n{prime_shard}')
            response = true_false('Is this correct?')
            if response == 'y':
                os.system('cls')
                return prime_shard


code_list = make_code_list()
code_command = code_text(code_list)

conn = sqlite3.connect('mydata.sqlite3')
c = conn.cursor()
max_pk = get_max_pk()


prime_shard = confirm_record()

shard_values = []
shard_moolah = abs(int(prime_shard[3]))
todays_date = datetime.date.today().strftime('%d/%m/%y')
shards = []
while shard_moolah>0:
        shard_c = less_than(f'There is ${shard_moolah} left to assign from the original entry and you are on entry {len(shard_values)+1}\nHow much money did you want to assign to this new entry?',shard_moolah)
        os.system('cls')
        shard_moolah -= shard_c
        this_code = choose_code()
        comment = input(f'Please enter a comment or press return.\n')
        shard_values.append([this_code,shard_c,comment])
        print(f'You have chosen to make an entry with ${shard_c}, the code {this_code} and the comment {comment}')
        input('-Press enter to continue-')
        os.system('cls')
        
for i in shard_values:
    max_pk+=1
    this_comment = f'{i[2]}. A child of parent entry {prime_shard[0]}'
    data = (max_pk, todays_date,prime_shard[2],i[1], prime_shard[4],prime_shard[5],prime_shard[6],prime_shard[7], i[0] ,this_comment,prime_shard[10],'Yes',prime_shard[12])
    c.execute('INSERT INTO bankdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
    shards.append(max_pk)

print(shards)

main_data = ('split','yes',f'This entry is the originator of the entries:{shards} and was updated on {todays_date}',prime_shard[0])
c.execute('UPDATE bankdata SET CODE = ?, EDITED = ?, COMMENT = ?  WHERE primary_key = ?', (main_data))


conn.commit()
conn.close()
'''
if __name__=="__main__":
    pass
'''
