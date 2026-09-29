"""Round-trip tests for the built-in file formats."""

from __future__ import annotations

import pathlib

import pytest

import nagata


@pytest.fixture
def manager(tmp_path: pathlib.Path) -> nagata.FileManager:
    """Returns a `FileManager` that reads and writes in a temp folder."""
    return nagata.FileManager(root_folder = tmp_path)


@pytest.fixture
def dataframe() -> object:
    """Returns a small dataframe."""
    pd = pytest.importorskip('pandas')
    return pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})


def test_registered_formats() -> None:
    """Tests that all formats and their extensions are registered."""
    formats = nagata.FileFramework.formats
    for key in (
        'csv', 'excel', 'feather', 'fixed_width', 'hdf', 'html', 'joblib',
        'jpeg', 'json', 'json_lines', 'latex', 'markdown', 'npy', 'npz', 'orc',
        'parquet', 'pdf', 'pickle', 'png', 'sas', 'spss', 'stata',
        'svg', 'text', 'toml', 'tsv', 'xml', 'yaml'):
        assert key in formats
    extensions = nagata.FileManager().extensions
    assert extensions['tsv'] == 'tsv'
    assert extensions['yml'] == 'yaml'
    assert extensions['jsonl'] == 'json_lines'


def test_pickle_round_trip(manager: nagata.FileManager) -> None:
    """Tests pickling, including when `pickle` was already imported."""
    item = {'a': [1, 2, 3]}
    manager.save(item, file_name = 'item.pkl')
    assert manager.load(file_name = 'item.pkl') == item


@pytest.mark.parametrize('name', ['data.csv', 'data.tsv', 'data.jsonl'])
def test_dataframe_text_formats(
    manager: nagata.FileManager,
    dataframe: object,
    name: str) -> None:
    """Tests dataframe formats that need no optional dependencies."""
    manager.save(dataframe, file_name = name, index = False)
    loaded = manager.load(file_name = name)
    assert loaded['a'].tolist() == [1, 2, 3]
    assert loaded['b'].tolist() == ['x', 'y', 'z']


def test_tsv_uses_tabs(
    manager: nagata.FileManager,
    dataframe: object,
    tmp_path: pathlib.Path) -> None:
    """Tests that TSV files are tab-delimited."""
    manager.save(dataframe, file_name = 'data.tsv', index = False)
    assert '\t' in (tmp_path / 'data.tsv').read_text().splitlines()[0]


@pytest.mark.parametrize(
    ('name', 'module'),
    [
        ('data.parquet', 'pyarrow'),
        ('data.orc', 'pyarrow'),
        ('data.feather', 'pyarrow'),
        ('data.xml', 'lxml'),
        ('data.html', 'lxml'),
        ('data.xlsx', 'openpyxl')])
def test_dataframe_optional_formats(
    manager: nagata.FileManager,
    dataframe: object,
    name: str,
    module: str) -> None:
    """Tests dataframe formats that need an optional dependency."""
    pytest.importorskip(module)
    kwargs = {'index': False} if name.endswith(('.xml', '.html', '.xlsx')) else {}
    manager.save(dataframe, file_name = name, **kwargs)
    loaded = manager.load(file_name = name)
    assert loaded['a'].tolist() == [1, 2, 3]
    assert loaded['b'].tolist() == ['x', 'y', 'z']


def test_markdown_save_only(
    manager: nagata.FileManager,
    dataframe: object,
    tmp_path: pathlib.Path) -> None:
    """Tests saving a markdown table and that loading is unsupported."""
    pytest.importorskip('tabulate')
    manager.save(dataframe, file_name = 'table.md')
    assert '|' in (tmp_path / 'table.md').read_text()
    with pytest.raises(NotImplementedError):
        manager.load(file_name = 'table.md')


def test_fixed_width_load_only(
    manager: nagata.FileManager,
    tmp_path: pathlib.Path) -> None:
    """Tests loading a fixed-width file and that saving is unsupported."""
    pytest.importorskip('pandas')
    (tmp_path / 'data.fwf').write_text('a  b\n1  x\n2  y\n')
    loaded = manager.load(file_name = 'data.fwf')
    assert loaded['a'].tolist() == [1, 2]
    with pytest.raises(NotImplementedError):
        manager.save(loaded, file_name = 'out.fwf')


def test_yaml_round_trip(manager: nagata.FileManager) -> None:
    """Tests saving and loading YAML."""
    pytest.importorskip('yaml')
    item = {'name': 'nagata', 'values': [1, 2, 3]}
    manager.save(item, file_name = 'config.yaml')
    assert manager.load(file_name = 'config.yaml') == item


def test_toml_round_trip(manager: nagata.FileManager) -> None:
    """Tests saving and loading TOML."""
    pytest.importorskip('tomli_w')
    item = {'name': 'nagata', 'values': [1, 2, 3]}
    manager.save(item, file_name = 'config.toml')
    assert manager.load(file_name = 'config.toml') == item


def test_numpy_round_trip(manager: nagata.FileManager) -> None:
    """Tests saving and loading `.npy` and `.npz` files."""
    numpy = pytest.importorskip('numpy')
    array = numpy.arange(6).reshape(2, 3)
    manager.save(array, file_name = 'array.npy')
    assert (manager.load(file_name = 'array.npy') == array).all()
    manager.save({'x': array, 'y': array * 2}, file_name = 'arrays.npz')
    loaded = manager.load(file_name = 'arrays.npz')
    assert (loaded['y'] == array * 2).all()
    manager.save(array, file_name = 'single.npz')
    assert (manager.load(file_name = 'single.npz')['arr_0'] == array).all()


