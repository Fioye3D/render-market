"""Original fictional environment studies, not scans or heritage replicas."""
import sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from lagos_scene_kit import *
name=sys.argv[sys.argv.index('--')+1];random.seed(811)
setup(22,camera=(17,-23,16),target=(0,0,1.5))
s=bpy.context.scene;s.cycles.samples=16;s.render.resolution_x=960;s.render.resolution_y=720
earth=mat('Laterite soil',(.23,.105,.045),rough=.96);sand=mat('Weathered earthen plaster',(.48,.29,.14),rough=.92);thatch=mat('Dry woven grass',(.31,.24,.105),rough=.98);water=mat('River water',(.035,.14,.12),rough=.18);bark=mat('Tree bark',(.105,.055,.027),rough=.94)
for material in [earth,sand,thatch,bark]:
 n=material.node_tree.nodes;links=material.node_tree.links;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=18;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.28;bump.inputs['Distance'].default_value=.07;links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
box('Earth plot',(0,0,-.13),(18,15,.3),earth,.06)
def leaf(a,b,width=.12,m=None):
 a,b=Vector(a),Vector(b);mid=(a+b)*.5;side=(b-a).cross(Vector((0,0,1))).normalized()*width
 verts=[a,mid+side, b,mid-side,mid+Vector((0,0,.045))];mesh=bpy.data.meshes.new('Leaf blade');mesh.from_pydata(verts,[],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)]);o=bpy.data.objects.new('Leaf',mesh);bpy.context.collection.objects.link(o);mesh.materials.append(m or M['leaf'])
def tree(x,y,h=4,cocoa=False):
 rod('Trunk',(x,y,0),(x+.08,y,h*.75),.14,bark)
 for i in range(6):
  a=i*2.4;end=(x+math.cos(a)*1.1,y+math.sin(a)*1.1,h*.7+random.uniform(-.2,.6));rod('Branch',(x,y,h*.45),end,.055,bark)
  for j in range(7):
   q=Vector(end)+Vector((random.uniform(-.6,.6),random.uniform(-.6,.6),random.uniform(-.2,.4)));leaf(q,q+Vector((random.uniform(-.5,.5),random.uniform(-.5,.5),.15)),.18)
 if cocoa:
  for i in range(6):
   a=i*2.1;ellipsoid('Cocoa pod',(x+.2*math.cos(a),y+.2*math.sin(a),.7+i*.22),(.1,.13,.24),M['ochre'],16,10)
def hut(x,y,r=1.7):
 cylinder('Round earthen wall',(x,y,1.05),r,2.1,sand,64)
 box('Dark doorway',(x,y-r-.013,.88),(.72,.035,1.76),M['ink'],.02)
 for z in [1.35,1.55]:box('Window shutter',(x+r*.75,y-r*.7,z),(.45,.05,.16),M['walnut'])
 bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=r+.42,radius2=.12,depth=1.65,location=(x,y,2.82));o=bpy.context.object;o.name='Conical thatch roof';o.data.materials.append(thatch)
 for i in range(72):
  a=i*math.tau/72;rod('Roof thatch ridge',(x+.12*math.cos(a),y+.12*math.sin(a),3.64),(x+(r+.43)*math.cos(a),y+(r+.43)*math.sin(a),2),.025,thatch)
 for i in range(8):
  a=i*math.tau/8;rod('Veranda pole',(x+(r+.2)*math.cos(a),y+(r+.2)*math.sin(a),0),(x+(r+.2)*math.cos(a),y+(r+.2)*math.sin(a),2.05),.045,bark)
def fence(x1=-7,x2=7,y=5):
 for x in range(x1,x2+1,2):rod('Fence post',(x,y,0),(x,y,1.25),.06,bark)
 for z in [.45,.95]:rod('Fence rail',(x1,y,z),(x2,y,z),.035,bark)
def cow(x,y,angle=0):
 before=set(bpy.context.scene.objects);hide=M['cream'] if random.random()>.4 else M['white']
 ellipsoid('Cattle torso',(x,y,1.03),(.37,.83,.43),hide,32,16);ellipsoid('Shoulders',(x,y-.48,1.17),(.31,.35,.4),hide)
 ellipsoid('Neck',(x,y-.83,1.17),(.2,.35,.34),hide);ellipsoid('Head',(x,y-1.09,1.28),(.19,.33,.25),hide)
 ellipsoid('Muzzle',(x,y-1.32,1.19),(.16,.14,.12),M['leather'])
 for side in [-1,1]:
  ellipsoid('Ear',(x+side*.28,y-.99,1.43),(.2,.095,.055),hide)
  ellipsoid('Eye',(x+side*.17,y-1.15,1.39),(.025,.025,.025),M['ink'],12,8)
  line('Long upward horn',[(x+side*.1,y-.99,1.49),(x+side*.23,y-.95,1.73),(x+side*.32,y-.92,2.02)],.025,M['cream'])
  for dy in [-.5,.52]:
   rod('Leg',(x+side*.23,y+dy,1),(x+side*.24,y+dy,.14),.064,hide);ellipsoid('Hoof',(x+side*.24,y+dy-.035,.09),(.075,.11,.085),M['leather'],16,8)
 line('Tail',[(x,y+.74,1.18),(x+.09,y+.98,.8),(x+.12,y+1.02,.39)],.022,hide);ellipsoid('Tail tuft',(x+.12,y+1.02,.34),(.05,.04,.1),M['hair'],12,8)
 rotate_group(set(bpy.context.scene.objects)-before,(x,y,0),angle)
