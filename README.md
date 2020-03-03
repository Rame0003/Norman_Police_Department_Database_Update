# cs5293p20-project0
## Norman Police Department Database Update
### Introduction:
This project aims to update the incidents and order them alphabetically. The program contains of 5 different steps to process the data from the PDF and pushing into the SQLite database that has been created. The final required result is to make sure that the nature of incidents is displayed along with the count. 

We will be going through the steps taken to analyse the data, the assumptions made and other important details.

### Assumptions:
1. Each of the column follows the following pattern:
  a. The timestamp is given as mm/dd/yyyy hh:mm
  b. The incident number is given in the form of 4x8 numbers seaprated by a (-)
  c. The addresses always are given in caps
  d. The nature of incident is a normal word which has a capital letter in the beginning and the rest is small (Eg: Norman)
  e. The Incident_ori column contains any of these 4 cases: OK0140200, EMSSTAT, 14005 or 14009.
  f. The files have no missing nature. All of the cases are assigned to some case.

### 
