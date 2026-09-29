# Changelog

All notable changes to this project will be documented in this file.

<!-- insertion marker -->

## 0.2.0 (2026-09-29)

### Added
- File formats for common data science files: TSV, JSON Lines, ORC, XML, HTML
  tables, Markdown tables (save only), fixed-width text (load only), SAS and
  SPSS (load only), YAML, TOML, NumPy (`.npy` and `.npz`), joblib, and JPEG,
  SVG, and PDF figures.
- Optional-dependency extras for the formats (`excel`, `hdf`, `html`, `joblib`,
  `latex`, `markdown`, `numpy`, `orc`, `parquet`, `spss`, `toml`, `xml`,
  `yaml`, and `all`, in addition to `pandas` and `seaborn`).
- Round-trip unit tests for every registered file format.
- Completed README with installation, usage examples, a table of supported
  formats, and instructions for adding custom formats.

### Changed
- Moved packaging from PDM to `uv` and `hatchling`, and updated the repository
  to the snickerdoodle 0.2.3 template (GitHub Actions, pre-commit, dependabot,
  and mkdocs configuration).
- The minimum supported Python version is now 3.11 (3.11 through 3.14 are
  tested).
- `nagata.core` was replaced by `nagata.base`, `nagata.descriptors`,
  `nagata.managers`, and `nagata.utilities`.
- CI now installs dependencies with `uv sync`, runs on Linux, macOS, and
  Windows, and only deploys documentation and creates releases from `main`.

### Fixed
- `FileManager` now creates and validates its input, interim, and output
  folders, and resolves folder names and paths correctly.
- Pickle files are now read and written in binary mode, and `pickle`, `pandas`,
  and `seaborn` no longer raise `NameError` when already imported.
- Loading Excel, Feather, HDF, Parquet, and Stata files no longer fails on
  missing or unsupported default parameters, and JSON, HDF, and Stata loaders
  no longer pass arguments that their pandas readers reject.
- Figures are saved with matplotlib's `savefig` method.
- `type` alias statements no longer prevent the package from importing on
  Python 3.11.
- The mkdocs build works with current `mkdocstrings`.

### Removed
- SQL file format support.

## 0.1.0
    Initial Commit
