"""Editable metre-scale kit for fictional contemporary Lagos catalogue scenes.
Human base geometry: MakeHuman bundled base.obj, CC0; see assets/vendor/makehuman.
All delivered figures are clothed adults; static poses, no animation/rig claim.
"""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector, Matrix
sys.path.insert(0,str(Path(__file__).parent))
from render_base import mat, light
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/artwork'
random.seed(417)
M={}

def box(name,loc,dim,m,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 # Metre-scaled planar UVs; image maps work in GLB, FBX and OBJ without baking.
 uv=o.data.uv_layers.active
 for face in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(face.normal[i]));axes=[i for i in range(3)if i!=axis]
  for li in face.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
 if bevel:
  b=o.modifiers.new('Manufactured edge radius','BEVEL');b.width=bevel;b.segments=2
  o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return o

def cylinder(name,loc,r,h,m,vertices=32,rot=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(m)
 if rot:o.rotation_euler=rot
 b=o.modifiers.new('Rim bevel','BEVEL');b.width=min(.008,h*.12);b.segments=2
 for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o

def ellipsoid(name,loc,scale,m,seg=24,rings=12):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(m)
 for p in o.data.polygons:p.use_smooth=True
 return o

def rod(name,a,b,r,m):
 a,b=Vector(a),Vector(b);o=cylinder(name,(a+b)/2,r,(a-b).length,m,16);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o

def line(name,points,r,m):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=2
 s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,v in zip(s.points,points):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(m);return o

def label(text,loc,size=.15,m=None):
 c=bpy.data.curves.new(text,'FONT');c.body=text;c.size=size;c.extrude=.0006;c.align_y='CENTER'
 font=ROOT/'assets/fonts/Inter.ttf'
 if font.exists():
  try:c.font=bpy.data.fonts.load(str(font),check_existing=True)
  except:pass
 o=bpy.data.objects.new('Sign / '+text,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(m or M['ink'])
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');return bpy.context.object

def palette():
 M.clear()
 specs={'white':((.76,.75,.69),.8,0),'ink':((.025,.035,.04),.5,0),'green':((.045,.14,.105),.56,0),'navy':((.035,.075,.12),.6,0),'blue':((.09,.19,.3),.73,0),'ochre':((.48,.29,.075),.8,0),'steel':((.45,.48,.48),.27,.88),'chrome':((.65,.67,.68),.15,.96),'blackmetal':((.035,.041,.042),.4,.7),'leather':((.033,.03,.026),.55,0),'ceramic':((.83,.82,.75),.25,0),'glass':((.19,.29,.3),.12,.5),'red':((.44,.07,.032),.6,0),'leaf':((.09,.23,.055),.8,0),'cream':((.59,.53,.38),.83,0),'skin':((.24,.105,.055),.58,0),'hair':((.019,.014,.011),.9,0)}
 for name,(color,rough,metal) in specs.items():M[name]=mat(name,color,metal,rough)
 for name in ['plaster','concrete','oak','walnut','terrazzo','fabric','turf','akara','asphalt']:
  m=mat(name,(.5,.5,.5),rough=.82 if name not in ['oak','walnut']else .53);n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(ROOT/'assets/textures/lagos-life'/(name+'.png')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);M[name]=m
 emit=M['light']=mat('Warm diffused light',(.92,.87,.68),rough=.3)
 p=emit.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.86,.66,1);p.inputs['Emission Strength'].default_value=1.5

def setup(size=9,camera=(9,-12,10),target=(0,0,1),ortho=None):
 bpy.ops.wm.read_factory_settings(use_empty=True);palette();s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=40;s.cycles.use_denoising=True
 s.render.resolution_x=1120;s.render.resolution_y=840;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX'
 s.world=bpy.data.worlds.new('Neutral daylight');s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.57,.64,.72,1);s.world.node_tree.nodes.get('Background').inputs[1].default_value=.45
 box('Studio floor',(0,0,-.23),(200,200,.18),mat('Backdrop',(.11,.13,.14),rough=.9),0)
 bpy.ops.object.camera_add(location=camera);cam=bpy.context.object;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=ortho or size;s.camera=cam
 light((-3,-5,9),1600,7,(1,.93,.82));light((6,1,7),1300,6,(.83,.9,1));light((-2,5,6),1000,5,(1,.95,.88))
 s.unit_settings.system='METRIC';s.unit_settings.length_unit='METERS';return s

