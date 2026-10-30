"""Ten distinct original scene/prop/material studies for the portfolio catalogue."""
import sys,os,math,random
sys.path.insert(0,os.path.dirname(__file__))
from render_base import *
random.seed(18)

def setup(bg=(.10,.115,.13),cam=(5,-7,4.4),target=(0,0,1.1),size=4.8):
 s=reset(bg,camera=cam,target=target,ortho=size);s.cycles.samples=28
 # Neutral product lighting and moderate roughness rather than glossy toy surfaces.
 for o in bpy.data.objects:
  if o.type=='LIGHT':o.data.color=(1,.94,.86) if o.location.x>0 else (.8,.88,1)
 return s

def lathe(name,profile,m,segments=96):
 verts=[];faces=[]
 for r,z in profile:
  for j in range(segments):a=2*math.pi*j/segments;verts.append((r*math.cos(a),r*math.sin(a),z))
 for i in range(len(profile)-1):
  for j in range(segments):a=i*segments+j;b=i*segments+(j+1)%segments;faces.append((a,b,b+segments,a+segments))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(m)
 for p in me.polygons:p.use_smooth=True
 return o

def grain(m,scale=55,strength=.18,distance=.025):
 n=m.node_tree.nodes;l=m.node_tree.links;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=strength;b.inputs['Distance'].default_value=distance;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])

# 01 / Lagos kiosk: steel frame, shutter, awning, counter and unbranded produce crates.
setup((.13,.15,.15),cam=(7,-9,6),target=(0,0,1.05),size=6.8)
steel=mat('Weathered teal sheet',(.055,.18,.17),.55,.5);timber=mat('Oiled timber',(.25,.13,.055),rough=.58);dark=mat('Dark frame',(.035,.04,.04),.65,.35);canvas=mat('Awning canvas',(.55,.33,.10),rough=.82);grain(timber)
cube('Kiosk plinth',(0,0,.05),(3.2,2.35,.18),mat('Concrete',(.28,.29,.28),rough=.9),.025)
cube('Kiosk rear',(0,.84,1.25),(2.8,.12,2.4),steel,.015)
for x in (-1.35,1.35):cube('Kiosk side',(x,0,1.25),(.12,1.8,2.4),steel,.015)
for x in [-1.3+i*.15 for i in range(18)]:cube('Corrugation',(x,.754,1.25),(.023,.035,2.35),steel,.006)
cube('Service counter',(0,-.95,1.1),(3,.55,.1),timber,.025)
cube('Front skirt',(0,-.8,.57),(2.7,.1,1.0),steel,.015)
cube('Roof sheet',(0,0,2.5),(3.2,2.15,.1),dark,.015)
awning=cube('Fabric canopy',(0,-1.02,2.23),(3.2,1.15,.055),canvas,.02);awning.rotation_euler[0]=.15
for x in (-1.48,1.48):tube('Canopy support',[(x,-1.5,.1),(x,-1.5,2.25),(x,-.5,2.4)],.025,dark)
for x in (-.75,.1,.87):
 cube('Display crate',(x,-.93,1.28),(.68,.43,.25),timber,.015)
 for j in range(5):sphere('Produce',(x-.24+j*.11,-.94,1.48),(.067,.065,.066),mat('Produce'+str(x)+str(j),(.35+.04*j,.17,.045),rough=.55))
save('lagos-kiosk')

# 02 / Djembe: turned wood, a membrane, rings and individually modelled tension cords.
setup((.13,.105,.075),size=4.4)
wood=mat('Dark carved wood',(.17,.065,.023),rough=.42);grain(wood,14,.3,.03);rope=mat('Natural rope',(.43,.32,.18),rough=.8);skin=mat('Drum skin',(.65,.52,.33),rough=.72)
lathe('Goblet drum body',[(.36,.08),(.42,.15),(.28,.4),(.24,.85),(.41,1.25),(.67,1.65),(.69,1.82)],wood)
for z,r in [(1.72,.69),(1.84,.71),(.95,.29)]:
 tube('Rope ring',[(r*math.cos(a),r*math.sin(a),z) for a in [j*2*math.pi/128 for j in range(129)]],.025,rope)
cyl('Drum head',(0,0,1.845),.67,.025,skin)
for j in range(28):
 a=j*2*math.pi/28;tube('Tension cord',[(.69*math.cos(a),.69*math.sin(a),1.8),(.30*math.cos(a+.05),.30*math.sin(a+.05),1.0),(.69*math.cos(a+.12),.69*math.sin(a+.12),1.8)],.012,rope)
save('djembe-drum')

# 03 / Three open calabash-form vessels with actual inner and outer surfaces.
setup((.16,.13,.09),cam=(5,-7,5.8),target=(0,0,.45),size=4.8)
gourd=mat('Dry calabash',(.41,.22,.065),rough=.6);grain(gourd,24,.22,.018)
for i,(x,y,scale) in enumerate([(-.8,.25,.93),(.75,.35,.75),(0,-.8,.56)]):
 profile=[]
 for j in range(33):a=j*math.pi/2/32;profile.append((.9*math.sin(a),.12+.7*(1-math.cos(a))))
 for j in reversed(range(33)):
  a=j*math.pi/2/32;profile.append((max(.015,(.9-.035)*math.sin(a)),.155+.7*(1-math.cos(a))))
 o=lathe('Calabash bowl '+str(i+1),profile,gourd);o.location=(x,y,0);o.scale=(scale,scale,scale)
