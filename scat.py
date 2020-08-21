import os
import pandas as pd
from typeguard import typechecked
import scattertext as st
import spacy
from IPython.display import HTML, IFrame
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from typing import List, Dict, Union
size = 25

@typechecked
def has_bad_symbol(text: str) -> bool:
    return "((" in text or "{{" in text




def filter_words(content):
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = English()

    text = content.replace('\n', ' ').replace('\r', '').replace('  ', '')

    #  "nlp" Object is used to create documents with linguistic annotations.
    my_doc = nlp(text)

    # Create list of word tokens
    token_list = []
    for token in my_doc:
        if token.pos_ != "VERB":
            token_list.append(token.text)

    # Create list of word tokens after removing stopwords
    filtered_sentence = []
    bad = "\\"
    for word in token_list:
        lexeme = nlp.vocab[word]
        if (len(word) > 5 and bad not in word):
            if lexeme.is_stop == False:
                filtered_sentence.append(word)
    f = ' '.join(filtered_sentence)
    return f


def load_all_from_dir(dir:str)->List[str]:
    5



wikiscrap1 = {'texts': texts1,
              'labels': 'ml'
              }
wikiscrap2 =  {'texts': texts2,
              'labels': 'stat'
              }



df2 = pd.DataFrame(wikiscrap2, columns=['texts', 'labels'])
df1 = pd.DataFrame(wikiscrap1, columns=['texts', 'labels'])
df3 = df2.append(df1, ignore_index=True)
print(df3)
nlp = spacy.load('en')
corpus = st.CorpusFromPandas(df3, category_col='labels', text_col='texts', nlp=nlp).build()
html = st.produce_scattertext_explorer(corpus,
          category='ml',
          category_name='ml',
          not_category_name='stat',
          width_in_pixels=1000,
          metadata=corpus.get_df()['labels'])
open("Visualization.html", 'wb').write(html.encode('utf-8'))
# x = ""
# with open("Visualization.html") as html:
#   x = html.read()
# HTML(x)

