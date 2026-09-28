#!/usr/bin/env python3
"""Compare same-named screenshots from two folders and write amplified diff images.

Requires Pillow (pip install pillow).
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def fit(image: Image.Image, size, crop):
    if crop:
        image = image.crop(crop)
    return image.convert("RGB").resize(size, Image.Resampling.LANCZOS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("a", type=Path, help="Reference folder (usually web)")
    parser.add_argument("b", type=Path, help="Candidate folder (usually Android)")
    parser.add_argument("--out", type=Path, default=Path("parity/diff"))
    parser.add_argument("--size", help="Compare at WxH (default: size of the reference image)")
    parser.add_argument("--crop-b", help="Crop the candidate first: left,top,right,bottom in its pixels")
    parser.add_argument("--threshold", type=int, default=16, help="Per-channel difference counted as changed (0-255)")
    parser.add_argument("--max-mean", type=float, default=2.0, help="Mean difference /255 above which a frame fails")
    args = parser.parse_args()

    crop_b = tuple(int(v) for v in args.crop_b.split(",")) if args.crop_b else None
    args.out.mkdir(parents=True, exist_ok=True)
    names = sorted(p.name for p in args.a.glob("*.png") if (args.b / p.name).exists())
    if not names:
        sys.exit(f"No matching .png names in {args.a} and {args.b}")

    failed = 0
    print(f"{'frame':>10}  {'mean/255':>8}  {'changed':>8}  result")
    for name in names:
        ref = Image.open(args.a / name)
        size = tuple(int(v) for v in args.size.split("x")) if args.size else ref.size
        a = fit(ref, size, None)
        b = fit(Image.open(args.b / name), size, crop_b)
        diff = ImageChops.difference(a, b)
        mean = sum(ImageStat.Stat(diff).mean) / 3
        mask = diff.convert("L").point(lambda v: 255 if v > args.threshold else 0)
        changed = 100 * ImageStat.Stat(mask).mean[0] / 255
        ok = mean <= args.max_mean
        failed += not ok
        diff.point(lambda v: min(255, v * 8)).save(args.out / name)
        print(f"{Path(name).stem:>10}  {mean:8.2f}  {changed:7.2f}%  {'ok' if ok else 'CHECK'}")

    print(f"\n{len(names) - failed}/{len(names)} within {args.max_mean}/255 · diffs (×8) in {args.out}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
