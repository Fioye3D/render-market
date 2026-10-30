"""Original digital interpretations for the West African starter collection.
Not scans, authenticated heritage reproductions, or production-ready products.
"""
import os,sys,math
sys.path.insert(0,os.path.dirname(__file__))
from render_base import *

reset((.21,.135,.09),camera=(7,-9,7),target=(0,0,1.0),ortho=7.6)
earth=mat('Ochre earth',(.49,.24,.105),rough=.82);plaster=mat('Sand plaster',(.66,.44,.25),rough=.8);timber=mat('Dark timber',(.10,.055,.025));indigo=mat('Indigo cloth',(.035,.06,.14),rough=.8)
cube('Courtyard base',(0,0,0),(4.8,4.0,.25),plaster,.1)
cube('Main earthen volume',(0,.85,1.35),(3.7,1.15,2.6),earth,.12)
cube('Side volume',(1.55,-.4,.78),(.75,2.3,1.5),earth,.12)
# Applied recessed-looking doorway and shutters; this is an original architectural study.
cube('Door recess',(-.55,.245,.85),(.9,.04,1.6),timber,.17)
for x in (-1.45,.5,1.45):
 cube('Buttress',(x,.13,1.38),(.28,.4,2.7),earth,.07)
for x in [-1.6+i*.4 for i in range(9)]:
 cube('Parapet cap',(x,.82,2.82),(.20,1.06,.4),earth,.05)
for x in (-1.1,.9):
 cube('Window recess',(x,.24,1.99),(.48,.04,.5),timber,.04)
 for dx in (-.13,0,.13):cube('Window grille',(x+dx,.20,1.99),(.025,.03,.43),plaster,.005)
for x in [-1.45+i*.48 for i in range(7)]:cube('Timber beam',(x,.2,2.5),(.065,.8,.07),timber,.01)
cube('Seating plinth',(.2,-1.05,.36),(1.45,.65,.45),earth,.1)
cube('Indigo seat',(.2,-1.05,.64),(1.33,.58,.16),indigo,.07)
cyl('Storage jar',(-1.4,-.55,.44),.23,.63,plaster)
sphere('Rounded jar shoulder',(-1.4,-.55,.62),(.25,.25,.22),plaster)
cyl('Jar mouth',(-1.4,-.55,.85),.11,.10,timber)
save('sahel-courtyard')

reset((.12,.17,.17),camera=(6,-8,4.7),target=(0,0,1.0),ortho=6.2)
yellow=mat('Lagos yellow',(.91,.48,.035),.1,.3);black=mat('Tyres and stripes',(.018,.022,.026),rough=.5);glass=mat('Smoked window glass',(.045,.095,.105),.35,.19);silver=mat('Wheel metal',(.34,.38,.39),.7,.25);white=mat('Headlight lenses',(.88,.86,.70),.2,.15)
cube('Minibus body',(0,0,1.10),(3.8,1.55,1.35),yellow,.19)
cube('Upper body',(0,0,1.93),(3.5,1.5,.65),yellow,.17)
cube('Front windscreen',(-1.765,0,1.90),(.055,1.25,.52),glass,.055)
cube('Rear window',(1.765,0,1.92),(.05,1.2,.48),glass,.04)
for side in (-1,1):
 for x in (-1.28,-.38,.52,1.3):cube('Side window',(x,side*.766,1.93),(.7,.045,.48),glass,.035)
 for z in (1.38,1.24):cube('Black side stripe',(0,side*.791,z),(3.65,.025,.055),black,.005)
 for x in (-1.15,1.15):
  cyl('Tyre',(x,side*.78,.55),.43,.22,black,(math.pi/2,0,0));cyl('Wheel hub',(x,side*.905,.55),.23,.03,silver,(math.pi/2,0,0))
 cube('Door handle',(.1,side*.8,1.58),(.19,.04,.045),black,.01)
cube('Front bumper',(-1.96,0,.82),(.15,1.6,.18),black,.05)
cube('Rear bumper',(1.96,0,.82),(.15,1.6,.18),black,.05)
for y in (-.5,.5):cube('Headlight',(-1.983,y,1.15),(.04,.32,.20),white,.04)
for z in (1.08,1.18,1.28):cube('Front grille',(-1.99,0,z),(.03,.42,.035),black,.005)
save('danfo-minibus')

reset((.16,.13,.095),camera=(5,-7,5),target=(0,0,.95),ortho=4.9)
straw=mat('Golden grass',(.56,.31,.095),rough=.7);dark=mat('Dyed indigo grass',(.045,.08,.13),rough=.72);leather=mat('Handle wrap',(.15,.065,.025),rough=.7)
# Open basket: densely spaced rising spirals plus vertical warp strands.
for row in range(52):
 z=.12+row*.023;r=.65+.38*(z/1.32)
 points=[(r*math.cos(a),r*math.sin(a),z+.005*math.sin(36*a)) for a in [2*math.pi*j/192 for j in range(193)]]
 tube('Woven coil',points,.018,dark if row in range(13,18) or row in range(36,41) else straw)
