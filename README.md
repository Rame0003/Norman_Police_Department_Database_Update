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
 Once the string is obtained, we begin the text processing by first removing `NORMAN POLICE DEPARTMENT\nDaily Incident Summary (Public)` string. If this is not removed, this will cause issues later when the dataframe is populated. Once this is executed, we begin breaking the strings by using regex to find the space between patterns. 
 The reason I begin using regex is to tackle a particular issue that people faced after converting their text into items in a list: Once the data was split according to the position of dates, the data is converted into list of lists to be placed into the database or dataframe. Some addresses are in two lines
