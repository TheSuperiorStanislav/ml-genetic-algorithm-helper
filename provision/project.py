from invoke import task

from . import common, git

##############################################################################
# Build project locally
##############################################################################

__all__ = (
    "init",
    "install_tools",
    "compile_requirements",
)


@task
def init(context):
    """Build project from scratch"""
    common.print_success("Setting up git")
    git.hooks(context)

    common.print_success("Initial assembly of all dependencies")
    install_tools(context)

    common.print_success("Installing requirements")
    sync_requirements(context)

    common.print_success("Setup done")


##############################################################################
# Manage dependencies
##############################################################################
@task
def install_tools(context):
    """Install shell/cli dependencies, and tools needed to install requirements

    """
    context.run("pip install -U pip setuptools pip-tools wheel")


@task
def sync_requirements(context, env="local"):
    """Install requirements."""
    common.print_success("Install requirements")
    context.run(f"pip-sync requirements/{env}.txt")


@task
def compile_requirements(context, update=False):
    """Recompile dependencies."""
    common.print_success("Compile requirements with pip-compile")
    update = "-U" if update else ""
    envs = (
        "local",
        "remote",
    )
    for env in envs:
        common.print_success(f"Compile requirements for {env=}.")
        context.run(f"pip-compile -q requirements/{env}.in {update}")
