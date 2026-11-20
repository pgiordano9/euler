import os
import pytest
import yaml
from process import combine_projects, extract_branches, process_projects, extract_image

PROJECTS_DIR = "project_files"
NAVIGATORS_DIR = "navigator_files"


def test_extract_image():
    # Realistic example.
    assert (
        extract_image(os.path.join(NAVIGATORS_DIR, "ansible-navigator.yml"))
        == "image: us-gh-l-apg001.worldpay.lab/iaas-ee:stable-174"
    )


def test_combine_projects():
    # Empty dicts.
    assert combine_projects({}, {}) == {}

    # No shared branches.
    assert combine_projects({"project": ["lab"]}, {"job": ["prod"]}) == {
        "project": ["lab"],
        "job": ["prod"],
    }

    # Shared branches.
    assert combine_projects({"project": ["lab"]}, {"project": ["prod"]}) == {
        "project": ["lab", "prod"]
    }

    # Realistic example.
    assert combine_projects(
        {"project": ["lab"], "job": ["prod"]},
        {"job": ["lab"], "deployment": ["lab", "prod"]},
    ) == {"project": ["lab"], "job": ["lab", "prod"], "deployment": ["lab", "prod"]}


def test_extract_branches():

    # File does not exist.
    with pytest.raises(FileNotFoundError):
        extract_branches(os.path.join(PROJECTS_DIR, "does_not_exist.yml"))

    # Invalid YAML.
    with pytest.raises(yaml.scanner.ScannerError):
        extract_branches(os.path.join(PROJECTS_DIR, "invalid_yaml.yml"))

    # Empty file.
    assert extract_branches(os.path.join(PROJECTS_DIR, "empty_file.yml")) == {}

    # Empty file referenced by absolute filepath.
    absolute_filepath = os.path.abspath(os.path.join(PROJECTS_DIR, "empty_file.yml"))
    assert extract_branches(absolute_filepath) == {}

    # Single quotes.
    assert extract_branches(os.path.join(PROJECTS_DIR, "single_quotes.yml")) == {
        "rand": ["prod"],
    }

    # Double quotes.
    assert extract_branches(os.path.join(PROJECTS_DIR, "double_quotes.yml")) == {
        "main": ["prod"],
    }

    # Two deployments that have the same branch name but different case.
    assert extract_branches(os.path.join(PROJECTS_DIR, "different_cases.yml")) == {
        "main": ["prod"],
        "MAIN": ["prod"],
    }

    # No job templates defined.
    assert extract_branches(os.path.join(PROJECTS_DIR, "no_jobs.yml")) == {}

    # One deployment that has no branch defined anywhere.
    assert extract_branches(os.path.join(PROJECTS_DIR, "no_branch.yml")) == {}

    # One deployment whose branch is defined as "".
    assert extract_branches(os.path.join(PROJECTS_DIR, "null_branch.yml")) == {}

    # Branch defined at project level.
    assert extract_branches(os.path.join(PROJECTS_DIR, "project_branch.yml")) == {
        "project": ["prod"]
    }

    # Branch defined at job level.
    assert extract_branches(os.path.join(PROJECTS_DIR, "job_branch.yml")) == {
        "job": ["prod"]
    }

    # Branch defined at deployment level.
    assert extract_branches(os.path.join(PROJECTS_DIR, "deployment_branch.yml")) == {
        "deployment": ["prod"]
    }

    # Two jobs which are identical.
    assert extract_branches(os.path.join(PROJECTS_DIR, "duplicate_jobs.yml")) == {
        "project": ["prod"]
    }

    # Branch defined at project and job level.
    assert extract_branches(
        os.path.join(PROJECTS_DIR, "project_and_job_branch.yml")
    ) == {"job": ["prod"]}

    # Branch defined at project and deployment level.
    assert extract_branches(
        os.path.join(PROJECTS_DIR, "project_and_deployment_branch.yml")
    ) == {"deployment": ["prod"]}

    # Branch defined at job and deployment level.
    assert extract_branches(
        os.path.join(PROJECTS_DIR, "job_and_deployment_branch.yml")
    ) == {"deployment": ["prod"]}

    # Branch defined at all three levels.
    assert extract_branches(os.path.join(PROJECTS_DIR, "all_branches.yml")) == {
        "deployment": ["prod"]
    }

    # Realistic example.
    assert extract_branches(os.path.join(PROJECTS_DIR, "realistic.yml")) == {
        "deployment": ["lab", "prod"],
        "job": ["lab"],
        "project": ["prod"],
    }

    # Two deployments with same branch but different controllers.
    assert extract_branches(
        os.path.join(PROJECTS_DIR, "different_controllers.yml")
    ) == {
        "project": ["lab", "prod"],
    }


def test_process_projects():

    assert process_projects(PROJECTS_DIR) == {
        "https://github.com/realistic.git": {
            "project": [
                "prod",
            ],
            "job": [
                "lab",
            ],
            "deployment": [
                "lab",
                "prod",
            ],
            "rand": [
                "prod",
            ],
        },
        "https://github.com/no_jobs.git": {},
        "https://github.com/duplicate_jobs.git": {
            "project": [
                "prod",
            ],
        },
        "https://github.com/double_quotes.git": {
            "main": [
                "prod",
            ],
        },
        "https://github.com/project_and_deployment_branch.git": {
            "deployment": [
                "prod",
            ],
        },
        "https://github.com/project_branch.git": {
            "project": [
                "prod",
            ],
        },
        "https://github.com/job_and_deployment_branch.git": {
            "deployment": [
                "prod",
            ],
        },
        "https://github.com/all_branches.git": {
            "deployment": [
                "prod",
            ],
        },
        "https://github.com/project_and_job_branch.git": {
            "job": [
                "prod",
            ],
        },
        "https://github.com/null_branch.git": {},
        "https://github.com/different_controllers.git": {
            "project": [
                "lab",
                "prod",
            ],
        },
        "https://github.com/no_branch.git": {},
        "https://github.com/job_branch.git": {
            "job": [
                "prod",
            ],
        },
        "https://github.com/different_cases.git": {
            "main": [
                "prod",
            ],
            "MAIN": [
                "prod",
            ],
        },
        "https://github.com/deployment_branch.git": {
            "deployment": [
                "prod",
            ],
        },
    }
