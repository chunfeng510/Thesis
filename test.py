from mytool import cui 
from mytool import perl_script
import subprocess

# cui_list = cui.extract("clinical_txt/2_modified.txt" , output=False)
cui_list_day_1 = cui.extract_sldi("clinical_txt/1_modified.txt", output=False)
cui_list_day_2 = cui.extract_sldi("clinical_txt/2_modified.txt", output=False)
# cui_list_day_3 = cui.extract_sldi("clinical_txt/3_modified.txt", output=False)
# cui_list_day_4 = cui.extract_sldi("clinical_txt/4_modified.txt", output=False)
# cui_list_day_5 = cui.extract_sldi("clinical_txt/5_modified.txt", output=False)

i_ctr = 1
j_ctr = 1
for i in cui_list_day_1 :
    for j in cui_list_day_2 :
        perl_script.generator(i, j)
        Command = "run.pl"
        perl_process = subprocess.Popen(["perl", Command], stdout = subprocess.PIPE)
        for line in iter(perl_process.stdout.readline, b''):
            print(line.rstrip())