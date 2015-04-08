import bpy
import math
import sys
import time
import os

#----ExampleUse----
##Output 32 images of Traffic_Cone_Base.stl, Traffic_Cone_Rings_Orange.stl and Traffic_Cone_Rings_White.stl contained in folder C:/Users/Tom/Downloads/cone/ in colours 1 0 0, 0 1 0, 0 0 1 to output folder C:/temp/. (Also redirects output to nul)
##blender -b -P C:\BlenderTest.py -- C:/Users/Tom/Downloads/cone/Traffic_Cone_Base.stl C:/Users/Tom/Downloads/cone/Traffic_Cone_Rings_Orange.stl C:/Users/Tom/Downloads/cone/Traffic_Cone_Rings_White.stl 1> nul

#name of single/multiple stl file
filenames = [] 

for i in range(0,len(sys.argv)):
	#print(sys.argv[i])	
	if sys.argv[i]=="--":
		argStart = i+1
		break
		
for i in range(argStart,len(sys.argv)):
	filenames = filenames + [sys.argv[i]]
	#print(os.path.split(sys.argv[i])[0])
	#print(os.path.split(sys.argv[i])[1])
	#print(sys.argv[i])

for i in range(0,len(filenames)):
	bpy.ops.import_mesh.stl(filepath=filenames[i], filter_glob="*.stl",  files=[{"name":os.path.split(filenames[i])[1], "name":os.path.split(filenames[i])[1]}], directory=os.path.split(filenames[i])[0])
	bpy.context.selected_objects[0].name = "STLObject"+str(i)
	

maximum = [float('-inf'),float('-inf'),float('-inf')]
minimum = [float('inf'),float('inf'),float('inf')]

for i in range(0,len(filenames)):
	maximum[0] = max(maximum[0],bpy.data.objects['STLObject'+str(i)].bound_box[6][0])
	maximum[1] = max(maximum[1],bpy.data.objects['STLObject'+str(i)].bound_box[6][1])
	maximum[2] = max(maximum[2],bpy.data.objects['STLObject'+str(i)].bound_box[6][2])
	minimum[0] = min(minimum[0],bpy.data.objects['STLObject'+str(i)].bound_box[0][0])
	minimum[1] = min(minimum[1],bpy.data.objects['STLObject'+str(i)].bound_box[0][1])
	minimum[2] = min(minimum[2],bpy.data.objects['STLObject'+str(i)].bound_box[0][2])


print("SizeX: " + str(maximum[0]-minimum[0]))
print("SizeY: " + str(maximum[1]-minimum[1]))
print("SizeZ: " + str(maximum[2]-minimum[2]))