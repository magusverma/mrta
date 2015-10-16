grids = len(range(4,11,2))
rs = len(range(1,5))
ts = len(range(1,11))
iss = len(range(1,3))

an = [[[{} for t in range(ts+1)] for r in range(rs+1)]for grid in range(grids)]

algorithm = "dijkstra"

for i,h in enumerate(range(4,11,2)):
	for j,ra in enumerate(range(1,5)):
		for k,ta in enumerate(range(1,11)):
			try:
				an[i][j+1][k+1]["tles"] = 0
				an[i][j+1][k+1]["ooms"] = 0
				an[i][j+1][k+1]["exp"] = []
				an[i][j+1][k+1]["mem"] = []
				for l in range(1,3):
					# h,ra,ta,i = 10,1,10,1
					test_case_file = str(h)+"_"+str(ra)+"_"+str(ta)+"_"+str(l)
					with open("../output/"+algorithm+"_"+test_case_file) as f: s = f.read()
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
					an[i][j+1][k+1]["tles"] += tle
					an[i][j+1][k+1]["ooms"] += oom
					an[i][j+1][k+1]["exp"].append(states)
					an[i][j+1][k+1]["mem"].append(memory)
			except Exception:
				an[i][j+1][k+1] = "FAIL"

for i,h in enumerate(range(4,11,2)):
	for j,ra in enumerate(range(1,5)):
		for k,ta in enumerate(range(1,11)):
			print h,ra,ta,an[i][j+1][k+1] 