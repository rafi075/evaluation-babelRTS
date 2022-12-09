from babelrts import BabelRTS
import subprocess
import os
from os.path import relpath
from fnmatch import fnmatch
import random
import linecache
from re import compile as recmp
import pandas
import re

#for compilation
from utils.run_cmd import rc
#from utils.java_evaluation import je


killableMutants = 0
killedMutants = 0

comilableRevisions = 0
UnComilableRevisions = 0

mutatedButNotCompiled = 0
mutatedAndCompiled = 0

maxRevNumber = 3
maxDeletionNumber = 20
revisions = []
checkForEligibility = 10

#projectName = "commons-collections"
#projectName = "commons-cli"
#srcPath = "src/main/java"
#testPath = "src/test/java"
#lang = "java"tests


#projectName = "commons-collections"
#projectName = "pyecharts"
#srcPath = "."
#testPath = "test"
#lang = "python"
#pattern = "*.py"

#[('commons-collections',  'src/main/java', 'src/test/java', 'java',  '*.java'),    
#               ('commons-cli',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-text',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-configuration',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-fileupload',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-dbcp',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-jxpath',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-lang',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-net',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-pool',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-validator',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('HikariCP',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('lambda',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('stream-lib',  'src/main/java', 'src/test/java', 'java',  '*.java'),
#              ('commons-io',  'src/main/java', 'src/test/java', 'java',  '*.java')]

projectList = [('commons-fileupload',  'src/main/java', 'src/test/java', 'java',  '*.java'),
              ('commons-dbcp',  'src/main/java', 'src/test/java', 'java',  '*.java'),
              ('commons-jxpath',  'src/main/java', 'src/test/java', 'java',  '*.java'),
              ('commons-lang',  'src/main/java', 'src/test/java', 'java',  '*.java'),
              ('commons-net',  'src/main/java', 'src/test/java', 'java',  '*.java'),
              ('commons-pool',  'src/main/java', 'src/test/java', 'java',  '*.java')]


#projectName = "pyecharts"
#srcPath = "."
#testPath = "test"
#lang = "python"

def isEligibleStatement(line, lang):
    if lang == 'java':
        if (not line) or '/*' in line or '*/' in line  or line.startswith('*') or re.search("^\s*$", line) or re.search("^[\s]*\*", line) or re.search("^[\s]*\/\/", line) or '{' in line or '}' in line or 'return ' in line or 'if' in line or 'for' in line or 'class ' in line or 'public ' in line or 'private ' in line or 'import' in line or 'package' in line:
            return False
        else:
            return True
        
    elif lang == 'python':
        if (not line) or  line.startswith('#') or re.search("^\s*$", line) or re.search("^[\s]*\#", line)  or '"""' in line or '"""' in line or 'return ' in line or 'if ' in line or 'for ' in line or ':\n' in line or 'def ' in line or 'class ' in line or 'import' in line:
            return False
        else:
            return True
        
    else:
        print('Language support not available')
        return False

    
def changeDirectory(projectName):
    cwd = os.getcwd()
    chDir = cwd + '/' + projectName
    os.chdir(chDir)
    return cwd, chDir

def returnToCommonDirectory(commonDirectory):
    os.chdir(commonDirectory)


def getRevisions(maxRevNumber):
    
    getMaxRevNumCommitCommand = "git --no-pager log --first-parent --pretty=tformat:%H -"+str(maxRevNumber)
    output = subprocess.getoutput(getMaxRevNumCommitCommand)
    revisions = output.splitlines()

    return revisions

def checoutToRevision(revision):
    subprocess.run(["git", "checkout", revision])
    #label = subprocess.check_output(["git", "describe"]).strip()
    label = ""
    return label


def compileRevision(revision):
    isSuccess = False
    
    return isSuccess

def sdMutation(pattern, srcPath, lang, testPath):
    
    fileList = getFileList(pattern, srcPath, testPath)
    fileListLen = len(fileList)
    print('File List Len :', fileListLen )
    
    while True:
        while True:
            selectedFile, selectedFilePath = getRandomFile(fileList)
            lineCount = getFileLineCount(selectedFilePath)
            print('Selected File ', selectedFile, ' Line Count ', lineCount)
            if lineCount>0:
                break

        selectedLineNumber, particular_line, isLineEligible = getRandomLine(selectedFilePath,lineCount, lang)
        if isLineEligible:
            break;
    
    lines = getAllFileContent(selectedFilePath)
    
    #deleteline
    # Write all lines except the 'selected removable line'
    with open(selectedFilePath, 'w') as fp:
        for number, line in enumerate(lines):
            if number != (selectedLineNumber-1):
                fp.write(line)  
            #else:
                #print('Skipped Line: ', line)
                
    fp.close()
    
    
    return selectedLineNumber, selectedFilePath, particular_line, fileListLen
    


