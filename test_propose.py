import pytest
from hypothesis import given, strategies as st
from propose import propose_optimizations

def test_threshold_includes_topic():
    result = propose_optimizations({"temas": {"demoras": 6}}, threshold=5)
    assert len(result) == 1
    assert result[0]["tema"] == "demoras"
    assert result[0]["validacion_humana_requerida"] is True

def test_below_threshold_returns_empty():
    assert propose_optimizations({"temas": {"demoras": 4}}, threshold=5) == []

@given(st.dictionaries(st.sampled_from(["demoras","congestion","ocupacion","seguridad","informacion","otro"]),
                       st.integers(min_value=0, max_value=100), max_size=6))
def test_output_is_always_a_list(temas):
    result = propose_optimizations({"temas": temas}, threshold=5)
    assert isinstance(result, list)
    assert all("propuesta" in item for item in result)

@given(st.integers(min_value=0, max_value=100))
def test_threshold_boundary(count):
    result = propose_optimizations({"temas": {"demoras": count}}, threshold=5)
    assert (len(result) == 1) == (count >= 5)
