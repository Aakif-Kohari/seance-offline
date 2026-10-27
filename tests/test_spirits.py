import pytest

from seance.spirits import all_spirits, get_spirit, spirit_keys


def test_there_are_enough_spirits():
    assert len(all_spirits()) >= 5


def test_keys_are_unique():
    keys = spirit_keys()
    assert len(keys) == len(set(keys))


@pytest.mark.parametrize('spirit', all_spirits(), ids=lambda s: s.key)
def test_every_spirit_is_complete(spirit):
    for name in ('key', 'name', 'born', 'made_by', 'status', 'voice', 'offering', 'greeting', 'epitaph'):
        assert getattr(spirit, name).strip(), name
    assert len(spirit.facts) >= 4
    assert all(fact.strip() for fact in spirit.facts)


def test_get_spirit_roundtrip():
    assert get_spirit('cobol').name == 'COBOL'


def test_unknown_spirit_raises():
    with pytest.raises(KeyError):
        get_spirit('klingon')
