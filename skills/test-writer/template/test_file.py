import pytest
from [module] import [function_or_class]


# --- Happy path ---

def test_[function]_[scenario]_[expected]():
    # Arrange
    [setup state]

    # Act
    result = [function]([args])

    # Assert
    assert result == [expected]


# --- Error path ---

def test_[function]_raises_on_[condition]():
    with pytest.raises([ExceptionType], match="[message fragment]"):
        [function]([bad_args])


# --- Edge cases ---

@pytest.mark.parametrize("input,expected", [
    ([case_1_input], [case_1_expected]),
    ([case_2_input], [case_2_expected]),
])
def test_[function]_parametrized(input, expected):
    assert [function](input) == expected