def room(w=7,d=5,h=3,wall='plaster',floor='terrazzo'):
 box('Floor slab',(0,0,-.045),(w+.24,d+.24,.18),M['concrete'])
 box('Finished floor',(0,0,.055),(w,d,.04),M[floor],.004)
 # Two cutaway walls. Open edge is intentional for inspection, roof omitted.
 box('Rear wall',(0,d/2,h/2),(w,.14,h),M[wall])
 box('Side wall',(-w/2,0,h/2),(.14,d,h),M[wall])
 box('Rear skirting',(0,d/2-.09,.14),(w,.035,.13),M['ink'],.003)
 box('Side skirting',(-w/2+.09,0,.14),(.035,d,.13),M['ink'],.003)
 for x in range(-int(w/2),int(w/2)+1):box('Floor grout',(x,0,.077),(.008,d,.002),M['white'],0)
 for y in range(-int(d/2),int(d/2)+1):box('Floor grout',(0,y,.078),(w,.008,.002),M['white'],0)

def window(x,y,z=1.85,w=1.4,h=1.1):
 box('Window glass',(x,y,z),(w,.035,h),M['glass'],.002)
 for dx in [-w/2,0,w/2]:box('Aluminium mullion',(x+dx,y-.035,z),(.035,.045,h+.05),M['white'],.003)
 for dz in [-h/2,h/2]:box('Window frame',(x,y-.035,z+dz),(w+.05,.045,.035),M['white'],.003)
 box('Window sill',(x,y-.1,z-h/2-.03),(w+.14,.22,.05),M['concrete'],.005)

def chair(x,y,rotation=0,m='oak',seat=.47):
 objects=set(bpy.context.scene.objects)
 box('Chair seat',(x,y,seat),(.43,.43,.045),M[m],.02)
 box('Chair back',(x,y+.19,seat+.38),(.44,.045,.35),M[m],.016)
 for dx in (-.17,.17):
  for dy in (-.17,.17):rod('Chair leg',(x+dx,y+dy,.08),(x+dx,y+dy,seat-.02),.017,M['blackmetal'])
 rotate_group(set(bpy.context.scene.objects)-objects,(x,y,0),rotation)

def rotate_group(objects,pivot,angle):
 bpy.context.view_layer.update()
 rot=Matrix.Rotation(angle,4,'Z');t=Matrix.Translation(Vector(pivot));trans=t@rot@t.inverted()
 for o in objects:o.matrix_world=trans@o.matrix_world

def table(x,y,w=1.1,d=.7,h=.77):
 box('Oak table top',(x,y,h),(w,d,.045),M['oak'],.015)
 for dx in (-w*.39,w*.39):
  for dy in (-d*.34,d*.34):box('Table leg',(x+dx,y+dy,h/2),(.045,.045,h-.08),M['blackmetal'],.004)

