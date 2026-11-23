# ASET YouTube Production System — Quality & Self-Healing v1

## North star
Make distinctive, trustworthy, highly watchable Marathi-first YouTube documentaries. Uploading is the final delivery step, not the definition of success. A file is never called "great" merely because FFmpeg produced it or YouTube accepted it.

## Production loop
1. **Discover** — select a timely, audience-relevant question; explain why viewers should care in the first 15 seconds.
2. **Research** — use primary sources first, then reputable reporting; record publication dates, source URLs, exact claims, counter-evidence and uncertainty. Never turn a forecast into a fact.
3. **Script** — Marathi-first, natural spoken language, clear narrative arc, concrete examples, chapter transitions, open loops and a useful conclusion. Avoid repetitive filler and unsupported certainty.
4. **Editorial fact check** — check every number, date, named entity, quote, causal claim and financial statement against the source ledger. Include context and a clear educational disclaimer where needed.
5. **Visual plan** — every paragraph gets a visual purpose: real licensed footage, original diagrams, charts, maps, animated typography or data-led scenes. Do not fill a long video with one static title card per chapter. Never use unlicensed footage or fabricate documentary evidence.
6. **Voice & sound** — natural Marathi pronunciation, consistent loudness, intentional pauses, subtle licensed/original music and sound design. Listen to the complete narration; automatic TTS success is not voice QA.
7. **Edit** — vary shot scale and motion; use visual changes to explain the story, not decoration. Make the first 30 seconds especially strong. Add readable Marathi captions, restrained typography and clean transitions.
8. **Review** — inspect the rendered video, thumbnail and captions. Score the creative rubric below. Technical checks cannot approve creative quality.
9. **Publish** — only publish a technically valid file that passes editorial and creative review. Verify the destination's returned status before reporting success.
10. **Learn** — after publication, capture CTR, average view duration, retention dips, traffic sources, comments and subscriber conversion when available. Compare against the channel's own baseline; do not optimize only for views.

## Creative release rubric (0–5 each)
- Hook and first 30 seconds: immediate stakes, curiosity, clarity.
- Story structure: coherent beginning, escalation, payoff; no dead air.
- Research integrity: accurate, sourced, balanced and current.
- Marathi narration: natural, understandable, consistent pronunciation.
- Visual storytelling: meaningful, varied, relevant visuals; no slideshow feel.
- Editing and sound: pacing, clean mix, readable captions, intentional transitions.
- Thumbnail/title: specific promise, legible on mobile, no misleading clickbait.
- Audience value: viewer learns something useful and remembers the central insight.

**Release threshold:** 30/40 overall, with no score below 3 for research integrity, narration or visual storytelling. A human/editorial visual review is required until an automated vision/audio reviewer is genuinely available. Do not fabricate a score.

## Self-healing rules
- Classify failures: dependency/network, source/data, script/Marathi text, TTS/audio, rendering, media validation, editorial/creative, publishing.
- Retry transient network/TTS/dependency failures with a bounded retry (up to 2 total render attempts in the current workflow); never loop indefinitely.
- For deterministic failures, capture the exact failing command, traceback, tool versions and artifact inventory; patch the root cause before retrying.
- Preserve the failed render and logs as diagnostics. Never overwrite the last known-good published asset.
- On missing/invalid media, stop publishing; retain the failed job report and retry only after correction.
- On factual or creative review failure, return to research/script/visual plan. Do not attempt to "heal" editorial errors by silently changing facts.
- Keep immutable episode inputs, source ledger, render report, quality-gate report and final release URL together.
- A failed upload is not a reason to re-render; retry the upload only after verifying the exact file and destination.
- Never claim "published" unless the platform reports sent/published and a public URL or platform post ID is verified.

## Automated technical gate
The companion `quality_gate.py` verifies deliverable presence, media streams, 1080p dimensions, minimum duration/file size, thumbnail dimensions and subtitle structure. This is necessary, not sufficient. Creative approval remains a separate gate.

## Current baseline and known gap
The current ASET 002 renderer is a basic chapter-card video with Google gTTS Marathi narration. It is a functional render prototype, **not yet the target cinematic documentary standard**. Next upgrades: shot-level visual asset pipeline, data-driven animated charts/maps, natural Marathi voice QA, music/sound design, scene-level captions, thumbnail variants, render preview/contact sheet and post-publication analytics feedback.
