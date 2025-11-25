# glambie-playground

Code playground for GlaMBIE-2 pilot studies (https://glambie.org/glambie-2). The main GlaMBIE code is managed by Earthwave at https://github.com/earthwave/glambie.

## Structure

* `data/`: Directory for storing the shared data files (ignored by `git` and omitted from this repository).
* [`environment.yaml`](environment.yaml): Conda environment specification file.
* [`helpers/`](helpers): Directory for shared helper modules.
  * `__init__.py`: Marks the directory as a Python package so that modules can be imported as `import helpers.{module}`.
  * `example.py`: Example helper module.
* [`example/`](example): Example project directory. Each project should create their own top-level directory similar to this one.
  * `__init__.py`: Marks the directory as a Python package so that modules therein can be imported as `import example.{module}` (which also limits directory and file names to a–z, A–Z, 0–9, and underscore).
  * `README.md`: Example project readme.
  * `script.py`: Example project script.

## Installation

_Tip: Use [`mamba`](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) instead of `conda` for faster installation._

Create and activate the Python `glambie-playground` conda environment:

```bash
conda env create --file environment.yaml
conda activate glambie-playground
```

Update the environment with changes to `environment.yaml`:

```bash
conda env update --file environment.yaml --prune
```

## Contribution guidelines

### Paths

Write your Python files (`*.py`) and Jupyter notebooks (`*.ipynb`) to run from the top-level directory.

For example, `example/script.py` uses the helper module `helpers/example.py` by importing it as `import helpers.example`. This works if you run the script from the top-level directory:

```bash
python -m example.script
# Hello, world!
```

But fails if you run it from within the `example` directory:

```bash
cd example
python -m script
# ModuleNotFoundError: No module named 'helpers'
```

Similarly, if there were an `example/otherscript.py`, import it in `example/script.py` as `import example.otherscript`, not `import otherscript`. Data files should likewise be accessed relative to the top-level directory, as `data/...`.

### Code style

* Comment your code to explain _why_ you did something (the code already answers _what_). Use descriptive names to make your code as self-explanatory as possible.

* Describe the project's goals, structure, and usage in the project's `README.md`. In Jupyter notebooks, make generous use of markdown cells to provide context.

* Write functions (classes, etc) as general as possible, filing them under `helpers` when they are likely to be reused across projects. Document each function and class method (at minimum) with a docstring that describes what it does, the purpose and type of each input, and the return value. Consider using [type annotations](https://typing.python.org/en/latest/spec/annotations.html) to make types explicit and machine-readable. See this [numpydoc-style](https://mkdocstrings.github.io/griffe/reference/docstrings/#numpydoc-style) for inspiration.

  ```python
  def do_something(a: int, b: float | None = None) -> float:
    """
    This function does something.

    Parameters
    ----------
    a
      The first parameter.
  
    b
      The second parameter.
    
    Returns
    -------
    :
      The result of the operation.
    """
    return b if b is not None else float(a)
  ```

* Script constants should be distinguished using `UPPER_SNAKE_CASE` (instead of `lower_snake_case`) and also described by a docstring.

  ```python
  DENSITY_FACTOR: tuple[float, float] = 0.85, 0.06
  """Density of ice (mean, sigma) relative to water (1000 kg m-3)."""
  ```
