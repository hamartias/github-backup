from github3 import login, GitHub
from getpass import getpass, getuser
from datetime import date
import sys
import subprocess
import os
import zipfile
import pathlib
import shutil


def compress_directory(zip_target_name, zipf):
    for root, dirs, files in os.walk(zip_target_name):
        for f in files:
            write_name = os.path.join(root, f)
            try:
                zipf.write(write_name)
            except FileNotFoundError:
                print("Skipping %s. File not found. Might be a symlink."
                      % write_name)


def clone_repos(repos, zip_target_name, g_object, date_string):
    for i, repo in enumerate(repos):
        url = repo.clone_url
        name = repo.name
        tar_name = "%s/%s_backup_%s" % (zip_target_name, name, date_string)
        subprocess.call(["git", "clone", url, tar_name])


def clone_and_compress(repos, zip_target_name, g_object):
    date_string = date.today().strftime("%d-%m-%Y")
    dirname = "%s-%s" % (zip_target_name, date_string)
    target_dir = os.mkdir(dirname)

    clone_repos(repos, dirname, g_object, date_string)

    zipf = zipfile.ZipFile('%s.zip' % zip_target_name, 'w',
                           zipfile.ZIP_DEFLATED)
    compress_directory(dirname, zipf)
    shutil.rmtree(dirname)


def main():
    try:
        user = input('GitHub username: ')
    except KeyboardInterrupt:
        user = getuser()
    password = getpass('GitHub password for {0}: '.format(user))
    if not (user and password):
        sys.exit(1)
    g = login(user, password)
    zip_target_name = input("Enter a name for the zip file (omit the .zip): ")
    clone_and_compress(g.repositories(), zip_target_name, g)


if __name__ == "__main__":
    main()
