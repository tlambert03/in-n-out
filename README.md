# in-n-out

[![License](https://img.shields.io/pypi/l/in-n-out.svg?color=green)](https://github.com/pyapp-kit/in-n-out/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/in-n-out.svg?color=green)](https://pypi.org/project/in-n-out)
[![Python Version](https://img.shields.io/pypi/pyversions/in-n-out.svg?color=green)](https://python.org)
[![CI](https://github.com/pyapp-kit/in-n-out/actions/workflows/ci.yml/badge.svg)](https://github.com/pyapp-kit/in-n-out/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/pyapp-kit/in-n-out/branch/main/graph/badge.svg)](https://app.codecov.io/gh/pyapp-kit/in-n-out)
[![Benchmarks](https://img.shields.io/badge/⏱-codspeed-%23FF7B53)](https://codspeed.io/pyapp-kit/in-n-out)

Python dependency injection you can taste.

A lightweight dependency injection and result processing framework
for Python using type hints. Emphasis is on simplicity, ease of use,
and minimal impact on source code.

```python
import in_n_out as ino


class Thing:
    def __init__(self, name: str):
        self.name = name


# use ino.inject to create a version of the function
# that will retrieve the required dependencies at call time
@ino.inject
def func(thing: Thing):
    return thing.name


def give_me_a_thing() -> Thing:
    return Thing("Thing")


# register a provider of Thing
ino.register_provider(give_me_a_thing)
print(func())  # prints "Thing"


def give_me_another_thing() -> Thing:
    return Thing("Another Thing")


with ino.register_provider(give_me_another_thing, weight=10):
    print(func())  # prints "Another Thing"
```

This also supports processing *return* values as well
(injection of intentional side effects):

```python

@ino.inject_processors
def func2(thing: Thing) -> str:
    return thing.name

def greet_name(name: str):
    print(f"Hello, {name}!")

ino.register_processor(greet_name)

func2(Thing('Bob'))  # prints "Hello, Bob!"
```

### Alternatives

Lots of other python DI frameworks exist, here are a few alternatives to consider:

- <https://github.com/ets-labs/python-dependency-injector>
- <https://github.com/google/pinject>
- <https://github.com/ivankorobkov/python-inject>
- <https://github.com/alecthomas/injector>
- <https://github.com/Finistere/antidote>
- <https://github.com/dry-python/returns>
- <https://github.com/adriangb/di>

## How in-n-out works

The vast majority of logic is in `in_n_out.Store`.

A `Store` maintains a list of provider and processor functions:

- **providers** are functions that should be able to take no arguments,
  and return a value: `ProviderType = Callable[[], Any]`.
  They are the source of the injected values.
- **processors** are functions that should be able to take a single argument,
  and may return anything (though it won't be used by `in-n-out`):
  `ProcessorType = Callable[[Any], Any]`.
  These are responsible for performing side-effects on the return values
  of functions decorated with `@ino.inject_processors`.

### The global `Store`

For convenience, `in-n-out` will create a global `Store` instance. Whenever you use any of the top-level functions like,
`in_n_out.inject`, `in_n_out.inject_processors`, `in_n_out.register_processor`,
or `in_n_out.register_provider`, etc... if you don't provide a specific `store`
argument, the global store will be used.

You can create & use a non-global store by creating a new `Store` instance with
a name: `Store.create("my_store")`; after which you may then pass the name of
the store (or the instance itself) to any top-level `store` arguments:

```python
store = Store.create("my_store")

class Thing:
    ...

@ino.inject(store=store)  # or store="my_store"
def func(thing: Thing):
    return thing.name
```

### Registering providers and processors

To register a provider, use `register_provider` or
`mark_provider` respectively:

```python
import in_n_out as ino

def provide_a_thing() -> Thing:
    return Thing("Thing")

ino.register_provider(provide_a_thing)

# OR -----------

@ino.mark_provider
def provide_a_thing() -> Thing:
    return Thing("Thing")
```

To register a processor, use `register_processor` or
`mark_processor` respectively:

```python
import in_n_out as ino

def process_a_thing(thing: Thing) -> None:
    print(f"Got a thing: {thing}")

ino.register_processor(process_a_thing)

# OR -----------

@ino.mark_processor
def process_a_thing(thing: Thing) -> None:
    print(f"Got a thing: {thing}")
```

> *Side note: `register_provider/processor` returns a context manager that can
> be used to temporarily override the provider for a given type. As such,
> **don't** use `register_provider/processor` as a decorator if you'd like to be
> able to call the function directly.  Instead use `mark_provider/processor`*

### Injecting dependencies

To make use of the registered providers and processors, you can use the
`@inject` and/or `@inject_processors` decorators:

```python
import in_n_out as ino

@ino.inject
def i_need_a_thing(thing: Thing):
    return thing.name
```

When this function is called, `in-n-out` will look for a registered provider
for `Thing`, and if one is found, it will call it to get the value to inject
into the function.

Note that providers *may* be registered after the function is decorated. Dependency providers are looked up at call time, not at decoration time.

### "Injecting" processors (side-effects)

To make use of the registered processors, you can use the
`@inject_processors` decorator:

```python
import in_n_out as ino

@ino.inject_processors
def please_process_my_output() -> Thing:
    return Thing("Thing")
```

When this function is called, `in-n-out` will look for *all* registered
processors for type `Thing`, and call them it to process the
return value of the function.  If you only want to call a single processor,
you can use `inject_processors(first_processor_only=True)` when you decorate
the function.

### Injecting both at the same time

To do both at the same time, you may pass `processors=True` to the `inject`
decorator:

```python
import in_n_out as ino

@ino.inject(processors=True)
def i_need_a_thing_and_want_my_output_processed(thing: Thing) -> int:
    return id(thing)
```
