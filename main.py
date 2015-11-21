# Driver for Menu
import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import normal, rand
from draw import customPointPlacer
from point import point

def introduction_prompt():
	print("\nCS 4102 Final Project: A Workbench of Computational Geometry Algorithms\n")
	print("You have the ability to populate a 2D scatter plot with random points and then\nselect from several algorithms to play with the data\n")


def main_menu():
	choice = 0
	print("\n############################################################\n")
	print("Enter number of selection")
	print("1. Clear and Seed: Generate a set of new, random points for the scatter plot")
	print("2. Clear: Clear the plot of all points")
	print("3. Place Custom Points")
	print("Algorithms")
	print("4. Gift Wrapping")
	print("5. Grahams Scan")
	print("6. KD Tree")
	print("\n0. Exit")
	print("\n############################################################\n")
	try:
		choice = int(input())
	except ValueError:
		print("That's not an int!")
	return choice


"""
name: seed()
purpose: populate the plot with points
postcondition: 100 points are added in random positions in the range 0 to 10 for x and y
"""
def seed():
	print("Seeding graph...")
	global xs;
	global ys;
	xs = (rand(100)*10).tolist()
	ys = (rand(100)*10).tolist()
	plt.scatter(xs,ys)
	plt.ylim([-2, 12]);
	plt.xlim([-2, 12]);
	display_plot()

def clear():
	print("Clearing graph...")
	global xs;
	global ys;
	global points;
	xs = [];
	ys = [];
	points = [];

"""
name: custom()
purpose: Place point(s) wherever your mouse is
postcondition: Pressing 'i' will place a custom point on the plot
"""
def custom():
	plt.ioff();
	fig, ax = plt.subplots()
	plt.ylim([-2, 12]);
	plt.xlim([-2, 12]);
	p = customPointPlacer(fig, ax, xs, ys)
	print("Press i to insert, press r to randomized insert")
	
	canvas = fig.canvas
	canvas.mpl_connect('key_press_event', p.key_press_callback)
	display_plot();

"""
name: gift_wrapping()
purpose: Find the convex hull of a set of points
postcondition: Animates Jarvis' March finds the list of points that make up the convex hull
"""
def gift_wrapping():
	try:
		import vector;
		import time;
	
		print("Convex Hull using gift wrapping method");
		global xs;
		global ys;
		stepmode = True;
		# 1. Start by finding coordinate with the smallest x value "minind"
		minval = xs[0];
		minind = 0;
		for i in range(len(xs)):
			if (xs[i] < minval):
				minind = i;
				minval = xs[i];
		# 2. Find the point "vstart" making the greatest angle with "minind"
		maxangle = -9999;
		vstart = -1;
		for i in range(len(xs)):
			if (i != minind):
				angle = (ys[i] - ys[minind])/(xs[i] - xs[minind]);
				if (angle > maxangle):
					maxangle = angle;
					vstart = i;
	
		## Plotting ##
		plt.ion();
		fig, ax = plt.subplots();
		plt.ylim([-2, 12]);
		plt.xlim([-2, 12]);
		plt.scatter(xs, ys);
		plt.plot([xs[minind], xs[vstart]], [ys[minind], ys[vstart]]);
		fig.canvas.draw();
		fig.canvas.flush_events();
		plt.show();
		if stepmode:
			a = input("Press Enter to step or c to continue:")
			if a == 'c':
				stepmode = False
				print("finishing...")
		else:
			time.sleep(0.01);
		## -------- ##
	
		# v1 is the vector from vstart->prevstart
		prevstart = minind;
		v1 = [ xs[minind] - xs[vstart], ys[minind] - ys[vstart] ];
		# v2 is the vector from vstart->v2end
	
		# 3. iterate through all the v2ends and choose the one that makes the greatest angle with v1. Set v1 to v2end_final->vstart, and repeat until we have wrapped back around to the starting index.
	
		while (vstart != minind):
			maxangle = -9999;
			v2end_final = -1;
			save = 0;
			for v2end in range(len(xs)):
				if (v2end != vstart and v2end != prevstart):
					v2 = [ xs[v2end] - xs[vstart], ys[v2end] - ys[vstart] ];
				
					## Plotting ##
					lines = plt.plot([xs[v2end], xs[vstart]], [ys[v2end], ys[vstart]]);
					plt.show();
					fig.canvas.draw();
					fig.canvas.flush_events();
					if stepmode:
						a = input("Press Enter to step or c to continue:")
						if a == 'c':
							stepmode = False
							print("finishing...")
					else:
						time.sleep(0.01);
					lines.pop(0).remove();
					plt.show();
					## -------- ##
				
					angle = vector.angle(v1, v2);
					if (angle > maxangle):
						## Plotting ##
						if (save != 0):
							save.pop(0).remove();
						save = plt.plot([xs[v2end], xs[vstart]], [ys[v2end], ys[vstart]]);
						plt.show();
						## -------- ##
						maxangle = angle;
						v2end_final = v2end;
			plt.plot([xs[v2end_final], xs[vstart]], [ys[v2end_final], ys[vstart]]);
			plt.show();
			v1 = [ xs[vstart] - xs[v2end_final], ys[vstart] - ys[v2end_final] ];
			prevstart = vstart;
			vstart = v2end_final;
		stepmode = True
		print("finished")
		plt.ioff();
		display_plot();
	except:
		plt.ioff();
		plt.close("all")

