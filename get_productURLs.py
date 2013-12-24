from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import Select
import time
import csv

ffProfile = FirefoxProfile()
ffProfile.set_preference('permissions.default.image', 2)
driver = webdriver.Firefox(ffProfile)
driver.implicitly_wait(5)


ifile = open("csv_files\sub_categories.csv", "rb")
csv_reader = csv.reader(ifile)

ofile = open("csv_files/product_links.csv", "wb")
csv_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

total = 0
i = 1
for row in csv_reader:
    #driver.get("http://www.avenuesupply.ca/en-ca/category/material-handling-casters-and-wheels-297393.aspx")
    driver.get(row[2])
    time.sleep(5)
    selectPage = Select(driver.find_element_by_name("resultsPerPage"))
    selectPage.select_by_visible_text("64")
    time.sleep(5)

    subtotal = 0
    while True:
        products = driver.find_elements_by_class_name("productDetailsContainer")
        subtotal += len(products)
        total += len(products)
        for product in products:
            product_link = product.find_element_by_tag_name("a")
            csv_writer.writerow([row[1], product_link.get_attribute("href")])

        nextbutton = driver.find_elements_by_class_name("nextOn")
        if len(nextbutton) > 0:
            nextbutton[0].find_element_by_tag_name("a").click()
            time.sleep(5)
        else:
            break
    print str(i) + " : " + row[1] + " : " + str(subtotal)
    i += 1
print total

ifile.close()
ofile.close()