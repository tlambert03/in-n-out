from typing import Any, Tuple, Type, Union, get_args, get_origin

try:
    import cython
except ImportError:  # pragma: no cover
    _compiled: bool = False
else:  # pragma: no cover
    try:
        _compiled = cython.compiled
    except AttributeError:
        _compiled = False


def _check_optional(type_: Any) -> Tuple[Type, bool]:
    optional = False
    if get_origin(type_) is Union:
        args = get_args(type_)
        if args and type(None) in args:
            optional = True
            type_ = Union[tuple(x for x in args if x is not type(None))]
    return type_, optional
