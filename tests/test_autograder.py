import pytest
from autograder import get_repo, is_branch_merged, get_commit_count, check_file_exists, check_gitignore

@pytest.fixture(scope="session")
def setup_repo():
    """Get repository reference before running tests."""
    return get_repo()

def test_feature_a_merged(setup_repo):
    assert is_branch_merged(setup_repo, "feature-a"), "❌ feature-a NOT merged!"

def test_feature_b_merged(setup_repo):
    assert is_branch_merged(setup_repo, "feature-b"), "❌ feature-b NOT merged!"

def test_feature_c_squashed(setup_repo):
    assert get_commit_count(setup_repo, "feature-c") < 3, "❌ feature-c has multiple commits!"

def test_gitignore_updated():
    assert check_gitignore(), "❌ .gitignore is missing required entries!"

def test_config_txt_restored():
    assert check_file_exists("config.txt"), "❌ config.txt is missing!"
