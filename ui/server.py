from flask import Flask, render_template, redirect, url_for, request
import numpy
from pprint import pprint
import os
app = Flask(__name__)
app.debug = True
app.my_vars = {'state_count': 0}
from time import sleep

@app.route('/')
def hello_world():
	test_case_file = request.args.get('input')
	algorithm = request.args.get('algo')
	delay = request.args.get('delay')
	# print test_case_file,algorithm
	# os.system(" touch ./output/"+algorithm+"_"+test_case_file)
	# os.system("./bin/"+algorithm + " < ./input/"+test_case_file+" > ./output/"+algorithm+"_"+test_case_file)
	# sleep(2)
	with open("./output/"+algorithm+"_"+test_case_file) as f: s = f.read()
	moves = s.split("\n")[1]
	# print s, moves, "move"
	with open("./input/"+test_case_file) as f: s = f.read()
	s = s.split("\n")
	[height, width] = map(int, s[0].split(" "))
	grid = [[False for i in range(width)] for j in range(height)]
	targets = "["
	comma = False
	for i,v in enumerate(s[1:]):
		for j,vv in enumerate(v):
			grid[i][j] = (vv=="*")
			if vv=="T":
				if comma:
					targets += ","
				else:
					comma = True
				targets +="["+str(i)+","+str(j)+"]"
	targets += "]"
	print grid
	return render_template("grid.html", width=width, height=height, ans=moves,targets=targets,delay=delay,grid=grid)

@app.route('/analysis')
def tests():
	grids = len(range(4,11,2))
	rs = len(range(1,5))
	ts = len(range(1,11))
	iss = len(range(1,3))

	an = [[[{} for t in range(ts+1)] for r in range(rs+1)]for grid in range(grids)]

	algorithm = request.args.get('algo')

	for i,h in enumerate(range(4,11,2)):
		for j,ra in enumerate(range(1,5)):
			for k,ta in enumerate(range(1,11)):
				try:
					for l in range(1,2):
						# h,ra,ta,i = 10,1,10,1
						test_case_file = str(h)+"_"+str(ra)+"_"+str(ta)+"_"+str(l)
						with open("./output/"+algorithm+"_"+test_case_file) as f: s = f.read()
						a = s.split("\n")[0].split(" ")
						print test_case_file, a
						soln = float(a[0])
						states = int(a[1])
						time = float(a[2])
						memory = int(a[3])
						tle = False
						oom = False
						if(len(s)>4):
							tle = (a[-1] == "TLE")
							oom = (a[-1] == "OOM")
						print tle,oom						
						an[i][j+1][k+1]["tles"] = tle
						an[i][j+1][k+1]["ooms"] = oom
						an[i][j+1][k+1]["exp"] = states
						an[i][j+1][k+1]["mem"] = memory
						an[i][j+1][k+1]["sol"] = soln
				except Exception:
					an[i][j+1][k+1] = "FAIL"

	htm = ""
	for i,h in enumerate(range(4,11,2)):
		htm += '<h2> Grid Size: '+str(h)+' X '+str(h)+" </h2>"
		htm += '<table><tr><td>robot\ target</td>'
		for k,ta in enumerate(range(1,11)):
			htm+='''<td style=" width: 100px; height: 50px;">'''+str(ta)+"</td>"
		htm += "</tr>"
		for j,ra in enumerate(range(1,5)):
			htm +='''<tr><td style=" width: 100px; height: 50px;">'''+str(ra)+'''</td>'''
			for k,ta in enumerate(range(1,11)):
				htm += "<td>"
				fname = str(h)+"_"+str(ra)+"_"+str(ta)+"_"+str(1)
				htm += "<a href='/?input="+fname+"&algo=dijkstra&delay=500'>"+"I: "+"</a>"
				print an[i][j+1][k+1]
				if an[i][j+1][k+1] == "FAIL":
					htm +='FAIL'
				elif an[i][j+1][k+1]["tles"] >0:
					htm +='TLE'
				elif an[i][j+1][k+1]["ooms"] >0:
					htm +='OOM'
				else:
					htm += str(an[i][j+1][k+1]["sol"])
				if an[i][j+1][k+1] != "FAIL":
					htm += " ("+str((an[i][j+1][k+1]["exp"]))+")"
				htm += "</td>"
			htm += "</tr>"
		htm += "</table>"
		htm += "</br>"
	return htm
	return render_template("analysis.html", htm=htm)

def get_array(s):
	return [int(x) for x in s.split(",")]

def get_list(s):
	return([get_array(x) for x in s.split(";")])
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

