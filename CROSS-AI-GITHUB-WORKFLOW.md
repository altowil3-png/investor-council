# คู่มือเชื่อม GitHub ให้ AGV + Codex + AI ตัวที่ 3 ตรวจและแก้กันเอง (ไม่ต้องโยน `.zip` ไปมา)

> **ภาพรวมระบบ:** แทนที่คุณจะต้องโหลด `.zip` แตกไฟล์ และก๊อปข้อความโยนข้ามแอป ให้เก็บโฟลเดอร์ `investor-council` ไว้ใน **Private GitHub Repo เดียว** แล้วให้ AI ทุกตัวคุยและแก้ผ่าน **Pull Request (PR)** โดยมี **GitHub Actions** คอยรัน `--self-test` ตรวจให้อัตโนมัติทุกครั้ง

```text
[AGV แก้โค้ด/โมดูล] ──push──▶ [GitHub PR] ──อัตโนมัติ──▶ [GitHub Actions รัน --self-test]
                                   │
                                   ▼
                      [Codex / Claude รีวิวใน PR]
                                   │
                                   ▼
                [คุณพิมพ์บอก AGV: "แก้ตามคอมเมนต์ PR #X"] ──▶ [Push ซ้ำ] ──▶ [คุณกด Merge]
```

---

## ขั้นตอนที่ 1: เอาโฟลเดอร์ `investor-council` ขึ้น Private GitHub Repo (ทำครั้งเดียว)

### แบบ A — ให้ AGV ทำให้เลย (ง่ายสุด, แนะนำ)
1. กดปุ่ม **Connect GitHub** บนการ์ดปลั๊กอินในแชท Antigravity แล้วล็อกอินบัญชี GitHub ของคุณ
2. กลับมาพิมพ์บอก AGV ในแชทนี้ว่า:
   > **"เชื่อม GitHub แล้ว สร้าง Private Repo ชื่อ `investor-council` แล้ว push ขึ้นไปเลย"**
3. AGV จะสร้าง Private Repo, Push โค้ดทั้งหมด (รวม `.github/workflows/verify.yml` ที่เตรียมไว้ให้แล้ว) และส่งลิงก์ Repo ให้คุณทันที

