from seance.prompt import build_messages, build_system_prompt, ofrenda_card
from seance.spirits import all_spirits, get_spirit


def test_system_prompt_has_name_voice_and_every_fact():
    spirit = get_spirit('pascal')
    prompt = build_system_prompt(spirit)
    assert spirit.name in prompt
    assert spirit.voice in prompt
    for fact in spirit.facts:
        assert fact in prompt


def test_system_prompt_forbids_inventing_facts():
    prompt = build_system_prompt(get_spirit('cobol'))
    assert 'faded' in prompt
    assert 'ONLY the facts' in prompt


def test_messages_shape_and_whitespace():
    msgs = build_messages(get_spirit('basic'), [], '  hello  ')
    assert [m['role'] for m in msgs] == ['system', 'user']
    assert msgs[-1]['content'] == 'hello'


def test_history_is_trimmed_to_recent_turns():
    history = []
    for i in range(20):
        history.append({'role': 'user', 'content': f'q{i}'})
        history.append({'role': 'assistant', 'content': f'a{i}'})
    msgs = build_messages(get_spirit('basic'), history, 'now', max_turns=2)
    assert len(msgs) == 6  # system + 4 history + new question
    assert msgs[1]['content'] == 'q18'


def test_history_extra_keys_are_dropped():
    history = [{'role': 'user', 'content': 'hi', 'ts': 123}]
    msgs = build_messages(get_spirit('basic'), history, 'again')
    assert set(msgs[1]) == {'role', 'content'}


def test_ofrenda_card_contains_the_remembrance():
    spirit = get_spirit('flash')
    card = spirit_card = ofrenda_card(spirit, 'Aakif', 'my first animation\nwith two lines', 'Loading...')
    assert spirit.name in card
    assert 'Aakif' in card
    assert '> my first animation' in card
    assert '> with two lines' in card
    assert '> Loading...' in card
    assert spirit_card == card


def test_ofrenda_card_handles_silence():
    card = ofrenda_card(get_spirit('algol'), '', '   ')
    assert 'a visitor' in card
    assert 'marigold' in card
    assert 'whispered back' not in card


def test_every_spirit_can_make_a_card():
    for spirit in all_spirits():
        assert spirit.epitaph in ofrenda_card(spirit, 'x', 'y')
