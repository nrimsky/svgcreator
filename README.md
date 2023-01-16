# SVG creator

Playing with OpenAI's image generation API to generate images and then convert them to SVG vector art

## How to use

Create a file called `.env` and include your OpenAI API key there (see `.env.example`)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Examples

Prompt: "Professional illustration of friendly elephant reading a book"

AI image (`png`):
![AI Image](examples/example.png)

Vector art (`svg`):
![Vector art](example/example.svg)

## Experimentation in jupyter

```bash
jupyter notebook
```