from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import datetime
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#charting
from reportlab.lib.colors import PCMYKColor
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend
import data
import sqlite3



month = 0
year = 0


def time_period(m=0,y=0):
    global month
    global year
    if m==0:
        month = (int(datetime.date.today().strftime('%m'))-1)
    if y==0:
        year = (int(datetime.date.today().strftime('%Y')))

time_period()

pdfmetrics.registerFont(TTFont('Alegreya-Regular', 'Alegreya-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Alegreya-Italic', 'Alegreya-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Oswald-Bold', 'Oswald-Bold.ttf'))
PAGE_WIDTH  = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]

todays_date = datetime.date.today().strftime('%d %B %Y')

clothing = ['uniforms','peter_clothing_allowance','emily_clothing_allowance','laiken_clothing_allowance','levi_clothing_allowance']
transport = ['bus_card','petrol','car_maintenance','parking']
insurance = ['contents_insurance','house_insurance','mazda_insurance',
             'nissan_insurance','peter_life_insurance','emily_life_insurance',
             'funeral_insurance']
food = ['groceries','takeaways']
medical_and_dental = ['medical_dental']
housing = ['mortgage','misc_house_spending']
utilities = ['power','phone','cellphone_topup']
education = ['school','stationary']
gifts = ['birthday_gifts','christmas_gifts','world_vision','jope']
entertainment = ['entertainment','holiday','netflix_spotify','allowances']


month_name = ['','January','Febuary','March','April','May','June','July','August','September','October','November','December']
year = '2019'
c = canvas.Canvas(f"./report/{month_name[month]}Budget.pdf", pagesize=A4)
main_title = f'Budget Report {month_name[month]} {year}'
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

serif_font ='Times-Roman'
serif_italic = 'Times-Italic'
serif_bold = 'Times-Bold'
sans_font = 'Oswald-Bold'

guides = False

def title(c, text):
    c.setFont(sans_font, 30, None)
    c.drawString((PAGE_WIDTH - c.stringWidth(text,sans_font,30)) / 2.0, 750, text)


def header(c):
    c.setFont(serif_font, 11, None)
    c.drawString(50, 820, main_title)
    page_number = c.getPageNumber()
    c.drawString(510, 820, f'Page {page_number}')
    a = 40
    b = PAGE_WIDTH-a
    c.line(a,810,b,810)


def paragraph(c,t,pw,ph):
    style = ParagraphStyle(
        name = 'Normal',
        fontName = serif_font,
        fontSize = 11)
    p = Paragraph(t,style)
    aW = 220 #Width
    aH = 100 #Height
    w, h = p.wrap(aW, aH)
    p.drawOn(c,pw,ph,aH)

figure_n = 1

#Overview
overview_text = 'Figure one shows how much money has been spent per month with the current month represented with the colour blue.  Figure two is a breakdown of this months spending by budget category.  Figure three shows the total spending by month and the remaining budget.  Figure four shows this months spending after removing housing.  Figure five shows spending so far, and a prediction of how much of the budget will be available by month. Table one shows the spending in dollars for the previous month and the current month by category.'
a = [f'{month_name[month]} has seen HIGH/MODERATE/LOW spending in comparison with previous months, this can be seen ',
     f' in Figure 1 where the current month is represented in blue and the previous months black. The five areas with',
     f' the most spending this month were a,b,c,d, and e (Figure 2).  Although {month_name[month]} represents % of the',
     f' year it is representative of % of the spending (Figure 3).  This suggests that if nothing is changed about the ',
     f' budget we will have bdivivdebymonth for the next x months, this is represented by the red bars in Figure 1.']

overview_text = ''.join(a)

def overview_year_spend_by_month(c,w,h):
    my_data = data.monthly_total(year)
    total_budget = data.budget()
    left_budget = (total_budget - sum(my_data))/(12-month)
    for i in range(month,12):
        my_data[i]=left_budget
    d = Drawing(0, 0)
    bar = VerticalBarChart()
    bar.x = 150
    bar.y = 150
    bar.data = [my_data]
    bar.valueAxis.valueMin = 0
    bar.categoryAxis.categoryNames = ['Jan', 'Feb', 'Mar',
                                      'Apr', 'May', 'Jun',
                                      'Jul','Aug','Sep','Oct','Nov','Dec']
    bar.categoryAxis.labels.fontName = serif_font
    bar.valueAxis.labels.fontName = serif_font
    bar.categoryAxis.labels.boxAnchor = 'n'
    bar.categoryAxis.labels.angle = 90
    bar.categoryAxis.labels.dy = -15
    bar.categoryAxis.labels.dx = -10
    bar.bars[0].fillColor   = PCMYKColor(150,150,150,150,alpha=85)
    bar.bars[(0,month-1)].fillColor = PCMYKColor(150,0,0,0,alpha=85)
    for i in range(month,13):
        bar.bars[(0,i)].fillColor = PCMYKColor(0,150,150,0,alpha=85)
    d.add(bar, '')
    d.drawOn(c,w,h)


