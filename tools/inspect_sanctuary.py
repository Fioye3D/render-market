"""Read-only inspection; run with Blender --disable-autoexec."""
import bpy,json,os
from pathlib import Path
out=Path(__file__).resolve().parents[2]/'working/sanctuary-inspection.json'
meshes=[o for o in bpy.data.objects if o.type=='MESH']
data={
 'blenderVersion':list(bpy.data.version),
 'objects':len(bpy.data.objects),'meshes':len(meshes),
 'vertices':sum(len(o.data.vertices)for o in meshes),
 'polygons':sum(len(o.data.polygons)for o in meshes),
 'sceneObjects':len(bpy.context.scene.objects),
 'cameras':[dict(name=o.name,location=list(o.location),rotation=list(o.rotation_euler),focalLength=o.data.lens)for o in bpy.data.objects if o.type=='CAMERA'],
 'images':[dict(name=i.name,path=bpy.path.abspath(i.filepath),packed=bool(i.packed_file),exists=os.path.isfile(bpy.path.abspath(i.filepath)),size=list(i.size))for i in bpy.data.images if i.source=='FILE'],
 'collections':[dict(name=c.name,objects=len(c.objects),hidden=c.hide_render)for c in bpy.data.collections],
 'largestMeshes':sorted([dict(name=o.name,polygons=len(o.data.polygons),vertices=len(o.data.vertices),instances=o.instance_type,hidden=o.hide_render,modifiers=[m.type for m in o.modifiers])for o in meshes],key=lambda o:o['polygons'],reverse=True)[:30],
 'nodeGroups':[g.name for g in bpy.data.node_groups],
 'materials':len(bpy.data.materials),
 'world':bpy.context.scene.world.name if bpy.context.scene.world else None,
 'sceneBounds':[list(bpy.context.scene.camera.location)] if bpy.context.scene.camera else [],
}
out.write_text(json.dumps(data,indent=2),encoding='utf-8')
print('INSPECTION:',json.dumps({k:data[k]for k in ['blenderVersion','objects','meshes','vertices','polygons','sceneObjects','materials']}),flush=True)
