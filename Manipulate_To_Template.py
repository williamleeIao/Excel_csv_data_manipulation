import pandas as pd
from os import walk
from pathlib import Path
import re
import ntpath
import tkinter as tk
import os
import numpy as np
from collections import defaultdict
file_name = "C:\\Users\\JMRW38\\Desktop\\CorrUnit\\Corr#1\\Head1\\Fix1\\totalfile_Corr#1_Head1_Fix1.csv"
mainpath ="C:\\Users\\JMRW38\\Desktop\\CorrUnit"


xl = pd.ExcelFile("C:\\Users\\JMRW38\\Documents\\project\\Monte+\\CorrelationDat.xlsx")
#xl_file = pd.ExcelFile(file_name)
path1,f_name=os.path.split(file_name)
component = re.split(r"[_.]",file_name)
print (component[1])
print (component[2])
print (component[3])
print (xl.sheet_names)
print (len(xl.sheet_names))

df1 = pd.read_excel(xl,xl.sheet_names[6])
print (df1)
print (df1.columns[:10])
print (df1.columns[0])
# Extract Serial number
print(df1[df1.columns[1]])
sn = df1[df1.columns[1]]
print (sn)
a =['A','NA','B','C','NA']
print (type(np.array(sn).tolist()))
print (type(a))
unique_sn = np.unique(np.array(sn).tolist())
print (unique_sn)
#---------------------------------------------------
# Using Component[2] to extract correct column
value =['Head1']
for i in range(1,6,1):
    value.append('Head1.' +str(i))

print (df1[value])

# Get the fixture number
print (df1[value].iloc[1])

#---------------------------------------------------
# From value get back index
#print (df1[df1['Serial Number']=='632TUD0468(04)'].index[0])
#---------------------------------------------------
#Extract Test Parameter
#print (df1[df1.columns[0]])
#print (np.unique(np.array(df1[df1.columns[0]]).tolist()))
#a = np.unique(np.array(df1[df1.columns[0]]).tolist())
# From test parameter get the value at template file
csv_file = pd.read_csv(file_name)
#print (csv_file[csv_file['Name'] == "TX_POW8_CORR_F1"])
# Testing Value
single = csv_file[csv_file['Name'] == "TX_POW8_CORR_F1"]
single['CRUHFMTP03'] = 100
print (single)

def DirSearch(mainpath,Freq_Test, unique_sn, df1):
    p = Path(mainpath)
    for dirnames in p.iterdir():
        # get dirnames get the next level directory
        p = Path(dirnames)
        if p.is_dir():
            DirSearch(dirnames, Freq_Test, unique_sn, df1)

        if p.is_file():
          #  File open at here
          path1, f_name = os.path.split(dirnames)
          if re.match(r'^totalfile',f_name):
              component = re.split(r"[_.]", f_name)
              station_name = component[1]
              head = component[2]
              fixture = component[3]
              print(xl.sheet_names)
              print(len(xl.sheet_names))
              Execute_File(dirnames, station_name,head,fixture,Freq_Test, unique_sn, df1)

def Execute_File(dirnames,station_name,head,fixture,Freq_Test, unique_sn, df1):
    # Station Name = xl,sheet_names
    csv_file = pd.read_csv(dirnames)
    for i in range(len(Freq_Test)-1):
        single_element = csv_file[csv_file['Name'] == Freq_Test[i]] # Pull out test parameter
        # Writing Value
        for j in range(len(unique_sn)-1):
            #
            value_from_file = single_element[unique_sn[j]].values[0]  # Serial number that arrange by column
            # Read for fixture locate for position by Head follow by Fix
            # Find the position of the template file
            # locate the head first follow by fixture
            for k in range(3, len(df1.columns.tolist())-1):
                if re.match(head,df1.columns.tolist()[k]):
                #if re.search(head,df1.columns.tolist()[k]).group(0) == head:
                    row_loc = df1.index[df1['Serial Number'] == unique_sn[j]].tolist()[0]
                    row_loc = row_loc + 2 # Update new location
                    if df1.loc[1,df1.columns.tolist()[k]] == fixture:
                        df1.loc[row_loc, df1.columns.tolist()[k]]  = value_from_file
#                        inner_value = df1.loc[row_loc,df1.columns.tolist()[k]]
                        # How to print out file to text
 #                       file = open ("text_value_file.txt","a+")
                        #s = "_" + head + "_" + fixture + "_" + ":" + inner_value + "\n"
 #                       s = station_name + "_" + head + "_" + fixture + "_" + Freq_Test[i] + "_" + unique_sn[j] +":" + str(inner_value) + "\n"
 #                       file.write(s)
 #                       file.close()

def Open_Template_File():
    df1 = pd.read_excel(xl, xl.sheet_names[6])
    print(df1)
    # Info Parameter , Serial Number
    General_info = df1.columns[:3]
    # Info Head1
    Head1_info = df1.columns[4:9]
    # Info Head2
    Head2_info = df1.columns[14:19]
    print (General_info)
    print(Head1_info)
    print(Head2_info)
    # Extract Serial number
    print(df1[df1.columns[1]])
    sn = df1[df1.columns[1]]
    print(type(np.array(sn).tolist()))
    unique_sn = np.unique(np.array(sn).tolist())
    print (unique_sn)
    # Take parameter out from CorrelationData.xls
    Freq_Test = np.unique(np.array(df1[General_info[0]]).tolist())
    print (Freq_Test)
    return (Freq_Test,unique_sn,df1)


if __name__ == "__main__":

    Freq_Test, unique_sn, df1 =  Open_Template_File()
    print (df1)
    DirSearch(mainpath,Freq_Test,unique_sn,df1)
#    file.close()