def overview_month_spending_breakdown_pie(c,h,w):
    categories = ['Clothing','Transport','Insurance','Food','Medical and Dental','Housing','Utilities','Education','Gifts','Entertainment']
    d = Drawing()
    pie = Pie()
    pie.sideLabels = 1
    pie._seriesCount = 10
    my_data = []
    for x in categories:
        my_data.append(data.category_data(x.lower(),month,2019))
    pie.x = 0
    pie.y = 0
    pie.width = 100

    pie.height = pie.width
    pie.data = my_data
    pie.slices.fontName = serif_font
    pie.slices.fontSize = 11
    pie.labels = tuple(categories)
    pie.slices.strokeWidth = 0.5
    #pie.slices[3].popout = 20
    d.add(pie)
    d.drawOn(c,h,w)

    
def overview_budget_spent(c,w,h):
    my_data = data.monthly_total(year)
    my_data = my_data[0:month]
    budget = data.budget()-sum(my_data)
    my_data.append(budget)
    my_label = []
    label = ['January','Febuary','March','April','May','June','July','August','September','October','November','December']
    for j in range(0,month):
        my_label.append(label[j])
    my_label.append('Budget remaining')
    d = Drawing()
    pie = Pie()
    pie.sideLabels = 1
    pie._seriesCount = 10
    pie.x = 0
    pie.y = 0
    pie.width = 100
    pie.height = pie.width
    pie.data = my_data
    pie.slices.fontName = serif_font
    pie.slices.fontSize = 11
    pie.labels = my_label
    pie.slices.strokeWidth = 0.5
    pie.slices[-1].popout = 20
    d.add(pie)
    d.drawOn(c,w,h)


def overview_table(c,h,w):
    width = 400
    height = 100
    category = ['Clothing','Transport','Insurance','Food','Housing','Medical and Dental','Utilities','Education','Gifts','Entertainment']
    my_data = [['Category', 'Previous M', 'Current M','M Average','Spent YTD','Budget','Budget Remaining']]
    for x in category:
        my_data.append([x.title(),f'${round(data.category_data(x.lower(),month-1,year),2)}',f'${round(data.category_data(x.lower(),month,year),2)}'])
    f = Table(my_data, style =[('LINEBELOW',(0,0),(-1,-1),1,colors.black)])
    f.wrapOn(c, width, height)
    f.drawOn(c, h, w)

#EOF Overview


#weekly
    
def monthly_spending_bar(c,category,h,w):
    """
    Creates a bar graph in a PDF
    """
    my_data = []
    for i in range(1,12+1):
        my_data.append(data.category_data(category.lower(),i,year))
    for i in range(month, 12):
        my_data[i]=0
    #d = Drawing(300, 250)
    d = Drawing(0, 0)
    bar = VerticalBarChart()
    bar.x = 150
    bar.y = 150
    bar.data = [my_data]
    bar.valueAxis.valueMin = 0
    bar.categoryAxis.categoryNames = ['Jan', 'Feb', 'Mar',
                                      'Apr', 'May', 'Jun',
                                      'Jul','Aug','Sep','Oct','Nov','Dec']
    bar.categoryAxis.labels.fontName = serif_font
    bar.valueAxis.labels.fontName = serif_font
    bar.categoryAxis.labels.boxAnchor = 'n'
    bar.categoryAxis.labels.angle = 90
    bar.categoryAxis.labels.dy = -15
    bar.categoryAxis.labels.dx = -10
    #below change monnth number based upon current month
    bar.bars[0].fillColor   = PCMYKColor(150,150,150,150,alpha=85)
    bar.bars[(0,month-1)].fillColor = PCMYKColor(150,0,0,0,alpha=85)
    d.add(bar, '')
    d.drawOn(c,200,480)


