"""Small, original tileable colour maps. No stock photography or raster AI imagery."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random, math
out=Path(__file__).resolve().parents[1]/'assets/textures/lagos-life'
out.mkdir(parents=True,exist_ok=True)
random.seed(412)
for name,base,kind in [('plaster',(205,204,192),'stone'),('concrete',(143,145,141),'stone'),('oak',(135,92,55),'wood'),('walnut',(72,46,30),'wood'),('terrazzo',(173,171,156),'chips'),('fabric',(110,116,119),'fabric'),('turf',(64,92,45),'grass'),('akara',(156,80,24),'food'),('asphalt',(75,78,77),'stone')]:
 im=Image.new('RGB',(512,512));p=im.load()
 for y in range(512):
  for x in range(512):
   n=random.gauss(0,3.6)
   if kind=='wood':n+=7*math.sin(y*.27+3*math.sin(x*.014))+4*math.sin(y*.93+math.sin(x*.022))
   if kind=='fabric':n+=5*((x%3==0)+(y%3==0)-.6)
   if kind=='grass':n+=random.gauss(0,9)
   if kind=='food':n+=8*math.sin(x*.08)*math.cos(y*.11)+random.gauss(0,7)
   p[x,y]=tuple(max(0,min(255,int(c+n)))for c in base)
 if kind=='chips':
  d=ImageDraw.Draw(im)
  for i in range(2100):
   x=random.randrange(512);y=random.randrange(512);r=random.randrange(1,5);c=random.choice([(98,104,98),(210,202,181),(151,135,115),(196,194,184)])
   for dx in (-512,0,512):
    for dy in (-512,0,512):d.polygon([(x+dx-r,y+dy),(x+dx,y+dy-r),(x+dx+r,y+dy+1),(x+dx+1,y+dy+r)],fill=c)
 im.save(out/(name+'.png'),optimize=True)
print('Wrote nine reusable 512px colour maps.')
