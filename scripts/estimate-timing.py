#!/usr/bin/env python3
"""Estimate spoken duration from a hypnosis script."""
from __future__ import annotations
import re, sys
from pathlib import Path
WPM = {"en": 120, "ar": 98}

def estimate(text: str, wpm: float = 120.0) -> dict:
    pause = sum(int(x) for x in re.findall(r"\(pause\s+(\d+)\s*s\)", text, re.I))
    silence = sum(int(x) for x in re.findall(r"\(silence\s+(\d+)\s*s\)", text, re.I))
    stop = len(re.findall(r"\[STOP\]", text)) * 5
    spoken = re.sub(r"\([^)]*\)", " ", text)
    spoken = re.sub(r"\[[^\]]*\]", " ", spoken)
    words = len(re.findall(r"\w+", spoken, flags=re.UNICODE))
    seconds = (words / wpm) * 60 + pause + silence + stop
    return {"words": words, "seconds": round(seconds),
            "mmss": f"{int(seconds)//60:02d}:{int(seconds)%60:02d}"}

def main() -> None:
    raw = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else sys.stdin.read()
    lang = "ar" if re.search(r"[\u0600-\u06FF]", raw) else "en"
    r = estimate(raw, WPM[lang])
    print(f"lang={lang} words={r['words']} => {r['mmss']}")

if __name__ == "__main__":
    main()
