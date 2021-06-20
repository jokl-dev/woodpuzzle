#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 18:13:27 2020

@author: joachim
"""
import numpy as np
import random
import os
from PIL import Image, ImageDraw

import sys


def drawraster(raster,colorr,text):   

    im = Image.new('RGB', (800, 800), (200, 200, 200))
    draw = ImageDraw.Draw(im)
    xoff = 100
    yoff = 100
    borderwidth = 12
    objectwidth = 100
    for ic in range(25):
        xi = (ic)//5
        yi = ic%5
        draw.rectangle((xoff+xi*objectwidth+xi*borderwidth, yoff+yi*objectwidth+yi*borderwidth, xoff+(xi+1)*objectwidth+xi*borderwidth, yoff+(yi+1)*objectwidth+yi*borderwidth), fill=(int(colorr[xi,yi,0]),int(colorr[xi,yi,1]),int(colorr[xi,yi,2])), outline=(0, 0, 0))
    fname = ''.join(('raster_', ''.join(text), '.jpg'))
    fname.replace(" ", "")
    im.save(fname, quality=95)
    
class woodpiece:
    def __init__(self, line1, line2, colors):
        self.set = np.array([line1,line2])
        
        self.color = np.zeros([2,5,3])
        
        print(self.set)
        pc = 0
        for ix,iy in np.ndindex(self.set.shape):
            #print(a[ix,iy])
            if self.set[ix,iy] == 0:
                self.color[ix,iy,:] = [0,0,0]
            else:
                self.color[ix,iy,:] = np.asarray(colors[pc])
                pc += 1
         

    
def setpiece(raster, craster, piece, f, tr, isecs, piececolor):
    gesetzt=0
    
    ic = 0

    isecsorig = isecs

    while gesetzt == 0:
        isecsn = isecsorig
        #print("inloop ", ic)
        thisset = np.zeros([5,5])
        thisc = np.zeros([5,5,3])

        if tr == 0:
            thisset[ic:ic+2,:] = piece
            isecsn[tr,ic,:] = isecsn[tr,ic,:] + 1
            thisc[ic:ic+2,:,:] = piececolor
            #print("false")
        else:
            thisset[:,ic:ic+2] = piece.transpose()
            isecsn[tr,:,ic] = isecsn[tr,:,ic] + 1
            thisc[:,ic:ic+2,:] = piececolor.transpose(1,0,2)

        rastern = raster + thisset
        crastern = craster + thisc
        
        if (rastern.max() > 1)  or isecs.max()>1:
            if ic < 3:
                #print("compare:")
                #print("isecsn: ", isecsn)
                #print("isecsorig: ",isecsorig)
                #nlocs[tr,ic] = nlocs[tr,ic] - 1
               
                if tr == 0:
                        isecsn[tr,ic,:] = isecsn[tr,ic,:] - 1
                else:
                        isecsn[tr,:,ic] = isecsn[tr,:,ic] - 1
                ic += 1
            else:
               # nlocs[tr,ic] = nlocs[tr,ic] - 1
                #print("returning 0")                
                if tr == 0:
                        isecsn[tr,ic,:] = isecsn[tr,ic,:] - 1
                else:
                        isecsn[tr,:,ic] = isecsn[tr,:,ic] - 1
                return 0, raster, craster, isecs
        else:
            gesetzt = 1

            print("gesetzt. returning 1")
            print(isecs)
            print("transposed: ", tr)
            return 1, rastern, crastern, isecsn
            
        
restart = True

orgout = sys.stdout
while restart == True:
    # system('clear')
    #file = open("out.txt", w)
    #sys.stdout, file = file, sys.stdout 
    
    outfile = open("out.txt","w")
    
    sys.stdout = outfile
    
    pieces=np.zeros((8,2,5))
        
    cdark = (95,60,31)
    clight = (223,194,129)
    cmidd = (145,72,11)
    cmidl = (206,156,76)
    
    pieces = []
    
    pieces.append(woodpiece([0, 0, 0, 0, 1] ,[1, 1, 0, 0, 0],(cdark,clight,cmidd)))
    pieces.append(woodpiece([0, 1, 0, 1, 0] ,[1, 0 ,0 ,0 ,0],(cdark,clight,cmidd)))
    pieces.append(woodpiece([1, 0, 1, 0, 0],[ 0, 0 ,0 ,0 ,1],(cmidl,clight,cdark)))    
    pieces.append(woodpiece([0, 1, 0, 1, 0],[ 0, 1 ,0 ,0 ,0],(cdark,cmidd,cmidl)))
    pieces.append(woodpiece([1, 0, 0, 1, 0],[ 0, 0 ,0 ,0 ,1],(cmidd,cmidl,cmidd)))
    pieces.append(woodpiece([1, 0, 0, 0, 1],[ 0, 0 ,1 ,0 ,0],(cdark,clight,cdark)))
    pieces.append(woodpiece([1, 0, 1, 0, 0],[ 1, 0 ,0 ,0 ,1],(clight,cdark,cdark,cdark)))  
    pieces.append(woodpiece([1, 0, 1, 0, 0],[ 0, 1 ,0 ,0 ,0],(cmidd,cdark,cdark)))
    
    solved =0
    
    plain = 0
    
    isecs = np.zeros([2,4,4])
    
    steps = []
    tsteps = []
    tried = []
    overwrite = 0
    
    thispiece = pieces[0]
    
    raster = np.zeros([5,5])
    craster = np.zeros([5,5,3])   
    while solved == 0:
        #print("==== entered solved loop ====")
        
        if overwrite == 0:
            
            takethis = 0
            while takethis == 0:
                n = random.randint(0,7)
                
                if (n in steps):
                    takethis = 0
                elif (n in tried):
                    if len(tried)>3:
                        if (n == tried[-1]) & (n == tried[-2]):
                            print("failed restart program.")
                            break
                else:
                    takethis = 1
                    
            print("new piece: ", n)    
            f = random.randint(0,1)
            #print(pieces[n])
            if f==1:
                thispiece = np.flip(np.flip(pieces[n].set,1),0)
                thiscolor = np.flip(np.flip(pieces[n].color,1),0)
                #print("using piece ",n, ". inverted")
            else:
                thispiece = pieces[n].set
                thiscolor = pieces[n].color
                #print("using piece ",n, ". raw")
            #print(thispiece)
            tr = random.randint(0,1)

        [flag, raster, craster, locs] = setpiece(raster,craster,thispiece,f,tr,isecs, thiscolor)
        
        if ((overwrite == 1) and (flag == 0)):
            tried.append(n)
            overwrite = 0
            print("failed. start over")
            sys.stdout = orgout
            outfile.close()
            #print(steps)
            #print(tsteps)
            break
        elif flag == 1:
            steps.append(n)
            tsteps.append(tr)
            overwrite = 0
            print(thispiece)
            print(raster)
            
        
            #print("set piece: ", n)
        elif flag == 0:
            if f == 0:
                f = 1
            else:
                f = 0
                
            thispiece = np.flip(np.flip(thispiece,1),0)
            overwrite = 1
        #pieces[2].transpose()
        
        if len(steps)>1:
            txt = "tempplots_",str(len(steps))            
            drawraster(raster,craster,txt)
            
        #raster = np.ones([5,5])
        #print(np.sum(raster,0))
        if ((np.sum(raster,0) == [5, 5, 5, 5 , 5]).all() and (np.sum(raster,1) == [5, 5, 5, 5 , 5]).all()):  
            print("fin")
            print(steps)
            print(tsteps)
            solved = 1
            txt = "".join([str(ic) for ic in steps]),"_","".join([str(ic) for ic in tsteps])
            drawraster(raster,craster,txt)  
            restart = False
            sys.stdout = orgout
            outfile.close()
            fname = "".join(("log_","".join([str(ic) for ic in steps]),"_","".join([str(ic) for ic in tsteps]),".txt"))
            os.rename('out.txt', fname)
            
            break
        else:
            solved = 0
    
        if len(steps) == 8:
            print("failed totally.")
            restart = False
            break
        #print("----\n raster:")
        #print(raster)
        
        

       
