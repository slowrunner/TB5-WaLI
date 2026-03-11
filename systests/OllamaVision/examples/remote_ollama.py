#!/bin/env python3



import time
import os
import io
from PIL import Image
from ollama import Client

# Configuration
REMOTE_SERVER_IP = "x.0.0.x"  # Replace with your actual server IP
MODEL_NAME = 'qwen3-vl:8b' # not bad but takes 220s for "What do you see?"
# MODEL_NAME = 'llama3.2-vision:11b' # not very good 
IMAGE_PATH = '../images/dave.jpg'
PROMPT = "Describe the robot in this image."
RESIZE_DIM = (448, 448)

# Initialize the remote client
client = Client(host=f"http://{REMOTE_SERVER_IP}:11434")

def get_image_bytes(path):
    """Resizes image on the Pi and returns raw bytes to send over the wire."""
    with Image.open(path) as img:
        # Resize to 448x448 to keep the network transfer fast
        img = img.resize(RESIZE_DIM, Image.Resampling.LANCZOS)
        
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='JPEG')
        return byte_arr.getvalue()  # Return raw bytes

def run_profile():
    print(f"--- Remote Robot Vision Profiling ---")
    print(f"Shipping image from Pi to Server at {REMOTE_SERVER_IP}")
    print("-" * 45)
    
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: {IMAGE_PATH} not found on the Raspberry Pi.")
        return

    # 1. Prepare image data (This stays on the Pi for now)
    img_bytes = get_image_bytes(IMAGE_PATH)
    
    # 2. Complete Response Timing
    print("[Stage 1: Complete Response]")
    start_complete = time.time()
    # Sending img_bytes inside the list actually uploads the data to the server
    full_res = client.generate(model=MODEL_NAME, prompt=PROMPT, images=[img_bytes], stream=False)
    print(f"Total Complete Query Time: {time.time() - start_complete:.2f}s")
    print(full_res['response'])
    print("-" * 20)

    # 3. Chunked Response Timing
    print("\n[Stage 2: Chunked Timing]")
    print(f"{'Chunked Word':<15} | {'Time (s)':<10}")
    print("-" * 28)
    
    start_stream = time.time()
    stream = client.generate(model=MODEL_NAME, prompt=PROMPT, images=[img_bytes], stream=True)
    
    for chunk in stream:
        word = chunk['response']
        current_time = time.time() - start_stream
        clean_word = word.replace('\n', ' ').strip()
        if clean_word:
            print(f"{clean_word[:14]:<15} | {current_time:.2f}")

if __name__ == "__main__":
    run_profile()
