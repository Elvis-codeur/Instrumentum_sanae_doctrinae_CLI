import click

@click.command()
@click.argument("repo", help="The repository to clone from (e.g., github, gitlab)")
@click.option("--branch", help="The branch to clone (Required for GitHub)")
@click.option("--token", help="Access token (Required for GitLab)")
def clone(repo, branch, token):
    """Clone a repository with specific parameters."""
    
    if repo == "github":
        if not branch:
            raise click.UsageError("Error: --branch is required when cloning from GitHub.")
        click.echo(f"Cloning from GitHub on branch {branch}...")

    elif repo == "gitlab":
        if not token:
            raise click.UsageError("Error: --token is required when cloning from GitLab.")
        click.echo(f"Cloning from GitLab using token {token}...")

    else:
        raise click.UsageError("Error: Unsupported repository type. Use 'github' or 'gitlab'.")

if __name__ == "__main__":
    clone()
