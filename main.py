# Driver for Menu
import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import normal, rand
from draw import customPointPlacer

def introduction_prompt():
    print("\nCS 4102 Final Project: A Workbench of Computational Geometry Algorithms\n")
    print("You have the ability to populate a 2D scatter plot with random points and then\nselect from several algorithms to play with the data\n")

def main_menu():
    choice = 0
    print("\n\n\n############################################################\n")
    print("Enter number of selection")
    print("1. Clear and Seed: Generate a set of new, random points for the scatter plot")
    print("2. Clear: Clear the plot of all points")
    print("3. Place Custom Points")
    print("Algorithms")
    print("4. Point Location")
    print("5. Range Search")
    print("6. Nearest Neighbor")
    print("7. Ray Tracing")
    print("8. Gift Wrapping")
    print("\n0. Exit")
    print("\n############################################################\n\n\n")
    try:
        choice = int(input())
    except ValueError:
        print("That's not an int!")
    return choice

global xs;
global ys;
xs = [];
ys = [];

def seed():
    print("Seeding graph...")
    global xs;
    global ys;
    xs = rand(100).tolist()
    ys = rand(100).tolist()
    plt.scatter(xs,ys)
    display_plot()

def clear():
    print("Clearing graph...")
    xs = [];
    ys = [];
    plt.clf()

def custom():
    fig, ax = plt.subplots()
    ax.set_xlim((-1,1))
    ax.set_ylim((-1,1))
    p = customPointPlacer(fig, ax, xs, ys)
    print("Press i to insert")
    
    canvas = fig.canvas
    canvas.mpl_connect('key_press_event', p.key_press_callback)
    display_plot();

def point_location():
    print("Enter number of points to place: ", end=' ')
    n = int(input())

def range_search():
    print("Range Search: Compute the number of points within a query region")

def nearest_neighbor():
    print("Nearest Neighbor: Compute the closest point to a query point")

def ray_trace():
    print("Ray Trace: Compute the point which first intersects a query ray")

def gift_wrapping():
    import vector;
    import time
    
    print("Convex Hull using gift wrapping method");
    global xs;
    global ys;
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
    plt.scatter(xs, ys);
    plt.plot([xs[minind], xs[vstart]], [ys[minind], ys[vstart]]);
    fig.canvas.draw();
    fig.canvas.flush_events();
    plt.show();
    time.sleep(0.5);
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
    plt.ioff();
    display_plot();

def display_plot():
    plt.show()

def switcher(choice):
    if choice == 1:
        seed()
    elif choice == 2:
        clear()
    elif choice == 3:
        custom()
    elif choice == 4:
        point_location()
    elif choice == 5:
        range_search()
    elif choice == 6:
        nearest_neighbor()
    elif choice == 7:
        ray_trace()
    elif choice == 8:
        gift_wrapping()
    else:
        sys.exit(0)

if __name__ == "__main__":
    introduction_prompt()
    while True:
        choice = main_menu()
        switcher(choice)