"""
name: grahams_scan()
purpose: Animate Graham's Scan algorithm and find the convex hull of a set of points
postcondition: Uses graham's scan to find the list of points that make up the convex hull
"""
def grahams_scan():
	try:
		import vector;
		import time;
	
		print("Convex Hull using gift Graham's Scan");
		global xs;
		global ys;
		global points;
		points = [];
		stepmode = True;
		# 1. Find leftmost
		minval = xs[0];
		minind = 0;
		for i in range(len(xs)):
			if (xs[i] < minval):
				minind = i;
				minval = xs[i];
		leftest = point( xs[minind], ys[minind] );
		# 2. Sort points by polar angle
		for i in range(len(xs)):
			if (i != minind):
				newpoint = point( xs[i], ys[i] );
				newpoint.angle = (ys[i] - ys[minind])/(xs[i] - xs[minind]);
				points.append(newpoint);
		points.sort(key=lambda x: x.angle, reverse=False);
		points.append(leftest);
	
		## Plotting ##
		plt.ion();
		fig, ax = plt.subplots();
		plt.ylim([-2, 12]);
		plt.xlim([-2, 12]);
		plt.scatter(xs, ys);
		plt.plot([points[len(points)-1].x, points[0].x], [points[len(points)-1].y, points[0].y]);
		fig.canvas.draw();
		fig.canvas.flush_events();
		plt.show();
		if stepmode:
			a = input("Press Enter to step or c to continue:")
			if a == 'c':
				stepmode = False
				print("finishing...")
		else:
			time.sleep(0.01);
		## -------- ##
	
		# 3. While end point doesn't equal initial start point
		end = 0;
		lines = [];
		while end != len(points)-1:
			# Get next point
		
			## Plotting ##
			lines.append( plt.plot([points[end].x, points[end+1].x], [points[end].y, points[end+1].y]) );
			plt.show();
			fig.canvas.draw();
			fig.canvas.flush_events();
			if stepmode:
				a = input("Press Enter to step or c to continue:")
				if a == 'c':
					stepmode = False
			else:
				time.sleep(0.01);
			## -------- ##
		
			# 4. (end-1) <-v1- (end) -v2-> (end+1)
			v1 = [ points[end].x - points[end-1].x, points[end].y - points[end-1].y ];
			v2 = [ points[end].x - points[end+1].x, points[end].y - points[end+1].y ];

			angle = vector.fullangle(v2, v1);
			while angle <= 0.0:
				points.pop(end);
				end -= 1;
			
				## Plotting ##
				if len(lines) > 1:
					lines[len(lines)-1].pop(0).remove();
					lines[len(lines)-2].pop(0).remove();
					lines.pop(len(lines)-1);
					lines.pop(len(lines)-1);
				
				lines.append( plt.plot([points[end].x, points[end+1].x], [points[end].y, points[end+1].y]) );
				plt.show();
				fig.canvas.draw();
				fig.canvas.flush_events();
				if stepmode:
					a = input("Press Enter to step or c to continue:")
					if a == 'c':
						stepmode = False
						print("finishing...")
				else:
					time.sleep(0.01);
				## -------- ##
			
				v1 = [ points[end].x - points[end-1].x, points[end].y - points[end-1].y ];
				v2 = [ points[end].x - points[end+1].x, points[end].y - points[end+1].y ];
				angle = vector.fullangle(v2, v1);
			
				# Until the angle between this point and previous point is less than or equal to 180
		
				# Move previous point back by one
			end += 1;
		stepmod = True
		print("finished")
		plt.ioff();
		points = [];
	except:
		plt.ioff();
		plt.close("all")

"""
name: kd_tree()
purpose: Makes a kd tree. Also gives the option for finding the nearest neighbor
postcondition: kd tree is created and plotted. The nearest neighbor method uses best bin first search
"""
def kd_tree():
	try:
		from kdtree import kdtree
		from kdnode import kdnode
	
		print("Create Kd tree")
		global xs;
		global ys;
		global points;
	
		points = []
		for i in range(len(xs)):
			newpoint = point( xs[i], ys[i] );
			points.append(newpoint);
		
		maxbinsz = int( input("Enter max bin size (integer): ") );
		emax = 100;
	
		tree = kdtree(maxbinsz, emax);
		tree.timer = 0.05;
		## Plotting ##
		minx, miny, maxx, maxy = -2, -2, 12, 12;
		## -------- ##
		root = tree.makeTree( points, minx, miny, maxx, maxy);
		print("finished")
		ch = 0;
		prev = 0;
		rectangles = 0;
		while True:
			print("1. for nearest neighbor");
			print("0. Exit");
			try:
				ch = int(input())
			except ValueError:
				print("That's not an int!");
				continue;
			if ch == 1:
				print("Enter: x y NN");
				i = input();
				i = i.split(' ');
				try:
					query = [float(i[0]), float(i[1])];
				except ValueError:
					print("Could not convert string to float");
					continue;
				if (prev != 0):
					## Plotting ##
					prev.set_color('gray');
					prev.set_alpha(0.4);
					for rect in rectangles:
						rect.set_color('black');
						rect.set_alpha(0.05);
					## -------- ##
				prev, rectangles = tree.queuryNNwrap(query, int(i[2]));
				print("finished")
			elif ch == 0:
				plt.ioff();
				points = [];
				break;
	except:
		plt.ioff();
		plt.close("all")

def display_plot():
	plt.show()

def switcher(choice):
	if choice == 1:
		clear()
		seed()
	elif choice == 2:
		clear()
	elif choice == 3:
		custom()
	elif choice == 4:
		gift_wrapping()
	elif choice == 5:
		grahams_scan()
	elif choice == 6:
		kd_tree()
	else:
		sys.exit(0)

if __name__ == "__main__":
   # xs, ys list the x and y coordinates of the points
	global xs;
	global ys;
	global points;
	points = [];

	introduction_prompt()
	xs = (rand(100)*10).tolist()
	ys = (rand(100)*10).tolist()
	while True:
		choice = main_menu()
		switcher(choice)
