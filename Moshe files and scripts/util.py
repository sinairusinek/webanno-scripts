#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this file contains helper functions for the module reconstruct.py
"""
#fitz to habdle file reading
import fitz
#json handling
import json
#pandas and numpy for data processing
import pandas as pd
import numpy as np


def read_file(path):
    """return and open file by fitz"""
    return fitz.open(path)

def get_blocks_info(file):
    """return block info"""
    blocks=[]

    for page in range(file.pageCount):
        page = file.getPageText(page, output="json")
        blocks_ = json.loads(page)["blocks"]

        blocks=np.concatenate([blocks,blocks_])

    return blocks

def get_cols(blocks,first_word,last_word):
    """return the columns"""
    cols=[]

    temp=[]

    text_first_word=''
    indx_a=0
    foundIt=False
    while indx_a< np.shape(blocks)[0] and not(foundIt):
        b=blocks[indx_a]
        for l in b['lines']:

            for ls in  l['spans']:

                text=ls['text']
                text_first_word=text.split(',')[0]
                foundIt=foundIt or (text_first_word == first_word)
        if not(foundIt):indx_a+=1


    text_last_word = ''
    indx_b=indx_a
    foundIt = False
    while indx_b < np.shape(blocks)[0] and not(foundIt):
        b = blocks[indx_b]
        temp.append(b)
        for l in b['lines']:

            for ls in l['spans']:

                text = ls['text']
                text_last_word = text.split(',')[0]
                foundIt = foundIt or (text_last_word == last_word)
        if not (foundIt): indx_b += 1

    cols.append(temp)
    return cols

def get_lines_text_cols(col):

    output=[]

    for b in col:

        for l in b['lines']:
            text=''
            for ls in l['spans']:
                text += ls['text']

            output.append(text)

    return (output)

def get_starting_bbox_cols(col):

    output=[]

    for b in col:

        for l in b['lines']:

            output.append(l['bbox'][0])

    return (output)

def get_starting_bbox_cols_y(col):

    output=[]

    for b in col:

        for l in b['lines']:

            output.append(l['bbox'][1])

    return (output)

def get_first_and_last_all_pages(blocks):

    output=[]

    starting_bboxs = (get_starting_bbox_cols(blocks))
    starting_bboxs_y = (get_starting_bbox_cols_y(blocks))

    lines_of_text = (get_lines_text_cols(blocks))

    u_1=45
    u_2=600
    u_3=100

    i=0
    while starting_bboxs_y[i]<u_1 or starting_bboxs_y[i]>u_2: i+=1

    first=lines_of_text[i].split(',')[0]
    cont=0
    size=len(starting_bboxs)
    while cont<size:
        j=cont
        s=starting_bboxs[j]
        if (s>u_1 and s<u_2 and starting_bboxs_y[j]>u_1 and starting_bboxs_y[j]<u_2) and ((lines_of_text[j].find('Index'))):


            cont+=1
        else:
            starting_bboxs=np.delete(starting_bboxs,cont)
            starting_bboxs_y = np.delete(starting_bboxs_y, cont)
            lines_of_text = np.delete(lines_of_text, cont)


        size=len(starting_bboxs)



    for j, s in enumerate(starting_bboxs[:-1]):

        if np.abs(s-starting_bboxs[j+1])>u_3:
            last = lines_of_text[j].split(',')[0]

            output.append([first, last])

            first=lines_of_text[j+1].split(',')[0]



    last = lines_of_text[-1].split(',')[0]

    output.append([first, last])


    return output
