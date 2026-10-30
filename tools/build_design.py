"""Shared editable scene source -> SVG artboards, web prototype data, Figma payload."""
from pathlib import Path
import json, html, base64, copy, math
from PIL import ImageFont
from functools import lru_cache

ROOT=Path(__file__).resolve().parents[1]
for d in ['design/screens','design/wireframes','design/figma-plugin','assets/screenshots','assets/logo','docs','research','prototype']:(ROOT/d).mkdir(parents=True,exist_ok=True)
BG='#101112'; SUR='#191B1E'; PANEL='#202327'; LINE='#3D424A'; INK='#F5F3EE'; MUT='#B2B7C1'; ACC='#285c82'; ACTION='#285c82'; SOFT='#c4ccd3'; GREEN='#bec8c2'
SCENES=[]; current=None

def frame(id,title,w=1440,h=1120,page='High fidelity'):
 global current
 current={'id':id,'title':title,'width':w,'height':h,'page':page,'background':BG,'nodes':[],'hotspots':[]};SCENES.append(current);return current
def rect(x,y,w,h,fill=SUR,r=0,stroke=None,name='Surface'):
 r=0
 n=dict(type='rect',x=x,y=y,w=w,h=h,fill=fill,r=r,name=name)
 if stroke:n['stroke']=stroke
 current['nodes'].append(n);return n
@lru_cache(maxsize=64)
def measure_font(family,size):return ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',size)

def wrap_text(s,width,size):
 font=measure_font('Arial' if size>=24 else 'Arial',size);lines=[];line=''
 for word in s.split():
  proposed=(line+' '+word).strip()
  if line and font.getlength(proposed)>width:lines.append(line);line=word
  else:line=proposed
 if line:lines.append(line)
 return '\n'.join(lines)

def txt(x,y,s,size=16,color=INK,weight=400,w=None,name=None):
 n=dict(type='text',x=x,y=y,text=s,size=size,color=color,weight=weight,name=name or s[:52],font='Arial' if size>=24 else 'Arial')
 if w:n['w']=w;n['text']=wrap_text(s,w,size)
 current['nodes'].append(n);return n
def line(x,y,w):rect(x,y,w,1,LINE,name='Divider')
def art(x,y,w,h,file,r=12):current['nodes'].append(dict(type='image',x=x,y=y,w=w,h=h,file=file,r=0,name=file.replace('-',' ')+' / original procedural preview'))
def hot(x,y,w,h,label,to=None,action=None):
 n=dict(x=x,y=y,w=w,h=h,label=label)
 if to:n['to']=to
 if action:n['action']=action
 current['hotspots'].append(n)
def button(x,y,w,label,to=None,kind='primary',action=None):
 start=len(current['nodes']);rect(x,y,w,48,ACTION if kind=='primary' else SUR,8,LINE if kind!='primary' else None,'Button / '+kind)
 txt(x+18,y+14,label,14,INK,600)
 current['nodes'][start]['component']='Button/'+kind
 hot(x,y,w,48,label,to,action)
def link(x,y,label,to,w=130):txt(x,y,label,14,MUT,500);hot(x,y-10,w,44,label,to)
def pill(x,y,label,selected=False,w=None):
 w=w or 24+len(label)*7
 rect(x,y,w,32,'#26333d' if selected else SUR,16,SOFT if selected else LINE)
 txt(x+12,y+9,label,12,SOFT if selected else MUT,500);return w
def inputbox(x,y,w,label,value='',placeholder='',key=None,h=52):
 txt(x,y,label,14,INK,500);rect(x,y+27,w,h,BG,8,LINE,'Input / '+label)
 txt(x+16,y+44,value or placeholder,14,INK if value else MUT)
 if key:current.setdefault('inputs',[]).append(dict(x=x+2,y=y+29,w=w-4,h=h-4,label=label,value=value,placeholder=placeholder,key=key,multiline=h>60))
def mark(x,y,s=28,color=SOFT):
 # A deliberately simple folded R: vertical stem, bowl and open diagonal leg.
 current['nodes'].append(dict(type='vector',x=x,y=y,w=s,h=s,path='M 0 28 L 0 0 L 18 0 L 28 10 L 18 20 L 28 28 L 17 28 L 7 18 L 7 28 Z M 7 7 L 7 13 L 16 13 L 20 10 L 16 7 Z',fill=color,name='RenderMarket / Fold R'))
def nav(active='Explore'):
 rect(0,0,1440,88,BG);mark(48,29);txt(88,30,'RenderMarket',23,INK,600)
 for x,label,to in [(345,'Explore','explore'),(449,'Creators','creator'),(560,'How it works','about')]:
  txt(x,37,label,14,INK if active==label else MUT,500);hot(x-5,20,100,48,label,to)
 if active=='Explore':rect(345,83,48,3,ACC)
 rect(685,22,278,44,SUR,8,LINE,'Navigation / search')
 txt(700,37,'Search African assets…',12,MUT)
 current.setdefault('inputs',[]).append(dict(x=687,y=24,w=274,h=40,label='Search marketplace',value='',placeholder='Search African assets…',key='search',multiline=False))
 link(1005,37,'Saved assets','saved',116);button(1152,20,184,'Creator studio  ↗','dashboard','secondary')
 line(48,87,1344)
def foot(y):
 line(48,y,1344);txt(48,y+28,'RenderMarket',18,INK,600)
 txt(245,y+32,'Independent portfolio · Sample prices · No transactions',12,MUT)
 txt(1115,y+32,'Created October 2026',12,MUT)
def eyebrow(x,y,s):txt(x,y,s.upper(),11,SOFT,600)
def heading(x,y,s,sub=None):
 txt(x,y,s,36,INK,500)
 if sub:txt(x,y+55,sub,15,MUT)

