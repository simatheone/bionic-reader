import re
from math import ceil
from typing import List


async def split_text_by_newlines(text: str) -> List[str]:
    splitted_text = text.split('\n')
    return splitted_text


async def insert_html_b_tag_in_word(word: str) -> str:
    if len(word) == 1:
        word_to_return = '<b>' + word + '</b>'
    if len(word) == 3:
        word_to_return = '<b>' + word[0] + '</b>' + word[1:]
    else:
        nums = ceil(len(word) / 2)
        word_to_return = '<b>' + word[:nums] + '</b>' + word[nums:]
    return word_to_return


async def transform_text(paragraph: str) -> str:
    words_and_symbols = paragraph.split()
    transfromed_paragraph = []

    for value in words_and_symbols:
        splitted_word_or_symbol = re.split(r'\b|(?!)\s', value)

        transformed_string = []
        for _ in splitted_word_or_symbol:
            if _.isalpha():
                _ = insert_html_b_tag_in_word(_)
                transformed_string.append(_)
            else:
                transformed_string.append(_)

        transformed_string = ''.join(transformed_string)
        transfromed_paragraph.append(transformed_string)
    return ' '.join(transfromed_paragraph)


async def execute_transformation_process(
    text_to_transform: str,
) -> str:
    paragraphs = await split_text_by_newlines(text_to_transform)
    result = []
    for paragraph in paragraphs:
        transformed_text = transform_text(paragraph)
        result.append(transformed_text)
    res = '<br>'.join(result)
    return res
