
import argparse
import json
import sox

import charapinlib
import shutil

def main_json(args):

    with open(args.songfile,"r") as fin:

        song = json.loads(fin.read())

    
    subelem = []
    for channel in song["channels"]:
        subelem.append( charapinlib.genChannel(channel,bpm=song["bpm"],repeat=args.repeat))
    
    
    finalName= None
    if len(subelem)>1:

        # mix all
        tmpfile = charapinlib.randomFileName()
        combiner = sox.combine.Combiner()
        combiner.build(subelem,tmpfile,combine_type="mix")
        
        finalName= tmpfile
    else:
        finalName= subelem[0]

    if not args.noplay:
        charapinlib.play(finalName)
    
    if args.write:
        shutil.copy(finalName,args.write)

    # clean WORK
    charapinlib.cleanWORK()

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("songfile", help="songfile (json)")
    parser.add_argument("-p","--noplay", action="store_true",default=False ,help="do not play song in the end.")
    parser.add_argument("-r","--repeat", type=int ,default = 1 ,help="repeat song")
    parser.add_argument("-w","--write", type=str ,help="write song as wav")
    #parser.add_argument("--pitchmf", type=int,help="play song in the end")

    charapinlib.makeFolders() 

    args = parser.parse_args()
    
    if ".json" in args.songfile:
        main_json(args)

