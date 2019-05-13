#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this is the initial version of a program to extract subject indexes from Documents
into a database for further processing,
this version is however primative, it supports only hardcoded conversion
that relies on simple regexes and modules.
"""
#db handling
import sqlite3
from sqlite3 import Error
#handle strings
import io
from io import BytesIO as StringIO
#handle pdf mining
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
#handle files and directories
import os
import shutil
#regex
import re
#reconstruction
from reconstruct import handlePdf,processLines
from docx2pdf import convert_to

#############################################################
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None
#############################################################

#############################################################
def create_table(conn, table_name):
    """ create a table with the create_table name
    the table is created for each file
    it stores the results of the search
    """
    sql_create_table = """ CREATE TABLE IF NOT EXISTS {} (
                                        key text,
                                        subjectIndex text
                                    ); """.format(table_name)
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)
#############################################################

#############################################################
def insert_row(conn,table, rownum, data):
    """insert the data into the table"""
    cur = conn.cursor()
    sql= "INSERT INTO {} (key,subjectIndex) VALUES (?,?)".format(table)
    cur.execute(sql,(rownum,data.decode('utf-8')))
    conn.commit()
#############################################################

#############################################################
def tableName(file_name):
    """substitute the invalid characters
    in the file name to make a valid sqlite3 table name"""
    return file_name.split(".")[0].replace(",","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_")
#############################################################

#############################################################
def exclude(text):
    """return text after excluding the unwanted parts
    please add new text to the ones in the list"""

    unwanted = [""""""]
#############################################################

#############################################################
def pdf_to_text(pdfname):
    """handle ptimative pdf convertion to text """
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()
    # Get text from StringIO
    text = sio.getvalue()
    device.close()
    sio.close()

    return text
#############################################################

#############################################################
def convertMultiple(pdfDir, txtDir):
    """convert multiple files in a directory from pdf to text"""
    #iterate through pdfs in pdf directory
    for pdf in os.listdir(pdfDir):
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf
            text = pdf_to_text(pdfFilename) #get string of text content of pdf
            textFilename = txtDir + pdf.split(".")[0] + ".txt"
            textFile = open(textFilename, "w") #make text file
            textFile.write(text) #write text to text file
#############################################################

#############################################################
def rec_multiple(pdfDir,recPdf):
    for pdf in os.listdir(pdfDir):
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            handlePdf(pdfDir+pdf,recPdf+pdf)
#############################################################

#############################################################
def make_pdf(recPdf):
    print "dir: ",recPdf,'\n'
    for doc in os.listdir(recPdf):
        fileExtension = doc.split(".")[-1]
        if fileExtension == "docx":
            print "converting: ",doc,'\n'
            convert_to(recPdf,recPdf+doc)
#############################################################

#############################################################
def main():

    #extract the cwd
    cwd = os.getcwd()
    access_rights = 0o755
    file = '/home/adminjesus/Documents/github_repos/work/pdfs/AlvarEzquerraJa_2008_GeneralIndex_RomanisingOrientalGod.pdf'
    lines = handlePdf(file)
    lines = processLines(lines)
    for linei in lines:
        print linei

    exit(1)
    #name of directory to store the text files after convertion
    path= "/texts/"

    # try:
    #     #if the text dir exists already, delete it, then create a new one
    #     if os.path.exists(cwd+path):
    #         shutil.rmtree(cwd+path)
    #         os.mkdir(cwd+path, access_rights)
    #     else:
    #         os.mkdir(cwd+path, access_rights)
    # except OSError:
    #     print ("Creation of the directory %s failed" % path)
    # else:
    #     print ("Successfully created the directory %s" % path)

    #define the directory for the pdf files and for the text creation
    pdfDir = "../pdfs/"
    txtDir = cwd+ "/texts/"
    recPdf = cwd+ "/data/"
    #reconstruct all pdfs in the directory
    #rec_multiple(pdfDir,recPdf)
    #build clean pdfs from the reconstructed
    #make_pdf(recPdf)
    #cnvert the pdfs
    pdfDir = recPdf
    # convertMultiple(pdfDir, txtDir)

    #compile the regex
    pattern = re.compile(r"^\b[A-Za-z]{1}[A-Z-]*")
    pattern2 = re.compile(r"[0-9]+")

    for text_file in os.listdir(txtDir):
        #connect to the database
        connection = create_connection("subject_index.db")
        errors = []
        linenum = 0
        fileExtension = text_file.split(".")[-1]
        if fileExtension == "txt":
            print "handling: ", text_file, "\n"
            with open(txtDir+text_file, 'rt') as currentFile:
                new_reg= re.compile(r"(\b[^\d.]{2,} [\d\W\nnf]{1,}[^,]*\n)",re.M|re.I)
                res = new_reg.findall(currentFile.read())
                # for line in currentFile:
                #     if pattern.search(line) != None:  # If pattern search finds a match,
                #         linenum += 1
                #         errors.append((linenum, line.rstrip('\n')))
                #     else:
                #         try:
                #             last = errors[-1][1]
                #             errors.pop()
                #             errors.append((linenum, last+ line.rstrip('\n')))
                #         except:
                #             print (line)
                #             continue

            table_name = tableName(text_file)
            print "table: ", table_name, "\n"
            create_table(connection, table_name)
            # for err in errors:
            #     list = err[1]
            for item in res:
                linenum += 1
                insert_row(connection,table_name, linenum, item.strip('\n'))

                # if len(err[1])>1 and pattern2.search(list) != None:
                #     insert_row(connection,table_name, err[0], list)
        connection.close()
#############################################################

if __name__ == "__main__":
    main()
