#!/bin/bash
function create_branch_if_not_exist()
{
    default_branch=${2:-master}

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

function gen_commit_if_empty()
{
    commit=$1

    git_comment="$(date +%F' '%r)"
    if [[ ${commit} -eq "" ]]
    then
        commit="$git_comment push code"
    else
        commit=${commit}
    fi
    echo "The commit's content are: ${commit}"
}

function push_code()
{
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
}

# Execute the flow of pushing code to git repository.
create_branch_if_not_exist
git status
gen_commit_if_empty
push_code