ASSETS=[
 dict(id='terra',title='Courtyard / Earthen scene kit',creator='Nia Forms',file='sahel-courtyard',cat='Environments',formats='BLEND',price=24000,tag='Sahel-inspired architecture',context='Original earthen courtyard study. Not a reconstruction of a heritage site.',region='Mali / architectural reference',desc='An original earthen courtyard study referencing the materiality of Sahelian architecture.'),
 dict(id='orbit',title='Danfo / Lagos minibus',creator='Dayo Objects',file='danfo-minibus',cat='3D models',formats='BLEND',price=12000,tag='Lagos, Nigeria / urban life',context='A stylised digital interpretation of a Lagos danfo. No vehicle-brand affiliation.',region='Nigeria / Lagos',desc='A stylised yellow minibus for a contemporary Lagos street scene. No manufacturer marks.'),
 dict(id='loop',title='Bolga / Market basket',creator='Nia Forms',file='bolga-basket',cat='3D models',formats='BLEND',price=8500,tag='Bolgatanga, Ghana / basketry',context='Digital basket study informed by Bolgatanga basketry. Not an artisan-made physical basket.',region='Ghana / Bolgatanga',desc='An original woven basket study informed by basketry from Bolgatanga, Ghana.'),
 dict(id='kora',title='Aso oke / Stripe study',creator='Sefi Materials',file='aso-oke-stripes',cat='Materials',formats='BLEND',price=6000,tag='Yoruba, Nigeria / textile study',context='Procedural stripe study inspired by aṣọ òkè. Not an authenticated traditional textile.',region='Nigeria / Yoruba reference',desc='A procedural fabric study inspired by Yoruba strip-woven cloth. An original interpretation.'),
 dict(id='ayo',title='Gangan / Talking drum',creator='Dayo Objects',file='gangan-drum',cat='3D models',formats='BLEND',price=18000,tag='Yoruba / instrument study',context='Hourglass-drum interpretation referencing Yoruba gangan. Not a measured museum replica.',region='Yoruba / Nigeria and Benin',desc='An original hourglass drum study referencing the gangan form. No audio or animation included.'),
 dict(id='lamp',title='Offset / Studio lamp',creator='Nia Forms',file='studio-lamp',cat='3D models',formats='BLEND',price=7500,tag='Lighting prop',desc='A compact desk light with a warm enamel shade.')]
ASSETS.extend(json.loads((ROOT/'design/catalogue-additions.json').read_text(encoding='utf-8')))
ASSETS[0:0]=json.loads((ROOT/'design/lagos-life.json').read_text(encoding='utf-8'))
ASSETS.insert(0,dict(id='sanctuary',title='Sanctuary Temple',creator='Adefioye Favour',file='sanctuary-temple',cat='Environments',formats='BLEND · GLB',price=None,tag='Featured environment',region='Fantasy environment / no regional attribution',context='User-supplied forest temple scene. Cultural origin is not assigned to this fantasy environment.',desc='A forest temple environment with stone arches, stairs, lanterns, water and vegetation.',placeLabel='Portfolio scene',featured=True))
def creator_route(a):return {'Nia Forms':'creator','Dayo Objects':'creator:dayo','Sefi Materials':'creator:sefi','Adefioye Favour':'creator:owner'}[a['creator']]
for a in ASSETS:a['creatorRoute']=creator_route(a)
def money(v):return 'Project files' if v is None else '₦'+f'{v:,}'
def card(x,y,w,a,small=False):
 ph=round(w*.7);rect(x,y,w,ph+116,SUR,12,LINE,'Asset card / '+a['title']);art(x+1,y+1,w-2,ph,a['file'],11)
 rect(x+w-46,y+12,34,34,'#17191D',17,LINE);txt(x+w-36,y+20,'+',18,INK);hot(x+w-48,y+7,44,44,'Save '+a['title'],action='save:'+a['id'])
 txt(x+16,y+ph+17,a['title'],14 if w<300 else 16,INK,500,w-32)
 place=a.get('placeLabel',{'terra':'Mali','orbit':'Lagos','loop':'Ghana','kora':'Yoruba reference','ayo':'Yoruba reference','lamp':'Product study'}.get(a['id'],''))
 txt(x+16,y+ph+61,a['creator']+' · '+place,11 if w<300 else 12,MUT);txt(x+16,y+ph+92,'BLEND · GLB',10 if w<300 else 11,MUT,500)
 txt(x+w-98,y+ph+90,money(a['price']),12 if w<300 else 14,INK,600)
 hot(x,y,w-48,ph+110,'View '+a['title'],'detail:'+a['id'])
 current['hotspots'][-1]['assetId']=a['id']
 hot(x+12,y+ph+52,w-122,32,'Meet '+a['creator'],creator_route(a));current['hotspots'][-1]['assetId']=a['id']
 current['nodes'][-1]['assetId']=a['id']

# Desktop home.
frame('home','01 / Marketplace home',h=2440);nav('Home')
eyebrow(56,137,'Models / materials / environments')
txt(56,180,'3D assets for',62,INK,500);txt(56,251,'African worlds.',62,INK,500)
txt(58,347,'Browse scenes, props and materials.',17,MUT)
txt(58,375,'Inspect the geometry. Download the source files.',17,MUT)
inputbox(56,423,446,'Find your next asset',placeholder='Try danfo, woven fabric or courtyard',key='search')
button(518,450,164,'Search assets  →',action='search')
txt(58,531,'Try',12,MUT)
for x,label,query in [(94,'Danfo','danfo'),(184,'Woven textiles','stripe'),(330,'Courtyards','courtyard')]:
 w=pill(x,520,label);hot(x,514,w,44,'Search '+label,action='query:'+query)
art(728,120,656,440,'sanctuary-temple',16)
rect(750,474,420,67,'#17191D',8,LINE);txt(766,486,'FEATURED / SANCTUARY TEMPLE',12,INK,600);txt(766,512,'View scene in 3D  ↗',13,SOFT);hot(728,120,656,440,'Inspect Sanctuary Temple','detail:sanctuary')
heading(56,636,'Browse asset categories');link(1210,649,'View all assets  ↗','explore',170)
for i,(label,count,category) in enumerate([('Models & props',str(sum(a['cat']=='3D models'for a in ASSETS))+' assets','3D models'),('Materials & textiles',str(sum(a['cat']=='Materials'for a in ASSETS))+' assets','Materials'),('Environments',str(sum(a['cat']=='Environments'for a in ASSETS))+' assets','Environments'),('All assets',str(len(ASSETS))+' assets','All assets')]):
 x=56+i*338;rect(x,714,314,100,SUR,12,LINE);rect(x+20,737,3,52,ACC,1);txt(x+38,738,label,16,INK,500);txt(x+38,772,count,12,MUT);hot(x,714,314,100,'Browse '+label,'explore',action='category:'+category)
