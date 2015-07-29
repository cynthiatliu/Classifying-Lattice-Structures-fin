#Main - actual data
#Implements the same strategy as main-frequency, but testing data is actual data

import numpy as np
import math
import re
import sys
import random as rd
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets, cross_validation
from sknn.mlp import Classifier, Layer
import randomCoords as rc
import randomCoords2 as rc2
import randomCoords3 as rc3

#Conversion to an understandable symbol
def numConvert(predictions):
    arr = []
    
    for pred in predictions:
        pred = int(float(pred))
        
        #Giant switch
        if pred == 0: arr.append('I')
        elif pred == 1: arr.append('F')
        elif pred == 2: arr.append('A')
        elif pred == 3: arr.append('B')
        elif pred == 4: arr.append('C')
        elif pred == 5: arr.append('R')
        else: arr.append('P')
        
    return arr

#Scrambles the testing coordinates
def scramble(coords):
    nums = np.arange(0, len(coords)) #possible indices
    origLength = len(nums)
    scrambledCoords = []
    
    for i in range(origLength):
        j = rd.randint(0,len(nums)-1) #Random index
        nums = np.delete(nums, j)
        scrambledCoords.append(coords[j])
        
    return scrambledCoords

#Formatting for fake and training data
def format(clf, toFit):
    #Ask for the number of points in 1 cluster
    good = False
    while good == False:
        try:
            groupSize = int(input("How many points would you like to have in one cluster? "))
            testPositive = math.sqrt(groupSize-1)
            good = True
        except:
            print ("Please input a valid value (numerical value larger than or equal to 1)")
            
    totalPtCount = len(toFit)/7 #Total number of points per structure
    pointLabels = np.zeros([7*math.ceil(totalPtCount/groupSize),groupSize])
    strucCounter = 0 #Number of structures we've been through
    while strucCounter < 7:
        count = 0 #basic counter - number of times we went through the loop
        numGroups = 0 #Number of completed groups within a structure
    
        while numGroups < math.ceil(totalPtCount)/groupSize:
            count = 0
            while count < groupSize and count < totalPtCount - numGroups*groupSize:
                index = strucCounter*totalPtCount + numGroups*groupSize + count
                pointLabels[strucCounter*len(pointLabels)/7+numGroups][count] = clf.predict(np.array([toFit[index]]))
                count += 1
    
            #print("Next group!")
            numGroups += 1
    
        #print ("Onto the next structure!")
        strucCounter += 1
        
    return pointLabels, groupSize

#Training-specific formatting
def formatTrain(clf, toFit):
    trPointLabels, ptsPerGroup = format(clf, toFit)
    print (trPointLabels.shape)
    totalPtCount = len(toFit)/7 #Total number of points per structure
        
    #Labeling groups of points to complete the training set
    targetVariables = np.zeros([len(trPointLabels)])
    count = 0
    for labelSet in trPointLabels:
        groupLabel = math.floor(count/math.ceil((totalPtCount/ptsPerGroup)))
        targetVariables[count] = groupLabel
        count += 1
        
    return trPointLabels, targetVariables, ptsPerGroup

#Formatting the frequency array
def formatFreq(arr, labels):
    count = 0
    for group in labels:
        group = [int(x+.00001) for x in group] #float error
        for num in group:
            arr[count][num] += 1
        count += 1
        
    return arr

