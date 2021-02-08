import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

Jsonfiles = ['/Users/sravani/Desktop/Sravani_python_project/archive/2005_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2006_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2007_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2008_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2009_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2010_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2011_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2012_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2013_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2014_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2015_codes.json']
Filenames = ["/Users/sravani/Desktop/Sravani_python_project/archive/2005_daita.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2006_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2007_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2008_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2009_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2010_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2011_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2012_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2013_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2014_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2015_data.csv"]
years = [2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]
Numberofdeaths=[]
print("The major causes of deaths in the United States for the years 2005-2015 are:")
for i in range(11):
    with open(Jsonfiles[i]) as json_file:
        json_data=json.load(json_file)
    csv_data = pd.read_csv(Filenames[i], low_memory=False)
#df = np.loadtxt(open("/Users/sravani/Desktop/Sravani_python_project/archive/2005_data.csv","rb"),delimiter=",")
    causeofdeath_year = csv_data['358_cause_recode']
    uniquevalue, elementcount = np.unique(causeofdeath_year, return_counts=True)
    #print(uniquevalue,elementcount)
    #print(len(causeofdeath_year))
    s = np.max(elementcount)    #Maximum number of times a disease occured in this year
    Numberofdeaths.append(s)
    #print("Maximum number of times a disease occured in this year is:", s)
    k = list(elementcount).index(s)
    #print("Index of maximum times that disease occured in the year is:", k)
    if (uniquevalue[k] < 10):
        major_cause = "00" + str(uniquevalue[k])
        #print("Cause-number for major cause of death"+" in the year "+ str(years[i]) +" is:"+ str(major_cause))
    elif (uniquevalue[k]>9 and uniquevalue[k]<100):
        major_cause = "0" + str(uniquevalue[k])
        #print("Cause-number for major cause of death" + " in the year " + str(years[i]) + " is:" + str(major_cause))
    else:
        major_cause = str(uniquevalue[k])
        #print("Cause-number for major cause of death" + " in the year " + str(years[i]) + " is:" + str(major_cause))
    #print(major_cause)
    print("Major cause of the death in the year " + str(years[i]) + " is: " + str(major_cause) + " - " + json_data['358_cause_recode'][major_cause])

print(Numberofdeaths)
plt.plot(years,Numberofdeaths,'b')
plt.ylabel("Number of deaths for each year in the United States")
plt.xlabel("Years")
plt.title("Number of deaths each year due to major cause of death")
plt.show()