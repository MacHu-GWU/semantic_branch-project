# -*- coding: utf-8 -*-

from semantic_branch import api


def test():
    _ = api
    _ = api.InvalidSemanticNameError
    _ = api.is_valid_semantic_name
    _ = api.ensure_is_valid_semantic_name
    _ = api.is_certain_semantic_branch
    _ = api.SemanticStubEnum
    _ = api.SemanticBranch
    _ = api.SemanticBranchEnum


if __name__ == "__main__":
    from semantic_branch.tests import run_cov_test

    run_cov_test(
        __file__,
        "semantic_branch.api",
        preview=False,
    )
