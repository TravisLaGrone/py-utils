from importlib import import_module
from itertools import accumulate
from typing import Dict, List, Tuple, Any, Optional

from jinja2 import Environment, PackageLoader

PUNCTUATION_PAIRS: List[Tuple[str, str]] = [
    ('(', ')'),
    ('{', '}'),
    ('[', ']'),
    ('<', '>'),
    ('"', '"'),
    ("'", "'"),
    ('`', '`'),
    ('"""', '"""'),
    ("'''", "'''"),
    ('```', '```'),
    ('/**', '*/'),
    ('/*', '*/'),
    ('(*', '*)'),
    ('<!--', '-->'),
    ('<!---', '--->'),
    ('BEGIN', 'END'),
    ('{%', '%}'),
    ('{#', '#}'),
    ('{{', '}}'),
    ('{{{', '}}}'),
]
PUNCTUATION_PAIRS_LEFT_TO_RIGHT: Dict[str, str] = {l:r for l,r in PUNCTUATION_PAIRS}
PUNCTUATION_PAIRS_RIGHT_TO_LEFT: Dict[str, str] = {r:l for l,r in PUNCTUATION_PAIRS}



def get_parent_qualname(qualname: str) -> str:
    return qualname.rpartition('.')[0]


def get_ancestor_qualnames(qualname: [str]) -> List[str]:
    # TODO: input validation
    if qualname == '__main__':
        return []
    parent_qualname = qualname.rpartition('.')[0]
    parent_names = parent_qualname.split('.')
    ancestors = accumulate(parent_names, lambda a,b: '.'.join(a,b))
    return list(ancestors).reverse()


def make_submodule_name(
        submodule: str,
        package: str
) -> str:
    """Intended to use within "__init__.py" and pass `package=__name__`."""
    if package == '__name__':
        name = submodule
    else:
        name = '.'.join([package, submodule])
    return name


def safe_import_from(
        name: str,
        module: str,
        package: Optional[str]=None,
        default: Optional[Any]=None
) -> Optional[Any]:
    try:
        imported_module = import_module(module, package) if package else import_module(module)
        imported_name = imported_module.__getattribute__(name)
    except (ImportError, AttributeError):
        return default
    else:
        return imported_name


def init_custom(
        category: str,
        template_subpackage: str
) -> Dict[str, Any]:
    """Intended to be called from `*/template/__init__.py` and pass `template_subpackage=__name__`."""
    module = make_submodule_name(category.lower(), template_subpackage)
    return safe_import_from(category.upper(), module, default={})


def create_environment(
        template_subpackage: str,
        builtin_extensions: List[str] = [],
        extensions: Dict[str, Any] = {},
        filters: Dict[str, Any] = {},
        globals_: Dict[str, Any] = {},
        policies: Dict[str, Any] = {},
        tests: Dict[str, Any] = {},
) -> Environment:
    """Intended to use within "__init__.py" and pass `template_subpackage=__name__`."""
    env = Environment(
        loader=PackageLoader(
            package_name='templates',
            package_path=get_parent_qualname(template_subpackage),
        ),
        extensions=builtin_extensions,
    )
    for ext in extensions:
        env.add_extension(ext)
    env.filters.update(filters)
    env.globals.update(globals_)
    env.policies.update(policies)
    env.tests.update(tests)
    return env
