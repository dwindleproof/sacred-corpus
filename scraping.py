import requests
from multiprocessing import Pool

from bs4 import BeautifulSoup
from bs4.element import NavigableString as n_str

from lxml import etree

from standard_works import standard_works_urls, process_chapter
from text_processing import escape

#################################################################################
# Fundamental HTTP Request Functions
#################################################################################
headers = { # Politely declares scraping source for raising issues with ToS etc.
    'User-Agent': 'github.com/dwindleproof/sacred-corpus',
}

def get(url):
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        return BeautifulSoup(page.text, 'html.parser')
    
    raise ValueError(f"Failed to get {url}")

#################################################################################
# Fundamental HTTP Request Functions
#################################################################################
# String used for failures in scraping
error_string = """<chapter name='{}'><verse name='1'>
    Failed to obtain: {} with {}
</verse></chapter>"""

def process(args):
    "Processes raw input into the corpus"
    try:
        url, tags = args
        return process_chapter(get(url), url, tags)
    except Exception as e:
        # Failures are shunted to a special collection, marking the failed parameters
        import traceback
        return (
            error_string.format(tags[-1], args, escape(traceback.format_exc()), )
            ['failures',] + tags[1:],
        )

def add(chapter, tags, corpus):
    "Adds a chapter with given tags to the corpus"

    # Collection is created if not already extant
    if not corpus.xpath(f'/corpus/collection[@name="{tags[0]}"]'):
        corpus.append(
            etree.Element('collection', name=tags[0])
        )

    # Book is created if not already extant
    if not corpus.xpath(f'/corpus/collection[@name="{tags[0]}"]/book[@name="{tags[1]}"]'):            
        corpus.xpath(f'/corpus/collection[@name="{tags[0]}"]')[0].append(
            etree.Element('book', name=tags[1])
        )

    # The chapter is appended, and the corpus returned
    corpus.xpath(f'/corpus/collection[@name="{tags[0]}"]/book[@name="{tags[1]}"]')[0].append(
        chapter
    )

    return corpus
    
def standard_works(corpus = None, size=50):
    "Multithreading generator "
    if corpus is None:
        corpus = etree.Element('corpus')
        
    with Pool(size) as p:
        results = p.map(
            process,
            standard_works_urls(),
        )
    
    for string, tags in results:
        corpus = add(
            etree.fromstring(string),
            tags,
            corpus
        )
    
    return corpus
