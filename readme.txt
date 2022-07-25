geometry -> defines geometry, tags, metadata, and includes it into a assembly.
geometry_processor -> exports .yaml file in ./geometry with the defined tags, exports step assembly 
mesh_processor -> handles gmsh import from .yaml+step 

gmsh.model.occ.importShapes doesn't support metadata or boundary import, thats why a wrote this little extension for CQ-gmsh import. 

requirements: 

pip install conda
conda install -c anaconda yaml
conda install -c conda-forge cadquery
conda install -c conda-forge gmsh
