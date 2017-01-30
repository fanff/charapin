import sox

import os,sys,subprocess
from pprint import pprint
import uuid

import notetofreq
NTF = notetofreq.notetofreq
sNTF = sorted(NTF.items(),key=lambda x:x[1])
import base64
import logging
import argparse
import shutil

def randomFileName():
    return os.path.join(WORKDIR,str(uuid.uuid4())+".wav")


def findPitchOn(txt,pitch):
    # find good espeak pitch 
    data=[]
    for pitchshift in [50]:
        tmpfile = randomFileName()

        ttscmd = ["espeak","-s","300","-v","fr","-p",str(pitchshift),"-w",tmpfile,txt ]
        subprocess.check_output( ttscmd) 
        #pprint( sox.file_info.stat(tmpfile))
        peakf = float(sox.file_info.stat(tmpfile)["Rough   frequency"])

        dist = abs(peakf-pitch)

        data.append([pitchshift,dist,tmpfile]) 
    sortedData = sorted(data,key=lambda x: x[1])
    #pprint(sortedData)
    goodshift= sortedData[0][2]
    #Found good espeak shift  
    
    soxpitchmin, soxpitchmax = (-12.,12.) 
    soxpitchstep = (soxpitchmax - soxpitchmin)/float(PITCHMF)
    data = []
    currentStep = soxpitchmin
    while currentStep<soxpitchmax:
        tmpfile2=randomFileName()
        tfm = sox.Transformer()
        tfm.pitch(currentStep)
        tfm.build(goodshift,tmpfile2)
        peakf = float(sox.file_info.stat(tmpfile2)["Rough   frequency"])

        dist = abs(peakf-pitch)

        data.append([currentStep,dist,tmpfile2]) 
        
        currentStep+=soxpitchstep

    sortedData = sorted(data,key=lambda x: x[1])
    #pprint(sortedData)

    pprint(sortedData[0])
    goodsoxshift= sortedData[0][2]


    return goodsoxshift    



def adjustTimeOn(tmpfile,length):
    """
    length in seconds
    """
    inlen = float(sox.file_info.stat(tmpfile)["Length (seconds)"])
    
    tempoFactor = (inlen/float(length))
    
    tmpfile2 = randomFileName()
    tfm = sox.Transformer()
    tfm.tempo(tempoFactor)
    tfm.build(tmpfile,tmpfile2)
    
    return tmpfile2

def play(filename):

    if isinstance(filename,list):
        for _ in filename:
            play(_)
    elif isinstance(filename,str):
        ttscmd = ["play",filename ]
        subprocess.check_output( ttscmd) 



def getWord(key):
    """
    """
    if os.path.isfile(os.path.join("CACHE",key+".wav")):
        return os.path.join("CACHE",key+".wav")
    else:
        return False

def storeWord(key,word):
    """
    word is a filename
    key is a key
    """
    shutil.copy(word,os.path.join("CACHE",key+".wav"))
    return os.path.join("CACHE",key+".wav") 
def genWord(txt,pitch,length):
    """

    length in note duration. 1 = black
    espeak -p 50 -w wav.wav lol

    """
    
    def makekey():
        key= (txt,pitch,length,BPM,PITCHMF)

        key = [str(_) for _ in key]
        key="SEP".join(key)
        
        return base64.b64encode(key)

    
    key = makekey()
    word = getWord(key)
    if word!=False:
        print "found word "+key

        return word
    else:
        print "building word "+key
        

        blackduration = 1.0/(BPM/60.0) # the more the slower
        
        pitched = findPitchOn(txt,NTF[pitch])
        timed = adjustTimeOn(pitched,length*blackduration)
        # 
        word = storeWord(key,timed)

        # clean WORK
        cleanWORK()

        
        return word

def cleanWORK():
    shutil.rmtree(WORKDIR)
    os.mkdir(WORKDIR)

PITCHMF = 100  # The more the better the longer the slower
BPM = 160
WORKDIR = "/dev/shm/WORK"

MONGOPORT = 5517
if __name__=="__main__":
    logging.basicConfig(level=logging.ERROR)
    
    try:
        os.mkdir(WORKDIR)
    except:
        pass
    sub =[

        genWord("a","A3",1),
        genWord("a","B3",1),

        genWord("a","C4",1),
        genWord("a","D4",1),
        genWord("a","E4",1),
        genWord("a","F4",1),
        genWord("a","G4",1),
        genWord("a","A4",1),
        genWord("a","B4",1),

        genWord("a","C5",1),
        genWord("a","D5",1),
        genWord("a","E5",1),
        genWord("a","F5",1),
        genWord("a","G5",1),
        genWord("a","A5",1),
        genWord("a","B5",1),
        
        genWord("a","C6",1),

        
    ]


    minorS = [
        genWord("a","A4",1),
        genWord("a","C5",1),
        genWord("a","E5",2),
        
        genWord("a","D5",1),
        genWord("a","E5",1),
        genWord("a","A5",2),

        genWord("a","A4",1),
        genWord("a","C5",1),
        genWord("a","E5",2),
        
        genWord("a","D5",1),
        genWord("a","E5",1),
        genWord("a","A5",2),

    ]
    charapinpin = [
        
        genWord("un","G4",.5),
        genWord("chat","C5",1.5),
        
        genWord("un","G4",.5),
        genWord("rat","C5",1.5),
        
        genWord("un","G4",.5),
        genWord("petit","C5",1),
        genWord("la","B4",.5),
        genWord("pie","C5",.5),
        genWord("nous","D5",1.5),
        
        genWord("un","G4",.5),
        ##
        genWord("chat","D5",1.5),

        genWord("un","G4",.5),
        genWord("rat","D5",1.5),
        
        genWord("un","G4",.5),
        ##
        genWord("peu","D5",.5),
        genWord("ti","D5",.5),
        genWord("la","C5",.5),
        genWord("pi","D5",.5),
        genWord("nous","E5",2),
    ]
    repeat = 1
    tocombine = []

    for _ in range(repeat):
        tocombine+=sub
        tocombine+=minorS
        tocombine+=charapinpin

    combiner = sox.combine.Combiner()
    outfile = "out.wav"
    combiner.build(tocombine,outfile,combine_type="concatenate")

    play(outfile)
    

