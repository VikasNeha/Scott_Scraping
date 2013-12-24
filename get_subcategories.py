from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv


BASE_URL = "http://www.avenuesupply.ca"


def make_soup(url):
    html = urlopen(url).read()
    #return BeautifulSoup(html, "lxml")
    return BeautifulSoup(html, "html.parser")


ifile = open("csv_files/categories.csv", "rb")
csv_reader = csv.reader(ifile)

ofile = open("csv_files/sub_categories.csv", "wb")
csv_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

for row in csv_reader:
    soup = make_soup(row[0])
    h2s = soup.find_all("h2", class_="title")
    for h2 in h2s:
        csv_writer.writerow([row[1], h2.a["title"], BASE_URL+h2.a["href"]])

ifile.close()
ofile.close()