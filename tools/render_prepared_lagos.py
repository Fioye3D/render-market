"""Render saved sources without regenerating geometry or altering source files."""
import bpy,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).parent))
from lagos_scene_kit import frame_render
for name in [x for x in sys.argv[sys.argv.index('--')+1:]if x!='--force']:
 source=root/'assets/artwork'/(name+'.blend');poster=root/'assets/artwork'/(name+'.png')
 if '--force' not in sys.argv and poster.exists() and poster.stat().st_mtime>=source.stat().st_mtime:
  print('Already rendered:',name,flush=True);continue
 bpy.ops.wm.open_mainfile(filepath=str(root/'assets/artwork'/(name+'.blend')),load_ui=False,use_scripts=False)
 bpy.context.scene.cycles.samples=20
 frame_render()
 bpy.context.scene.render.filepath=str(root/'assets/artwork'/(name+'.png'))
 bpy.ops.render.render(write_still=True)
 print('LAGOS_RENDER_COMPLETE',name,flush=True)
