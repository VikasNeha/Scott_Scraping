from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv
import re
from urllib import urlretrieve

BASE_URL = "http://www.avenuesupply.ca/en-ca"


def getValueFromScript(script, key, *variation):
    if variation:
        if variation[0] == "price":
            value = script[script.index(key):]
            value = value[:value.index(",")]
            value = value[value.index('[') + 1:value.rindex(']')]
            return str(value)
    value = script[script.index(key):]
    value = value[:value.index(",")]
    value = value[value.index('"') + 1:value.rindex('"')]
    return value


def getDescription(script):
    try:
        value = script[script.index("Specifications"):script.index('|"')]
        value = value[value.index(":")+2:]
        return value
    except ValueError:
        return ""


def getShortDescription(script):
    value = script[script.index("Description"):]
    value = value[value.index(":")+2:value.index('","')]
    return value

def getOptions(script):
    value = script[script.index("OptionId"):]
    value = value[value.index(":")+2:value.index('",')]
    if len(value) > 0:
        value = script[script.index("OptionLabel"):]
        value = value[value.index(":")+2:value.index('",')]
        strToReturn = value + ":"
        scriptLeft = script
        first = True
        while True:

            isValueLeft = scriptLeft.find("OptionValue")
            if isValueLeft == -1:
                break
            else:
                value = scriptLeft[scriptLeft.index("OptionValue"):]
                scriptLeft = scriptLeft[scriptLeft.index("OptionValue"):]
                lastIndex = value.index('",')
                value = value[value.index(":")+2:lastIndex]
                if first:
                    strToReturn += value
                    first = False
                else:
                    strToReturn += ","+value
                scriptLeft = scriptLeft[lastIndex:]
        return strToReturn
    else:
        return ""

def isBulkDiscount(script):
    value = script[script.index("ShowBulkDiscount"):]
    value = value[value.index(":")+1:value.index(',')]
    if value == 'true':
        return True
    else:
        return False

def getImageURL(script):
    value = script[script.index("S7MainProductImageEnlarge"):]
    value = value[value.index(":")+2:value.index('","')]
    return value

def make_soup(url):
    html = urlopen(url).read()
    #return BeautifulSoup(html, "lxml")
    return BeautifulSoup(html, "html.parser")

ifile = open("csv_files/product_links_remd_10.csv", "rb")
csv_reader = csv.reader(ifile)

ofile = open("csv_files/products_scrapped_10.csv", "wb")
csv_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

#csv_writer.writerow(["Category", "SKU", "Name", "Image", "Small Image", "Thumbnail",
#                     "Price", "Special Price", "Description", "Short Description", "Options", "Discount", "URL"])

for row in csv_reader:
    soup = make_soup(row[2])

    script = soup.find("script", text=re.compile("utag_data"))

    category = getValueFromScript(script.text, "page_category_name") + "," + getValueFromScript(script.text, "page_subcategory_name")
    category = category.encode('ascii', 'ignore')

    sku = getValueFromScript(script.text, "product_sku")
    sku = sku.encode('ascii', 'ignore')
    prod_name = getValueFromScript(script.text, "product_name")
    prod_name = prod_name.encode('ascii', 'ignore')
    price = getValueFromScript(script.text, "product_unit_price", "price")
    price = price.encode('ascii', 'ignore')

    script_desc = soup.find("script", text=re.compile("jsonProduct"))
    description = getDescription(script_desc.text)
    description = description.encode('ascii', 'ignore')
    short_description = getShortDescription(script_desc.text)
    short_description = short_description.encode('ascii', 'ignore')
    options = getOptions(script_desc.text)
    options = options.encode('ascii', 'ignore')
    isBulk = isBulkDiscount(script_desc.text)
    imageURL = getImageURL(script_desc.text)
    imageStorePath = "Images/" + str(sku) + ".jpg"
    urlretrieve(imageURL, imageStorePath)
    imagePath = "/" + sku + ".jpg"

    csv_writer.writerow([category, sku, prod_name, imagePath, imagePath, imagePath,
                         price, "", description, short_description, options, isBulk, row[2]])
    print row[0]

ifile.close()
ofile.close()