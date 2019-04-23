# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 18:25:11 2017

@author: Jake
"""


def buildLoopList(fileName):
    inputFile = open(fileName,'r')
    inputFile = inputFile.read()

    lininputFilees = filter(lambda x: not x.isspace(), inputFile)

    fileLines = inputFile.split('\n')
    loopArray = []
    print(len(fileLines))

    # look for new line ; pattern
    i = 0
    #loop through list
    while i < len(fileLines):
        print("siuf",fileLines[i])
        #look for new line then ; character pattern
        if fileLines[i] == '' and fileLines[i+1] == ';':
            #find the enclosing ; character and join everything between
            for x in range(i+2,len(fileLines)):
                    print("loojs",fileLines[x],fileLines[x][0])
                    if fileLines[x][0] == ';':

                        print("FOund reset",i,x,''.join(fileLines[i+2:x+1]))
                        if len(fileLines[x+1])== 1:
                            fileLines[i:x+1] = [''.join(fileLines[i+2:x+1])]
                        else:
                            fileLines[x] = fileLines[x][1:]
                            print(fileLines)
                            fileLines[i:x] = [''.join(fileLines[i+2:x])]

                        #restart looking through list for multiple newline
                        i = 0
                        break
        i+=1


    fileLines = ['loop_' if len(i) == 0 else i for i in fileLines]

    print((fileLines))
    newLoop = False
    tempLoopItem = ""
    
    lineCount = 0
    numLines = len(fileLines)
    
    while lineCount < numLines : #Loop Through Lines of file
        if newLoop == True or lineCount == numLines-1 :#Check if the previous cycle loop of the loop contained a 'loop_' keyword or it's the last line in the file
            if lineCount == numLines-1 and fileLines[lineCount]!="":
                tempLoopItem = tempLoopItem + " " + fileLines[lineCount]
            newLoop = False
            tempLoopItem = " ".join(tempLoopItem.split()) #Remove large whitespace and replace with single space
            loopArray.append(tempLoopItem) #Append loop text to loop array
            tempLoopItem = ""
        #Check if line is comment
        if(len(str(fileLines[lineCount].lstrip())))==0:
            continue
        if fileLines[lineCount][len(str(fileLines[lineCount]))-len(str(fileLines[lineCount].lstrip()))] == '#': #Is first char in the string a comment character?
            lineCount +=1
            continue
        if 'loop_' in fileLines[lineCount] or (len(str(fileLines[lineCount].lstrip())))==0: #Does the string contain the loop_ keyword?
            newLoop = True
            lineCount +=1
            continue
        tempLoopItem = tempLoopItem + " " + fileLines[lineCount]
        lineCount +=1
    
        
    return loopArray

def buildInfoList(loopArray):
    finalLoop = []
    for items in loopArray:
        splitLoopArray=[]
        newItem = ""
        i=0
        while i < len(items):

            if items[i] ==" ":
                if newItem!="":
                    splitLoopArray.append(newItem)
                    newItem =""
                if items[i+1]== "'":
                    newItem = ""
                    for x in range(i+2,len(items)):
                        if items[x] == "'":
                            splitLoopArray.append(newItem)   
                            i = x
                            print("newItem",newItem)

                            newItem =""
                            break
                        else:
                            newItem += items[x]

                else:
                    if newItem != "":
                        splitLoopArray.append(newItem)
                    newItem =""
            elif items[i] == "'":
                i -= 1
            else:
                newItem += items[i]
            i+=1
        if newItem != "":
            splitLoopArray.append(newItem)

        finalLoop.append(splitLoopArray)
                
    return finalLoop
       # print(items)
    
def sortInfoList(dataTable):
    finalTable =[]
    i =0
    
    while i < len(dataTable):
        newList = []
        if len(dataTable[i])>0:
            if len(dataTable[i][0][0])>0:
                if dataTable[i][0][0] != "_":
                    del dataTable[i][0]
        x=0
        innerLen = len(dataTable[i])
        while x < innerLen:    
            if len(dataTable[i][x])>0:                    
                if dataTable[i][x][0] == "_":
                    newList.append(dataTable[i][x])
                    innerLen-= 1
                    del dataTable[i][x]
                else:
                    x+=1
            else:
                x+=1            
        for x in range(len(dataTable[i])):
            newList.append(dataTable[i][x])
        finalTable.append(newList)
        i+=1
        
    return finalTable
    
def createInfoTable(dataTable):
        finalList = []
        outerLen = len(dataTable)
        for i in range(outerLen):
            innerLen = len(dataTable[i])
            labelCount = 0
            for x in range(innerLen):  #Count how many labels are in list
                if dataTable[i][x] !="":
                    if dataTable[i][x][0] =="_":
                        labelCount +=1
            labeledList = []
            y = 0
            while y < labelCount: #build empty list according to number of labels
                tempLabelList =[]
                labeledList.append(tempLabelList)
                y+=1
            x=0
            while x < innerLen: #go through list, with a perioiddicity of the number of labels in each list collecting the info for each label
                y = 0
                while y < labelCount or x < innerLen:
                    if y>=labelCount or x>= innerLen:
                        break
                    labeledList[y].append(dataTable[i][x])
                    x+=1
                    y+=1
                
            finalList.extend(labeledList)
        return finalList

def openFileBuildCifInfo(fileName):
    
    dataTable = buildLoopList(fileName) 
    print("1",dataTable)
    dataTable = buildInfoList(dataTable)
    print("2",dataTable)

    dataTable = sortInfoList(dataTable)
    print("3",dataTable)

    dataTable = createInfoTable(dataTable)
    print("4",dataTable)

    return dataTable
    
def getCifInfo(infoLabel, dataTable):
    
    for i in range(len(dataTable)):
        if infoLabel == dataTable[i][0]:
            return dataTable[i]
 