def monthly_spending_breakdown_pie(c,category,h,w,v=False):
    d = Drawing()
    pie = Pie()
    pie.sideLabels = 1
    pie._seriesCount = 10
    output = []
    my_data = []
    output = data.cat_ind_data(category,month,year)

    my_data = output[1]
    labels = output[0]
    if sum(my_data)==0:
        return
    pie.x = 0
    pie.y = 0
    pie.width = 100
    pie.height = pie.width
    pie.data = my_data
    pie.slices.fontName = serif_font
    pie.slices.fontSize = 11
    pie.labels = labels
    pie.slices.strokeWidth = 0.5
    #pie.slices[3].popout = 20
    d.add(pie)
    d.drawOn(c,h,w)

def monthly_spending_cat_pie(c,category,h,w,v=False):
    d = Drawing()
    pie = Pie()
    pie.sideLabels = 1
    pie._seriesCount = 10
    spent = 0
    my_data = []
    for i in range(1,month+1):
        spent+=int(data.month_code(category,i,year))
    print(spent,category)
    my_data.append(spent)
    my_data.append(data.code_budget(category)-spent)
    labels = [f'{category} spending','budget left']
    if sum(my_data)==0:
        return
    pie.x = 0
    pie.y = 0
    pie.width = 50
    pie.height = pie.width
    pie.data = my_data
    pie.slices.fontName = serif_font
    pie.slices.fontSize = 11
    pie.labels = labels
    pie.slices.strokeWidth = 0.5
    #pie.slices[3].popout = 20
    d.add(pie)
    d.drawOn(c,h,w)
    
def category_budget_left_pie(c,category,h,w):
    my_data = []
    for x in range(1,month+1):
        my_data.append(data.category_data(category,x,year))
    labels = month_name[1:month+1]
    labels.append('Budget')
    my_data.append(data.category_budget(category)-sum(my_data))
    d = Drawing()
    pie = Pie()
    pie.sideLabels = 1
    pie._seriesCount = 10
    #if legend:
    #    add_legend(d, pie, data)
    pie.x = 0
    pie.y = 0
    pie.width = 100
    pie.height = pie.width
    pie.data = my_data
    pie.slices.fontName = serif_font
    pie.slices.fontSize = 11
    pie.labels = labels
    pie.slices.strokeWidth = 0.5
    #pie.slices[3].popout = 20
    d.add(pie)
    d.drawOn(c,h,w)


def category_predicted_spending(c,category,h,w):
    """
    Creates a bar graph in a PDF
    """
    my_data = []
    for i in range(1,month+1):
        my_data.append(round(data.category_data(category,i,year)))
    budget = data.category_budget(category)
    re_budget = (budget - sum(my_data))/(12-month)
    for x in range(month,12):
        my_data.append(re_budget)

    d = Drawing(0, 0)
    bar = VerticalBarChart()
    bar.x = 150
    bar.y = 150
    bar.data = [my_data]
    bar.valueAxis.valueMin = 0
    bar.categoryAxis.categoryNames = ['Jan', 'Feb', 'Mar',
                                      'Apr', 'May', 'Jun',
                                      'Jul','Aug','Sep','Oct','Nov','Dec']
    bar.categoryAxis.labels.fontName = serif_font
    bar.valueAxis.labels.fontName = serif_font
    bar.categoryAxis.labels.boxAnchor = 'n'
    bar.categoryAxis.labels.angle = 90
    bar.categoryAxis.labels.dy = -15
    bar.categoryAxis.labels.dx = -10
    #below change monnth number based upon current month
    bar.bars[0].fillColor   = PCMYKColor(150,150,150,150,alpha=85)
    for i in range(month,12):
        bar.bars[(0,i)].fillColor = PCMYKColor(0,150,150,0,alpha=85)
    d.add(bar, '')
    d.drawOn(c,h,w)


def category_overview_table(c,category,h,w):
    my_codes = ''
    if category =='clothing':
        my_codes = clothing
    elif category =='transport':
        my_codes = transport
    elif category =='insurance':
        my_codes = insurance
    elif category =='food':
        my_codes = food
    elif category == 'medical and dental':
        my_codes = medical_and_dental
    elif category == 'housing':
        my_codes = housing
    elif category == 'utilities':
        my_codes = utilities
    elif category == 'education':
        my_codes = education
    elif category == 'gifts':
        my_codes = gifts
    elif category == 'entertainment':
        my_codes = entertainment
    width = 400
    height = 100
    my_data = [['Category', 'Previous', 'Current']]
    for x in my_codes:
        my_data.append([x.replace('_',' ').title(),f'${round(data.month_code(x.lower(),month-1,year),2)}',f'${round(data.month_code(x.lower(),month,year),2)}'])
    f = Table(my_data, style =[('LINEBELOW',(0,0),(-1,-1),1,colors.black)])
    f.wrapOn(c, width, height)
    f.drawOn(c, h, w)

