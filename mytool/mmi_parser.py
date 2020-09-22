import re


def parser(output_msg):
    str = output_msg.split(',',)


def trigger_parser(input):
    input = input.replace('[', '').replace(']', '')
    info = list(input.split('-'))
    '''
    info[0] = UMLS concept
    info[1] = loc
    info[2] = locPos
    info[3] = text
    info[4] = Part os Speech
    info[5] = Negation flag
    '''
    return info
