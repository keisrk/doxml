import docutils.parsers
from docutils import utils, nodes
from xml.etree import ElementTree
from docutils.utils.code_analyzer import Lexer, LexerError

def setup(x, d):
    common_attr = ['ids', 'names', 'dupnames', 'source', 'classes']
    for k, v in x.items():
        if '{' in k and '}' in k:
            pass
        elif k == 'class':
            d['classes'].append(v)
        # Every node.Element shares the common attributes.
        elif k in common_attr:
            d[k].append(v)
        else:
            d[k] = v
    return d

def code_setup(x, d):
    classes = x.attrib.get('classes')
    if classes is not None:
        cls = classes.split()
        language = cls[cls.index('code') + 1]
        if language is not None:
            d['language'] = language
            return setup(x, d)
        else:
            return setup(x, d)
    else:
        return setup(x, d)

node_map = {
    # Title Elements
    'title'          :(lambda x: setup(x, nodes.title())),
    'subtitle'       :(lambda x: setup(x, nodes.subtitle())),
    'rublic'         :(lambda x: setup(x, nodes.rublic())),
    # Bibliographic Elements
    'docinfo'        :(lambda x: setup(x, nodes.docinfo())), 
    'author'         :(lambda x: setup(x, nodes.author())),
    'authors'        :(lambda x: setup(x, nodes.authors())),
    'organization'   :(lambda x: setup(x, nodes.organization())),
    'address'        :(lambda x: setup(x, nodes.address())),
    'contact'        :(lambda x: setup(x, nodes.contact())),
    'version'        :(lambda x: setup(x, nodes.version())),
    'revision'       :(lambda x: setup(x, nodes.revision())),
    'status'         :(lambda x: setup(x, nodes.status())),
    'date'           :(lambda x: setup(x, nodes.date())),
    'copyright'      :(lambda x: setup(x, nodes.copyright())),  
    # Decorative Elements
    'decoration'     :(lambda x: setup(x, nodes.decoration())),
    'header'         :(lambda x: setup(x, nodes.header())),
    'footer'         :(lambda x: setup(x, nodes.footer())),
    # Structural Elements
    'section'        :(lambda x: setup(x, nodes.section())),
    'topic'          :(lambda x: setup(x, nodes.topic())),
    'sidebar'        :(lambda x: setup(x, nodes.sidebar())),
    'transition'     :(lambda x: setup(x, nodes.transition())),
    # Body Elements
    'paragraph'      :(lambda x: setup(x, nodes.paragraph())),
    'compound'       :(lambda x: setup(x, nodes.compound())),
    'container'      :(lambda x: setup(x, nodes.container())),
    'bullet_list'    :(lambda x: setup(x, nodes.bullet_list())),
    'enumerated_list':(lambda x: setup(x, nodes.enumerated_list())),
    'list_item'      :(lambda x: setup(x, nodes.list_item())),
    'definition_list':(lambda x: setup(x, nodes.definition_list())),
    'definition_list_item':(lambda x: setup(x, nodes.definition_list_item())),
    'term'           :(lambda x: setup(x, nodes.term())),  
    'classifier'     :(lambda x: setup(x, nodes.classifier())),
    'definition'     :(lambda x: setup(x, nodes.definition())),
    'field_list'     :(lambda x: setup(x, nodes.field_list())),
    'field'          :(lambda x: setup(x, nodes.field())),
    'field_name'     :(lambda x: setup(x, nodes.field_name())),
    'field_body'     :(lambda x: setup(x, nodes.field_body())),
    'option'         :(lambda x: setup(x, nodes.option())),
    'option_argument':(lambda x: setup(x, nodes.option_argument())),
    'option_group'   :(lambda x: setup(x, nodes.option_group())),
    'option_list'    :(lambda x: setup(x, nodes.option_list())),
    'option_list_item':(lambda x: setup(x, nodes.option_list_item())),
    'option_string'  :(lambda x: setup(x, nodes.option_string())),
    'description'    :(lambda x: setup(x, nodes.description())),
    'literal_block'  :(lambda x: code_setup(x, nodes.literal_block())),
    'doctest_block'  :(lambda x: setup(x, nodes.doctest_block())),
    'math_block'     :(lambda x: setup(x, nodes.math_block())), 
    'line_block'     :(lambda x: setup(x, nodes.line_block())),
    'line'           :(lambda x: setup(x, nodes.line())),
    'block_quote'    :(lambda x: setup(x, nodes.block_quote())),
    'attribution'    :(lambda x: setup(x, nodes.attribution())),
    'attention'      :(lambda x: setup(x, nodes.attention())),
    'caution'        :(lambda x: setup(x, nodes.caution())),
    'danger'         :(lambda x: setup(x, nodes.danger())),
    'error'          :(lambda x: setup(x, nodes.error())),
    'important'      :(lambda x: setup(x, nodes.important())),
    'note'           :(lambda x: setup(x, nodes.note())),
    'tip'            :(lambda x: setup(x, nodes.tip())),
    'hint'           :(lambda x: setup(x, nodes.hint())),
    'warning'        :(lambda x: setup(x, nodes.warning())),
    'admonition'     :(lambda x: setup(x, nodes.admonition())),
    'comment'        :(lambda x: setup(x, nodes.comment())), 
    'substitution_definition':(lambda x: setup(x, nodes.substitution_definition())), 
    'target'         :(lambda x: setup(x, nodes.target())),  
    'footnote'       :(lambda x: setup(x, nodes.footnote())),
    'citation'       :(lambda x: setup(x, nodes.citation())),
    'label'          :(lambda x: setup(x, nodes.label())),
    'figure'         :(lambda x: setup(x, nodes.figure())),
    'caption'        :(lambda x: setup(x, nodes.caption())),
    'legend'         :(lambda x: setup(x, nodes.legend())),
    'table'          :(lambda x: setup(x, nodes.table())),
    'tgroup'         :(lambda x: setup(x, nodes.tgroup())),
    'colspec'        :(lambda x: setup(x, nodes.colspec())),
    'thead'          :(lambda x: setup(x, nodes.thead())),
    'tbody'          :(lambda x: setup(x, nodes.tbody())),
    'row'            :(lambda x: setup(x, nodes.row())),
    'entry'          :(lambda x: setup(x, nodes.entry()))
}
leaf_map = {
    # Inline Elements 
    'emphasis'       :(lambda x: setup(x, nodes.emphasis())),  
    'strong'         :(lambda x: setup(x, nodes.strong())), 
    'literal'        :(lambda x: code_setup(x, nodes.literal())), 
    'reference'      :(lambda x: setup(x, nodes.reference())),  
    'footnote_reference':(lambda x: setup(x, nodes.footnote_reference())), 
    'citation_reference':(lambda x: setup(x, nodes.citation_reference())), 
    'substitution_reference':(lambda x: setup(x, nodes.substitution_reference())), 
    'title_reference':(lambda x: setup(x, nodes.title_reference())), 
    'abbreviation'   :(lambda x: setup(x, nodes.abbreviation())),
    'acronym'        :(lambda x: setup(x, nodes.acronym())),
    'superscript'    :(lambda x: setup(x, nodes.superscript())),
    'subscript'      :(lambda x: setup(x, nodes.subscript())),
    #'math'           :(lambda x: setup(x, nodes.math(latex=x.text)) if x.text is not None else setup(x, nodes.math(latex='\mathit{None}'))),     
    'math'           :(lambda x: setup(x, nodes.math())), 
    'image'          :(lambda x: setup(x, nodes.image())), 
    'inline'         :(lambda x: setup(x, nodes.inline())), 
    'problematic'    :(lambda x: setup(x, nodes.problematic())), 
    'generated'      :(lambda x: setup(x, nodes.generated())),   
    'text'           :(lambda x: setup(x, nodes.Text()))
}
sys_msg = {

    'system_message' :(lambda x: setup(x, nodes.Text()))
}

