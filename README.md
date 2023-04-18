# AMM

The AI model manager.

# Use it

```sh

# Initialize a new project
amm init

# Probe an existing directory to build a map file
amm probe

# Install a model from Civitai
amm install https://civitai.com/models/7240/meinamix

# Install a model to a specific place
amm install https://civitai.com/models/7240/meinamix ./models/meinamix

# Install a Lora from Civitai, and automatically pair it with previews
amm install https://civitai.com/models/13213

# Install a model from Hugging Face
amm install https://huggingface.co/THUDM/chatglm-6b/blob/main/pytorch_model-00001-of-00008.bin

# Download a model by name
amm install bloom

# Install from an existing amm.json
amm install
amm install -r non-default-named.amm.json

```

# License
MIT