save('calabash-bowls')

# 04 / Original coastal timber doorway study. No historic pattern/calligraphy copied.
setup((.12,.14,.15),cam=(5,-8,4.5),target=(0,0,1.5),size=5.1)
wood=mat('Coastal hardwood',(.16,.075,.029),rough=.48);grain(wood,22,.25,.025);brass=mat('Aged brass',(.46,.29,.085),.75,.38);plaster=mat('Limewash',(.59,.59,.52),rough=.9)
cube('Door surround',(0,.18,1.65),(2.6,.3,3.3),plaster,.035)
for x in (-1.02,1.02):cube('Carved jamb',(x,-.02,1.55),(.2,.28,3.05),wood,.018)
cube('Lintel',(0,-.02,3.0),(2.24,.29,.26),wood,.025)
for x in (-.47,.47):
 cube('Door leaf',(x,-.02,1.52),(.9,.15,2.8),wood,.015)
 for z in (.55,1.35,2.15):
  cube('Recessed door panel',(x,-.12,z),(.67,.05,.56),mat('Panel grain'+str(x)+str(z),(.115,.05,.019),rough=.45),.014)
  for dx in (-.31,.31):cube('Panel beading',(x+dx,-.16,z),(.025,.035,.58),wood,.005)
 for z in (.4,.8,1.2,1.6,2.0,2.4):sphere('Brass fitting',(x-.24,-.17,z),(.035,.022,.035),brass)
for x in (-.14,.14):
 tube('Ring handle',[(x+.065*math.cos(a),-.205,1.48+.065*math.sin(a)) for a in [j*2*math.pi/32 for j in range(33)]],.009,brass)
for x in [-.87+i*.145 for i in range(13)]:
 o=cube('Original geometric lintel detail',(x,-.183,2.99),(.06,.025,.06),wood,.006);o.rotation_euler[1]=math.pi/4
cube('Stone threshold',(0,-.35,.05),(2.55,.8,.13),plaster,.025)
save('coastal-door')

def fabric(name,palette,setup_color):
 setup(setup_color,cam=(4,-7,5.5),target=(0,0,.5),size=4.8)
 m=mat(name,palette[0],rough=.85);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Generated'],sep.inputs['Vector'])
 mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=20;l.new(sep.outputs['X'],mul.inputs[0])
 ping=n.new('ShaderNodeMath');ping.operation='PINGPONG';ping.inputs[1].default_value=1;l.new(mul.outputs[0],ping.inputs[0])
 ramp=n.new('ShaderNodeValToRGB');r=ramp.color_ramp;r.interpolation='CONSTANT';r.elements[0].color=(*palette[0],1);r.elements[1].color=(*palette[-1],1)
 for i,c in enumerate(palette[1:-1]):r.elements.new((i+1)/(len(palette)-1)).color=(*c,1)
 l.new(ping.outputs[0],ramp.inputs['Fac']);l.new(ramp.outputs[0],p.inputs['Base Color']);grain(m,220,.5,.014)
 verts=[];faces=[];nx=80;ny=60
 for j in range(ny):
  for i in range(nx):
   x=(i/(nx-1)-.5)*3.1;y=(j/(ny-1)-.5)*2.45;z=.26+.15*math.sin(x*5)*(.35+.5*j/ny)+.09*math.cos(y*4)
   verts.append((x,y,z))
 for j in range(ny-1):
  for i in range(nx-1):a=j*nx+i;faces.append((a,a+1,a+1+nx,a+nx))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(m);o.modifiers.new('Fabric edge','SOLIDIFY').thickness=.018
 for p in me.polygons:p.use_smooth=True
 return o,m

# 05 / New strip-weave colour composition rather than a copied traditional motif.
fabric('Kente-inspired strip study',[(.46,.22,.018),(.035,.14,.065),(.12,.025,.025),(.7,.43,.04),(.035,.04,.045)],(.12,.11,.09));save('kente-strip-study')

# 06 / Natural-fibre mat, with a bound edge and visible woven relief.
o,m=fabric('Natural fibre weave',[(.28,.18,.065),(.45,.32,.14),(.61,.47,.25),(.39,.25,.095)],(.12,.14,.12))
for x in (-1.55,1.55):tube('Bound textile edge',[(x,-1.22+j*.061,.26+.15*math.sin(x*5)*(.35+.5*j/40)+.09*math.cos((-1.22+j*.061)*4))for j in range(41)],.022,m)
save('woven-mat')

