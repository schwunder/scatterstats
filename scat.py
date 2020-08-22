import os
from typing import List, Dict
from typeguard import typechecked
import spacy
import pandas as pd
import scattertext as st
from toolz import thread_first


# dirnames
# max_len
# pos_filter (Verb)
# stop_words
# replace_words
# regex


@typechecked
def load_size_from_dir(dir: str, size: int) -> List[str]:
    iterator = os.listdir(dir)
    filenames = [dir + "/" + filename for filename in iterator[:size]]
    raw_texts = []
    for fn in filenames:
        with open(fn, "r") as file:
            raw_text = file.read()
            raw_texts.append(raw_text)
    return raw_texts


@typechecked
def clean_text_list(raw_texts: List[str]) -> List[str]:
    clean_texts = [raw_text.replace('=', ' ').replace('\\n', ' ').replace('\n', ' ').replace('\r', '').replace('  ', '')
                   for raw_text in
                   raw_texts]
    return clean_texts


@typechecked
def filter_pos(text: str, pos: str, nlp=spacy.load("en")) -> str:
    doc = nlp(text)
    return " ".join([token.text for token in doc if token.pos_ != pos])


@typechecked
def filter_stopwords(text: str, nlp=spacy.load("en")) -> str:
    doc = nlp(text)
    bad = "\\"
    return ' '.join([word for word in [token.text for token in doc] if
                     len(word) > 2 and bad not in word and not nlp.vocab[word].is_stop])


@typechecked
def make_data_frame(texts: List[str], label: str):
    dicty = {
        'texts': texts,
        'labels': label
    }
    return pd.DataFrame(dicty, columns=['texts', 'labels'])


@typechecked
def parse_to_df(dirname: str) -> pd.DataFrame:
    # dirname = config["dirname"]
    return thread_first(
        dirname,

        (load_size_from_dir, 2),
        clean_text_list,
        lambda txt_lst: [filter_pos(filter_stopwords(text), 'VERB') for text in txt_lst],
        (make_data_frame, dirname)
    )


def scatter_vis(dirs):
    a, b = dirs
    df = parse_to_df(a).append(parse_to_df(b), ignore_index=True)
    nlp = spacy.load("en")
    corpus = st.CorpusFromPandas(df, category_col='labels', text_col='texts', nlp=nlp).build()
    html = st.produce_scattertext_explorer(corpus,
                                           category=a,
                                           category_name=a,
                                           not_category_name=b,
                                           width_in_pixels=1000,
                                           )
    return html


h = scatter_vis(["ml_wiki", "stat_wiki"])
open("Visualization.html", 'wb').write(h.encode('utf-8'))
