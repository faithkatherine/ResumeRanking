#Pilot Testing 
import pandas as pd
from tika import parser
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize 
import io
import textract
import fitz
import os

#Dataset Loading and Preprocessing Module
def loadSkillDataset():
    skillDataset = pd.read_csv('ResumeSkill.csv')
    frontEnd = list(skillDataset['Front_End'])
    backEnd = list(skillDataset['Back_End'])
    machineLearning = list(skillDataset['Machine_Learning'])
    androidDeveloper = list(skillDataset['Android_Developer'])
    educationLevel = list(skillDataset['Education'])
    cleanedFrontEndList = [x for x in frontEnd if str(x) != 'nan']
    cleanedBackEndList = [x for x in backEnd if str(x) != 'nan']
    cleanedMachineLearningList = [x for x in machineLearning if str(x) != 'nan']
    cleanedAndroidDeveloperList = [x for x in androidDeveloper if str(x) != 'nan']
    cleanedEducationLevel = [x for x in educationLevel if str(x) != 'nan']
    return cleanedFrontEndList , cleanedBackEndList , cleanedMachineLearningList , cleanedAndroidDeveloperList, cleanedEducationLevel

frontEndList , backEndList , machineLearningList , androidDevelopmentList, educationLevelList = loadSkillDataset()

dir_list = os.listdir(r'D:/FINAL YEAR PROJECT/Resumes/NewTestData/')
resumes=r'D:/FINAL YEAR PROJECT/Resumes/NewTestData/'
# Resume File Text Extractor Module
for i in dir_list:
    #c = c + 1
    #if c == 5000:
        #break
    pfinal = os.path.join(resumes, i)

    #def extract_text_from_pdf(file):
    def fileTextExtractor():
        '''Opens and reads in a PDF file from path'''
        resume_text=''
        if i.endswith('.pdf'):
            doc = fitz.open(pfinal)
            
            for page in doc:
                resume_text = resume_text + str(page.getText())
            resume_text = "".join(resume_text.split("\n"))
        
        '''Opens en reads in a .doc or .docx file from path'''

        if i.endswith('.doc'):
            resume_text = textract.process(pfinal).decode('utf-8')
        return resume_text

    obtainedResumeText = fileTextExtractor()



