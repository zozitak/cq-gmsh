import math
import os
import sys
from unittest import case
import yaml
import cadquery as cq 
from cadquery import exporters
from geometry import geometry_definition
import math

def geometries2dict(Assembly):
	GeometriesDictionary = {}
	GeometryDict = {}
	for i in Assembly.traverse():
		if len(i[1].shapes) != 0:
			#geometry
			item = i[1]
			GeometryDict = {}
			GeometryDict = {item.metadata.get("name",item.name):  
	                {"description": item.metadata.get("description"), 
	                "comment": item.metadata.get("comment"), 
	                "loc": item.metadata.get("location",item.loc.toTuple()),  
	                "material": item.metadata.get("material"),
					"boundary condition":item.metadata.get("boundary condition"),
					"other" : {}
	                } 
	               }
			GeometriesDictionary.update(GeometryDict)
		else: 
			#assembly
			pass	
	return GeometriesDictionary

def global_vertices(i,tag_object):
	list_of_v = []
	list_loc = []
	obj = i[1]
	while obj != None:
		list_loc.append(obj.loc)
		if obj.parent == None:
			break 
		else:
			obj = obj.parent
	
	list_loc = list(reversed(list_loc))
	loc_t = cq.Location()
	for loc in list_loc:
		loc_t = loc_t*loc 
	
	for vertex in tag_object.Vertices():
		temp_v = cq.Vertex.makeVertex(vertex.X,vertex.Y,vertex.Z)
		list_of_v.append(temp_v.located(loc_t).toTuple())

	return list_of_v

def gmshgetdimfromtype(shape_type):
	dim = -1
	if   shape_type == "Solid":
		dim = 3
	elif shape_type == "Face":
		dim = 2
	elif shape_type == "Edge":
		dim = 1
	elif shape_type == "Vertex":
		dim = 0
	else:
		dim = -1
	return dim 

def boundaries2dict(item):
	
	# shape_name: {tag_name : { vertices : []}}	
	BoundariesDictionary = {}

	for i in Assembly.traverse():
		if len(i[1].shapes) != 0:
			#boundaries
			item = i[1]
			BoundaryDict = {}
			BoundaryDict = {item.metadata.get("name",item.name):  {} }
			tags = item.obj.ctx.tags
			for k, v in tags.items():
				BoundaryDict[item.metadata.get("name",item.name)].update({k:{}})
				for ob in v.objects:
					BoundaryDict[item.metadata.get("name",item.name)][k].update(
						{ob.hashCode(): 
							{
								"shape type": v.objects[0].ShapeType(),
								"shape dim": gmshgetdimfromtype(v.objects[0].ShapeType()), 
								"vertices" : global_vertices(i,ob)
								}
							}
						)
			BoundariesDictionary.update(BoundaryDict)
		else: 
			#general assembly
			pass	

	return BoundariesDictionary

#create cadquery geometry and assembly with metadata
Assembly = geometry_definition()

#create Dictionary for YAML export
MainDict = {"main": {}}
MainDict["main"].update({"geometries": {},"boundaries": {},"meshes":{} ,"simulation":{}})
MainDict["main"]["geometries"].update(geometries2dict(Assembly))
MainDict["main"]["boundaries"].update(boundaries2dict(Assembly))

#export .yaml and .step 
with open(r'./geometry/characteristics.yaml', 'w') as file:
    doc = yaml.dump(MainDict, file, default_flow_style=None, sort_keys=False)

exporters.assembly.exportAssembly(Assembly,'./geometry/' + 'main' + '.step')
#exporters.export(shape, './geometry/' + 'main' + '.step', exporters.ExportTypes.STEP)
