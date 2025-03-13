+++
title = "Cheat Sheet for Git"
description = ""
tags = [
    "git",
    "cheat-sheet",
]
date = "2022-08-30"
categories = [
    "Studylog",
]
menu = "main"
+++

This is a summary of basic Git learning materials.

## 1. Configuration commands
<hr>

* check current configuration
    ```bash
    git config -l
    ```
* change configuration
    ```bash
    git config --global user.name "user_name"
    git config --global user.email "user_email"
    ```
* cache github key for 15 minutes
    ```bash
    git config --global credential.helper cache
    ```

## 2. Staging & Commit commands
<hr>

* initialize an empty git repository in current directory
    ```bash
    git init
    ```
* get information of current working tree
    ```bash
    git status
    ```

### 2.1. Control Staging Area
* command git to track follwing file
    ```bash
    git add file_name.py
    ```
* stage every change in the staging area
    ```bash
    git add .
    ```
* alias to --cached, show all staged but not commited files
    ```bash
    git diff --staged
    ```
* reset(clear) staging area
    ```bash
    git reset HEAD --
    ```
* rename `file1.py` with `file2.py` (similar to Linux `mv`)
    ```bash
    git mv file1.py file2.py
    ```
* remove `file_name.py` from working space (similar to Linux `rm`)
    ```bash
    git rm file_name.py
    ```

### 2.2. Commit
* commit everything in current staging area
    - opens a text editor to enter a commit message
    ```bash
    git commit
    ```
* stage changes to tracked file & commit in one step
    ```bash
    git commit -a
    ```
* stage & commit & enter message
    ```bash
    git commit -a -m "commit message"
    ```

### 2.3. Show Commit Status
* check history of all commits
    ```bash
    git log
    ```
* show actual lines that changed in each commit
    ```bash
    git log -p
    ```
* show statistics about the changes in the commit
    ```bash
    git log --stat
    ```
* show commit branch tree
    ```bash
    git log --graph --oneline --all
    ```
* show the information about the commit `commit_id` and associated petches
    ```bash
    git show [commit_id]
    ```
* compare two commits `commit_id1` and `commit_id2` (similar to Linux `diff`)
    ```bash
    git diff [commit_id1] [commit_id2]
    ```

### 2.4. Reset/Revert Commit
* reset the repo in the Index, the next snapshot to commit
    ```bash
    git reset --soft [commit_id]
    ```
* update Index to the snapshot that HEAD is pointing 
    ```bash
    git reset --mixed [commit_id]
    ```
* update Index to the snapshot that HEAD is pointing 
    - and reset staging area and working directory
    ```bash
    git reset --hard [commit_id]
    ```
* make changes to commits after-the-fact on local commits
    ```bash
    git commit --amend
    ```
* make a new commit which rolls back a previous commit
    ```bash
    git revert HEAD/[commit_id]
    ```
* roll back `num_commit_to_reverse`-many commit
    ```bash
    git reset --soft HEAD~[num_commit_to_reverse]
    ```
* change the base commit used for the branch `branch_name`
    ```bash
    git rebase [branch_name]
    ```

## 3. Branch commands
<hr>

* list all branches
    ```bash
    git branch
    ```
* shows read-only remote branches
    ```bash
    git branch -r
    ```
* creates branch named `branch_name`
    ```bash
    git branch [branch_name]
    ```
* switch to branch `branch_name`
    ```bash
    git checkout [branch_name]
    ```
* creates a new branch `branch_name` and switches to it
    ```bash
    git checkout -b [branch_name]
    ```
* delete the branch `branch_name`
    ```bash
    git branch -d [branch_name]
    ```
* forcibly delete the branch `branch_name`
    ```bash
    git branch -D [branch_name]
    ```
* join branche `branch_name` together to the master branch
    ```bash
    git merge [branch_name]
    ```
* when merge conflicts, abort merge action
    ```bash
    git merge --abort
    ```

## 4. Github commands
<hr>

* Github manages access to the accounts using [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). 
* When pushing to github, there is **120MB storage limit** per file. If files larger than this limit is pushed, remote rejected error occurs.

### 4.1. Manage Remote Repository
* clone a remote repository into a local workspace
    ```bash
    git clone [URL] 
    ```
* list remote repos
    ```bash
    git remote
    ```
* show URL of remote repo
    ```bash
    git remote -v
    ```
* describe a single remote repo with URL `remote_URL`
    ```bash
    git remote show [remote_URL]
    ```
* fetche the most up-to-date objects to local repo
    ```bash
    git remote update
    ```
* transfer a repository from origin to `new-url`
    ```bash
    git remote set-url origin [new-url]
    ```

### 4.2. Synchronize Remote <-> Local Repo
* push commits from local repo to a remote repo
    ```bash
    git push
    ```
* copy the commits done in the remote repository
    ```bash
    git fetch
    ```
* fetch from remote & merge with local branch
    ```bash
    git pull
    ```



<hr>

## References
1. Git Docs ([link](https://git-scm.com/doc))
2. GitHub Docs ([link](https://docs.github.com/en))
3. Coursera, Google, Introduction to Git and Github ([link](https://www.coursera.org/learn/introduction-git-github))
