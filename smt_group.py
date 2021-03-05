import csv

def smt_grouping(cui_all_unique_path, patient_id):
    smt_category = ["clnd", "dsyn", "acab", "anab", "fndg", "inpo", "mobd", "neop"
                    , "patf", "sosy", "aapp", "antb", "bacs", "chem", "enzy", "hops"
                    , "horm", "imft", "inch", "lbpr", "medd", "nnon", "orch", "phsu"
                    ,"topp", "vita"]

    csv_all_cui_unique =  open(cui_all_unique_path, newline='')
    rows = csv.DictReader(csv_all_cui_unique)
    for row in rows:
        for smt in smt_category:
            if row['SMT'] == smt:
                f = open("Clinical_Note/"+str(patient_id)+'/smt_grouping/'+smt+'.txt', 'a')
                f.write(row['CUI']+'\n')
    




smt_grouping("Clinical_Note/80001/80001_all_12_cui_unique.csv", 80001)