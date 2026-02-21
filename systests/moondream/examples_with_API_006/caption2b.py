#!/bin/env python3



import moondream as md
from PIL import Image
import time
import inspect

print("Using moondream-2b model with moondream 0.0.6 Python API")
# Start timer
start_time = time.time()

# Load the model file
# print(inspect.signature(md.vl))

# THIS ONLY WORKS FOR Moondream 0.0.6 (later requires moondream-station)

model = md.vl(model = "../models/moondream-2b-int8.mf")

# Load the image file

image = Image.open("../images/how-to-be-a-people-person.jpg")
model_done_time = time.time()
print(f"Model Load Time: {model_done_time - start_time:.2f} seconds")

# Encode the image

encoded_image = model.encode_image(image)
encode_done_time = time.time()
print(f"Image Load and Encode Time: {encode_done_time - model_done_time:.2f} seconds")

# Caption and stream the image
print("Short Caption")
caption_start_time = time.time()
caption = model.caption(image, length="short")["caption"]
caption_done_time = time.time()
print(f"Caption: {caption} in {caption_done_time - caption_start_time:.2f} seconds")


# With streaming
print("Short Caption - w/chuncking")
caption_start_time = time.time()
for chunk in model.caption(image, length="short", stream=True)["caption"]:
    caption_next_word_time = time.time()
    # print(chunk, end="", flush=True)
    print(f"{chunk:10}  :at {caption_next_word_time - caption_start_time:.2f} seconds")

