# cs5293p20-project0
## Norman Police Department Database Update
### Introduction:
This project aims to update the incidents and order them alphabetically. The program contains of 5 different steps to process the data from the PDF and pushing into the SQLite database that has been created. The final required result is to make sure that the nature of incidents is displayed along with the count. 

We will be going through the steps taken to analyse the data, the assumptions made and other important details.

### Assumptions:
Each of the column follows the following pattern:
  * The timestamp is given as mm/dd/yyyy hh:mm 
  * The incident number is given in the form of 4x8 numbers seaprated by a (-) 
  * The addresses always are given in caps
  * The nature of incident is a normal word which has a capital letter in the beginning and the rest is small (Eg: Norman) 
  * The Incident_ori column contains any of these 4 cases: OK0140200, EMSSTAT, 14005 or 14009
  * The files have no missing nature. All of the cases are assigned to some case

### Code:
 This exercise was undertaken to give us a feel for text analytics. Though this can not be considered real text analysis, we can say that this exercise has made us understand what we can expect in upcoming projects and activities. Many people chose to write their code using indices as benchmarks. I chose to take a different approach and, with the above assumptions, chose to split up the text using regex. 
 The code is categorized into 5 sections, each of them performing a particular task to achieve the end goal:
 1. fetchincidents(url)
 2. extractincidents(file)
 3. createdb()
 4. populatedb(file)
 5. status()

#### Fetchincidents(url):
 
