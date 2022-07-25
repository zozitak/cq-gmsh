geometry -> defines geometry, tags, metadata, and includes it into a assembly.
geometry_processor -> exports .yaml file in ./geometry with the defined tags, exports step assembly 
mesh_processor -> handles gmsh import from .yaml+step 

gmsh.model.occ.importShapes doesn't support metadata or boundary import, thats why a wrote this little extension for CQ-gmsh import. 

requirements: 

pip install conda
conda install -c anaconda yaml
conda install -c conda-forge cadquery
conda install -c conda-forge gmsh

use: 

git clone https://github.com/zozitak/cq-gmsh.git <directory>
cd <directory>
#define CQ geometry into geometry.py, don't forget to add it into Assemby
python main.py
