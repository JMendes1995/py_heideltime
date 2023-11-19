from py_heideltime.utils import process_text


def test_process_text_emojis():

    text = "Text with one emoji 👍. And a few more: 🌍, 😂, 😃, 😂, 🌍, 🌦️."
    import emoji
    print(emoji.emoji_list(text))
    expected_result = "Text with one emoji  . And a few more:  ,  ,  ,  ,  ,   ."
    result = process_text(text)
    assert result == expected_result
