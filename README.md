# cs5293p20-project0
## Norman Police Department Database Update
### Introduction:
This project aims to update the incidents and order them alphabetically. The program contains of 5 different steps to process the data from the PDF and pushing into the SQLite database that has been created. The final required result is to make sure that the nature of incidents is displayed along with the count. 

We will be going through the steps taken to analyse the data, the assumptions made and other important details.

### Assumptions:
Each of the column follows the following pattern:
  * The timestamp is given as `mm/dd/yyyy hh:mm` 
  * The incident number is given in the form of `4x8` numbers seaprated by a (-) 
  * The addresses always are given in caps
  * The nature of incident is a normal word which has a capital letter in the beginning and the rest is small `(Eg: Norman)` 
  * The Incident_ori column contains any of these 4 cases: `OK0140200, EMSSTAT, 14005` or `14009`
  * The files have no missing nature. All of the cases are assigned to some case
  * The url is only given for incidents summary
  * The url is obtained from Norman PD website

### Code:
 This exercise was undertaken to give us a feel for text analytics. Though this can not be considered real text analysis, we can say that this exercise has made us understand what we can expect in upcoming projects and activities. Many people chose to write their code using indices as benchmarks. I chose to take a different approach and, with the above assumptions, chose to split up the text using regex. 
 The code is categorized into 5 sections, each of them performing a particular task to achieve the end goal:
 1. fetchincidents(url)
 2. extractincidents(file)
 3. createdb()
 4. populatedb(file)
 5. status()

#### Fetchincidents(url):
 This function is used to obtain the pdf from the given url. The function uses the urllib package to obtain the pdf file from the website. The obtained file is stored as a `urllib` file. This file is then written into a temporary file created inside the function. 
 The temporary file is used to store the pdf file obtained from the url. We then proceed to extract the text from the page. We use the `PyPDF2` package to perform this operation. We record the number of pages in the PDF and we initialize a string to store all the text. The reason for initializing the string is due to the fact that regex prefers string inputs. We loop the string to record the information from all the pages. The string thus obtained contains all the entries separated by '\n'. The string file is passed onto the next function.
 
#### Extractincidents(file):
 This function is used to process the text string obtained from the pdf and input the data into the dataframe. The text is processed by removing, editing and replacing the `\n` charecter in different places. We identify the different patterns according to the given assumptions and replace the spaces with the `\n` charecter to represent a new column. We then proceed to split the string into a list with the `re.split()` command where we specify to split along the dates, which makes it such that each row begins with a timestamp. 
 Once the list is created, the list is converted into a list of lists which is then fed into an initial dataframe. The individual columns are then split using the `str.split()` command. Once the columns are split, they are given the headings and the extraction of data is complete. The dataframe is returned and is sent into the `populatedb()` function.
 
#### Createdb():
 This function is run inside the main program to create the SQLite database in the running system. Once created, we can use it to store all the data and obtain the output. The columns of the table are given to us. We create the database and the table in this function. 

#### Populatedb(df):
 This function is used to populate the database with the details from the dataframe. The function is used to connect to the database, initialize the dataframe to be uploaded and loads it into the SQLite table. Using this function, we fill the database with the required information. We will run the `status()` function to display our results. 
 
 #### Status():
  This function is used to retrieve the number of incidents and the nature of incident separated by the `|` charecter. This function is invoked once the database is populated. 
 
 #### Issues faced:
1. Due to a few regex cases, some of the nature values *esp. EMS Mutual Aid* might get misplaced. This is represented by EMS in the nature column. 
2. When an address is separated by a ` ,` the text that follows it is pushed to a new line. From what I noticed, this has occured only once. 
3. Some of the addresses are given in coordinates. These coordinates are separated by a `;~`. Such coordinates are also collected as a part of the address. Only a few coordinates which use the `~` to be separated cause the data to be misplaced. This occured only once when the code was run. 
4. Missing values were encountered. Sometimes, the nature was not given at all. An issue with the PDF reader is that it does not read any white spaces, thus pulling the text from the next column into the respective column. This was countered by giving the `\n\n` charecter if something was amiss between the addresses and Incident_ori. 

### Execution:
 To run the program, use the pipenv command given below:
 >pipenv run python project0/main.py --incidents <copied url>
 This should provide you with the result. 

# References:
* https://stackoverflow.com/questions/29138054/how-to-replace-tabs-in-a-string/29138079
* https://stackoverflow.com/questions/41220172/regex-to-splitstring-on-date-and-keep-it
* https://www.geeksforgeeks.org/python-convert-list-into-list-of-lists/
* https://datascience.stackexchange.com/questions/26333/convert-a-list-of-lists-into-a-pandas-dataframe
