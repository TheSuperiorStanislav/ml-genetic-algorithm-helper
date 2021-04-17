from invoke import Exit, task

from . import common, linters

__all__ = (
    "hooks",
    "pre_commit",
    "pre_push",
)


@task
def hooks(context):
    """Install git hooks."""
    common.print_success("Setting up GitHooks")
    context.run("git config core.hooksPath .git-hooks")


@task
def pre_commit(context):
    """Perform pre commit check"""
    common.print_success("Perform pre-commit check")
    try:
        linters.all_git_staged(context)
    except Exit as e:
        common.print_error(
            "Style check failed\n"
            "Commit aborted due to errors - pls fix them first!"
        )
        raise e
    common.print_success("Wonderful JOB! Thank You!")


@task
def pre_push(context):
    """Perform pre push check"""
    common.print_success("Perform pre-push check")
    code_style_passed = True
    try:
        linters.all(context)
    except Exit:
        common.print_warn("Code style checks failed")
        code_style_passed = False
    if not all((code_style_passed, )):
        common.print_error("Push aborted due to errors\nPLS fix them first!")
        raise Exit(code=1)
    common.print_success("Wonderful JOB! Thank You!")
