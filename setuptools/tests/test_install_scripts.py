"""install_scripts tests
"""

import io
import sys

import pytest

from setuptools.command.install_scripts import install_scripts
from setuptools.dist import Distribution
from . import contexts


class TestInstallScripts:
    settings = dict(
        name='foo',
        entry_points={'console_scripts': ['foo=foo:foo']},
        version='0.0',
    )
    unix_exe = '/usr/bin/env python'
    win32_exe = 'C:\\Program Files\\Python 3.3\\python.exe'

    def _run_install_scripts(self, install_dir, executable=None):
        dist = Distribution(self.settings)
        dist.script_name = 'setup.py'
        cmd = install_scripts(dist)
        cmd.install_dir = install_dir
        if executable is not None:
            bs = cmd.get_finalized_command('build_scripts')
            bs.executable = executable
        cmd.ensure_finalized()
        with contexts.quiet():
            cmd.run()

    @pytest.mark.skipif(sys.platform == 'win32', reason='non-Windows only')
    def test_sys_executable_escaping_unix(self, tmpdir, monkeypatch):
        monkeypatch.setattr('sys.executable', self.unix_exe)
        expected = '#!%s\n' % self.unix_exe
        with tmpdir.as_cwd():
            self._run_install_scripts(str(tmpdir))
            with io.open(str(tmpdir.join('foo')), 'r') as f:
                actual = f.readline()
        assert actual == expected

    @pytest.mark.skipif(sys.platform != 'win32', reason='Windows only')
    def test_sys_executable_escaping_win32(self, tmpdir, monkeypatch):
        expected = '#!"%s"\n' % self.win32_exe
        monkeypatch.setattr('sys.executable', self.win32_exe)
        with tmpdir.as_cwd():
            self._run_install_scripts(str(tmpdir))
            with io.open(str(tmpdir.join('foo-script.py')), 'r') as f:
                actual = f.readline()
        assert actual == expected

    @pytest.mark.skipif(sys.platform == 'win32', reason='non-Windows only')
    def test_executable_escaping_unix(self, tmpdir):
        expected = '#!%s\n' % self.unix_exe
        with tmpdir.as_cwd():
            self._run_install_scripts(str(tmpdir), self.unix_exe)
            with io.open(str(tmpdir.join('foo')), 'r') as f:
                actual = f.readline()
        assert actual == expected

    @pytest.mark.skipif(sys.platform != 'win32', reason='Windows only')
    def test_executable_escaping_win32(self, tmpdir):
        expected = '#!"%s"\n' % self.win32_exe
        with tmpdir.as_cwd():
            self._run_install_scripts(str(tmpdir), self.win32_exe)
            with io.open(str(tmpdir.join('foo-script.py')), 'r') as f:
                actual = f.readline()
        assert actual == expected