for j in range(88):
 a=j*2*math.pi/88
 points=[]
 for i in range(40):
  z=.12+i*.031;r=.65+.38*(z/1.32)+.012*math.sin(i*math.pi)
  points.append((r*math.cos(a),r*math.sin(a),z))
 tube('Warp strand',points,.009,straw)
cyl('Woven base',(0,0,.12),.65,.035,straw)
for k in range(3):
 points=[((1.0+k*.016)*math.cos(a),0,1.29+1.0*math.sin(a)) for a in [math.pi*j/64 for j in range(65)]]
 tube('Wrapped handle',points,.025,leather)
save('bolga-basket')

reset((.08,.095,.15),camera=(4,-7,4.2),target=(0,0,1.0),ortho=4.8)
cloth=mat('Aso oke inspired stripe interpretation',(.1,.14,.28),rough=.85)
n=cloth.node_tree.nodes;l=cloth.node_tree.links;p=n.get('Principled BSDF')
tc=n.new('ShaderNodeTexCoord');wave=n.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='X';wave.inputs['Scale'].default_value=4
l.new(tc.outputs['Generated'],wave.inputs['Vector'])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT';r=ramp.color_ramp
r.elements.remove(r.elements[1]);r.elements[0].position=0;r.elements[0].color=(.025,.04,.10,1)
for pos,col in [(.12,(.68,.50,.23,1)),(.2,(.035,.06,.14,1)),(.32,(.78,.72,.55,1)),(.38,(.035,.06,.14,1)),(.72,(.2,.09,.13,1)),(.80,(.68,.50,.23,1)),(.85,(.035,.06,.14,1))]:r.elements.new(pos).color=col
l.new(wave.outputs['Color'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],p.inputs['Base Color'])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=180
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.4;bump.inputs['Distance'].default_value=.025
l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal'])
# Draped strip surface, not a flat decorative pattern.
verts=[];faces=[];nx=72;ny=60
for j in range(ny):
 for i in range(nx):
  x=(i/(nx-1)-.5)*3.15;y=(j/(ny-1)-.5)*2.5;z=.68+.18*math.sin(x*5)+.08*math.cos(y*5)+.1*y
  verts.append((x,y,z))
for j in range(ny-1):
 for i in range(nx-1):a=j*nx+i;faces.append((a,a+1,a+1+nx,a+nx))
mesh=bpy.data.meshes.new('Draped fabric mesh');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Woven stripe material study',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(cloth)
for poly in mesh.polygons:poly.use_smooth=True
o.modifiers.new('Fabric thickness','SOLIDIFY').thickness=.014
save('aso-oke-stripes')

reset((.15,.105,.075),camera=(5,-7,4.3),target=(0,0,1.1),ortho=4.7)
wood=mat('Carved wood',(.26,.095,.025),rough=.48);skin=mat('Drum membrane',(.72,.56,.31),rough=.8);rope=mat('Tension cord',(.54,.37,.17),rough=.7)
# Lathed hourglass body with two membranes and longitudinal tension cords.
profile=[(.0,.55),(.15,.53),(.42,.38),(.72,.25),(.98,.27),(1.25,.4),(1.5,.54),(1.63,.56)]
verts=[];faces=[];segments=72
for z,r in profile:
 for j in range(segments):a=2*math.pi*j/segments;verts.append((r*math.cos(a),r*math.sin(a),z+.22))
for i in range(len(profile)-1):
 for j in range(segments):a=i*segments+j;b=i*segments+(j+1)%segments;faces.append((a,b,b+segments,a+segments))
mesh=bpy.data.meshes.new('Hourglass drum mesh');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Gangan body study',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(wood)
for p in mesh.polygons:p.use_smooth=True
for z in (.23,1.85):cyl('Tension hoop',(0,0,z),.59,.07,rope);cyl('Membrane',(0,0,z+.04),.54,.028,skin)
for j in range(22):
 a=j*2*math.pi/22
 tube('Tension thong',[(.57*math.cos(a),.57*math.sin(a),.27),(.37*math.cos(a+.04),.37*math.sin(a+.04),1.03),(.57*math.cos(a),.57*math.sin(a),1.85)],.014,rope)
tube('Curved beater',[(1.0,0,.1),(1.03,0,.6),(1.1,0,.9),(1.30,0,1.04),(1.45,0,1.01)],.035,wood)
save('gangan-drum')
