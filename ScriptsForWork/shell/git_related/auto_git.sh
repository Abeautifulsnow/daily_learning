#!/bin/bash

push_bran=""
pull_bran=""
exclude_dir=()
index=0

git_comment=""
b_error=0

function parse_ini_info()
{
	args=$1
	
	if [[ ${args:0:1} != '#' ]]	#注释
	then
		#分支名不超过30字符	只能a-z/A-Z/0-9/_
		if [[ ${args:0:12} == "push_branch:" ]]
		then
			push_bran=$(echo ${args:12:30} | grep '[(0-9)|(a-z)|(A-z)|_]*')
			echo $push_bran
		elif [[ ${args:0:12} == "pull_branch:" ]]
		then
			pull_bran=$(echo ${args:12:30} | grep '[(0-9)|(a-z)|(A-z)|_]*')
			echo $pull_bran
		elif [[ ${args:0:12} == "exclude_dir:" ]]
		then
			#排除文件夹名不超过30字符	只能a-z/A-Z/0-9/_
			exclude_dir[$index]=$(echo ${args:12:30} | grep '[(0-9)|(a-z)|(A-z)|_]*')
			index=$[$index+1]
		fi
	fi
}

function read_ini_info()
{
	#遍历branch.ini每行内容
	while read line
	do
		echo $line
		
		parse_ini_info $(echo $line | sed 's/ //g') #去空格

	done < branch.ini

	#文件没换行的话最后一行读完
	if [[ -n $(tail branch.ini -c 1) ]]
	then
		echo 'Warnning: ini File Has Last Line Unfinish'

		last_line=$(tail -n 1 branch.ini)
		
		parse_ini_info $(echo $last_line | sed 's/ //g') #去空格
	fi
}

function check_origin_branch()
{
	b_exit=0
	
	#验证是否有远程分支
	all_brans=$(git branch -r)

	for branch in $all_brans
	do
		if [[ $branch = origin/$push_bran ]]
		then
			echo "Tips: Current Push Branch Found in Origin Branchs."
			b_exit=$[$b_exit+1]
		elif [[ $branch = origin/$pull_bran ]]
		then
			echo "Tips: Current Pull Branch Found in Origin Branchs."
			b_exit=$[$b_exit+1]
		fi
	done
	
	
	if [ $b_exit -lt 2 ]
	then
		#远程分支未匹配，询问用户是否需要继续操作
		echo "Error: ini FIle Branch Info Don't Exit in Origin Branchs."
		b_error=1
		
		read -r -p "If Continue Pull/Push Code Unless Not In Origin Branchs: [Y/N] " input

		case $input in
			[yY][eE][sS]|[yY])
				return 0
				;;

			[nN][oO]|[nN])
				return 1
				;;

			*)
				echo "invalid input"
				exit -1
				;;
		esac
		
	elif [ $b_exit -eq 2 ]
	then
		return 0
	fi
	
	return 1
}

function is_branch_exit()
{
	#检查文件大小
	file_size=$(ls -l branch.ini | awk '{ print $5 }')
	if [ $file_size -gt 200 ]
	then
		echo 'Error: ini File Size Too Big!'
		b_error=1
		return -1
	fi

	read_ini_info

	if [[ -n $push_bran ]] && [[ -n $pull_bran ]]
	then
		return 0
	else
		echo "Error: Read ini File Error, Can't Find Useful Info."
		b_error=1
	fi
	return -1
}

