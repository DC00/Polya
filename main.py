# Driver for Menu
import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import normal, rand
from draw import PolygonInteractor
from matplotlib.patches import Polygon

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
    print("\n0. Exit")
    print("\n############################################################\n\n\n")
    try:
        choice = int(input())
    except ValueError:
        print("That's not an int!")
    return choice

def seed():
    print("Seeding graph...")
    a = rand(100)
    b = rand(100)
    plt.scatter(a,b)
    display_plot()

def clear():
    print("Clearing graph...")
    plt.clf()

def custom():

    xs = [0]
    ys = [0]

    poly = Polygon(list(zip(xs, ys)), animated=True)

    fig, ax = plt.subplots()
    ax.add_patch(poly)
    p = PolygonInteractor(ax, poly)
    print("Press i to insert, d to delete")
    ax.set_title('Click and drag a point to move it')
    ax.set_xlim((-2,2))
    ax.set_ylim((-2,2))
    plt.show()

def point_location():
    print("Enter number of points to place: ", end=' ')
    n = int(input())

def range_search():
    print("Range Search: Compute the number of points within a query region")

def nearest_neighbor():
    print("Nearest Neighbor: Compute the closest point to a query point")

def ray_trace():
    print("Ray Trace: Compute the point which first intersects a query ray")

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
    else:
        sys.exit(0)

if __name__ == "__main__":
    introduction_prompt()
    while True:
        choice = main_menu()
        switcher(choice)
