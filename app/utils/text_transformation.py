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


def split_text_by_newlines(text: str) -> List[str]:
    """Split incoming text by newlines."""
    splitted_text = text.split('\n')
    return splitted_text


def insert_bold_tag_in_word(
    word_to_transform: str, open_tag: str, close_tag: str
) -> str:
    """Transforms the word by inserting a bold tag in
    specific place in word.

    The base logic of adding bold tags.
        If word's length is equal to 1 then bold tags will be added
        at both sides of a word.
        If word's length is equal to 3 then bold tag will be added
        before and after first letter.
        For words which length is more then 3 symbols logic is:
            The last index of character is calculated by the formula:
            - `last_char_idx = ceil(word's length / 2)`
            The bold tags will be added before the word and after
            `last_char_idx` (exclusively). The rest part of the word will
            stay tha same (not transformed).

    Example for the file `output_type = 'html'`:
        `word = 'a'` -> transforms to: `<b>a</b>`
        `word = 'dog'` -> transforms to: `<b>d</b>og`
        `word = 'home'` -> transforms to: `<b>ho</b>me`
        `word = 'hello'` -> transforms to: `<b>hel</b>lo`
    Same logic is provided for the `output_type = 'markdown'`.
    HTML tags will be replaced with markdown tags.
    """
    transformed_word = None
    word_length = len(word_to_transform)
    if word_length == 1:
        transformed_word = f'{open_tag}' + word_to_transform + f'{close_tag}'
    elif word_length == 3:
        transformed_word = (
            f'{open_tag}'
            + word_to_transform[0]
            + f'{close_tag}'
            + word_to_transform[1:]
        )
    else:
        last_bold_letter_idx = ceil(word_length / 2)
        transformed_word = (
            f'{open_tag}'
            + word_to_transform[:last_bold_letter_idx]
            + f'{close_tag}'
            + word_to_transform[last_bold_letter_idx:]
        )
    return transformed_word


def transform_text(paragraph: str, open_tag: str, close_tag: str) -> str:
    sentences = paragraph.split()
    transformed_paragraph = []

    for sentence in sentences:
        splitted_words_or_symbols = re.split(REGEX_SPLIT_PATTERN, sentence)

        transformed_sentence = []
        for characters in splitted_words_or_symbols:
            if characters.isalpha():
                characters = insert_bold_tag_in_word(
                    characters, open_tag, close_tag
                )
                transformed_sentence.append(characters)
            else:
                transformed_sentence.append(characters)

        transformed_sentence = ''.join(transformed_sentence)
        transformed_paragraph.append(transformed_sentence)
    return ' '.join(transformed_paragraph)


async def execute_transformation_process(
    text_to_transform: str,
    output_type: Union[Literal['html'], Literal['markdown']] = 'html',
) -> str:
    paragraphs = split_text_by_newlines(text_to_transform)

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
        transformed_text = transform_text(paragraph, open_tag, close_tag)
        fully_transformed_text.append(transformed_text)

    fully_transformed_text = f'{new_line_tag}'.join(fully_transformed_text)
    return fully_transformed_text
