from jinja2 import Environment

from rnet93dd.templating import init_custom, create_environment as base_create_environment


BUILTIN_EXTENSIONS = []

EXTENSIONS = init_custom('extensions', __name__)
FILTERS    = init_custom('filters',    __name__)
GLOBALS    = init_custom('globals',    __name__)
POLICIES   = init_custom('policies',   __name__)
TESTS      = init_custom('tests',      __name__)

ENVIRONMENT_SETTINGS = {
    'builtin_extensions': BUILTIN_EXTENSIONS,
    'extensions': EXTENSIONS,
    'filters': FILTERS,
    'globals_': GLOBALS,
    'policies': POLICIES,
    'tests': TESTS,
}


def create_environment() -> Environment:
    return base_create_environment(__name__, **ENVIRONMENT_SETTINGS)
