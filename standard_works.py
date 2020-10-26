from bs4 import BeautifulSoup
from bs4.element import NavigableString as n_str

from lxml import etree

from text_processing import process_raw_web_string

#################################################################################
# Scraping URLs
#################################################################################
base_url = 'https://www.churchofjesuschrist.org'

standard_works_base_url = base_url + '/study/scriptures'

#################################################################################
# Standard Works Nested Structure
#################################################################################
ot = {
    'dedication' : {'Epistle Dedicatory': None},
    'gen'        : {'Genesis'           : 50  },
    'ex'         : {'Exodus'            : 40  },
    'lev'        : {'Leviticus'         : 27  },
    'num'        : {'Numbers'           : 36  },
    'deut'       : {'Deuteronomy'       : 34  }, 
    'josh'       : {'Joshua'            : 24  },
    'judg'       : {'Judges'            : 21  },
    'ruth'       : {'Ruth'              :  4  },
    '1-sam'      : {'1 Samuel'          : 31  },
    '2-sam'      : {'2 Samuel'          : 24  },
    '1-kgs'      : {'1 Kings'           : 22  },
    '2-kgs'      : {'2 Kings'           : 25  },
    '1-chr'      : {'1 Chronicles'      : 29  },
    '2-chr'      : {'2 Chronicles'      : 36  },
    'ezra'       : {'Ezra'              : 10  },
    'neh'        : {'Nehemiah'          : 13  },
    'esth'       : {'Esther'            : 10  },
    'job'        : {'Job'               : 42  },
    'ps'         : {'Psalms'            : 150 },
    'prov'       : {'Proverbs'          : 31  },
    'eccl'       : {'Ecclesiastes'      : 12  },
    'song'       : {'Song of Solomon'   :  8  },
    'isa'        : {'Isaiah'            : 66  },
    'jer'        : {'Jeremiah'          : 52  },
    'lam'        : {'Lamentations'      :  5  },
    'ezek'       : {'Ezekiel'           : 48  },
    'dan'        : {'Daniel'            : 12  },
    'hosea'      : {'Hosea'             : 14  },
    'joel'       : {'Joel'              :  3  },
    'amos'       : {'Amos'              :  9  },
    'obad'       : {'Obadiah'           :  1  },
    'jonah'      : {'Jonah'             :  4  },
    'micah'      : {'Micah'             :  7  },
    'nahum'      : {'Nahum'             :  3  },
    'hab'        : {'Habakkuk'          :  3  },
    'zeph'       : {'Zephaniah'         :  3  },
    'hag'        : {'Haggai'            :  2  },
    'zech'       : {'Zechariah'         : 14  },
    'mal'        : {'Malachi'           :  4  },
}

nt = {
    'matt'       : {'Matthew'           : 28  },
    'mark'       : {'Mark'              : 16  },
    'luke'       : {'Luke'              : 24  },
    'john'       : {'John'              : 21  },
    'acts'       : {'Acts'              : 28  },
    'rom'        : {'Romans'            : 16  },
    '1-cor'      : {'1 Corinthians'     : 16  },
    '2-cor'      : {'2 Corinthians'     : 13  },
    'gal'        : {'Galatians'         :  6  },
    'eph'        : {'Ephesians'         :  6  },
    'philip'     : {'Philippians'       :  4  },
    'col'        : {'Colossians'        :  4  },
    '1-thes'     : {'1 Thessalonians'   :  5  },
    '2-thes'     : {'2 Thessalonians'   :  3  },
    '1-tim'      : {'1 Timothy'         :  6  },
    '2-tim'      : {'2 Timothy'         :  4  },
    'titus'      : {'Titus'             :  3  },
    'philem'     : {'Philemon'          :  1  },
    'heb'        : {'Hebrews'           : 13  },
    'james'      : {'James'             :  5  },
    '1-pet'      : {'1 Peter'           :  5  },
    '1-pet'      : {'2 Peter'           :  3  },
    '1-jn'       : {'1 John'            :  5  },
    '2-jn'       : {'2 John'            :  1  },
    '3-jn'       : {'3 John'            :  1  },
    'jude'       : {'Jude'              :  1  },
    'rev'        : {'Revelation'        : 22  },
}

