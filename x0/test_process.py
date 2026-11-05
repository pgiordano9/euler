import os
import yaml
import pytest
from process import extract_branches

FILES_DIR = "project_files"

-rw-rw-r-- 1 e6001892 e6001892 329 Oct 30 10:42 all_branches.yml
-rw-rw-r-- 1 e6001892 e6001892 438 Oct 30 10:24 duplicated_jobs.yml
-rw-rw-r-- 1 e6001892 e6001892 312 Oct 30 10:39 job_and_deployment_branch.yml
-rw-rw-r-- 1 e6001892 e6001892 287 Oct 30 10:36 job_branch.yml
-rw-rw-r-- 1 e6001892 e6001892 266 Oct 30 10:33 no_branch.yml
-rw-rw-r-- 1 e6001892 e6001892 308 Oct 30 10:35 project_and_deployment_branch.yml
-rw-rw-r-- 1 e6001892 e6001892 304 Oct 30 10:33 project_and_job_branch.yml

def test_extract_branches():

    # File does not exist.
    with pytest.raises(FileNotFoundError):
        extract_branches(os.path.join(FILES_DIR, "does_not_exist.yml"))

    # Invalid YAML.
    with pytest.raises(yaml.scanner.ScannerError):
        extract_branches(os.path.join(FILES_DIR, "invalid_yaml.yml"))

    # Empty file.
    assert extract_branches(os.path.join(FILES_DIR, "empty_file.yml")) == {}

    # Single quotes.
    assert extract_branches(os.path.join(FILES_DIR, "single_quotes.yml")) == {
        "main": ["prod"],
    }

    # Double quotes.
    assert extract_branches(os.path.join(FILES_DIR, "double_quotes.yml")) == {
        "main": ["prod"],
    }

    # Empty file referenced by absolute filepath.
    absolute_filepath = os.path.abspath(os.path.join(FILES_DIR, "empty_file.yml"))
    assert extract_branches(absolute_filepath) == {}

    # CaC file with two deployments that have the same branch name but use different case.
    assert extract_branches(os.path.join(FILES_DIR, "different_cases.yml")) == {
        "main": ["prod"],
        "MAIN": ["prod"],
    }

    # Non-empty CaC file with no job templates defined.
    assert extract_branches(os.path.join(FILES_DIR, "no_jobs.yml")) == {}

    assert extract_branches(os.path.join(FILES_DIR, "project_branch.yml")) == {
        "project": ["prod"]
    }

    assert extract_branches(
        os.path.join(FILES_DIR, "job_branch.yml")
    ) == {"job": ["prod"]}

    assert extract_branches(
        os.path.join(FILES_DIR, "deployment_branch.yml")
    ) == {"deployment": ["prod"]}

    assert extract_branches(os.path.join(FILES_DIR, "prod.yml")) == {
        "dev": ["prod"]
    }

    # CaC file with two deployments, both using default branch.
    assert extract_branches(os.path.join(FILES_DIR, "two_default.yml")) == {
        "master": ["prod"]
    }

    # CaC file with two deployments, both using branch defined at deployment level.
    assert extract_branches(os.path.join(FILES_DIR, "two_deployment.yml")) == {
        "dev": ["prod"]
    }

    # CaC file with two deployments, one using the default branch and one using a
    # branch set at the deployment level.
    assert extract_branches(
        os.path.join(FILES_DIR, "one_default_one_deployment.yml")
    ) == {
        "master": ["prod"],
        "dev": ["prod"],
    }

    # CaC file with one deployment that uses a branch defined at the deployment level,
    # but with different controllers configured at the project and deployment level.
    assert extract_branches(
        os.path.join(FILES_DIR, "deployment_branch_controller_check.yml")
    ) == {"dev": ["lab", "prod"]}

    # CaC file with multiple deployments that each deploy to a different controller.
    assert extract_branches(
        os.path.join(FILES_DIR, "multiple_deployments_distinct_controllers.yml")
    ) == {"ede": ["lab"], "prod": ["prod"]}

    # CaC file with two deployments that both use the same branch and deploy to the same controller.
    assert extract_branches(os.path.join(FILES_DIR, "duplication_check.yml")) == {
        "prod": ["prod"]
    }

    # CaC file with one deployment that has no branch defined anywhere.
    assert extract_branches(os.path.join(FILES_DIR, "no_branch.yml")) == {}

    # CaC file with one deployment whose branch is defined as "".
    assert extract_branches(os.path.join(FILES_DIR, "empty_branch.yml")) == {}

