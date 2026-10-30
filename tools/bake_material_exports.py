"""Bake base colour for the three procedural textile studies into portable exports."""
import bpy,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for name in ['aso-oke-stripes','kente-strip-study','woven-mat']:
 print('Baking portable material',name,flush=True)
 source=root/'assets/artwork'/f'{name}.blend';out=root/'assets/downloads/catalogue'/name
 bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=1
 bpy.ops.object.select_all(action='DESELECT');objects=[o for o in scene.objects if o.type in {'MESH','CURVE'}and o.name!='Studio floor'and not o.hide_render]
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.convert(target='MESH')
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.02);bpy.ops.object.mode_set(mode='OBJECT')
 image=bpy.data.images.new('Portable base colour',1024,1024);mats={m for o in bpy.context.selected_objects for m in o.data.materials if m and m.use_nodes}
 for m in mats:
  for n in m.node_tree.nodes:n.select=False
  node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;node.select=True;m.node_tree.nodes.active=node
 bpy.ops.object.bake(type='DIFFUSE',pass_filter={'COLOR'},use_clear=True,margin=6)
 image.filepath_raw=str(out/(name+'-basecolor.png'));image.file_format='PNG';image.save();image.pack()
 for m in mats:
  node=m.node_tree.nodes.active;p=m.node_tree.nodes.get('Principled BSDF')
  if p:m.node_tree.links.new(node.outputs['Color'],p.inputs['Base Color'])
 bpy.ops.export_scene.gltf(filepath=str(out/(name+'.glb')),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_animations=False)
 bpy.ops.wm.obj_export(filepath=str(out/(name+'.obj')),export_selected_objects=True,export_materials=True,path_mode='RELATIVE')
 bpy.ops.export_scene.fbx(filepath=str(out/(name+'.fbx')),use_selection=True,object_types={'MESH'},bake_anim=False,path_mode='COPY',embed_textures=True)
 with zipfile.ZipFile(out/(name+'-obj.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
  for file in [name+'.obj',name+'.mtl',name+'-basecolor.png']:z.write(out/file,file)
 meta=json.loads((out/'manifest.json').read_text());meta['bakedBaseColour']=True
 for f in meta['downloads']:
  if f['format']!='BLEND':f['bytes']=(out/f['file']).stat().st_size
 (out/'manifest.json').write_text(json.dumps(meta,indent=2));print('Baked material export ready:',name,flush=True)
