"""Package all authored code, catalogue data and documentation without large media."""
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root.parent/'output';out.mkdir(exist_ok=True)
extensions={'.py','.js','.cjs','.html','.css','.md','.json','.txt','.toml','.yml','.yaml'}
excluded={'design/rendermarket.figmadraft.json'}
files=[p for p in root.rglob('*')if p.is_file() and not any(v in p.relative_to(root).parts for v in ('.git','__pycache__','node_modules','downloads','vendor'))and p.relative_to(root).as_posix()not in excluded and(p.suffix in extensions or p.name in {'LICENSE','.gitignore'})]
# Include the bundled viewer's code/licence and original font/base-mesh notices.
files+=list((root/'prototype/vendor/three').rglob('*.js'))+[root/'prototype/vendor/three/LICENSE']
files+=list((root/'assets/vendor/makehuman').glob('*.md'))
files+=list((root/'assets/logo').glob('*.svg'))
target=out/'RenderMarket_Code_v0.4.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(set(files)):z.write(p,root.name+'/'+p.relative_to(root).as_posix())
 z.writestr('READ-ME-FIRST.txt','RENDERMARKET CODE PACKAGE\n\nAll authored HTML, CSS, JavaScript, Python tools, catalogue JSON and project documentation are included, plus the locally bundled Three.js code and licence notices.\n\nThis is the code-only archive. Fonts, rendered images, generated SVG/image payloads, human mesh, editable Blender scenes and downloadable 3D assets are in RenderMarket_Portfolio_v0.4.zip. Use the complete archive for the working visual prototype.\n\nUnzip the archive before adding its contents to your GitHub repository. Do not upload the ZIP as the only repository file.\n\nThe project is a new independent UI/UX portfolio study with disclosed Codex assistance, separate from the Access Forge competition proposal. Figma account import and public hosting are not completed.\n')
with zipfile.ZipFile(target)as z:assert z.testzip()is None
print('Packaged',len(set(files)),'code/documentation files;',round(target.stat().st_size/1048576,2),'MiB;',target)
