import sqlite3
import openpyxl
import datetime
import csv
from openpyxl.styles.borders import Border, Side
todate = str(datetime.datetime.now()).split()[0]
db = 'mydata.sqlite3'
conn = sqlite3.connect(db)


def data_grabber(code):
    c = conn.cursor()
    c.execute(f"SELECT * FROM bankdata WHERE code LIKE '{code}';")
    data = c.fetchall()
    return data


border_style = Border(left=Side(border_style=None,
                           color='FF000000'),
                 right=Side(border_style=None,
                            color='FF000000'),
                 top=Side(border_style=None,
                          color='FF000000'),
                 bottom=Side(border_style='thick',
                             color='FF000000'),
                 diagonal=Side(border_style=None,
                               color='FF000000'),
                 diagonal_direction=0,
                 outline=Side(border_style=None,
                              color='FF000000'),
                 vertical=Side(border_style=None,
                               color='FF000000'),
                 horizontal=Side(border_style=None,
                                color='FF000000'))


code_list = []
with open('./configuration/coding.csv') as coding:
    csv_reader = csv.reader(coding, delimiter=',')
    line_count=0
    for row in csv_reader:
        if line_count == 0:
            line_count +=1
        else:
            code_list.append(row[0])


def budget(code):
    conn = sqlite3.connect('mydata.sqlite3')
    cz = conn.cursor()
    cz.execute(f'SELECT amount FROM budget WHERE category like "{code}"')
    output = cz.fetchone()[0]
    return output
    
def styler(i):
    wb[i]['A1'].font = openpyxl.styles.Font(bold=True, color='FFF00000')
    wb[i]['B1'].font = openpyxl.styles.Font(bold=True, color='FFF00000')
    wb[i]['C1'].font = openpyxl.styles.Font(bold=True, color='FFF00000')
    wb[i]['D1'].font = openpyxl.styles.Font(bold=True, color='FFF00000')
    wb[i]['A1'].border = border_style
    wb[i]['B1'].border = border_style
    wb[i]['C1'].border = border_style
    wb[i]['D1'].border = border_style

path = f'./report/Report-{todate}.xlsx'
wb = openpyxl.Workbook()
ws_count = 0
for i in code_list:
    if ws_count == 0:
        ws = wb.active
        ws.title = i
        wb[i].append(['DATE','AMOUNT','PAYEE','PK'])
        wb[i].freeze_panes = 'A2'
        styler(i)
        w_data = data_grabber(i)
        count = 1
        for entry in w_data:
            ws.append([entry[2],((entry[3])),entry[4],entry[0]])
            count+=1
        ws_count +=1
        wb[i].append([''])
        wb[i].append(['Spent',f'=SUM(B2:B{count})',])
        this_budget = budget(i)
        wb[i].append(['Budget',this_budget])
        wb[i].append(['Remaining',f'={this_budget}-SUM(B2:B{count})'])
    else:
        w_data = data_grabber(i)
        if len(w_data)>0:
            wb.create_sheet(i)
            wb[i].append(['DATE','AMOUNT','PAYEE','PK'])
            wb[i].freeze_panes = 'A2'
            styler(i)
            count = 1
            for entry in w_data:
                wb[i].append([entry[2],((entry[3])),entry[4],entry[0]])
                count+=1
            if count>1:
                wb[i].append([''])
                wb[i].append(['Spent',f'=SUM(B2:B{count})',])
                this_budget = budget(i)
                if i!='NULL':
                    wb[i].append(['Budget',this_budget])
                    wb[i].append(['Remaining',f'={this_budget}-SUM(B2:B{count})'])
                              
wb.save(path)



