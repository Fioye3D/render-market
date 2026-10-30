"""Meaningful structural checks: destinations, image integrity, contrast, clickable target bounds."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
scenes=json.loads((root/'design/scenes.json').read_text(encoding='utf-8'))
tokens=json.loads((root/'design/design-tokens.json').read_text())
ids={s['id'] for s in scenes};errors=[]
for s in scenes:
 for n in s['nodes']:
  if n['type']=='image' and not(root/'assets/artwork'/f'{n["file"]}.png').exists():errors.append('Missing artwork '+n['file'])
  if n['x']<0 or n['y']<0:errors.append('Negative position '+s['id']+' '+n.get('name',''))
 for h in s['hotspots']:
  if h.get('to') and h['to']not in ids:errors.append('Broken destination '+s['id']+' → '+h['to'])
  if h['x']+h['w']>s['width']+1 or h['y']+h['h']>s['height']+1:errors.append('Out-of-bounds target '+s['id']+' '+h['label'])
  if min(h['w'],h['h'])<24:errors.append('Undersized target '+s['id']+' '+h['label'])
def lum(c):
 v=[int(c[i:i+2],16)/255 for i in (1,3,5)];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
def contrast(a,b):x,y=sorted([lum(a),lum(b)]);return(y+.05)/(x+.05)
c=tokens['color'];pairs=[('Body on canvas',c['text'],c['canvas']),('Muted on canvas',c['muted'],c['canvas']),('Muted on surface',c['muted'],c['surface']),('Primary button',c['text'],c['action']),('Accent on surface',c['accent'],c['surface']),('Error on canvas',c['error'],c['canvas'])]
report=[]
for name,a,b in pairs:
 ratio=round(contrast(a,b),2);report.append(dict(pair=name,foreground=a,background=b,ratio=ratio,target=4.5,passes=ratio>=4.5))
 if ratio<4.5:errors.append('Contrast failed '+name)
(root/'design/contrast-report.json').write_text(json.dumps(report,indent=2))
print('Artboards:',len(scenes),'Interactions:',sum(len(s['hotspots'])for s in scenes),'Contrast pairs:',len(report))
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print('PASS: destinations, images, target bounds/minimum sizes and selected contrast pairs.')
