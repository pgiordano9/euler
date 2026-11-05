import yaml

def extract_branches(project_filepath: str) -> dict:
    """Extract branches and corresponding AAP controllers from a project CaC file.

    For a project CaC file, specified by its filepath (`project_filepath`), extract all in-use
    branches. Record which AAP controllers (lab and/or prod) each branch is being used in within
    job template(s) in that environment.

    Args:
        project_filepath: Filepath (absolute or relative) to a project CaC file.

    Returns:
        A dict mapping in-use branches to the AAP controller(s) they are deployed to. For example:

        {
          "v0.1.1": ["lab"],
          "2026.0917.2890": ["lab", "prod"]
        }
    """

    with open(project_filepath, "r", encoding="utf-8") as file:
        project_cac = yaml.safe_load(file)

        jobs = project_cac["jobs"]

        for job in jobs:
            for deployment in job["deployments"]:
                print(deployment)

    return {}

extract_branches("project_files/one_default_one_deployment.yml")


def process_project_files(projects_dir: str) -> dict:
    """Read all CaC files in a projects directory and extract branches from each of them.

    Iterate over all CaC files in a project directory, specified by its filepath (`project_dir`),
    and use the `extract_branches` function on each, constructions a larger dictioning that stores
    project repo URLs, in-use branches and corresponding AAP controllers.

    Args:
        projects_dir: Filepath (absolute or relative) to a directory containing project CaC files.

    Returns:
        A dict mapping project repo URL to the corresponding dict returned from the
        `extract_branches` function. For example:

        {
          "https://github.com/wp-iaas/Network-Base-Config.git": {
            "v0.1.1": ["lab"],
            "2026.0917.2890": ["lab", "prod"]

          }
        }

    """
