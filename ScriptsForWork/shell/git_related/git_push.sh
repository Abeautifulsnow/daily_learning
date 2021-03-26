#!/bin/bash
commit=$1
default_branch=${2:-master}

function create_branch_if_not_exist()
{
    branch_arr=$(git branch -a)
    for branch in "${branch_arr}"
    do
        branch_in=$(echo "${branch}" | grep "${default_branch}")
        if [[ ${branch_in} != "" ]]
        then
            default_branch=${default_branch}
        else
            echo "Branch ==> ${default_branch} does not exist, we will create it..."
            git checkout -b "${default_branch}"
        fi
        echo "Current branch is: ${default_branch}"
    done
}

create_branch_if_not_exist

git status

while true;
do
    read -r -p "Continue or not? [Y/n] " input
 
    case $input in
        [yY][eE][sS]|[yY])
            echo "Continue to submit..."
            git add -A
            git commit -m "${commit}"
            git push origin ${default_branch}
                        exit 1
            ;;
 
        [nN][oO]|[nN])
            echo "Submit interrupted..."
            exit 1
                   ;;
 
        *)
        echo "Input error, please retry it..."
        ;;
    esac
done