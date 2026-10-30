"""Download open-source fonts and their licence notices from Google Fonts."""
from pathlib import Path
import urllib.request

out=Path(__file__).resolve().parents[1]/'assets/fonts'
out.mkdir(parents=True,exist_ok=True)
files={
 'Inter.ttf':'inter/Inter%5Bopsz,wght%5D.ttf',
 'SpaceGrotesk.ttf':'spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf',
 'Inter-OFL.txt':'inter/OFL.txt',
 'SpaceGrotesk-OFL.txt':'spacegrotesk/OFL.txt'
}
for name,path in files.items():
 urllib.request.urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/'+path,out/name)
 print('Saved',name)
