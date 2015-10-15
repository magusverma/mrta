for f in `ls ./src`;
do
	file="${f%.*}";
	g++-4.8 ./src/$f -o bin/$file;
	echo "Compiled src/$f as bin/$f"
done;

python ./ui/server.py