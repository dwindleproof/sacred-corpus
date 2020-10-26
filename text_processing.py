from lxml import etree

#################################################################################
# Text Processing Functions
#################################################################################
replacements = { # Replacements for processing raw web strings from unicode
    'â\x80\x94'         : ' - ' , # Long m dash
    'â\x80\x99'         : "'"   , # Apostrophe : ’
    'Â¶ '               : ''    , # Paragraph mark : ¶
    'Ã¦'                : 'ae'  , # Diphthong ae: æ
    'Ã'                : 'Ae'  , # Capitalized Ae: Æ
    'Â\xa0'             : ' '   , # Link artifact in D&C introduction TODO: understand better
    'â\x80\x9c'         : '"'   , # Opening quote: “
    'â\x80\x9d'         : '"'   , # Closing quote: ”
    'â\x80¦'            : '...' , # Elipsis: …
    'â\x80\x93'         : '-'   , # Dash for scripture references: –
    'â\x80\x98'         : "'"   , # Opening single quote: ‘
    'Â©'                : '(C)' , # Copyright Mark: ©

}

def process_raw_web_string(s):
    "Processes raw unicode strings from curchofjesuschrist.org"
    for old, new in replacements.items():
        s = s.replace(old, new)
    
    return s

# Escape a python string to be XML compatible
escape = lambda s: str(s).replace("&", "&amp;").replace(
    "<", "&lt;").replace(">", "&gt;").replace(
    '"', "&quot;").replace("'", "&apos;")

# Unescape an escaped string using escape
unescape = lambda s: str(s).replace("&amp;", "&").replace(
    "&lt;", "<").replace("&gt;", ">").replace(
    "&quot;", '"').replace("&apos;", "'")

def flatten(xml):
    "Iteratively Renders XML as a unicode string"
    if isinstance(xml, bytes):
        return flatten(etree.fromstring(xml))
    
    return (
        xml.text if xml.text is not None else ''
    ) + ' '.join([
        flatten(x)
        for x in xml
        if isinstance(x, etree._Element)
    ])