#Resume email and phone number extractor Module
    def personalDetailExtractor():
        finalExtractedEmail = []
        finalExtractedPhone = []
        oneFourthOfResume = obtainedResumeText[0:len(obtainedResumeText)//4] 
        emailResume = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", oneFourthOfResume)
        phoneResume = re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})",oneFourthOfResume)
        
        if len(emailResume) > 1:
            finalExtractedEmail = emailResume[0]
        else:
            finalExtractedEmail = emailResume
            
        for i in range(len(phoneResume)):
            if len(phoneResume[i])>=10:
                finalExtractedPhone = phoneResume[i]
        return finalExtractedEmail,finalExtractedPhone

    finalExtractedEmail , finalExtractedPhone = personalDetailExtractor()

    #Capitalizing, LowerCase and Upper Case Conversion of the Resume Text Module
    firstLetterCapitalizedObtainedResumeText = []
    def CapitalizeFirstLetter(obtainedResumeText):
        capitalizingString = " "
        obtainedResumeTextLowerCase = obtainedResumeText.lower()
        obtainedResumeTextUpperCase = obtainedResumeText.upper()
        splitListOfObtainedResumeText = obtainedResumeText.split()
        for i in splitListOfObtainedResumeText:
            firstLetterCapitalizedObtainedResumeText.append(i.capitalize())        
        return (capitalizingString.join(firstLetterCapitalizedObtainedResumeText),obtainedResumeTextLowerCase,obtainedResumeTextUpperCase)
    firstLetterCapitalizedText,obtainedResumeTextLowerCase,obtainedResumeTextUpperCase = CapitalizeFirstLetter(obtainedResumeText)

    #Combination of LowerCase UpperCase and FirstLetter Capitalized
    obtainedResumeText = obtainedResumeTextLowerCase + obtainedResumeTextUpperCase + firstLetterCapitalizedText
    # Removing numbers from text file
    obtainedResumeText = re.sub(r'\d+','',obtainedResumeText)
    # Remove punctuation from the text files
    obtainedResumeText = obtainedResumeText.translate(str.maketrans('','',string.punctuation))

    #Resume educational Details Extracting Module
    def EducationDetailsExtractor(obtainedResumeText):
        obtainedResumeText.strip('/n')
        newLineRemovedResumeText = obtainedResumeText    
        resumeEducationSpecificationList = {'Education':educationLevelList}

        # Create an empty list where the scores will be stored
        educationExtracted = []
        for area in resumeEducationSpecificationList.keys():
            if area == 'Education' or 'Highschool' or 'Bachelors' or 'Bsc.':
                educationWord = []
                for word in resumeEducationSpecificationList[area]:
                    if word in obtainedResumeText:
                        educationWord.append(word)
                educationExtracted.append(educationWord)
        return educationExtracted

    extractedEducatioDetails = EducationDetailsExtractor(obtainedResumeText)

    def stopWordRemoval(obtainedResumeText):
        stop_words = set(stopwords.words('english')) 
        word_tokens = word_tokenize(obtainedResumeText) 
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 

        filtered_sentence = [] 
        joinEmptyString = " "
        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w)
        return(joinEmptyString.join(filtered_sentence))
        
    filteredTextForSkillExtraction = stopWordRemoval(obtainedResumeText)

    #Resume Skill Specification Listing and Extracting Module
    resumeTechnicalSkillSpecificationList = {'Front End':frontEndList,

                'Back End':backEndList, 'Machine Learning':machineLearningList,'Android Developer':androidDevelopmentList}

    def ResumeSkillExtractor(resumeTechnicalSkillSpecificationList,filteredTextForSkillExtraction):
        frontend = 0
        backend = 0
        machinelearning = 0
        androiddeveloper = 0

        # Create an empty list where the scores will be stored
        skillScores = []
        skillExtracted = []


        # Obtain the scores for each area
        for area in resumeTechnicalSkillSpecificationList.keys():

            if area == 'Front End':
                frontEndWord = []
                for word in resumeTechnicalSkillSpecificationList[area]:
                    if word in filteredTextForSkillExtraction:
                        frontend += 1
                        frontEndWord.append(word)
                skillExtracted.append(frontEndWord)
                skillScores.append(frontend)

            elif area == 'Back End':
                backEndWord = []
                for word in resumeTechnicalSkillSpecificationList[area]:
                    if word in filteredTextForSkillExtraction:
                        backend += 1
                        backEndWord.append(word)
                skillExtracted.append(backEndWord)
                skillScores.append(backend)

            elif area == 'Machine Learning':
                machineLearningWord = []
                for word in resumeTechnicalSkillSpecificationList[area]:
                    if word in filteredTextForSkillExtraction:
                        machinelearning += 1
                        machineLearningWord.append(word)
                skillExtracted.append(machineLearningWord)
                skillScores.append(machinelearning)

            elif area == 'Android Developer':
                androidDeveloperWord = []
                for word in resumeTechnicalSkillSpecificationList[area]:
                    if word in filteredTextForSkillExtraction:
                        androiddeveloper += 1
                        androidDeveloperWord.append(word)
                skillExtracted.append(androidDeveloperWord)
                skillScores.append(androiddeveloper)
        return skillScores,skillExtracted
    technicalSkillScore , technicalSkillExtracted = ResumeSkillExtractor(resumeTechnicalSkillSpecificationList,filteredTextForSkillExtraction)


    '''Personal Details, Skills and Academic Qualification Output Display'''

    dataList = {'Scores':technicalSkillScore,"Skills":technicalSkillExtracted}
    softwareDevelopemtTechnicalSkills = pd.DataFrame(dataList,index=resumeTechnicalSkillSpecificationList.keys())
    print("Email Address:",finalExtractedEmail)
    print("Phone Number:",finalExtractedPhone)
    print("Academic Qualifications:",extractedEducatioDetails)
    print(softwareDevelopemtTechnicalSkills)
    df = pd.DataFrame({"Email":[finalExtractedEmail], "Phone":[finalExtractedPhone], 
    "Academic Qualifications":[extractedEducatioDetails], "Skills":[softwareDevelopemtTechnicalSkills]})
    print(df)