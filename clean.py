from typing import List, Union

import pandas as pd
import spacy
from toolz import thread_first
from typeguard import typechecked


# @timeit
@typechecked
def clean_text_list(raw_texts: List[str]) -> List[str]:
    clean_texts = [raw_text.replace('=', ' ').replace('\\n', ' ').replace('\n', ' ').replace('\r', '').replace('  ', '')
                   for raw_text in
                   raw_texts]
    return clean_texts


# @timeit
@typechecked
def filter_stopwords(text: str, nlp=spacy.load("en")) -> str:
    doc = nlp(text)
    bad = "\\"
    return ' '.join([word for word in [token.text for token in doc] if
                     len(word) > 2 and bad not in word and not nlp.vocab[word].is_stop])


# @timeit
@typechecked
def filter_stopwords_wrap(texts: List[str]) -> List[str]:
    return [filter_stopwords(text) for text in texts]


# @timeit
@typechecked
def filter_pos(text: str, pos: str, nlp=spacy.load("en")) -> str:
    doc = nlp(text)
    return " ".join([token.text for token in doc if token.pos_ != pos])


# @timeit
@typechecked
def filter_pos_wrap(texts: List[str], pos: str) -> List[str]:
    return [filter_pos(text, pos) for text in texts]


# @timeit
@typechecked
def make_data_frame(texts: List[str], label: str) -> pd.DataFrame:
    dicty = {
        'texts': texts,
        'labels': label
    }
    return pd.DataFrame(dicty, columns=['texts', 'labels'])


# @timeit
@typechecked
def clean_pipe(txt_lst: List[Union[str, None]], label: str) -> pd.DataFrame:
    return thread_first(txt_lst,
                        clean_text_list,
                        filter_stopwords_wrap,
                        # (filter_pos_wrap, 'VERB'),
                        (make_data_frame, label))
