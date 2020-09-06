import pandas as pd
import scattertext as st
import spacy
from toolz import thread_first
from typeguard import typechecked
from model import nlp
from clean import clean_pipe
from scrap import scrap_pipe
from util import last_of_route


# @timeit
@typechecked
def scat_pipe(in_page: str, label: str, size: int) -> pd.DataFrame:
    return thread_first(in_page,
                        (scrap_pipe, label, size),
                        (clean_pipe, label)
                        )


# @typechecked
# def get_page_lists(in1: str, in2: str) -> List[List]:
#     x = get_page_lists(in1)
#     y = get_page_lists(in2)
#     return [x, y]


# @timeit
@typechecked
def scatter_vis(in1: str, in2: str, size: int):
    lab1 = last_of_route(in1)
    lab2 = last_of_route(in2)

    df = scat_pipe(in1, lab1, size).append(scat_pipe(in2, lab2, size), ignore_index=True)
    corpus = st.CorpusFromPandas(df, category_col='labels', text_col='texts', nlp=nlp).build()
    html = st.produce_scattertext_explorer(corpus,
                                           category=lab1,
                                           category_name=lab1,
                                           not_category_name=lab2,
                                           width_in_pixels=1000,
                                           )
    return html

#
x = scatter_vis('https://en.wikipedia.org/wiki/Tweed_Courthouse', 'https://en.wikipedia.org/wiki/GW190521', 5)
with open("aa.html", 'wb') as f:
    f.write(x.encode('utf-8'))
