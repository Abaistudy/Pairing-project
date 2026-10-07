# The Cipher of Rishengchang · 晋商票号密押
### An Interactive Ink-Wash Mystery Game — for *Digital Studies of Chinese Culture*

A playable one-file web game where you play a Shanxi draft-bank apprentice in 1844:
learn the secret cipher rhymes, write a draft, cash it in Beijing, catch a forger —
and discover that it was a **cryptographic signature, two centuries early**.

---

## Run it (offline-safe)

```bash
cd piaohao-mystery
python -m http.server 8765
# open http://localhost:8765
```

All dependencies (Vue 3, Tailwind, GSAP) and all art assets are **local files** —
no internet needed. For the class demo: double-click `index.html` also works in
most browsers, but serving via `http.server` is the reliable path.

## The Historical Cipher (史料密押)

| Field | Rhyme (口诀) | Mapping |
|---|---|---|
| Months 月 | 谨防假票冒取勿忘细视书章 | char #1–12 → month 1–12 |
| Days 日 | 堪笑世情薄天道最公平昧心图自利阴谋害他人善恶终有报到头必分明 | char #1–30 → day 1–30 |
| Digits 数 | 生客多察看斟酌而后行 | char #1–10 → digit 1–10 |
| Units 位 | 国宝流通 | 国→万 宝→千 流→百 通→十 |

Amounts are written digit-by-digit with units interleaved:
**1,200 taels = 一千二百 = 生宝客流**

Example: month 9, day 6, 1,200 taels → cipher **书 取 生 宝 客 流**
(written vertically in the 密押 column of the draft).

## Game Flow (7 acts, ≈ 5 min)

| Act | 幕 | Player action |
|---|---|---|
| I | 入号 Entering the House | scroll unfurls, story intro |
| II | 学艺 Learning the Rhymes | 3-question cipher quiz |
| III | 开票 Writing the Draft | fill 6 cipher slots, master validates, red seal stamps |
| IV | 验票 Cashing in Beijing | decode a stranger's cipher, pay out silver |
| V | 辨伪 Catching the Forger | decode a tampered draft — plain text ≠ cipher → forged! |
| VI | 结业 Graduation | earn your own seal (name input → personal chop) |
| — | 回响 Epilogue | 1844 cipher vs. modern HMAC/digital signature, side by side |

## 5-Minute Demo Script (English class)

1. **0:00–0:30** — Cover: "In 1844, China's largest bank moved silver across the empire *on paper*. How could a piece of paper be trusted? This is a mystery game — you're the apprentice."
2. **0:30–1:15** — Act II: show the four rhymes. "These look like moral proverbs — 'Beware fake drafts, look carefully' — but each character is a lookup-table entry. The advice *is* the algorithm."
3. **1:15–2:15** — Act III: write the draft live. Decode one character aloud (month 9 = 9th char of 谨防假票冒取勿忘细视书章 = 书). Stamp the seal.
4. **2:15–3:00** — Act IV: Beijing branch. "No telegraph. The Beijing clerk only needs the same rhyme — a shared secret key — to verify."
5. **3:00–4:00** — Act V: the forger. Plain text says 4,500 taels, cipher says 7,800 — tamper detection, exactly like a broken signature check.
6. **4:00–5:00** — Epilogue: rhyme = key, cipher = MAC, branch network = distributed verification, rhyme rotation = key rotation. "A handwritten HMAC, 200 years early."

## Tech & Credits

- Vue 3 (CDN build, local) · Tailwind CSS (Play CDN, local) · GSAP 3 (local)
- Scene art: AI-generated ink-wash illustrations, post-processed into a woodblock-print style (`tools/woodblock.py`)
- Sound: WebAudio-synthesized stamp/click tones + an original ambient pentatonic BGM loop (guqin-pluck melody over a low drone), no audio files, toggle via the ♪ button
- Story: every act opens with a first-person dialogue prologue (typewriter text, speaker tags, player choices) before its gameplay
- Historical basis: cipher rhymes attributed to 日昇昌 (Rishengchang, est. 1823, Pingyao, Shanxi) — the first Chinese piaohao (draft bank)
