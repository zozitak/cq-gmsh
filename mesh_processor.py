import math
import os
import sys
import gmsh
import yaml

epsilon = 1e-9

def list_remove_duplicates(x):
  return list(dict.fromkeys(x))

def getAdjacencies(e):
    dim = e[0]
    tag = e[1]
    u, d = gmsh.model.getAdjacencies(dim,tag)
    return u, d

def getOneDimLessItems(list_e1):
    list_e0 = []
    for e in list_e1:
        temp_l0 = getAdjacencies(e)[1]
        list_e0.extend([(e[0]-1,ent) for ent in temp_l0])
    list_e0 = list_remove_duplicates(list_e0)
    return list_e0

# input list of entities (dim, tag) , dimension |: output list of entities in dimension from the input entities
# points_of_e = getDimEntities([(3,1),(3,2)],2) 
def getDimEntities(list_en,dimension):
    list_e0 = []
    #all of the items are in the same dimension and in range[0...3]
    if len(list_remove_duplicates([d for d,t in list_en])) == 1 and list_remove_duplicates([d for d,t in list_en])[0] >= 0 and list_remove_duplicates([d for d,t in list_en])[0] <= 3:
        if dimension >= 0 and dimension <= 3:
            list_e0 = getOneDimLessItems(list_en)
            if len(list_e0) == 0 or list_remove_duplicates([d for d,t in list_en])[0] == dimension:
                return list_en
            else:
                return getDimEntities(list_e0,dimension)
        else:
            raise ValueError("Dimension error")
    else:
        return []

#import CADQ geometry as .STEP file 
#import characteristics.yaml properties for the geometries
#choose meshing strategies for geometries 
#generate mesh
#export .msh 

gmsh.initialize()

#gmsh.option.setString('Geometry.OCCTargetUnit', 'M')

gmsh.model.add("geometry")

gmsh.model.occ.importShapes('./geometry/main.step', highestDimOnly=True, format="step")

gmsh.model.occ.synchronize()

#import yaml 
with open('./geometry/characteristics.yaml') as f:
    MainDict = yaml.full_load(f)

#find shapes 
geometry_names_from_yaml = list(MainDict["main"]["geometries"].keys())

e3_list = []
entities = gmsh.model.getEntities(dim=3)
for e in entities:
    # Dimension and tag of the entity:
    dim = e[0]
    tag = e[1]

    # * Type and name of the entity:
    geometry_type = gmsh.model.getType(e[0], e[1])
    geometry_name = gmsh.model.getEntityName(e[0], e[1])

    #find name in yaml list 
    if len(geometry_name):
        if geometry_name.split("/")[-1][:-5] in geometry_names_from_yaml:
            e3_list.append(e)

#Pgroup shapes 
for e in e3_list: 
    dim = e[0]
    tag = e[1]
    tag_list = [tag]
    geometry_name = gmsh.model.getEntityName(e[0], e[1])
    gmsh.model.addPhysicalGroup(dim,tag_list,name = geometry_name.split("/")[-1][:-5])

#find boundaries in yaml 
e_list = []
entities = gmsh.model.getEntities(dim=-1)

for shape_name, tag_dicts in MainDict["main"]["boundaries"].items():
    for tag_name, tag_dict in tag_dicts.items():
        
        #get "shape_name" [(dim,tag)]
        pgrps = gmsh.model.getPhysicalGroups()
        search_group = ()
        for pgrp in pgrps:
            dimgroup = pgrp[0]  # 1D, 2D or 3D
            taggroup = pgrp[1]
            group_name = gmsh.model.getPhysicalName(dimgroup, taggroup)
            if group_name == shape_name: 
                search_group = (dimgroup,taggroup)
                break
        
        vEntities = gmsh.model.getEntitiesForPhysicalGroup(search_group[0], search_group[1])
        list_e = [(search_group[0],i) for i in vEntities]
        
        #get yaml vertex and make boundingbox entity search with its coords ->
        list_geom_dtgs = []
        list_check_points = getDimEntities(list_e,0)
        shape_dim = 0
        for hash_code, geo_dict in tag_dict.items(): 
            shape_dim = geo_dict["shape dim"]
            p_dim_tags = []
            for vertex in geo_dict["vertices"]:
                x, y, z = vertex[0], vertex[1], vertex[2]
                p_tags = []
                p_tags = gmsh.model.get_entities_in_bounding_box(x - epsilon, y - epsilon, z - epsilon,x + epsilon, y + epsilon, z + epsilon,dim=0)
                p_dim_tags.extend(p_tags)

            for e in p_dim_tags:
                if not set([e]).issubset(list_check_points):
                    p_dim_tags.remove(e)
            
            for entity in getDimEntities(list_e,shape_dim):
                if set(p_dim_tags).issubset(getDimEntities([entity],0)):
                    list_geom_dtgs.append(entity)
                
        gmsh.model.addPhysicalGroup(shape_dim, [t for d, t in list_geom_dtgs], name = tag_name) 

#generate mesh
gmsh.model.mesh.generate(3)

#export mesh
gmsh.write("./mesh/main.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

#TODO: create meshing strategies tetra, hex, linear, quadratic meshes

"""
#import geometry to gmsh
gmsh.initialize()

gmsh.option.setString('Geometry.OCCTargetUnit', 'M')

gmsh.model.add("box")

path = os.path.dirname(os.path.abspath(__file__))
v = gmsh.model.occ.importShapes('./geometry/box.step')

gmsh.model.occ.synchronize()

#generate mesh
gmsh.model.mesh.generate(3)

#export mesh
gmsh.write("./mesh/box.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

"""
