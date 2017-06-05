__version__ = '0.1'

def setup():
    """Initialize Sphinx extension."""
    from .parser import XmlParser
    app.add_source_parser('.xml', XmlParser)  # needs Sphinx >= 1.4
    return {'version': __version__, 'parallel_read_safe': False}
