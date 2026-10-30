from pathlib import Path
import json,base64
root=Path(__file__).resolve().parents[1]
scenes=json.loads((root/'design/scenes.json').read_text(encoding='utf-8'))
names={n['file'] for s in scenes for n in s['nodes'] if n['type']=='image'}
payload={'format':'rendermarket.figmadraft','version':1,'scenes':scenes,'tokens':json.loads((root/'design/design-tokens.json').read_text()),'images':{n:base64.b64encode((root/'assets/artwork'/f'{n}.png').read_bytes()).decode() for n in names}}
(root/'design/rendermarket.figmadraft.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
print('Packaged',len(scenes),'artboards and',len(names),'original images. This is an import payload, not a .fig file.')
