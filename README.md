# github-backup
Python script to clone all repos in an organization and pull all remote branches  

## Requirements  
You will need git installed and a github account with access to the organization's repos.You
will also need to generate a personalised access token (PAT) to be used in place of your
github password. Instructions for doing this 
are [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). 
When selecting the scopes, just tick the "repo" and "gist" boxes.

## Use  
Running the script ```python github_backup.py``` you will be prompted to enter your github
organization, username and PAT. The script will create a new folder labelled by the date and then clone 
all repos into here, pulling all remote branches at the same time.  

If you are behind a firewall you may need to supply your proxy and port. Do this in the format
"proxy:port" in the PROXYPORT variable in the script.








