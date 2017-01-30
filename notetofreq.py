
d ="""N Note/octave     0   1   2   3   4   5   6   7
C  32.70   65.41   130.81  261.63  523.25  1046.50     2093.00     4186.01
C#  34.65   69.30   138.59  277.18  554.37  1108.73     2217.46     4434.92
D  36.71   73.42   146.83  293.66  587.33  1174.66     2349.32     4698.64
D# 38.89   77.78   155.56  311.13  622.25  1244.51     2489.02     4978.03
E 41.20   82.41   164.81  329.63  659.26  1318.51     2637.02     5274.04
F 43.65   87.31   174.61  349.23  698.46  1396.91     2793.83     5587.65
F#      46.25   92.50   185.00  369.99  739.99  1479.98     2959.96     5919.91
G 49.00   98.00   196.00  392.00  783.99  1567.98     3135.96     6271.93
G#     51.91   103.83  207.65  415.30  830.61  1661.22     3322.44     6644.88
A  55.00   110.00  220.00  440.00  880.00  1760.00     3520.00     7040.00
A#    58.27   116.54  233.08  466.16  932.33  1864.66     3729.31     7458.62
B  61.74   123.47  246.94  493.88  987.77  1975.53     3951.07     7902.13"""


notetofreq = {

}

for _id ,_ in enumerate(d.split("\n")):
    
    if _id==0:
        pass
    else :
        noteName = _.split(" ")[0].replace(" ","")

        it = 0
        for eid , e in enumerate(_.split(" ")[1:]):
            try: 
                notetofreq[noteName+str(it)] =float(e)
                it+=1
            except :
                pass

notetonotekey = { j[0]:i for i,j in enumerate( sorted(notetofreq.items(),key=lambda x : x[1] ))}

def relativePitch(note,root):
    """

    """
    return (notetonotekey[note] - notetonotekey[root] )

if __name__ == "__main__":

    from pprint import pprint

    
    pprint(notetonotekey)


        
