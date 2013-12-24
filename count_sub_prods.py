import csv


# subcat_prods = dict()

ifile = open("csv_files/product_links_remd.csv", "rb")
csv_reader = csv.reader(ifile)

# for row in csv_reader:
#     if row[0] in subcat_prods:
#         subcat_prods[row[0]] += 1
#     else:
#         subcat_prods[row[0]] = 1

ofile = open("csv_files/product_links_remd_backup.csv", "wb")
csv_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

i = 1
for row in csv_reader:
    csv_writer.writerow([str(i), row[0], row[1]])
    i += 1

ifile.close()
ofile.close()