import re
from math import ceil
from typing import List


REGEX_SPLIT_PATTERN = r'\b|(?!)\s'
OPEN_TAG = 0
CLOSE_TAG = 1
NEW_LINE_TAG = 2
TRANSFORMATION_OPTIONS = {
    'html': ('<b>', '</b>', '<br />'),
    'markdown': ('**', '**', '\n')
}


def split_text_by_newlines(text: str) -> List[str]:
    splitted_text = text.split('\n')
    return splitted_text


def insert_bold_tag_in_word(
    word: str,
    open_tag: str,
    close_tag: str
) -> str:
    if len(word) == 1:
        word_to_return = f'{open_tag}' + word + f'{close_tag}'
    if len(word) == 3:
        word_to_return = f'{open_tag}' + word[0] + f'{close_tag}' + word[1:]
    else:
        nums = ceil(len(word) / 2)
        word_to_return = (
            f'{open_tag}' + word[:nums] + f'{close_tag}' + word[nums:]
        )
    return word_to_return


def transform_text(
    paragraph: str,
    open_tag: str,
    close_tag: str
) -> str:
    words_and_symbols = paragraph.split()
    transfromed_paragraph = []

    for _ in words_and_symbols:
        splitted_word_or_symbol = re.split(REGEX_SPLIT_PATTERN, _)

        transformed_string = []
        for _ in splitted_word_or_symbol:
            if _.isalpha():
                _ = insert_bold_tag_in_word(_, open_tag, close_tag)
                transformed_string.append(_)
            else:
                transformed_string.append(_)

        transformed_string = ''.join(transformed_string)
        transfromed_paragraph.append(transformed_string)
    return ' '.join(transfromed_paragraph)


async def execute_transformation_process(
    text_to_transform: str,
    output_type: str = 'html'
) -> str:
    paragraphs = split_text_by_newlines(text_to_transform)
    open_tag = TRANSFORMATION_OPTIONS[output_type][OPEN_TAG]
    close_tag = TRANSFORMATION_OPTIONS[output_type][CLOSE_TAG]
    new_line_tag = TRANSFORMATION_OPTIONS[output_type][NEW_LINE_TAG]

    fully_transformed_text = []
    for paragraph in paragraphs:
        transformed_text = transform_text(
            paragraph, open_tag, close_tag
        )
        fully_transformed_text.append(transformed_text)

    fully_transformed_text = f'{new_line_tag}'.join(fully_transformed_text)
    return fully_transformed_text
