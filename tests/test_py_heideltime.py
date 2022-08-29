from py_heideltime.py_heideltime import remove_emoji


def test_remove_emoji():
    """Assert that the emojis are being removed."""
    text = "text with emoji 😀"
    expected_result = "text with emoji "

    result = remove_emoji(text)

    assert result == expected_result
