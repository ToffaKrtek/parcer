from bs4 import BeautifulSoup
import requests as req
import xlwt

main_link = "https://dinkom.ru/study/"
# parent_selector = input()
# child_selector = input()
all_links = []
all_ready_links = []

# def getLinks(link, selector_parent, selector_child):


resp = req.get(main_link)
html = BeautifulSoup(resp.content, 'html.parser')

for el in html.select('div.item-views.sections'):
    title = el.select('div.image > a')
    for link in title:
        all_links.append(link.get('href'))

# getLinks(main_link, )

for link in all_links:
    unready_link = link
    s = main_link.split("/")
    for word in s:
        unready_link = unready_link.replace(word, "")
    unready_link = unready_link.lstrip("/")
    ready_link = main_link + unready_link
    all_ready_links.append(ready_link)

all_links.clear()

for link in all_ready_links:
    next_resp = req.get(link)
    next_html = BeautifulSoup(next_resp.content, 'html.parser')

    for el in next_html.select(
            'body > div.body > div.main > div > div > div > div.col-md-9.col-sm-9.col-xs-8.content-md > div.item-views.list.image_left.study > div.items.row'):
        title = el.select('div > div.col-md-8.col-sm-8.col-xs-12 > div > a')
        for anylink in title:
            all_links.append(anylink.get('href'))

all_ready_links.clear()

for link in all_links:
    unready_link = link
    s = main_link.split("/")
    for word in s:
        unready_link = unready_link.replace(word, "")
    unready_link = unready_link.lstrip("/")
    ready_link = main_link + unready_link
    all_ready_links.append(ready_link)

my_titles = []
my_contents = []
my_price = []
my_timelong = []

for link in all_ready_links:
    final_resp = req.get(link)
    final_html = BeautifulSoup(final_resp.content, 'html.parser')
    content_place = final_html.find('div', class_='content')
    content_row = content_place.find_all('div', class_='col-md-6')

    title_un = content_row[0]
    title_re = title_un.get_text('', strip=True)
    my_titles.append(title_re)

    tables_in_content = content_place.find_all('table')
    second_table = tables_in_content[0]
    content_ready = second_table.find_all_next(name='div', class_='page-content-text')

    price_content = content_ready[4].get_text('', strip=True)
    my_price.append(price_content)

    date_content = content_ready[1].get_text('', strip=True)
    my_timelong.append(date_content)
    string_content = ""

    for i in range(5, len(content_ready)):
        string_content += content_ready[i].get_text('', strip=True) + "\n"

    my_contents.append(string_content)



curses = xlwt.Workbook('utf8')
font = xlwt.easyxf('font: height 240,name Arial,colour_index black, bold off,\
    italic off; align: wrap on, vert top, horiz left;\
    pattern: pattern solid, fore_colour white;')

sheet = curses.add_sheet("Страница")

for i in range(len(my_titles)):

    sheet.write(i, 0, my_titles[i], font)
    sheet.write(i, 1, my_price[i], font)
    sheet.write(i, 2, my_timelong[i], font)
    sheet.write(i, 3, my_contents[i], font)

    sheet.row(i).height = 7500
    sheet.col(0).width = 2000
    sheet.col(1).width = 2000
    sheet.col(2).width = 2000
    sheet.col(3).width = 20000

curses.save('Курсы.xls')