function check_git_status()
{
	git_stat=$(git status 2>&1)

	#echo $git_stat;

	str_add="Changes not staged for commit"
	str_commit="Changes to be committed"
	str_clean="nothing to commit, working tree clean"
	str_fail="fatal: not a git repository"
	str_conlict="You have unmerged paths."
	str_unmerge="Unmerged paths:"
	str_fixed="All conflicts fixed but you are still merging."
	
	if [[ $git_stat =~ $str_clean ]]
	then
		#echo -e 'Code Need Add!'
		return 0
	elif [[ $git_stat =~ $str_conlict ]] || [[ $git_stat =~ $str_unmerge ]]
	then
		#echo -e 'Code Need Commit!'
		return 1
	elif [[ $git_stat =~ $str_fixed ]]
	then
		#echo -e 'Conflicts Had Fixed'
		return 2
	elif [[ $git_stat =~ $str_add ]]
	then
		#echo -e 'Workspace Clean!'
		return 3
	elif [[ $git_stat =~ $str_commit ]]
	then
		#echo -e 'Code Conflicts!'
		return 4
	elif [[ $git_stat =~ $str_fail ]]
	then
		#echo -e 'Not Exit Git Repository!'
		return 5
	elif [[ -z $git_stat ]]
	then
		echo -e "Error: Git Status Empty Output!"
		b_error=1
	fi

	return -1
}

function gen_push_comment()
{
	git_comment="$(date +%F' '%r)"
	
	args=$1
	
	#echo $args
	
	if [[ $args -eq 2 ]]
	then
		git_comment="$git_comment merge confilcts"
	else
		git_comment="$git_comment push code"
	fi
	
	#echo $git_comment
}

function push_code_main()
{
	for files in $(ls)
	do
		if [ -d $files ]
		then
			b_exit=0
			#遍历当前目录文件夹
			echo -e "\n:/$files"
			
			#是否为排除文件夹
			for dir in ${exclude_dir[*]}
			do
				if [[ $dir == $files ]]
				then
					b_exit=1
					break
				fi
			done
			
			if [ $b_exit -eq 1 ]
			then
				echo "Skip To $files Dir..."
				continue
			fi
			
			cd $files

				check_git_status
				rtn=$?
				
				#生成备注
				gen_push_comment $rtn
				
				
				#工作区干净
				if [ $rtn == 0 ]
				then
					echo 'TIps: Workspace Clean'

					echo "/********************************************"
					git pull origin $pull_bran
					echo "********************************************/"
					echo "/********************************************"
					git push origin $push_bran
					echo "********************************************/"

				#代码冲突
				elif [ $rtn == 1 ]
				then
					echo 'Error: Code Need Merge Conflicts'
					b_error=1

				#冲突已解决
				elif [ $rtn == 2 ]
				then
					echo 'Tips: Conflicts had Fixed And Push Code'

					check_origin_branch
					
					git add ./
					git commit -m "$git_comment"
					echo "/********************************************"
					git pull origin $pull_bran
					echo "********************************************/"
					echo "/********************************************"
					git push origin $push_bran
					echo "********************************************/"
					
				#没有add代码
				elif [ $rtn == 3 ]
				then
					echo 'Tips: Not add Code'

					check_origin_branch
					
					git add ./
					git commit -m "$git_comment"
					echo "/********************************************"
					git pull origin $pull_bran
					echo "********************************************/"
					echo "/********************************************"
					git push origin $push_bran
					echo "********************************************/"

				#没有commit代码
				elif [ $rtn == 4 ]
				then
					echo 'Tips: Not commit Code'

					check_origin_branch
					
					git commit -m "$git_comment"
					echo "/********************************************"
					git pull origin $pull_bran
					echo "********************************************/"
					echo "/********************************************"
					git push origin $push_bran
					echo "********************************************/"
					
				#不存在Git仓库
				elif [ $rtn == 5 ]
				then
					echo 'Warnning: Not Exit Git Repository!'

				#其他情况
				else
					echo 'Error: Other Question'
					b_error=1
				fi

			cd ..
		fi
	done
}


#入口 main
is_branch_exit

if [ $? == 0 ]
then
	push_code_main
else
	echo "Error: branch.ini File Configure Error!"
	b_error=1
fi

if [ $b_error -eq 1 ]
then
	echo 'press return or enter to quit: '
	read
fi
