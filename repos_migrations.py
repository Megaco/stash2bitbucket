# Stash to Bitbucket Cloud migration
import os
from atlassian import Bitbucket
from atlassian.bitbucket.cloud import Cloud
import shutil
import subprocess

# Stash (Bitbucket server) credentials and url
stash_url = ''
stash_login = ''
stash_password = ''

# Bitbucket Cloud credentials and workspace
bitbucket_workspace = ''
bitbucket_login = ''
bitbucket_password = ''  # bitbucket application password

stash = Bitbucket(
    url=f'https://{stash_url}',
    username=stash_login,
    password=stash_password)

bitbucket = Cloud(
    url='https://api.bitbucket.org/',
    username=bitbucket_login,
    password=bitbucket_password,
    cloud=True)


def create_repo(repository_slug, full_path, project_key):
    print(f'Creating: {full_path} directory')
    os.makedirs(full_path, exist_ok=True)
    os.chdir(full_path)

    print(f'Cloning:  {full_path}')
    subprocess.run(
        f'git clone ssh://git@{stash_url}:7999/{project_key}/{repository_slug}.git', shell=True)

    print(f'Changing current directory to: {repository_slug}')
    os.chdir(f'{full_path}/{repository_slug}')

    print('Fetching everything from stash')
    subprocess.run(
        "git branch -r | grep -v '\->' | grep -v master | while read remote; do git branch --track \"${remote#origin/}\" \"$remote\"; done",
        shell=True)
    subprocess.run("git fetch --all", shell=True)
    subprocess.run("git pull --all", shell=True)

    print('Adding remote cloud')
    subprocess.run(
        f"git remote add cloud git@bitbucket.org:{bitbucket_workspace}/{repository_slug}.git", shell=True)

    print('Pushing all to cloud')
    subprocess.run('git push cloud --all', shell=True)

    print('Pushing tag to cloud')
    subprocess.run('git push cloud --tags', shell=True)

    print(f'Deleting: {full_path}')
    shutil.rmtree(f'{full_path}')


def master():
    project_list = stash.project_list()
    cwd = os.getcwd()

    for project in project_list:
        project_key = project['key']
        print(f'\nProject key: {project_key}')
        w = bitbucket.workspaces.get(bitbucket_workspace)

        if not w.projects.exists(project_key):
            project_name = project['name']
            print(f'Creating {project_name} project')
            w.projects.create(project_name, project_key,
                              description=project['description'], is_private=False)

        for repo in stash.repo_list(project_key):
            full_path = f'{cwd}/repos/{project_key}'
            repository_slug = repo['slug']

            print(f'\nRepository slug: {repository_slug}')

            if not w.repositories.exists(repository_slug):
                try:
                    print(
                        f'Creating {project_key}/{repository_slug} repository')
                    w.repositories.create(
                        repository_slug, project_key=project_key, is_private=True)
                    create_repo(repository_slug, full_path, project_key)
                except BaseException as error:
                    print('An exception occurred: {}'.format(error))
            else:
                create_repo(repository_slug, full_path, project_key)


if __name__ == "__main__":
    master()
