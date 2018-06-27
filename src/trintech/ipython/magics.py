

from IPython.core.getipython import get_ipython
from IPython.core.magic import Magics, line_magic, magics_class


LINE_MAGICS = []
CELL_MAGICS = []
LINE_CELL_MAGICS = []
MAGICS = []
STATEFUL_MAGICS = []  # assumes that all have `__init__(self, shell)`


@magics_class
class PDir(Magics):
    @line_magic
    def pdir(self, line):
        return sorted(e for e in self.shell.user_ns.keys() if not e.startswith('_'))

MAGICS.append(PDir)


def load_ipython_extension(ipython):
    for fun in LINE_MAGICS:
        ipython.register_magic_function(fun, 'line')
    for fun in CELL_MAGICS:
        ipython.register_magic_function(fun, 'cell')
    for fun in LINE_CELL_MAGICS:
        ipython.register_magic_function(fun, 'line_cell')
    for cls in MAGICS:
        ipython.register_magics(cls)
    for cls in STATEFUL_MAGICS:
        magics = cls.__init__(ipython)
        ipython.register_magics(magics)

if __name__ == '__main__':
    ipython = get_ipython()
    load_ipython_extension(ipython)
