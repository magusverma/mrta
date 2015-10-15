from flask import Flask, render_template, redirect, url_for, request
import numpy
from pprint import pprint
app = Flask(__name__)
app.debug = True
app.my_vars = {'state_count': 0}

@app.route('/')
def hello_world():
	pprint(request.args)
	# count = app.my_vars['state_count']
	# test_case_file = request.args.get('run')
	# grid_size = get_array(request.args.get('grid_size'))
	# bots= get_list(request.args.get('bots'))
	# targets= get_list(request.args.get('targets'))
	# Matrix = [["" for x in range(grid_size[1])] for x in range(grid_size[0])] 
	# for bot in bots:
	# 	Matrix[bot[0]][bot[1]] = "bot" 
	# for target in targets:
	# 	Matrix[target[0]][target[1]] = "target" 
		
	# return render_template("grid.html",
	# 	count_variable_visible_in_template=count,
	# 	Matrix = Matrix)

def get_array(s):
	return [int(x) for x in s.split(",")]

def get_list(s):
	return([get_array(x) for x in s.split(";")])
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

