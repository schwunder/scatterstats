from scrap import scrap_pipe
from clean import clean_pipe
from toolz import thread_first
from util import timeit
import spacy
import pandas as pd
import scattertext as st
from typeguard import typechecked


#@timeit
@typechecked
def scat_pipe(in_page: str, label: str) -> pd.DataFrame:
    return thread_first(in_page,
                        (scrap_pipe, label),
                        (clean_pipe, label)
                        )


#@timeit
@typechecked
def scatter_vis(in1: str, in2: str):
    lab1 = str(in1.split("/")[-1])
    lab2 = str(in2.split("/")[-1])

    df = scat_pipe(in1, lab1).append(scat_pipe(in2, lab2), ignore_index=True)
    nlp = spacy.load("en")
    corpus = st.CorpusFromPandas(df, category_col='labels', text_col='texts', nlp=nlp).build()
    html = st.produce_scattertext_explorer(corpus,
                                           category=lab1,
                                           category_name=lab1,
                                           not_category_name=lab2,
                                           width_in_pixels=1000,
                                           )
    return html


input1 = 'https://en.wikipedia.org/wiki/Capitalism'
input2 = 'https://en.wikipedia.org/wiki/Communism'
h = scatter_vis(input1, input2)
open("Visualization.html", 'wb').write(h.encode('utf-8'))
