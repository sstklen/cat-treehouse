#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cat Treehouse 可公開驗證開獎 — v2「種子鎖死版」

修正 v1 的 P1 漏洞：種子字串若由人手寫，同一組開獎號可寫成多種格式 → 多個中獎者，
主辦在看到號碼後仍有挑選空間。v2 把「種子正規化規則」寫死在程式裡並一併承諾，
操作者只能輸入 7 個官方號碼，無任何格式/日期/彩種裁量權。

═══ 開獎前鎖死的承諾常數（一旦公布不可更改）═══
  ROSTER_HASH    : 名單指紋（綁定每筆 票數+票號區間）
  LOTTERY_PREFIX : 指定唯一一期彩券 = 2026-06-08（含）之後第一個「威力彩」開獎
                   （由台灣彩券官網客觀認定；不開則順延至下一個威力彩開獎日，
                     僅在官網明確未公告該期時觸發，主辦無裁量）

═══ 種子正規化（唯一寫法，程式強制）═══
  第一區 6 號：由小到大排序，各自補零成 2 位，逗號連接無空白
  第二區 1 號：補零成 2 位
  seed = "威力彩|2026-06-08|<第一區>|<第二區>"

═══ 開獎演算法 ═══
  H   = SHA256( ROSTER_HASH + ":" + seed )
  win = int(H,16) mod TOTAL + 1          # 中獎票號 1..TOTAL
  winner = 票號區間 [start,end] 涵蓋 win 的那一筆報名

用法：
  python3 draw.py 03 11 18 24 29 38 07
  （傳入威力彩 2026-06-08 開獎號：第一區 6 號 + 第二區 1 號；順序/補零不拘，程式自動正規化）
"""
import json, hashlib, sys, os

# ── 承諾常數（開獎前鎖死）─────────────────────────────
ROSTER_HASH    = "0dfd15aebb26d75e382fb0060023d73c64c9cf93f9662a45a795989695458aab"
LOTTERY_PREFIX = "威力彩|2026-06-08"
HERE = os.path.dirname(os.path.abspath(__file__))

def load_and_verify_roster():
    """載入名單並重算指紋，與承諾比對；不符即中止（防事後竄改）"""
    R = json.load(open(os.path.join(HERE, "roster.json"), encoding="utf-8"))
    pool, total = R["pool"], R["total"]
    canon = "\n".join(f"{e['n']}|{e['who']}|{e['tickets']}|{e['start']}-{e['end']}" for e in pool)
    h = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    if h != ROSTER_HASH:
        sys.exit(f"❌ 名單指紋不符！承諾={ROSTER_HASH} 實算={h} — 名單可能被竄改，拒絕開獎")
    if sum(e["tickets"] for e in pool) != total or pool[-1]["end"] != total:
        sys.exit("❌ 票號區間/總數不自洽，拒絕開獎")
    return pool, total

def build_seed(nums):
    """把 7 個官方號碼正規化成唯一種子字串（強制格式，消除人為挑選）"""
    if len(nums) != 7:
        sys.exit("❌ 需要 7 個號碼：第一區 6 號 + 第二區 1 號")
    z1 = sorted(int(x) for x in nums[:6])
    z2 = int(nums[6])
    if len(set(z1)) != 6:
        sys.exit("❌ 第一區 6 號不可重複")
    zone1 = ",".join(f"{n:02d}" for n in z1)
    zone2 = f"{z2:02d}"
    return f"{LOTTERY_PREFIX}|{zone1}|{zone2}"

def draw(seed, pool, total):
    H = hashlib.sha256(f"{ROSTER_HASH}:{seed}".encode("utf-8")).hexdigest()
    win = int(H, 16) % total + 1
    winner = next(e for e in pool if e["start"] <= win <= e["end"])
    return H, win, winner

if __name__ == "__main__":
    pool, total = load_and_verify_roster()
    if len(sys.argv) != 8:
        print(__doc__)
        sys.exit(f"\n名單已驗證 ✅  指紋={ROSTER_HASH}  總票={total}  抽獎池={len(pool)} 筆\n"
                 f"請輸入威力彩 2026-06-08 開獎號：python3 draw.py <6個第一區號> <1個第二區號>")
    seed = build_seed(sys.argv[1:8])
    H, win, w = draw(seed, pool, total)
    print(f"名單承諾 ROSTER_HASH = {ROSTER_HASH}")
    print(f"總票數 TOTAL         = {total}")
    print(f"正準種子 seed        = {seed}")
    print(f"開獎雜湊 H           = {H}")
    print(f"中獎票號 winning     = {win}")
    print(f"🏆 中獎報名: issue #{w['n']}  {w['who']}  ({w['tickets']} 票, 票號區間 {w['start']}-{w['end']})")
