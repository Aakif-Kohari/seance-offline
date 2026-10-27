'''Séance: Streamlit front end. Run with:  streamlit run app.py'''
from __future__ import annotations

import streamlit as st

from seance import llm
from seance.prompt import build_messages, ofrenda_card
from seance.spirits import all_spirits, get_spirit

st.set_page_config(page_title='Séance: offline spirit board', page_icon='🕯️')

if 'chats' not in st.session_state:
    st.session_state.chats = {}

spirits = all_spirits()

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.header('The circle')
    key = st.selectbox(
        'Who do you wish to summon?',
        [s.key for s in spirits],
        format_func=lambda k: get_spirit(k).name,
    )
    model = st.text_input(
        'Local model',
        value=llm.DEFAULT_MODEL,
        help='Any model you have pulled into Ollama. Default: Gemma 4 (E4B).',
    )
    temperature = st.slider('Restlessness (temperature)', 0.0, 1.5, 0.8, 0.1)

    status = llm.check_ollama(model)
    if not status.reachable:
        st.error('Ollama is not answering. Start it, then refresh this page.')
        st.code('ollama serve', language='bash')
    elif not status.model_ready:
        st.warning(f'The model {model} has not been pulled yet.')
        st.code(f'ollama pull {model}', language='bash')
    else:
        st.success(f'The circle is closed. {model} is listening, fully offline.')

    if st.button('Dismiss the spirit (clear chat)'):
        st.session_state.chats[key] = []
        st.rerun()

spirit = get_spirit(key)
history = st.session_state.chats.setdefault(key, [])

# ------------------------------------------------------------------ main
st.title('🕯️ Séance')
st.caption(
    'An offline spirit board for dead (and undead) programming languages. '
    'Runs on a local open-weight model: no cloud, no API key, no data leaves this machine.'
)

st.subheader(spirit.name)
st.markdown(f'**Born:** {spirit.born}  \n**Made by:** {spirit.made_by}  \n**Status:** {spirit.status}')
with st.expander('The grimoire: what this spirit is allowed to remember'):
    for fact in spirit.facts:
        st.markdown(f'- {fact}')

with st.chat_message('assistant', avatar='🕯️'):
    st.write(spirit.greeting)
for msg in history:
    avatar = '🕯️' if msg['role'] == 'assistant' else None
    with st.chat_message(msg['role'], avatar=avatar):
        st.write(msg['content'])

ready = status.reachable and status.model_ready
prompt = st.chat_input(
    'Ask the spirit something...' if ready else 'The circle is not closed yet (see the sidebar)',
    disabled=not ready,
)

if prompt:
    messages = build_messages(spirit, history, prompt)
    with st.chat_message('user'):
        st.write(prompt)
    with st.chat_message('assistant', avatar='🕯️'):
        try:
            reply = st.write_stream(llm.stream_reply(messages, model=model, temperature=temperature))
        except Exception as exc:  # the spirit slipped away mid-sentence
            st.error(f'The spirit slipped away: {exc}')
            reply = None
    if reply:
        history.append({'role': 'user', 'content': prompt})
        history.append({'role': 'assistant', 'content': reply})

# --------------------------------------------------------------- ofrenda
st.divider()
st.subheader('🌼 Leave an ofrenda')
st.caption(
    'On Día de los Muertos, an ofrenda holds the things a person loved. '
    f'Leave something for {spirit.name}: the first program it taught you, a bug you will never forget.'
)
visitor = st.text_input('Your name (optional)')
note = st.text_area(f'What do you leave for {spirit.name}?')
last = next((m['content'] for m in reversed(history) if m['role'] == 'assistant'), None)
st.download_button(
    'Download the ofrenda card',
    data=ofrenda_card(spirit, visitor, note, last),
    file_name=f'ofrenda-{spirit.key}.md',
    mime='text/markdown',
)
