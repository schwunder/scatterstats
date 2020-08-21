import os
from typing import List, Dict
from typeguard import typechecked
import spacy


def load_size_from_dir(dir: str, size: int) -> List[str]:
    iterator = os.listdir(dir)
    filenames = [dir + "/" + filename for filename in iterator[:size]]
    raw_texts = []
    for fn in filenames:
        with open(fn, "r") as file:
            raw_text = file.read()
            raw_texts.append(raw_text)
    return raw_texts


def clean_text_list(raw_texts: List[str]) -> List[str]:
    clean_texts = [raw_text.replace('=', ' ').replace('\\n', ' ').replace('\n', ' ').replace('\r', '').replace('  ', '')
                   for raw_text in
                   raw_texts]
    return clean_texts


def filter_pos(text, pos, nlp=spacy.load("en_core_web_sm")) -> str:
    doc = nlp(text)
    return " ".join([token.text for token in doc if token.pos_ != pos])


def filter_stopwords(text, nlp=spacy.load("en_core_web_sm")) -> str:
    doc = nlp(text)
    return ' '.join([word for word in [token.text for token in doc] if not nlp.vocab[word].is_stop])
