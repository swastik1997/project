from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Stock
from .serializers import StockSerializer
import random
import numpy as np
from shapely import geometry
from shapely.geometry import Point, LineString, shape, mapping
from shapely.geometry.polygon import LinearRing, Polygon
from geovoronoi import voronoi_regions_from_coords
import json
from shapely.ops import triangulate
from shapely.affinity import affine_transform
from django.http import JsonResponse

class StockList(APIView):
	def get(self,request):
		

		def random_points_within(poly, num_points):
		    min_x, min_y, max_x, max_y = poly.bounds

		    points = []

		    while len(points) < num_points:
		        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
		        if (random_point.within(poly)):
		            points.append(random_point)

		    return points


		lis=[]
		lis.append(geometry.Point(6.63104 ,3.96982))
		lis.append(geometry.Point(6.63106 ,3.9686))
		lis.append(geometry.Point(6.63167 ,3.96793))
		lis.append(geometry.Point(6.63114 ,3.96665))
		lis.append(geometry.Point(6.63209 ,3.96595))
		lis.append(geometry.Point(6.63275 ,3.9651))
		lis.append(geometry.Point(6.63338 ,3.96423))
		lis.append(geometry.Point(6.63586 ,3.96309))
		lis.append(geometry.Point(6.63945 ,3.96526))
		lis.append(geometry.Point(6.64067 ,3.9671))
		lis.append(geometry.Point(6.64193 ,3.96807))
		lis.append(geometry.Point(6.64255 ,3.9697))
		lis.append(geometry.Point(6.64214 ,3.97081))
		lis.append(geometry.Point(6.64076 ,3.97208))
		lis.append(geometry.Point(6.64076 ,3.97208))
		lis.append(geometry.Point(6.63777 ,3.97611))
		lis.append(geometry.Point(6.6362 ,3.97729))
		lis.append(geometry.Point(6.63411 ,3.97856))
		lis.append(geometry.Point(6.63098 ,3.97704))
		lis.append(geometry.Point(6.63184 ,3.97365))
		lis.append(geometry.Point(6.6331 ,3.97206))
		lis.append(geometry.Point(6.63384 ,3.96978))
		#with open('India.geojson') as f:
		#    js = json.load(f)
		#js=js['features'][0]
		#js=js['geometry']['coordinates'][0]
		#polygon=js[0]
		#lis=[]
		#for points in polygon:
		#    lis.append(geometry.Point(points[0],points[1]))
		#lis.append(geometry.Point(polygon[0][0],polygon[0][1]))
		poly = geometry.Polygon(lis)
		points = random_points_within(poly,10)
		checks = [point.within(poly) for point in points]
		coords=[ np.array((geom.xy[0][0], geom.xy[1][0])) for geom in points ]
		poly_shapes, pts, poly_to_pt_assignments = voronoi_regions_from_coords(coords, poly)
		mini=float('inf')
		maxi=0
		for i in poly_shapes:
		    if mini>i.area:
		        mini=i.area
		    if maxi<i.area:
		        maxi=i.area
		diff=maxi-mini
		for j in range(1000):
		    points1 = random_points_within(poly,10)
		    checks1 = [point.within(poly) for point in points1]
		    coords1=[ np.array((geom.xy[0][0], geom.xy[1][0])) for geom in points1 ]
		    poly_shapes1, pts, poly_to_pt_assignments1 = voronoi_regions_from_coords(coords1, poly)
		    mini=float('inf')
		    maxi=0
		    for i in poly_shapes1:
		        if mini>i.area:
		            mini=i.area
		        if maxi<i.area:
		            maxi=i.area
		    diff1=maxi-mini
		    if(diff>diff1):
		        diff=diff1
		        poly_shapes=poly_shapes1
		s=""
		s+=('[')
		for p10 in poly_shapes:
		    x, y = p10.exterior.coords.xy
		    s+=('{"type": "Feature","geometry":{"type": "Polygon","coordinates": [[')
		    for i in range(len(x)):
		        s+=('[')
		        s+=(str(x[i]))
		        s+=(', ')
		        s+=(str(y[i]))
		        s+=(']')
		        if(i!=len(x)-1):
		            s+=(', ')
		    s+=(']]}}')
		    if p10!=poly_shapes[len(poly_shapes)-1]:
		        s+=(',')
		s+=(']')
		response_data = {}
		response_data['result'] = 'error'
		response_data['message'] = s
		return JsonResponse(response_data)