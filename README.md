# Description
This script automatically suggests new titles for untitled notes in an Obsidian vault by analyzing their content with the Ollama API. It also updates references to these notes in other documents, ensuring consistency across your notes. Additionally, it offers an option to delete notes directly and regenerate a note title for a note (while giving feedback on what you didn't like about the previous generation.
## Getting Started
- Install Ollama: Ensure you have the Ollama package installed. If not, install it via pip:
    - `pip install ollama`
- Model Setup: Set up your Ollama model by pulling the necessary model configuration for note title generation.
    - `ollama pull mistral` in this case (but pull whatever model and then update the Ollama API call)
- Run the Script: Execute main.py to start the process:
    - `python main.py`
