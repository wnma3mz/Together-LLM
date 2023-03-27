## Deployment App

### Quantification

First, to reduce the resource consumption of model reasoning. We need to quantify it. Of course, you can skip this step and use the GPU version if you have enough video memory (See folder `llama`). And you can skip the second step.

In fact, [llamacpp-for-kobold](https://github.com/LostRuins/llamacpp-for-kobold) is based on [llama.cpp](https://github.com/ggerganov/llama.cpp). Therefore, llamacpp-for-kobold could be used directly.

```bash
# Compile 
make

# Convert Model
python3 convert-pth-to-ggml.py models/7B/ 1

# Quantize the model
python3 quantize.py 7B
```

### C and Python

Secondly, to abstract the model interface for Python to call. Based on the [llamacpp-for-kobold](https://github.com/LostRuins/llamacpp-for-kobold) project, some minor changes have been made.

I changed it a little bit:

- Added the function prompt_tokenize
- Avoid counting prompt repeatedly during multiple rounds of conversation

```bash
# Compile DLL
make 

# Start Flask API
python3 api.py
```

### Visualization

The final step is to develop the visual interface using gradio. See `app_chatbox.py`

```bash
# Start App Web Service
python3 app_chatbox.py
```

### TODO

- [ ] Detailed Step
- [ ] CPU and GPU Deployment

### Reference

- https://github.com/facebookresearch/llama

- https://github.com/ggerganov/llama.cpp

- https://github.com/LostRuins/llamacpp-for-kobold

