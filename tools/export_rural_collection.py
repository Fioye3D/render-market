"""Export actual GLB/OBJ/FBX files from the prepared sample Blender studies."""
import bpy,json,os,sys,zipfile,time,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];art=root/'assets/artwork';base=root/'assets/downloads/catalogue';base.mkdir(parents=True,exist_ok=True)
result={}
for source in sorted(art.glob('*.blend')):
 if source.stem not in ['rural-hut', 'rural-village', 'river-landscape', 'royal-courtyard', 'yam-farm', 'cocoa-farm', 'maize-farm', 'mixed-farm', 'cattle-ranch', 'fulani-herdsman', 'courtyard-mosque', 'herbalist-shrine']:continue
 name=source.stem;out=base/name;out.mkdir(exist_ok=True);marker=out/'manifest.json'
 if marker.exists() and marker.stat().st_mtime>=source.stat().st_mtime:result[name]=json.loads(marker.read_text());continue
 print('Exporting catalogue asset',name,flush=True);bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
 bpy.ops.object.select_all(action='DESELECT')
 keep=[o for o in bpy.context.scene.objects if o.type in {'MESH','CURVE','SURFACE'} and o.name!='Studio floor' and not o.hide_render]
 for o in keep:o.select_set(True)
 if not keep:continue
 bpy.context.view_layer.objects.active=keep[0]
 bpy.ops.object.convert(target='MESH')
 # OBJ/FBX need real image paths even when the source BLEND uses packed files.
 images={n.image for o in bpy.context.selected_objects for slot in o.material_slots if slot.material and slot.material.use_nodes for n in slot.material.node_tree.nodes if n.type=='TEX_IMAGE' and n.image}
 for image in images:
  target=out/Path(image.filepath).name
  if image.packed_file:target.write_bytes(image.packed_file.data);image.unpack(method='REMOVE')
  else:
   original=Path(bpy.path.abspath(image.filepath))
   if original.resolve()!=target.resolve():shutil.copy2(original,target)
  image.filepath=str(target)
 def run(op,kwargs):valid=set(op.get_rna_type().properties.keys());op(**{k:v for k,v in kwargs.items()if k in valid})
 run(bpy.ops.export_scene.gltf,dict(filepath=str(out/(name+'.glb')),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_animations=False))
 run(bpy.ops.wm.obj_export,dict(filepath=str(out/(name+'.obj')),export_selected_objects=True,export_materials=True,path_mode='COPY'))
 run(bpy.ops.export_scene.fbx,dict(filepath=str(out/(name+'.fbx')),use_selection=True,object_types={'MESH'},bake_anim=False,path_mode='COPY',embed_textures=True))
 with zipfile.ZipFile(out/(name+'-obj.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
  for p in out.rglob('*'):
   if p.is_file() and p.suffix.lower() in {'.obj','.mtl','.png','.jpg','.jpeg'}:z.write(p,p.relative_to(out).as_posix())
 meta={'downloads':[{'format':'BLEND','file':'../../../artwork/'+source.name,'bytes':source.stat().st_size,'variant':'original study'},{'format':'GLB','file':name+'.glb','bytes':(out/(name+'.glb')).stat().st_size,'variant':'portable export'},{'format':'OBJ','file':name+'-obj.zip','bytes':(out/(name+'-obj.zip')).stat().st_size,'variant':'portable export'},{'format':'FBX','file':name+'.fbx','bytes':(out/(name+'.fbx')).stat().st_size,'variant':'portable export'}],'previewObjects':sum(o.type=='MESH' and o.select_get() for o in bpy.context.scene.objects),'previewPolygons':sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH' and o.select_get()),'previewTriangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH' and o.select_get()),'note':'Portable exports use simplified materials; original procedural materials are retained in BLEND.'}
 if name.startswith('lagos-') and name!='lagos-kiosk' or name=='akara-breakfast-pack':
  meta['note']='Packed image colour maps and portable PBR settings. Static clothed characters where listed; no rigging or animation. Cutaway scenes are intentionally open for inspection.'
  meta['materials']='512px packed image maps; scalar metallic and roughness'
 marker.write_text(json.dumps(meta,indent=2));result[name]=meta
 print('Catalogue export complete:',name,flush=True)
(base/'index.json').write_text(json.dumps(result,indent=2))
