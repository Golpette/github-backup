# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:36:37 2020
@author: SCOURT01

Script to back up all repos and branches from our github organization.
You will need git installed and a github user account.

"""

import os
from datetime import date
from contextlib import contextmanager


###### Use your github username ########################
USER = "xxx"
#####################################################

# Orgsanisation name
ORGANISATION = "xxxx"

# Specify the "proxy:port" or set to None
#PROXYPORT = "http://xxx:xxxx"
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


def get_repos():
    """Return list of repos in organisation
    """
    # curl the organisation page. 
    # Need popen().read() to store output as string
    if PROXYPORT is not None:
        curl = os.popen(f"curl -i -u {USER} -x {PROXYPORT} https://api.github.com/orgs/{ORGANISATION}/repos?type=all").read().split("\n")
    else:
        curl = os.popen(f"curl -i -u {USER} https://api.github.com/orgs/{ORGANISATION}/repos?type=all").read().split("\n")   
    
    # get repo names
    repos = []
    for line in curl:
        if '"full_name":' in line:
            # repo lines like: '    "full_name": "UCLHp/pbtMod",'
            ##repo = line.split(":")[1].strip(",").strip()
            repo = line.split(f"{ORGANISATION}/")[1].strip(",").strip("\"")
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
    
    repos = get_repos()
    print("Repos found:")
    print(repos)

    #test on 2
    #repos = ["xrv124","pdd-analysis"]
 
    # Make dated directory for backup
    dirname = date_for_dir()
    os.mkdir(dirname)   
    with cd(dirname):
        for repo in repos:
            # Clone repo (makes dir automatically)
            print(f"xx Cloning repo {repo} xx")
            os.system(f"git clone https://github.com/{ORGANISATION}/{repo}.git")
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
        ##raise Exception("Going back a directory")
        
    


if __name__=="__main__":
    main()