### แบบ B — ถ้าอยาก Push จากเครื่อง Mac ของคุณเอง (4 บรรทัด)
1. เข้า [github.com/new](https://github.com/new) → ตั้งชื่อ `investor-council` → เลือก **Private** → กด **Create repository** *(ไม่ต้องติ๊ก Add README)*
2. แตกไฟล์ `investor-council-full-os-bundle.zip` ทับโฟลเดอร์เดิมบน Mac แล้วเปิด Terminal รัน:
```bash
cd /Users/natchapol/Documents/investor-council
git init -b main
git add .
git commit -m "init: Investor Council OS v3 with CI verification"
git remote add origin https://github.com/<USERNAME_ของคุณ>/investor-council.git
git push -u origin main
```

---

## ขั้นตอนที่ 2: เชื่อม Codex (OpenAI) เข้ากับ Repo เดียวกัน

1. เข้าหน้า **Codex** (ใน ChatGPT / Codex web) → ไปที่ **Settings / Environments** → กด **Connect GitHub**
2. อนุญาตสิทธิ์เฉพาะ Repo **`investor-council`** (เลือก *Only select repositories* เพื่อความปลอดภัย)
3. เปิดฟีเจอร์ **Code Review on Pull Requests** (หรือเวลาเปิด PR แล้ว แค่พิมพ์คอมเมนต์ใน PR ว่า `@codex review` — Codex จะอ่าน `git diff` ทั้งหมด รันเทสต์ใน Sandbox แล้วคอมเมนต์จุดที่ต้องแก้ตรงบรรทัดโค้ดจริงทันที)

---

## ขั้นตอนที่ 3: เชื่อม AI ตัวที่ 3 (Claude / Cursor) *(เลือกทำตามแอปที่ใช้)*

* **ถ้าใช้ Cursor / Claude Code บน Mac:**
  แค่ `git clone https://github.com/<USERNAME_ของคุณ>/investor-council.git` ครั้งเดียว เวลาจะตรวจงานใหม่ก็แค่ `git pull` แล้วสั่งรีวิว/แก้และ `git push` ขึ้น Branch ได้เลย
* **ถ้าอยากให้ Claude รีวิวอัตโนมัติใน GitHub PR เหมือน Codex:**
  ติดตั้ง **Claude GitHub App** ใน Repo `investor-council` แล้วเวลาเปิด PR พิมพ์ `@claude review` ในคอมเมนต์ PR ได้เช่นกัน

---

## ขั้นตอนที่ 4: วิธีใช้งานจริงประจำวัน (ลดงานคุณเหลือแค่ 2 บรรทัด)

1. **สั่ง AGV แก้หรือวิเคราะห์หุ้นใหม่บน Branch:**
   > *"วิเคราะห์หุ้น `COST` หรือแก้จุดอ่อนใน `valuation_engine.py` แล้วเปิด PR ขึ้น GitHub"*
2. **GitHub Actions ตรวจอัตโนมัติทันที:**
   ไฟล์ `.github/workflows/verify.yml` จะรัน `python3 os-modules/valuation_engine.py --self-test` ให้อัตโนมัติ ถ้าพังจะขึ้นไฟแดง (Red X)
3. **ให้ Codex / AI ตัวที่ 3 รีวิวใน PR:**
   พิมพ์ `@codex review` (หรือ `@claude review`) ในช่องคอมเมนต์ของ PR นั้น → รอ Codex คอมเมนต์จุดอ่อน
4. **สั่ง AGV แก้ตามคอมเมนต์โดยไม่ต้องก๊อปข้อความ:**
   กลับมาบอก AGV สั้นๆ แค่ว่า:
   > **"ไปอ่านคอมเมนต์ทั้งหมดใน PR #1 แล้วแก้ข้อที่เห็นด้วย หรือโต้แย้งข้อที่ไม่เห็นด้วย พร้อม Push ซ้ำ"**
5. **คุณตรวจสรุปและกด Merge:**
   *แนะนำกฎเหล็ก:* วนซ้ำไม่เกิน **2–3 รอบต่อ PR** และให้คุณเป็นคนกด **Merge** สุดท้ายเสมอ เพื่อคุมคุณภาพไม่ให้ AI วนลูปแก้ทับกันเองครับ

---

## กติกา v4 สำหรับ AI ทุกตัวที่แก้ Repo นี้

1. **ห้าม push เข้า `main` ตรงๆ** — ทำงานบน branch ใหม่แล้วเปิด PR เสมอ ให้ CI รันและเจ้าของพอร์ตกด Merge เอง
2. **ตัวเลขอยู่ที่ `inputs/TICKER.json` เท่านั้น** — ห้ามแก้บล็อกระหว่าง `<!-- AUTO-SUMMARY:...:START -->` กับ `END` ด้วยมือ ให้แก้ JSON แล้วรัน `python3 tools/sync_summaries.py --write`
3. **ก่อนเปิด PR ต้องผ่าน 2 คำสั่งนี้บนเครื่อง:**
   ```bash
   python3 os-modules/valuation_engine.py --self-test
   python3 tools/sync_summaries.py --check
   ```
4. **ห้ามลบเทสต์เดิม** — เจอช่องโหว่ใหม่ให้เพิ่มเทสต์ต่อท้าย (9 เคส v3 จากรอบ Codex ต้องอยู่ครบ)
5. **ตัวเลขที่ยังไม่ได้เทียบเอกสารยื่นทางการ** ให้ติด `"verification": "carried_over_unverified"` ตามจริง ห้ามติด `verified` ถ้ายังไม่ได้เปิดดูต้นฉบับ

