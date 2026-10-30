"""Original procedural sample artwork. Run with Blender 4.2 in background mode."""
import bpy, math, os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'artwork')
os.makedirs(OUT, exist_ok=True)

def mat(name, color, metallic=0, rough=.38):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metallic; p.inputs['Roughness'].default_value=rough
    return m

def cube(name,loc,scale,m,bevel=.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name
    o.dimensions=scale; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(m)
    if bevel:
        mod=o.modifiers.new('Soft manufactured edges','BEVEL'); mod.width=bevel; mod.segments=3
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

def cyl(name,loc,r,d,m,rotation=None,vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=d, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(m)
    if rotation:o.rotation_euler=rotation
    b=o.modifiers.new('Edge highlights','BEVEL'); b.width=.025; b.segments=3
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL'); return o

def sphere(name,loc,scale,m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(m)
    for p in o.data.polygons:p.use_smooth=True
    return o

def tube(name,points,r,m):
    c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.bevel_depth=r; c.bevel_resolution=4
    s=c.splines.new('POLY'); s.points.add(len(points)-1)
    for p,v in zip(s.points,points): p.co=(*v,1)
    o=bpy.data.objects.new(name,c); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o

def light(loc,power,size,color):
    bpy.ops.object.light_add(type='AREA', location=loc); o=bpy.context.object
    o.data.energy=power; o.data.shape='DISK'; o.data.size=size; o.data.color=color
    o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()

def reset(bg=(.08,.10,.12),camera=(6,-8,6),target=(0,0,1),ortho=6.3):
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.samples=20; s.cycles.use_denoising=True
    s.render.resolution_x=960; s.render.resolution_y=720; s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG'; s.world.color=(.24,.24,.24)
    s.view_settings.view_transform='AgX'
    ground=mat('Studio backdrop',bg,rough=.65); cube('Studio floor',(0,0,-.14),(200,200,.2),ground,0)
    bpy.ops.object.camera_add(location=camera); cam=bpy.context.object
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=ortho; s.camera=cam
    light((1,-4,7),1000,5,(1,.82,.65)); light((-4,-1,4),650,4,(.58,.72,1)); light((3,4,6),1400,3,(1,.66,.4))
    return s

def save(name):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,name+'.blend'))
    bpy.context.scene.render.filepath=os.path.join(OUT,name+'.png'); bpy.ops.render.render(write_still=True)
    print('RENDERMARKET RENDER FINISHED:',name,flush=True)


