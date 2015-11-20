for file in ../random_grid_inputs/*
do 
	echo $file
	python main.py $file > ../random_grid_results/random_grid_inputs/$file
done