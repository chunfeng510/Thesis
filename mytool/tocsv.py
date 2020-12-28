import csv
csvfile = open('80001/output/1.csv', 'w', newline='')
writer = csv.writer(csvfile)
writer.writerow(['CUI', 'ROW', 'POSITION', 'NEGATION', 'SMT'])
writer.writerow(['C0015472', 10, '14-20', 1, 'clnd'])