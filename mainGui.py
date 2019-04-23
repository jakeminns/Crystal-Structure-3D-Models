# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:51:38 2017

@author: Jake
"""
from mpl_toolkits.mplot3d import Axes3D

from os.path import expanduser#import the os
import tkinter
from pathlib import Path
import numbers    
import cif_extractor as cifEx
import cifToScad as cifScad
from tkinter.filedialog import askopenfilename
import getpass
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class MainGui:
    
    def __init__(self,master, path):
        self.master=master
        master.title("CIF to STL")
        self.cifInfoTable =[]
        framebg = "white"
        labelbg = "white"
        buttonbg = "white"
        
        framepadx = 10
        framepady = 5

        #Bonds
        self.bondsList = []

        #Atom Positions
        self.atomPositionTable =[]
        
        #File Path Box
        self.file_path_text = tkinter.StringVar()
        self.fileFrame = tkinter.LabelFrame(master, text='Load CIF',padx=5, pady=5,bg=framebg)

        self.file_path = tkinter.Entry(self.fileFrame )
        #Go to Path Button
        self.load_button = tkinter.Button(self.fileFrame , text="Load", command=lambda: self.loadCif(), bg=buttonbg)
        self.run_button = tkinter.Button(self.fileFrame , text="Run", command=lambda: self.buildModel(), bg=buttonbg)

        


        #Cell Parameter Info
        self.cellLabelFrame = tkinter.LabelFrame(master, text='Cell Parameters', bg=framebg)
        self.cellParamLabel_a = tkinter.Label( self.cellLabelFrame, text="a:",bg=labelbg)
        self.cellParamLabel_b = tkinter.Label( self.cellLabelFrame, text="b:",bg=labelbg)
        self.cellParamLabel_c = tkinter.Label( self.cellLabelFrame, text="c:",bg=labelbg)
        self.cellParamLabel_alpha = tkinter.Label( self.cellLabelFrame, text="alpha:",bg=labelbg)
        self.cellParamLabel_beta = tkinter.Label( self.cellLabelFrame, text="beta:",bg=labelbg)
        self.cellParamLabel_gamma = tkinter.Label( self.cellLabelFrame, text="gamma:",bg=labelbg)
        self.cellParamLabel_volume = tkinter.Label( self.cellLabelFrame, text="volume:",bg=labelbg)
        
        self.cellParamEntry_a = tkinter.Entry (self.cellLabelFrame)
        self.cellParamEntry_b = tkinter.Entry( self.cellLabelFrame)
        self.cellParamEntry_c = tkinter.Entry( self.cellLabelFrame)
        self.cellParamEntry_alpha = tkinter.Entry( self.cellLabelFrame)
        self.cellParamEntry_beta = tkinter.Entry( self.cellLabelFrame)
        self.cellParamEntry_gamma = tkinter.Entry( self.cellLabelFrame)
        self.cellParamEntry_volume = tkinter.Entry( self.cellLabelFrame)
        
        self.cellParamEntryText_a = tkinter.StringVar()
        self.cellParamEntryText_b = tkinter.StringVar()
        self.cellParamEntryText_c = tkinter.StringVar()
        self.cellParamEntryText_alpha = tkinter.StringVar()
        self.cellParamEntryText_beta = tkinter.StringVar()
        self.cellParamEntryText_gamma = tkinter.StringVar()
        self.cellParamEntryText_volume = tkinter.StringVar()
        
        #Model Parameters
        self.modelParametersFrame = tkinter.LabelFrame(master, text='Model Parameters',padx=5, pady=5,bg=framebg)

        self.modelScaler = tkinter.Label(self.modelParametersFrame,text="Scaler:",bg=labelbg)
        self.modelScalerEntry = tkinter.Entry(self.modelParametersFrame)
        self.modelScalerEntryText = tkinter.StringVar()
        
        self.modelScalerEntryText.set("1")        
        self.modelScalerEntry.insert(0,self.modelScalerEntryText.get())
        
        self.modelSphereSize = tkinter.Label(self.modelParametersFrame,text="Sphere Size:",bg=labelbg)
        self.modelSphereSizeEntry = tkinter.Entry(self.modelParametersFrame)
        self.modelSphereSizeEntryText = tkinter.StringVar()
        self.modelSphereSizeEntryText.set("0.1")        
        self.modelSphereSizeEntry.insert(0,self.modelSphereSizeEntryText.get())
        self.modelBondWidth = tkinter.Label(self.modelParametersFrame,text="Bond Width:",bg=labelbg)
        self.modelBondWidthEntry = tkinter.Entry(self.modelParametersFrame)
        self.modelBondWidthEntryText = tkinter.StringVar()
        self.modelBondWidthEntryText.set("0.1")        
        self.modelBondWidthEntry.insert(0,self.modelBondWidthEntryText.get())       
        self.bondsOnVar = tkinter.IntVar()


        self.modelBoundariesFrame = tkinter.LabelFrame(master, text='Model Boundaries',padx=5, pady=5,bg=framebg)

        self.modelXMax = tkinter.Label(self.modelBoundariesFrame,text="x(max):",bg=labelbg)
        self.modelXMaxEntry = tkinter.Entry(self.modelBoundariesFrame)
        self.modelXMaxEntryText = tkinter.StringVar()
        self.modelXMaxEntryText.set("1")        
        self.modelXMaxEntry.insert(0,self.modelXMaxEntryText.get())       
        self.modelXMin = tkinter.Label(self.modelBoundariesFrame,text="x(min):",bg=labelbg)
        self.modelXMinEntry = tkinter.Entry(self.modelBoundariesFrame)
        self.modelXMinEntryText = tkinter.StringVar()
        self.modelXMinEntryText.set("0")        
        self.modelXMinEntry.insert(0,self.modelXMinEntryText.get())  

        self.modelYMax = tkinter.Label(self.modelBoundariesFrame,text="y(max):",bg=labelbg)
        self.modelYMaxEntry = tkinter.Entry(self.modelBoundariesFrame)
        self.modelYMaxEntryText = tkinter.StringVar()
        self.modelYMaxEntryText.set("1")        
        self.modelYMaxEntry.insert(0,self.modelYMaxEntryText.get())       
        self.modelYMin = tkinter.Label(self.modelBoundariesFrame,text="y(min):",bg=labelbg)
        self.modelYMinEntry = tkinter.Entry(self.modelBoundariesFrame)
        self.modelYMinEntryText = tkinter.StringVar()
        self.modelYMinEntryText.set("0")        
        self.modelYMinEntry.insert(0,self.modelYMinEntryText.get())
        
        self.modelZMax = tkinter.Label(self.modelBoundariesFrame,text="z(max):",bg=labelbg)
        self.modelZMaxEntry = tkinter.Entry(self.modelBoundariesFrame)
        self.modelZMaxEntryText = tkinter.StringVar()
        self.modelZMaxEntryText.set("1")        
        self.modelZMaxEntry.insert(0,self.modelZMaxEntryText.get())       
        self.modelZMin = tkinter.Label(self.modelBoundariesFrame,text="z(min):",bg=labelbg)
        self.modelZMinEntry = tkinter.Entry(self.modelBoundariesFrame)
        self.modelZMinEntryText = tkinter.StringVar()
        self.modelZMinEntryText.set("0")        
        self.modelZMinEntry.insert(0,self.modelZMinEntryText.get())
        
        #Atom List
        self.atomListFrame = tkinter.LabelFrame(master, text='Atom Positions',padx=5, pady=5,bg=framebg)
        self.atomLabelHead = tkinter.Label(self.atomListFrame,text="Atom",bg=labelbg)
        self.atomXLabelHead = tkinter.Label(self.atomListFrame,text="x",bg=labelbg)
        self.atomYLabelHead = tkinter.Label(self.atomListFrame,text="y",bg=labelbg)
        self.atomZLabelHead = tkinter.Label(self.atomListFrame,text="z",bg=labelbg)

        self.atomLabel = tkinter.Listbox(self.atomListFrame, selectmode=tkinter.SINGLE)
        self.atomXLabel = tkinter.Listbox(self.atomListFrame, selectmode=tkinter.SINGLE)   
        self.atomYLabel = tkinter.Listbox(self.atomListFrame, selectmode=tkinter.SINGLE)   
        self.atomZLabel = tkinter.Listbox(self.atomListFrame, selectmode=tkinter.SINGLE)   
        
        #Bonds
        self.bondsFrame = tkinter.LabelFrame(master, text='Bonds',padx=5, pady=5,bg=framebg)
        self.addBondsFrame = tkinter.LabelFrame(self.bondsFrame, text='Add Bonds',padx=5, pady=5,bg=framebg)

        self.modelBondsOnCheck= tkinter.Checkbutton(self.addBondsFrame, text="Bonds",variable=self.bondsOnVar,bg=labelbg)

        self.bondAtom1Label = tkinter.Label(self.addBondsFrame, text="Atom 1:",bg=labelbg)
        self.bondAtom2Label = tkinter.Label(self.addBondsFrame, text="Atom 2:",bg=labelbg)
        self.bondAtom1Entry = tkinter.Entry(self.addBondsFrame)
        self.bondAtom1Text = tkinter.StringVar()
        self.bondAtom2Entry = tkinter.Entry(self.addBondsFrame)
        self.bondAtom2Text = tkinter.StringVar()

        self.bondAtomDisLabel = tkinter.Label(self.addBondsFrame, text="Distance:",bg=labelbg)
        self.bondAtomDisEntry = tkinter.Entry(self.addBondsFrame)
        self.bondAtomDisText = tkinter.StringVar()
      
        self.bondAddButton = tkinter.Button(self.addBondsFrame, text="add", command=lambda: self.addBond(), bg=buttonbg)
        
        self.bondLabelList = tkinter.Listbox(self.bondsFrame, selectmode=tkinter.SINGLE)
        self.bondLabelList.bind("<Double-1>",self.deleteBondItem)
      
        
        

                       
        #Layout
        
        self.fileFrame.grid(row=0,column=0,sticky="W,E,N,S",padx=framepadx, pady=framepady, )
        self.load_button.grid(row=0, column=0)
        self.file_path.grid(row=0,column=1,columnspan=4,sticky="W,E,N,S")
        self.run_button.grid(row=0,column=5)
        
        self.cellLabelFrame.grid(row=1, column=0,sticky="W,E,N,S",padx=framepadx, pady=framepady)

        self.cellParamLabel_a.grid(row=0,column=0,sticky="E")
        self.cellParamEntry_a.grid(row=0,column=1)
        
        self.cellParamLabel_b.grid(row=0,column=2,sticky="E")
        self.cellParamEntry_b.grid(row=0,column=3)
        
        self.cellParamLabel_c.grid(row=0,column=4,sticky="E")
        self.cellParamEntry_c.grid(row=0,column=5)
        
        self.cellParamLabel_alpha.grid(row=1,column=0,sticky="E")
        self.cellParamEntry_alpha.grid(row=1,column=1)
        
        self.cellParamLabel_beta.grid(row=1,column=2,sticky="E")
        self.cellParamEntry_beta.grid(row=1,column=3)
        
        self.cellParamLabel_gamma.grid(row=1,column=4,sticky="E")
        self.cellParamEntry_gamma.grid(row=1,column=5)
        
        self.cellParamLabel_volume.grid(row=2,column=0,sticky="E")
        self.cellParamEntry_volume.grid(row=2,column=1)
        
        self.modelParametersFrame.grid(row=2,column=0,sticky="W,E,N,S",padx=framepadx, pady=framepady)
        self.modelScaler.grid(row=0,column =0,sticky="E")
        self.modelScalerEntry.grid(row=0,column =1)
        
        self.modelSphereSize.grid(row=1,column=0,sticky="E")
        self.modelSphereSizeEntry.grid(row=1,column = 1)

        self.modelBondWidth.grid(row=1,column = 2,sticky="E")
        self.modelBondWidthEntry.grid(row=1, column = 3)
        
        self.modelBoundariesFrame.grid(row=3,column=0,sticky="W,E,N,S",padx=framepadx, pady=framepady)
        self.modelXMax.grid(row=0,column=0,sticky="E")
        self.modelXMaxEntry.grid(row=0,column=1)
        self.modelXMin.grid(row=0,column=2,sticky="E")
        self.modelXMinEntry.grid(row=0,column=3)
        
        self.modelYMax.grid(row=1,column=0,sticky="E")
        self.modelYMaxEntry.grid(row=1,column=1)
        self.modelYMin.grid(row=1,column=2,sticky="E")
        self.modelYMinEntry.grid(row=1,column=3)
        
        self.modelZMax.grid(row=2,column=0,sticky="E")
        self.modelZMaxEntry.grid(row=2,column=1)
        self.modelZMin.grid(row=2,column=2,sticky="E")
        self.modelZMinEntry.grid(row=2,column=3)
        
        self.atomListFrame.grid(row=4,column=0,sticky="W,E,N,S",padx=framepadx, pady=framepady)
        self.atomLabelHead.grid(row=0,column=0)
        self.atomXLabelHead.grid(row=0,column=1)
        self.atomYLabelHead.grid(row=0,column=2)
        self.atomZLabelHead.grid(row=0,column=3)

        self.atomLabel.grid(row=1,column=0)
        self.atomXLabel.grid(row=1,column=1)
        self.atomYLabel.grid(row=1,column=2)
        self.atomZLabel.grid(row=1,column=3)

        self.bondsFrame.grid(row=5,column=0,sticky="W,E,N,S",padx=framepadx, pady=framepady)
        self.addBondsFrame.grid(row=0, column = 0,sticky="W")
        self.modelBondsOnCheck.grid(row=0,column=0)

        self.bondAtom1Label.grid(row=1,column=0,sticky="E")
        self.bondAtom1Entry.grid(row=1,column=1)
        
        self.bondAtom2Label.grid(row=2,column=0,sticky="E")
        self.bondAtom2Entry.grid(row=2,column=1)
 
        self.bondAtomDisLabel.grid(row=3,column=0,sticky="E")
        self.bondAtomDisEntry.grid(row=3,column=1)  
        self.bondAddButton.grid(row=4, column =0,columnspan=2,sticky="W,E,N,S")
        self.bondLabelList.grid(row=0,column = 2,sticky="W,E,N,S")
        
            
    def deleteBondItem(self, index):
        
        contentIndex = self.bondLabelList.curselection()        
        del self.bondsList[contentIndex[0]]                
        self.refreshBondList()
                 
    def addBond(self):
        print("DGD")
        tempBond = []
        tempBond.append(self.bondAtom1Entry.get())
        tempBond.append(self.bondAtom2Entry.get())
        tempBond.append(self.bondAtomDisEntry.get())
        
        self.bondsList.append(tempBond)

        self.refreshBondList()

    def refreshBondList(self):
        self.bondLabelList.delete(0, tkinter.END)  

        for i in self.bondsList:                
            label = str(i[0] + "    " + i[1] + "    " + i[2])
                #labelIn = labelIn[len(label):len(labelIn)]
            self.bondLabelList.insert(tkinter.END, label)    
        
    def fillCifInfoEntries(self):
        
        cellParams = cifScad.buildLatticeParams(self.cifInfoTable)

        
        self.cellParamEntryText_a.set(cellParams[0])
        self.cellParamEntryText_b.set(cellParams[1])
        self.cellParamEntryText_c.set(cellParams[2])
        self.cellParamEntryText_alpha.set(cellParams[3])
        self.cellParamEntryText_beta.set(cellParams[4])
        self.cellParamEntryText_gamma.set(cellParams[5])
        self.cellParamEntryText_volume.set(cellParams[6])

        self.cellParamEntry_a.delete(0,tkinter.END)
        self.cellParamEntry_b.delete(0,tkinter.END)
        self.cellParamEntry_c.delete(0,tkinter.END)
        self.cellParamEntry_alpha.delete(0,tkinter.END)
        self.cellParamEntry_beta.delete(0,tkinter.END)
        self.cellParamEntry_gamma.delete(0,tkinter.END)
        self.cellParamEntry_volume.delete(0,tkinter.END)
        
        self.cellParamEntry_a.insert(0,self.cellParamEntryText_a.get())
        self.cellParamEntry_b.insert(0,self.cellParamEntryText_b.get())
        self.cellParamEntry_c.insert(0,self.cellParamEntryText_c.get())
        self.cellParamEntry_alpha.insert(0,self.cellParamEntryText_alpha.get())
        self.cellParamEntry_beta.insert(0,self.cellParamEntryText_beta.get())
        self.cellParamEntry_gamma.insert(0,self.cellParamEntryText_gamma.get())
        self.cellParamEntry_volume.insert(0,self.cellParamEntryText_volume.get())  
        self.atomPositionTable = cifScad.buildPositionsTable(self.cifInfoTable)
        self.displayAtomInfo()
        
    def displayAtomInfo(self):
            
        self.atomPositionTable = cifScad.buildPositionsTable(self.cifInfoTable)
        
        self.atomLabel.delete(0, tkinter.END)
        self.atomXLabel.delete(0, tkinter.END)
        self.atomYLabel.delete(0, tkinter.END)   
        self.atomZLabel.delete(0, tkinter.END)  

        for i in self.atomPositionTable:
                
            label = str(i[0])
                #labelIn = labelIn[len(label):len(labelIn)]
            self.atomLabel.insert(tkinter.END, label)
            xlabel = str(i[1])
            self.atomXLabel.insert(tkinter.END, xlabel)                
            xlabel = str(i[2])
            self.atomYLabel.insert(tkinter.END, xlabel)                
            ylabel = str(i[3])
            self.atomZLabel.insert(tkinter.END, ylabel)

    def buildModel(self):
        
        a = self.cellParamEntry_a.get()
        b = self.cellParamEntry_b.get()
        c= self.cellParamEntry_c.get()
        alpha = self.cellParamEntry_alpha.get()
        beta = self.cellParamEntry_beta.get()
        gamma = self.cellParamEntry_gamma.get()
        volume = self.cellParamEntry_volume.get()
        
        cellParams = []
        
        cellParams.append(a)
        cellParams.append(b)
        cellParams.append(c)
        cellParams.append(alpha)
        cellParams.append(beta)
        cellParams.append(gamma)
        cellParams.append(volume)
        
        xmax = self.modelXMaxEntry.get()
        xmin = self.modelXMinEntry.get()
        ymax = self.modelYMaxEntry.get()
        ymin = self.modelYMinEntry.get()
        zmax = self.modelZMaxEntry.get()
        zmin = self.modelZMinEntry.get()
        
        boundaries = []
        boundaries.append(float(xmax))
        boundaries.append(float(xmin))
        boundaries.append(float(ymax))
        boundaries.append(float(ymin))
        boundaries.append(float(zmax))
        boundaries.append(float(zmin))
        
        sphereSize = self.modelSphereSizeEntry.get()
        scaler = self.modelScalerEntry.get()
        bondsOn = self.bondsOnVar.get()
        bondWidth = self.modelBondWidthEntry.get()
        cifScad.buildOpenScad(self.cifInfoTable, cellParams,  scaler,sphereSize,bondsOn, bondWidth, boundaries, self.bondsList,False,scaler*10,10,[True,0.8,0.1,0.1])
        
    def loadCif(self):
        user = getpass.getuser()

        fileName = askopenfilename(initialdir='C:/Users/%s' % user,title = "Select CIF",filetypes = (("cif files","*.cif"),("all files","*.*")))

        if fileName:
            print("FILE: ",fileName)
            self.cifInfoTable=cifEx.openFileBuildCifInfo(fileName)
            self.file_path_text.set(fileName)
            self.file_path.delete(0,tkinter.END)
            self.file_path.insert(0,self.file_path_text.get())
            self.fillCifInfoEntries()
            print(self.cifInfoTable)
            try:
                pass
            except:                     # <- naked except is a bad idea
                print("Open Source File", "Failed to read file\n'%s'" % fileName)
            return



root = tkinter.Tk()

root.configure(background='white')
the_gui = MainGui(root, Path.home())


root.mainloop()