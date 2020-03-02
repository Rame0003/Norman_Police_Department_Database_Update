import pandas as pd
import numpy as np
import math
import PyPDF2
import datetime
import urllib
import subprocess
import tempfile
import sqlite3
from sqlite3 import Error
import re
from tika import parser
import sys
import argparse

def createdb():
    
    conn= sqlite3.connect('normandb.db')
    c=conn.cursor()
    #pd.read_sql('drop table normandb', conn)
    
    c.execute
    (
        '''CREATE TABLE normandb 
        (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
        );'''
    )
    
    conn.commit()
    

def fetchincidents(download_url):
    
    data=urllib.request.urlopen(download_url).read()
    tmp=tempfile.NamedTemporaryFile()
    tmp.write(data)
    tmp.seek(0)
    
    page_content=" "
    tmp.seek(0)
    temp=PyPDF2.pdf.PdfFileReader(tmp)
    
    num=temp.getNumPages()
    for i in range(0,num):
        page_content += temp.getPage(i).extractText()
    return page_content
    
    
def extractincidents(file):
    
    lst=(file)
    lst=lst.replace('\nNORMAN POLICE DEPARTMENT\nDaily Incident Summary (Public)\n',' ')
    pat2=re.compile(r'(?<=(\d{8})\b)\s')
    pat3=re.compile(r'(?<=[A-Z])\s(?=([A-Z][a-z]))')
    pat4=re.compile(r'(?<=[A-Z])\s(?=\bCOP\s..)')
    pat5=re.compile(r'(?<=[A-Z])\s(?=\bMVA\s..)')
    pat6=re.compile(r'(?<=\w)\s(?=\bOK|\bEMSSTAT|1400.$)')
    pat7=re.compile(r'(?<=COP)\s(?=([A-Z][a-z]))')
    pat8=re.compile(r'(?<=MVA)\s(?=([A-Z][a-z]))')
    patmiss=re.compile(r'(?<=[A-Z])\s(?=\bOK|\bEMSSTAT|1400.$)')
    patcom=re.compile(r'(?<=[A-Z]),\s(?=[A-Z])')
    lst=re.sub(' \n', ' ', (lst))
    lst1=re.sub(pat2,'\n', lst)
    lst2=re.sub(pat3,'\n', lst1)
    lst3=re.sub(pat4,'\n', lst2)
    lst4=re.sub(pat5, '\n', lst3)
    lst5=re.sub(pat6, '\n', lst4)
    lst6=re.sub(pat7, ' ', lst5)
    lst7=re.sub(pat8, ' ', lst6)
    lst8=re.sub(patcom,'/',lst7)
    lstfin=re.sub(patmiss, '\n \n', lst8)

    extra=" "
    rx = r"\s+(?=\d+/\d+/\d+\s)"
    extra = re.split(rx,lstfin)
    
    res = [] 
    for el in extra: 
        sub = el.split(', ') 
        res.append(sub)
    
    df=pd.DataFrame.from_records(res, nrows=len(res))
    
    df=df.drop(0)
    
    if (len(df.columns)==2):
        df.columns=['Data','None']
    elif(len(df.columns)==1):
        df.columns=['Data']
    
    data=df.Data.str.split("\n", expand=True)
    
    data=data.drop(len(data)-1)
    
    if ((len(data.columns))==5):
        data.columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori']
    elif((len(data.columns))>5):
        data=(data.iloc[:,:-1])
        data.columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori']
        
    return data
    

def populatedb(df):
    conn = sqlite3.connect('normandb')
    df.to_sql('normandb', conn, if_exists='replace', index=False)
    return df
    status()
    
def status():
    conn = sqlite3.connect('normandb')
    result=pd.read_sql('select nature,count(nature) from normandb group by nature order by nature', conn)
    print(result)  
