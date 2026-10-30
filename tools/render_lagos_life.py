"""Ten distinct, inspectable Lagos scene studies. Run with Blender --python.
Optional names after -- select individual outputs. Fictional venues, no brand marks.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from lagos_scene_kit import *
if '--prepare' in sys.argv:
 from lagos_scene_kit import save as save_source
 def save(name):save_source(name,render=False)

def canteen():
 setup(10.7,target=(0,0,1.15));room(7,5,3.05)
 # Contemporary painted dado, stainless food service and a tiled splashback.
 box('Green painted dado',(0,2.414,.65),(6.98,.03,1.15),M['green'],.002)
 for x in [-2.7+i*.3 for i in range(19)]:
  for z in [1.1,1.4,1.7]:box('Splashback tile',(x,2.39,z),(.29,.025,.29),M['ceramic'],.002)
 box('Serving cabinet',(-.5,1.45,.56),(4.1,.8,.96),M['white'])
 box('Stainless counter',(-.5,1.43,1.075),(4.2,.91,.055),M['steel'])
 for x in [-1.9,-1.05,-.2,.65]:
  box('Steam tray',(x,1.4,1.115),(.67,.52,.045),M['steel'])
  box('Food in tray',(x,1.4,1.145),(.56,.42,.035),M['ochre' if x<0 else 'red'],.022)
 # Glass sneeze screen on slender poles, with a clear serving gap.
 for x in [-2.4,1.4]:rod('Screen support',(x,1.02,1.1),(x,1.02,1.62),.014,M['chrome'])
 box('Service screen',(-.5,1.02,1.48),(3.8,.012,.28),M['glass'],.002)
 for x in [-1.95,-.9,.15]:box('Counter panel seam',(x,1.038,.56),(.012,.014,.86),M['steel'],.002)
 box('Menu panel',(-1,2.36,2.4),(2.5,.055,.74),M['green'])
 label('LAGOS CANTEEN',(-2.12,2.32,2.57),.19,M['white']);label('Jollof rice   /   Beans   /   Stew',(-2.12,2.32,2.32),.105,M['white']);label('Order here  >',(-.8,1.006,.61),.12,M['green'])
 box('Undercounter fridge',(2.55,1.7,.65),(.8,.8,1.16),M['steel']);box('Fridge door',(2.55,1.27,.65),(.7,.04,1.04),M['glass'])
 for z in [.4,.7,.95]:
  for x in [2.35,2.55,2.75]:bottle(x,1.2,z,'green')
 for x,y in [(-1.6,-1.05),(.55,-1.05)]:
  table(x,y)
  chair(x,y-.66,math.pi);chair(x,y+.66)
  plate(x-.25,y,.8,True);plate(x+.25,y,.8,True);bottle(x+.43,y+.17,.8)
 person('Canteen attendant',-.5,2.0,pose='work',shirt='white',apron=True)
 person('Diner',-1.6,-1.64,math.pi,pose='sit',shirt='ochre')
 person('Diner',.55,-.45,pose='sit',shirt='cream')
 window(2.1,2.4,2.36,1.7,.75);clock(-2.8,2.35,2.55);fan(-3,2.31,1.8)
 plant(2.8,-1.7)
 box('Wash station',(-3.05,.15,.55),(.58,.8,.95),M['white']);bowl(-3.05,.15,1.04,.23,'steel',.07);line('Tap',[(-3.05,.4,1.1),(-3.05,.4,1.35),(-3.05,.18,1.35),(-3.05,.18,1.26)],.016,M['chrome'])
 save('lagos-canteen')

def barber_chair(x,y):
 cylinder('Hydraulic chair base',(x,y,.13),.37,.09,M['chrome'],48);cylinder('Hydraulic piston',(x,y,.32),.065,.35,M['chrome'])
 box('Barber seat',(x,y,.56),(.56,.52,.13),M['leather'],.05);box('Reclining back',(x,y+.24,.94),(.56,.14,.68),M['leather'],.05)
 box('Headrest',(x,y+.25,1.37),(.28,.12,.17),M['leather'],.04)
 for dx in [-.34,.34]:
  rod('Armrest rail',(x+dx,y-.18,.58),(x+dx,y+.16,.85),.022,M['chrome']);box('Padded armrest',(x+dx,y,.88),(.1,.45,.07),M['leather'],.025)
 line('Footrest rail',[(x-.2,y-.15,.45),(x-.2,y-.62,.22),(x+.2,y-.62,.22),(x+.2,y-.15,.45)],.018,M['chrome']);box('Footrest plate',(x,y-.56,.23),(.4,.22,.025),M['blackmetal'])

def barbershop():
 setup(9.5,camera=(8,-11,8),target=(0,0,1.15));room(6.1,4.8,3.05,floor='concrete')
 box('Navy rear feature wall',(0,2.31,1.55),(6.05,.04,2.95),M['navy'])
 for x in [-1.4,1.25]:
  box('Mirror frame',(x,2.23,1.9),(1.45,.11,1.65),M['blackmetal'])
  mirror=mat('Mirror',(.76,.8,.81),1,.035);box('Mirror glass',(x,2.16,1.9),(1.32,.025,1.52),mirror,.002)
  box('Work counter',(x,1.96,.98),(1.65,.53,.055),M['walnut']);box('Drawer cabinet',(x,2.02,.64),(1.4,.42,.62),M['walnut'])
  for dx in [-.35,.35]:box('Drawer handle',(x+dx,1.78,.69),(.19,.025,.018),M['chrome'],.004)
  for i in range(3):cylinder('Unbranded hair product',(x-.5+i*.14,1.9,1.1),.04,.2,M['white'],24)
  box('Hair clipper',(x+.3,1.82,1.037),(.065,.15,.037),M['blackmetal']);box('Clipper blade',(x+.3,1.74,1.04),(.06,.025,.017),M['steel'])
  for i in range(7):box('Comb tooth',(x+.47+i*.008,1.87,1.035),(.004,.075,.006),M['ink'],0)
  barber_chair(x,.2)
 person('Seated customer',-1.4,.2,pose='sit',shirt='white')
 person('Barber',-.82,.81,angle=-.25,pose='work',shirt='navy',apron=True)
 # Cutting cape fitted over torso/lap; retains visible clothed arms and shoes.
 box('Customer cutting cape',(-1.4,.10,1.08),(.48,.19,.42),M['cream'],.07)
 box('Waiting bench',(1,-1.78,.5),(2.35,.52,.1),M['walnut']);box('Bench back',(1,-1.53,.86),(2.35,.05,.62),M['walnut'])
 for x in [.1,1.9]:box('Bench legs',(x,-1.78,.26),(.055,.46,.47),M['blackmetal'])
 person('Waiting customer',1,-1.75,pose='sit',shirt='ochre')
 label('THE BARBER ROOM',(-1.2,2.14,2.88),.16,M['white']);clock(2.65,2.22,2.53)
 # Traditional pole is a trade cue, no copied shop identity.
 for i in range(12):cylinder('Barber pole stripe',(2.9,-.8,1.7+i*.055),.065,.05,M['red' if i%3==0 else 'blue' if i%3==1 else 'white'],32)
 cylinder('Pole cap',(2.9,-.8,2.38),.075,.07,M['chrome']);plant(-2.55,-1.7)
 save('lagos-barbershop')

def church():
 setup(12,camera=(11,-15,11),target=(0,.5,1.2));room(8,8,3.6,wall='plaster',floor='concrete')
 box('Raised sanctuary platform',(0,2.5,.24),(7.7,2.8,.32),M['oak']);box('Platform step',(0,.93,.12),(4.4,.55,.15),M['oak'])
 box('Pulpit stem',(0,2.4,.94),(.57,.44,1.13),M['walnut']);o=box('Pulpit top',(0,2.36,1.53),(.78,.62,.055),M['walnut']);o.rotation_euler[0]=.12
 box('Open book',(0,2.29,1.59),(.31,.22,.035),M['cream'],.004)
 box('Cross vertical',(0,3.88,2.55),(.12,.06,1.2),M['walnut']);box('Cross arms',(0,3.87,2.79),(.68,.065,.12),M['walnut'])
 for y in [-2.8,-1.7,-.6]:
  for x in [-2.2,2.2]:
   box('Upholstered pew seat',(x,y,.57),(2.6,.43,.1),M['blue'],.025);box('Pew back',(x,y+.2,.94),(2.6,.08,.61),M['walnut'])
   for dx in [-1.15,1.15]:box('Pew support',(x+dx,y,.31),(.09,.42,.48),M['walnut'])
 for x in [-3.45,3.45]:box('PA speaker',(x,2.7,1.55),(.44,.4,.8),M['ink'],.018);rod('Speaker stand',(x,2.7,.4),(x,2.7,1.15),.025,M['blackmetal'])
 rod('Microphone stand',(.9,2.1,.4),(.9,2.1,1.65),.012,M['chrome']);rod('Microphone boom',(.9,2.1,1.6),(.4,2.04,1.8),.01,M['blackmetal'])
 box('Keyboard',(2.55,2.6,1.13),(1.15,.32,.09),M['ink'])
 for i in range(28):box('Keyboard key',(2.03+i*.037,2.45,1.18),(.033,.18,.016),M['white'],.001)
 for a,b in [((2.05,2.5,.4),(3.05,2.7,1.1)),((3.05,2.5,.4),(2.05,2.7,1.1))]:rod('Keyboard X stand',a,b,.02,M['blackmetal'])
 for x in [-2.5,2.5]:window(x,3.91,2.6,1.25,1.3)
 fan(-3.4,3.85,2.8);fan(3.4,3.85,2.8);plant(-3.4,1.6);plant(3.4,1.6)
 label('COMMUNITY CHAPEL',(-1.2,3.87,3.33),.16,M['walnut'])
 save('lagos-church')

def produce(x,y,z,kind='tomato'):
 for i in range(12):
  xx=x+(i%4-.5)*.08;yy=y+(i//4-1)*.09
  if kind=='plantain':
   o=ellipsoid('Plantain', (xx,yy,z),(.12,.026,.027),M['ochre'],16,8);o.rotation_euler[2]=.35
  else:ellipsoid('Tomato' if kind=='tomato'else'Green pepper',(xx,yy,z),(.043,.04,.04),M['red' if kind=='tomato'else'leaf'],16,8)

def market():
 setup(12.9,camera=(12,-15,12),target=(0,0,1.0));box('Paved market plot',(0,0,-.02),(10,7.2,.14),M['concrete'])
 for x in [-3.2,0,3.2]:
  # Proper counter-height stalls with open circulation, not a miniature shanty.
  box('Market stall counter',(x,1.1,.9),(2.7,1,.055),M['oak']);box('Stall front',(x,.66,.48),(2.7,.04,.76),M['green'])
  for dx in [-1.4,1.4]:
   for dy in [.55,1.7]:rod('Stall steel post',(x+dx,dy,.06),(x+dx,dy,2.45),.025,M['blackmetal'])
  canopy=box('Pitched canopy',(x,1.1,2.5),(3,1.7,.045),M['cream']);canopy.rotation_euler[0]=.1
  box('Canopy fascia',(x,.27,2.37),(3,.035,.18),M['green']);label('FRESH PRODUCE',(x-.64,.244,2.37),.115,M['white'])
  for i,kind in enumerate(['tomato','pepper','plantain']):
   xx=x-.85+i*.8;box('Produce crate',(xx,1.05,1.01),(.7,.65,.19),M['oak'])
   for j in range(6):box('Crate slat',(xx-.32+j*.125,.707,1.05),(.07,.025,.2),M['walnut'],.003)
   produce(xx-.09,1.05,1.15,kind)
 person('Market seller',-3.2,1.6,shirt='ochre',apron=True,headwrap=True)
 person('Customer',.4,-.15,angle=math.pi,shirt='cream')
 person('Market seller',3.2,1.7,shirt='green')
 # Central aisle, crates and hand trolley parked outside walking line.
 for y in [-2,-1.4]:box('Stacked supply crate',(-4.4,y,.26),(.75,.5,.4),M['oak'])
 line('Hand trolley',[(-3.9,-2.8,.1),(-3.9,-2.5,1.3),(-3.9,-2.25,1.3)],.022,M['blackmetal'])
 for y in [-2.8,-2.4]:cylinder('Trolley wheel',(-3.9,y,.16),.14,.07,M['leather'],32,(0,math.pi/2,0))
 for x in [-3.9,3.9]:box('Market boundary bollard',(x,-3.05,.43),(.13,.13,.75),M['steel'])
 box('Rear boundary',(0,3.48,.65),(10,.14,1.2),M['plaster']);save('lagos-produce-market')

def football():
 setup(31,camera=(22,-29,25),target=(0,0,.5));box('Compact training pitch',(0,0,-.025),(26,18,.16),M['turf'])
 # Authored small-sided pitch, not advertised as regulation-sized.
 for x in [-12,12]:box('Touch line',(x,0,.064),(.065,16,.008),M['white'],0)
 for y in [-8,8]:box('Goal line',(0,y,.064),(24,.065,.008),M['white'],0)
 box('Halfway line',(0,0,.065),(24,.065,.008),M['white'],0)
 line('Centre circle',[(2.4*math.cos(a),2.4*math.sin(a),.07)for a in [i*math.tau/120 for i in range(121)]],.035,M['white'])
 for sy in [-1,1]:
  yy=sy*8
  for xx in [-2,2]:rod('Goal upright',(xx,yy,.07),(xx,yy,2.0),.045,M['white'])
  rod('Goal crossbar',(-2,yy,2),(2,yy,2),.045,M['white'])
  for xx in [-2,2]:line('Goal rear support',[(xx,yy,2),(xx,yy+sy*1.25,.07),(xx,yy,.07)],.03,M['steel'])
  for i in range(17):
   xx=-2+i*.25;line('Goal net strand',[(xx,yy,2),(xx,yy+sy*1.25,.07)],.006,M['cream'])
  for j in range(8):
   z=j*.25;dy=sy*1.25*(1-z/2);line('Goal net cross weave',[(-2,yy+dy,z+.07),(2,yy+dy,z+.07)],.006,M['cream'])
  line('Penalty area',[(-5,yy,.07),(-5,yy-sy*4,.07),(5,yy-sy*4,.07),(5,yy,.07)],.035,M['white'])
 # Mesh fence on the long sides and a small spectator bench.
 for side in [-1,1]:
  for yy in range(-9,10,3):rod('Boundary post',(side*13,yy,0),(side*13,yy,2.7),.035,M['blackmetal'])
  for z in [.4,.8,1.2,1.6,2,2.4]:rod('Fence wire',(side*13,-9,z),(side*13,9,z),.006,M['steel'])
 for y in [-3,0,3]:box('Sideline bench',(14,y,.52),(.5,2.5,.065),M['oak']);box('Bench base',(14,y,.26),(.4,.1,.5),M['blackmetal'])
 ellipsoid('Football',(0,-.4,.18),(.115,.115,.115),M['white'],32,16)
 for x in [-2,0,2]:
  bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.13,radius2=.035,depth=.22,location=(x,-5,.18));bpy.context.object.name='Training cone';bpy.context.object.data.materials.append(M['ochre'])
 save('lagos-football-field')

def school():
 setup(17.5,camera=(15,-19,13),target=(0,0,1.15));box('School courtyard',(0,-.5,-.03),(14,9,.18),M['concrete'])
 box('Classroom block',(0,1.85,1.65),(11,3.7,3.2),M['plaster']);box('Blue lower facade',(0,-.025,.55),(11,.045,1),M['blue'])
 box('Front verandah',(0,-.7,.16),(11.5,1.4,.2),M['concrete']);box('Verandah step',(0,-1.4,.06),(7,.4,.15),M['concrete'])
 for x in [-3.65,0,3.65]:
  box('Classroom door',(x,-.1,1.22),(.95,.07,2.2),M['green']);box('Door handle',(x+.32,-.15,1.15),(.1,.035,.035),M['steel'])
  label('CLASS '+str(int((x+3.65)/3.65)+1),(x-.35,-.15,2.58),.12,M['ink'])
 for x in [-2.25,-1.3,1.3,2.25,4.7,-4.7]:window(x,-.14,1.85,.8,1)
 for x in [-5.4,-1.8,1.8,5.4]:box('Verandah support',(x,-1.1,1.73),(.12,.12,3.2),M['white'])
 box('Roof sheet',(0,1.3,3.37),(11.8,5.2,.12),M['navy'])
 for x in [-5.8+i*.21 for i in range(56)]:box('Standing seam roof',(x,1.3,3.455),(.025,5.1,.025),M['steel'],.005)
 box('School sign',(0,-1.15,3.04),(4.9,.05,.38),M['navy']);label('LAGOS COMMUNITY SCHOOL',(-1.95,-1.19,3.06),.17,M['white'])
 rod('Flag mast',(-5,-3.3,.05),(-5,-3.3,4.7),.027,M['steel'])
 for i,m in enumerate(['green','white','green']):box('Nigerian flag panel',(-4.82+i*.28,-3.3,4.25),(.28,.015,.5),M[m],0)
 for x in [-3.5,3.5]:box('Courtyard bench',(x,-2.7,.55),(2.2,.48,.075),M['oak']);box('Bench support',(x,-2.7,.29),(.18,.4,.48),M['concrete'])
 for x in [-5.9,5.9]:plant(x,-1.8)
 save('lagos-school')

def classroom():
 setup(10.7,camera=(10,-13,10),target=(0,.2,1.1));room(7.3,6.3,3.05,floor='concrete')
 box('Painted lower wall',(0,3.06,.6),(7.25,.025,1.05),M['blue'],.002)
 box('Blackboard frame',(0,3.02,1.95),(3.8,.07,1.5),M['walnut']);box('Chalkboard',(0,2.97,1.95),(3.65,.025,1.35),M['green'])
 label('MATHEMATICS',(-1.57,2.94,2.38),.17,M['white']);label('Fractions   /   1/2 + 1/4 = 3/4',(-1.57,2.94,2.03),.135,M['white']);label('Practice:  2/3 + 1/6 = ?',(-1.57,2.94,1.73),.13,M['white'])
 box('Chalk ledge',(0,2.86,1.24),(3.8,.18,.035),M['walnut'])
 for y in [-2,-.65,.7]:
  for x in [-2.25,0,2.25]:
   table(x,y,1.25,.56,.73);chair(x-.3,y-.66,math.pi);chair(x+.3,y-.66,math.pi)
   for dx in [-.27,.27]:
    box('Exercise book',(x+dx,y,.773),(.22,.29,.018),M['cream'],.002);rod('Pencil',(x+dx+.12,y-.1,.79),(x+dx+.12,y+.09,.79),.003,M['ochre'])
 table(-2.45,2.08,1.2,.65,.8);chair(-2.45,2.7)
 box('Teacher register',(-2.45,2.05,.84),(.3,.24,.03),M['navy'])
 clock(2.7,3,2.51);fan(-2.8,2.98,2.5);window(2.65,3.03,1.65,1,.9)
 box('Notice board',(-3.55,.8,1.85),(.06,1.25,.92),M['oak'])
 save('lagos-classroom')

def suya():
 setup(7.3,camera=(7,-10,7),target=(0,0,1));box('Paved forecourt',(0,0,0),(5.5,4,.16),M['concrete']);box('Low boundary wall',(0,1.9,.8),(5.5,.12,1.5),M['plaster'])
 box('Steel grill body',(-.7,-.15,.76),(1.55,.68,.28),M['blackmetal'])
 for x in [-1.38,-.02]:
  for y in [-.4,.1]:rod('Grill legs',(x,y,.09),(x,y,.65),.023,M['blackmetal'])
 for i in range(11):rod('Grill grate bar',(-1.37+i*.135,-.48,.92),(-1.37+i*.135,.17,.92),.008,M['steel'])
 for i in range(10):
  x=-1.3+i*.13;rod('Bamboo skewer',(x,-.66,.96),(x,.15,.96),.004,M['oak'])
  for j in range(5):ellipsoid('Seasoned suya beef',(x,-.37+j*.093,.975),(.054,.046,.025),M['akara'],16,8)
 for i in range(16):ellipsoid('Charcoal lump',(-1.3+random.random()*1.2,-.38+random.random()*.45,.83),(.055,.045,.035),M['ink'],12,8)
 table(1.25,.1,1.3,.75,.9);box('Food wrapping paper',(1.25,.05,.934),(.65,.5,.004),M['cream'],0)
 bowl(1.58,.14,.94,.14,'steel',.1);bowl(.96,.15,.94,.1,'ceramic',.06)
 for i in range(10):ellipsoid('Cut tomato',(1.35+random.random()*.2,-.1+random.random()*.1,.96),(.035,.03,.018),M['red'],16,8)
 box('Spice tin',(1.02,.3,1.03),(.16,.16,.18),M['steel']);cylinder('Yaji spice',(1.02,.3,1.125),.062,.012,M['ochre'])
 person('Suya cook',-.7,.75,pose='work',shirt='white',apron=True)
 for x in [-2.3,2.3]:rod('Canopy upright',(x,1.45,.1),(x,1.45,2.8),.025,M['blackmetal'])
 box('Canopy',(0,.85,2.85),(5,2.2,.06),M['green']);box('Suya sign',(0,1.78,2.28),(2.5,.065,.45),M['green']);label('EVENING SUYA',(-.94,1.73,2.3),.18,M['white'])
 cylinder('Stool',(1.6,-1.3,.5),.22,.06,M['oak'])
 for a in [0,math.tau/3,2*math.tau/3]:rod('Stool leg',(1.6+.17*math.cos(a),-1.3+.17*math.sin(a),.1),(1.6+.12*math.cos(a),-1.3+.12*math.sin(a),.48),.018,M['blackmetal'])
 save('lagos-suya-spot')

def akara_piece(x,y,z,r=.043):
 o=ellipsoid('Akara / bean fritter',(x,y,z),(r*1.1,r,r*.83),M['akara'],20,12)
 # Slight irregularity; actual mesh detail, not a normal-map promise.
 for v in o.data.vertices:v.co*=1+random.uniform(-.065,.065)
 return o

def akara_vendor():
 setup(6.9,camera=(6,-8,6.1),target=(0,0,.95));box('Vendor pavement',(0,0,.015),(4.8,3.8,.17),M['concrete']);box('Rear wall',(0,1.8,.67),(4.8,.12,1.2),M['plaster'])
 table(.7,-.1,1.7,.75,.89);box('Serving tray',(.6,-.15,.95),(.85,.54,.045),M['steel'])
 for i in range(21):akara_piece(.29+(i%7)*.1,-.3+(i//7)*.13,1.005,.045)
 bowl(1.27,.03,.92,.23,'steel',.2);ellipsoid('Bean batter',(1.27,.03,1.09),(.195,.195,.026),M['cream'],32,12)
 rod('Ladle handle',(1.25,.0,1.12),(1.48,-.17,1.26),.008,M['oak']);bowl(1.24,.01,1.11,.045,'steel',.018)
 # Burner, frying pan and oil surface. No flame/fire simulation claim.
 cylinder('Gas burner',(-1.05,-.1,.37),.26,.54,M['blackmetal']);bowl(-1.05,-.1,.66,.36,'steel',.13)
 cylinder('Cooking oil',(-1.05,-.1,.746),.315,.008,M['ochre'],48)
 for i in range(7):a=i*math.tau/7;akara_piece(-1.05+.21*math.cos(a),-.1+.21*math.sin(a),.78,.042)
 rod('Pan handle',(-.76,-.1,.77),(-.42,-.1,.8),.025,M['blackmetal'])
 person('Akara vendor',-.1,.75,angle=.14,pose='work',shirt='cream',apron=True,headwrap=True)
 box('Paper serving bags',(1.24,-.3,1.07),(.2,.17,.2),M['cream']);bowl(.02,-.17,.94,.12,'ceramic',.08)
 for x in [-2,2]:rod('Umbrella awning frame',(x,1.5,.1),(x,1.5,2.6),.023,M['blackmetal'])
 box('Vendor sunshade',(0,1.0,2.63),(4.4,1.65,.045),M['cream']);box('Vendor sign',(0,1.69,1.94),(2.15,.05,.42),M['green']);label('AKARA  /  BREAKFAST',(-.94,1.65,1.96),.145,M['white'])
 save('lagos-akara-vendor')

def akara_food():
 setup(2.65,camera=(3,-4,3.8),target=(0,0,.18));box('Breakfast tabletop',(0,0,.035),(2.1,1.6,.08),M['oak'])
 bowl(-.31,-.05,.08,.37,'ceramic',.04)
 for i in range(12):
  a=i*2.4;r=.21*math.sqrt((i+.5)/12);akara_piece(-.31+r*math.cos(a),-.05+r*math.sin(a),.17+(i%3)*.014,.073)
 bowl(.49,.22,.09,.22,'ceramic',.19);cylinder('Pap / breakfast serving',(.49,.22,.25),.196,.018,M['cream'],48)
 rod('Spoon handle',(.5,.1,.29),(.72,-.13,.3),.008,M['steel']);ellipsoid('Spoon bowl',(.49,.11,.29),(.035,.052,.006),M['steel'],24,12)
 box('Folded napkin',(.48,-.39,.105),(.4,.29,.025),M['fabric'],.008)
 for i in range(3):
  o=box('Bread slice',(-.54+i*.11,.54,.15),(.1,.25,.12),M['cream'],.025);o.rotation_euler[2]=-.12
 save('akara-breakfast-pack')

SCENES={'lagos-canteen':canteen,'lagos-barbershop':barbershop,'lagos-church':church,'lagos-produce-market':market,'lagos-football-field':football,'lagos-school':school,'lagos-classroom':classroom,'lagos-suya-spot':suya,'lagos-akara-vendor':akara_vendor,'akara-breakfast-pack':akara_food}
args=sys.argv[sys.argv.index('--')+1:]if'--'in sys.argv else list(SCENES)
args=[a for a in args if a!='--prepare']
for name in args:SCENES[name]()
