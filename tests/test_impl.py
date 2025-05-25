# -*- coding: utf-8 -*-

import pytest

from semantic_branch.impl import (
    InvalidSemanticNameError,
    semantic_name_charset,
    is_valid_semantic_name,
    ensure_is_valid_semantic_name,
    is_certain_semantic_branch,
    SemanticStubEnum,
    SemanticBranch,
    SemanticBranchEnum,
)

VALID_SEMANTIC_NAMES = [
    "main",
    "feature",
    "feat",
    "dev",
    "test123",
    "build2",
    "a",
]
INVALID_SEMANTIC_NAMES = [
    "",
    "123abc",
    "1",
    "feature-123",
    "Feature",
    "MAIN",
    "dev_branch",
    "release@1.2.3",
    "dev/description",
    "test branch",
    "fix-hotfix",
    "branch.name",
    "branch+name",
]


class TestSemanticNameValidation:
    """Test semantic name validation functions."""

    def test_semantic_name_charset(self):
        """Test that semantic_name_charset contains expected characters."""
        # Should contain a-z and 0-9
        assert "a" in semantic_name_charset
        assert "z" in semantic_name_charset
        assert "0" in semantic_name_charset
        assert "9" in semantic_name_charset
        # Should not contain uppercase, special chars, or spaces
        assert "A" not in semantic_name_charset
        assert "-" not in semantic_name_charset
        assert "_" not in semantic_name_charset
        assert "/" not in semantic_name_charset
        assert " " not in semantic_name_charset

    def test_is_valid_semantic_name(self):
        """Test semantic name validation with various inputs."""
        for name in VALID_SEMANTIC_NAMES:
            assert is_valid_semantic_name(name) is True
        for name in INVALID_SEMANTIC_NAMES:
            assert is_valid_semantic_name(name) is False

    def test_ensure_is_valid_semantic_name_success(self):
        """Test ensure_is_valid_semantic_name with valid names."""
        # Should return the same value for valid names
        for name in VALID_SEMANTIC_NAMES:
            assert ensure_is_valid_semantic_name(name) == name

    def test_ensure_is_valid_semantic_name_failure(self):
        """Test ensure_is_valid_semantic_name with invalid names."""
        for name in INVALID_SEMANTIC_NAMES:
            with pytest.raises(InvalidSemanticNameError) as exc_info:
                ensure_is_valid_semantic_name(name)
            assert f"{name!r} is not a valid semantic name" in str(exc_info.value)


