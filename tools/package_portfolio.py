"""Package the local portfolio, including real downloads and licence notices."""
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root.parent/'output';out.mkdir(exist_ok=True)
skip={'assets/downloads/sanctuary/sanctuary.obj','assets/downloads/sanctuary/sanctuary.mtl','assets/downloads/sanctuary/sanctuary.fbx'}
files=[p for p in root.rglob('*')if p.is_file()and not any(v in p.relative_to(root).parts for v in ('.git','__pycache__','node_modules'))and p.relative_to(root).as_posix()not in skip and not p.name.endswith(('.pyc','.blend1','.log')) and not ('downloads/catalogue/' in p.as_posix() and p.suffix in {'.obj','.mtl'})]
target=out/'RenderMarket_Portfolio_v0.4.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=4)as z:
 for p in files:z.write(p,root.name+'/'+p.relative_to(root).as_posix())
print('Packaged',len(files),'files;',round(target.stat().st_size/1048576,1),'MB;',target)
