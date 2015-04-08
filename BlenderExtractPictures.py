import bpy
import math
import sys
import time

pi = math.pi
cos = math.cos
sin = math.sin

#----ExampleUse----
##Output 32 images of Traffic_Cone_Base.stl, Traffic_Cone_Rings_Orange.stl and Traffic_Cone_Rings_White.stl contained in folder C:/Users/Tom/Downloads/cone/ in colours 1 0 0, 0 1 0, 0 0 1 to output folder C:/temp/. (Also redirects output to nul)
##blender -b -P C:\BlenderTest.py -- 32 "C:/Users/Tom/Downloads/cone/"  "C:/temp/" image .jpg Traffic_Cone_Base.stl 1 0 0 Traffic_Cone_Rings_Orange.stl 0 1 0 Traffic_Cone_Rings_White.stl 0 0 1 1> nul

#----Prerequisites----
#This file was made for Blender 2.72. It might not work on other blender versions					

#----Functions----
def wipeOutObject(ob,and_data=True) :
    
    data = bpy.data.objects[ob.name].data
    
    # never wipe data before unlink the ex-user object of the scene else crash (2.58 3 770 2) 
    # so if there's more than one user for this data, never wipeOutData. will be done with the last user
    # if in the list
    if data.users > 1 :
        and_data=False
    
    # odd :    
    ob=bpy.data.objects[ob.name]    
    # if the ob (board) argument comes from bpy.data.groups['aGroup'].objects,
    #  bpy.data.groups['board'].objects['board'].users_scene

    for sc in ob.users_scene :
        print(sc.name)
        sc.objects.unlink(ob)

    try : bpy.data.objects.remove(ob)
    except : print('data.objects.remove issue with %s'%ob.name)
    
    # never wipe data before unlink the ex-user object of the scene else crash (2.58 3 770 2) 
    if and_data :
        wipeOutData(data)    

def wipeOutData(data) :
    if data.users == 0 :
        try : 
            data.user_clear()
        
            # mesh
            if type(data) == bpy.types.Mesh :
                bpy.data.meshes.remove(data)
            # lamp
            elif type(data) == bpy.types.PointLamp :
                bpy.data.lamps.remove(data)
            # camera
            elif type(data) == bpy.types.Camera :
                bpy.data.cameras.remove(data)
            # Text, Curve
            elif type(data) in [ bpy.types.Curve, bpy.types.TextCurve ] :
                bpy.data.curves.remove(data)
            # metaball
            elif type(data) == bpy.types.MetaBall :
                bpy.data.metaballs.remove(data)
            # lattice
            elif type(data) == bpy.types.Lattice :
                bpy.data.lattices.remove(data)
            # armature
            elif type(data) == bpy.types.Armature :
                bpy.data.armatures.remove(data)
            else :
                print('data still here : forgot %s'%type(data))

        except :
            # empty, field
            print('%s has no user_clear attribute.'%data.name)
    else :
        print('%s has %s user(s) !'%(data.name,data.users))

def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 0
    return mat
	
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

#----Code----

#Number of images to take in 360 rotation
shots = 1 	
#Directory containing stl file (must end with a slash)
filepath = "" 	
#name of single/multiple stl file
filenames = [] 
colors = []
#Directory to store outputted images
outputpath = ""					
#base name of images
outputname = ""						
#filetype of images
outputfiletype = ""	
for i in range(0,len(sys.argv)):
	print(sys.argv[i])	
	if sys.argv[i]=="--":
		argStart = i+1
		break

shots = int(sys.argv[argStart])
print(shots)		
filepath = sys.argv[argStart+1]
print(filepath)
outputpath = sys.argv[argStart+2]
print(outputpath)
outputname = sys.argv[argStart+3]
print(outputname)
outputfiletype = sys.argv[argStart+4]
print(outputfiletype)

for i in range(argStart+5,len(sys.argv),4):
	filenames = filenames + [sys.argv[i]]
	print(sys.argv[i])
	color = (int(sys.argv[i+1]),int(sys.argv[i+2]),int(sys.argv[i+3]))
	colors = colors + [color]
	#print((int(sys.argv[i+1]),int(sys.argv[i+2]),int(sys.argv[i+3])))

