'''
把功能變成模組工具 塞入 mytool 之前
的測試區域

'''

import re
sen_before = list()
sen_tmp = list()
sen_after = list()

file = 'clinical_txt/1.txt'
out_file = 'ex1_o.txt'


sen1 = "cycle 2 on 2017.07.14 to 2017.07.1 cycle 3 on 2017.08.11 to 2017.08.13 ;"


def read_file(txt_file):
    f = open(txt_file)
    lines = f.readlines()
    # print(type(lines))
    for line in lines:
        sen_before.append(line)
    f.close()
    # sen_after= [re.sub(pattern, '/', line) for line in sen_before]
    sen_after = [re.sub(r'(\d{4}) . (\d{2}) . (\d{2}) .', r'\1/\2/\3', line) for line in sen_before]

    sen_after = [re.sub(r'(\d{4}).(\d{2}).(\d{2})', r'\1/\2/\3', line) for line in sen_after]

    sen_after = [re.sub(r'(\d{4}).(\d{2}).(\d{1})', r'\1/\2/\3', line) for line in sen_after]

    sen_after = [re.sub(r'(\d{4}) . (\d{2})', r'\1/\2', line) for line in sen_after]
    
    sen_after = [re.sub(r'(\d{4}).(\d{2})', r'\1/\2', line) for line in sen_after]

    sen_after = [re.sub (r'★|■|#', '', line) for line in sen_after]
    
    return sen_after

sen_after = read_file(file)
print("sen_after : ",sen_after)

print('\n')
print(sen_before)

def save_file():
    f = open(out_file,'w')
    f.writelines(sen_before)
    f.close()

# save_file()