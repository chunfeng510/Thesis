import csv
# csvfile = open('80001/output/1.csv', 'w', newline='')
# writer = csv.writer(csvfile)
# writer.writerow(['CUI', 'ROW', 'POSITION', 'NEGATION', 'SMT'])
# writer.writerow(['C0015472', 10, '14-20', 1, 'clnd'])

def score2csv(file_in, ):

    file_in = file_in
    file_out = file_in.replace('.txt', '.csv')
    f = open(file_in, 'r')
    csvfile = open(file_out, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['SCORE', 'CUI1', 'CUI2'])

    for i in f:
        res = i.replace('\n', '').split('<>', 2)
        writer.writerow([res[0], res[1], res[2]])
        print(res[0], res[1], res[2])
    csvfile.close()

# score2csv('score_test.txt')