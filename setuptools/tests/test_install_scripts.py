"""install_scripts tests
"""

import io
import sys

import pytest

from setuptools.command.install_scripts import install_scripts
from setuptools.dist import Distribution
from . import contexts


class TestInstallScripts:
    @pytest.mark.skipif(sys.platform != 'win32', reason='Windows only')
    def test_executable_escaping_win32(self, tmpdir):
        executable = 'C:\\Program Files\\Python\\python.exe'
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
            bs = cmd.get_finalized_command('build_scripts')
            bs.executable = executable
            cmd.ensure_finalized()
            with contexts.quiet():
                cmd.run()

            with io.open(str(tmpdir.join('foo-script.py')), 'r') as f:
                shebang = f.readline()
        assert shebang == '#!"%s"\n' % executable

    @pytest.mark.skipif(sys.platform == 'win32', reason='non-Windows only')
    def test_executable_escaping_non_win32(self, tmpdir):
        executable = '/usr/bin/env python'
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
            bs = cmd.get_finalized_command('build_scripts')
            bs.executable = executable
            cmd.ensure_finalized()
            with contexts.quiet():
                cmd.run()

            with io.open(str(tmpdir.join('foo')), 'r') as f:
                shebang = f.readline()
        assert shebang == '#!%s\n' % executable
