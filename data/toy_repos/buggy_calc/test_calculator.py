from calculator import add, divide

def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero_contract():
    assert divide(1, 0) is None
