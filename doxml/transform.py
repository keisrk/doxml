from docutils import nodes, transforms
from docutils.parsers.rst import Parser
from docutils.utils import new_document
from sphinx import addnodes
from sphinx.ext import mathbase

class SphinxExtMathEnv(transforms.Transform):
    """Transform math env to sphinx ext math env."""
    def __init__(self, *args, **kwargs):
        transforms.Transform.__init__(self, *args, **kwargs)
        self.reporter = self.document.reporter
        self.config = self.default_config.copy()
        try:
            new_cfg = self.document.settings.env.config.doxml_config
            self.config.update(new_cfg)
        except AttributeError:
            pass

    default_priority = 1
    default_config = {
        'enable_sphinx_ext_math_env': False,
        'doxml_suffixes': ['.xml']
    }
    def math_env_replace(self, node):
        math = None
        if isinstance(node, nodes.math_block):
            math = mathbase.displaymath(latex=node.astext(), number=None, label=None, nowrap=None)
        else:
            math = mathbase.math(latex=node.astext(), number=None, label=None, nowrap=None)
        return math

    def traverse(self, node):
        """Traverse the document tree rooted at node.
        node : docutil node
            current root node to traverse
        """
        to_visit = []
        to_replace = []
        for c in node.children[:]:
            if isinstance(c, nodes.math_block) or isinstance(c, nodes.math):
                newnode = self.math_env_replace(c)
                to_replace.append((c, newnode))
            else:
                to_visit.append(c)

        for old, new in to_replace:
            node.replace(old, new)
        for child in to_visit:
            self.traverse(child)

    def apply(self):
        """Apply the transformation by configuration."""
        source = self.document['source']

        self.reporter.info('SphinxExtMathEnv: %s' % source)
        # only transform doxml
        if not source.endswith(tuple(self.config['doxml_suffixes'])):
            return
        self.traverse(self.document)
