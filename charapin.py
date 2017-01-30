
import argparse
import json


import test
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("songfile", help="songfile")
    parser.add_argument("-p","--play", action="store_true",help="play song in the end")
    #parser.add_argument("--pitchmf", type=int,help="play song in the end")


    args = parser.parse_args()

    print test.WORKDIR
    print test.CACHEDIR
