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