def test_joblib_round_trip(manager: nagata.FileManager) -> None:
    """Tests saving and loading with joblib."""
    pytest.importorskip('joblib')
    item = {'a': [1, 2, 3]}
    manager.save(item, file_name = 'model.joblib')
    assert manager.load(file_name = 'model.joblib') == item


@pytest.mark.parametrize('name', ['plot.png', 'plot.jpg', 'plot.svg', 'plot.pdf'])
def test_figure_formats(
    manager: nagata.FileManager,
    tmp_path: pathlib.Path,
    name: str) -> None:
    """Tests saving matplotlib figures to image formats."""
    pytest.importorskip('seaborn')
    figure_module = pytest.importorskip('matplotlib.figure')
    figure = figure_module.Figure()
    figure.subplots().plot([1, 2, 3])
    manager.save(figure, file_name = name)
    assert (tmp_path / name).stat().st_size > 0


def test_text_round_trip(manager: nagata.FileManager) -> None:
    """Tests saving and loading plain text, with and without a format."""
    manager.save('line one' + chr(10) + 'line two', file_name = 'notes.txt')
    assert manager.load(file_name = 'notes.txt') == 'line one' + chr(10) + 'line two'
    manager.save('abc', file_name = 'plain', file_format = 'text')
    assert manager.load(file_name = 'plain', file_format = 'text') == 'abc'


def test_json_round_trip(manager: nagata.FileManager, dataframe: object) -> None:
    """Tests saving and loading JSON."""
    manager.save(dataframe, file_name = 'data.json')
    loaded = manager.load(file_name = 'data.json')
    assert loaded['a'].tolist() == [1, 2, 3]
    assert loaded['b'].tolist() == ['x', 'y', 'z']


def test_json_lines_file_layout(
    manager: nagata.FileManager,
    dataframe: object,
    tmp_path: pathlib.Path) -> None:
    """Tests that JSON Lines files hold one record per line."""
    manager.save(dataframe, file_name = 'data.jsonl')
    lines = (tmp_path / 'data.jsonl').read_text().splitlines()
    assert len(lines) == 3
    assert lines[0].startswith('{')


def test_stata_round_trip(manager: nagata.FileManager, dataframe: object) -> None:
    """Tests saving and loading Stata files."""
    manager.save(dataframe, file_name = 'data.dta')
    loaded = manager.load(file_name = 'data.dta')
    assert loaded['a'].tolist() == [1, 2, 3]
    assert loaded['b'].tolist() == ['x', 'y', 'z']


def test_hdf_round_trip(manager: nagata.FileManager, dataframe: object) -> None:
    """Tests saving and loading HDF5 files."""
    pytest.importorskip('tables')
    manager.save(dataframe, file_name = 'data.h5', key = 'df', file_format = 'hdf')
    loaded = manager.load(
        file_name = 'data.h5', key = 'df', file_format = 'hdf')
    assert loaded['a'].tolist() == [1, 2, 3]


def test_latex_save_only(
    manager: nagata.FileManager,
    dataframe: object,
    tmp_path: pathlib.Path) -> None:
    """Tests saving a LaTeX table and that loading is unsupported."""
    pytest.importorskip('jinja2')
    manager.save(dataframe, file_name = 'table.latex')
    assert 'tabular' in (tmp_path / 'table.latex').read_text()
    with pytest.raises(NotImplementedError):
        manager.load(file_name = 'table.latex')


def test_sas_load(manager: nagata.FileManager, tmp_path: pathlib.Path) -> None:
    """Tests loading a SAS transport file and that saving is unsupported."""
    pd = pytest.importorskip('pandas')
    pyreadstat = pytest.importorskip('pyreadstat')
    pyreadstat.write_xport(
        pd.DataFrame({'a': [1.0, 2.0]}),
        str(tmp_path / 'data.xpt'),
        file_format_version = 5)
    loaded = manager.load(file_name = 'data.xpt')
    assert loaded['a'].tolist() == [1.0, 2.0]
    with pytest.raises(NotImplementedError):
        manager.save(loaded, file_name = 'out.xpt')


def test_spss_load(manager: nagata.FileManager, tmp_path: pathlib.Path) -> None:
    """Tests loading an SPSS file and that saving is unsupported."""
    pd = pytest.importorskip('pandas')
    pyreadstat = pytest.importorskip('pyreadstat')
    pyreadstat.write_sav(
        pd.DataFrame({'a': [1.0, 2.0]}), str(tmp_path / 'data.sav'))
    loaded = manager.load(file_name = 'data.sav')
    assert loaded['a'].tolist() == [1.0, 2.0]
    with pytest.raises(NotImplementedError):
        manager.save(loaded, file_name = 'out.sav')


def test_html_returns_first_table(
    manager: nagata.FileManager,
    dataframe: object,
    tmp_path: pathlib.Path) -> None:
    """Tests that loading HTML returns a single dataframe."""
    pytest.importorskip('lxml')
    manager.save(dataframe, file_name = 'table.html', index = False)
    loaded = manager.load(file_name = 'table.html')
    assert list(loaded.columns) == ['a', 'b']


def test_unknown_extension_and_format(manager: nagata.FileManager) -> None:
    """Tests errors for unrecognized extensions and format names."""
    with pytest.raises(KeyError):
        manager.load(file_name = 'data.unknown')
    with pytest.raises(KeyError):
        manager.load(file_name = 'data', file_format = 'not_a_format')


def test_every_format_has_extensions_and_methods() -> None:
    """Tests that each registered format is complete."""
    for name, file_format in nagata.FileFramework.formats.items():
        assert file_format.extensions, name
        assert callable(file_format.load), name
        assert callable(file_format.save), name
