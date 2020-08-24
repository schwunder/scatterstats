import requests
import bs4
import wikipediaapi
from bs4 import BeautifulSoup
from toolz import thread_first
from typeguard import typechecked
from typing import List, Dict, Union
from util import timeit

Maybe_WikiPages = List[Union[None, wikipediaapi.WikipediaPage]]


# @timeit
@typechecked
def get_soup(elem: requests.models.Response) -> BeautifulSoup:
    soup = BeautifulSoup(elem.text, features="html.parser")
    return soup


# @timeit
@typechecked
def get_html_elem(elem: BeautifulSoup) -> bs4.element.Tag:
    navtable = elem.find_all('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}) or elem.find_all('table',
                                                                                                             attrs={
                                                                                                                 'class': 'vertical-navbox nowraplinks'})
    return navtable[0]


# @timeit
@typechecked
def get_links_to_elem(elem: bs4.element.Tag, max=5) -> List[Union[str, None]]:
    navtable_links = [d.get("href") for d in elem.descendants if d.name == "a"]
    return navtable_links[:max]


# @timeit
@typechecked
def get_pure_links(elem: List[Union[str, None]]) -> List[Union[str, None]]:
    pure_links = [w.split("/")[-1] for w in elem if w and "/wiki/" in w]
    return pure_links


# @timeit
@typechecked
def get_pages_from_links(elem: List[Union[str, None]], origin: str) -> Maybe_WikiPages:
    from util import safe
    wiki_wiki = wikipediaapi.Wikipedia('en')
    complete_content = [safe(w, wiki_wiki.page) for w in elem]
    complete_content.append(safe(origin, wiki_wiki.page))
    return complete_content


# @timeit
@typechecked
def get_texts_from_pages(elem: Maybe_WikiPages) -> List[Union[str, None]]:
    # wiki_wiki = wikipediaapi.Wikipedia('en')
    contents = [c.text for c in elem if c]
    return contents


# @timeit
@typechecked
def scrap_pipe(in_page: str, label: str) -> List[Union[str, None]]:
    return thread_first(in_page,
                        requests.get,
                        get_soup,
                        get_html_elem,
                        (get_links_to_elem, 5),
                        get_pure_links,
                        (get_pages_from_links, label),
                        get_texts_from_pages)
