import pandas as pd
import scattertext as st
import spacy
from toolz import thread_first
from typeguard import typechecked

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
    nlp = spacy.load("en")
    corpus = st.CorpusFromPandas(df, category_col='labels', text_col='texts', nlp=nlp).build()
    html = st.produce_scattertext_explorer(corpus,
                                           category=lab1,
                                           category_name=lab1,
                                           not_category_name=lab2,
                                           width_in_pixels=1000,
                                           )
    return html
