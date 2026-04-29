# a guide for using BeautifulSoup to scrape HTML text and tables

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Reference links for BeautifulSoup documentation:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://beautiful-soup-4.readthedocs.io/en/latest/

######################################
# Scraping text elements
# 1. Set values for your request
# 2. Request the page
# 3. Convert to BeautifulSoup object
# 4. Figure out what you want to pull out of the HTML structure
# 5. Write code (often involving iteration) to extract the values you want
# 6. Convert/combine extracted values into a more convenient object (dict, DataFrame, etc.)

# 1. Set values
# set header values for your requests

# one that Wikipedia requires: User-Agent
# when in doubt, you can get your own from: https://www.browserscan.net/user-agent
my_headers = {"User-Agent" : "Mozilla/5.0"}

# set URL
page_url = "https://en.wikipedia.org/wiki/The_Beatles"

# 2. Request the page
beatles_page = requests.get(page_url,
                            headers = my_headers)

# 3. Convert page *content* to BeautifulSoup object 
beatles_soup = BeautifulSoup(beatles_page.content, "html.parser")
type(beatles_soup)
beatles_soup.contents

# 4. Use get and find functions (and possibly others) to 
#    locate the info you're interested in


# <TAG attrib='value'> </TAG>
# <h1>Title header text</h1> 
# <h2>Section header text</h2> 
# <p> = paragraph
# <table>
#  <th>
#  <tr>
#  <td>
# <div>

# Just dump all the text (without tags) into a string
all_page_text = beatles_soup.get_text()
type(all_page_text)
print(all_page_text)

# BeautifulSoup.find(), .find_all() 
# looks for tags
page_header = beatles_soup.find("h1")
type(page_header)
print(page_header.get_text())
page_header2s = beatles_soup.find_all("h2")
type(page_header2s)
len(page_header2s)
type(page_header2s[0])
print(page_header2s[0].get_text())

page_header2s[0]
for header in page_header2s:
    print(header.get_text())

page_ps = beatles_soup.find_all("p")
page_ps[1]

beatles_history_h2 = page_header2s[1]
beatles_history_h2
ps_after_history = beatles_history_h2.find_all_next("p")
ps_after_history[0]

beatles_artistry_h2 = page_header2s[2]
ps_before_artistry = beatles_artistry_h2.find_all_previous("p")
ps_before_artistry[0] # previous means first thing going backward

ps_between = [paragraph for paragraph in ps_after_history if paragraph in ps_before_artistry]

ps_between[0]
ps_between[-1]


####################################################
# Scraping tables
# 1. Set values for your request
# 2. Request the page
# 3. Convert to BeautifulSoup object
# 4. Find the table you want
# 5. Figure out if you should pull table headers as <th> tags
# 6. Loop through <tr> tags to loop through rows
# 7. Loop through <td> tags to loop through cells in a row
# 8. Convert to DataFrame or other convenient object
# Also: add more inside the loops to pull out any other specific tag values
#       other than just text. For example, href from <a> tags to get links.

# 1. Set values
my_headers = {"User-Agent" : "Mozilla/5.0"}
deaths_url = "https://en.wikipedia.org/wiki/List_of_2026_deaths_in_popular_music"

# 2. Make request
deaths_page = requests.get(deaths_url, headers = my_headers)

# 3. Convert
deaths_soup = BeautifulSoup(deaths_page.content, "html.parser")

# 4. Find the table
deaths_tables = deaths_soup.find_all("table")
len(deaths_tables)

death_info_table = deaths_tables[1]

# 5. Figure out if you should pull table headers as <th> tags
header_cells = death_info_table.find_all("th")
print(header_cells)
death_info_columns = [cell.get_text().strip() for cell in header_cells]
death_info_columns # does this look right?

# 6. Loop through <tr> tags to loop through rows
death_table_rows = death_info_table.find_all("tr")

death_info_records = [] # a list of lists
for row in death_table_rows:
    cells = row.find_all("td") # get all of the cells
    if len(cells) == 0: # skips the header row that has no <td> tags
        continue

    # 7. Loop through <td> tags to loop through cells in a row
    cell_list = [] # this is a list that represents a "row" of data values
    for cell in cells:
        cell_list.append(cell.get_text().strip())
    death_info_records.append(cell_list) # add to the list of lists

print(death_info_records[:3])

# 8. Convert to DataFrame or other convenient object
# NOTE: the "list of lists" format works when you pass a list of column names
deaths_df = pd.DataFrame(death_info_records, columns = death_info_columns)
deaths_df


# Going further: getting links out of cells

# check example values for more complex stuff
death_table_rows[1].contents
death_table_rows[1].find("td").find("a")
bool(death_table_rows[1].find("td").find("a")) # when there's a link in the first cell
bool(death_table_rows[14].find("td").find("a")) # when there's NOT a link in the first cell

artist_urls = [] # to hold the results, one per row
base_url = "https://en.wikipedia.org/" # to paste onto the href values
# still looping over rows, then cells
for row in death_table_rows:
    cells = row.find_all("td")
    if len(cells) == 0:
        continue

    # don't need to loop through every cell,
    # just get the first cell on each row
    name_cell = cells[0]
    # instead of getting the text:
    # grab the URL if there is one from the name cell
    if artist_url := name_cell.find("a"): # "walrus operator" trick
        artist_urls.append(base_url + artist_url["href"])
    else:
        artist_urls.append("no link found")

len(artist_urls)
print(artist_urls)

deaths_df["link to artist Wikipedia page"] = artist_urls

