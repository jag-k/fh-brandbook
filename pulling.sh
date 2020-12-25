git pull origin master

(
    cd tmp
) || (
    mkdir tmp && cd tmp
)

rm restart.txt || touch restart.txt