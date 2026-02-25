# Moondream 0.0.6 Vision Language Assistant for TB5-WaLI 

Ref: https://core-electronics.com.au/guides/raspberry-pi/getting-started-with-moondream-on-the-pi-5-human-like-computer-vision/  
(This article uses MoonDream API version 0.0.6 which includes the local model server.  Later versions require moondream-station)
 
=== create virtual environment ===

sudo apt install python3.12-venv  

python3 -m venv --system-site-packages moondream_006_venv

=== install moondream ===

ref suggests because has built in server: pip install moondream==0.0.6  

see https://pypi.org/project/moondream/  

(pip install moondream   will install version 0.2.0 Nov 25, 2025 which requires moondream-station to serve model)  

pip3 install numpy==1.26.4   (already installed)  


=== download models ===

mkdir models  

2b model:  

wget https://huggingface.co/vikhyatk/moondream2/resolve/9dddae84d54db4ac56fe37817aeaeb502ed083e2/moondream-2b-int8.mf.gz?download=true  

0.5b model:  

wget https://huggingface.co/vikhyatk/moondream2/resolve/9dddae84d54db4ac56fe37817aeaeb502ed083e2/moondream-0_5b-int8.mf.gz?download=true  

(had to mv them to clean up the names)  

gunzip *.gz  


=== Images ===

how-to-be-a-people-person.jpg 960x504 included in moondream git  
crash1.jpg                    512x512 from Ref article  
                                      wget https://core-electronics.com.au/media/wysiwyg/tutorials/Jaryd/pi-moondream/crash1.jpg  

=== Examples ===
(with 2b in name use 2b model, others use 0.5b model)

caption2b.py         short caption and short caption with chunking  
car_drivable.py      query "is car drivable?" with 0.5b model  
car_drivable2b.py    query "is car drivable?" with 2b model  
see_people.py        queries of larger than 512x512 image with 0.5b model  
see_people2b.py      queries of larger than 512x512 image with 2b model  



```
(moondream_006_venv) ubuntu@TB5WaLI:~/TB5-WaLI/systests/moondream/examples_with_API_006$ ./see_dave.py
Using moondream-0.5b model with moondream 0.0.6 Python API
Using image of Dave
Model Load Time: 7.10 seconds
Image Load and Encode Time: 35.33 seconds
What do you see?
Query Time: 18.48 seconds
 The image features a collection of electronic components, including a camera, a fan, and a fan, all attached to a wall. There is also a poster or a sheet of paper with text on it, which is partially visible in the image.


(moondream_006_venv) ubuntu@TB5WaLI:~/TB5-WaLI/systests/moondream/examples_with_API_006$ ./see_dave2b.py
Using moondream-2b model with moondream 0.0.6 Python API
Using image of Dave
Model Load Time: 22.99 seconds
Image Load and Encode Time: 66.35 seconds
What do you see?
Query Time: 47.61 seconds
 The image features a robot with a Minion head, which is a Minion character from the popular movie franchise. The robot is positioned on a white surface, and it appears to be connected to a power source. The robot is also adorned with a variety of wires, which are likely used for its various functions and components.

(moondream_006_venv) ubuntu@TB5WaLI:~/TB5-WaLI/systests/moondream/examples_with_API_006$ ./see_wali.py 
Using moondream-0_5b model with moondream 0.0.6 Python API
Using image of Wali
Model Load Time: 6.99 seconds
Image Load and Encode Time: 24.21 seconds
What do you see?
Query Time: 22.62 seconds
 The image features a large, black, dome-shaped device with a speaker and a screen. The speaker is located in the middle of the device, while the screen is positioned towards the top. The device appears to be a speaker with a dome-shaped structure, designed for audio and audio purposes.


(moondream_006_venv) ubuntu@TB5WaLI:~/TB5-WaLI/systests/moondream/examples_with_API_006$ ./see_wali2b.py 
Using moondream-2b model with moondream 0.0.6 Python API
Using image of Wali
Model Load Time: 23.69 seconds
Image Load and Encode Time: 48.03 seconds
What do you see?
Query Time: 32.87 seconds
 The image features a robot with two large eyes, sitting on a tiled floor. The robot has a black and yellow color scheme, and it appears to be a toy or a model of a robot.
```
