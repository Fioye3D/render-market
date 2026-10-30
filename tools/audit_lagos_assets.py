"""Validate new GLB containers, geometry/material payloads and companion archives."""
from pathlib import Path
import json,struct,zipfile,hashlib
root=Path(__file__).resolve().parents[1]
assets=json.loads((root/'design/lagos-life.json').read_text(encoding='utf-8'))
report=[]
for a in assets:
 folder=root/'assets/downloads/catalogue'/a['file'];m=json.loads((folder/'manifest.json').read_text());p=folder/(a['file']+'.glb');raw=p.read_bytes()
 magic,version,total=struct.unpack_from('<4sII',raw);assert magic==b'glTF' and version==2 and total==len(raw)
 length,kind=struct.unpack_from('<I4s',raw,12);assert kind==b'JSON';g=json.loads(raw[20:20+length])
 bin_start=20+length;bin_length,bin_kind=struct.unpack_from('<I4s',raw,bin_start);assert bin_kind==b'BIN\x00'
 assert bin_length==len(raw)-bin_start-8
 for v in g.get('bufferViews',[]):assert v.get('byteOffset',0)+v['byteLength']<=bin_length
 triangles=0
 for mesh in g['meshes']:
  for prim in mesh['primitives']:
   assert prim.get('mode',4)==4
   pos=g['accessors'][prim['attributes']['POSITION']];assert pos['count']>0
   count=g['accessors'][prim['indices']]['count']if'indices'in prim else pos['count'];assert count%3==0;triangles+=count//3
 for image in g.get('images',[]):assert 'bufferView'in image and image.get('mimeType')in ['image/png','image/jpeg']
 with zipfile.ZipFile(folder/(a['file']+'-obj.zip'))as z:
  assert z.testzip()is None;names=set(z.namelist());mtls=[n for n in names if n.endswith('.mtl')];assert mtls
  refs=[]
  for name in mtls:
   for line in z.read(name).decode('utf-8').splitlines():
    if line.startswith('map_Kd '):
     ref=line[7:].strip().replace('\\','/');assert ref in names,(a['id'],ref);refs.append(ref)
  assert refs,(a['id'],'missing OBJ image maps')
 for f in m['downloads']:
  target=(folder/f['file']).resolve();assert target.is_relative_to(root)and target.is_file()and target.stat().st_size==f['bytes']
 blend=root/'assets/artwork'/(a['file']+'.blend');assert blend.read_bytes()[:7]==b'BLENDER'
 fbx=folder/(a['file']+'.fbx');fbxbytes=fbx.read_bytes();assert fbxbytes.startswith(b'Kaydara FBX Binary')
 assert fbxbytes.count(b'\x89PNG\r\n\x1a\n')==len(g.get('images',[])),(a['id'],'FBX embedded PNG count')
 report.append({'id':a['id'],'title':a['title'],'triangles':triangles,'previewObjects':m['previewObjects'],'embeddedImages':len(g.get('images',[])),'characters':a['characters'],'GLBbytes':len(raw),'GLBsha256':hashlib.sha256(raw).hexdigest(),'files':{f['format']:f['bytes']for f in m['downloads']},'checks':'GLB structure and geometry, embedded images, OBJ texture references and CRC, BLEND/FBX headers, all four paths/sizes pass'})
result={'assets':len(report),'downloads':len(report)*4,'largestGLBbytes':max(x['GLBbytes']for x in report),'assetsUnder8MiB':all(x['GLBbytes']<8*1048576 for x in report),'assetsUnder15MiB':all(x['GLBbytes']<15*1048576 for x in report),'results':report,'limits':'Static validation; not a browser GPU performance test, visual equivalence certification or complete importer conformance test.'}
(root/'design/lagos-asset-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items()if k!='results'},indent=2))
for x in report:print(x['id'],round(x['GLBbytes']/1048576,2),'MiB',x['triangles'],'triangles',x['embeddedImages'],'images')
