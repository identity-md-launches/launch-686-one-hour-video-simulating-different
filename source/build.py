#!/usr/bin/env python3
"""Offline rebuild: Python 3.12, Node, ffmpeg. Bundled fonts, Pillow and speech engine."""
import sys, pathlib, subprocess, json, tempfile, wave, shutil, os, textwrap
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'source/vendor'))
from PIL import Image, ImageDraw, ImageFont
from course import CHAPTERS
OUT=ROOT/'artifacts'; OUT.mkdir(exist_ok=True)
FONT=ROOT/'source/fonts'
def font(s,b=False):return ImageFont.truetype(str(FONT/('LiberationSans-Bold.ttf' if b else 'LiberationSans-Regular.ttf')),s)
def wrap(draw,text,f,width):
 lines=[]; line=''
 for w in text.split():
  trial=(line+' '+w).strip()
  if draw.textlength(trial,font=f)>width and line:lines.append(line);line=w
  else:line=trial
 if line:lines.append(line)
 return lines
cards=[]
for c,(chapter,subtitle,scenes) in enumerate(CHAPTERS):
 for s,(title,body) in enumerate(scenes):cards.append(dict(chapter=chapter,subtitle=subtitle,title=title,body=body,c=c,s=s))
assert len(cards)==120
with tempfile.TemporaryDirectory(prefix='imd-film-') as tmp:
 work=pathlib.Path(tmp)
 (work/'cards.json').write_text(json.dumps(cards))
 for scene in range(len(cards)):
  subprocess.run(['node',str(ROOT/'source/narrate.js'),str(work/'cards.json'),str(work),str(scene)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 stats=[]
 with wave.open(str(work/'audio.wav'),'wb') as output:
  output.setnchannels(1);output.setsampwidth(2);output.setframerate(22050)
  for i,card in enumerate(cards):
   p=work/f'speech-{i:03}.wav'
   with wave.open(str(p),'rb') as w:
    assert w.getframerate()==22050 and w.getsampwidth()==2 and w.getnchannels()==1
    duration=w.getnframes()/22050
   if duration>28:
    q=work/f'adjusted-{i:03}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-af',f'atempo={duration/27.5:.6f}',str(q)],check=True);p=q
   with wave.open(str(p),'rb') as w:data=w.readframes(w.getnframes())
   assert len(data)<=30*22050*2
   output.writeframes(data+b'\0'*(30*22050*2-len(data)))
   stats.append(dict(scene=i+1,original_speech_seconds=round(duration,3),final_speech_seconds=round(len(data)/44100,3)))
 # Render slide plus five-second progress increments. Every visual is original.
 concat=[]
 for i,card in enumerate(cards):
  for tick in range(6):
   im=Image.new('RGB',(1280,720),'#101923');d=ImageDraw.Draw(im)
   teal='#6ee7c8';white='#f3f6fa';muted='#aebdc9'
   d.rectangle((0,0,1280,9),fill=teal)
   d.text((48,31),'IMD / SWARM FIELD GUIDE',font=font(22,True),fill=teal)
   d.text((931,33),'SIMULATED WALKTHROUGH',font=font(18,True),fill=muted)
   d.text((48,90),f'{card["c"]+1:02}  /  {card["chapter"].upper()}',font=font(21,True),fill=muted)
   titlefont=font(42,True)
   for j,line in enumerate(wrap(d,card['title'],titlefont,1130)):d.text((48,133+j*48),line,font=titlefont,fill=white)
   d.rounded_rectangle((47,213,871,580),radius=14,fill='#1c2b3a')
   bodyfont=font(27)
   lines=wrap(d,card['body'],bodyfont,762)
   assert len(lines)<=10,(i,len(lines))
   for j,line in enumerate(lines):d.text((73,239+j*32),line,font=bodyfont,fill=white)
   d.rounded_rectangle((898,213,1231,580),radius=14,outline='#355365',width=2)
   d.text((922,237),'REQUEST JOURNEY',font=font(19,True),fill=teal)
   phase=min(4,card['s']//2)
   for j,label in enumerate(['CHOOSE','DESCRIBE / CHECK','FOLLOW THE WORK','INSPECT OUTCOME','REVISE / PRACTICE']):
    y=285+j*52
    d.ellipse((922,y+3,938,y+19),fill=teal if j==phase else '#355365')
    d.text((950,y),label,font=font(17,True),fill=white if j==phase else muted)
   d.text((922,554),'Examples are not live jobs.',font=font(17),fill=muted)
   for j,line in enumerate(wrap(d,card['subtitle'],font(22),740)):d.text((48,609+j*27),line,font=font(22),fill=teal)
   sec=i*30+tick*5
   d.text((942,610),f'{sec//60:02}:{sec%60:02} / 60:00',font=font(23,True),fill=white)
   d.text((942,643),f'Scene {i+1:03} / 120',font=font(18),fill=muted)
   d.rectangle((48,690,1230,694),fill='#355365');d.rectangle((48,690,48+int(1182*(sec+5)/3600),694),fill=teal)
   p=work/f'frame-{i:03}-{tick}.png';im.save(p)
   concat.extend([f"file '{p}'",'duration 5'])
 concat.append(f"file '{p}'")
 (work/'frames.txt').write_text('\n'.join(concat)+'\n')
 meta=[';FFMETADATA1','title=IMD Swarm Field Guide - One Hour of Simulated Requests','comment=Educational simulation. No live jobs or transactions.']
 for c,(chapter,_,__) in enumerate(CHAPTERS):meta+=['[CHAPTER]','TIMEBASE=1/1000',f'START={c*300000}',f'END={(c+1)*300000}',f'title={chapter}']
 (work/'chapters.txt').write_text('\n'.join(meta)+'\n')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','concat','-safe','0','-i',str(work/'frames.txt'),'-i',str(work/'audio.wav'),'-i',str(work/'chapters.txt'),'-map','0:v','-map','1:a','-map_metadata','2','-map_chapters','2','-t','3600','-r','5','-c:v','libx264','-preset','veryfast','-crf','30','-pix_fmt','yuv420p','-c:a','aac','-b:a','48k','-ar','22050','-ac','1','-movflags','+faststart',str(OUT/'video.mp4')],check=True)
 (ROOT/'source/narration-timing.json').write_text(json.dumps(stats,indent=2)+'\n')
# A full accessible transcript and precise scene navigation.
transcript=['# IMD Swarm Field Guide','', 'Educational simulation. No live jobs, signatures, addresses or payments.','']
for i,card in enumerate(cards):
 if card['s']==0:transcript+=['',f'## {i//2:02}:00 — {card["chapter"]}','']
 t=i*30;transcript += [f'### {t//60:02}:{t%60:02} — {card["title"]}', '',card['body'],'']
(ROOT/'TRANSCRIPT.md').write_text('\n'.join(transcript))
print('Created artifacts/video.mp4: 120 scenes, 3600 seconds',flush=True)
