import yaml
import glob


def combine_projects(project_one: dict, project_two: dict) -> dict:
    combined_project = project_one

    for branch, controllers in project_two.items():
        if branch in combined_project:
            combined_project[branch] = list(set(combined_project[branch] + controllers))
        else:
            combined_project[branch] = controllers

        combined_project[branch].sort()

    return combined_project


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
        branches = {}
        project_cac = yaml.safe_load(file)

        # If empty YAML file.
        if project_cac == None:
            return {}

        project_branch = project_cac.get("scm_branch")
        jobs = project_cac.get("jobs", [])

        for job in jobs:
            job_branch = job.get("scm_branch")

            for deployment in job["deployments"]:
                deployment_branch = deployment.get("scm_branch")

                # Set branch based on order of priority: deployment first, then job, then project.
                if deployment_branch:
                    branch = deployment_branch
                elif job_branch:
                    branch = job_branch
                else:
                    branch = project_branch

                if branch:
                    if branch in branches:
                        current_controllers = branches[branch]
                        branches[branch] = list(
                            set(current_controllers + deployment["controllers"])
                        )
                        branches[branch].sort()
                    else:
                        branches[branch] = deployment["controllers"]

    return branches


def process_projects(projects_dir: str) -> dict:
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

    branches = {}

    for project_filepath in glob.glob(projects_dir + "/*.yml"):
        with open(project_filepath, "r", encoding="utf-8") as file:
            try:
                project_cac = yaml.safe_load(file)

                if "scm_url" in project_cac:
                    project_url = project_cac["scm_url"]

                    if project_url in branches:
                        branches[project_url] = combine_projects(
                            extract_branches(project_filepath),
                            branches[project_url],
                        )
                    else:
                        branches[project_url] = extract_branches(project_filepath)
            except:
                next

    return branches


extract_branches("project_files/different_controllers.yml")