def txt_add(x, d):
    if not x.text is None:
        t = nodes.Text(x.text)
        d.append(t)            

def tail_add(x, d):
    if not x.tail is None:
        t = nodes.Text(x.tail)
        d.append(t)  
            
def nd_add(x, d):
    if x.tag in leaf_map:
        t = leaf_map[x.tag](x)
        txt_add(x, t)
        d.append(t)
        tail_add(x, d)
    else:
        t = node_map[x.tag](x)
        txt_add(x, t)
        d.append(t)
    return t

def xml_parse(xrt, document):
    for n in xrt:
        t = nd_add(n, document)
        xml_parse(n, t)

def demote_title(xrt):
    assert xrt.tag == 'document'
    doc = ElementTree.Element('document')
    sec = ElementTree.SubElement(doc, 'section')
    for n in xrt:
        if n.tag == 'title':
            sec.set('ids', n.text + 'title')
        sec.append(n)
    return doc

class XmlParser(docutils.parsers.Parser):

    """The xml parser."""

    supported = ('xml')
    """Aliases this parser supports."""

    settings_spec=('Xml Parser Options',
                   None,
                   (('Enable sphinx math extensions',
                     ['--sphinx-ext-enabled'],
                     {'action': 'store_true', 'default': False}),
                   ))
    config_section = 'xml parser'
    config_section_dependencies = ('parsers',)

    def __init__(self, rfc2822=False, inliner=None):
        pass

    def parse(self, inputstring, document):
        """Parse `inputstring` and populate `document`, a document tree."""
        self.setup_parse(inputstring, document) #boilorplate

        xrt = ElementTree.fromstring(self.inputstring)
        """
        if self.document.settings.sphinx_ext_enabled:
            from sphinx.ext import mathbase
            node_map['math_block'] = (lambda x: setup(x, mathbase.displaymath(latex=x.text, number=None, label=None, nowrap=None)))
        else:
            node_map['math_block'] = (lambda x: setup(x, nodes.math_block()))
        """
        if xrt[0].tag == 'title':
            xrt = demote_title(xrt)
        xml_parse(xrt, document)

        self.finish_parse() #boilorplate

'''
from doxml.parser import XmlParser
import docutils

xp = XmlParser()
with open ("src/test01.xml", "r") as myfile:
    data=myfile.read()
settings = docutils.frontend.OptionParser(                 
                components=(docutils.parsers.rst.Parser,)
                ).get_default_values()
document = docutils.utils.new_document(data, settings)
'''

'''
tree = ElementTree.parse('src/test01.xml')
xrt = tree.getroot()
for n in xrt:
     print(n)
doc = demote_title(xrt)
doc[0]
for n in doc[0]:
     print(n)
'''
