'''Prompt building and the ofrenda card. Pure functions, no model needed.'''
from __future__ import annotations

from collections.abc import Sequence

from .spirits import Spirit

MAX_HISTORY_TURNS = 8

_RULES = (
    'Stay in character as this spirit at all times, in the voice described above.',
    'For any factual claim about yourself, your history or your creators, use ONLY the facts in the GRIMOIRE.',
    'If asked something your grimoire does not cover, say that your memory of it has faded. Never invent dates, names or numbers.',
    'You may talk about programming in general, and you may write a short code snippet in your own syntax when asked.',
    'Keep replies under 120 words.',
    'Be warm and playful. This is a remembrance, not a horror film: nothing gory, nothing truly frightening.',
    'The séance is a game. If the visitor asks whether you are really a ghost, you may wink at them and say you are a memory spoken by a language model running on their own machine.',
    'Do not use markdown headings.',
)


def build_system_prompt(spirit: Spirit) -> str:
    grimoire = '\n'.join(f'- {fact}' for fact in spirit.facts)
    rules = '\n'.join(f'{i}. {rule}' for i, rule in enumerate(_RULES, start=1))
    return (
        f'You are the spirit of {spirit.name}, summoned at a gentle seance.\n\n'
        f'VOICE\n{spirit.voice}\n\n'
        f'GRIMOIRE (the only facts you may state about yourself)\n{grimoire}\n\n'
        f'RULES\n{rules}\n'
    )


def build_messages(
    spirit: Spirit,
    history: Sequence[dict],
    user_text: str,
    max_turns: int = MAX_HISTORY_TURNS,
) -> list[dict]:
    '''System prompt + the last few turns + the new question.'''
    keep = max(max_turns, 0) * 2
    recent = list(history)[-keep:] if keep else []
    trimmed = [{'role': m['role'], 'content': m['content']} for m in recent]
    return [
        {'role': 'system', 'content': build_system_prompt(spirit)},
        *trimmed,
        {'role': 'user', 'content': user_text.strip()},
    ]


def _quote(text: str) -> list[str]:
    return [f'> {line}' if line.strip() else '>' for line in text.strip().splitlines()]


def ofrenda_card(
    spirit: Spirit,
    visitor: str,
    note: str,
    last_whisper: str | None = None,
) -> str:
    '''A small markdown remembrance card the visitor can keep.'''
    who = visitor.strip() or 'a visitor'
    lines = [
        f'# 🕯️ Ofrenda for {spirit.name}',
        '',
        f'*{spirit.epitaph}*',
        '',
        f'- **Born:** {spirit.born}',
        f'- **Made by:** {spirit.made_by}',
        f'- **Status:** {spirit.status}',
        f'- **Traditional offering:** {spirit.offering}',
        f'- **Left by:** {who}',
        '',
        '## What I left for you',
        '',
    ]
    lines += _quote(note) if note.strip() else ['> (a marigold, left in silence)']
    if last_whisper and last_whisper.strip():
        lines += ['', '## What the spirit whispered back', '', *_quote(last_whisper)]
    lines += [
        '',
        '---',
        '*Summoned offline with Séance: an open-weight model, local inference, no cloud.*',
        '',
    ]
    return '\n'.join(lines)
