# Gemini Coded Vision Model Script


REQUIRES:

```
python3 -m venv --system-site-packages ollama_vision_LM_venv
. activate.sh
pip3 install ollama

On Mac:
 - curl -fsSL https://ollama.com/install.sh | sh

 - ollama pull qwen3-vl:8b  (6GB)

 - test: ollama run qwen3-vl:8b

 - temporarily serve:  
   OLLAMA_HOST=0.0.0.0:11434 OLLAMA_NUM_PARALLEL=4 OLLAMA_NO_CUDA=1 ollama serve

```


To exit the venv type: ```deactivate```

To test remote access to Ollama server running on my mac (x.x.x.x)

```curl http://x.x.x.x:11434/api/tags  ```
returns:   
```
{"models":[{"name":"qwen3-vl:8b","model":"qwen3-vl:8b","modified_at":"2026-02-24T20:00:35.422624443-05:00","size":6140415879,"digest":"901cae73216286ea8c5aba8b46d307ff7188f737285ec500c795a12f05225d28","details":{"parent_model":"","format":"gguf","family":"qwen3vl","families":["qwen3vl"],"parameter_size":"8.8B","quantization_level":"Q4_K_M"}}]}
```
