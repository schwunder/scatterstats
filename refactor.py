import os
from typing import List, Dict
from typeguard import typechecked
import spacy
import pandas as pd
import scattertext as st


@typechecked()
def load_size_from_dir(dir: str, size: int) -> List[str]:
    iterator = os.listdir(dir)
    filenames = [dir + "/" + filename for filename in iterator[:size]]
    raw_texts = []
    for fn in filenames:
        with open(fn, "r") as file:
            raw_text = file.read()
            raw_texts.append(raw_text)
    return raw_texts


@typechecked()
def clean_text_list(raw_texts: List[str]) -> List[str]:
    clean_texts = [raw_text.replace('=', ' ').replace('\\n', ' ').replace('\n', ' ').replace('\r', '').replace('  ', '')
                   for raw_text in
                   raw_texts]
    return clean_texts


@typechecked()
def filter_pos(text: str, pos: str, nlp=spacy.load("en_core_web_sm")) -> str:
    doc = nlp(text)
    return " ".join([token.text for token in doc if token.pos_ != pos])


@typechecked()
def filter_stopwords(text: str, nlp=spacy.load("en_core_web_sm")) -> str:
    doc = nlp(text)
    bad = "\\"
    return ' '.join([word for word in [token.text for token in doc] if
                     len(word) > 2 and bad not in word and not nlp.vocab[word].is_stop])


@typechecked()
def make_data_frame(texts: List[str], label: str):
    dicty = {
        'texts': texts,
        'labels': label
    }
    return pd.DataFrame(dicty, columns=['texts', 'labels'])


size = 25
t1 = load_size_from_dir('ml_wiki', size)
t2 = load_size_from_dir('stat_wiki', size)
print('load conplete')
t1 = clean_text_list(t1)
t2 = clean_text_list(t2)
t3 = [filter_pos(filter_stopwords(text), 'VERB') for text in t1]
t4 = [filter_pos(filter_stopwords(text), 'VERB') for text in t2]
df1 = make_data_frame(t3, 'ml')
df2 = make_data_frame(t4, 'stat')
df = df2.append(df1, ignore_index=True)
print(df)
nlp = spacy.load("en")
corpus = st.CorpusFromPandas(df, category_col='labels', text_col='texts', nlp=nlp).build()
html = st.produce_scattertext_explorer(corpus,
                                       category='ml',
                                       category_name='ml',
                                       not_category_name='stat',
                                       width_in_pixels=1000,
                                       )
open("Visualization.html", 'wb').write(html.encode('utf-8'))