class TestIsCertainSemanticBranch:
    """Test the core is_certain_semantic_branch function with feature branches as primary examples."""

    def test_exact_match_feature_branches(self):
        """Test exact matches for feature branch names."""
        feature_stubs = ["feat", "feature"]

        # Exact matches should return True
        assert is_certain_semantic_branch("feat", feature_stubs) is True
        assert is_certain_semantic_branch("feature", feature_stubs) is True

    def test_case_insensitive_feature_branches(self):
        """Test case insensitive matching for feature branches."""
        feature_stubs = ["feat", "feature"]

        # Case variations should all work
        assert is_certain_semantic_branch("FEAT", feature_stubs) is True
        assert is_certain_semantic_branch("Feat", feature_stubs) is True
        assert is_certain_semantic_branch("fEaT", feature_stubs) is True
        assert is_certain_semantic_branch("FEATURE", feature_stubs) is True
        assert is_certain_semantic_branch("Feature", feature_stubs) is True
        assert is_certain_semantic_branch("FeatuRE", feature_stubs) is True

    def test_whitespace_handling_feature_branches(self):
        """Test whitespace handling for feature branches."""
        feature_stubs = ["feat", "feature"]

        # Leading/trailing whitespace should be stripped
        assert is_certain_semantic_branch(" feat", feature_stubs) is True
        assert is_certain_semantic_branch("feat ", feature_stubs) is True
        assert is_certain_semantic_branch(" feat ", feature_stubs) is True
        assert is_certain_semantic_branch("  feature  ", feature_stubs) is True

    def test_dash_separator_feature_branches(self):
        """Test dash separator handling for feature branches."""
        feature_stubs = ["feat", "feature"]

        # Everything after dash should be ignored
        assert is_certain_semantic_branch("feat-123", feature_stubs) is True
        assert is_certain_semantic_branch("feat-abc", feature_stubs) is True
        assert is_certain_semantic_branch("feat-user-auth", feature_stubs) is True
        assert is_certain_semantic_branch("feature-123", feature_stubs) is True
        assert is_certain_semantic_branch("feature-add-login", feature_stubs) is True
        assert is_certain_semantic_branch("feature-v2", feature_stubs) is True

    def test_slash_separator_feature_branches(self):
        """Test slash separator handling for feature branches."""
        feature_stubs = ["feat", "feature"]

        # Everything after slash should be ignored
        assert is_certain_semantic_branch("feat/description", feature_stubs) is True
        assert (
            is_certain_semantic_branch("feat/add-this-feature", feature_stubs) is True
        )
        assert (
            is_certain_semantic_branch("feat/user/auth/system", feature_stubs) is True
        )
        assert is_certain_semantic_branch("feature/add-login", feature_stubs) is True
        assert (
            is_certain_semantic_branch("feature/v2/improvements", feature_stubs) is True
        )

    def test_combined_separators_feature_branches(self):
        """Test combined dash and slash separators for feature branches."""
        feature_stubs = ["feat", "feature"]

        # Dash takes precedence, then slash
        assert is_certain_semantic_branch("feat-123/description", feature_stubs) is True
        assert (
            is_certain_semantic_branch("feature-abc/add-login", feature_stubs) is True
        )
        assert is_certain_semantic_branch("feat-v2/user/auth", feature_stubs) is True

    def test_no_match_feature_branches(self):
        """Test cases where feature branch names don't match."""
        feature_stubs = ["feat", "feature"]

        # Different semantic names should return False
        assert is_certain_semantic_branch("main", feature_stubs) is False
        assert is_certain_semantic_branch("master", feature_stubs) is False
        assert is_certain_semantic_branch("dev", feature_stubs) is False
        assert is_certain_semantic_branch("fix", feature_stubs) is False
        assert is_certain_semantic_branch("release", feature_stubs) is False
        assert is_certain_semantic_branch("build", feature_stubs) is False

    def test_partial_match_feature_branches(self):
        """Test partial matches that should return False."""
        feature_stubs = ["feat", "feature"]

        # Partial matches should not work
        assert is_certain_semantic_branch("fea", feature_stubs) is False
        assert is_certain_semantic_branch("featur", feature_stubs) is False
        assert is_certain_semantic_branch("features", feature_stubs) is False
        assert is_certain_semantic_branch("featx", feature_stubs) is False

    def test_empty_inputs_feature_branches(self):
        """Test edge cases with empty inputs."""
        feature_stubs = ["feat", "feature"]

        # Empty branch name should return False
        assert is_certain_semantic_branch("", feature_stubs) is False

        # Empty stubs should return False
        assert is_certain_semantic_branch("feat", []) is False

    def test_invalid_stubs_raise_error(self):
        """Test that invalid stubs raise InvalidSemanticNameError."""
        # Invalid stubs should raise errors
        with pytest.raises(InvalidSemanticNameError):
            is_certain_semantic_branch("feat", ["feat-123"])

        with pytest.raises(InvalidSemanticNameError):
            is_certain_semantic_branch("main", ["dev/branch"])

    def test_duplicate_stubs(self):
        """Test behavior with duplicate stubs."""
        # Duplicates should be handled gracefully (converted to set)
        assert is_certain_semantic_branch("feat", ["feat", "feat", "feature"]) is True
        assert (
            is_certain_semantic_branch("feature", ["feat", "feature", "feature"])
            is True
        )

    def test_various_semantic_branches(self):
        """Test a few other semantic branches to ensure general functionality."""
        # Test main branches
        main_stubs = ["main", "master"]
        assert is_certain_semantic_branch("main", main_stubs) is True
        assert is_certain_semantic_branch("master", main_stubs) is True
        assert is_certain_semantic_branch("main-backup", main_stubs) is True
        assert is_certain_semantic_branch("master/description", main_stubs) is True

        # Test fix branches
        fix_stubs = ["fix", "hotfix"]
        assert is_certain_semantic_branch("fix", fix_stubs) is True
        assert is_certain_semantic_branch("hotfix", fix_stubs) is True
        assert is_certain_semantic_branch("fix-urgent", fix_stubs) is True
        assert is_certain_semantic_branch("hotfix/security", fix_stubs) is True


