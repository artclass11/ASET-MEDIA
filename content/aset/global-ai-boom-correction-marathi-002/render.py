#!/usr/bin/env python3
"""Render ASET 002: Marathi narration + original editorial graphic cards."""
import re, subprocess, pathlib, json
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "render"
OUT.mkdir(exist_ok=True)
W,H = 1920,1080
FONT_PATH = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
BOLD_PATH = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"
if not pathlib.Path(FONT_PATH).exists():
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not pathlib.Path(BOLD_PATH).exists():
    BOLD_PATH = FONT_PATH
font_title = ImageFont.truetype(BOLD_PATH, 72)
font_small = ImageFont.truetype(FONT_PATH, 25)

script = (ROOT / "script_mr.md").read_text(encoding="utf-8")
chapters=[]
current=None
for raw in script.splitlines():
    line=raw.strip()
    if line.startswith("### "):
        if current and current["text"].strip(): chapters.append(current)
        current={"title": re.sub(r"^###\s*\d+:?\s*", "", line), "text": ""}
    elif current and line and not line.startswith("#") and not line.startswith("**"):
        current["text"] += line + " "
if current and current["text"].strip(): chapters.append(current)
if len(chapters) < 8:
    raise SystemExit(f"Expected at least 8 chapters, got {len(chapters)}")

def run(cmd):
    subprocess.run(cmd, check=True)

def wrap(draw, text, font, max_width):
    words=text.split(); lines=[]; line=""
    for word in words:
        trial=(line+" "+word).strip()
        if draw.textbbox((0,0), trial, font=font)[2] <= max_width:
            line=trial
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    return lines

audio_files=[]; scene_files=[]; subtitle_entries=[]
cursor=0.0
palette=[(11,18,24),(14,22,31),(18,23,31),(12,25,30),(19,24,33)]
for i,ch in enumerate(chapters,1):
    text=ch["text"].strip()
    audio=OUT/f"voice_{i:02d}.mp3"
    chunks=re.split(r"(?<=[।!?])\s+", text)
    pieces=[]
    for j,chunk in enumerate(chunks):
        if chunk.strip():
            p=OUT/f"part_{i:02d}_{j:02d}.mp3"
            gTTS(text=chunk.strip(), lang="mr", slow=False).save(str(p))
            pieces.append(p)
    concat_txt=OUT/f"audio_{i:02d}.txt"
    concat_txt.write_text("".join(f"file '{p.as_posix()}'\n" for p in pieces),encoding="utf-8")
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat_txt),"-c","copy",str(audio)])
    for p in pieces: p.unlink(missing_ok=True)
    audio_files.append(audio)
    duration=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(audio)],text=True).strip())
    im=Image.new("RGB",(W,H),palette[(i-1)%len(palette)])
    d=ImageDraw.Draw(im)
    for x in range(0,W,120): d.line((x,0,x,H),fill=(26,37,46),width=1)
    for y in range(0,H,120): d.line((0,y,W,y),fill=(26,37,46),width=1)
    d.rectangle((130,145,139,920),fill=(91,164,151))
    d.text((175,145),"ASET  /  GLOBAL MARKETS",font=font_small,fill=(148,185,177))
    y=310
    for ln in wrap(d,ch["title"],font_title,1500)[:3]:
        d.text((175,y),ln,font=font_title,fill=(242,245,242))
        y+=100
    d.text((175,760),f"CHAPTER {i:02d}   •   MARATHI DOCUMENTARY",font=font_small,fill=(170,184,190))
    d.text((175,820),"AI BOOM  /  MARKET CORRECTION  /  FINANCIAL RISK",font=font_small,fill=(120,151,153))
    d.text((175,950),"ASET  •  EDUCATIONAL MARKET ANALYSIS",font=font_small,fill=(112,130,139))
    scene=OUT/f"scene_{i:02d}.png"; im.save(scene)
    scene_files.append((scene,duration))
    sentences=[s.strip() for s in re.split(r"(?<=[।!?])\s+",text) if s.strip()]
    total=max(1,sum(len(s) for s in sentences)); local=cursor
    for s in sentences:
        seg=duration*len(s)/total
        subtitle_entries.append((local,local+seg,s)); local+=seg
    cursor+=duration

audio_list=OUT/"audio_all.txt"
audio_list.write_text("".join(f"file '{p.as_posix()}'\n" for p in audio_files),encoding="utf-8")
full_audio=OUT/"narration_mr.mp3"
run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(audio_list),"-c","copy",str(full_audio)])
scene_list=OUT/"scenes.txt"
scene_list.write_text("".join(f"file '{p.as_posix()}'\nduration {dur:.3f}\n" for p,dur in scene_files)+f"file '{scene_files[-1][0].as_posix()}'\n",encoding="utf-8")
def stamp(t):
    ms=int(round(t*1000)); h=ms//3600000; ms%=3600000; m=ms//60000; ms%=60000; sec=ms//1000; ms%=1000
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"
srt=[]
for n,(a,b,txt) in enumerate(subtitle_entries,1):
    srt.append(f"{n}\n{stamp(a)} --> {stamp(b)}\n{txt}\n")
(OUT/"captions_mr.srt").write_text("\n".join(srt),encoding="utf-8")
video=OUT/"ASET_Global_AI_Boom_Market_Correction_Marathi_002.mp4"
run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(scene_list),"-i",str(full_audio),"-vf","scale=1920:1080,format=yuv420p","-r","25","-c:v","libx264","-preset","veryfast","-crf","23","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",str(video)])
thumb=OUT/"ASET_Global_AI_Boom_Market_Correction_Marathi_002_thumbnail.jpg"
im=Image.open(scene_files[0][0]).convert("RGB")
d=ImageDraw.Draw(im)
d.rectangle((130,120,1790,900),outline=(91,164,151),width=5)
d.text((175,600),"AI बूम की आर्थिक फुगा?",font=font_title,fill=(245,246,241))
im.save(thumb,quality=92)
duration=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(video)],text=True).strip())
streams=subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height","-of","json",str(video)],text=True)
info={"duration_seconds":round(duration,2),"chapters":len(chapters),"video_bytes":video.stat().st_size,"audio_bytes":full_audio.stat().st_size,"streams":json.loads(streams),"narration":"Google gTTS Marathi (unofficial free endpoint)","thumbnail_bytes":thumb.stat().st_size}
(OUT/"render_report.json").write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding="utf-8")
if duration < 540 or duration > 720: raise SystemExit(f"Runtime outside 9-12 minute acceptance band: {duration:.1f}s")
if video.stat().st_size < 5_000_000: raise SystemExit("Rendered video unexpectedly small")
print(json.dumps(info,ensure_ascii=False,indent=2))
