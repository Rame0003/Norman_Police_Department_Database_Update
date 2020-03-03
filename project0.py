#Import all required packages:
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

#Function to create the database:
def createdb():
    
    #Initialize the connection to the SQLite database. 
    conn= sqlite3.connect('normandb.db')
    c=conn.cursor()
    #Creating the table norman DB
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
    #Signalling that the process has committed
    conn.commit()
    
#Function to fetch the pdf from the URL and extract all the text data from the downloaded pdf:
def fetchincidents(download_url):
    
    #Download data into file
    data=urllib.request.urlopen(download_url).read()
    
    #Creating temporary file named tmp
    tmp=tempfile.NamedTemporaryFile()
    
    #Write data from url object into temporary file
    tmp.write(data)
    
    #Set cursor to the beginning
    tmp.seek(0)
    
    #Create list to store the extracted text from pdf file
    page_content=" "
    
    #Set cursor to the beginning
    tmp.seek(0)
    #Read given PDF file into temporary file to be processed
    temp=PyPDF2.pdf.PdfFileReader(tmp)
    #Get the number of pages of the PDF file
    num=temp.getNumPages()
    for i in range(0,num):
        page_content += temp.getPage(i).extractText()
        
    #Return the string of text into the next function. 
    #The next function will work to split and accomodate the text in the correct places
    return page_content
    
    
def extractincidents(file):
    
    #Download the string into a variable lst
    lst=(file)
    
    #Find and replace the given text
    lst=lst.replace('\nNORMAN POLICE DEPARTMENT\nDaily Incident Summary (Public)\n',' ')
    
    #I had analyzed the patterns by which the file was divided and hence my approach uses regex quite extensively. 
    #Storing the required patterns in between which the necessary charecter will be replaced. 
    pat2=re.compile(r'(?<=(\d{8})\b)\s')
    pat3=re.compile(r'(?<=[A-Z])\s(?=([A-Z][a-z]))')
    pat4=re.compile(r'(?<=[A-Z])\s(?=\bCOP\s..)')
    pat5=re.compile(r'(?<=[A-Z])\s(?=\bMVA\s..)')
    pat6=re.compile(r'(?<=\w)\s(?=\bOK|\bEMSSTAT|1400.$)')
    pat7=re.compile(r'(?<=COP)\s(?=([A-Z][a-z]))')
    pat8=re.compile(r'(?<=MVA)\s(?=([A-Z][a-z]))')
    patmiss=re.compile(r'(?<=[A-Z])\s(?=\bOK|\bEMSSTAT|1400.$)')
    patcom=re.compile(r'(?<=[A-Z]),\s(?=[A-Z])')
    
    #Manipulating the string using regex:
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
    
    #Splitting the string into list according to date:
    #Fact: Regex does not like lists. It likes only strings for processing
    extra=" "
    rx = r"\s+(?=\d+/\d+/\d+\s)"
    extra = re.split(rx,lstfin)
    
    #Creating list of lists to be added into dataframe:
    res = [] 
    for el in extra: 
        sub = el.split(', ') 
        res.append(sub)
    
    #Adding records into dataframes:
    df=pd.DataFrame.from_records(res, nrows=len(res))
    
    #Dropping the first row as it contains only the column names from the PDF:
    df=df.drop(0)
    
    #Sometimes, a special charecter between the addresses can create an entirely separate line 
    #This causes an address to be pushed into another column creating a separate column altogether.
    #We remove this column to allow easier processing. After several attempts to fix this issue, I see that it appears in 
    #one of 300 records. Thus, I considered this decision.
    if (len(df.columns)==2):
        df.columns=['Data','None']
    elif(len(df.columns)==1):
        df.columns=['Data']
    
    #Seaprating the data according to the custom charecter, in our case it is a new line. 
    data=df.Data.str.split("\n", expand=True)
    
    #Drop the last row as it reads the timestamp that the file was compiled along with the date.
    data=data.drop(len(data)-1)
    
    #We know that the result needs to display the nature of the incident. Sometimes, the nature can push the incident_ori
    #into the fifth column, thus causing issues while pushing the n dataframe into the database. We correct that
    #using the following loop:
    if ((len(data.columns))==5):
        data.columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori']
    elif((len(data.columns))>5):
        data=(data.iloc[:,:-1])
        data.columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori']
     
    #Return the data to be sent into the database.
    return data
    
#Populate the database with the given dataframe
def populatedb(df):
    conn = sqlite3.connect('normandb')
    df.to_sql('normandb', conn, if_exists='replace', index=False)
    return df
    
    #Calling the status() function to execute the sql query delivering the result
    status()
    
#Function to display the required result
def status():
    conn = sqlite3.connect('normandb')
    result=pd.read_sql('select nature,count(nature) from normandb group by nature order by nature', conn)
    print(result)  