class TestSemanticStubEnum:
    """Test SemanticStubEnum values."""

    def test_essential_stubs(self):
        """Test essential semantic stubs."""
        assert SemanticStubEnum.main.value == "main"
        assert SemanticStubEnum.master.value == "master"

    def test_use_case_stubs(self):
        """Test use case based semantic stubs."""
        assert SemanticStubEnum.feat.value == "feat"
        assert SemanticStubEnum.feature.value == "feature"
        assert SemanticStubEnum.build.value == "build"
        assert SemanticStubEnum.doc.value == "doc"
        assert SemanticStubEnum.fix.value == "fix"
        assert SemanticStubEnum.hotfix.value == "hotfix"
        assert SemanticStubEnum.rls.value == "rls"
        assert SemanticStubEnum.release.value == "release"
        assert SemanticStubEnum.clean.value == "clean"
        assert SemanticStubEnum.cleanup.value == "cleanup"

    def test_environment_stubs(self):
        """Test environment based semantic stubs."""
        assert SemanticStubEnum.sbx.value == "sbx"
        assert SemanticStubEnum.sandbox.value == "sandbox"
        assert SemanticStubEnum.dev.value == "dev"
        assert SemanticStubEnum.develop.value == "develop"
        assert SemanticStubEnum.tst.value == "tst"
        assert SemanticStubEnum.test.value == "test"
        assert SemanticStubEnum.int.value == "int"
        assert SemanticStubEnum.stg.value == "stg"
        assert SemanticStubEnum.stage.value == "stage"
        assert SemanticStubEnum.staging.value == "staging"
        assert SemanticStubEnum.qa.value == "qa"
        assert SemanticStubEnum.preprod.value == "preprod"
        assert SemanticStubEnum.prd.value == "prd"
        assert SemanticStubEnum.prod.value == "prod"
        assert SemanticStubEnum.blue.value == "blue"
        assert SemanticStubEnum.green.value == "green"


class TestSemanticBranch:
    """Test SemanticBranch class."""

    def test_semantic_branch_creation(self):
        """Test SemanticBranch creation and basic functionality."""
        feature_branch = SemanticBranch(name="feature", stubs=["feat", "feature"])

        assert feature_branch.name == "feature"
        assert feature_branch.stubs == ["feat", "feature"]

    def test_semantic_branch_is_it_method(self):
        """Test SemanticBranch.is_it method."""
        feature_branch = SemanticBranch(name="feature", stubs=["feat", "feature"])

        # Should work like is_certain_semantic_branch
        assert feature_branch.is_match("feat") is True
        assert feature_branch.is_match("feature") is True
        assert feature_branch.is_match("feat-123") is True
        assert feature_branch.is_match("feature/description") is True
        assert feature_branch.is_match("main") is False
        assert feature_branch.is_match("fix") is False


