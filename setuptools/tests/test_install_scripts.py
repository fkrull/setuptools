"""install_scripts tests
"""

import io
import sys

import pytest

from setuptools.command.install_scripts import install_scripts
from setuptools.dist import Distribution
from . import contexts


@pytest.yield_fixture
def sys_executable_with_space(monkeypatch):
    e = 'C:\\Program Files\\Python\\python.exe'
    monkeypatch.setattr('sys.executable', e)
    yield e


class TestInstallScripts:
    @pytest.mark.skipif(sys.platform != 'win32',
                        reason='Only makes sense on Windows')
    def test_sys_executable_with_space(self, tmpdir, sys_executable_with_space):
        settings = dict(
            name='foo',
            entry_points={'console_scripts': ['foo=foo:foo']},
            version='0.0',
        )
        with tmpdir.as_cwd():
            dist = Distribution(settings)
            dist.script_name = 'setup.py'
            cmd = install_scripts(dist)
            cmd.install_dir = str(tmpdir)
            cmd.ensure_finalized()
            with contexts.quiet():
                cmd.run()

            with io.open(str(tmpdir.join('foo-script.py')), 'r') as f:
                shebang = f.readline()
        assert shebang == '#!"%s"\n' % sys_executable_with_space
