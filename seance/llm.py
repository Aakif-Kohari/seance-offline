'''Thin wrapper around a local Ollama server. Nothing here touches the internet.'''
from __future__ import annotations

import os
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field

DEFAULT_MODEL = os.environ.get('SEANCE_MODEL', 'gemma4:e4b')
DEFAULT_NUM_CTX = int(os.environ.get('SEANCE_NUM_CTX', '8192'))


@dataclass
class Status:
    reachable: bool
    model_ready: bool
    available: list[str] = field(default_factory=list)
    error: str = ''


def _client(host: str | None = None):
    import ollama  # imported lazily so tests do not need Ollama installed

    return ollama.Client(host=host) if host else ollama.Client()


def model_names(resp) -> list[str]:
    '''Pull model names out of an Ollama list() response (objects or dicts).'''
    models = getattr(resp, 'models', None)
    if models is None and isinstance(resp, dict):
        models = resp.get('models')
    names: list[str] = []
    for m in models or []:
        if isinstance(m, dict):
            name = m.get('model') or m.get('name')
        else:
            name = getattr(m, 'model', None) or getattr(m, 'name', None)
        if name:
            names.append(name)
    return names


def has_model(wanted: str, names: Sequence[str]) -> bool:
    if wanted in names:
        return True
    if ':' not in wanted:
        return f'{wanted}:latest' in names
    return False


def check_ollama(model: str, host: str | None = None) -> Status:
    '''Is the local server up, and is the model pulled?'''
    try:
        resp = _client(host).list()
    except Exception as exc:  # connection refused, ollama not installed, etc.
        return Status(reachable=False, model_ready=False, error=str(exc))
    names = model_names(resp)
    return Status(reachable=True, model_ready=has_model(model, names), available=names)


def stream_reply(
    messages: Sequence[dict],
    model: str | None = None,
    temperature: float = 0.8,
    num_ctx: int = DEFAULT_NUM_CTX,
    host: str | None = None,
) -> Iterator[str]:
    '''Yield the spirit’s reply piece by piece from the local model.'''
    stream = _client(host).chat(
        model=model or DEFAULT_MODEL,
        messages=list(messages),
        stream=True,
        options={'temperature': temperature, 'num_ctx': num_ctx},
    )
    for chunk in stream:
        piece = chunk['message']['content']
        if piece:
            yield piece
