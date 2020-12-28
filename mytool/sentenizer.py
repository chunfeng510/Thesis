'''
將原始病例(raw clinical note data) 做優化
如：
1. 去除標點符號
2. 日期標示法替換
3. 拼字檢查
4. 加入前置 ID

'''

import re
sen_before = list()
sen_after = list()

# file = 'clinical_txt/1.txt'
# out_file = 'ex1_o.txt'

# sen1 = "cycle 2 on 2017.07.14 to 2017.07.1 cycle 3 on 2017.08.11 to 2017.08.13 ;"

def file_process(patient_id, total_days):
    for cnt in range(1, total_days+1):
        sen_before = list()
        sen_after = list()
        file_in = 'Clinical Note/'+str(patient_id)+'/'+str(cnt)+'.txt'
        file_out = 'Clinical Note/'+str(patient_id)+'/output/'+str(cnt)+'_o.txt'
        try:
            f = open(file_in)
        except FileNotFoundError:
            print("File not found! \nPlease make sure the path is correct and file indeed exist.")
            break
        lines = f.readlines()
        print("Input file : ", file_in)
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

        sen_after = [re.sub(r'★|■|#|@|\*|-|>|<', '', line) for line in sen_after]
        
        sen_after = [re.sub(r'\\|\[|\]|\+|\$|%|\(|\)|\^|\!|＼|／|○|↓|\||▽|:|—|！|，|。|？|、|~|￥|…|（|）|＜|＞|&|╴|│', ' ', line) for line in sen_after]

        while '\n' in sen_after:
            sen_after.remove('\n')
        while ' \n' in sen_after:
            sen_after.remove(' \n')

        counter = len(sen_after)
        for i in range(1,counter+1):
            if i<10:
                sen_after[i-1]="SID00"+ str(i)+"|"+ sen_after[i-1]
            elif i<100:
                sen_after[i-1]="SID0"+ str(i)+"|"+ sen_after[i-1]
            else :
                sen_after[i-1]="SID"+ str(i)+"|"+ sen_after[i-1]


        f = open(file_out,'w')
        f.writelines(sen_after)
        f.close()
        print("Output file : ", file_out)
        print("Processing completed !")

def single_txt_process(file_in, file_out):
    
    f = open(file_in)
    lines = f.readlines()
    print("Input file : ", file_in)
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

    sen_after = [re.sub(r'★|■|#|@|\*|-|>|<', '', line) for line in sen_after]

    sen_after = [re.sub(r'\\|\[|\]|\+|\$|%|\(|\)|\^|\!|＼|／|○|↓|\||▽|:|—|！|，|。|？|、|~|￥|…|（|）|＜|＞|&|╴|│', '', line) for line in sen_after]
    # sen_after = [re.sub('[-\s+\.\!\/_,$%^*()+\"\']+|[+——！○↓，■★。？、~@#￥%……&*（）:＞╴／▽＼╴＜│]+', ' ', line) for line in sen_after]
    
    while '\n' in sen_after:
        sen_after.remove('\n')
    while ' \n' in sen_after:
        sen_after.remove(' \n')

    counter = len(sen_after)
    for i in range(1,counter+1):
        if i<10:
            sen_after[i-1]="SID00"+ str(i)+"|"+ sen_after[i-1]
        elif i<100:
            sen_after[i-1]="SID0"+ str(i)+"|"+ sen_after[i-1]
        else :
            sen_after[i-1]="SID"+ str(i)+"|"+ sen_after[i-1]


    f = open(file_out,'w')
    f.writelines(sen_after)
    f.close()
    print("Output file : ", file_out)
    print("Processing completed !")