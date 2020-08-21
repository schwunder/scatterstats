
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English


a = """From a Bayesian point of view, we would regard it as a prior distribution.
That is, it is our believed probability distribution on the states of nature, prior to observing data.\nMore important, it is sometimes convenient to use an improper prior \n  \n    \n      \n        \u03c0\n        (\n        \u03b8\n        )\n        \n        \n      \n    \n    {\\displaystyle \\pi (\\theta )\\,\\!
\n\n\n=== Admissibility of (generalized) Bayes rules ===\nAccording to the complete class theorems, under mild conditions every admissible rule is a (generalized) Bayes rule (with respect to some prior \n  \n    \n      \n        \u03c0\n        (\n        \u03b8\n        )\n        \n        \n      \n    \n    {\\displaystyle \\pi (\\theta )\\,\\!"""

#print(a)
import re
#a.replace('\\n', '')
#newstr = re.sub("\\\\", "aaa", a)
#newstr = re.sub("\\\\n", "aaa", newstr)
mystring = a
print(mystring)


print(filter_words(mystring))
