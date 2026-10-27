# 🕯️ Séance

**An offline spirit board for dead (and undead) programming languages.**

Summon COBOL, Fortran, ALGOL 60, Pascal, BASIC or Flash, ask them anything, and then leave an *ofrenda* for the language that taught you to code. Everything runs on your own machine with an open-weight model (Gemma 4 through Ollama). No cloud, no API key, and the lights can be off and the Wi-Fi unplugged.

Built for the **Hacktoberfest Open-Source AI Challenge, Week 4: Ghost in the Machine**.

## Why this exists

Halloween asks for something spooky. Día de los Muertos asks us to remember. Programming languages are a strange kind of dead: ALGOL is gone but lives inside every language you use, Flash was switched off in 2020 and is being kept alive by volunteers, and COBOL refuses to die at all. Séance lets you sit down with them for a few minutes.

## How it works

1. **Pick a spirit** in the sidebar.
2. **Ask it things.** Replies stream from a local Gemma model, in the spirit’s own voice.
3. **Leave an ofrenda.** Write what that language meant to you and download a small markdown remembrance card.

### How the spirits stay honest

Small local models love to invent history. So every spirit has a hand-written **grimoire** of verified facts (`seance/spirits.py`). The system prompt tells the model it may state facts about itself **only** from that grimoire, and to say its memory has *faded* about anything else. You can open the grimoire in the app and check the spirit against it.

The grimoire is written by hand and kept short on purpose. Please double-check anything you plan to cite, and open an issue if you spot a mistake.

## Run it

You need Python 3.10+ and [Ollama](https://ollama.com/download) 0.22 or newer (Gemma 4 support).

```bash
# 1. Pull the model once (needs internet this one time; use gemma4:e2b on small machines)
ollama pull gemma4:e4b

# 2. Get the code
git clone https://github.com/Aakif-Kohari/seance-offline.git
cd seance-offline

# 3. Install and run
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

After step 1 you can disconnect from the internet. Nothing else needs it.

If the sidebar says Ollama is not answering, start it with `ollama serve`. If it says the model has not been pulled, run the `ollama pull` command shown there.

### Settings

| Variable | Default | What it does |
| --- | --- | --- |
| `SEANCE_MODEL` | `gemma4:e4b` | Any model you have pulled into Ollama |
| `SEANCE_NUM_CTX` | `8192` | Context window passed to the model |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Where your Ollama server lives |

Swapping the model is a one-line change, which is the whole point of open weights: try `gemma4:e2b`, `gemma4:26b`, or any other model Ollama can run.

## Tests

```bash
pytest
```

The tests cover the grimoire, the prompt builder, the ofrenda card and the Ollama helpers. They need no model and no network.

## Project layout

```
app.py               Streamlit interface
seance/spirits.py    The grimoire: facts, voice and ofrenda details per spirit
seance/prompt.py     System prompt, message trimming, ofrenda card (pure functions)
seance/llm.py        Local Ollama client: health check and streaming
tests/               pytest suite
```

## Why open models

- **It works with the lights off.** After one model download, the whole séance runs offline.
- **Your remembrance stays yours.** What you leave on an ofrenda never touches a server you do not control.
- **It cannot disappear.** A hosted API can change, reprice or shut down, which is exactly what happened to Flash. A model on your disk keeps working.
- **You can change the spirit.** Swap the model, edit the grimoire, add a language. The voice and the facts are plain text in this repo.

## Limitations

- A small local model can still slip, even with a grimoire. Treat the spirits as theatre grounded in facts, not as a reference.
- Only six spirits so far. Adding one is a single entry in `seance/spirits.py`.
- Quality and speed depend on your hardware and which Gemma 4 size you choose.

## Adding a spirit

Copy any entry in `seance/spirits.py`, fill in verified facts, a voice, an offering, a greeting and an epitaph, and run `pytest`. The tests check that every spirit is complete.

## License

MIT. See [LICENSE](LICENSE).
