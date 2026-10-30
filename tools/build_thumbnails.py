from pathlib import Path
from PIL import Image,ImageOps
root=Path(__file__).resolve().parents[1];out=root/'assets/thumbnails';out.mkdir(exist_ok=True)
for p in (root/'assets/artwork').glob('*.png'):
 image=Image.open(p).convert('RGB');image.thumbnail((560,420));image.save(out/(p.stem+'.webp'),'WEBP',quality=82,method=6)
print('Prepared',len(list(out.glob('*.webp'))),'lightweight catalogue previews.')
