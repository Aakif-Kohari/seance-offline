from types import SimpleNamespace

from seance.llm import has_model, model_names


def test_model_names_from_objects():
    resp = SimpleNamespace(models=[SimpleNamespace(model='gemma4:e4b'), SimpleNamespace(model='llama3:latest')])
    assert model_names(resp) == ['gemma4:e4b', 'llama3:latest']


def test_model_names_from_dicts():
    resp = {'models': [{'name': 'gemma4:e4b'}, {'model': 'x:1'}]}
    assert model_names(resp) == ['gemma4:e4b', 'x:1']


def test_model_names_empty():
    assert model_names(SimpleNamespace(models=[])) == []
    assert model_names({}) == []


def test_has_model_exact_match():
    assert has_model('gemma4:e4b', ['gemma4:e4b'])


def test_has_model_latest_alias():
    assert has_model('gemma4', ['gemma4:latest'])


def test_has_model_missing_tag():
    assert not has_model('gemma4:e4b', ['gemma4:latest'])
    assert not has_model('gemma4:e2b', ['gemma4:e4b'])
