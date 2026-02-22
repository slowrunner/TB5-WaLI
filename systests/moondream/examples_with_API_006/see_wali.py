#!/bin/env python3



import moondream as md
from PIL import Image
import time
import inspect

print("Using moondream-0_5b model with moondream 0.0.6 Python API")
# print("Using moondream-2b model with moondream 0.0.6 Python API")
print("Using image of Wali")

# Start timer
start_time = time.time()

# Load the model file
# print(inspect.signature(md.vl))

# THIS ONLY WORKS FOR Moondream 0.0.6 (later requires moondream-station)

model = md.vl(model = "../models/moondream-0_5b-int8.mf")
# model = md.vl(model = "../models/moondream-2b-int8.mf")

# Load the image file

image = Image.open("../images/wali.jpg")
model_done_time = time.time()
print(f"Model Load Time: {model_done_time - start_time:.2f} seconds")

# Encode the image

encoded_image = model.encode_image(image)
encode_done_time = time.time()
print(f"Image Load and Encode Time: {encode_done_time - model_done_time:.2f} seconds")

# Ask quetions about the image
print("What do you see?")
query_start_time = time.time()
answer = model.query(encoded_image, "What do you see?")["answer"]
query_done_time = time.time()
print(f"Query Time: {query_done_time - query_start_time:.2f} seconds")
print(answer)


