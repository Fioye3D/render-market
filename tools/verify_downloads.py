"""Check real download paths, sizes, GLB headers and ZIP CRCs without browser side effects."""
from pathlib import Path
import json,struct,zipfile,hashlib
root=Path(__file__).resolve().parents[1];errors=[];checked=0
manifests=list((root/'assets/downloads/catalogue').glob('*/manifest.json'))+[root/'assets/downloads/sanctuary/manifest.json']
for p in manifests:
 d=json.loads(p.read_text());formats={f['format']for f in d['downloads']}
 if formats!={'BLEND','GLB','OBJ','FBX'}:errors.append('Incomplete formats: '+str(p))
 for f in d['downloads']:
  path=(p.parent/f['file']).resolve()
  if not path.is_relative_to(root.resolve()):errors.append('Path leaves project: '+str(path));continue
  if not path.is_file():errors.append('Missing download: '+str(path));continue
  if path.stat().st_size!=f['bytes']:errors.append('Stale size: '+str(path))
  if f['format']=='GLB':
   with path.open('rb')as stream:
    magic,version,length=struct.unpack('<4sII',stream.read(12))
    if magic!=b'glTF'or version!=2 or length!=path.stat().st_size:errors.append('Invalid GLB header: '+str(path))
  if path.suffix=='.zip':
   with zipfile.ZipFile(path)as z:
    if z.testzip():errors.append('Bad ZIP: '+str(path))
  checked+=1
source=Path(r'C:\Users\HP\Desktop\projects\Sanctuary_kael UPDATED.blend')
original=root/'assets/downloads/sanctuary/sanctuary-original.blend'
if source.exists()and hashlib.sha256(source.read_bytes()).digest()!=hashlib.sha256(original.read_bytes()).digest():errors.append('Original BLEND copy differs from supplied source')
report={'assets':len(manifests),'downloads':checked,'errors':errors,'originalBlendCopyMatches':not any('copy differs'in e for e in errors)}
(root/'design/download-verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
if errors:raise SystemExit(1)
