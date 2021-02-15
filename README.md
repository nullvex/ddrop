# ddrop - distributed drop system in python 

The ddrop (distributed drop) allows a sharer and a sharee to exchange digital information in a very secure and private fashion. ddrop uses multiple mechanisms and multiple clouds to allow users to set and forget private informaton that only people they give certain keys, will be able to obtain. 

#Sharing Flow
Sharer Provided File -> ddrop -> encyrypted archive -> multiple file parts -> multiple object store providers > sharers_file.ddrop

Sharer -> sharers_file.ddrop -> Sharee

Sharer -> passphrase -> Sharee

#Retrieval Flow
Sharee -> ddrop with passphrase and sharers_file.ddrop -> fetches encryption hash(es) -> retrieves file(s) from cloud -> combines files -> decryption using hash(s). -> Destroy hash keys




### Project Dependencies


#### Installing ddrop 



#### Installing this Projects' Dependencies


### Running Unit Tests

All test have been written using the [PyTest](https://docs.pytest.org/en/latest/) package. Tests are kept in the `tests` folder and can be run from the command line by - e.g. by invoking,

```bash
pipenv run pytest
```

The test suite is structured as an independent Python package as follows:

```bash
tests/
 |-- test_data/
 |   |-- supply_demand_data.json
 |   __init__.py
 |   conftest.py
 |   test_curves.py
```

The `conftest.py` module is used by PyTest - in this particular instance for loading test data and building objects that will then be used by potentially many other tests. These are referred to as 'fixtures' in PyTest - more details can be found [here](https://docs.pytest.org/en/latest/fixture.html).

### Linting Code

I prefer to use [flake8](http://flake8.pycqa.org/en/latest/) for style guide enforcement. This can be invoked from the command line by running,

```bash
pipenv run flake8 py_pkg
```

Flake8 could easily be swapped-out for another tool by using Pipenv as described above.

### Static Type Checking

We have used the Python type annotation framework, together with the [MyPy package](http://mypy-lang.org), to perform static type checks on the codebase. Analogous to any linter or unit testing framework, MyPy can be run from the command line as follows,

```bash
pipenv run python -m mypy py_pkg/*.py
```

MyPy options for this project can be defined in the `mypy.ini` file that MyPy will look for by default. For more information on the full set of options, see the [mypy documentation](https://mypy.readthedocs.io/en/stable/config_file.html).

Examples of type annotation and type checking for library development can be found in the `py_pkg.curves.py` module. This should also be cross-referenced with the improvement to readability (and usability) that this has on package documentation.

### Documentation

The documentation in the `docs` folder has been built using [Sphinx](http://www.sphinx-doc.org). We have used the default 'quickstart' automatic configuration, which was originally triggered by executing,

```bash
pipenv run sphinx-quickstart
```

The output is based primarily on the Docstrings in the source code, using the `autodoc` extension within Sphinx (specified during the 'quickstart'). The contents for the entry point into the docs (`index.html`), is defined in the `index.rst` file, which itself imports the `modules.rst` file that lists all of the modules to document. The documentation can be built by running the following command,

```bash
pipenv run sphinx-build -b html docs/source docs/build_html
```

The resulting HTML documentation can be accessed by opening `docs/build_html/index.html` in a web browser.

My preferred third party theme from [Read the Docs](https://readthedocs.org) has also been used, by installing the `sphinx_rtd_theme` as a development dependency and modifying `docs/source/config.py` as follows:

```python
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```

#### Creating a PDF Version Using LaTeX

So long as a LaTex distribution is present on your system (e.g. MikTeX for Mac OS X), then it is possible to create a PDF version of the documentation, as well. Start by building the prerequisite LaTex version from the ReStructured Text originals,

```bash
pipenv run sphinx-build -b latex docs/source docs/build_latex
```

Then, navigate to `docs/build_latex` and run,

```bash
make
```

Both LaTeX and PDF versions can then be found in `docs/build_latex`.

### Building Deployable Distributions

The recommended (and most pragmatic) way of deploy this package is to build a Python [wheel](https://wheel.readthedocs.io/en/stable/) and to then to install it in a fresh virtual environment on the target system. The exact build configuration is determined by the parameters in `setup.py`. Note, that this requires that all package dependencies also be specified in the `install_requires` declaration in `setup.py`, **regardless** of their entry in `Pipfile`. For more information on Python packaging refer to the [Python Packaging User Guide](https://packaging.python.org) and the accompanying [sample project](https://github.com/pypa/sampleproject). To create the Python wheel run,

```bash
pipenv run python setup.py bdist_wheel
```

This will create `build`, `py_package_template.egg-info` and `dist` directories - the wheel can be found in the latter. This needs to be copied to the target system (which we are assuming has Python and Pipenv available as a minimum), where it can be installed into a new virtual environment, together with all downstream dependencies, using,

```bash
pipenv install path/to/your-package.whl
```

### Automated Testing and Deployment using Travis CI

We have chosen Travis for Continuous Integration (CI) as it integrates very easily with Python and GitHub (where I have granted it access to my public repositories). The configuration details are kept in the `.travis.yaml` file in the root directory:

```yaml
ncsudo: required

language: python

python:
  - 3.7-dev

install:
  - pip install pipenv
  - pipenv install --dev

script:
  - pipenv run pytest

deploy:
  provider: pypi
  user: alexioannides
  password:
    secure: my-encrypted-pypi-password
  on:
    tags: true
  distributions: bdist_wheel
```

Briefly, this instructs the Travis build server to:

1. download, build and install Python 3.7;
2. install Pipenv
3. use Pipenv and `Pipfile.lock` to install **all** dependencies (dev dependencies are necessary for running PyTest);
4. run all unit tests using PyTest;
5. if the tests were run successfully and if we have pushed a new tag (i.e. a release) to the master branch then:
    - build a Python wheel; and,
    - push it to PyPI.org using my PyPI account credentials.

Note that we provide Travis with an encrypted password, that was made using the Travis command line tool (downloaded using HomeBrew on OS X). For more details on this and PyPI deployment more generally see the [Travis CI documentation](https://docs.travis-ci.com/user/deployment/pypi/#stq=&stp=0).
