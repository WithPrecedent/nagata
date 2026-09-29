# nagata

| | |
| --- | --- |
| Version | [![PyPI Latest Release](https://img.shields.io/pypi/v/nagata.svg?style=for-the-badge&color=steelblue&label=PyPI&logo=PyPI&logoColor=yellow)](https://pypi.org/project/nagata/) [![GitHub Latest Release](https://img.shields.io/github/v/tag/WithPrecedent/nagata?style=for-the-badge&color=navy&label=GitHub&logo=github)](https://github.com/WithPrecedent/nagata/releases)
| Status | [![Build Status](https://img.shields.io/github/actions/workflow/status/WithPrecedent/nagata/ci.yml?branch=main&style=for-the-badge&color=cadetblue&label=Tests&logo=pytest)](https://github.com/WithPrecedent/nagata/actions/workflows/ci.yml?query=branch%3Amain) [![Development Status](https://img.shields.io/badge/Development-Active-seagreen?style=for-the-badge&logo=git)](https://www.repostatus.org/#active) [![Project Stability](https://img.shields.io/pypi/status/nagata?style=for-the-badge&logo=pypi&label=Stability&logoColor=yellow)](https://pypi.org/project/nagata/)
| Documentation | [![Hosted By](https://img.shields.io/badge/Hosted_by-Github_Pages-blue?style=for-the-badge&color=navy&logo=github)](https://WithPrecedent.github.io/nagata)
| Tools | [![Documentation](https://img.shields.io/badge/MkDocs-magenta?style=for-the-badge&color=deepskyblue&logo=markdown&labelColor=gray)](https://squidfunk.github.io/mkdocs-material/) [![Linter](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/charliermarsh/Ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/Ruff) [![Dependency Manager](https://img.shields.io/badge/uv-mediumpurple?style=for-the-badge&logo=uv&labelColor=gray)](https://docs.astral.sh/uv/) [![Pre-commit](https://img.shields.io/badge/pre--commit-darkolivegreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=gray)](https://github.com/TezRomacH/python-package-template/blob/master/.pre-commit-config.yaml) [![CI](https://img.shields.io/badge/GitHub_Actions-navy?style=for-the-badge&logo=githubactions&labelColor=gray&logoColor=white)](https://github.com/features/actions) [![Editor Settings](https://img.shields.io/badge/Editor_Config-paleturquoise?style=for-the-badge&logo=editorconfig&labelColor=gray)](https://editorconfig.org/) [![Repository Template](https://img.shields.io/badge/snickerdoodle-bisque?style=for-the-badge&logo=cookiecutter&labelColor=gray)](https://www.github.com/WithPrecedent/nagata) [![Dependency Maintainer](https://img.shields.io/badge/dependabot-navy?style=for-the-badge&logo=dependabot&logoColor=white&labelColor=gray)](https://github.com/dependabot)
| Compatibility | [![Compatible Python Versions](https://img.shields.io/pypi/pyversions/nagata?style=for-the-badge&color=steelblue&label=Python&logo=python&logoColor=yellow)](https://pypi.python.org/pypi/nagata/) [![Linux](https://img.shields.io/badge/Linux-lightseagreen?style=for-the-badge&logo=linux&labelColor=gray&logoColor=white)](https://www.linux.org/) [![MacOS](https://img.shields.io/badge/MacOS-snow?style=for-the-badge&logo=apple&labelColor=gray)](https://www.apple.com/macos/) [![Windows](https://img.shields.io/badge/windows-blue?style=for-the-badge&logo=Windows&labelColor=gray&color=orangered)](https://www.microsoft.com/en-us/windows?r=1)
| Stats | [![PyPI Download Rate (per month)](https://img.shields.io/pypi/dm/nagata?style=for-the-badge&color=steelblue&label=Downloads%20💾&logo=pypi&logoColor=yellow)](https://pypi.org/project/nagata) [![GitHub Stars](https://img.shields.io/github/stars/WithPrecedent/nagata?style=for-the-badge&color=navy&label=Stars%20⭐&logo=github)](https://github.com/WithPrecedent/nagata/stargazers) [![GitHub Contributors](https://img.shields.io/github/contributors/WithPrecedent/nagata?style=for-the-badge&color=navy&label=Contributors%20🙋&logo=github)](https://github.com/WithPrecedent/nagata/graphs/contributors) [![GitHub Issues](https://img.shields.io/github/issues/WithPrecedent/nagata?style=for-the-badge&color=navy&label=Issues%20📘&logo=github)](https://github.com/WithPrecedent/nagata/graphs/contributors) [![GitHub Forks](https://img.shields.io/github/forks/WithPrecedent/nagata?style=for-the-badge&color=navy&label=Forks%20🍴&logo=github)](https://github.com/WithPrecedent/nagata/forks)
| | |

-----

## What is nagata?

*This package is under heavy construction. Use at your own risk*

`nagata` is a small Python package for loading and saving files with one
common, intuitive syntax. Instead of remembering `pandas.read_parquet`,
`yaml.safe_load`, `numpy.load`, `pickle.load`, and so on, you create a
`FileManager` once and call `load` and `save`. `nagata` picks the right reader
or writer from the file extension and resolves folders for you.

<p align="center">
<img src="https://media.giphy.com/media/PsDjz6KasrK3l6MFAm/giphy.gif" alt="I came to help you." style="width:300px;"/>
</p>

*"Don’t decide for them. Tell them the truth and let them decide for themselves."* - Naomi Nagata

## Why use nagata?

* **One syntax for many formats:** `load` and `save` work the same way for
  tabular data, arrays, configuration files, figures, and pickled objects.
* **Format detection:** the file extension selects the format. You can also
  name the format explicitly.
* **Project folders:** set a root, input, interim, and output folder once and
  refer to them by name (`'input'`, `'output'`) or just by file name.
* **Shared defaults:** settings such as text encoding and index handling live
  in one place (`FileFramework.settings`) and are applied to every format.
* **Extensible:** subclass `FileFormat` and your format is registered
  automatically.
* **Light by default:** `nagata` only imports `pandas`, `numpy`, `pyyaml`, and
  the other libraries when you use a format that needs them.

You may not want `nagata` if you need lazy or out-of-core loading, remote
storage (S3, GCS, etc.), or fine-grained control over every reader option in
the underlying libraries. For those cases, use those libraries (or something
like [`fsspec`](https://filesystem-spec.readthedocs.io/)) directly. `nagata`
does let you pass any extra keyword arguments through to the underlying
reader or writer.

## Getting started

### Requirements

`nagata` requires Python 3.11 or later and runs on Linux, macOS, and Windows.
It is tested on Python 3.11 through 3.14. Its only required dependency is
[`wonka`](https://github.com/WithPrecedent/wonka). Support for most file
formats relies on optional third-party libraries, described below.

### Installation

To install `nagata`, use `pip`:

```sh
pip install nagata
```

Formats that rely on other libraries need those libraries installed. You can
install them yourself or use one of `nagata`'s extras:

```sh
pip install "nagata[pandas]"   # CSV, TSV, JSON, JSON Lines, Stata
pip install "nagata[excel]"    # Excel (pandas and openpyxl)
pip install "nagata[parquet]"  # Parquet and Feather (pandas and pyarrow)
pip install "nagata[all]"      # everything below
```

| Extra | Installs | Enables |
| --- | --- | --- |
| `pandas` | `pandas` | CSV, TSV, JSON, JSON Lines, Stata, fixed-width, SAS |
| `excel` | `pandas`, `openpyxl` | Excel |
| `hdf` | `pandas`, `tables` | HDF5 |
| `parquet` | `pandas`, `pyarrow` | Parquet, Feather |
| `orc` | `pandas`, `pyarrow` | ORC |
| `latex` | `pandas`, `jinja2` | LaTeX tables (saving) |
| `spss` | `pandas`, `pyreadstat` | SPSS |
| `xml` | `pandas`, `lxml` | XML |
| `html` | `pandas`, `lxml` | HTML tables |
| `markdown` | `pandas`, `tabulate` | Markdown tables (saving) |
| `numpy` | `numpy` | NumPy `.npy` and `.npz` |
| `yaml` | `pyyaml` | YAML |
| `toml` | `tomli-w` | TOML saving (loading uses the standard library) |
| `joblib` | `joblib` | Joblib |
| `seaborn` | `seaborn` | PNG, JPEG, SVG, and PDF figures |

Text, pickle, and TOML loading need nothing beyond the standard library.

### Usage

Create a `FileManager` with the folders for your project. Relative folder
names are placed inside the root folder, and any folders that do not exist are
created.

```python
import nagata

files = nagata.FileManager(
    root_folder = 'project',
    input_folder = 'raw',
    output_folder = 'processed')
```

#### Loading and saving

The file extension tells `nagata` which format to use. By default, files are
loaded from the input folder and saved to the output folder.

```python
df = files.load(file_name = 'survey.csv')        # project/raw/survey.csv
files.save(df, file_name = 'survey.parquet')     # project/processed/survey.parquet
```

Additional keyword arguments are passed to the underlying library:

```python
df = files.load(file_name = 'survey.csv', usecols = ['age', 'income'])
files.save(df, file_name = 'survey.csv', index = True)
```

> [!WARNING]
> By default, CSV, Excel, and other pandas-based loaders read at most 1,000
> rows, taken from the `test_size` setting. To load every row, pass
> `nrows = None`, or change the default with
> `nagata.FileFramework.settings['test_size'] = None`.

#### Choosing folders

Pass `folder` to use a different location. It can be the name of one of the
manager's folders (`'input'`, `'interim'`, `'output'`, `'root'`), or a folder
name inside the root folder.

```python
df = files.load(file_name = 'survey', file_format = 'parquet', folder = 'output')
files.save(df, file_name = 'survey_backup.csv', folder = 'root')
```

Or skip the folder logic and pass a complete path (the folder must already
exist):

```python
df = files.load(file_path = 'project/raw/survey.csv')
files.save(df, file_path = 'project/processed/survey.tsv')
```

#### Different kinds of data

The same two methods work for configuration files, arrays, models, and figures.

```python
files.save({'seed': 42, 'folds': 5}, file_name = 'params.yaml')
params = files.load(file_name = 'params.yaml', folder = 'output')

files.save(features, file_name = 'features.npy')       # NumPy array
files.save(model, file_name = 'model.joblib')          # fitted scikit-learn model
files.save(figure, file_name = 'accuracy.png')         # matplotlib or seaborn figure
files.save(notes, file_name = 'notes.txt')             # plain text
```

#### Supported file formats

| Format | Extensions | Load | Save |
| --- | --- | :---: | :---: |
| CSV | `csv` | ✅ | ✅ |
| TSV | `tsv`, `tab` | ✅ | ✅ |
| Excel | `xlsx`, `xls` | ✅ | ✅ |
| JSON | `json` | ✅ | ✅ |
| JSON Lines | `jsonl`, `ndjson` | ✅ | ✅ |
| Parquet | `parquet` | ✅ | ✅ |
| Feather | `feather` | ✅ | ✅ |
| ORC | `orc` | ✅ | ✅ |
| HDF5 | `hdf`, `hdf5` | ✅ | ✅ |
| Stata | `dta` | ✅ | ✅ |
| XML | `xml` | ✅ | ✅ |
| HTML tables | `html`, `htm` | ✅ | ✅ |
| LaTeX tables | `latex` | | ✅ |
| Markdown tables | `md`, `markdown` | | ✅ |
| Fixed-width text | `fwf` | ✅ | |
| SAS | `sas7bdat`, `xpt` | ✅ | |
| SPSS | `sav` | ✅ | |
| YAML | `yaml`, `yml` | ✅ | ✅ |
| TOML | `toml` | ✅ | ✅ |
| NumPy array | `npy` | ✅ | ✅ |
| NumPy archive | `npz` | ✅ | ✅ |
| Joblib | `joblib` | ✅ | ✅ |
| Pickle | `pickle`, `pkl` | ✅ | ✅ |
| Text | `txt`, `text` | ✅ | ✅ |
| Figures | `png`, `jpg`, `jpeg`, `svg`, `pdf` | | ✅ |

You can see every registered format with `nagata.FileFramework.formats`. If a
file has no extension, or the extension is not the one you want, pass
`file_format` with the format's name (for example, `file_format = 'json_lines'`).

#### Adding your own format

Subclassing `FileFormat` registers the new format automatically. Give it the
extension(s) it handles and `load` and `save` methods:

```python
import dataclasses
import pathlib
from typing import ClassVar

import nagata


@dataclasses.dataclass
class FileFormatShout(nagata.FileFormat):
    """Stores text in upper case and loads it in lower case."""

    extensions: ClassVar[str] = 'shout'
    load_parameters: ClassVar[dict] = {}
    save_parameters: ClassVar[dict] = {}

    def load(self, path, **kwargs):
        return pathlib.Path(path).read_text().lower()

    def save(self, item, path, **kwargs):
        pathlib.Path(path).write_text(item.upper())


files = nagata.FileManager(root_folder = 'project')
files.save('hello', file_name = 'greeting.shout')
files.load(file_name = 'greeting.shout')  # 'hello'
```

`load_parameters` and `save_parameters` map an argument of your `load` or `save`
method to a key in `nagata.FileFramework.settings`, so that shared defaults such
as `'file_encoding'` are applied automatically. The built-in CSV format is a
good example.


<p align="center">
<img src="https://media.giphy.com/media/Aay77tMwvrmiuXuGPo/giphy.gif" alt="There are other ways." style="width:300px;"/>
</p>


## Contributing

Contributors are always welcome. Feel free to grab an [issue](https://www.github.com/WithPrecedent/nagata/issues) to work on or make a suggested improvement. If you wish to contribute, please read the [Contribution Guide](https://www.github.com/WithPrecedent/nagata/contributing.md) and [Code of Conduct](https://www.github.com/WithPrecedent/nagata/code_of_conduct.md).

## Similar Projects

`nagata` builds on, and is not a replacement for, the excellent libraries it
wraps. If it is not quite what you need, these projects solve related problems:

* [pandas I/O](https://pandas.pydata.org/docs/user_guide/io.html): the reader
  and writer functions that `nagata` uses for most tabular formats.
* [fsspec](https://filesystem-spec.readthedocs.io/): a uniform interface to
  local and remote filesystems.
* [Kedro's Data Catalog](https://docs.kedro.org/en/stable/data/data_catalog.html)
  and [Intake](https://intake.readthedocs.io/): declarative catalogs of datasets
  for larger data pipelines.
* [joblib](https://joblib.readthedocs.io/): efficient persistence for Python
  objects, including large NumPy arrays and fitted models.

## Acknowledgments

Thanks to the maintainers and contributors of pandas, NumPy, seaborn and
matplotlib, PyYAML, joblib, and the other open-source libraries that do the
heavy lifting behind `nagata`'s formats. The quotation at the top of this
README is from James S. A. Corey's *The Expanse* series.

## License

Use of this repository is authorized under the [Apache Software License 2.0](https://www.github.com/WithPrecedent/nagata/blog/main/LICENSE).
