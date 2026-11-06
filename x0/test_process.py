import os
import pytest
import yaml
from process import extract_branches

FILES_DIR = "project_files"


def test_extract_branches():

    # File does not exist.
    with pytest.raises(FileNotFoundError):
        extract_branches(os.path.join(FILES_DIR, "does_not_exist.yml"))

    # Invalid YAML.
    with pytest.raises(yaml.scanner.ScannerError):
        extract_branches(os.path.join(FILES_DIR, "invalid_yaml.yml"))

    # Empty file.
    assert extract_branches(os.path.join(FILES_DIR, "empty_file.yml")) == {}

    # Empty file referenced by absolute filepath.
    absolute_filepath = os.path.abspath(os.path.join(FILES_DIR, "empty_file.yml"))
    assert extract_branches(absolute_filepath) == {}

    # Single quotes.
    assert extract_branches(os.path.join(FILES_DIR, "single_quotes.yml")) == {
        "main": ["prod"],
    }

    # Double quotes.
    assert extract_branches(os.path.join(FILES_DIR, "double_quotes.yml")) == {
        "main": ["prod"],
    }

    # Two deployments that have the same branch name but different case.
    assert extract_branches(os.path.join(FILES_DIR, "different_cases.yml")) == {
        "main": ["prod"],
        "MAIN": ["prod"],
    }

    # No job templates defined.
    assert extract_branches(os.path.join(FILES_DIR, "no_jobs.yml")) == {}

    # One deployment that has no branch defined anywhere.
    assert extract_branches(os.path.join(FILES_DIR, "no_branch.yml")) == {}

    # One deployment whose branch is defined as "".
    assert extract_branches(os.path.join(FILES_DIR, "null_branch.yml")) == {}

    # Branch defined at project level.
    assert extract_branches(os.path.join(FILES_DIR, "project_branch.yml")) == {
        "project": ["prod"]
    }

    # Branch defined at job level.
    assert extract_branches(
        os.path.join(FILES_DIR, "job_branch.yml")
    ) == {"job": ["prod"]}

    # Branch defined at deployment level.
    assert extract_branches(
        os.path.join(FILES_DIR, "deployment_branch.yml")
    ) == {"deployment": ["prod"]}

    # Two jobs which are identical.
    assert extract_branches(os.path.join(FILES_DIR, "duplicate_jobs.yml")) == {
        "project": ["prod"]
    }

    # Branch defined at project and job level.
    assert extract_branches(os.path.join(FILES_DIR, "project_and_job_branch.yml")) == {
        "job": ["prod"]
    }

    # Branch defined at project and deployment level.
    assert extract_branches(os.path.join(FILES_DIR, "project_and_deployment_branch.yml")) == {
        "deployment": ["prod"]
    }

    # Branch defined at job and deployment level.
    assert extract_branches(os.path.join(FILES_DIR, "job_and_deployment_branch.yml")) == {
        "deployment": ["prod"]
    }

    # Branch defined at all three levels.
    assert extract_branches(os.path.join(FILES_DIR, "all_branches.yml")) == {
        "deployment": ["prod"]
    }

    # Realistic example.
    assert extract_branches(os.path.join(FILES_DIR, "realistic.yml")) == {
        "deployment": ["prod", "lab"],
        "job": ["lab"],
        "project": ["prod"],
    }