def bowl(x,y,z,r=.12,m='steel',depth=.1):
 # Lathed open vessel, including inner wall and a rolled rim.
 profile=[(0,z),(.8*r,z),(.98*r,z+depth*.75),(r,z+depth),(.94*r,z+depth+.008),(.9*r,z+depth*.92),(.74*r,z+.014),(0,z+.014)]
 verts=[];faces=[];n=40
 for rr,zz in profile:
  for j in range(n):a=j*math.tau/n;verts.append((x+rr*math.cos(a),y+rr*math.sin(a),zz))
 for i in range(len(profile)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
 mesh=bpy.data.meshes.new('Open vessel');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Bowl / open inner wall',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(M[m])
 for f in mesh.polygons:f.use_smooth=True
 # Planar food/dish UVs.
 uv=mesh.uv_layers.new()
 for f in mesh.polygons:
  for li in f.loop_indices:v=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(v.x*2,v.y*2)
 return o

def plate(x,y,z,food=False):
 bowl(x,y,z,.14,'ceramic',.018)
 if food:
  for i in range(20):
   a=random.random()*math.tau;r=random.random()*.08;ellipsoid('Jollof rice portion',(x+math.cos(a)*r,y+math.sin(a)*r,z+.035),(.018,.009,.009),M['ochre'],12,6)
  ellipsoid('Stew portion',(x+.07,y,z+.043),(.043,.04,.024),M['red'],16,8)

def bottle(x,y,z,color='green'):
 cylinder('Unbranded drink bottle',(x,y,z+.11),.037,.2,M[color],24);cylinder('Bottle neck',(x,y,z+.24),.017,.07,M[color],20);cylinder('Bottle cap',(x,y,z+.28),.019,.015,M['steel'],20)

def clock(x,y,z=2.5):
 cylinder('Wall clock',(x,y,z),.19,.035,M['white'],48,(math.pi/2,0,0))
 for i in range(12):
  a=i*math.tau/12;rod('Clock index',(x+.147*math.sin(a),y-.024,z+.147*math.cos(a)),(x+.163*math.sin(a),y-.024,z+.163*math.cos(a)),.004,M['ink'])
 rod('Clock hour hand',(x,y-.03,z),(x-.07,y-.03,z+.04),.006,M['ink']);rod('Clock minute hand',(x,y-.034,z),(x+.05,y-.034,z+.12),.004,M['ink'])

def fan(x,y,z=2.5):
 cylinder('Wall fan grille',(x,y,z),.24,.06,M['blackmetal'],48,(math.pi/2,0,0))
 for j in range(20):
  a=j*math.tau/20;rod('Fan grille spoke',(x,y-.05,z),(x+.22*math.cos(a),y-.05,z+.22*math.sin(a)),.003,M['steel'])
 cylinder('Fan hub',(x,y-.07,z),.055,.045,M['white'],24,(math.pi/2,0,0))

def plant(x,y,z=0):
 bowl(x,y,z,.2,'concrete',.34)
 for i in range(10):
  a=i*2.4;tip=(x+.3*math.cos(a),y+.3*math.sin(a),z+.65+.23*(i%3));rod('Plant stem',(x,y,z+.3),tip,.009,M['green']);o=ellipsoid('Plant leaf',tip,(.055,.18,.016),M['leaf'],16,8);o.rotation_euler=(.45,0,a)

_human=None
def human_data():
 global _human
 if _human:return _human
 vertices=[];groups={};g='body'
 for l in (ROOT/'assets/vendor/makehuman/base.obj').open():
  if l.startswith('v '):
   x,y,z=map(float,l.split()[1:4]);vertices.append(Vector((x*.105,-z*.105,(y+8.168)*.105)))
  elif l.startswith('g '):g=l.strip()[2:]
  elif l.startswith('f '):groups.setdefault(g,[]).append(tuple(int(t.split('/')[0])-1 for t in l.split()[1:]))
 _human=vertices,groups;return _human

def person(name,x,y,angle=0,pose='stand',shirt='white',apron=False,headwrap=False):
 source,groups=human_data();before=set(bpy.context.scene.objects)
 # Use the neutral anatomy mesh with a loose garment shell; conceal torso/legs underneath.
 def transform(v):
  v=v.copy();side=1 if v.x>0 else -1
  is_arm=(abs(v.x)>.177 and v.z>1.28) or (abs(v.x)>.28 and v.z>.85)
  if is_arm:
   pivot=Vector((side*.176,-.015,1.409));weight=min(1,max(0,(abs(v.x)-.17)/.085));a=side*math.radians(34)*weight
   v=pivot+Matrix.Rotation(a,3,'Y')@(v-pivot)
  if pose in ['sit','work']:
   if pose=='sit' and v.z<.98 and not is_arm:
    knee=Vector((side*.166,-.034,.47));hip=Vector((side*.116,-.013,.91))
    if v.z<.51:v=knee+Matrix.Rotation(math.radians(88),3,'X')@(v-knee)
    v=hip+Matrix.Rotation(math.radians(-88)*min(1,max(0,(.98-v.z)/.1)),3,'X')@(v-hip)
   if pose=='sit':v.z-=.39
   elif is_arm and v.z<1.4:
    p=Vector((side*.2,-.025,1.3));v=p+Matrix.Rotation(math.radians(-48),3,'X')@(v-p)
  return v
 def meshpart(label,faces,material,inflate=0):
  ids=sorted(set(i for f in faces for i in f));lookup={j:i for i,j in enumerate(ids)};vs=[]
  for i in ids:
   v=source[i].copy()
   if inflate:
    v.x*=1+inflate;v.y*=1+inflate
   vs.append(transform(v))
  me=bpy.data.meshes.new(label);me.from_pydata(vs,[],[tuple(lookup[i]for i in f)for f in faces]);me.update();o=bpy.data.objects.new(name+' / '+label,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
  for p in me.polygons:p.use_smooth=True
  return o
 body=[];top=[];pants=[];shoes=[];scalp=[]
 for f in groups['body']:
  c=sum((source[i]for i in f),Vector())/len(f)
  if c.z<.12:shoes.append(f)
  elif c.z<.97 and abs(c.x)<.29:pants.append(f)
  elif c.z<1.5 and (abs(c.x)<.23 or c.z>1.20) and not(c.z>1.445 and abs(c.x)<.07):top.append(f)
  else:body.append(f)
  if c.z>1.66 or (c.z>1.55 and c.y>-.015):scalp.append(f)
 meshpart('Visible skin',body+top,M['skin'])
 garment=meshpart('Short sleeve shirt',top,M[shirt],.075)
 smooth=garment.modifiers.new('Relax fabric surface','SMOOTH');smooth.factor=.4;smooth.iterations=3
 hem=garment.modifiers.new('Garment edge thickness','SOLIDIFY');hem.thickness=.003
 meshpart('Trousers',pants,M['navy'],.05);meshpart('Shoes',shoes,M['leather'],.05);meshpart('Cropped hair',scalp,M['hair'],.025)
 for eye in ['helper-l-eye','helper-r-eye']:
  ids=set(i for f in groups[eye]for i in f);c=sum((source[i]for i in ids),Vector())/len(ids);c=transform(c);ellipsoid('Eyes',c,(.013,.014,.013),M['cream'],16,8);ellipsoid('Dark iris',(c.x,c.y-.012,c.z),(.006,.003,.006),M['ink'],12,8)
 if apron:
  zoff=-.39 if pose=='sit'else 0
  box('Apron bib',(0,-.13,1.23+zoff),(.29,.025,.33),M['green'],.015)
  box('Apron skirt',(0,-.145,.86+zoff),(.43,.03,.45),M['green'],.015)
  line('Apron neck strap',[(-.11,-.12,1.39+zoff),(-.09,-.08,1.49+zoff),(.09,-.08,1.49+zoff),(.11,-.12,1.39+zoff)],.011,M['green'])
 if headwrap:
  ellipsoid('Cloth headwrap',(0,.005,1.72),(.119,.115,.074),M['ochre'],32,16)
  ellipsoid('Tied cloth knot',(.105,.03,1.73),(.055,.065,.048),M['ochre'],24,12)
 after=set(bpy.context.scene.objects)-before
 bpy.context.view_layer.update()
 t=Matrix.Translation((x,y,.08))@Matrix.Rotation(angle,4,'Z')
 for o in after:o.matrix_world=t@o.matrix_world
 return after

def save(name,render=True):
 frame_render()
 s=bpy.context.scene;s['RenderMarket collection']='Lagos everyday life';s['Authorship']='Scripted scene with Codex assistance; MakeHuman CC0 human base where present';s['Characters']='Clothed adults in static poses; not rigged';s['View']='Two-wall cutaway or open site; no hidden complete building implied'
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(name+'.blend')))
 if render:s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
 print('LAGOS_SCENE_COMPLETE',name,flush=True)

def frame_render(margin=.055):
 """Keep the full authored scene inside the poster, excluding the studio floor."""
 bpy.context.view_layer.update();s=bpy.context.scene;cam=s.camera;inv=cam.matrix_world.inverted();points=[]
 for o in s.objects:
  if o.type in {'MESH','CURVE','SURFACE'} and o.name!='Studio floor' and not o.hide_render:
   points.extend(inv@(o.matrix_world@Vector(p))for p in o.bound_box)
 if not points:return
 low=[min(v[i]for v in points)for i in range(2)];high=[max(v[i]for v in points)for i in range(2)]
 center=Vector(((low[0]+high[0])/2,(low[1]+high[1])/2,0));cam.location+=cam.rotation_euler.to_quaternion()@center
 aspect=s.render.resolution_x/s.render.resolution_y;cam.data.ortho_scale=max(high[0]-low[0],(high[1]-low[1])*aspect)/(1-2*margin)