def getFileList(pattern, srcPath, testPath):
    cwd = os.getcwd()
    testPathMatch =  '/' + testPath + '/'
    
    fileList = []
    #get all the files in a list
    walkPath = cwd + "/"+ srcPath
    #print("Walk path : ",walkPath)
    for path, subdirs, files in os.walk(walkPath):
        for name in files:
            if fnmatch(name, pattern):
                fileData =[]
                fileData.append(path)
                fileData.append(name)
                selectedFilePath = path + '/' + name
                if testPathMatch in selectedFilePath:
                    continue
                fileList.append(fileData)


    return fileList


def getRandomFile(fileList):
    #select random files from the list
    selectedFile = random.choice(fileList)
    selectedFilePath = selectedFile[0] + '/' + selectedFile[1]

    return selectedFile,selectedFilePath


def getFileLineCount(selectedFilePath):
    lineCount = 0
    with open(selectedFilePath, 'r') as fp:
        lineCount = len(fp.readlines())
    #print('Total Number of lines:', lineCount)

    fp.close() 
    
    return lineCount

def getRandomLine(selectedFilePath,lineCount, lang):
    
    #select random line of the selected file
    selectedLineNumber = None
    count = 0
    isLineEligible = False
    
    while True:
        selectedLineNumber = random.randint(1,lineCount)   
 
        # extracting the nth line
        particular_line = linecache.getline(selectedFilePath, selectedLineNumber)
        if isEligibleStatement(particular_line, lang):
            print('Eligible line: ',  particular_line)
            isLineEligible =True
            break
        count = count + 1
        if checkForEligibility == count:
            break
            
    return selectedLineNumber, particular_line, isLineEligible

def getAllFileContent(selectedFilePath):
    #get all lines in a list
    lines = []
    # read file
    with open(selectedFilePath, 'r') as fp:
    # read an store all lines into list
        lines = fp.readlines()   
    fp.close()   
    return lines

def revertToUnmutatedVersion():
    label = subprocess.run(["git", "checkout", "."])
    return label


#JAVA Build Methods
def build_java_project():
    labelRun = rc('mvn clean install -DskipTests -Drat.skip=true')
    return labelRun

def checkSuccessfulBuild_Java(buildOutPut):
    if buildOutPut.find('BUILD SUCCESS')==-1:
        return False
    return True

def run_all_java_test():
    labelRunTest = rc('mvn test -Drat.skip=true')
    return labelRunTest


#PYTHON Build Methods
def run_all_python_test():
    labelRunTest = rc('python -m pytest')
    return labelRunTest


def compileRevision(language):
    var = False
    if language == 'java':
        revBuild = build_java_project()
        revBuildOutPut = revBuild[1]
        var = checkSuccessfulBuild_Java(revBuildOutPut)

    elif language == 'python':
        var = True
    else:
        print('Language not supported. Language: ', language)
        
    return var 


def testRevision(language):
    testOutPut = None
    if language == 'java':
        testOutPut = run_all_java_test()

    elif language == 'python':
        testOutPut = run_all_python_test()
    else:
        print('Language not supported. Language: ', language)
        
    return testOutPut


def runBabelRts(cwd, projectName, babelRTS):
    returnToCommonDirectory(cwd)
    selected_test = babelRTS.rts()
    cwd,chDir = changeDirectory(projectName)
    return selected_test

def setChangedFileAndgetSelectedTestsForBabelRTS(cwd, projectName, babelRTS,selectedFilePath, lang):
    selected_tests = {}
    returnToCommonDirectory(cwd)
   
    try:
        if lang == 'java' or lang == 'python':
            relPath = relpath(selectedFilePath,projectName)
            print('Rel Path: ', relPath, ' Lang: ', lang)
            babelRTS.get_change_discoverer().set_changed_files({relPath})

        else:
            print("not supported for other languages")
    except Exception as e:
        print('Exception: ', e)
    
    selected_tests = babelRTS.get_test_selector().select_tests()
    cwd,chDir = changeDirectory(projectName)
    
    return selected_tests

def runSelectedTestsBabelRTS(selected_tests,lang):
    
    testLog = None
    if lang == 'java':
        
        selected_classes = (file.split('/java/',1)[1].replace('/','.') for file in selected_tests)
        testLog = rc(f'mvn test -Drat.skip=true -Dtest={",".join(selected_classes)}')
    
    elif lang == 'python':
        testLog = rc(f'python3.9 -m pytest {" ".join(selected_tests)}')
    else:
        
        print("not supported for other languages")
        
        
    return testLog
    
    

