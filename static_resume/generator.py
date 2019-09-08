import sys
import os
import yaml
import jinja2
import typing
import shutil

from pathlib import Path

try:
    from importlib.machinery import SourceFileLoader
except ImportError:
    pass

try:
    import imp
except ImportError:
    pass

try:
    import importlib.util
except ImportError:
    pass


import static_resume


def load_python_module(path: Path):
    """Load a python module (credits to https://stackoverflow.com/a/67692)

    :param path: path to the module
    """

    module_name, script_path = str(path.parent), str(path.name)
    if sys.version_info <= (3, 2):
        module_obj = imp.load_source(module_name, script_path)
    elif sys.version_info < (3, 5):
        module_obj = SourceFileLoader(module_name, script_path).load_module()
    else:
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module_obj = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_obj)

    return module_obj


class GenError(Exception):
    pass


class Generator:
    """Generator for the resume
    """

    def __init__(self):
        print('This is {}, version {}'.format(static_resume.__name__, static_resume.__version__))

        self.config = static_resume.DEFAULT_CONFIG
        self.base_template = jinja2.Template(static_resume.BASE_TEMPLATE)
        self.template = jinja2.Template('{% extends base_template %}')

        self.data = {}
        self.exts = self.config['INTERNAL_EXTS'].copy()

    @staticmethod
    def act_on_file(
            f: [str, Path], callback: typing.Callable[[Path], typing.Any] = None, typ: str = 'file') -> typing.Any:
        """
        Raises GenError if file is missing, use callback on it otherwise

        :param f: file path
        :param callback: callback to call if file exists
        :param typ: type
        """

        if type(f) is str:
            p = Path(f)
        else:
            p = f

        print('- {} `{}`'.format(typ, p))

        if not p.exists():
            raise GenError('missing {} `{}`'.format(typ, p))
        else:
            if callback:
                return callback(p)

    def generate(self, conf_file: str = static_resume.CONFIG_FILE, remove_dir=False) -> None:
        """Generate the whole stuffs into OUTPUT_DIR

        :param conf_file: config file
        :param remove_dir: clean directory
        """

        print('Generating ...\n')

        # load config file and update `self.config` if any
        config_module = Generator.act_on_file(
            Path(os.getcwd(), conf_file),
            lambda p: load_python_module(p),
            'config')

        if 'CONFIG' in config_module.__dict__:
            self.config.update(config_module.CONFIG)

        if 'EXTS' in self.config:
            self.exts.update(self.config['EXTS'])

        # load data
        if 'DATA_FILE' in self.config:
            self.data = Generator.act_on_file(
                self.config['DATA_FILE'],
                lambda p: yaml.load(p.open().read(), Loader=yaml.Loader),
                'data')

        # load template (in any)
        if 'TEMPLATE_FILE' in self.config:
            self.template = Generator.act_on_file(
                self.config['TEMPLATE_FILE'],
                lambda p: jinja2.Template(p.open().read()),
                'template')

        # create directory
        output_dir_path = Path(self.config['OUTPUT_DIR'])
        if output_dir_path.exists():
            if remove_dir:
                shutil.rmtree(output_dir_path)
                output_dir_path.mkdir()
        else:
            output_dir_path.mkdir()

        # copy style if any
        if 'STYLE_FILE' in self.config:
            Generator.act_on_file(
                self.config['STYLE_FILE'],
                lambda p: shutil.copy(p, output_dir_path / 'style.css'),
                'style')

        # copy assets if any
        def copy_dir_or_fail(p):
            if not p.is_dir():
                raise GenError('`{}` is not a directory'.format(p))
            else:
                shutil.copytree(p, output_dir_path / p.name())

        if 'ASSETS_DIR' in self.config:
            Generator.act_on_file(self.config['ASSETS_DIR'], copy_dir_or_fail, 'assets')

        # generate output file
        print('- index `{}`'.format(self.config['OUTPUT_FILE']))

        context = {'base_template': self.base_template}

        if self.data:  # create context
            for key, value in self.data.items():
                print('  - using ext `{}`'.format(key))

                if key not in self.exts:
                    raise GenError('missing ext `{}`'.format(key))
                else:
                    context.update(self.exts[key](key, value))

        with (output_dir_path / self.config['OUTPUT_FILE']).open('w') as f:  # write file
            f.write(self.template.render(**context))

        print('\n... Generated in `{}`'.format(output_dir_path))
