import cv2, numpy as np, pathlib, json, argparse
from PIL import Image,ImageDraw,ImageFont
ap=argparse.ArgumentParser()
ap.add_argument('input_dir',help='Folder holding the extracted six MP4 files')
ap.add_argument('--out',default='video_probe_output',help='Output directory for probe JSON and contact sheets')
a=ap.parse_args()
base=pathlib.Path(a.input_dir)
outdir=pathlib.Path(a.out)
outdir.mkdir(parents=True,exist_ok=True)
vids=sorted(base.glob('*.mp4'))
fp=[1,100,200,300,400,500,600,700,800,900,975,999]
res={}
for p in vids:
 cap=cv2.VideoCapture(str(p));n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=cap.get(cv2.CAP_PROP_FPS);w=int(cap.get(3));h=int(cap.get(4))
 black=[]; bright=[]; imgs={}; nread=0
 while True:
  ok,im=cap.read()
  if not ok:break
  level=float(np.mean(im));mx=int(np.max(im));bright.append(level)
  if mx<12 or level<2: black.append(nread)
  if nread in (fp+[i+1 for i in fp if i<999]+[0,2,3,4]):imgs[nread]=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
  nread+=1
 cap.release()
 res[p.name]={'frames_header':n,'decoded':nread,'fps':fps,'resolution':[w,h],'black_frame_count':len(black),'black_sample_first':black[:20], 'black_sample_last':black[-20:],'black_parity':{'even':sum(i%2==0 for i in black),'odd':sum(i%2==1 for i in black)},'min_brightness':min(bright),'median_brightness':float(np.median(bright)), 'mean_brightness':float(np.mean(bright))}
 def montage(indices, dst):
  cell=(410,245);title=28;sheet=Image.new('RGB',(cell[0]*4,(cell[1]+title)*3),(25,25,25)); d=ImageDraw.Draw(sheet)
  for k,i in enumerate(indices):
   if i not in imgs:continue
   f=Image.fromarray(imgs[i]);f.thumbnail(cell);x=(k%4)*cell[0];y=(k//4)*(cell[1]+title)
   sheet.paste(f,(x,y+title));d.text((x+8,y+6),f'{p.name} | f={i} t={i/fps:.2f}s',fill=(240,240,240))
  sheet.save(outdir/dst,quality=87)
 montage(fp, p.stem+'_overview.jpg')
 montage([i+1 if i<999 else i for i in fp],p.stem+'_adjacent.jpg')
 print(p.name,res[p.name])
(outdir/'video_probe.json').write_text(json.dumps(res,indent=2,ensure_ascii=False))
