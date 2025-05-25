# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from semantic_branch.tests import run_cov_test

    run_cov_test(
        __file__,
        "semantic_branch",
        is_folder=True,
        preview=False,
    )
