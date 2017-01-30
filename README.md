

# Dependancies

sox 

    pip install --user sox

espeak as command line



# tests bash


Pitching :


     sox wav.wav -C 192 pitc.wav pitch -300  && sox pitc.wav -n stat -freq 

# run a charapin server

    docker run -d --name charapin -p 5527:27017 mongo 


    docker stop charapin
    
    # suppression avec le volume mongo
    docker rm charapin -v  

