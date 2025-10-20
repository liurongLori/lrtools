declare -a array=("，" "”" "“" "’" "‘" "。" "：" "？" "！")
for char in "${array[@]}";
do
    echo $char;
    grep $char $1/*.py;
done
grep ', " ' $1/*.py;
grep ' ",' $1/*.py;
grep '} "' $1/*.py;