#Main
def main():
    
    #Generate training data
    good = False
    while good == False:
        randomGenNum = raw_input("Within what range lies your hkl data? If none fit choose the closest.\n\nBetween -10 and 10 inclusive (choose 1)\nBetween 0 and 20 inclusive (choose 2)\nBetween -20 and 20 inclusive (choose 3)\n")
        randomGenNum = int(randomGenNum.strip())
        if (randomGenNum == 1 or randomGenNum == 2 or randomGenNum == 3):
            good = True
            if randomGenNum == 1: 
                rawTrain1 = rc.genCoords()
                rawX_train1 = rc.buildTrain(rawTrain1)[:,0:9]
                rawY_train1 = rc.buildTrain(rawTrain1)[:,-1]
                
                rawTrain2 = rc.genCoords()
                rawX_train2 = rc.buildTest(rawTrain2)[:] #Used in clf1 to make individual point predictions, the "actual training data"                
            elif randomGenNum == 2: 
                rawTrain1 = rc2.genCoords()
                rawX_train1 = rc2.buildTrain(rawTrain1)[:,0:9]
                rawY_train1 = rc2.buildTrain(rawTrain1)[:,-1]
                
                rawTrain2 = rc2.genCoords()
                rawX_train2 = rc2.buildTest(rawTrain2)[:] #Used in clf1 to make individual point predictions, the "actual training data"                
            else: 
                rawTrain1 = rc3.genCoords()
                rawX_train1 = rc3.buildTrain(rawTrain1)[:,0:9]
                rawY_train1 = rc3.buildTrain(rawTrain1)[:,-1]
                
                rawTrain2 = rc3.genCoords()
                rawX_train2 = rc3.buildTest(rawTrain2)[:] #Used in clf1 to make individual point predictions, the "actual training data"                
        else: print ("That's not a valid range, please try again.")
    
    print ("All training coordinates generated")
    
    #Reading testing data!
    good = False
    while good == False:
        fileName = raw_input("What is the name of the file you want to read? \n(Must be .txt) (enter 0 to quit) ")
        fileName = fileName.strip()
        if fileName == "0": break
        try:
            data = open(fileName, 'r')
            good = True
        except:
            print ("Sorry, we can't find that file. Try again?")
    
    if fileName == "0": sys.exit() #Leaves the program
    #Reading testing data
    rawTest = []
    line = data.readline()
    while line != '':
        lineArr = line.split()
        works = True
        for part in lineArr: #Looks at whether there are letters in the line
            if re.search('[a-zA-Z]', part): works = False
            
        if ('\n' not in lineArr) and len(lineArr) != 0 and works:
            rawTest.append([int(float(lineArr[0])), int(float(lineArr[1])), int(float(lineArr[2]))])
        line = data.readline()
    rawTest = scramble(rawTest)
    print ("Testing data read and scrambled.")   
    
    #Define and train the individual-point neural net
    clf1 = Classifier(
        layers=[
            Layer("Maxout", units=10, pieces=2),
            Layer("Maxout", units=10, pieces=2),
            Layer("Maxout", units=10, pieces=2),
            Layer("Softmax")],
        learning_rate=0.001,
        n_iter=25)
    clf1.fit(rawX_train1, rawY_train1)
    print ("Individual point neural net trained.")
    
    #Formatting the actual training data
    medX_train, Y_train, groupSize = formatTrain(clf1, rawX_train2) #Get it...raw, medium, well done? Ok, that was a horrid pun
    X_train = np.zeros([len(medX_train),7])
    X_train = formatFreq(X_train, medX_train)
    
    #Formatting testing data
    medTest = rc.buildTest(rawTest) #All buildTests are equivalent
    wellishTest = clf1.predict(medTest); wellTest = []
    for i in range(int(math.ceil(len(wellishTest)/groupSize))): #For all future frequency groups of the right size
        arr = []
        for j in range(groupSize):
            try:
                arr.append(wellishTest[i*int(math.ceil(len(wellishTest)/groupSize))+j][0])
            except:
                arr.append(0)
        wellTest.append(arr)
    
    test = np.zeros([len(wellTest),7])
    test = formatFreq(test, wellTest)     
    print ("Testing data formatted")

    #Define and train the frequency-group random forest
    clf2 = RandomForestClassifier(n_estimators=300)
    clf2 = clf2.fit(X_train, Y_train)    
    print ("Frequency group random forest trained")
    
    #Reading frequency groups to file
    good = False
    while good == False:
        fileName2 = raw_input("What would you like to call the file containing the frequency groups? \n(Must be .txt) ")
        fileName2 = fileName2.strip()
        try:
            freqGroups = open(fileName2, 'w')
            good = True
        except:
            print ("The file name contains illegal characters such as '/'. Try again?")    
            
    counter = 1
    for group in test:
        freqGroups.write(str(counter))
        freqGroups.write(str(group))
        freqGroups.write("\n\n")
        counter += 1
    
    #Read results to file
    Y_test = clf2.predict(test)
    Y_test = numConvert(Y_test)
    #results = open("Actual results.txt", 'w')
    #for i in range(math.ceil(len(Y_test)/5)):
        #try:
            #results.write("{}\t{}\t{}\t{}\t{}".format(Y_test[5*i], Y_test[5*i+1], Y_test[5*i+2], Y_test[5*i+3], Y_test[5*i+4]))
            #results.write("\n")
            #if (i%(math.ceil(len(Y_test)/(5*groupSize))) == (math.ceil(len(Y_test)/(5*groupSize)-1))): results.write("\n")
        #except:
            #break
        
    print Y_test
    
main()
