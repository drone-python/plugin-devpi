#!/usr/bin/env python
"""
Everything needed to publish Python modules to a DevPi server.

Recommended reading: http://doc.devpi.net/latest/quickstart-releaseprocess.html
"""
import sys
import subprocess

import plugin_input

# devpi uses a 'clientdir' arg to determine where to store state. We make
# this overridable below to facilitate the integration test process.
DEFAULT_CLIENTDIR = '/tmp/devpi-clientdir'


def die_on_error(f):
    """
    Since this plugin wraps the devpi client's CLI, we do a lot of the same
    error handling. We don't capture stdout/stderr, so they get emitted.
    This decorator just finishes the job and kills the build (by exiting).
    """
    def wrapped(*args, **kwargs):
        result = f(*args, **kwargs)
        if result.returncode == 1:
            sys.exit(1)
    return wrapped


@die_on_error
def select_server(server, clientdir=DEFAULT_CLIENTDIR):
    """
    Before the devpi CLI can do much of anything, it has to be pointed at the
    root of a devpi server.

    :param str server: Absolute URI to the root of a devpi server (not an
        index within the devpi server).
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run(['devpi', 'use', '--clientdir', clientdir, server])


@die_on_error
def login(username, password, clientdir=DEFAULT_CLIENTDIR):
    """
    Uploading packages to a devpi server usually requires an authenticated
    account with write permissions.

    :param str username: The devpi username we'll be uploading as.
    :param str password: The devpi user's password.
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run([
        'devpi', 'login', '--clientdir', clientdir,
        username, '--password', password])


@die_on_error
def select_index(index, clientdir=DEFAULT_CLIENTDIR):
    """
    Before we can upload a package to an index, we must select it since there's
    no one-shot select + upload command.

    :param str index: The index to upload to. For example, ``root/devpitest``.
        This gets appended to whatever ``server`` value gets passed into
        :py:func:`select_server`.
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run(['devpi', 'use', '--clientdir', clientdir, index])


@die_on_error
def create_index(index, clientdir=DEFAULT_CLIENTDIR):
    """
    Creates an index on the devpi server.

    :param str index: The index to create. For example, ``root/devpitest``.
        This gets appended to whatever ``server`` value gets passed into
        :py:func:`select_server`.
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run([
        'devpi', 'index', '--clientdir', clientdir, '-c', index])


@die_on_error
def upload_package(path, clientdir=DEFAULT_CLIENTDIR):
    """
    Upload the package in the CWD to the currently selected devpi
    server + index.

    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    cmd = subprocess.Popen([
        'devpi', 'upload', '--clientdir', clientdir,
        '--from-dir', '--no-vcs'], cwd=path)
    cmd.wait()
    return cmd


def main():
    plugin_input.values.load_values()

    select_server(plugin_input.values['SERVER'])
    login(plugin_input.values['USERNAME'], plugin_input.values['PASSWORD'])
    select_index(plugin_input.values['INDEX'])
    upload_package(plugin_input.values['PACKAGE_PATH'])

if __name__ == "__main__":
    main()
