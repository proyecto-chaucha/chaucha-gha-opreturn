import inspect


def debug(message = ""):
    stack = inspect.stack()
    here = stack[0]
    file, line, func = here[1:4]
    print(f"::debug file={file},line={line}::{message}")

def warn(message = ""):
    stack = inspect.stack()
    here = stack[0]
    file, line, func = here[1:4]
    print(f"::warning file={file},line={line}::{message}")

def error(message = ""):
    stack = inspect.stack()
    here = stack[0]
    file, line, func = here[1:4]
    print(f"::error file={file},line={line}::{message}")

def output(name, value):
    print(f"::set-output name={name}::{value}")

def add_mask(value):
    print(f"::add-mask::{value}")