def getErrorFailureFromLog(log, lang):
    errorPlusFailure = 0 
    error = 0
    failure = 0
    
    if lang == "java":
        log = log[1]  
        MVN_TESTS = recmp(r'Tests run: \d+, Failures: (\d+), Errors: (\d+), Skipped: \d+')
        errList = MVN_TESTS.findall(log)[-1]
        errorPlusFailure = int(errList[0]) + int(errList[1])
        error = int(errList[0])
        failure = int(errList[1])
        
    elif lang == "python":
        log = log[1]  
        errorPlusFailure, error, failure = gerErrFailCount_from_PythonLog(log)
   
    else:
        print('Language not supported')
  
    return errorPlusFailure, error, failure


def gerErrFailCount_from_PythonLog(my_str):
    erro_failure = 0
    error = 0
    failure = 0
    
    saveStr = ''
    indicator = 0
    for char in my_str[::-1]:
        if char != '=' :
            saveStr = saveStr + char
            indicator = 1
        else:
            if indicator ==1:
                break;


    saveStr = saveStr[::-1]
    position = saveStr.index(' in ')
    if(position<2):
        print('Position Less Than 2, ', saveStr )
        return erro_failure, error, failure
    
    saveStr = saveStr[1 : position : ]
    listOfResult = saveStr.split(", ")

    
    
    for info in listOfResult:
        splitRes = info.split(" ")
        if 'error' in info or 'errors' in info :
            erro_failure = erro_failure + int(splitRes[0])
            error = error + int(splitRes[0])
        elif 'failed' in info:
            erro_failure = erro_failure + int(splitRes[0])
            failure = failure + int(splitRes[0])
    return erro_failure, error, failure


def prepareResultData(Project_Name,Language, revision, isRevCompileable = 0, isRevTestSuccess =0, No_of_Files = 0, File_Path= None, Deleted_Line= 'N/A', isMutantCompiled = 0, isKillableMutant = 0, Mut_All_Test_Error =0, Mut_All_Test_Failure =0, BRTS_Error =0, BRTS_Failure =0, isKilledByBRTS =0):
    
    dataRow = []
    dataRow.append(Project_Name)
    dataRow.append(Language)
    dataRow.append(revision)
    dataRow.append(isRevCompileable)
    dataRow.append(isRevTestSuccess)
   
    dataRow.append(No_of_Files)
    dataRow.append(File_Path)
    #dataRow.append(deleted_Line_No)
    #dataRow.append(Total_Line)
    dataRow.append(Deleted_Line)
    
    dataRow.append(isMutantCompiled)
    dataRow.append(isKillableMutant)
    
    dataRow.append(Mut_All_Test_Error)
    dataRow.append(Mut_All_Test_Failure)
    
    dataRow.append(BRTS_Error)
    dataRow.append(BRTS_Failure)
    dataRow.append(isKilledByBRTS)
    
    
    return dataRow
    
    



#---------------------------------------------main code ---------------------------------
dataFrame = []
col_name = ['Project Name','Language', 'revision',  'isRevCompileable', 'isRevTestSuccess', 'No of Files', 'File Path', 'Deleted Line', 'isMutantCompiled', 'isKillableMutant', 'Mut All Test Error', 'Mut All Test Failure', 'BRTS Error', 'BRTS Failure', 'isKilledByBRTS']

