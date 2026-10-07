# -*- coding: utf-8 -*-
"""把 AI 生图转成「晚清木刻版画」质感，去 AI 渲染的油滑感。
管线：灰度 → 对比拉伸 → USM 锐化(墨线) → FIND_EDGES 刀刻线叠加 → 三级平涂 → 墨/宣纸双色调。
"""
import os
import numpy as np
from PIL import Image, ImageFilter, ImageOps

BASE = r"C:\Users\14257\WorkBuddy\vibe coding\piaohao-mystery\assets\img"
INK = (43, 38, 34)        # 墨色
PAPER = (238, 228, 205)   # 宣纸

def woodblock(path, out, edge_boost=0.6, contrast_cutoff=2, unsharp=(2, 150, 3)):
    im = Image.open(path).convert('L')
    im = ImageOps.autocontrast(im, cutoff=contrast_cutoff)
    im = im.filter(ImageFilter.UnsharpMask(radius=unsharp[0], percent=unsharp[1], threshold=unsharp[2]))

    edges = im.filter(ImageFilter.FIND_EDGES)

    a = np.array(im, dtype=np.float32)
    # 三级平涂（版画的墨块/灰调/留白）
    q = np.where(a < 85, 52.0, np.where(a < 165, 158.0, 244.0))
    e = np.array(edges, dtype=np.float32)
    # 刀刻线：在边缘处压暗，形成墨线
    mixed = np.clip(q - edge_boost * e, 0, 255)
    # 加轻微颗粒，模拟木刻/宣纸
    rng = np.random.default_rng(7)
    grain = rng.normal(0, 3.2, mixed.shape).astype(np.float32)
    mixed = np.clip(mixed + grain, 0, 255)

    t = mixed / 255.0
    r = INK[0] + (PAPER[0] - INK[0]) * t
    g = INK[1] + (PAPER[1] - INK[1]) * t
    b = INK[2] + (PAPER[2] - INK[2]) * t
    rgb = np.stack([r, g, b], axis=-1).astype(np.uint8)
    Image.fromarray(rgb, 'RGB').save(out)
    print('ok', os.path.basename(out))

# 备份原图
os.makedirs(os.path.join(BASE, '_orig'), exist_ok=True)
files = {
    'scene-cover.png': 0.68,
    'scene-counter.png': 0.66,
    'scene-night.png': 0.66,
    'master.png': 0.46,   # 人物立绘柔和一些
}
for name, boost in files.items():
    src = os.path.join(BASE, name)
    if os.path.exists(src):
        os.replace(src, os.path.join(BASE, '_orig', name))
        woodblock(os.path.join(BASE, '_orig', name), src, edge_boost=boost)

print('done')