bofm = {
    'bofm-title'  : {'Title Page of the Book of Mormon'           : None},
    'introduction': {'Introduction'                               : None},
    'three'       : {'The Testimony of Three Witnesses'           : None},
    'eight'       : {'The Testimony of Eight Witnesses'           : None},
    'js'          : {'The Testimony of the Prophet Joseph Smith'  : None},
    'explanation' : {'Brief Explanation about the Book of Mormon' : None},
    '1-ne'        : {'1 Nephi'                                    : 22  },
    '2-ne'        : {'2 Nephi'                                    : 33  },
    'jacob'       : {'Jacob'                                      :  7  },
    'enos'        : {'Enos'                                       :  1  },
    'jarom'       : {'Jarom'                                      :  1  },
    'omni'        : {'Omni'                                       :  1  },
    'w-of-m'      : {'Words of Mormon'                            :  1  },
    'mosiah'      : {'Mosiah'                                     : 29  },
    'alma'        : {'Alma'                                       : 63  },
    'hel'         : {'Helaman'                                    : 16  },
    '3-ne'        : {'3 Nephi'                                    : 30  },
    '4-ne'        : {'4 Nephi'                                    :  1  },
    'morm'        : {'Mormon'                                     :  9  },
    'ether'       : {'Ether'                                      : 15  },
    'moro'        : {'Moroni'                                     : 10  },
}

dc = {
    #'title-page'  : {'Title Page of the Doctrine and Covenants'   : None},
    'introduction': {'Introduction'                               : None},
    'dc'          : {'Doctrine and Covenants'                     : 138 },
    'od'          : {'Official Declaration'                       :  2  },
}

pgp = {
    #'title-page'  : {'Title Page'                                 : None},
    'introduction': {'Introduction'                               : None},
    'moses'       : {'Moses'                                      :  8  },
    'abr'         : {'Abraham'                                    :  5  },
    'js-m'        : {'Joseph Smith-Matthew'                       :  1  },
    'js-h'        : {'Joseph Smith-History'                       :  1  },
    'a-of-f'      : {'Articles of Faith'                          :  1  },
}

standard_works_structure = {
    'Old Testament'         : {'ot'          : ot  },
    'New Testament'         : {'nt'          : nt  },
    'Book of Mormon'        : {'bofm'        : bofm},
    'Doctrine and Covenants': {'dc-testament': dc  },
    'Pearl of Great Price'  : {'pgp'         : pgp },
}

#################################################################################
# Scraping Functions
#################################################################################
def process_verse(verse):
    "Processes a verse in the standard works"
    # Superscripts are removed TODO: integrate superscripts as corpus links
    trim_sups = lambda v: process_raw_web_string(v) if isinstance(v, n_str) else ''.join(
        [
            trim_sups(c)
            for c in v.contents
            if c.name != 'sup'
        ])
    
    return ''.join([trim_sups(c) for c in verse.contents[1:]])

def process_paragraph(paragraph):
    "Processes a paragraph in the standard works"
    return process_raw_web_string(paragraph.text)

def process_chapter(page, source, tags):
    "Processes a chapter from a standard work, given a page from churchofjesuschrist.org"
    name = "/".join([str(s) for s in tags])
    chapter = etree.Element('chapter', name=name, source=source)
    
    try:
        body = page.find('div', **{'class': 'body-block'})
        summary = page.find('p', **{'id': 'study_summary1'})
                
        if summary: # This is a typical verse-based chapter
            chapter.append(etree.Element(
                'summary',
                content = process_raw_web_string(page.find('p', **{'id': 'study_summary1'}).text)
            ))

            for verse in body.find_all('p', **{'class': 'verse'}):
                new = etree.Element('verse', number=verse['id'][1:])
                new.text = process_verse(verse)
                chapter.append(new)
        else:
            for paragraph in body.find_all('p'):
                new = etree.Element('verse', number=paragraph['id'][1:])
                new.text = process_paragraph(paragraph)
                chapter.append(new)
        
    except (TypeError, AttributeError) as e:
        import traceback
        
        escape = lambda s: str(s).replace("&", "&amp;").replace(
            "<", "&lt;").replace(">", "&gt;").replace(
            '"', "&quot;").replace("'", "&apos;")
        
        new = etree.Element(
            'verse',
            number=str(
                len(
                    chapter.xpath('//verse')
                )+1
            )
        )
        new.text = f"Encountered error: {escape(traceback.format_exc())}"
        chapter.append(new)
        tags[0] = 'failures'
    
    return etree.tostring(chapter), tags

def standard_works_urls(structure=standard_works_structure, top=True):
    "Generator consumes nested dicts ending on None/int indicating URL at churchofjesuschrist.org"
        
    for key, value in structure.items():
        if value is None:             # Stand-alone not in a book
            yield None, [key]
        
        elif isinstance(value, int):  # Series of chapters
            for i in range(1, value + 1):
                yield str(i), [key, i]
        
        elif isinstance(value, dict): # Substructure
            for result in standard_works_urls(value, top=False):
                
                if result[0] is None: # URL is prepared
                    url = f"{standard_works_base_url}" if top else f"{key}"
                    keys = result[1]
                else:
                    url = f"{standard_works_base_url}/{result[0]}" if top else f"{key}/{result[0]}"
                    keys = ([key] if top else []) + result[1]
                
                yield url+"?lang=eng" if top else url, keys          
