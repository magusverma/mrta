for file in `grep -rl "changed" .`
do 
	echo $file
	cat $file|grep "states expanded" 
done