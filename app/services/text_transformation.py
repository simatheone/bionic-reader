import re
from enum import Enum
from math import ceil
from typing import List, Literal, Union

REGEX_SPLIT_PATTERN = r'\b|(?!)\s'


class FormatTags(str, Enum):
    HTML_OPEN_B_TAG = '<b>'
    HTML_CLOSE_B_TAG = '</b>'
    HTML_NEW_LINE_TAG = '<br />'
    MARKDOWN_B_TAG = '**'
    MARKDOWN_NEW_LINE_TAG = '\n'


def _split_text_by_newlines(text: str) -> List[str]:
    """Split incoming text by newlines."""
    splitted_text = text.split('\n')
    return splitted_text


def _insert_bold_tag_in_word(
    word_to_transform: str,
    open_tag: str,
    close_tag: str
) -> str:
    """
    Transforms the word by inserting a bold tag in
    spicific place in word.

    The base logic of adding bold tags.
    If word's length is equal to 1 then bold tags will be added
    at both sides of a word.
    If word's length is equal to 3 then bold tag will be added
    before and after first letter.
    For words which length is more then 3 symbols logic is:
        The last index of character is calculated by the formula:
            -> last_char_idx = ceil(word's length / 2)
        The bold tags will be added before the word and after
        last_char_idx (excluded). The rest part of the word will
        stay tha same (not transformed).

    Example for the file output_type = 'html':
        word = 'a' -> transforms to: <b>a</b>
        word = 'dog' -> transforms to: <b>d</b>og
        word = 'home' -> transforms to: <b>ho</b>me
        word = 'hello' -> transforms to: <b>hel</b>lo
    Same logic is provided for the output_type = 'markdown'.
    HTML tags will be replaced with markdown tags.
    """
    transformed_word = None
    word_length = len(word_to_transform)
    if word_length == 1:
        transformed_word = (
            f'{open_tag}' + word_to_transform + f'{close_tag}'
        )
    elif word_length == 3:
        transformed_word = (
            f'{open_tag}' + word_to_transform[0] +
            f'{close_tag}' + word_to_transform[1:]
        )
    else:
        last_bold_letter_idx = ceil(word_length / 2)
        transformed_word = (
            f'{open_tag}' + word_to_transform[:last_bold_letter_idx] +
            f'{close_tag}' + word_to_transform[last_bold_letter_idx:]
        )
    return transformed_word


def _transform_text(
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
                _ = _insert_bold_tag_in_word(_, open_tag, close_tag)
                transformed_string.append(_)
            else:
                transformed_string.append(_)

        transformed_string = ''.join(transformed_string)
        transfromed_paragraph.append(transformed_string)
    return ' '.join(transfromed_paragraph)


async def execute_transformation_process(
    text_to_transform: str,
    output_type: Union[Literal['html'], Literal['markdown']] = 'html'
) -> str:
    paragraphs = _split_text_by_newlines(text_to_transform)

    open_tag = close_tag = new_line_tag = None
    if output_type == 'html':
        open_tag = FormatTags.HTML_OPEN_B_TAG.value
        close_tag = FormatTags.HTML_CLOSE_B_TAG.value
        new_line_tag = FormatTags.HTML_NEW_LINE_TAG.value
    else:
        open_tag = close_tag = FormatTags.MARKDOWN_B_TAG.value
        new_line_tag = FormatTags.MARKDOWN_NEW_LINE_TAG.value

    fully_transformed_text = []
    for paragraph in paragraphs:
        transformed_text = _transform_text(
            paragraph, open_tag, close_tag
        )
        fully_transformed_text.append(transformed_text)

    fully_transformed_text = f'{new_line_tag}'.join(fully_transformed_text)
    return fully_transformed_text