for projectName, srcPath, testPath, lang, pattern in projectList:
    print(projectName, srcPath, testPath, lang, pattern)
    #Create a BabelRTS object
    babelRTS = BabelRTS(projectName, srcPath, testPath, languages=lang)


    #go to project folder
    cwd,chDir = changeDirectory(projectName)
    revisions = getRevisions(maxRevNumber)
    #print(revisions)

    for revision in revisions: 

        checkedOutHash = checoutToRevision(revision)

        #build or run project
        checkRevBuildSuccess = compileRevision(lang)

        #test all
        if checkRevBuildSuccess :

            labelRunTest = testRevision(lang)

            error_failure, error, failure = getErrorFailureFromLog(labelRunTest,lang)

            if error_failure > 0 :
                print('Revision contains error/failure. Discarding.')
                
                #Saving Result
                resultData = prepareResultData(projectName, lang, revision, isRevCompileable=1, isRevTestSuccess =0  )
                dataFrame.append(resultData)
                
                continue
        else:
            print('Build failed for checkout to revision')
            
            #Saving Result
            resultData = prepareResultData(projectName, lang, revision, isRevCompileable=0 )
            dataFrame.append(resultData)
            
            continue

        #run babelRTS to create DOT_BABELRTS File
        print('Revision Build sucessful. Running babelRTS')
        runBabelRts(cwd, projectName, babelRTS)


        #Revision Build is successful. So mutate
        for i in range (maxDeletionNumber):
            try:
                print('Mutation Number: ', i, ' Revision: ', revision)
                #delete one line of code
                selectedLineNumber, selectedFilePath, particular_line, fileListLen = sdMutation(pattern, srcPath, lang, testPath)

                #check if mutated program builds
                checkMutBuildSuccess = compileRevision(lang)

                if checkMutBuildSuccess :
                    print('Build successful for mutated program. Now test execution')
                    labelRunTestAfterMutation = testRevision(lang)

                    #detect failure or error
                    mut_error_failure, mut_error, mut_failure = getErrorFailureFromLog(labelRunTestAfterMutation,lang)

                    if mut_error_failure > 0:

                        killableMutants = killableMutants + 1
                        print('Found error+failure in Mutant. Current Killable mutant ', killableMutants)
                        selected_tests = setChangedFileAndgetSelectedTestsForBabelRTS(cwd, projectName, babelRTS,selectedFilePath, lang)

                        #run babelRTS selection on the mutan
                        testLog = runSelectedTestsBabelRTS(selected_tests,lang)
                        print('Testlog from babelRTS changed file ' )

                        mut_error_failure_by_babelRTS, error_by_babelRTS, failure_by_babelRTS = getErrorFailureFromLog(testLog,lang)
                        print('mut_error_failure_by_babelRTS ',mut_error_failure_by_babelRTS,' error_by_babelRTS ', error_by_babelRTS,' failure_by_babelRTS ', failure_by_babelRTS )

                        if mut_error_failure_by_babelRTS > 0:
                            killedMutants = killedMutants + 1
                            
                            #Saving Result
                            resultData = prepareResultData(projectName, lang, revision, isRevCompileable=1, isRevTestSuccess =1, No_of_Files = fileListLen, File_Path = selectedFilePath, Deleted_Line = particular_line, isMutantCompiled=1,isKillableMutant=1, Mut_All_Test_Error = mut_error, Mut_All_Test_Failure = mut_failure, BRTS_Error = error_by_babelRTS, BRTS_Failure =failure_by_babelRTS, isKilledByBRTS = 1)
                            dataFrame.append(resultData)
                    
                        else:
                            print('Not Killed By BabelRTS')
               
                            #Saving Result
                            resultData = prepareResultData(projectName, lang, revision, isRevCompileable=1, isRevTestSuccess =1, No_of_Files = fileListLen, File_Path = selectedFilePath, Deleted_Line = particular_line, isMutantCompiled=1,isKillableMutant=1, Mut_All_Test_Error = mut_error, Mut_All_Test_Failure = mut_failure, BRTS_Error =0, BRTS_Failure =0, isKilledByBRTS =0)
                            dataFrame.append(resultData)
                    
                    else:
                        print('Mutation has no effect. No test fail while running all_test')
                        
                        #Saving Result
                        resultData = prepareResultData(projectName, lang, revision, isRevCompileable=1, isRevTestSuccess =1, No_of_Files = fileListLen, File_Path = selectedFilePath, Deleted_Line = particular_line, isMutantCompiled = 1,isKillableMutant=0)
                        dataFrame.append(resultData)

                else:
                    print('Build failed for mutated program')
                    
                    #Saving Result
                    resultData = prepareResultData(projectName, lang, revision, isRevCompileable=1, isRevTestSuccess =1, No_of_Files = fileListLen, File_Path = selectedFilePath, Deleted_Line = particular_line, isMutantCompiled = 0 )
                    dataFrame.append(resultData)
                    
            except Exception as e:
                #Saving Result
                #resultData = prepareResultData(projectName, lang, revision, isRevCompileable=0 )
                #dataFrame.append(resultData)
                print('Unexpected Error Occured: ', e)


            #revert to um mutated version
            print('Returning to UnMutated versiob')
            label = revertToUnmutatedVersion()
    #return to common directory
    returnToCommonDirectory(cwd)
        
        
        

print("---------------------------summary-------------------")
        
print("Killeable Mutants: ",killableMutants)
print("Killed Mutants: ",killedMutants)

print("mutatedButNotCompiled: ",mutatedButNotCompiled)

print("Total Attempts: ", maxRevNumber * maxDeletionNumber)

if killableMutants == 0:    
    print("No killable mutants found")
else:
    print("killed/killable: ", (killedMutants*100)/killableMutants)
    
#Result Summation
pandasDF = pandas.DataFrame(dataFrame)
pandasDF.columns = col_name
print(pandasDF)
pandasDF.to_excel('Result.xlsx')
   
 

        
    
    

