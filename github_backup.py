# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:36:37 2020
@author: SCOURT01

Script to back up all repos and branches from your github organisation.
You will need git installed and a github user account.

Update: use of password in API calls is now deprecated so to run 
this script you will need to create a personal access token (PAT) at
github.com and use this instead. Instructions for generating a PAT:
https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

!! Be careful not to push / share your PAT with anyone !!

"""

import os
from datetime import date
from contextlib import contextmanager


#####################################################
# Behind a firewall? Specify your "proxy:port" or set to None
#PROXYPORT = "http://www-xxx:1234"
PROXYPORT = None
#####################################################



@contextmanager
def cd(newdir):
    # Using generator and decorator to switch between directories
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def has_master_branch( remotebranches ):
    """Check list of remote branches in a repo for 'master' 
    """
    has_master = False
    for b in remotebranches:
        if "origin/master" in b:
            has_master = True           
    return has_master


def get_repos(user, org, pat):
    """Return list of repos in organisation
    """
    # curl the organisation page. 
    # Need popen().read() to store output as string
    if PROXYPORT is not None:
        curl = os.popen(f"curl -i -u {user}:{pat} -x {PROXYPORT} https://api.github.com/orgs/{org}/repos?type=all").read().split("\n")
    else:
        curl = os.popen(f"curl -i -u {user}:{pat} https://api.github.com/orgs/{org}/repos?type=all").read().split("\n")
        
    # get repo names
    repos = []
    for line in curl:
        if '"full_name":' in line:
            # repo lines like: '    "full_name": "UCLHp/pbtMod",'
            repo = line.split(f"{org}/")[1].strip(",").strip("\"")
            repos.append(repo)
            
    return repos



def date_for_dir():
    """Returns date as YYYY MM DD string for directory name
    """
    year = str(date.today().year)
    month = str(date.today().month).zfill(2)
    day = str(date.today().day).zfill(2)
    return f"{year} {month} {day}"



def main():
    
    # Get organization, username and PAT
    print("Input the github organization name:")
    org = input()
    print("Input your github username:")
    user = input()
    print("Input your github personal access token, NOT your password")
    pat = input()
    
    repos = get_repos(user, org, pat)
    print(f"Repos found: {repos}")
 
    # Make dated directory for backup
    dirname = date_for_dir()
    os.mkdir(dirname)   
    with cd(dirname):
        for repo in repos:
            # Clone repo (makes dir automatically)
            print(f"xx Cloning repo {repo} xx")
            os.system(f"git clone https://github.com/{org}/{repo}.git")
            # cd to repo and pull all branches
            with cd(repo):
                gitbranch = os.popen("git branch -r").read().strip().split("\n")
                remote_branches = [b.strip() for b in gitbranch if "/HEAD" not in b and "/master" not in b]
                for branch in remote_branches:
                    # remote branches will be like "origin/branchname"
                    local_branch = branch.split("/")[1].strip()
                    print(f"xx Pulling branch {local_branch} xx")
                    os.system(f"git checkout -b {local_branch} {branch}")
                has_master = has_master_branch( gitbranch )
                if has_master:
                    # Checkout to master branch
                    os.system("git checkout master")        
    


if __name__=="__main__":
    main()