print(colors)	
#Create new scene and name it STLScene
bpy.ops.scene.new(type='NEW')
bpy.context.scene.name = "STLScene"

#Add new camera and name it STLCamera
bpy.ops.object.camera_add()
bpy.context.object.name = "STLCamera"

#Set STLCamera as default camera for STLScene
bpy.data.scenes['STLScene'].camera = bpy.data.objects['STLCamera']

#Load our mesh(s) from STL file and name it STLObject
for i in range(0,len(filenames)):
	bpy.ops.import_mesh.stl(filepath=filepath+filenames[i], filter_glob="*.stl",  files=[{"name":filenames[i], "name":filenames[i]}], directory=filepath)
	bpy.context.object.name = "STLObject"+str(i)
	material = makeMaterial('Material'+str(i), colors[i], (0.5,0.5,0.5), 1)
	setMaterial(bpy.context.object, material)
	

#Give our scene light and name it STLLight
bpy.ops.object.lamp_add(type='HEMI')
bpy.context.object.name = "STLLight"


#Get minimum and maximum points of mesh(s) bounding box
maximum = [float('-inf'),float('-inf'),float('-inf')]
minimum = [float('inf'),float('inf'),float('inf')]

for i in range(0,len(filenames)):
	maximum[0] = max(maximum[0],bpy.data.objects['STLObject'+str(i)].bound_box[6][0])
	maximum[1] = max(maximum[1],bpy.data.objects['STLObject'+str(i)].bound_box[6][1])
	maximum[2] = max(maximum[2],bpy.data.objects['STLObject'+str(i)].bound_box[6][2])
	minimum[0] = min(minimum[0],bpy.data.objects['STLObject'+str(i)].bound_box[0][0])
	minimum[1] = min(minimum[1],bpy.data.objects['STLObject'+str(i)].bound_box[0][1])
	minimum[2] = min(minimum[2],bpy.data.objects['STLObject'+str(i)].bound_box[0][2])

#Select STLObject(s)
for i in range(0,len(filenames)):
	bpy.data.objects['STLObject'+str(i)].select = True

#Unselect all other objects
bpy.data.objects['STLLight'].select = False
bpy.data.objects['STLCamera'].select = False

#Move STLObject(s) to center point with object in positive z space
bpy.ops.transform.translate(value=((maximum[0]+minimum[0])*-0.5,(maximum[1]+minimum[1])*-0.5,-minimum[2]))

#Change cursor to 0,0,0 and set our object origin to cursor location
bpy.context.scene.cursor_location = (0.0,0.0,0.0)  
bpy.ops.object.origin_set(type='ORIGIN_CURSOR') 

#Calculate what number to scale object by to get it to maximally fit in 5x5x5 box
scale = 5/max((maximum[0]-minimum[0]),(maximum[1]-minimum[1]),(maximum[2]-minimum[2]))

#Resize STLObject by scale
bpy.ops.transform.resize(value=(scale,scale,scale))

#Loop 'shots' number of times to create 'shots' number of images
for i in range(0,shots):
	#Set angle from x axis
	theta = i*2*pi/shots

	#Calculate x,y from angle
	x = 16*cos(theta)
	y = 16*sin(theta)
	z = 8

	#Calculate the angle the camera needs to be to point at 0,0,0
	roll = theta - pi/2

	#Set camera location
	bpy.data.objects['STLCamera'].location[0] = x
	bpy.data.objects['STLCamera'].location[1] = y
	bpy.data.objects['STLCamera'].location[2] = z

	#Set camera rotation
	bpy.data.objects['STLCamera'].rotation_euler[0] = -1.9373154640197754
	bpy.data.objects['STLCamera'].rotation_euler[1] = pi
	bpy.data.objects['STLCamera'].rotation_euler[2] = roll
	
	#Set image output file path/name
	bpy.context.scene.render.filepath = outputpath+outputname+str(i)+outputfiletype
	
	#Output image
	bpy.ops.render.render(write_still=True)


for item in bpy.data.objects:  
	wipeOutObject(bpy.data.objects[item.name])

time.sleep(2)
print("bye")

