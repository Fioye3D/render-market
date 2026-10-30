"""Assign portable material colours to the optimized GLB; preserve original BLEND."""
from pathlib import Path
import json,struct
root=Path(__file__).resolve().parents[1];path=root/'assets/downloads/sanctuary/sanctuary-web.glb'
data=path.read_bytes();length,kind=struct.unpack('<II',data[12:20]);doc=json.loads(data[20:20+length]);tail=data[20+length:]
palette={
 'M_Stone_Inscribed_01':[.22,.245,.19,1],
 'M_Stone_Weathered_01':[.245,.265,.225,1],
 'M_Ground_Forest_01':[.075,.09,.037,1],
 'M_Shore_DampEarth_01':[.06,.045,.022,1],
 'M_Lakebed_Silt_01':[.055,.07,.035,1],
 'M_Bark_Detailed_01':[.105,.075,.038,1],
 'M_Foliage_Broadleaf_01':[.045,.115,.022,1],
 'M_Foliage_Broadleaf_02':[.075,.16,.035,1],
 'M_Foliage_UndergrowthDetailed_01':[.045,.11,.018,1],
 'M_Grass_FineMeadow_01':[.105,.14,.035,1],
 'M_Foliage_ClimberDetailed_01':[.04,.095,.02,1],
 'M_Rock_ShoreWet_01':[.13,.15,.12,1],
 'M_Reeds_LakeEdge_01':[.13,.15,.04,1],
 'M_Foliage_Foreground_01':[.035,.085,.018,1],
 'M_Foliage_Foreground_02':[.07,.12,.025,1],
 'M_Water_ForestLake_01':[.035,.085,.06,.82]
}
for m in doc.get('materials',[]):
 if m.get('name')in palette:
  p=m.setdefault('pbrMetallicRoughness',{});p['baseColorFactor']=palette[m['name']]
  if 'Water'in m['name']:p['roughnessFactor']=.24;m['alphaMode']='BLEND';m.pop('extensions',None)
chunk=json.dumps(doc,separators=(',',':')).encode();chunk+=b' '*((-len(chunk))%4)
body=struct.pack('<II',len(chunk),kind)+chunk+tail
path.write_bytes(struct.pack('<4sII',b'glTF',2,len(body)+12)+body)
print('Prepared portable scene material colours.')