def top_spend_table(c,category,h,w):
    my_codes = ''
    if category =='clothing':
        my_codes = clothing
    elif category =='transport':
        my_codes = transport
    elif category =='insurance':
        my_codes = insurance
    elif category =='food':
        my_codes = food
    elif category == 'medical and dental':
        my_codes = medical_and_dental
    elif category == 'housing':
        my_codes = housing
    elif category == 'utilities':
        my_codes = utilities
    elif category == 'education':
        my_codes = education
    elif category == 'gifts':
        my_codes = gifts
    elif category == 'entertainment':
        my_codes = entertainment
    width = 600
    height = 500
    my_data = [['Category', 'Payee', 'Amount','Date']]
    for x in my_codes:
        k = data.top_five(x,month,year)
        if k[0]!=None:
            k = k[0]
            my_data.append([x.replace('_',' ').title(),k[4].title(),f'${k[3]}',k[2]])
        else:
            my_data.append([x.replace('_',' ').title(),'',f'$0',''])
    f = Table(my_data, style =[('LINEBELOW',(0,0),(-1,-1),1,colors.black)])
    f.wrapOn(c, width, height)
    f.drawOn(c, h, w)

#eof weekly


def figure_label(c,w,h,z,text):
    global figure_n
    c.setFont(serif_italic, 11, None)
    c.drawString(w, h, f'Figure {figure_n}.')
    c.setFont(serif_font, 11, None)
    c.drawString(w+45, h, f'{text}')
    figure_n+=1

    
def title_page_heading(c,text):
    c.setFont(sans_font, 40, None)
    c.drawString((PAGE_WIDTH - c.stringWidth(text,sans_font,40)) / 2.0, PAGE_HEIGHT/2.0, text)
    line_height_up = PAGE_HEIGHT/2.0 +60
    line_height_down = PAGE_HEIGHT/2.0 -30
    c.line(30,line_height_up,560,line_height_up)
    c.line(30,line_height_down,560,line_height_down)


def title_page_time_stamp(c,text,h):
    c.setFont(serif_font, 11, None)
    text_width = c.stringWidth(text,serif_font, 11)
    c.drawString((PAGE_WIDTH - c.stringWidth(text,serif_font,11)) / 2.0, h, text)


def contents_list(c):
    pages = ['Overview','Clothing','Transport','Insurance','Food','Medical and Dental','Housing','Utilities','Education','Gifts','Entertainment','Conclusion']
    subheadings = [[],['Uniforms','Peter\'s Clothing','Emily\'s Clothing','Laiken\'s Clothing','Levi\'s Clothing'],['Bus card','Petrol','Car Maintenance'],['Content Insurance','House Insurance','Emily\'s Insurance','Peter\'s Insurance','Mazda Insurance','Nissan Insurance','Funeral Insurance'],
               ['Takeaways','Groceries'],['Medical','Dental'],['Mortgage','Rates','Home Amenities'],['Power','Phone','Cellphone'],['School Fees','Stationary'],['Birthday Gifts','Christmas Gifts','World Vision','Jope'],['Entertainment','Holiday Trips','Netflix/Spotify','Allowances'],[]]
    start_page = 3
    starting_height = 720
    height_modifier = -15
    for i in range(0,len(pages)):
        c.setFont(serif_bold, 12, None)
        c.drawString(100,starting_height,f'{pages[i]}')
        c.line(102+c.stringWidth(pages[i],serif_bold,12),starting_height,PAGE_WIDTH-102,starting_height)
        c.setFont(serif_bold, 11, None)
        c.drawString(PAGE_WIDTH-100,starting_height,f'{start_page}')
        starting_height+= height_modifier
        c.setFont(serif_font, 11, None)
        for j in subheadings[i]:        
            c.drawString(130,starting_height,f'{j}')
            c.drawString(PAGE_WIDTH-100,starting_height,f'{start_page}')
            starting_height+=height_modifier
        start_page+=1

       
def table_label(c,w,h,text,n):
    c.setFont(serif_font, 11, None)
    c.drawString(w, h+20, f'Table {n}.')
    c.setFont(serif_italic, 11, None)
    c.drawString(w, h, f'{text}')
    
