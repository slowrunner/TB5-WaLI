# USB Speaker/Mic for TB5-WaLI

Purchased the "ROFAL Speaker with Mic"   

Initially, it was recognized but no sound out or in.  Was ready to send back,  
then thought to try 
```
alsamixer 
```
to adjust the playback and record levels.  

Voila - raising playback to 80% and record (capture) to 84%  
gave great playback and sufficient record level when I am several feet from the robot in a quiet room.  

I haven't tried it with speech recognition, but I believe it will be acceptable  
based on prior experience with pocketsphinx speech recognition on my robots.  

It registers as a P1OS chip  
and the box says "Punk Wolf USB PC Speaker" P1U-4 Computer Speaker.  

The quiescent current seems to be less than 50mA.  
The box states 3W, the manual states 5W max.
The speaker states 5v 1A on the bottom.

