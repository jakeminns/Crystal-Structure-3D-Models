# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:50:31 2017

@author: Jake
"""
import re
import math
import cif_extractor


   
def splitSymmetryXYZ(symComp):
    output = [[],[],[]]
    
    z = 0
    comp = ""
    for i in range(len(symComp)):
        if i >= len(symComp)-1: #final z componant
            if symComp[i]!=" ":
                comp += symComp[i]
            output[z].append(comp)
            continue
        elif symComp[i] == ',': #look for , char and temp string comp to output
            output[z].append(comp)
            comp=""
            z+=1
            continue
        else:
            if symComp[i]!=" ":
                comp += symComp[i]
                
    return output
                 
def buildSymVectors(limit): # 0 = aPos, 1 = aNeg, 2 = bPos, 3 =  bNeg, 4 =cPos, 5 =cNeg
    symmetryOp = []
    cNeg = limit[5]
    cPos = limit[4]
    for c in range(math.floor((limit[5])),math.ceil((limit[4]))+1):
        for b in range(math.floor(limit[3]),math.ceil(limit[2])+1):
            for a in range(math.floor(limit[1]),math.ceil(limit[0])+1):
                symmetryOp.append(splitSymmetryXYZ("x+"+str(a)+", y+"+str(b)+", z+"+str(c)))
                symmetryOp.append(splitSymmetryXYZ("x-"+str(a)+", y+"+str(b)+", z+"+str(c)))
                symmetryOp.append(splitSymmetryXYZ("x+"+str(a)+", y-"+str(b)+", z+"+str(c)))
                symmetryOp.append(splitSymmetryXYZ("x-"+str(a)+", y-"+str(b)+", z+"+str(c)))
                symmetryOp.append(splitSymmetryXYZ("x+"+str(a)+", y-"+str(b)+", z-"+str(c)))
                symmetryOp.append(splitSymmetryXYZ("x-"+str(a)+", y+"+str(b)+", z-"+str(c)))
    return symmetryOp
    
def buildPositionsTable(dataTable):
    
    label = cif_extractor.getCifInfo("_atom_site_type_symbol",dataTable)
    x = cif_extractor.getCifInfo("_atom_site_fract_x",dataTable)
    y =cif_extractor.getCifInfo("_atom_site_fract_y",dataTable)
    z =cif_extractor.getCifInfo("_atom_site_fract_z",dataTable)
    label = cif_extractor.getCifInfo("_atom_site_label",dataTable)

    positions = []
    
    for i in range(len(label)):
        if i!=0:
            pos = []
            pos.append(label[i])
            pos.append(x[i])
            pos.append(y[i])
            pos.append(z[i])
            #pos.append(label[i])
            positions.append(pos)
            
    return positions

def buildAndApplySymmetryOpperations(positions, symmetryOpp):
    NewPositions=[]
    for sym in range(len(symmetryOpp)):
        for pos in range(len(positions)):
            tempPos =[]
            tempPos.append(positions[pos][0])
            tempPos.append(applyOpperation(positions[pos],symmetryOpp[sym][0],"x"))
            tempPos.append(applyOpperation(positions[pos],symmetryOpp[sym][1],"y"))
            tempPos.append(applyOpperation(positions[pos],symmetryOpp[sym][2],"z"))
            #tempPos.append((positions[pos][4]))
            NewPositions.append(tempPos)

        print(NewPositions)

    return NewPositions

def removeBrackets(input):
    
    input = str(input).replace("(","")
    input = str(input).replace(")","")
    
    return input
def applyOpperation(position, symmetryOpp, variable):
    a = symmetryOpp[0].replace("x",str(removeBrackets(position[1])))
    a = a.replace("y",str(removeBrackets(position[2])))
    a = a.replace("z",str(removeBrackets(position[3])))

    return round(eval(a),3)

def buildSymmetryPosFromCif(dataTable):
    symm = cif_extractor.getCifInfo("_space_group_symop_operation_xyz",dataTable)
    if symm is None:
        symm = cif_extractor.getCifInfo("_symmetry_equiv_pos_as_xyz",dataTable)
        
        # if there is no sym operator statement in cif add just xyz
        if symm is None:
            symm = ['_symmetry_equiv_pos_as_xyz','x, y, z']
            print("WARNING: Cif has no symm operator statement")

    symmetryPos = []

    for i in range(len(symm)):
        if i !=0:
            symmetryPos.append(splitSymmetryXYZ(symm[i]))
    
    return symmetryPos
def buildLatticeParams(dataTable):
    
    a = cif_extractor.getCifInfo("_cell_length_a",dataTable)
    b = cif_extractor.getCifInfo("_cell_length_b",dataTable)
    c = cif_extractor.getCifInfo("_cell_length_c",dataTable)
    alpha = cif_extractor.getCifInfo("_cell_angle_alpha",dataTable)
    beta = cif_extractor.getCifInfo("_cell_angle_beta",dataTable)
    gamma = cif_extractor.getCifInfo("_cell_angle_gamma",dataTable)
    volume = cif_extractor.getCifInfo("_cell_volume",dataTable)
    ##### Add exception for if cell volume is not there
    cellParams=[]
    cellParams.append(a[1])
    cellParams.append(b[1])
    cellParams.append(c[1])
    cellParams.append(alpha[1])
    cellParams.append(beta[1])
    cellParams.append(gamma[1])
    cellParams.append(volume[1])

    return cellParams

def buildMagParams(dataTable):

    label = cif_extractor.getCifInfo("_atom_site_moment_label",dataTable)
    mag_x = cif_extractor.getCifInfo("_atom_site_moment_crystalaxis_x",dataTable)
    mag_y = cif_extractor.getCifInfo("_atom_site_moment_crystalaxis_y",dataTable)
    mag_z = cif_extractor.getCifInfo("_atom_site_moment_crystalaxis_z",dataTable)

    return (list(zip(label,mag_x,mag_y,mag_z))[1:])


def removePosBeyondLim(limit, positionTable):
    outOfBounds = False
    i=0
    posSize = len(positionTable)
    while i < posSize:
        l = 0
        outOfBounds = False
        for x in range(len(positionTable[i])-1):
            if float(positionTable[i][x+1]) > limit[l]:
                outOfBounds = True
            if float(positionTable[i][x+1]) < limit[l+1]:
                outOfBounds = True
            l+=2
        if outOfBounds:
            del positionTable[i]
            posSize-=1
        else:
            i+=1
    return positionTable

def removeDuplicatePos(positionTable):
    i = 0
    posSize = len(positionTable)-1
    while i <= posSize:
        z = 0
        while z <= posSize:
            if i == z:
                z+=1
                continue
            if float(positionTable[i][1]) == float(positionTable[z][1]):
                if float(positionTable[i][2]) == float(positionTable[z][2]):
                    if float(positionTable[i][3]) == float(positionTable[z][3]):
                        del positionTable[z]
                        posSize-=1
                    else:
                        z+=1
                else:
                    z+=1
            else:
                z+=1  
        i+=1
            
    return positionTable

def fractionalToCartesian(scaler, atomType, fracX, fracY, fracZ, cellParams, sphereSize):
    a = float(removeBrackets(cellParams[0]))
    b = float(removeBrackets(cellParams[1]))
    c= float(removeBrackets(cellParams[2]))
    Pi = 3.14159265359
    alpha = (float(removeBrackets(cellParams[3]))*Pi)/180
    beta = (float(removeBrackets(cellParams[4]))*Pi)/180
    gamma = (float(removeBrackets(cellParams[5]))*Pi)/180
    volume = (float(removeBrackets(cellParams[6])))
    x = fracX*a + fracY*b*math.cos(gamma)+fracZ*c*math.cos(beta)
    y = fracY*b*math.sin(gamma) + fracZ*((c*(math.cos(alpha)-math.cos(beta)*math.cos(gamma)))/(math.sin(gamma)))
    z = fracZ *((volume)/(a*b*math.sin(gamma)))
    
    x = x*scaler
    y = y*scaler
    z = z*scaler
    
    outputCart = []
    outputCart.append(sphereSize*atomicRadiiLookUp(atomType))
    outputCart.append(x)
    outputCart.append(y)
    outputCart.append(z)
    outputCart.append(removeOxidation(atomType))
    
    return outputCart

def atomicRadiiLookUp(atomType):
    
    if atomType == "La":
        return 8
    elif atomType == "Ir":
        return 6
    elif atomType == "Pb":
        return 3
    
    return 2

def removeOxidation(atomType):
    
    output =""
    for i in atomType:
        if i.isalpha():
            output+=i
    return output
def distanceBetweenAtoms(atom1,atom2):
    
    return (((atom2[1]-atom1[1])**2)+((atom2[2]-atom1[2])**2)+((atom2[3]-atom1[3])**2))**0.5

def bondDoesntExist(bonds,atom1,atom2):
    
    for i in bonds:
        if i[7]==atom1 and i[8] == atom2:
            return False
        if i[8] == atom1 and i[7] == atom2:
            return False
    
    return True#6,7
    
    
def buildBonds(atomPositions, scaler, dataTable, specifiedBonds):
    output = []
    
    numPositions = len(atomPositions)
    numSpecBonds = len(specifiedBonds)
    i =0
    bondLabel = 0
    while i < numPositions:
        z = 0
        while z < numPositions:
            if i == z:
                z+=1
                continue
            x = 0
            while x < numSpecBonds: 
                if atomPositions[i][4]==specifiedBonds[x][0] and atomPositions[z][4] == specifiedBonds[x][1]:
                    print(atomPositions[i],specifiedBonds[x])
                    tempBond = []
                    distance = distanceBetweenAtoms(atomPositions[i],atomPositions[z])
                    if distance<scaler*float(specifiedBonds[x][2]):
                        if bondDoesntExist(output, atomPositions[i][5],atomPositions[z][5]):
                            xi = atomPositions[z][1]-atomPositions[i][1]
                            yj = atomPositions[z][2]-atomPositions[i][2]
                            zk = atomPositions[z][3]-atomPositions[i][3]
        
                            alpha,beta,gamma = openScadAngleConvert(distance,xi,yj,zk)
                                    
                            tempBond.append(round(atomPositions[i][1],3))
                            tempBond.append(round(atomPositions[i][2],3)) 
                            tempBond.append(round(atomPositions[i][3],3))
                            tempBond.append(round(alpha,3))
                            tempBond.append(round(beta,3))
                            tempBond.append(round(gamma,3))
                            tempBond.append(round(distance,3))
                            tempBond.append(atomPositions[i][5])
                            tempBond.append(atomPositions[z][5])
                            print(tempBond)
                            output.append(tempBond)
                x+=1
            z+=1
        i+=1
    return output


def openScadAngleConvert(distance,xi,yj,zk):
    alpha = 0
    Pi = math.pi
        
    if distance==0:
        beta = (180/Pi)*math.acos(zk)
        print("distance=0",beta)
    elif xi>=0:
        beta = (180/Pi)*math.acos(zk/distance)
        print("distance88=0",beta,zk,distance)

    else:
        beta = -(180/Pi)*math.acos(zk/distance)
        print("distance=9990",beta,zk,distance,xi)

    if xi ==0:
        #if xi == 0 then yj/xi = infintity , atan(x) curve tends to -90 and 90 as x tends to -infintiy and +infintiy
        
        gamma = 90.0 *(yj/abs(yj))
        print("xi=0",gamma,yj, atomPositions[z][2],atomPositions[i][2],xi,zk)
        print(atomPositions[z],atomPositions[i])
    else:
        print("xi!=0")
        gamma = (180/Pi)*math.atan(yj/xi)

    return alpha,beta,gamma
        

def removeDuplicateBonds(bonds):
    i = 0
    bondSize = len(bonds)-1
    while i <= bondSize:
        z = 0
        while z <= bondSize:
         
            if i == z:
                z+=1
                continue
            if bonds[i][0] == bonds[z][0]:
                if bonds[i][1] == bonds[z][1]:
                    if bonds[i][2] == bonds[z][2]:
                        if bonds[i][4] == bonds[z][4]:
                            if bonds[i][5] == bonds[z][5]:
                                if bonds[i][6] == bonds[z][6]:
                                    del bonds[z]
                                    bondSize-=1
                                else:
                                    z+=1
                            else:
                                z+=1
                        else:
                            z+=1
                    else:
                        z+=1
                else:
                    z+=1
            else:
                z+=1
            
        i+=1
            
    return bonds   

def labelAtoms(atomPositions):
    
    label = 0
    for i in atomPositions:
        i.append(label)
        label+=1

    return atomPositions
    
def generateSupports(scaler,positionTable, sphereSize, numSupports):
    
    
    support=[]
    while(len(support)<float(numSupports)):
        supportTemp =[]
        store = 100000000000
        index = 0
        indexTrack = 0
        for i in positionTable:
            if i[3] < store:
                index = indexTrack
                store = i[3]
                
            indexTrack+=1
        print(index,len(positionTable))
        print(positionTable[index])
        supportTemp.append(positionTable[index][0])
        supportTemp.append(positionTable[index][1])
        supportTemp.append(positionTable[index][2])
        supportTemp.append(positionTable[index][3])
        support.append(supportTemp)
        del positionTable[index]
    
    return support
def writeOpenScadFile(scaler, sphereSize, outputName, positionTable, bondsOn, cellParams, specifiedBonds, dataTable, bondWidth, standOn, standHeight,numSupports,magVec):
    file = open(outputName+".scad","w")
    atomPositions = []

    if magVec[0] == True:
        magPos = buildMagParams(dataTable)

    file.write("$fn=90;"+"\n")

    for i in positionTable:
        pos=[]
        file.write("translate([")
        pos = fractionalToCartesian(scaler, i[0], i[1], i[2], i[3], cellParams,sphereSize)
        file.write(str(pos[1])+","+str(pos[2])+","+str(pos[3])+"]){"+"\n"+"sphere("+str(pos[0])+");"+"\n"+"}"+"\n")
        atomPositions.append(pos)

        if magVec[0]==True:
            for mag in magPos:
                if mag[0] == i[0]:
                    file.write("translate([")
                    xi = float(mag[1])
                    yj = float(mag[2])
                    zk = float(mag[3])
                    distance = (xi**2+yj**2+zk**2)**0.5
                    alpha,beta,gamma = openScadAngleConvert(distance,xi,yj,zk)

                    file.write(str(pos[1])+","+str(pos[2])+","+str(pos[3])+"]){"+"\n"+"rotate(a=["+str(alpha)+","+str(beta)+","+str(gamma)+"]){"+"\n")
                    file.write("cylinder("+str(magVec[1])+","+str(magVec[2])+","+str(magVec[3])+",true);}}")

                    #Arrow head calculate unit vector of mag vector and multply it by half the arrow height to find the shift in arrow head position then add to position for shifted position
                    file.write("translate([")
                    unit_x = pos[1]+((float(mag[1])/distance)*(magVec[1]/2.0))
                    unit_y = pos[2]+(float(mag[2])/distance*(magVec[1]/2.0))
                    unit_z = pos[3]+(float(mag[3])/distance*(magVec[1]/2.0))

                    file.write(str(unit_x)+","+str(unit_y)+","+str(unit_z)+"]){"+"\n"+"rotate(a=["+str(alpha)+","+str(beta)+","+str(gamma)+"]){"+"\n")
                    file.write("cylinder("+str(magVec[1]/2.0)+","+str(magVec[2]*2.0)+","+"0.0"+",false);}}")




    if bondsOn == True:
        print(len(atomPositions))
        bondPositions = labelAtoms(atomPositions)
        print("1",bondPositions)
        bondPositions = buildBonds(bondPositions,scaler,dataTable,specifiedBonds)
        print("2",bondPositions)
        bondPositions = removeDuplicateBonds(bondPositions)
        print("3",bondPositions)

        i = 0
        atomSize = len(bondPositions)
        
        while i < atomSize:
            if str(bondPositions[i][5] == "-73.142"):
                print(bondPositions[i],i)
            file.write("translate(["+str(bondPositions[i][0])+","+str(bondPositions[i][1])+","+str(bondPositions[i][2])+"]){"+"\n")
            file.write("rotate(a=["+str(bondPositions[i][3])+","+str(bondPositions[i][4])+","+str(bondPositions[i][5])+"]){"+"\n")
            file.write("cylinder("+str(bondPositions[i][6])+","+bondWidth+","+bondWidth+",false);}}"+"\n")
            i+=1
            
    if standOn==True:
        standFile = open(outputName+"_stand.scad","w")
        standFile.write("$fn=90;"+"\n")
        supports = []
        
        standFile.write("module support(x,y,z,sphereSize,height){difference(x,y,z,sphereSize,height){difference(x,y,z,sphereSize,height){translate([x,y,z])sphere(sphereSize*1.1);cubeSize = 2*(sphereSize*1.1);translate([x,y,z+sphereSize*0.7])cube([cubeSize,cubeSize,cubeSize],true);}translate([x,y,z])sphere(sphereSize);}supportHeight=(z-sphereSize)+height;translate([x,y,z+(-((supportHeight*0.5)+sphereSize))])cylinder(supportHeight,sphereSize*0.3,sphereSize*0.3,true);}")
        
        supports = generateSupports(scaler,atomPositions,sphereSize,numSupports)
        for i in supports:
            standFile.write("support("+str(i[1])+","+str(i[2])+","+str(i[3])+","+str(i[0])+", 1);")
        print(supports)
        
def displayList(list):
    x=0
    for i in list:
        print(x, ": ",i)
        x+=1
        

def buildOpenScad(dataTable, cellParams,sphereSize, scaler, bondsOn, bondWidth, boundaries, specifiedBonds,standOn,standHeight,numSupports,mag):
    

    #dataTable=cif_extractor.openFileBuildCifInfo("test.cif")
    #print("DATA",dataTable)
    positionTable = buildPositionsTable(dataTable)
    positionTable = (buildAndApplySymmetryOpperations(positionTable,buildSymmetryPosFromCif(dataTable)))
    positionTable = (buildAndApplySymmetryOpperations(positionTable,buildSymVectors(boundaries)))
    positionTable = removePosBeyondLim(boundaries, positionTable)
    positionTable = removeDuplicatePos(positionTable)
    
    print(specifiedBonds)
    if bondsOn==1:
        bondsOn = True
    else:
        bondsOn = False
    print("BONDS", bondsOn)
    writeOpenScadFile(float(sphereSize),float(scaler),"out",positionTable,bondsOn,cellParams, specifiedBonds,dataTable, bondWidth,standOn,standHeight,numSupports,mag)
