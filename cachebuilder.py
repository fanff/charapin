import logging

from test import genWord
if __name__=="__main__":
    logging.basicConfig(level=logging.ERROR)
    words = ["a","o","chat","rat","un","lapinou","petit"]
    
    scale1 = ["C1","D1","E1","F1","G1","A1","B1"]
    scale2 = ["C2","D2","E2","F2","G2","A2","B2"]
    scale3 = ["C3","D3","E3","F3","G3","A3","B3"]
    scale4 = ["C4","D4","E4","F4","G4","A4","B4"]
    scale5 = ["C5","D5","E5","F5","G5","A5","B5"]
    scale6 = ["C6","D6","E6","F6","G6","A6","B6"]
    

    allnotes = []
    allnotes+=scale4
    allnotes+=scale5

    duration = [.5,1,2]
    
    
    todocount = (len(duration)*len(allnotes)*len(words))
    print "to do: %s"%todocount
    quit()
    i=0
    for w in words:
        for n in allnotes:
            for d in duration:
                i+=1
                print "%s / %s"%(i,todocount)
                genWord(w,n,d)