def test(c):
    c.setFont(serif_font, 11, None)
    c.drawString(PAGE_WIDTH / 2.0, 300, f'{PAGE_HEIGHT} {PAGE_WIDTH}')
def table(c,h,w):
    width = 400
    height = 100
    data = [['Category', 'Jan', 'Feb', 'Avg'],
        ['Clothing', '11', '12', '13'],
        ['Transport', '21', '22', '23'],
        ['Insurance', '21', '22', '23'],
        ['Food', '11', '12', '13'],
        ['Medical and Dental', '21', '22', '23'],
        ['Housing', '21', '22', '23'],
        ['Utilities', '11', '12', '13'],
        ['Education', '21', '22', '23'],
        ['Gifts', '21', '22', '23'],
        ['Entertainment', '31', '32', '33'],
        ['Total', '31', '32', '33']]
    f = Table(data, style =[('LINEBELOW',(0,0),(-1,-1),1,colors.black)])
    f.wrapOn(c, width, height)
    f.drawOn(c, h, w)

def guidelines(c):
    if guides==True:
        c.line(50,50,50,800)
        c.line(272.5,50,272.5,800)
        c.line(322.5,50,322.5,800)
        c.line(545,50,545,800)

figure = 1

table = 1

#==|contents|==#
def contents():
    for x in ['contents','overview','clothing','transport',
          'food','house','utilities','insurance',
          'medical and dental','gift','entertainment','summary']:
        pass


title_page_heading(c,main_title)
title_page_time_stamp(c,f'Created on {todays_date}',50)
title_page_time_stamp(c,'Generated from code written by Peter Tapasu',30)
c.showPage()

#contents page
header(c)
title(c, 'Contents')
contents_list(c)                                                                                                                                            
c.showPage()

def page_fluff(cat):
    figure_n = 1
    header(c)
    guidelines(c)
    title(c, cat)
#month_minus_housing_spending_breakdown_pie
#overview page
    '''
figure_n = 1
header(c)
guidelines(c)
title(c, 'Overview')
'''
page_fluff('Overview')
paragraph(c,overview_text,55,590)
overview_year_spend_by_month(c,200,480)
figure_label(c,325,590,1,f'{year} Spending by month')
overview_month_spending_breakdown_pie(c,110,460)
figure_label(c,55,420,2,f'{month_name[month]} spending breakdown')
overview_budget_spent(c,370,460)
figure_label(c,325,420,3,'Spending by month and remainder')
table_label(c,55,360,'Spending breakdown (Month)',1)
overview_table(c,55,120)
c.showPage()

#clothing page W
figure_n = 1
header(c)
guidelines(c)
page_category = 'Clothing'
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_cat_pie(c,'takeaways',110,460)
figure_label(c,55,420,2,f'{month_name[month]} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()

#transport page W
figure_n = 1
header(c)
guidelines(c)
page_category = "Transport"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()


#insurance page A
header(c)
guidelines(c)
page_category = "Insurance"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,200)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,50)
c.showPage()


#food page W
header(c)
guidelines(c)
page_category = "Food"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()


#medical and dental I
header(c)
guidelines(c)
page_category = "Medical and Dental"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()


#housing page W
header(c)
guidelines(c)
page_category = "Housing"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()


#utilites page W
header(c)
guidelines(c)
page_category = "Utilities"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()

#education page I
header(c)
guidelines(c)
page_category = "Education"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460, v=True)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()

#gifts page I
header(c)
guidelines(c)
page_category = "Gifts"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()

#entertainment page I
header(c)
guidelines(c)
page_category = "Entertainment"
title(c, page_category )
paragraph(c,lorem,55,600)
monthly_spending_bar(c,page_category,200,480)
figure_label(c,325,590,1,f'Spending on {page_category} by month')
monthly_spending_breakdown_pie(c,page_category.lower(),110,460)
figure_label(c,55,420,2,f'{month} {page_category} spending breakdown')
category_budget_left_pie(c,page_category.lower(),370,460)
figure_label(c,330,420,3,f'{page_category} Total Spending by Month')
category_predicted_spending(c,page_category.lower(),-40,140)
figure_label(c,55,250,4,'Predicted Budget Available by Month')
table_label(c,325,360,'Spending breakdown (Month)',1)
category_overview_table(c,page_category.lower(),324,240)
table_label(c,55,200,'Largest purchases',2)
top_spend_table(c,page_category.lower(),55,90)
c.showPage()

c.save()
