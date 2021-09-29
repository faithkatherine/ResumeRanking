import os
from pandas.core.frame import DataFrame
import textract
import fitz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from resume_parser import resumeparse # Library 1
#from pyresparser import ResumeParser #Library 2
import os
#import spacy
import pandas as pd
#spacy.load('en_core_web_sm')
from django.conf import settings
            

class resume_ranking:

    def resumeranker(self):

        #res_list =np.array([name][extract_email_addresses])
        #res_list.shape()
        res_list = []
        dir_list = os.listdir(r'D:/FINAL YEAR PROJECT/Resumes/NewTestData/')
        resumes = r'D:/FINAL YEAR PROJECT/Resumes/NewTestData/'
        #c = 0
        for i in dir_list:
            #c = c + 1
            #if c == 5000:
                #break
            pfinal = os.path.join(resumes, i)

        #def extract_text_from_pdf(file):
            '''Opens and reads in a PDF file from path'''
            resume_text = ""
            if i.endswith('.pdf'):
                doc = fitz.open(pfinal)
                
                for page in doc:
                    resume_text = resume_text + str(page.getText())
                resume_text = "".join(resume_text.split("\n"))
            
            '''Opens en reads in a .doc or .docx file from path'''

            if i.endswith('.doc'):
                resume_text = textract.process(pfinal).decode('utf-8')

            job_description = open( "D:/FINAL YEAR PROJECT/Resumes/JobDescriptions/java.txt", "r")
            job_text = job_description.read()
        
            job_description.close()

            my_list = [resume_text, job_text]

            cv = CountVectorizer()
            count_matrix = cv.fit_transform(my_list)

            #Print the similarity scores
            print("\nSimilarity Scores:")
            print(cosine_similarity(count_matrix))

            matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
            matchPercentage = round(matchPercentage, 2) # round to two decimal
            print("Your resume matches about "+ str(matchPercentage)+ "% of the job description.")
            
            res_list.append(matchPercentage)
            #print(len(res_list))
            res_list.sort(reverse=True)
            print(res_list)
            df= pd.DataFrame(res_list)
            result = df.to_html()
        return(result)

    




            
                 
            
            #return txt.replace('\n', ' ').replace('\t', ' ')