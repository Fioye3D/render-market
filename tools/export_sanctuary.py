"""Export a reduced web scene without modifying the supplied Blender source file."""
import bpy,sys,os,json,math,shutil,zipfile,re,time
from pathlib import Path
from collections import defaultdict
root=Path(__file__).resolve().parents[1];out=root/'assets/downloads/sanctuary';out.mkdir(parents=True,exist_ok=True)
source=Path(bpy.data.filepath);shutil.copyfile(source,out/'sanctuary-original.blend')
start=time.time();scene=bpy.context.scene
hidden=set()
def collect_hidden(c,parent=False):
 bad=parent or c.hide_render
 if bad:hidden.update(o.name for o in c.all_objects)
 for child in c.children:collect_hidden(child,bad)
collect_hidden(scene.collection)
limits={'COL_Undergrowth':110,'COL_Trees':56,'COL_ReferenceBackgroundForest':14,'COL_DistantForest':8,'COL_ShoreVegetation':24,'COL_BankVegetation':24}
omit=set()
for name,limit in limits.items():
 c=bpy.data.collections.get(name)
 if not c:continue
 objects=sorted(list(c.objects),key=lambda o:o.name)
 keep={objects[min(len(objects)-1,int(i*len(objects)/limit))].name for i in range(min(limit,len(objects)))}
 omit.update(o.name for o in objects if o.name not in keep)
selected=[o for o in scene.objects if o.type=='MESH' and not o.hide_render and o.name not in hidden and o.name not in omit and not any(k in o.name.lower() for k in ['cutter','sky','volume','referenceimage'])]
print('Selected',len(selected),'of',len(scene.objects),'objects for the browser export',flush=True)
bpy.ops.object.select_all(action='DESELECT')
groups=defaultdict(list)
for o in selected:groups[o.data.name].append(o)
for index,(key,objects)in enumerate(groups.items()):
 o=objects[0];o.data=o.data.copy();bpy.context.view_layer.objects.active=o;o.select_set(True)
 # Preserve existing mesh geometry and skip bevel amplification for the web copy.
 for mod in list(o.modifiers):o.modifiers.remove(mod)
 faces=len(o.data.polygons);target=12000 if any(k in o.name.lower()for k in ['arch','rock','ground'])else 3500
 if faces>target:
  mod=o.modifiers.new('Web preview reduction','DECIMATE');mod.ratio=max(.015,target/faces)
  try:bpy.ops.object.modifier_apply(modifier=mod.name)
  except RuntimeError:pass
 mesh=o.data
 for other in objects[1:]:
  other.data=mesh
  for mod in list(other.modifiers):other.modifiers.remove(mod)
 o.select_set(False)
 if index%25==0:print('Reduced mesh groups',index,'/',len(groups),flush=True)
for o in selected:o.select_set(True)
bpy.context.view_layer.objects.active=selected[0]
# Use the diffuse image already in the file where possible. Procedural shading remains
# available in the original .blend; GLB/OBJ/FBX materials are simplified for portability.
texdir=out/'textures';texdir.mkdir(exist_ok=True)
for im in bpy.data.images:
 if im.source!='FILE' or not im.has_data:continue
 try:
  if max(im.size)>1024:im.scale(max(1,int(im.size[0]*1024/max(im.size))),max(1,int(im.size[1]*1024/max(im.size))))
  name=re.sub(r'[^a-zA-Z0-9_-]','_',im.name)+'.png';im.filepath_raw=str(texdir/name);im.file_format='PNG';im.save();im.pack()
 except Exception as error:print('Texture note',im.name,str(error),flush=True)
def export(op,settings):
 valid=set(op.get_rna_type().properties.keys());filtered={k:v for k,v in settings.items()if k in valid};return op(**filtered)
print('Exporting GLB',flush=True)
export(bpy.ops.export_scene.gltf,dict(filepath=str(out/'sanctuary-web.glb'),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_materials='EXPORT',export_animations=False,export_extras=False,export_yup=True))
print('Exporting OBJ',flush=True)
export(bpy.ops.wm.obj_export,dict(filepath=str(out/'sanctuary.obj'),export_selected_objects=True,export_materials=True,path_mode='RELATIVE',apply_modifiers=True))
print('Exporting FBX',flush=True)
export(bpy.ops.export_scene.fbx,dict(filepath=str(out/'sanctuary.fbx'),use_selection=True,object_types={'MESH'},path_mode='COPY',embed_textures=True,bake_anim=False,use_mesh_modifiers=True))
for kind in ['obj','fbx']:
 with zipfile.ZipFile(out/f'sanctuary-{kind}.zip','w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
  for p in out.glob(f'*.{kind}'):z.write(p,p.name)
  if kind=='obj':
   for p in out.glob('*.mtl'):z.write(p,p.name)
  for p in texdir.glob('*'):z.write(p,'textures/'+p.name)
meta={'title':'Sanctuary Temple','source':'User-supplied Sanctuary_kael UPDATED.blend','originalBytes':source.stat().st_size,'preview':'Reduced geometry and vegetation; simplified portable materials. Original Blender scene is provided separately.','previewObjects':len(selected),'previewPolygons':sum(len(o.data.polygons)for o in selected),'originalPolygonsBeforeReduction':13889170,'elapsedSeconds':round(time.time()-start),'camera':{'position':[0,4.5,26],'target':[0,2.5,0]},'downloads':[]}
for label,name in [('BLEND','sanctuary-original.blend'),('GLB','sanctuary-web.glb'),('OBJ','sanctuary-obj.zip'),('FBX','sanctuary-fbx.zip')]:
 p=out/name
 if p.exists():meta['downloads'].append({'format':label,'file':name,'bytes':p.stat().st_size,'variant':'original source'if label=='BLEND'else'optimized export'})
(out/'manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8');print('SANCTUARY EXPORT COMPLETE',json.dumps(meta),flush=True)
