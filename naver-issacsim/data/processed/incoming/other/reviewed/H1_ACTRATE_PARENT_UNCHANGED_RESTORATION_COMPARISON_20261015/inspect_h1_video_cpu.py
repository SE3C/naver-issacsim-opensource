#!/usr/bin/env python
"""Decode provided original MP4s on CPU; no rendering or input modifications."""
from pathlib import Path
from collections import Counter
import cv2,numpy as np, csv, time
from PIL import Image,ImageDraw,ImageFont
import argparse
parser=argparse.ArgumentParser(description='CPU-decode all 18 H1 videos extracted from the three original nested ZIPs')
parser.add_argument('--extracted-root',required=True,type=Path,help='Directory containing A/B/C folders with original MP4s')
parser.add_argument('--output',required=True,type=Path)
args=parser.parse_args()
ROOT=args.extracted_root
OUT=args.output; OUT.mkdir(parents=True,exist_ok=True)
SLOTS=[0,0.5,1,1.5,2,2.5,3,4,5,6,7,8,10,12,15,18,19.5]
FRAMES=sorted({min(999,int(round(t*50))) for t in SLOTS}|{min(999,int(round(t*50))+1) for t in SLOTS})
files=['01_stairs.mp4','02_inverted_stairs.mp4','03_boxes.mp4','04_random_rough.mp4','05_slope_up_10deg.mp4','06_slope_down_10deg.mp4']
records=[]; sampled={}
for f in files:
 for p in 'ABC':
  cap=cv2.VideoCapture(str(ROOT/p/f));assert cap.isOpened()
  fps=cap.get(cv2.CAP_PROP_FPS); nf=cap.get(cv2.CAP_PROP_FRAME_COUNT)
  black=[0,0]; total=[0,0]; saved={}; usable=[];first_visible=None;last_visible=None
  for i in range(int(nf)):
   ret,frame=cap.read()
   if not ret:break
   # mean BGR light on small spatial sampling; all black captures are near zero
   lum=float(frame[::25,::25,:].mean())
   b=lum<4.0
   total[i%2]+=1;black[i%2]+=int(b)
   if not b:
    first_visible = i if first_visible is None else first_visible
    last_visible=i
   if i in FRAMES:
    small=cv2.resize(frame,(320,180),interpolation=cv2.INTER_AREA)
    saved[i]=(cv2.cvtColor(small,cv2.COLOR_BGR2RGB),lum,b)
  cap.release()
  sampled[(p,f)]=saved
  records.append(dict(policy=p,filename=f,frame_count=int(nf),fps=fps,decoded=i+1,black_even=black[0],black_odd=black[1],all_black=sum(black),visible=int(nf)-sum(black),first_visible_frame=first_visible,last_visible_frame=last_visible))
  print(p,f,'decoded',i+1,'blacks',black,flush=True)
 for block,ts in [('early',SLOTS[:12]),('late',SLOTS[12:])]:
  CW,CH=320,180; head=29; left=22; n=len(ts)
  sheet=Image.new('RGB',(left+CW*n,head+(CH+20)*3),'white')
  draw=ImageDraw.Draw(sheet)
  for j,t in enumerate(ts):draw.text((left+j*CW+8,7),f'{t:.1f}s',fill='black')
  for row,p in enumerate('ABC'):
   draw.text((4,head+row*(CH+20)+6),p,fill='black')
   for j,t in enumerate(ts):
    idx=int(round(t*50)); idx2=min(999,idx+1)
    sm=sampled[(p,f)]
    frame,lum,isblack=sm[idx]
    show=idx
    if isblack and idx2 in sm and not sm[idx2][2]:frame,lum,isblack=sm[idx2];show=idx2
    x,y=left+j*CW,head+row*(CH+20)
    sheet.paste(Image.fromarray(frame),(x,y));draw.text((x+6,y+CH+1),f'#{show} '+('BLACK' if isblack else 'valid'),fill='red' if isblack else 'black')
  sheet.save(OUT/f'{f[:-4]}_{block}.jpg',quality=81)
with (OUT/'decode_audit.csv').open('w',newline='') as o:
 w=csv.DictWriter(o,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
