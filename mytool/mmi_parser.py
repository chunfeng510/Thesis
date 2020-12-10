'''
解析 mmi(metamap index) 回傳的內容
有以下，詳見程式碼區塊
'''

import re


def parser(output_msg):
    str = output_msg.split(',',)


def trigger_parser(input_phrase):
    input_phrase = input_phrase.replace('[', '').replace(']', '').replace(',', '-')
    info = list(input_phrase.split('-'))
    '''
    info[0] = UMLS concept
    info[1] = loc
    info[2] = locPos
    info[3] = text
    info[4] = Part os Speech
    info[5] = Negation flag
    '''
    for n in range(5, 11):
        if info[n] == '1' or info[n] == '0':
            return(info[n])
            break
 
