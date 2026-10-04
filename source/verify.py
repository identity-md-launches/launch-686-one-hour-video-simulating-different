#!/usr/bin/env python3
"""Inspect the finished deliverable and persist reproducible check evidence."""
import sys,json,pathlib,subprocess,tempfile,hashlib,struct
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'source/vendor'))
from PIL import Image,ImageDraw,ImageFont
video=ROOT/'artifacts/video.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(video)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
assert (v['width'],v['height'])==(1280,720)
assert a['codec_name']=='aac' and a['channels']==1
assert abs(float(probe['format']['duration'])-3600)<.1
assert len(probe['chapters'])==12
assert video.stat().st_size<64*1024*1024
atoms=[]
with video.open('rb') as f:
 while True:
  pos=f.tell();header=f.read(8)
  if len(header)<8:break
  size,kind=struct.unpack('>I4s',header)
  if size==1:size=struct.unpack('>Q',f.read(8))[0]
  if size==0:size=video.stat().st_size-pos
  atoms.append(dict(type=kind.decode('ascii'),offset=pos,size=size));f.seek(pos+size)
assert next(x['offset'] for x in atoms if x['type']=='moov')<next(x['offset'] for x in atoms if x['type']=='mdat')
# Decode the complete MP4: container assertions alone cannot reveal broken packets.
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
# Audio measurement across the entire hour, saved for independent review.
audio=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vn','-af','volumedetect','-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
audio_lines=[l for l in audio.stderr.splitlines() if 'mean_volume:' in l or 'max_volume:' in l]
assert len(audio_lines)==2
with tempfile.TemporaryDirectory(prefix='imd-check-') as tmp:
 sheet=Image.new('RGB',(960,660),'#101923');draw=ImageDraw.Draw(sheet)
 font=ImageFont.truetype(str(ROOT/'source/fonts/LiberationSans-Regular.ttf'),16)
 for c in range(12):
  frame=pathlib.Path(tmp)/f'{c}.png'
  subprocess.run(['ffmpeg','-v','error','-ss',str(c*300+1),'-i',str(video),'-frames:v','1','-vf','scale=320:180',str(frame)],check=True)
  x=(c%3)*320;y=(c//3)*165
  with Image.open(frame) as im:sheet.paste(im.resize((288,162)),(x+16,y))
 sheet.save(ROOT/'source/preview.jpg',quality=88)
result={'file':'artifacts/video.mp4','bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'probe':probe,'top_level_mp4_atoms':atoms,'complete_decode':'passed','audio_measurements':audio_lines,'contact_sheet':'source/preview.jpg','checks':'Codecs, pixel format, dimensions, duration, chapter count, size, moov-before-mdat and complete decoding passed.'}
(ROOT/'source/verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'bytes':result['bytes'],'duration':probe['format']['duration'],'video':v['codec_name'],'audio':a['codec_name'],'audio_measurements':audio_lines,'checks':'passed'},indent=2))