def crop(x,y,kind):
 if kind=='yam':
  rod('Yam stake',(x,y,0),(x+.05,y,1.8),.018,bark)
  for i in range(7):
   z=.2+i*.21;a=i*2;leaf((x,y,z),(x+math.cos(a)*.38,y+math.sin(a)*.38,z+.1),.13)
 elif kind=='maize':
  h=random.uniform(1.4,2);rod('Maize stalk',(x,y,0),(x,y,h),.018,M['leaf'])
  for i in range(5):
   z=.25+i*.27;side=(-1)**i;leaf((x,y,z),(x+side*.55,y+.14,z+.16),.065)
  for i in [-1,0,1]:rod('Tassel',(x,y,h),(x+i*.12,y+.04,h+.22),.008,M['cream'])
  ellipsoid('Husk',(x+.075,y,.88),(.05,.05,.2),M['leaf'],12,8)
def farm(kind):
 if kind=='cocoa':
  for x in [-5,-1.5,2,5.5]:
   for y in [-3,1,5]:tree(x,y,3.5,True)
 else:
  for i in range(9):
   x=-6+i*1.5;box('Raised planting ridge',(x,0,.08),(.7,12,.16),earth,.12)
   for j in range(12):crop(x,-5.5+j,kind)
 fence();hut(6,-5,1.05)
def mosque():
 box('Prayer hall',(0,1,1.5),(6,5,3),M['plaster']);box('Courtyard', (0,-3,.05),(9,4,.12),M['concrete'])
 for x in [-2,-1,0,1,2]:
  box('Entrance recess',(x,-1.53,1.05),(.6,.04,1.8),M['navy']);ellipsoid('Arched opening',(x,-1.53,1.92),(.3,.04,.36),M['navy'])
 ellipsoid('Central dome',(0,1,3.05),(1.7,1.7,1.1),M['cream'],48,24)
 for x in [-4,4]:
  cylinder('Minaret',(x,2,2.8),.38,5.6,M['plaster'],32);cylinder('Balcony',(x,2,4.65),.62,.18,M['cream'],32)
  bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.5,radius2=0,depth=.9,location=(x,2,6));bpy.context.object.data.materials.append(M['cream'])
def palace():
 box('Royal courtyard',(0,0,.03),(13,11,.15),M['concrete']);box('Rear palace hall',(0,3,1.6),(10,3.3,3.2),sand)
 for x in [-4,-2,0,2,4]:
  box('Recessed door',(x,1.3,1.25),(.9,.04,2.5),M['walnut']);rod('Veranda column',(x-.65,.45,0),(x-.65,.45,3.1),.13,sand)
 box('Colonnade canopy',(0,.7,3.15),(11,1.8,.2),M['cream']);box('Ceremonial platform',(0,-2,.25),(4,2,.5),sand)
 for x in [-5.5,5.5]:box('Courtyard wing',(x,0,1.2),(1.1,8,2.4),sand)
 for x in [-4.6,4.6]:cylinder('Entrance pillar',(x,-5,1.6),.33,3.2,sand,48)
 for x in [-2,2]:bowl(x,-1.8,.54,.35,'ceramic',.4)
if name=='rural-hut':hut(0,0);tree(-4,3);tree(4,4);fence()
elif name=='rural-village':
 for x,y,r in [(-4,2,1.5),(0,3,1.7),(4,2,1.5),(-4,-3,1.25),(4,-3,1.3)]:hut(x,y,r)
 tree(-7,5);tree(6,5);fence()
elif name=='river-landscape':
 box('River',(0,0,.09),(5,15,.08),water,.03)
 for side in [-1,1]:
  for i in range(8):
   y=-6+i*1.8;x=side*random.uniform(3,5);ellipsoid('Riverbank stone',(x,y,.1),(.65,.45,.3),M['concrete'],16,8)
  for y in [-5,0,5]:tree(side*6,y,3.5)
 for i in range(12):box('Water ripple',(random.uniform(-2,2),random.uniform(-6,6),.14),(random.uniform(.3,1),.015,.004),M['glass'],0)
elif name=='royal-courtyard':palace();tree(-7,5);tree(7,5)
elif name in ['yam-farm','cocoa-farm','maize-farm']:farm(name.split('-')[0])
elif name=='mixed-farm':
 for x in range(-6,7,2):
  for y in range(-5,6):crop(x,y,'yam' if x<0 else 'maize')
 hut(6,5,1.1);fence()
elif name in ['cattle-ranch','fulani-herdsman']:
 for i in range(6):cow(-4+(i%3)*3,-2+(i//3)*4,random.uniform(-.4,.4))
 fence();fence(y=-6);tree(-7,4)
 if name=='fulani-herdsman':
  person('Fictional adult herdsman',5,-2,shirt='white',headwrap=True);rod('Walking staff',(5.5,-2.1,0),(5.5,-2.1,1.8),.025,bark)
 else:box('Water trough',(5,2,.5),(1.1,2.4,.9),M['concrete']);box('Trough water',(5,2,.96),(.9,2.2,.02),water)
elif name=='courtyard-mosque':mosque();tree(-6,-3);tree(6,-3)
elif name=='herbalist-shrine':
 hut(0,3,2);tree(-5,2,5);tree(5,4,4);table(0,-1,1.9,.9,.75)
 for x in [-.6,0,.6]:bowl(x,-1,.8,.18,'oak',.18)
 for x in [-3,3]:
  for y in [-3,-1,1]:plant(x,y)
 person('Fictional adult herbalist',1.7,-.2,shirt='cream',headwrap=True)
 box('Preparation mat',(0,-3,.03),(3,1.6,.03),M['fabric'],0)
else:raise ValueError(name)
frame_render(.06);s.render.filepath=str(OUT/(name+'.png'));bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(name+'.blend')));bpy.ops.render.render(write_still=True)
print('RURAL_COMPLETE',name,flush=True)
