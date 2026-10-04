# Zoro

Zoro is a simple one-page AI chat app in Python, built with Streamlit and Claude. It has streaming replies, a few personalities, and a butterfly logo.

## Setup

1. Install Python 3.10 or newer.
2. Open a terminal in this folder and install the packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and paste in your Anthropic API key (get one at console.anthropic.com).
4. Run the app:

   ```bash
   streamlit run app.py
   ```

It opens in your browser at http://localhost:8501.

## Run it online

You can also host Zoro for free on Streamlit Community Cloud (share.streamlit.io). Connect this repo, set `app.py` as the main file, and add your key under Secrets:

```
ANTHROPIC_API_KEY = "your-key-here"
```

## Project files

| File | What it does |
| --- | --- |
| `app.py` | The whole app: page, styling, and chat logic |
| `assets/logo.svg` | The butterfly logo |
| `requirements.txt` | Python packages to install |
| `.env.example` | Template for your API key |
| `.gitignore` | Keeps your real `.env` out of GitHub |

## Customize

- Rename the app by changing `APP_NAME` in `app.py`.
- Change the colors in the `STYLE` block.
- Add or edit personalities in the `PERSONALITIES` dictionary.
