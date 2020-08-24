import requests
import bs4
import spacy
import pandas as pd
import scattertext as st
import wikipediaapi
import time
from bs4 import BeautifulSoup
from toolz import thread_first
from typeguard import typechecked
from typing import List, Dict, Union
from toolz import interpose

wiki_wiki = wikipediaapi.Wikipedia('en')
Maybe_WikiPages = List[Union[None, wikipediaapi.WikipediaPage]]


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


def safe(x, fn):
    try:
        return fn(x)
    except:
        pass

# data_pipe = interpose(spy, [])
def spy(x):
    #print(x)
    return x

#class TextClean:
#   @staticmethod

@timeit
@typechecked
def get_soup(elem: requests.models.Response) -> BeautifulSoup:
    soup = BeautifulSoup(elem.text, features="html.parser")
    return soup

@timeit
@typechecked
def get_html_elem(elem: BeautifulSoup) -> bs4.element.Tag:

    navtable = elem.find_all('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}) or elem.find_all('table', attrs={'class': 'vertical-navbox nowraplinks'})
    return navtable[0]

@timeit
@typechecked
def get_links_to_elem(elem: bs4.element.Tag, max=10) -> List[Union[str, None]]:
    navtable_links = [d.get("href") for d in elem.descendants if d.name == "a"]
    return navtable_links[:max]

@timeit
@typechecked
def get_pure_links(elem: List[Union[str, None]]) -> List[Union[str, None]]:
    pure_links = [w.split("/")[-1] for w in elem if w and "/wiki/" in w]
    return pure_links

@timeit
@typechecked
def get_pages_from_links(elem: List[Union[str, None]], origin: str) -> Maybe_WikiPages:
    complete_content = [safe(w, wiki_wiki.page) for w in elem]
    complete_content.append(safe(origin, wiki_wiki.page))
    return complete_content

@timeit
@typechecked
def get_texts_from_pages(elem: Maybe_WikiPages) -> List[Union[str, None]]:
    contents = [c.text for c in elem if c]
    return contents

@timeit
@typechecked
def clean_text_list(raw_texts: List[str]) -> List[str]:
    clean_texts = [raw_text.replace('=', ' ').replace('\\n', ' ').replace('\n', ' ').replace('\r', '').replace('  ', '')
                   for raw_text in
                   raw_texts]
    return clean_texts

@timeit
@typechecked
def filter_stopwords(text: str, nlp=spacy.load("en")) -> str:
    doc = nlp(text)
    bad = "\\"
    return ' '.join([word for word in [token.text for token in doc] if
                     len(word) > 2 and bad not in word and not nlp.vocab[word].is_stop])

@timeit
@typechecked
def filter_stopwords_wrap(texts: List[str]) -> List[str]:
    return [filter_stopwords(text) for text in texts]

@timeit
@typechecked
def filter_pos(text: str, pos: str, nlp=spacy.load("en")) -> str:
    doc = nlp(text)
    return " ".join([token.text for token in doc if token.pos_ != pos])

@timeit
@typechecked
def filter_pos_wrap(texts: List[str], pos: str) -> List[str]:
    return [filter_pos(text, pos) for text in texts]

@timeit
@typechecked
def make_data_frame(texts: List[str], label: str) -> pd.DataFrame:
    dicty = {
        'texts': texts,
        'labels': label
    }
    return pd.DataFrame(dicty, columns=['texts', 'labels'])



@timeit
def pipe(in_page):
    a = str(in_page.split("/")[-1])
    return thread_first(in_page,
                        requests.get,
                        get_soup,
                        get_html_elem,
                        (get_links_to_elem, 3),
                        get_pure_links,
                        (get_pages_from_links, a),
                        get_texts_from_pages,
                        clean_text_list,
                        filter_stopwords_wrap,
                        #(filter_pos_wrap, 'VERB'),
                        (make_data_frame, a)
                        )

@timeit
def scatter_vis(in1, in2):
    a = str(in1.split("/")[-1])
    b = str(in2.split("/")[-1])
    df = pipe(in1).append(pipe(in2), ignore_index=True)
    nlp = spacy.load("en")
    corpus = st.CorpusFromPandas(df, category_col='labels', text_col='texts', nlp=nlp).build()
    html = st.produce_scattertext_explorer(corpus,
                                           category=a,
                                           category_name=a,
                                           not_category_name=b,
                                           width_in_pixels=1000,
                                           )
    return html


input1 = 'https://en.wikipedia.org/wiki/Bayesian_statistics'
input2 = 'https://en.wikipedia.org/wiki/Machine_learning'
h = scatter_vis(input1, input2)
open("Visualization.html", 'wb').write(h.encode('utf-8'))


