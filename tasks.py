import os
import sys
from importlib import util

from invoke import Collection

from provision import git, linters, project

ns = Collection(
    git,
    linters,
    project,
)

# Configurations for run command
# https://github.com/pyinvoke/invoke/issues/561
is_pty_enabled = True if sys.platform.startswith('linux') else False
ns.configure(
    dict(
        run=dict(
            pty=is_pty_enabled,
            echo=True
        )
    )
)

# let's load custom commands defined in
# ~/.invoke/my.py

sys.path.append(os.path.expanduser("~/.invoke"))

spec = util.find_spec("my")

# load custom invoke commands in the case such
# file exists
if spec:
    zzz = util.module_from_spec(spec)
    spec.loader.exec_module(zzz)
