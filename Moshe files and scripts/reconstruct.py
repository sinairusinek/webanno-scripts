#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains three functions:
    handlePdf(pdf_input): takes pdf file, and parses it into a list of the lines
    first_ind(lines): finds the first line where an index appears and returns its
        nimber, it assumes alphabetical order
    processLines(lines): takes the lines as input and does some reformatting
"""
from util import (read_file,get_blocks_info,get_cols,get_lines_text_cols,
get_starting_bbox_cols,get_starting_bbox_cols_y,get_first_and_last_all_pages)
import numpy as np
import pandas as pd
import fitz
import re
#############################################################

#############################################################
def handlePdf(pdf_input):
    """take pdf, read and store it in a list, then return the list"""
    input_file= pdf_input
    #read the pdf
    file= read_file(input_file)

    blocks_info=get_blocks_info(file)

    first=[]
    second=[]
    pages=[]
    lines = []
    for (first_word,last_word) in get_first_and_last_all_pages(blocks_info):

        cols=get_cols(blocks_info,first_word,last_word)

        lines_of_text= (get_lines_text_cols(cols[0]))
        starting_bboxs= (get_starting_bbox_cols(cols[0]))

        for j,starting_point in enumerate(starting_bboxs):
            lines.append(lines_of_text[j])
    return lines
#############################################################

#############################################################
def first_ind(lines):
    """find the first line of a genuine index and return it"""
    regex = re.compile(r"^[aA]+.*\d+.*")
    for line in lines:
        if re.search(regex,line)!=None:
            return lines.index(line)
#############################################################

#############################################################
def processLines(lines):
    """resegment the lines and make the lines that start with a digit appended
    to the previews line, and return a full list to the caller"""
    i=first_ind(lines)
    new_lines = []
    digit = re.compile(r"^\d.*")
    empty = re.compile(r"^\n")
    ischar = re.compile(r"^[\w‘].*")
    newline = ""
    while i < len(lines):
        if re.search(empty,lines[i])==None:
            if (re.search(digit,lines[i])==None) and (re.search(ischar,lines[i])!=None):
                new_lines.append(newline)
                newline = lines[i]
            else:
                if (i == len(lines)-1):
                    newline += lines[i]
                    new_lines.append(newline)
                else:
                    newline += lines[i]
            i += 1
        else:
            i += 1
    return new_lines
#############################################################

#############################################################
