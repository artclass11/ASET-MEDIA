#!/usr/bin/env python3
"""Technical release gate for ASET renders. Creative quality is scored separately."""
import json, pathlib, subprocess, sys, re
root=pathlib.Path(__file__).parent/"render"
video=root/"ASET_Global_AI_Boom_Market_Correction_Marathi_002.mp4"
thumb=root/"ASET_Global_AI_Boom_Market_Correction_Marathi_002_thumbnail.jpg"
srt=root/"captions_mr.srt"
report=root/"render_report.json"
errors=[]; checks={}
def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],text=True))
for p in (video,thumb,srt,report):
    checks[p.name]={"exists":p.exists(),"bytes":p.stat().st_size if p.exists() else 0}
    if not p.exists() or p.stat().st_size==0: errors.append(f"Missing/empty deliverable: {p.name}")
if video.exists() and video.stat().st_size:
    data=probe(video); streams=data.get("streams",[]); fmt=data.get("format",{})
    v=next((x for x in streams if x.get("codec_type")=="video"),None)
    a=next((x for x in streams if x.get("codec_type")=="audio"),None)
    duration=float(fmt.get("duration",0))
    checks["duration_seconds"]=round(duration,2)
    checks["video_codec"]=v.get("codec_name") if v else None
    checks["audio_codec"]=a.get("codec_name") if a else None
    checks["resolution"]=f'{v.get("width")}x{v.get("height")}' if v else None
    if not v: errors.append("No video stream")
    if not a: errors.append("No audio stream")
    if v and (v.get("width")!=1920 or v.get("height")!=1080): errors.append("Video must be 1920x1080")
    if duration<60: errors.append("Video shorter than 60 seconds")
    if video.stat().st_size<5_000_000: errors.append("Video file smaller than 5 MB")
if thumb.exists() and thumb.stat().st_size:
    from PIL import Image
    with Image.open(thumb) as im:
        checks["thumbnail_dimensions"]=list(im.size)
        if im.size!=(1920,1080): errors.append("Thumbnail must be 1920x1080")
if srt.exists() and srt.stat().st_size:
    txt=srt.read_text(encoding="utf-8")
    blocks=[b for b in re.split(r"\\n\\s*\\n",txt.strip()) if b.strip()]
    checks["subtitle_blocks"]=len(blocks)
    if len(blocks)<10: errors.append("Too few subtitle blocks")
    if "-->" not in txt: errors.append("Subtitle timestamps missing")
if report.exists() and report.stat().st_size:
    try:
        meta=json.loads(report.read_text(encoding="utf-8"))
        checks["renderer_report"]=meta
    except Exception as e: errors.append(f"Invalid render_report.json: {e}")
result={"passed":not errors,"checks":checks,"errors":errors,"gate_version":"1.0"}
(root/"quality_gate.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
