For your convenience, you can be gitfooled just exceute this command in you repository directory:

curl -s https://raw.githubusercontent.com/kxion/shit_uestc_zfsystem/master/gitfool| sh -s `pwd` 365 --push


USAGE
./gitfool [repo_path] [days] --push
repo_path

the repository path you want to add commits

days

the past days you wish to add these commits, for example : 365 means the past one year.

--push

with this option, Gitfool will push the commits to remote (execute git push)

don't use sh gitfool syntax, and it will report an error.

EXAMPLE
./gitfool ~/Code/acme 365 --push
