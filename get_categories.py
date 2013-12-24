from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv


BASE_URL = "http://www.avenuesupply.ca/en-ca"


def make_soup(url):
    html = urlopen(url).read()
    #return BeautifulSoup(html, "lxml")
    return BeautifulSoup(html, "html.parser")


soup = make_soup(BASE_URL)
categories_section = soup.find("ul", class_="categories")
categories_sections = categories_section.find_all("a", class_="categoryTextLink")


ofile = open("csv_files/categories.csv", "wb")
csv_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
for curr_item in categories_sections:
    csv_writer.writerow(["http://www.avenuesupply.ca"+curr_item["href"], curr_item.text.strip()])
ofile.close()