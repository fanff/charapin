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
    # ROOT NOTE = B4
        
    pitchshift = notetofreq.relativePitch(pitch,"B4")
    #print pitch,pitchshift
    tmpfile = randomFileName()
    
    espeakPitch = 50
    ttscmd = ["espeak","-s","300","-v","fr","-p",str(espeakPitch),"-w",tmpfile,txt ]
    subprocess.check_output( ttscmd) 
    

    tmpfile2=randomFileName()
    tfm = sox.Transformer()
    tfm.pitch(pitchshift)
    tfm.build(tmpfile,tmpfile2)
    
    return tmpfile2    





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
    if os.path.isfile(os.path.join(CACHEDIR,key+".wav")):
        return os.path.join(CACHEDIR,key+".wav")
    else:
        return False

def storeWord(key,word):
    """
    word is a filename
    key is a key
    """
    shutil.copy(word,os.path.join(CACHEDIR,key+".wav"))
    return os.path.join(CACHEDIR,key+".wav") 


def genChannel(wordList,bpm=160.0,repeat=1):

    gens = []
    for word in wordList:
        txt,pitch,length = word
        w = genWord(txt,pitch,length,bpm)
        gens.append(w)
    
    #concat
    tmpfile = randomFileName()
    combiner = sox.combine.Combiner()

    repeated = []
    for i in range(repeat):
        repeated+=gens

    combiner.build(repeated,tmpfile,combine_type="concatenate")

    return tmpfile

def genWord(txt,pitch,length,bpm=160.0):
    """

    length in note duration. 1 = black
    espeak -p 50 -w wav.wav lol

    """
    
    def makekey():
        key= (txt,pitch,length,bpm)

        key = [str(_) for _ in key]
        key="SEP".join(key)
        
        return base64.b64encode(key)

    
    key = makekey()
    word = getWord(key)
    if word!=False:
        #print "found word "+key

        return word
    else:
        #print "building word "+key
        

        blackduration = 1.0/(bpm/60.0) # the more the slower
        
        pitched = findPitchOn(txt,pitch)
        timed = adjustTimeOn(pitched,length*blackduration)
        # 
        word = storeWord(key,timed)


        
        return word

def cleanWORK():
    shutil.rmtree(WORKDIR)
    os.mkdir(WORKDIR)

def makeFolders():
    try:
        os.mkdir(WORKDIR)
    except:
        pass

    try:
        os.mkdir(CACHEDIR)
    except:
        pass


WORKDIR = "/dev/shm/WORK"
CACHEDIR = "./CACHE"

if __name__=="__main__":
    logging.basicConfig(level=logging.ERROR)
    makeFolders() 
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

    # clean WORK
    cleanWORK()
    play(outfile)
    

