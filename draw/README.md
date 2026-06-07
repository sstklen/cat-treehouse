# 🐱 cat Treehouse 抽獎 — 公開名單與開獎承諾

> 一人中獎、四人同行 · 公開可驗證開獎 · 公布於 **2026-06-07**（開獎隨機種子產生前）

## 承諾 (Commitment)
| 項目 | 值 |
|---|---|
| 抽獎池 | **231 筆** |
| 總票數 | **219,367 張** |
| 中獎名額 | 1 名（+3 友） |
| 名單指紋 `ROSTER_SHA256` | `0dfd15aebb26d75e382fb0060023d73c64c9cf93f9662a45a795989695458aab` |
| 演算法指紋 `DRAW_PY_SHA256` | `b9d004e567911ef5283eeb130641e41389cb88e26193d75ee29f290472710dbe` |

## 開獎（先承諾、後開獎）
- **種子**：台灣彩券「威力彩」2026-06-08 開獎號（全國公開、主辦無法操控）
- **演算法**：`H=SHA256(ROSTER_SHA256+":"+seed)` → `中獎票號=int(H,16) mod 219367 +1` → 找該票號所屬報名
- **重跑驗證**：`python3 draw.py 03 11 18 24 29 38 07`（輸入威力彩 7 號）

## 檔案
- [`ROSTER.md`](ROSTER.md) — 完整名單（231 筆，含票號區間）
- [`roster.csv`](roster.csv) / [`roster.json`](roster.json) — 機器可讀名單
- [`COMMITMENT.txt`](COMMITMENT.txt) — 雙重承諾雜湊
- [`PROTOCOL.md`](PROTOCOL.md) — 完整開獎協議與公平性聲明
- [`draw.py`](draw.py) — 開獎程式（種子鎖死版）

> 隱私：系統從未保存原始 email；名單以遮罩 email + issue 編號識別（無法寄信、已公開於本 repo issues）。
