import pandas as pd
from os import walk
from pathlib import Path
import re
import ntpath
import tkinter as tk
import os
from collections import defaultdict
f =[]
dn =[]
dp =[]
d = defaultdict(list)
pathbuilt =[]
mainpath ="C:\\Users\\JMRW38\\Desktop\\CorrUnit"
global counter
#counter = 0
path_to_dictonary ={}
add_in_dictionary = False

def DirSearch(mainpath,counter):
    internal_file_counter = 0
    p = Path(mainpath)
    for dirnames in p.iterdir():
        # get dirnames get the next level directory
        p = Path(dirnames)
        if p.is_dir():
            _, counter = DirSearch(dirnames, counter)

        if p.is_file():
          # inside here, should be all the file split the file out from the path
          path,file = os.path.split(dirnames)
          Amount_of_file = len(os.listdir(path))
          internal_file_counter = internal_file_counter + 1
          # Here is a file
          d[counter].append(dirnames)
          if internal_file_counter == Amount_of_file:
              counter = counter + 1
              # Reset the file_counter
              internal_file_counter = 0

    return (d,counter)


def DataCombine(value_in_dictionary,value):
    # Come in all files
    base_file = value_in_dictionary[0]
    path, file = os.path.split(base_file)
    component = re.split(r"_", file)
    data = pd.read_csv(base_file,skiprows= 9 , usecols=['Name','Measurement'])
    data_rename = data.rename(columns={"Measurement": component[0]})
    for i in range(1, len(value_in_dictionary)):
        child_file = value_in_dictionary[i]
        path, file = os.path.split(child_file)
        component = re.split(r"_", file)
        child = pd.read_csv(child_file,skiprows= 9 , usecols=['Name','Measurement'])
        data_rename1 = child.rename(columns={"Measurement": component[0]})
        data_rename = data_rename.join(data_rename1[component[0]])
    # Save inside new file
    # Split the file to get the path
    path, file = os.path.split(base_file)
    a = re.split(r"\\",path)
    # Use path to save the data
    save_path = path + "\\totalfile_" + a[5] +"_" + a[6] +"_"+ a[7] +".csv"
    data_rename.to_csv(save_path)

def path_split(base_path,list_to_process):
#    ntpath.basename(base_path)
    for i,value_in_dictionary in enumerate(list_to_process):
        DataCombine(list_to_process[value_in_dictionary],i)
        # for single_to_process in list_to_process[value_in_dictionary]:
        #     head, tail = ntpath.split(single_to_process)
        #     print (head,tail)
# for (dirpath,dirnames,filenames) in walk(mainpath):
#     dp.extend(dirpath)
#     dn.extend(dirnames)
#     print (dirnames)
#     #look for corr name
#     corr = []
#     for dirname in dirnames:
#  #       match = re.search(r"Corr#\d", dirname)
#         match = re.search(r"[\w*]\d", dirname)
#         if match != None:
#             pass
# #            print (match.group())
#     print (len(corr))
#     f.extend(filenames)
#     # Construct path
#
#
#
# print (dp)
# print (dn)
# print (f)
# print (len(f))


# data = pd.read_csv("C:\\Users\\JMRW38\\Desktop\\CorrUnit\\Corr#1\\Head1\\Fix1\\CRUHFMTP03_1_636597549675588253.csv",
#                    skiprows= 9,usecols = ['Name','Measurement'])
#
# print (data)
# data_rename1 = data.rename(columns={"Measurement":"1"})
# print (data_rename1)
# data2 = pd.read_csv("C:\\Users\\JMRW38\\Desktop\\CorrUnit\\Corr#1\\Head1\\Fix1\\CRUHFMTP04_1_636597550974915571.csv",
#                    skiprows= 9,usecols = ['Name','Measurement'])
#
# data_rename2 = data2.rename(columns={"Measurement":"2"})
# print (data_rename2)
# #join data
# total = data_rename1.join(data_rename2["2"])
# print (total)

if __name__ == "__main__":
   dp1,_ =  DirSearch(mainpath,counter = 0)
   path_split(mainpath,dp1)