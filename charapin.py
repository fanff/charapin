
import argparse
import json
import sox

import charapinlib


def main_json(args):

    with open(args.songfile,"r") as fin:

        song = json.loads(fin.read())

    
    subelem = []
    for channel in song["channels"]:
        subelem.append( charapinlib.genChannel(channel,bpm=song["bpm"],repeat=3))
    
    
    finalName= None
    if len(subelem)>1:

        # mix all
        tmpfile = charapinlib.randomFileName()
        combiner = sox.combine.Combiner()
        combiner.build(subelem,tmpfile,combine_type="mix")
        
        finalName= tmpfile
    else:
        finalName= subelem[0]

    if args.play:
        charapinlib.play(finalName)
    
    # clean WORK
    charapinlib.cleanWORK()

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("songfile", help="songfile")
    parser.add_argument("-p","--play", action="store_true",help="play song in the end")
    #parser.add_argument("--pitchmf", type=int,help="play song in the end")

    charapinlib.makeFolders() 

    args = parser.parse_args()
    
    if ".json" in args.songfile:
        main_json(args)

