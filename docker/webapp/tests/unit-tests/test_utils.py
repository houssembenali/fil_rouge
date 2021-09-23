import src.utils as utils

def test_index_validity():
    assert not utils.is_index_valid(-2)
    assert not utils.is_index_valid(0)
    assert utils.is_index_valid(5)