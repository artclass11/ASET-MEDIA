# ASET — 24 November 2026

**Working title:** उत्पादन वाढतंय, पण महागाईही का चढतेय?  
**English editorial note:** India’s three economic signals — CPI, WPI and the Index of Core Industries.  
**Language:** Marathi, Devanagari-first.  
**Research snapshot:** 24 November 2026, 08:57 Asia/Kolkata.  
**Status:** PREPRODUCTION ARCHIVED — BOTH FORMATS ON HOLD.

## Editorial decision

This episode is distinct from the recent AI valuation/correction coverage and the 23 November crude-oil/Hormuz supply-risk episode. It explains why consumer inflation, wholesale inflation and core-industry output can move at different speeds, and how those signals enter market expectations.

## Separate formats

- `script_mr_long.md` — independent 6–10 minute, 16:9 YouTube explainer.
- `script_mr_short.md` — independent 45–90 second, 9:16 YouTube Short. It is not a cut-down of the long-form script.

## Package

- `candidate_angles.md` — candidate selection and 30-day duplicate review.
- `research_sources.md` — dated source register, claim ledger and caveats.
- `visual_plan.md` — original motion-graphics storyboard for both formats.
- `motion_graphics_data.json` — exact data values for animation.
- `metadata.json` and `youtube_description.md` — publishing drafts.
- `thumbnail.svg` — editable original thumbnail artwork; final raster thumbnail is not rendered.
- `release_manifest.json` — asset provenance and release checklist.
- `qa_report.json` — evidence-based stage status and blockers.
- `RUN_RECORD.json` — this run’s state-machine record.

## Release decision

Both formats remain HOLD. The current local execution environment has FFmpeg, ffprobe, Python, Pillow and Noto Sans Devanagari, but no Blender or Kdenlive binary, no pinned Bol TTS Marathi model cache, and no GPU. DOCS documents a self-hosted `docs-production` runner for its Marathi 3D lane; the latest checked Marathi workflow attempt returned zero jobs and the package-quality job failed before running validation steps. No licensed, auditioned Marathi voice is runnable here.

A 2D text-led Short is technically conceivable, but this run cannot independently verify its creative quality to the required threshold. It is therefore not being passed off as a finished video. No MP4, SRT, final thumbnail JPG/PNG or final-media hash exists.

No Buffer post was created. The scripts and research are archived; production and publishing are held until the required voice/renderer and independent QA are available.
