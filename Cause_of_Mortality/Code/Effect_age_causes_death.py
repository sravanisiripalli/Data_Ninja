# Code for finding out the major cause of death in a single year
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

Jsonfiles = ['/Users/sravani/Desktop/Sravani_python_project/archive/2005_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2006_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2007_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2008_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2009_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2010_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2011_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2012_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2013_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2014_codes.json','/Users/sravani/Desktop/Sravani_python_project/archive/2015_codes.json']
Filenames = ["/Users/sravani/Desktop/Sravani_python_project/archive/2005_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2006_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2007_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2008_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2009_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2010_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2011_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2012_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2013_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2014_data.csv","/Users/sravani/Desktop/Sravani_python_project/archive/2015_data.csv"]
years = [2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]

for y in range(11):
    with open(Jsonfiles[y]) as json_file:
        json_data = json.load(json_file)
    df = pd.read_csv(Filenames[y], low_memory=False)

    indx = df.groupby(['age_recode_52'], sort=True)
    groupby_ages = []
    for key, item in indx:
        groupby_ages.append(indx.get_group(key))
    Numberofdeaths={}
    Majorcauses=[]
    for i in range(len(groupby_ages)):
        L1 = groupby_ages[i]['358_cause_recode']
        L2 = str((list(groupby_ages[i]['age_recode_52']))[0])
        if int(L2) < 10:
            L2 = "0" + L2
        uniquevalue, elementcount = np.unique(L1, return_counts=True)
        k = uniquevalue[list(elementcount).index(np.max(elementcount))]
        major_cause = str(k)
        if k < 9:
            major_cause = "00" + major_cause
        if 9 < k < 99:
            major_cause = "0" + major_cause
        Numberofdeaths[L2]=np.max(elementcount)
        Majorcauses.append(major_cause)
        #print("In the year"+str(years[y]))
        print("In "+str(years[y])+" Major cause of the death for the age group code " + L2 +" "+ json_data['age_recode_52'][L2] + " is: " + major_cause + " - " + json_data['358_cause_recode'][major_cause])
    print("*********************************************************************************************************")
    plt.bar(Numberofdeaths.keys(), Numberofdeaths.values(),width=0.75, color='r', data =Majorcauses)
    plt.xlabel('Age groups')
    plt.ylabel('Number of deaths due to major cause of disease')
    plt.title('Number of deaths for different age groups'+'in year'+str(years[y]))
    plt.show()

