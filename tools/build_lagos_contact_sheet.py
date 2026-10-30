"""Contact sheet from the actual authored 3D renders, not UI screenshots."""
from PIL import Image,ImageDraw,ImageFont,ImageOps
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
assets=json.loads((root/'design/lagos-life.json').read_text(encoding='utf-8'))
w=1184;cardw=368;gap=20;top=110;cardh=330
im=Image.new('RGB',(w,top+4*(cardh+gap)+30),'#101112');d=ImageDraw.Draw(im)
f=lambda n:ImageFont.truetype(str(root/'assets/fonts/Inter.ttf'),n)
d.text((20,22),'RenderMarket / Everyday Lagos',font=f(28),fill='#f5f3ee')
d.text((20,66),'10 new scene and prop studies · actual Blender renders',font=f(16),fill='#b2b7c1')
for i,a in enumerate(assets):
 x=20+(i%3)*(cardw+gap);y=top+(i//3)*(cardh+gap)
 d.rounded_rectangle((x,y,x+cardw,y+cardh),radius=8,fill='#191b1e')
 picture=Image.open(root/'assets/artwork'/(a['file']+'.png')).convert('RGB');im.paste(ImageOps.fit(picture,(cardw,276)),(x,y))
 title=a['title'].split(' / ')[-1].replace('Neighbourhood football pitch','Football pitch').replace('Contemporary canteen','Contemporary canteen')
 d.text((x+12,y+286),title,font=f(16),fill='#f5f3ee')
 d.text((x+12,y+310),'BLEND / GLB / OBJ / FBX',font=f(10),fill='#b2b7c1')
target=root/'assets/screenshots/everyday-lagos-collection.jpg';im.save(target,quality=92,optimize=True)
print(target)
