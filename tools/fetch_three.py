"""Vendor the browser renderer from the official npm registry; no package scripts run."""
from pathlib import Path
import urllib.request,json,tarfile,io
root=Path(__file__).resolve().parents[1];out=root/'prototype/vendor/three';out.mkdir(parents=True,exist_ok=True)
meta=json.load(urllib.request.urlopen('https://registry.npmjs.org/three/latest'))
data=urllib.request.urlopen(meta['dist']['tarball']).read()
with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz')as archive:
 for name in ['build/three.module.js','build/three.core.js','examples/jsm/loaders/GLTFLoader.js','examples/jsm/controls/OrbitControls.js','examples/jsm/utils/BufferGeometryUtils.js','examples/jsm/utils/SkeletonUtils.js','examples/jsm/environments/RoomEnvironment.js','LICENSE']:
  member=archive.getmember('package/'+name);dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(archive.extractfile(member).read())
(out/'version.json').write_text(json.dumps({'package':'three','version':meta['version'],'source':meta['dist']['tarball'],'license':'MIT'},indent=2))
print('Vendored three',meta['version'])
