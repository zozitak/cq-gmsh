import cadquery as cq 

def geometry_definition():
   #create cadquery geometry and assembly with metadata
   shape1 = (
       cq.Workplane("XZ").rect(1.0, 1.0)
       .extrude(1.0)
       .faces("+Z").tag("face_pozitive").end()
       .faces("-Z").tag("face_negative").end()
       )
   
#    shape2 = (
#        cq.Workplane("XY").rect(2.0, 2.0)
#        .extrude(0.5)
#        .faces("-Z").tag("face2").end()
#        .faces("-Z or +Z").tag("foobarzoo").end()
#        )
   
   Assembly = cq.Assembly(name="main",loc=cq.Location(cq.Vector(0,0,0),cq.Vector(1,0,0),0))
   Assembly.add(shape1,name="shape1",loc=cq.Location(cq.Vector(0,0,0),cq.Vector(1,0,0),0))
   #Assembly.add(shape2,name="shape2", loc=cq.Location(cq.Vector(0,-0.5,0.5),cq.Vector(1,0,0),45))
   #Assembly.constrain("shape1?face1", "shape2?face2", "Plane")
   #Assembly.solve()
   
   return Assembly

