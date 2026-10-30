"""Regenerate portable OBJ/FBX files from the corrected web scene."""
import bpy,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'assets/downloads/sanctuary'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(out/'sanctuary-web.glb'))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.obj_export(filepath=str(out/'sanctuary.obj'),export_selected_objects=True,export_materials=True,path_mode='RELATIVE')
bpy.ops.export_scene.fbx(filepath=str(out/'sanctuary.fbx'),use_selection=True,object_types={'MESH'},bake_anim=False)
for kind in ['obj','fbx']:
 with zipfile.ZipFile(out/f'sanctuary-{kind}.zip','w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
  z.write(out/f'sanctuary.{kind}',f'sanctuary.{kind}')
  if kind=='obj':z.write(out/'sanctuary.mtl','sanctuary.mtl')
meta=json.loads((out/'manifest.json').read_text())
for f in meta['downloads']:f['bytes']=(out/f['file']).stat().st_size
meta['preview']='Reduced geometry and vegetation; portable material colours. Original Blender materials retained in the original source.'
(out/'manifest.json').write_text(json.dumps(meta,indent=2))
print('Portable Sanctuary formats refreshed.',flush=True)
