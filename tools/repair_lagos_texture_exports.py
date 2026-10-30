"""Refresh OBJ/FBX supporting maps from the source's packed image bytes."""
import bpy,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for a in json.loads((root/'design/lagos-life.json').read_text(encoding='utf-8')):
 name=a['file'];out=root/'assets/downloads/catalogue'/name
 bpy.ops.wm.open_mainfile(filepath=str(root/'assets/artwork'/(name+'.blend')),load_ui=False,use_scripts=False)
 bpy.ops.object.select_all(action='DESELECT');keep=[o for o in bpy.context.scene.objects if o.type in {'MESH','CURVE','SURFACE'} and o.name!='Studio floor' and not o.hide_render]
 for o in keep:o.select_set(True)
 bpy.context.view_layer.objects.active=keep[0];bpy.ops.object.convert(target='MESH')
 images={n.image for o in bpy.context.selected_objects for slot in o.material_slots if slot.material and slot.material.use_nodes for n in slot.material.node_tree.nodes if n.type=='TEX_IMAGE' and n.image}
 for image in images:
  target=out/Path(image.filepath).name;assert image.packed_file;target.write_bytes(image.packed_file.data);image.unpack(method='REMOVE');image.filepath=str(target)
 bpy.ops.wm.obj_export(filepath=str(out/(name+'.obj')),export_selected_objects=True,export_materials=True,path_mode='COPY')
 bpy.ops.export_scene.fbx(filepath=str(out/(name+'.fbx')),use_selection=True,object_types={'MESH'},bake_anim=False,path_mode='COPY',embed_textures=True)
 with zipfile.ZipFile(out/(name+'-obj.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
  for p in out.iterdir():
   if p.suffix in {'.obj','.mtl','.png'}:z.write(p,p.name)
 m=json.loads((out/'manifest.json').read_text())
 for f in m['downloads']:f['bytes']=(out/f['file']).stat().st_size
 (out/'manifest.json').write_text(json.dumps(m,indent=2))
 print('TEXTURE_REPAIR_COMPLETE',name,len(images),flush=True)
base=root/'assets/downloads/catalogue';(base/'index.json').write_text(json.dumps({p.parent.name:json.loads(p.read_text())for p in base.glob('*/manifest.json')},indent=2))