class TestSemanticBranchEnum:
    """Test SemanticBranchEnum functionality."""

    def test_enum_structure(self):
        """Test that all expected enum values exist."""
        assert SemanticBranchEnum.main.value.name == "main"
        assert SemanticBranchEnum.feature.value.name == "feature"
        assert SemanticBranchEnum.build.value.name == "build"
        assert SemanticBranchEnum.doc.value.name == "doc"
        assert SemanticBranchEnum.fix.value.name == "fix"
        assert SemanticBranchEnum.release.value.name == "release"
        assert SemanticBranchEnum.cleanup.value.name == "cleanup"
        assert SemanticBranchEnum.sandbox.value.name == "sandbox"
        assert SemanticBranchEnum.develop.value.name == "develop"
        assert SemanticBranchEnum.test.value.name == "test"
        assert SemanticBranchEnum.int.value.name == "int"
        assert SemanticBranchEnum.staging.value.name == "staging"
        assert SemanticBranchEnum.qa.value.name == "qa"
        assert SemanticBranchEnum.preprod.value.name == "preprod"
        assert SemanticBranchEnum.prod.value.name == "prod"
        assert SemanticBranchEnum.blue.value.name == "blue"
        assert SemanticBranchEnum.green.value.name == "green"

    def test_feature_branch_enum(self):
        """Test feature branch enum specifically."""
        feature_enum = SemanticBranchEnum.feature

        assert isinstance(feature_enum.value, SemanticBranch)
        assert feature_enum.value.name == "feature"
        assert feature_enum.value.stubs == ["feat", "feature"]

        # Test the is_it method
        assert feature_enum.value.is_match("feat") is True
        assert feature_enum.value.is_match("feature") is True
        assert feature_enum.value.is_match("feat-123") is True
        assert feature_enum.value.is_match("feature/add-login") is True
        assert feature_enum.value.is_match("main") is False

    def test_main_branch_enum(self):
        """Test main branch enum."""
        main_enum = SemanticBranchEnum.main

        assert isinstance(main_enum.value, SemanticBranch)
        assert main_enum.value.name == "main"
        assert main_enum.value.stubs == ["main", "master"]

        # Test the is_it method
        assert main_enum.value.is_match("main") is True
        assert main_enum.value.is_match("master") is True
        assert main_enum.value.is_match("main-backup") is True
        assert main_enum.value.is_match("feature") is False

    def test_fix_branch_enum(self):
        """Test fix branch enum."""
        fix_enum = SemanticBranchEnum.fix

        assert isinstance(fix_enum.value, SemanticBranch)
        assert fix_enum.value.name == "fix"
        assert fix_enum.value.stubs == ["fix", "hotfix"]

        # Test the is_it method
        assert fix_enum.value.is_match("fix") is True
        assert fix_enum.value.is_match("hotfix") is True
        assert fix_enum.value.is_match("fix-urgent") is True
        assert fix_enum.value.is_match("feature") is False

    def test_all_enum_values_are_semantic_branches(self):
        """Test that all enum values are SemanticBranch instances."""
        for branch_enum in SemanticBranchEnum:
            assert isinstance(branch_enum.value, SemanticBranch)
            assert isinstance(branch_enum.value.name, str)
            assert isinstance(branch_enum.value.stubs, list)
            assert len(branch_enum.value.stubs) > 0
            assert all(isinstance(stub, str) for stub in branch_enum.value.stubs)


class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error conditions."""

    def test_special_characters_in_branch_names(self):
        """Test how special characters in branch names are handled."""
        feature_stubs = ["feat", "feature"]

        # These should work (special chars are after the semantic part)
        assert (
            is_certain_semantic_branch("feat/123", feature_stubs) is True
        )  # @ is not dash/slas
        assert (
            is_certain_semantic_branch("feat-test", feature_stubs) is True
        )  # - is not dash/slash
        assert (
            is_certain_semantic_branch("feat_test", feature_stubs) is True
        )  # _ is not dash/slash
        assert (
            is_certain_semantic_branch("feat@123", feature_stubs) is True
        )  # @ is not dash/slash
        assert (
            is_certain_semantic_branch("feat+branch", feature_stubs) is True
        )  # + is not dash/slash

    def test_very_long_branch_names(self):
        """Test very long branch names."""
        feature_stubs = ["feat", "feature"]

        long_branch = "feat-" + "x" * 1000
        assert is_certain_semantic_branch(long_branch, feature_stubs) is True

        long_branch_with_slash = "feature/" + "x" * 1000
        assert is_certain_semantic_branch(long_branch_with_slash, feature_stubs) is True

    def test_unicode_characters(self):
        """Test unicode characters in branch names."""
        feature_stubs = ["feat", "feature"]

        # These should work as unicode chars are after semantic part
        assert is_certain_semantic_branch("feat-测试", feature_stubs) is True
        assert is_certain_semantic_branch("feature/描述", feature_stubs) is True


if __name__ == "__main__":
    from semantic_branch.tests import run_cov_test

    run_cov_test(
        __file__,
        "semantic_branch.impl",
        preview=False,
    )
