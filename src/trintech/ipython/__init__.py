

from typing import List


def public(dir_: List[str]) -> List[str]:
    return [e for e in dir_ if not e.startswith('_')]

p = public  # alias