eyebrow(56,875,'Selected assets')
heading(56,909,'Everyday Lagos','Canteens, neighbourhood spaces and food scenes.')
link(1210,928,'View all '+str(len(ASSETS))+' assets  ↗','explore',170)
featured_ids=['canteen','barbershop','market','suya','church','school','classroom','akara-vendor']
for i,key in enumerate(featured_ids):card(56+(i%4)*338,1013+(i//4)*370,314,next(a for a in ASSETS if a['id']==key))
heading(56,1795,'Creator profiles');txt(56,1848,'Browse each creator’s catalogue.',14,MUT)
for i,(maker,initials,speciality,to) in enumerate([('Adefioye Favour','AF','Sanctuary Temple','creator:owner'),('Nia Forms','NF','Spaces & objects','creator'),('Sefi Materials','SM','Procedural textiles','creator:sefi')]):
 x=56+i*452;rect(x,1890,428,122,SUR,12,LINE);rect(x+22,1917,54,54,'#26333d',27);txt(x+35,1935,initials,16,SOFT,600);txt(x+96,1917,maker,20,INK,500);txt(x+96,1951,speciality,13,MUT);txt(x+387,1923,'↗',20,SOFT);hot(x,1890,428,122,'Visit '+maker,to)
rect(56,2055,1328,146,'#20222A',16);txt(88,2087,'Publish your work',31,INK,500);txt(88,2142,'Prepare files, previews and licensing in one listing workflow.',15,MUT);button(1116,2104,236,'Open creator studio  →','register')
foot(2252);current['height']=2340

# Search/filter gallery. Renderer can hide cards without inventing new data.
frame('explore','02 / Explore assets',h=2200);nav()
eyebrow(56,125,'Asset library');heading(56,158,'Explore assets','Browse '+str(len(ASSETS))+' assets. Filter by type, price and place reference.')
inputbox(56,261,1020,'Search assets',placeholder='Search models, materials, environments…',key='search')
button(1100,288,284,'Search library',action='search')
line(56,376,1328)
txt(56,413,'Refine your search',18,INK,600);link(56,452,'Reset filters','explore',170)
txt(56,518,'Asset type',13,INK,600)
for i,label in enumerate(['All assets','3D models','Materials','Environments']):
 y=554+i*43;rect(56,y,18,18,BG,4,LINE);txt(87,y+2,label,14,MUT);hot(52,y-9,220,39,'Filter '+label,action='category:'+label)
line(56,838,212);txt(56,867,'Compatibility',13,INK,600);pill(56,901,'Blender 4.2',True,140)
txt(56,958,'Sample prices',13,INK,600)
for i,label in enumerate(['Any price','Under ₦10,000','₦10,000 and above']):
 y=994+i*38;txt(56,y,'○  '+label,13,MUT);hot(52,y-10,220,38,label,action='price:'+str(i))
txt(56,1153,'Place reference',13,INK,600)
for i,label in enumerate(['All places','Nigeria','Ghana','Mali']):
 y=1190+i*38;txt(56,y,'○  '+label,13,MUT);hot(52,y-10,220,38,'Place: '+label,action='region:'+label)
txt(316,414,str(len(ASSETS))+' assets',15,INK,600,name='Results count');txt(1090,417,'Sort: Featured  ↓',14,MUT);hot(1082,402,260,44,'Change sorting',action='sort')
current['selects']=[dict(x=1078,y=400,w=306,h=44,label='Sort assets',key='sort',options=[['featured','Featured'],['price-asc','Price: low to high'],['price-desc','Price: high to low']])]
for i,a in enumerate(ASSETS):card(316+(i%4)*273,470+(i//4)*314,249,a)
foot(470+math.ceil(len(ASSETS)/4)*314+50);current['height']=470+math.ceil(len(ASSETS)/4)*314+150

# Product detail and licensing review.
for a in ASSETS:
 frame('detail:'+a['id'],'03 / Asset detail / '+a['title'],h=1720);nav()
 link(56,125,'← Back to explore','explore',200);txt(968,125,'SAMPLE LISTING / NOT FOR SALE',11,SOFT,600)
 art(56,183,826,620,a['file'],16)
 txt(56,835,'01 / ORIGINAL PREVIEW',11,MUT,600)
 txt(356,835,'BLENDER 4.2 / EDITABLE SOURCE',11,SOFT,600)
 eyebrow(930,187,'Everyday Lagos / '+a['cat'] if a.get('collection') else a['tag']);txt(930,221,a['title'].split(' / ')[0],42 if not a.get('featured') else 36,INK,500)
 txt(930,278,a['title'].split(' / ')[1] if ' / 'in a['title'] else 'Forest temple environment',25,INK,500)
 rect(930,328,454,76,SUR,10,LINE);rect(946,344,44,44,'#26333d',22);txt(956,358,''.join(p[0] for p in a['creator'].split()),14,SOFT,600);txt(1006,344,a['creator'],17,INK,500);txt(1006,375,'View creator storefront  ↗',12,MUT);hot(930,328,454,76,'By '+a['creator']+'  ↗',creator_route(a))
 txt(930,439,money(a['price']),35,INK,500);txt(930,489,'Original source and optimized exports' if a.get('featured') else 'Illustrative price · NGN',13,MUT)
 rect(930,536,454,126,SUR,12,LINE);txt(950,555,'Download formats' if a.get('featured') else 'Standard / one end project',17,INK,500)
 txt(950,594,'BLEND / GLB / OBJ / FBX' if a.get('featured') else 'Personal or commercial project use.',13,MUT);txt(950,622,'Commercial-use terms not specified.' if a.get('featured') else 'No standalone redistribution.',13,MUT)
 if a.get('featured'):
  button(930,690,454,'Inspect scene in 3D  →');current['hotspots'][-1]['url']='http://127.0.0.1:8765/prototype/asset.html?id=sanctuary'
 else:button(930,690,454,'Review licence & request  →','licence:'+a['id'])
 button(930,754,454,'Save to collection',kind='secondary',action='save:'+a['id'])
 txt(930,825,'3D preview and files available in the browser.' if a.get('featured') else 'Marketplace pricing is sample content.',12,MUT)
 txt(56,910,'Overview',28,INK,500);txt(56,962,a['desc'],14,MUT,w=826)
 txt(56,1024,'Included files',22,INK,500)
 rect(56,1071,826,184,SUR,12,LINE)
 txt(80,1096,'sanctuary-original.blend' if a.get('featured') else a['file']+'.blend',17,INK,500);txt(80,1130,'Original full scene · Blender 4.2' if a.get('featured') else 'Editable scene and materials · authored in Blender 4.2',13,MUT)
 pill(743,1093,'BLEND',True,106);line(80,1170,778)
 txt(80,1191,'sanctuary-web.glb' if a.get('featured') else a['file']+'.png',15,INK,500);txt(621,1194,'Optimized web preview' if a.get('featured') else 'Original preview image',12,MUT)
 rect(930,919,454,257,'#202327',12,LINE);eyebrow(954,944,'Technical information');txt(954,982,'Compatibility and usage',21,INK,500)
 details=['Blender 4.2 editable source','GLB · OBJ · FBX exports','512px packed colour maps' if a.get('collection') else 'Materials retained in the source',str(a['characters'])+' static adults · not rigged' if a.get('characters') else 'No character animation included']
 for j,s in enumerate(details):txt(954,1034+j*29,s,13,MUT)
 txt(56,1310,'Place, context and interpretation',26,INK,500)
 txt(56,1360,a.get('region','Contemporary product study'),15,SOFT,500)
 txt(56,1394,a.get('context','Original contemporary prop study. No real product affiliation.'),14,MUT,w=1328)
 line(56,1462,1328)
 for x,label,value in [(56,'SOURCE FORMAT',a['formats']),(405,'AUTHORING TOOL','Blender 4.2'),(754,'CONTENTS','Editable scene + materials'),(1103,'ASSET STATUS','Original digital study')]:
  eyebrow(x,1491,label);txt(x,1524,value,14,INK,500)
 foot(1624)

 frame('licence:'+a['id'],'04 / Licence review / '+a['title'],h=1080);nav();link(96,130,'← Back to asset','detail:'+a['id'],200)
 eyebrow(96,196,'Usage information');heading(96,232,'File formats and usage' if a.get('featured') else 'Licence details','Source scene usage terms' if a.get('featured') else 'Example terms for the marketplace design prototype.')
 rect(96,353,760,480,SUR,12,LINE);txt(128,387,'Portfolio scene' if a.get('featured') else 'Standard / single project',25,INK,500)
 usage=[('Original source','The full supplied Blender environment.'),('Portable exports','Reduced geometry in GLB, OBJ and FBX.'),('Usage terms','A commercial-use licence has not been specified.')] if a.get('featured') else [('Use in one end project','For example, a game, film or visualisation.'),('Adapt the asset for your scene','Edit forms, materials and colours to suit your project.'),('Keep the source files private','Do not resell, share or redistribute the standalone asset.')]
 for i,(t,s) in enumerate(usage):
  y=460+i*104;txt(128,y,'0'+str(i+1),15,SOFT,600);txt(174,y,t,18,INK,500);txt(174,y+33,s,14,MUT)
 art(902,353,442,275,a['file'],12);txt(902,659,a['title'],20,INK,500,w=442);txt(902,718,money(a['price'])+' · illustrative',18,MUT)
 button(902,762,442,'Request asset · demo','request:'+a['id']);txt(903,828,'No charge. No personal information collected.',12,MUT)
 foot(981)

 frame('request:'+a['id'],'05 / Request acknowledgement',h=1000);nav();eyebrow(395,220,'Buyer journey / demo complete')
 txt(395,274,'Request preview',44,INK,500);txt(395,347,'You reviewed the asset, its compatibility and the example licence.',16,MUT)
 rect(395,414,650,184,SUR,12,LINE);txt(427,446,'Request previewed',22,INK,500)
 txt(427,494,'This interaction ends the design prototype.',16,MUT);txt(427,524,'Nothing was purchased, sent or downloaded.',16,MUT)
 button(395,646,220,'Keep exploring  →','explore');button(631,646,204,'View creator',creator_route(a),'secondary');foot(897)

# Creator profile.
for cid,maker,tag in [('creator','Nia Forms','Environment art'),('creator:dayo','Dayo Objects','Object design'),('creator:sefi','Sefi Materials','Material studies'),('creator:owner','Adefioye Favour','Sanctuary Temple')]:
 frame(cid,'06 / Creator profile / '+maker,h=1160);nav('Creators');rect(56,125,1328,280,'#222C2B',16)
 mark(96,172,76,'#D5BFA5');eyebrow(204,169,'Portfolio creator' if maker=='Adefioye Favour' else 'Sample creator profile');txt(204,202,maker,46,INK,500)
 txt(206,269,'Sanctuary Temple / environment study' if maker=='Adefioye Favour' else 'Environment, object and material studies.',18,MUT);pill(206,315,tag);pill(365,315,'Blender',False,110)
 txt(1052,183,'3D ARTIST' if maker=='Adefioye Favour' else 'SAMPLE CREATOR',11,MUT,600);txt(1052,214,'Blender · 3D design',14,INK);txt(1052,247,'Instagram @fioye_3d' if maker=='Adefioye Favour' else 'Fictional identity',12,MUT)
 if maker=='Adefioye Favour':
  hot(1044,232,300,44,'Instagram @fioye_3d');current['hotspots'][-1]['url']='https://www.instagram.com/fioye_3d/'
 heading(56,464,'Asset catalogue');txt(56,520,'Forest temple environment with editable source files.' if maker=='Adefioye Favour' else 'Illustrative catalogue entries for the marketplace prototype.',16,MUT)
 own_assets=[a for a in ASSETS if a['creator']==maker]
 for i,a in enumerate(own_assets):card(56+(i%3)*452,600+(i//3)*440,428,a)
 footer_y=600+math.ceil(len(own_assets)/3)*440+45
 foot(footer_y);current['height']=footer_y+95

def studio(title,sub,id='dashboard',h=1100):
 frame(id,title,h=h);rect(0,0,256,h,SUR);mark(28,30);txt(69,33,'RenderMarket',20,INK,600);txt(28,95,'CREATOR STUDIO',11,MUT,600)
 for i,(name,to) in enumerate([('Overview','dashboard'),('My listings','listings'),('Upload asset','upload-1'),('View marketplace','home')]):
  y=146+i*62
  if (to==id or (id.startswith('upload') and to=='upload-1')):rect(16,y-12,224,48,'#26333d',8)
  txt(32,y,name,15,INK if to==id else MUT,500);hot(16,y-12,224,48,name,to)
 txt(28,h-108,'DEMO WORKSPACE',11,SOFT,600);txt(28,h-77,'No account required',12,MUT)
 txt(304,36,'Studio / Nia Forms',13,MUT);txt(1100,36,'Sample creator session',12,SOFT)
 line(304,87,1088);heading(304,133,title,sub)

for id in ['dashboard','listings']:
 studio('Creator dashboard' if id=='dashboard' else 'My listings','Manage listings and drafts. Sample workspace.',id)
 button(1170,133,214,'Upload an asset  +','upload-1')
 for i,(val,label) in enumerate([('3','Sample listings'),('1','Draft to finish'),(' / ','No sales connected')]):
  x=304+i*368;rect(x,271,344,134,SUR,12,LINE);txt(x+24,296,val,38,INK,500);txt(x+24,360,label,14,MUT)
 txt(304,465,'Your listings',24,INK,500);txt(304,510,'ASSET',11,MUT,600);txt(902,510,'STATUS',11,MUT,600);txt(1145,510,'SAMPLE PRICE',11,MUT,600)
 for i,a in enumerate([next(a for a in ASSETS if a['id']==key)for key in ['terra','loop','lamp']]):
  y=548+i*126;line(304,y-12,1080);art(304,y,126,92,a['file'],8);txt(452,y+14,a['title'],17,INK,500);txt(452,y+47,a['formats'],12,MUT)
  pill(902,y+25,'Demo listing',True,132);txt(1145,y+31,money(a['price']),16,INK);hot(442,y,430,92,'Review '+a['title'],'detail:'+a['id'])
 line(304,957,1080);txt(304,990,'Ready to finish your next idea? Continue the sample draft.',14,MUT);link(1170,990,'Continue draft  →','upload-1',200)

# Account entry without collecting credentials.
frame('register','07 / Creator entry',h=1000);nav();art(56,143,626,660,'danfo-minibus',16)
eyebrow(764,218,'Creator account');heading(764,259,'Creator studio')
txt(764,330,'In a live product, you would create a secure account here.',15,MUT);txt(764,362,'This prototype uses a fictional creator session.',15,MUT)
rect(764,426,610,127,SUR,12,LINE);txt(790,451,'Nia Forms / Demo workspace',20,INK,500);txt(790,493,'No email, password or personal information needed.',14,MUT)
button(764,599,450,'Enter demo creator studio  →','dashboard');link(764,682,'Return to marketplace','home',250);foot(898)

def steps(active):
 for i,label in enumerate(['01  Asset basics','02  Files & details','03  Price & review']):
  x=304+i*367;rect(x,255,343,58,'#2A2B44' if i==active else SUR,8,SOFT if i==active else LINE);txt(x+18,276,label,14,INK if i==active else MUT,500)
def upload(id,title,sub,active):studio(title,sub,id,1240);steps(active)

upload('upload-1','Asset basics','Upload flow / step 1 of 3. Values stay in this browser session only.',0)
inputbox(304,361,650,'Asset title','Courtyard / Earthen scene kit',key='title')
inputbox(304,474,650,'Description','An original earthen courtyard with modular walls and an indigo seat.','',key='description',h=130)
inputbox(304,665,650,'Category','Environments',key='category')
inputbox(304,778,650,'Tags','Architecture, Sahel-inspired, courtyard',key='tags')
inputbox(1002,755,382,'Place or cultural reference','Sahel-inspired architectural study',key='culturalContext')
inputbox(1002,868,382,'Reference note','Original interpretation; not a replica',key='referenceNote')
rect(1002,361,382,348,SUR,12,LINE);eyebrow(1026,389,'A small bit of guidance');txt(1026,431,'Describe the asset',25,INK,500);txt(1026,467,'and its limitations.',25,INK,500)
txt(1026,531,'Describe what is included and how',14,MUT);txt(1026,558,'the asset could be used. Be specific',14,MUT);txt(1026,585,'about any limitations.',14,MUT)
button(304,949,170,'Save demo draft',kind='secondary',action='draft');button(707,949,247,'Continue to files  →','upload-2')
txt(304,1042,'No real file upload or publication occurs in this prototype.',13,MUT)

upload('upload-2','Files and technical details','Upload flow / step 2 of 3. Use the supplied sample to continue.',1)
rect(304,361,650,201,BG,12,LINE);txt(334,391,'Asset files & previews',20,INK,500)
txt(334,440,'Sample bundle: sahel-courtyard.blend · 4.2 MB',14,MUT);txt(334,468,'One original preview · simulated file size',13,MUT)
button(334,500,220,'Attach sample files',kind='secondary',action='attach')
art(1002,361,382,286,'sahel-courtyard',12);txt(1002,670,'Preview / original procedural render',12,MUT)
inputbox(304,603,310,'File formats','BLEND',key='formats');inputbox(644,603,310,'Software version','Blender 4.2',key='software')
inputbox(304,716,310,'Geometry','Modular mesh objects',key='geometry');inputbox(644,716,310,'Textures','Procedural materials',key='textures')
txt(304,837,'Avoid unsupported claims such as “game-ready” or “rigged”.',14,MUT)
button(304,949,164,'← Asset basics','upload-1','secondary');button(707,949,247,'Continue to pricing  →','upload-3')

upload('upload-3','Pricing and licence','Upload flow / step 3 of 3. Illustrative prices and example licence only.',2)
inputbox(304,361,650,'Price in NGN','24000',key='price')
txt(304,474,'Example licence',14,INK,500);rect(304,508,650,154,'#26333d',12,SOFT)
txt(329,534,'Standard / one end project',20,INK,500);txt(329,581,'Personal or commercial project use.',14,MUT);txt(329,609,'No redistribution of the standalone source files.',14,MUT)
rect(304,712,650,96,SUR,8,LINE);txt(328,736,'Before a real marketplace launches',15,INK,600);txt(328,766,'Licence terms need legal review and creator agreement.',14,MUT)
art(1002,361,382,286,'sahel-courtyard',12);txt(1002,676,'Courtyard / Earthen scene kit',23,INK,500);txt(1002,720,'Nia Forms · sample listing',14,MUT)
button(304,949,164,'← Files & details','upload-2','secondary');button(707,949,247,'Preview listing  →','upload-preview')

studio('Listing preview','Review the sample listing. Publishing below is a local simulation.','upload-preview',1140)
art(304,274,600,450,'sahel-courtyard',12);eyebrow(952,278,'Sample listing preview');txt(952,320,'Courtyard /',36,INK,500);txt(952,370,'Earthen scene kit',36,INK,500)
txt(952,443,'₦24,000 · Standard licence',20,INK,500);txt(952,490,'BLEND / Blender 4.2',14,MUT)
txt(952,540,'An original earthen courtyard with',14,MUT);txt(952,567,'modular walls and an indigo seat.',14,MUT)
button(952,631,432,'Publish demo listing  →','published');button(952,697,432,'← Edit pricing','upload-3','secondary')
rect(304,790,1080,105,SUR,12,LINE);txt(329,819,'Publication preview',18,INK,500);txt(329,856,'No files are transmitted. No listing is made public. The next screen confirms the simulation.',14,MUT)

studio('Demo listing published','Creator journey complete / simulation only.','published',1050)
rect(304,281,1080,371,SUR,16,LINE);eyebrow(344,324,'Draft → details → licence → preview');txt(344,375,'Listing prepared',43,INK,500);txt(344,431,'Demo publication',43,INK,500)
txt(344,519,'The sample listing has been marked ready in this session.',16,MUT);txt(344,551,'Nothing was uploaded or published to a real marketplace.',16,MUT)
button(304,708,226,'Return to dashboard','dashboard');button(546,708,220,'View sample listing','detail:terra','secondary')

frame('saved','08 / Saved assets',h=1050);nav();heading(56,151,'Keep a little inspiration close.','Save and remove sample assets in this prototype session.')
for i,a in enumerate(ASSETS[:3]):card(56+i*452,305,428,a)
foot(952)

frame('about','09 / About the concept',h=1020);nav();eyebrow(96,170,'RenderMarket / independent portfolio project')
txt(96,220,'About RenderMarket',54,INK,500)
for i,s in enumerate(['Discover African objects, materials and environments.','Inspect file formats, compatibility and an example licence.','Try a creator workflow from draft to demo publication.']):
 txt(96,348+i*92,'0'+str(i+1),15,SOFT,600);txt(158,343+i*92,s,22,INK,500)
rect(96,663,1248,113,SUR,12,LINE);txt(122,688,'Created now, with an honest scope.',21,INK,500);txt(122,731,'Fictional catalogue. AI-assisted design and code. No user research, backend, payments or real marketplace.',14,MUT)
button(96,823,202,'Explore the prototype','explore');button(314,823,206,'Try the creator flow','register','secondary');foot(940)

# Reference pages: reusable foundation, components, original logo options.
frame('cover','00 / Cover & project status',1440,1000,'Overview');mark(72,70,64);txt(156,75,'RenderMarket',46,INK,500)
eyebrow(72,220,'Independent UI/UX exploration / October 2026')
txt(72,270,'Asset marketplace',72,INK,500);txt(72,354,'UI/UX design study',72,INK,500)
txt(72,488,'A marketplace concept connecting African 3D creativity',22,MUT);txt(72,522,'with the people building their next world.',22,MUT)
button(72,615,218,'Explore buyer journey','home');button(306,615,218,'Explore creator journey','register','secondary')
txt(72,769,'SELF-INITIATED · IN PROGRESS · AI-ASSISTED',12,SOFT,600)
txt(72,806,'Fictional listings. No production marketplace or fabricated research.',16,MUT)
txt(72,840,'Separate from the Access Forge competition proposal.',16,MUT)

frame('foundations','01 / Foundations',h=1360,page='Foundations');heading(56,70,'Foundations','Dark premium direction / shared tokens used in every screen.')
colors=[('Canvas',BG),('Surface',SUR),('Raised',PANEL),('Border',LINE),('Text',INK),('Muted',MUT),('Action',ACTION),('Accent',SOFT)]
for i,(name,c) in enumerate(colors):
 x=56+i*168;rect(x,190,144,112,c,12,LINE);txt(x,322,name,16,INK,500);txt(x,350,c,12,MUT)
line(56,403,1328);eyebrow(56,438,'Type / Arial + Arial')
for i,(size,s) in enumerate([(62,'Give your next world a head start.'),(36,'Thoughtful details. Clear decisions.'),(24,'A system with room to create.'),(16,'Readable body copy and useful asset metadata.'),(14,'UI labels / compact and direct'),(12,'Captions / sample content disclosures')]):
 y=487+sum([s+24 for s,_ in [(62,''),(36,''),(24,''),(16,''),(14,''),(12,'')]][:i]);txt(56,y,s,size,INK,500 if size>16 else 400);txt(1205,y,str(size)+' px',14,MUT)
line(56,945,1328);eyebrow(56,982,'8 px rhythm / 4 px substeps')
for i,v in enumerate([4,8,12,16,24,32,48,64]):
 x=56+i*168;rect(x,1028,v,v,ACC,2);txt(x,1110,str(v)+' px',14,MUT)
txt(56,1190,'Desktop 1440 px · 12 columns · 56 px margins · 24 px gutters',18,INK)
txt(56,1235,'Mobile 390 px · 4 columns · 20 px margins · 16 px gutters',18,MUT)

frame('components','02 / Components & states',h=1220,page='Components');heading(56,64,'Components','Reusable buttons, cards, input fields and feedback. Native Figma components are generated by the importer.')
eyebrow(56,196,'Actions');button(56,234,190,'Explore assets','explore');button(270,234,190,'Secondary action','home','secondary')
rect(484,234,190,48,'#303238',8);txt(502,249,'Unavailable',14,'#878B94',600)
rect(698,230,198,56,BG,12,SOFT);button(702,234,190,'Keyboard focus','explore')
eyebrow(56,344,'Inputs / default / error');inputbox(56,386,406,'Asset title',placeholder='Name your asset')
inputbox(494,386,406,'Price in NGN','-20');rect(494,413,406,52,BG,8,'#d4c3ba');txt(494,485,'Enter a price of zero or greater.',13,'#d4c3ba')
eyebrow(56,571,'Asset card');card(56,608,342,ASSETS[1])
eyebrow(470,571,'Feedback / state is also written in words')
for i,(title,body,c) in enumerate([('Draft saved','Your demo details stay in this browser session.',GREEN),('No matching assets','Try another term or reset your filters.',MUT),('Upload unavailable','Use the sample files to continue this prototype.','#d4c3ba')]):
 y=608+i*128;rect(470,y,880,104,SUR,10,LINE);txt(494,y+22,title,18,c,500);txt(494,y+60,body,14,MUT)
txt(56,1107,'48 px action height · 8 px control radius · 12 px card radius · restrained borders, no decorative glow',14,MUT)

frame('brand','03 / Logo exploration',h=1040,page='Foundations');heading(56,64,'Logo studies','Original vector explorations. Fold R is the working selection and remains open to refinement.')
for i,(title,sub) in enumerate([('01 / Fold R','A folded plane, a readable initial.'),('02 / Open cube','An open structure, a modular world.'),('03 / Typographic cut','A distinctive wordmark with a cut R.')]):
 x=56+i*452;rect(x,209,428,504,SUR,12,LINE);txt(x+28,250,title,22,INK,500);txt(x+28,295,sub,14,MUT)
 if i==0:mark(x+140,406,130)
 elif i==1:
  for dx,dy in [(0,0),(50,28),(0,56)]:rect(x+138+dx,413+dy,90,6,SOFT,0)
  rect(x+138,413,6,110,SOFT);rect(x+275,441,6,110,SOFT)
 else:txt(x+32,432,'Render',53,INK,600);rect(x+33,502,132,7,SOFT)
pill(84,652,'Working selection',True,170);txt(56,793,'A simple mark survives small sizes and stays quiet beside the artwork.',26,INK,500)
txt(56,854,'The final identity should be refined by the project owner before presenting it as a personal design decision.',16,MUT)

# Structural wireframes retained as actual intermediate artefacts, not claimed as historical research.
for kind,title in [('home','Home'),('explore','Explore'),('detail:terra','Asset detail'),('upload-1','Creator upload')]:
 source=next(s for s in SCENES if s['id']==kind);s=copy.deepcopy(source);s['id']='wire-'+kind;s['title']='Wireframe / '+title;s['page']='Wireframes';s['background']='#F1F1EF';s['hotspots']=[];s.pop('inputs',None)
 for n in s['nodes']:
  if n['type']=='image':n.clear();n.update(type='rect',x=0,y=0,w=1,h=1,fill='#DDDEDA',r=0,name='Preview placeholder')
 # Preserve image geometry using original nodes.
 for n,o in zip(s['nodes'],source['nodes']):
  if o['type']=='image':n.update(x=o['x'],y=o['y'],w=o['w'],h=o['h'])
  elif n['type']=='text':n['color']='#363A3A';n['font']='Arial'
  elif n['type']=='rect':n['fill']='#FFFFFF' if n.get('fill')!=BG else '#F1F1EF';n['stroke']='#A7ABA8'
  elif n['type']=='vector':n['fill']='#363A3A'
 SCENES.append(s)

# Designed mobile adaptations of the buyer flow.
def mobile_nav():
 mark(20,23,25);txt(58,25,'RenderMarket',20,INK,600);txt(320,27,'Menu',13,MUT);hot(310,16,60,44,'Open navigation',action='menu');line(20,75,350)
def mobile_bottom():
 rect(0,current['height']-76,390,76,SUR);y=current['height']-56
 for i,(label,to) in enumerate([('Explore','explore'),('Saved','saved'),('Studio','register')]):txt(28+i*124,y,label,14,INK,500);hot(14+i*124,y-12,106,48,label,to)

frame('mobile-home','Mobile / Home',390,1690,'Mobile');mobile_nav();eyebrow(20,111,'A new perspective on digital craft')
txt(20,155,'3D assets for',39,INK,500);txt(20,204,'African worlds.',39,INK,500)
txt(20,276,'Models, materials and environments.',15,MUT);txt(20,300,'Inspect the geometry. Get the source files.',15,MUT)
inputbox(20,348,350,'Find your next asset',placeholder='Search danfo, textiles, courtyards…',key='search')
button(20,447,350,'Search assets  →',action='search')
for x,label,query in [(20,'Danfo','danfo'),(110,'Textiles','stripe'),(212,'Courtyards','courtyard')]:
 w=pill(x,516,label);hot(x,510,w,44,'Search '+label,action='query:'+query)
art(20,582,350,265,'sanctuary-temple',12);hot(20,582,350,265,'Inspect Sanctuary Temple','detail:sanctuary')
txt(20,886,'Selected assets',28,INK,500);txt(20,925,'Sanctuary Temple',24,INK,500);txt(20,973,'Featured Blender scene / 3D preview available',12,MUT)
card(20,1013,350,ASSETS[0])
rect(20,1430,350,112,SUR,12,LINE);txt(40,1451,'Meet the maker',11,SOFT,600);txt(40,1477,'Dayo Objects  ↗',22,INK,500);txt(40,1513,'Urban props & instruments · sample creator',12,MUT);hot(20,1430,350,112,'Visit Dayo Objects','creator:dayo')
txt(20,1590,'Independent portfolio concept · No transactions',11,MUT);mobile_bottom()

frame('mobile-explore','Mobile / Explore',390,1340,'Mobile');mobile_nav();txt(20,112,'Explore assets',32,INK,500);txt(20,167,str(len(ASSETS))+' assets',13,MUT,name='Mobile results count')
inputbox(20,216,350,'Search assets',placeholder='Try “danfo” or “materials”',key='search');button(20,321,168,'Search',action='search');button(204,321,166,'Filters',kind='secondary',action='mobile-filter')
txt(20,404,'Asset library',17,INK,500)
for i,a in enumerate(ASSETS[:2]):card(20,457+i*372,350,a)
mobile_bottom()

frame('mobile-detail:terra','Mobile / Asset detail',390,1900,'Mobile');mobile_nav();link(20,109,'← Back to explore','explore',200);art(20,161,350,302,'sahel-courtyard',12)
eyebrow(20,501,'Modular environment');txt(20,538,'Courtyard /',36,INK,500);txt(20,583,'Earthen scene kit',36,INK,500);link(20,645,'By Nia Forms  ↗','creator',200)
line(20,696,350);txt(20,730,'₦24,000',32,INK,500);txt(20,777,'Illustrative price · NGN',13,MUT);pill(20,825,'Standard licence',True,172)
txt(20,884,'One personal or commercial end project.',14,MUT);txt(20,913,'No standalone asset redistribution.',14,MUT)
button(20,967,350,'Review licence & request  →','licence:terra');button(20,1031,350,'Save to collection',kind='secondary',action='save:terra')
txt(20,1110,'Prototype only. No payment or download.',12,MUT)
for i,(l,v) in enumerate([('FILE FORMATS','BLEND'),('AUTHORING TOOL','Blender 4.2'),('CONTENTS','Editable scene + materials')]):eyebrow(20,1184+i*94,l);txt(20,1214+i*94,v,16,INK)
txt(20,1480,'Included source files',22,INK,500);rect(20,1524,350,112,SUR,12,LINE);txt(38,1546,'sahel-courtyard.blend',15,INK,500);txt(38,1594,'sahel-courtyard.png / preview',13,MUT)
eyebrow(20,1680,'Place and interpretation');txt(20,1712,'Mali / Sahel-inspired architecture',14,INK);txt(20,1744,'Original study, not a heritage reconstruction.',12,MUT)
mobile_bottom()

TOKENS=dict(meta=dict(name='RenderMarket',version='0.4.0',status='reference-informed design iteration, created 2026-10-29'),color=dict(canvas=BG,surface=SUR,raised=PANEL,border=LINE,text=INK,muted=MUT,action=ACTION,accent=SOFT,success=GREEN,error='#d4c3ba'),typography=dict(heading='Arial',body='Arial',scale=[12,14,16,18,24,36,44,62]),spacing=[4,8,12,16,24,32,48,64],radius=dict(control=8,card=12,hero=16),layout=dict(desktop=1440,mobile=390,desktopMargin=56,mobileMargin=20,gutter=24))
(ROOT/'design/design-tokens.json').write_text(json.dumps(TOKENS,indent=2))
(ROOT/'design/scenes.json').write_text(json.dumps(SCENES,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'prototype/scenes.js').write_text('window.RM_SCENES='+json.dumps(SCENES,ensure_ascii=False)+';\nwindow.RM_ASSETS='+json.dumps(ASSETS,ensure_ascii=False)+';',encoding='utf-8')
(ROOT/'prototype/catalogue.js').write_text('window.RM_ASSETS='+json.dumps(ASSETS,ensure_ascii=False)+';',encoding='utf-8')

def svg(s,embed=False):
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{s["width"]}" height="{s["height"]}" viewBox="0 0 {s["width"]} {s["height"]}"><title>{html.escape(s["title"])}</title><rect width="100%" height="100%" fill="{s["background"]}"/>']
 for i,n in enumerate(s['nodes']):
  x,y=n['x'],n['y'];name=html.escape(n.get('name',''),quote=True)
  if n['type']=='rect':parts.append(f'<rect x="{x}" y="{y}" width="{n["w"]}" height="{n["h"]}" rx="{n.get("r",0)}" fill="{n["fill"]}" stroke="{n.get("stroke","none")}"/>')
  elif n['type']=='text':
   spans=''.join(f'<tspan x="{x}" dy="{0 if j==0 else n["size"]*1.2}">{html.escape(t)}</tspan>' for j,t in enumerate(n['text'].split('\n')))
   parts.append(f'<text x="{x}" y="{y+n["size"]*.83}" fill="{n["color"]}" font-family="{n["font"]}, Arial, sans-serif" font-size="{n["size"]}" font-weight="{n["weight"]}">{spans}</text>')
  elif n['type']=='vector':parts.append(f'<path d="{n["path"]}" fill="{n["fill"]}" fill-rule="evenodd" transform="translate({x},{y}) scale({n["w"]/28})"/>')
  elif n['type']=='image':
   path=ROOT/'assets/artwork'/f'{n["file"]}.png';href='../../assets/artwork/'+n['file']+'.png'
   if embed and path.exists():href='data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()
   parts.append(f'<defs><clipPath id="c{i}"><rect x="{x}" y="{y}" width="{n["w"]}" height="{n["h"]}" rx="{n["r"]}"/></clipPath></defs><image x="{x}" y="{y}" width="{n["w"]}" height="{n["h"]}" href="{href}" preserveAspectRatio="xMidYMid slice" clip-path="url(#c{i})"><title>{name}</title></image>')
 parts.append('</svg>');return ''.join(parts)

for s in SCENES:
 name=s['id'].replace(':','-')+'.svg';folder='wireframes' if s['page']=='Wireframes' else 'screens'
 (ROOT/'design'/folder/name).write_text(svg(s,True),encoding='utf-8')

# Compact, original identity exports.
for name,bg,color in [('logo-dark',BG,INK),('logo-light','#FFFFFF',BG),('logo-mono','none',INK)]:
 content=f'<svg xmlns="http://www.w3.org/2000/svg" width="304" height="64" viewBox="0 0 304 64"><rect width="304" height="64" fill="{bg}"/><path fill="{color}" fill-rule="evenodd" d="M 0 28 L 0 0 L 18 0 L 28 10 L 18 20 L 28 28 L 17 28 L 7 18 L 7 28 Z M 7 7 L 7 13 L 16 13 L 20 10 L 16 7 Z" transform="translate(16,18)"/><text x="57" y="43" font-family="Arial,sans-serif" font-size="25" font-weight="600" fill="{color}">RenderMarket</text></svg>'
 (ROOT/'assets/logo'/f'{name}.svg').write_text(content)
print('Built',len(SCENES),'editable artboards and design tokens.')
