#####
doxml
#####

Parser for docutils' internal XML.

In the conf.py
::
   from doxml.parser import XmlParser

   source_parsers = {
       '.xml': XmlParser,
   }

   source_suffix = ['.rst', '.xml']
