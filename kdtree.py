from kdnode import kdnode;
from quickselect import select;
import matplotlib.pyplot as plt;
from matplotlib.patches import Rectangle;
import time;
import numpy;
import heapq
from point import point

def sqedEucDist(p1, p2):
	s = 0;
	for d in range( 2 ):
		s += pow(p1[d] - p2[d], 2);
	return s;

class kdtree:
	def __init__(self, binsize, e):
		self.root = 0;
		self.pts = 0;
		self.maxbinsz = binsize;
		self.emax = e;
		self.timer = 0.5;
	
	def maxRangeDim(self, points, start, end):
		dims = 2;
		mins = [];
		rnge = [];
		for d in range(dims):
			mins.append( points[start][d] );
			rnge.append(0);
			
		for p in range(start, end):
			for d in range(dims):
				if (points[p][d] > rnge[d]):
					rnge[d] = points[p][d]; # range holds maxs
				if (points[p][d] < mins[d]):
					mins[d] = points[p][d]; # min holds mins
		maxd = 0; # find the dimension with the biggest range
		for d in range(dims):
			rnge[d] -= mins[d];
			if (rnge[d] > rnge[maxd]):
				maxd = d;
		return maxd;
	
	def partition(self, points, start, end, cutdim, minx, miny, maxx, maxy):
		n = kdnode();
		n.st = start;
		n.end = end;
		n.minx = minx;
		n.miny = miny;
		n.width = maxx-minx;
		n.height = maxy-miny;
		if ( cutdim >= 2 ):
			cutdim = 0;
		if ( (end-start) > self.maxbinsz ):
			med = select(points, int( (start+end)/2 )-start, cutdim, start, end-1);
			n.dim = cutdim;
			n.val = med;
			## Plotting ##
			s = [minx, miny];
			e = [maxx, maxy];
			s[n.dim] = n.val[n.dim];
			e[n.dim] = n.val[n.dim];
			plt.plot([s[0], e[0]], [s[1], e[1]]);
			self.fig.canvas.draw();
			self.fig.canvas.flush_events();
			plt.show();
			time.sleep(self.timer);
			## -------- ##
			mid = int( (start+end)/2 );
			if (cutdim == 0):
				n.lessChild = self.partition(points, start, mid, cutdim+1, minx, miny, e[0], maxy);
				n.greaterChild = self.partition(points, mid, end, cutdim+1, s[0], miny, maxx, maxy);
			elif (cutdim == 1):
				n.lessChild = self.partition(points, start, mid, cutdim+1, minx, miny, maxx, e[1]);
				n.greaterChild = self.partition(points, mid, end, cutdim+1, minx, s[1], maxx, maxy);
		return n;
	
	def makeTree(self, points, minx, miny, maxx, maxy):
		## Plotting ##
		plt.ion();
		self.fig, self.ax = plt.subplots();
		plt.ylim([-2, 12]);
		plt.xlim([-2, 12]);
		plt.scatter([p.x for p in points], [p.y for p in points]);
		## -------- ##
		cutdim = self.maxRangeDim( points, 0, len(points) );
		self.root = self.partition( points, 0, len(points), cutdim, minx, miny, maxx, maxy );
		self.pts = points;
		return self.root;

	def queuryNNwrap(self, queury, n):
		## Plotting ##
		self.currentAxis = plt.gca();
		qpt = plt.scatter(queury[0], queury[1], marker=u'x', color='black', s=50);
		## -------- ##
		NNs = self.queuryNN(queury, n, self.root);
		return NNs;

	def queuryNN(self, queury, n, root):
		distances = [];
		NNs = [];
		plotted = [];
		for i in range(n):
			distances.append(9999999999); # nearest neighbor distances initialized to infinity
			NNs.append((-1, -1)); # nearest neighbor indices initialized to -1
			plotted.append(point(-100, -100));
		ordering = [];
		
		dx = max(root.minx - queury[0], 0, queury[0] - root.minx-root.width);
		dy = max(root.miny - queury[1], 0, queury[1] - root.miny-root.height);
		root.dist = dx*dx + dy*dy;
		heapq.heappush( ordering, root );
		count = 0;
		rectangles = [];
		while (len(ordering) != 0 and count < self.emax):
			dCur = heapq.heappop(ordering);
			while (dCur.dim != -1):
				dx = max(dCur.greaterChild.minx - queury[0], 0, queury[0] - dCur.greaterChild.minx-dCur.greaterChild.width);
				dy = max(dCur.greaterChild.miny - queury[1], 0, queury[1] - dCur.greaterChild.miny-dCur.greaterChild.height);
				dCur.greaterChild.dist = dx*dx + dy*dy;
				
				dx = max(dCur.lessChild.minx - queury[0], 0, queury[0] - dCur.lessChild.minx-dCur.lessChild.width);
				dy = max(dCur.lessChild.miny - queury[1], 0, queury[1] - dCur.lessChild.miny-dCur.lessChild.height);
				dCur.lessChild.dist = dx*dx + dy*dy;

				heapq.heappush( ordering, dCur.greaterChild );
				heapq.heappush( ordering, dCur.lessChild );
				dCur = heapq.heappop(ordering);
			if (dCur.dist < distances[0]):
				## Plotting ##
				rect = self.currentAxis.add_patch( Rectangle( (dCur.minx, dCur.miny), dCur.width, dCur.height, alpha=0.3, color=numpy.random.rand(3,1) ) );
				rectangles.append(rect);
				## -------- ##
				for i in range( dCur.st, dCur.end ):
					## Plotting ##
					prev = plt.scatter([p.x for p in plotted], [p.y for p in plotted], color='red', marker=u's');
					cur = plt.scatter( self.pts[i][0], self.pts[i][1], color='black', s = 50);
					self.fig.canvas.draw();
					self.fig.canvas.flush_events();
					plt.show();
					time.sleep(0.5);
					cur.remove();
					prev.remove();
					## -------- ##
					dist = sqedEucDist(self.pts[i], queury);
					if (dist < distances[0]):
						distances[0] = dist;
						NNs[0] = self.pts[i];
						
						plotted[0] = self.pts[i];
						ii = 0;
						while (ii < n-1 and distances[ii] < distances[ii+1]):
							distances[ii] = distances[ii+1];
							distances[ii+1] = dist;
							NNs[ii] = NNs[ii+1];
							NNs[ii+1] = self.pts[i];
							
							plotted[ii] = plotted[ii+1];
							plotted[ii+1] = self.pts[i];
							ii += 1;
				count += 1;
			else:
				break;
		## Plotting ##
		prev = plt.scatter([p.x for p in plotted], [p.y for p in plotted], color='red', s = 50);
		## -------- ##
		return prev, rectangles;


	
		

