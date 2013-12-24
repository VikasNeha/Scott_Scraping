import csv

prods_urls = []
ifile = open("csv_files/product_links.csv", "rb")
csv_reader = csv.reader(ifile)
ofile = open("csv_files/product_links_remd.csv", "wb")
csv_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

for row in csv_reader:
    if row[1] not in prods_urls:
        prods_urls.append(row[1])
        csv_writer.writerow(row)

ifile.close()
ofile.close()

