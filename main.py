#Importing packages for smooth processing:
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
import main



def main(url):
    
    # Download data
    file=project0.fetchincidents(url)
    
    # Extract Data
    incidents = project0.extractincidents(file)
	
    # Create Dataase
    db = project0.createdb()
	
    # Insert Data
    project0.populatedb(incidents)
	
    # Print Status
    project0.status()


if __name__ == '__main__':
#Initialize parser to parse URL into main function:
    parser = argparse.ArgumentParser()
#Specifying start of string which should be parsed into the .py function
    parser.add_argument("--incidents", type=str, required=True, 
                         help="The arrest summary url.")
#Check to see if url contains the fields necessary for the program:
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)