# 07 / Stylised botanical study with a broad trunk, tapering branches and bark relief.
setup((.12,.14,.12),cam=(7,-10,5.7),target=(0,0,2.1),size=7.2)
bark=mat('Baobab bark',(.26,.22,.16),rough=.85);grain(bark,18,.55,.08)
lathe('Swollen trunk',[(.75,.08),(.94,.35),(.81,1.2),(.65,2.2),(.53,2.9),(.35,3.35)],bark)
for j in range(8):
 a=2*math.pi*j/8;start=Vector((.28*math.cos(a),.28*math.sin(a),2.6+.1*(j%3)));end=Vector((2.0*math.cos(a),2.0*math.sin(a),3.65+.4*(j%2)))
 # Tapered curved branches from a series of variable-radius rings.
 d=end-start;length=d.length;bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.32,radius2=.07,depth=length,location=(start+end)/2);b=bpy.context.object;b.rotation_euler=d.to_track_quat('Z','Y').to_euler();b.data.materials.append(bark)
 for k in (-1,1):
  tip=end+Vector((.55*math.cos(a+k*.8),.55*math.sin(a+k*.8),.6));tube('Outer branch',[end,tip],.055,bark)
save('baobab-study')

# 08 / Kenyan jiko-inspired metal stove study, with a lined chamber and air door.
setup((.105,.12,.14),cam=(5,-7,5.2),target=(0,0,.75),size=3.8)
steel=mat('Dark stove steel',(.065,.075,.08),.7,.45);clay=mat('Clay liner',(.37,.19,.085),rough=.9);rust=mat('Worn metal',(.18,.105,.045),.55,.6)
lathe('Cylindrical stove shell',[(.52,.25),(.52,1.18),(.48,1.22),(.41,1.18),(.41,.32)],steel)
lathe('Clay-lined chamber',[(.405,.4),(.405,1.17),(.35,1.17),(.35,.45)],clay)
cyl('Charcoal grate',(0,0,.65),.35,.035,steel)
for x in [-.25+i*.10 for i in range(6)]:cube('Grate slots',(x,-.0,.68),(.025,.55,.014),rust,.004)
cube('Air door',(0,-.525,.49),(.33,.025,.25),rust,.012);cube('Door pull',(0,-.565,.5),(.09,.06,.025),steel,.009)
for j in range(3):
 a=j*2*math.pi/3;x=.45*math.cos(a);y=.45*math.sin(a);cube('Stove foot',(x,y,.16),(.10,.10,.25),steel,.015);o=cube('Pot rest',(x,y,1.22),(.27,.08,.06),steel,.01);o.rotation_euler[2]=a
tube('Wire carry handle',[(-.5,0,.75),(-.67,0,1.55),(.67,0,1.55),(.5,0,.75)],.018,steel)
save('jiko-stove')

# 09 / Timber market handcart: boards, tyre treads, axle and towing arms.
setup((.10,.135,.14),cam=(6,-8,5),target=(0,0,.85),size=5.8)
wood=mat('Cart timber',(.26,.15,.065),rough=.65);grain(wood,15,.35,.025);metal=mat('Galvanised fittings',(.15,.17,.16),.7,.48);rubber=mat('Tyre rubber',(.02,.024,.026),rough=.8)
for i in range(7):cube('Bed plank',(-.9+i*.30,0,.72),(.285,2.1,.075),wood,.01)
for x in (-1.02,1.02):
 for z in (.9,1.15,1.4):cube('Side board',(x,0,z),(.065,2.2,.18),wood,.008)
 for y in (-.95,.95):cube('Corner post',(x,y,1.1),(.08,.08,.9),metal,.008)
for y in (-1.05,1.05):
 for z in (.9,1.15,1.4):cube('End board',(0,y,z),(2.0,.065,.18),wood,.008)
cyl('Axle',(0,0,.5),.055,2.7,metal,(0,math.pi/2,0))
for x in (-1.23,1.23):
 cyl('Cart wheel',(x,0,.5),.47,.17,rubber,(0,math.pi/2,0));cyl('Wheel hub',(x+(.1 if x>0 else -.1),0,.5),.23,.02,metal,(0,math.pi/2,0))
for x in (-.65,.65):tube('Tow arm',[(x,-.8,.67),(x,-2.1,.8),(x,-2.5,1.0)],.04,metal)
save('market-handcart')

# 10 / Original earthenware storage vessel, with wall thickness and a removable lid.
setup((.15,.115,.09),cam=(5,-7,4.5),target=(0,0,.95),size=4.4)
clay=mat('Fired red clay',(.39,.145,.065),rough=.72);grain(clay,60,.35,.018)
lathe('Earthenware jar',[(.32,.05),(.49,.14),(.71,.48),(.77,.9),(.62,1.28),(.36,1.5),(.33,1.65),(.29,1.65),(.32,1.49),(.57,1.25),(.71,.9),(.65,.5),(.43,.17)],clay)
lathe('Lid',[(.0,1.68),(.39,1.68),(.34,1.75),(.12,1.8),(.08,1.9),(.0,1.92)],clay)
for j in range(5):
 z=.84+j*.045;r=.775;tube('Wheel-thrown line',[(r*math.cos(a),r*math.sin(a),z) for a in [k*2*math.pi/128 for k in range(129)]],.004,clay)
save('earthenware-jar')
