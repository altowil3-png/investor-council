# สารบัญคลังบทวิเคราะห์หุ้น (Stock Analyses Index)

จัดเก็บแยกตามตลาด (`us/`, `th/`, `global/`) — ตั้งแต่รุ่น v4 ตัวเลขทุกตัวในตารางแรกสร้างอัตโนมัติจาก `inputs/TICKER.json` ผ่าน `os-modules/valuation_engine.py` และ CI จะไม่ให้ผ่านถ้าตารางไม่ตรงกับผลจากสคริปต์

> **สถานะ v4 คืออะไร:** `Starter` / `Core` / `Fat Pitch` = ราคาวันนี้ไม่เกินเพดาน (ใช้ 2 เลนส์ที่ขึ้นกับราคาจริง: ส่วนเผื่อความปลอดภัยเทียบมูลค่ากรณีฐาน และอัตราได้ต่อเสียเทียบกรณีหมี) **และ** ผลตอบแทน 5 ปีแบบตัวคูณคงที่ ณ ราคาวันนี้ผ่านด่านขั้นต่ำของขั้นนั้น — `Watchlist` = ยังไม่ผ่าน (0% ของพอร์ต) — การให้น้ำหนักพอร์ตจริงยึดโมดูล `05` เท่านั้น

---

## 1. บทวิเคราะห์รุ่น v4 (สร้างอัตโนมัติ — ห้ามแก้ด้วยมือ)

<!-- AUTO-SUMMARY:INDEX:START -->
| Ticker | บริษัท | ราคา ณ วันที่ | สถานะ v4 | เพดาน Starter | เพดาน Core | ไฟล์ |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **ALC** | Alcon Inc. | $76.64 (2026-11-24) | **Watchlist** | ~$47 (ช่วง $45–$49) | ~$44 (ช่วง $43–$46) | [ALC-alcon.md](./us/ALC-alcon.md) |
| **BKNG** | Booking Holdings Inc. | $146 (2026-11-23) | **Watchlist** | ~$120 (ช่วง $115–$125) | ~$110 (ช่วง $110–$115) | [BKNG-booking-holdings.md](./us/BKNG-booking-holdings.md) |
| **MDT** | Medtronic plc | $96.68 (2026-11-24) | **Watchlist** | ~$53 (ช่วง $50–$55) | ~$50 (ช่วง $48–$52) | [MDT-medtronic.md](./us/MDT-medtronic.md) |
| **RMD** | ResMed Inc. | $235.63 (2026-11-20) | **Watchlist** | ~$165 (ช่วง $160–$170) | ~$155 (ช่วง $150–$160) | [RMD-resmed.md](./us/RMD-resmed.md) |
| **ZTS** | Zoetis Inc. | $83.82 (2026-11-24) | **Watchlist** | ~$54 (ช่วง $52–$56) | ~$51 (ช่วง $49–$53) | [ZTS-zoetis.md](./us/ZTS-zoetis.md) |
<!-- AUTO-SUMMARY:INDEX:END -->

แก้ตัวเลขที่ `inputs/TICKER.json` แล้วรัน `python3 tools/sync_summaries.py --write`

---

## 2. บทวิเคราะห์รุ่นเก่า `[LEGACY v1 — Pending v4 Re-audit]`

ทำก่อนกฎ v4 — ตัวเลขไม่มีแหล่งอ้างอิงและไม่ได้ผูกกับสคริปต์ ข้อสรุปด้านล่างเป็นของเดิม **ห้ามใช้ตัดสินใจลงเงิน** จนกว่าจะสร้าง `inputs/TICKER.json` และรันใหม่

| Ticker | ชื่อบริษัท | ราคาวันวิเคราะห์ | ข้อสรุปเดิม (ยังไม่ผ่าน v4) | วันที่ | ไฟล์ |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **BKNG (v2)** | Booking Holdings Inc. — ฉบับ AGV เก็บไว้เทียบ | ~$146 | BUY / สะสม $137–$148 — ⚠️ ถูกแทนที่ด้วยฉบับ v4 ในตารางแรก | 23 พ.ย. 2026 | [BKNG-booking-holdings-v2-agv.md](./us/BKNG-booking-holdings-v2-agv.md) `[LEGACY v1 — Pending v4 Re-audit]` |
| **SYK** | Stryker Corporation | ~$310 | Starter $295–$310 / Core ≤ $275–$285 — ⚠️ ขัดกฎ v4 เอง: ผลตอบแทนกรณีฐาน ~10% ต่ำกว่าด่าน 11% | 23 พ.ย. 2026 | [SYK-stryker.md](./us/SYK-stryker.md) `[LEGACY v1 — Pending v4 Re-audit]` |
| **UBER** | Uber Technologies, Inc. | ~$64.07 | Small Starter (2%–3%) $60–$64 / Core ≤ $55–$58 / Fat Pitch ≤ $48–$50 | 23 พ.ย. 2026 | [UBER-uber-technologies.md](./us/UBER-uber-technologies.md) `[LEGACY v1 — Pending v4 Re-audit]` |
| **GOOGL** | Alphabet Inc. | ~$283.93 | Watchlist — Starter ≤ $255–$260 / Core ≤ $230–$245 | 23 พ.ย. 2026 | [GOOGL-alphabet.md](./us/GOOGL-alphabet.md) `[LEGACY v1 — Pending v4 Re-audit]` |
| **POOL** | Pool Corporation | ~$208.23 | Watchlist — Starter ≤ $180–$188 / Core ≤ $155–$170 | 23 พ.ย. 2026 | [POOL-pool-corp.md](./us/POOL-pool-corp.md) `[LEGACY v1 — Pending v4 Re-audit]` |
| **MDT (v1)** | Medtronic plc — ฉบับ AGV เก็บไว้เทียบ (เขียนก่อนงบ Q2 FY27) | ~$100–$103 | Watchlist — ≤ $78–$82 — ⚠️ ถูกแทนที่ด้วยฉบับ v4 ในตารางแรก | 24 พ.ย. 2026 | [MDT-medtronic-v1-agv.md](./us/MDT-medtronic-v1-agv.md) `[LEGACY v1 — Pending v4 Re-audit]` |
| **BSX** | Boston Scientific Corp. | ~$42 | Pass — หนี้ >3.6x หลังดีล Penumbra $14.5B + หั่นเป้า 3 รอบ (ดูใหม่ ≤ $32–$35) | 23 พ.ย. 2026 | [BSX-boston-scientific.md](./us/BSX-boston-scientific.md) `[LEGACY v1 — Pending v4 Re-audit]` |
