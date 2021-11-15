from resume_parser import resumeparse # Library 1
from pyresparser import ResumeParser #Library 2
import os
import spacy
import pandas as pd


spacy.load('en_core_web_sm')
dir_list = os.listdir(r"D:\FINAL YEAR PROJECT\Resumes\TestData")
#print(dir_list)

res_list = []
paths = r"D:\FINAL YEAR PROJECT\Resumes\TestData"
c = 0
for i in dir_list:
    c = c + 1
    if c == 5000:
        break
    pfinal = os.path.join(paths, i)
    data = ResumeParser(pfinal).get_extracted_data()
    res_list.append(data)

df= pd.DataFrame(res_list)
df.to_csv('file1.csv')
