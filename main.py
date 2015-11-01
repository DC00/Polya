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
    print("4. Point Location")
    print("5. Range Search")
    print("6. Nearest Neighbor")
    print("7. Ray Tracing")
    print("8. Gift Wrapping")
    print("9. Grahams Scan")
    print("10. Fortunes Algorithm")
    print("\n0. Exit")
    print("\n############################################################\n")
    try:
        choice = int(input())
    except ValueError:
        print("That's not an int!")
    return choice

global xs;
global ys;
global points;
points = [];
xs = [];
ys = [];

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

def custom():
    plt.ioff();
    fig, ax = plt.subplots()
    plt.ylim([-2, 12]);
    plt.xlim([-2, 12]);
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
    import time;
    
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
    plt.ylim([-2, 12]);
    plt.xlim([-2, 12]);
    plt.scatter(xs, ys);
    plt.plot([xs[minind], xs[vstart]], [ys[minind], ys[vstart]]);
    fig.canvas.draw();
    fig.canvas.flush_events();
    plt.show();
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

def grahams_scan():
    import vector;
    import time;
    
    print("Convex Hull using gift Graham's Scan");
    global xs;
    global ys;
    global points;
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
        time.sleep(0.01);
        ## -------- ##
        
        # 4. (end-1) <-v1- (end) -v2-> (end+1)
        v1 = [ points[end].x - points[end-1].x, points[end].y - points[end-1].y ];
        v2 = [ points[end].x - points[end+1].x, points[end].y - points[end+1].y ];

        angle = vector.fullangle(v2, v1);
        while angle < 0:
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
            time.sleep(0.01);
            ## -------- ##
            
            v1 = [ points[end].x - points[end-1].x, points[end].y - points[end-1].y ];
            v2 = [ points[end].x - points[end+1].x, points[end].y - points[end+1].y ];
            angle = vector.fullangle(v2, v1);
            
            # Until the angle between this point and previous point is less than or equal to 180
        
            # Move previous point back by one
        end += 1;
    plt.ioff();
    points = [];

def fortunes():
    import vector;
    import time;
    
    print("Voronoi Diagram using Fortunes Algorithm");
    global xs;
    global ys;
    global points;
    # 2. Sort points by polar angle
    for i in range(len(xs)):
        newpoint = point( xs[i], ys[i] );
        points.append(newpoint);
    points.sort(key=lambda x: x.y, reverse=True);
    linepos = 12;
    ## Plotting ##
    plt.ion();
    fig, ax = plt.subplots();
    plt.ylim([-2, 12]);
    plt.xlim([-2, 12]);
    plt.scatter(xs, ys);
    ## -------- ##
    brkbot = 0
    brk = 0
    parabolas = []
    while linepos > -2:
        linepos -= 0.05;

        ## Plotting ##
        l = len(points)
        while brk < l and linepos < points[brk].y:
            brk += 1;
        for pt in range(brkbot, brk):
            # Use polyfit.
            x1 = [points[pt].x-0.02,points[pt].x,points[pt].x+0.02]
            y1 = [points[pt].y+1,points[pt].y,points[pt].y+1]
            coefficients1 = np.polyfit(x1,y1,2)
            polynomial = np.poly1d(coefficients1)
            # Feed data into pyplot.
            xpoints = np.linspace(points[pt].x-0.1, points[pt].x+0.1, 20)
            # Draw the plot to the screen
            parabolas.append( (plt.plot(xpoints,polynomial(xpoints),'-'), points[pt]) )
        
        for p in parabolas:
            pt = p[1]
            # Use polyfit.
            x1 = [pt.x-0.02, pt.x, pt.x+0.02]
            y1 = [pt.y+1, pt.y-0.3, pt.y+1]
            coefficients1 = np.polyfit(x1,y1,2)
            polynomial = np.poly1d(coefficients1)
            # Feed data into pyplot.
            xpoints = np.linspace(pt.x-0.1, pt.x+0.1, 20)
            p[0][0].set_xdata(xpoints);
            p[0][0].set_ydata(polynomial(xpoints));
            
        

        
        
        sweepline = plt.plot([-2, 12], [linepos, linepos], c = 'b');
        fig.canvas.draw();
        fig.canvas.flush_events();
        plt.show();
        time.sleep(0.001);
        sweepline.pop(0).remove();
        ## -------- ##
        brkbot = brk;
    points = [];
    

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
        point_location()
    elif choice == 5:
        range_search()
    elif choice == 6:
        nearest_neighbor()
    elif choice == 7:
        ray_trace()
    elif choice == 8:
        gift_wrapping()
    elif choice == 9:
        grahams_scan()
    elif choice == 10:
        fortunes()
    else:
        sys.exit(0)

if __name__ == "__main__":
    introduction_prompt()
    while True:
        choice = main_menu()
        switcher(choice)

