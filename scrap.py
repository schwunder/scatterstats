import requests
from bs4 import BeautifulSoup

r = requests.get('https://en.wikipedia.org/wiki/Bayesian_statistics')
soup = BeautifulSoup(r.text, features="html.parser")


def safe(x, fn):
    try:
        return fn(x)
    except:
        pass

print('adfadfa')
navtable = soup.find_all('table', attrs={'class': 'vertical-navbox nowraplinks hlist'})[0]
navtable_links = [d.get("href") for d in navtable.descendants if d.name == "a"]
pure_links = [w.split("/")[-1] for w in navtable_links if w and "/wiki/" in w]
print('asfads')
import wikipedia
print('sadfadsf')
complete_content = [safe(w, wikipedia.page) for w in pure_links]
print('adsfad')
contents = [c.content for c in complete_content if c]
print('asdfa')
for idx, content in enumerate(contents):
    print(idx, "---")
    with open("stat_wiki/" + str(idx) + ".txt", "w+") as file:
        file.write(content.encode('unicode-escape').decode('utf-8'))
