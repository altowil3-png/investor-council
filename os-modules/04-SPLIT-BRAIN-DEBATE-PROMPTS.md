# 04 — Split-Brain Debate & Workflow Prompts (ก๊อปไปใช้ข้ามแอป AI ได้ทันที)

> **ทำไม "Split-Brain Debate" ถึงให้ผลลัพธ์เหนือกว่าการถาม AI ตัวเดียวแบบเดิมหลายเท่า?**
> เมื่อคุณถาม AI ตัวเดียวว่า *"หุ้น X น่าซื้อไหม?"* AI จะมี **Confirmation Bias** (โน้มเอียงไปทางใดทางหนึ่งตั้งแต่ย่อหน้าแรก และเขียนฝั่งตรงข้ามแบบขอไปที)
> แต่ใน **Split-Brain Debate** เราแยกสมอง 2 ฝั่งขาดจากกันโดยสิ้นเชิง (ห้ามเห็นงานกันในรอบแรก) แล้วบังคับให้ **Cross-Examine (ซักค้านคำต่อคำ)** ก่อนส่งให้ **Chairman (กรรมการกลาง)** ตรวจตัวเลขใหม่ทั้งหมดด้วยคณิตศาสตร์จริงแล้วชี้ขาด

---

## สูตรการจัดทีมข้ามแอป (Cross-App Setup ที่ดีที่สุด)

หากคุณใช้หลายแอป AI บนคอมพิวเตอร์พร้อมกัน นี่คือการจับคู่ที่ให้ผลลัพธ์เฉียบคมที่สุด:

| บทบาท | แอปที่แนะนำ | เหตุผล |
| :--- | :--- | :--- |
| **ฝั่ง Bull (Lead Analyst)** | **ChatGPT / Gemini (เปิด Web Search)** | ดึงข้อมูลล่าสุด งบไตรมาส Earnings Call และมุมมอง Growth/Valuation ได้เร็วและกว้าง |
| **ฝั่ง Bear (Short-Seller / Risk)** | **Claude (Opus/Sonnet)** | โหด คม จับช่องโหว่ทางบัญชี ความเสี่ยงเชิงโครงสร้าง และตอกกลับ Bull แบบไม่ไว้หน้าได้ดีที่สุด |
| **ฝั่ง Chairman (Adjudicator)** | **Antigravity / Cursor / Claude / ChatGPT (มี Python)** | เป็นกลาง ไม่ยึดติดฝั่งใด รัน `valuation_engine.py` ตรวจเลขทั้งสองฝั่งแล้วออกคำตัดสิน + โซนราคา |

*(หมายเหตุ: ถ้าคุณใช้แอปเดียว เช่น Claude Projects ก็สามารถทำ Split-Brain ได้ด้วยการเปิด **3 แชทแยกกัน** ใน Project เดียวกัน: แชท 1 = Bull, แชท 2 = Bear, แชท 3 = Chairman)*

---

## MODE A: Full 3-Round Split-Brain Debate (วิเคราะห์หุ้นเต็มรูปแบบ — มาตรฐานสูงสุด)

### ขั้นตอนที่ 1 (รอบ 1 — รันพร้อมกันในแชท Bull และแชท Bear แยกกัน)

#### Prompt 1A: ส่งให้แชท **BULL ANALYST**
```text
[ROLE: LEAD FUNDAMENTAL ANALYST — BULL & FAIR VALUE CASE]
ยึดกฎเหล็กใน 00-START-HERE-SYSTEM-PROMPT.md และโมดูล 01, 02, 03 ทั้งหมด (Zero Fluff, 50% Quant / 50% Qual)

ภารกิจ: วิเคราะห์หุ้น [ใส่ชื่อหุ้น / Ticker] แบบเจาะลึกเพื่อสร้าง "Strongest Possible Bull & Fair Value Case"

สิ่งที่ต้องทำครบทุกข้อ:
1. ดึงข้อมูลล่าสุด: ราคาหุ้น, Market Cap, Diluted Shares, งบ TTM/ไตรมาสล่าสุด, US 10Y Treasury Yield ปัจจุบัน และสัดส่วนรายได้แยกตาม Segment / แบรนด์ในเครือ
2. ทำ Forensic Accounting ตามโมดูล 01:
   - แยก GAAP vs Non-GAAP, หัก SBC 100%, แยก Customer Float/Deferred Bookings ออกจากเงินสดอิสระ
   - คำนวณ Float-Adjusted EV, Clean Economic FCF, Unlevered FCF (ตรงจาก Core EBIT*(1-Tax) + Depr - CapEx) และ ROCE/ROIC
   - เทียบมาร์จิ้นปัจจุบันกับยุค Pre-COVID (2018–2019)
3. ขุด Grassroots Scuttlebutt ตามโมดูล 02:
   - ค้นหาข้อมูลจาก Reddit, เว็บบอร์ดสายอาชีพ, Glassdoor/Blind, Trustpilot/App Store
   - ติดป้ายกำกับทุกข้อเท็จจริงว่า [Official] หรือ [Reddit/Board/Scuttlebutt]
   - ระบุหลักฐานหน้างานที่ยืนยันว่าคูเมืองยังแข็งแกร่งหรือกำลังกว้างขึ้น
4. วิเคราะห์ 5 Qualitative Pillars (Moat & Value Stick, Management/Incentives, Industry Structure, Customers/Suppliers/Culture, AI/Tech/Regulatory Runway)
5. ประเมินมูลค่าตามโมดูล 03:
   - Reverse DCF (ตลาดกำลัง Price-in โตกี่ %?)
   - Explicit 10Y DCF (Base & Bull Case)
   - Self-Consistent 5Y Forward IRR (รวม Zero-Rerating Floor) และตาราง Required Growth
6. ปิดท้ายด้วย: ทำไมตลาดถึงเข้าใจบริษัทนี้ผิด (Variant Perception) และสมมติฐานอะไรที่ต้องเป็นจริงเพื่อให้ได้ IRR >= 13%–15%
```

#### Prompt 1B: ส่งให้แชท **BEAR ANALYST** *(เปิดแชทใหม่ แยกขาด ห้ามให้เห็นคำตอบ Bull)*
```text
[ROLE: ADVERSARIAL SHORT-SELLER & RISK COMMITTEE — BEAR / DEVIL'S ADVOCATE CASE]
ยึดกฎเหล็กใน 00-START-HERE-SYSTEM-PROMPT.md และโมดูล 01, 02, 03, 05 (Zero Fluff, ไม่ต้องเกรงใจ)

ภารกิจ: โจมตีหุ้น [ใส่ชื่อหุ้น / Ticker] อย่างถึงรากถึงโคน — หาเหตุผลว่าทำไมหุ้นนี้จึงอาจเป็น "Value Trap" หรือ "Permanent Capital Loss" ในอีก 5 ปีข้างหน้า

สิ่งที่ต้องทำครบทุกข้อ:
1. Phase 1 Kill Filter & Forensic Red Flags (โมดูล 01):
   - ตรวจหา Accounting Traps: SBC บวม, Customer Float หลอกตา, M&A/Debt โป่งพอง, CapEx พุ่ง, ภาษีปลอม/รายได้ดอกเบี้ยชั่วคราว, หรือ Margin Peak จากช่วงโควิดเทียบปี 2018–2019
2. ขุดแผลหน้างานด้วย Grassroots Scuttlebutt (โมดูล 02):
   - เจาะ Reddit, เว็บบอร์ดคู่ค้า/ซัพพลายเออร์, Trustpilot, Glassdoor/Blind
   - หาสัญญาณ Leading Indicators ก่อนงบพัง: ลูกค้าย้ายหนี, ซัพพลายเออร์เกลียด/โดนบีบ, พนักงานเก่งลาออก, คุณภาพสินค้า/ซัพพอร์ตตกต่ำ, คู่แข่ง/AI เริ่มกินแชร์จริงหรือยัง?
   - ติดป้าย [Official] vs [Reddit/Board/Scuttlebutt] ทุกจุด
3. Howard Marks Devil's Advocate Check (โมดูล 05):
   - ถ้าตัวเลขในงบดูดีและราคาดูถูก "ทำไมนักลงทุนสถาบันถึงยอมขายทิ้งที่ราคานี้?"
   - จับสัญญาณ Divergence (เช่น ธุรกิจหลักเริ่มชะลอแต่บริษัทเอาเงินไปทำอย่างอื่น/ซื้อหุ้นคืนกลบไว้หรือไม่?)
4. Bear Valuation & 5-Year Pre-Mortem:
   - สร้างฉากทัศน์ Bear Case 10Y DCF และ 5Y IRR (กรณี Take Rate หด / Margin กลับสู่ระดับต่ำสุดในอดีต / โดนค่าปรับ / Multiple De-rate)
   - เขียน Pre-Mortem: "สมมติวันนี้คือปี 2031 แล้วหุ้นนี้ขาดทุน 40% — ลำดับเหตุการณ์ที่ทำให้พังคืออะไร?"
5. ระบุ 3 คำถามเชือดเฉือน (Kill Questions) ที่ฝั่ง Bull ต้องตอบให้ได้ด้วยตัวเลขจริง ห้ามแถ
```

---

### ขั้นตอนที่ 2 (รอบ 2 — Cross-Examination ซักค้านกันตรงๆ)

ก๊อปคำตอบของอีกฝั่งไปวางในแต่ละแชทด้วย Prompt นี้:

#### Prompt 2A: ส่งให้แชท **BULL** (เอาคำตอบ Bear รอบ 1 มาวาง)
```text
[ROUND 2: CROSS-EXAMINATION — BULL REBUTTAL]
ด้านล่างนี้คือรายงานโจมตีจากฝ่าย Bear Analyst:
---
[วางคำตอบของ Bear รอบ 1 ที่นี่]
---
ภารกิจของคุณ (Zero Fluff, ซื่อสัตย์ทางปัญญา 100%):
1. ข้อไหนที่ Bear พูดถูกหรือจับผิดตัวเลขเราได้? ให้ "ยอมรับตรงๆ" และปรับแก้ตัวเลข DCF/IRR ของคุณทันที (ห้ามแถ)
2. ข้อไหนที่ Bear เข้าใจผิด, ใช้ข้อมูลเก่า, หรือคำนวณบัญชี/Working Capital/Float ผิด? ให้โต้กลับด้วยตัวเลขจริงและหลักฐาน [Official] / [Reddit/Board/Scuttlebutt]
3. ตอบ 3 Kill Questions ของ Bear ทีละข้อแบบมีหลักฐานรองรับ
4. สรุปให้สั้นที่สุด: อะไรคือ 2–3 "Crucible Variables" (ตัวแปรชี้ชะตา) ที่แยก Bull ออกจาก Bear จริงๆ?
```

#### Prompt 2B: ส่งให้แชท **BEAR** (เอาคำตอบ Bull รอบ 1 มาวาง)
```text
[ROUND 2: CROSS-EXAMINATION — BEAR REBUTTAL]
ด้านล่างนี้คือรายงานเชียร์ซื้อจากฝ่าย Bull Analyst:
---
[วางคำตอบของ Bull รอบ 1 ที่นี่]
---
ภารกิจของคุณ (Zero Fluff, ซื่อสัตย์ทางปัญญา 100%):
1. จุดไหนในโมเดลการเงินหรือสมมติฐานของ Bull ที่ "มองโลกสวยเกินจริง" หรือ "คำนวณผิดพลาด" (เช่น นับ Float เป็นเงินสด, ลืมหัก SBC, ใช้ Margin Peak, ลืมหัก Interest Income ใน UFCF, ลืม Pending M&A)? ชำแหละให้เห็นตัวเลข
2. จุดไหนที่ Bull มีเหตุผลแข็งแรงจริงจนเราต้องยอมรับว่าเป็นตัวช่วยพยุงราคา (Floor)?
3. ถ้าฝั่ง Bull ถูกบางส่วน ราคาที่ "ขนาด Bear ยังยอมรับว่าซื้อได้ไม่เจ็บตัว (Fat Pitch)" ควรอยู่ที่เท่าไร?
4. อะไรคือเงื่อนไขที่ทำให้ฝั่ง Bear ยอม "กลับลำ (Flip Condition)" มาเห็นด้วยกับการซื้อ?
```

---

### ขั้นตอนที่ 3 (รอบ 3 — Chairman Adjudication ชี้ขาดและตรวจคณิตศาสตร์อิสระ)

เปิดแชทที่ 3 (**Chairman**) แล้วก๊อปสรุปรอบ 1+2 ของทั้งสองฝั่งมาวางด้วย Prompt นี้:

#### Prompt 3: ส่งให้แชท **CHAIRMAN (INVESTMENT COMMITTEE)**
```text
[ROLE: INDEPENDENT INVESTMENT COMMITTEE CHAIRMAN — FINAL ADJUDICATION]
ยึดโมดูล 00, 01, 03, 05 ทั้งหมด (Zero Fluff)

ด้านล่างนี้คือสำนวนการโต้วาทีรอบ 1 และรอบ 2 ระหว่าง Bull Analyst และ Bear Analyst สำหรับหุ้น [ใส่ชื่อหุ้น / Ticker]:
---
[วางผล Bull รอบ 1 & 2]
---
[วางผล Bear รอบ 1 & 2]
---
บริบทพอร์ตของฉัน (ถ้ามี): [เช่น ปัจจุบันถือ TCOM อยู่แล้ว 8% ในกลุ่มท่องเที่ยว / ต้องการถือยาว 5+ ปี / เน้น Margin of Safety]

ภารกิจชี้ขาดของ Chairman:
1. [Audit] ตรวจสอบตัวเลขของทั้ง Bull และ Bear ใหม่ทั้งหมดอย่างอิสระ (หากมี Python ให้รัน `valuation_engine.py` v3 ทันที):
   - ยืนยัน Float-Adjusted EV, Clean Economic FCF, Unlevered FCF (รวม `ΔNWC` ปกติ + Reconciliation Bridge ส่วนต่าง ≤ 5%), Reverse DCF (ระบุตัวแปร มาร์จิ้น ค่าปรับครบ), Audited Base DCF (พร้อม Implied Reinvestment Rate `g / ROIIC`), 5Y IRR (ปันผลลงวันที่ + Cash Ledger ยืนยันว่าปันผลและซื้อหุ้นคืนมีแหล่งเงินครบ + Constant-Multiple Case) และตาราง Required Growth
   - **ตรวจข้ออ้างที่ทั้ง Bull และ Bear เห็นพ้องกันโดยไม่ได้ตรวจต้นฉบับ (Shared Unverified Assumptions):** ตรวจงบ/10-K/10-Q ต้นทางด้วยตัวเองเพื่อกันจุดบอดร่วมกันของทั้งสองฝั่ง
   - ระบุชัดๆ ว่าใครคำนวณผิดหรือมองข้ามอะไรในรอบโต้วาที
2. [Scorecard & Unresolved Unknowns] ตัดสินประเด็นโต้แย้งหลักทีละข้อ ทั้งฝั่ง Quant และ Grassroots Qual และ **แยกหัวข้อ "สิ่งที่ยังตัดสินไม่ได้ ณ วันนี้ (Unresolved Unknowns)"** พร้อมระบุหลักฐานที่ต้องรอพิสูจน์
3. [Verdict & Single-Stock Ceilings] ออกคำตัดสินเด็ดขาดพร้อมเพดานราคาจากกฎผูกมัด 3 เลนส์ (`Starter / Core / Fat Pitch` — แยกสถานะ `SOLVED / IMPOSSIBLE / UNQUALIFIED` ชัดเจน):
   - กติกาขนาดพอร์ตทั้งหมดให้ยึดตาม **โมดูล `05` (SSOT)** เท่านั้น — หากยังไม่มีข้อมูลพอร์ตครบ ให้รายงานเฉพาะ **Single-Stock Ceilings + รายการข้อมูลพอร์ตที่ต้องใช้ก่อนกำหนดสัดส่วน %**
4. [Thesis, Opportunity Cost & Pre-Registered Log] สรุป:
   - เปรียบเทียบค่าเสียโอกาสกับทางเลือกที่ดีที่สุดของเงินก้อนเดียวกัน (Cash / T-Bill / หุ้นดีที่สุดในพอร์ต)
   - 3 Crucible Variables + ช่วงตัวเลขที่คาดและวันตรวจทาน (สำหรับบันทึกใน Calibration Log โมดูล `05` §6)
   - Thesis Breakers (กฎขายทิ้งแบบไม่ลังเล) และ Flip Conditions (เงื่อนไขกลับลำ)
```

---

## MODE B: Fast 3-Minute Kill-Filter & Screening Prompt (คัดกรองเร็ว 3 นาทีก่อนลงลึก)

ใช้เมื่อมีหุ้นผ่านตาเยอะๆ อยากคัดทิ้ง 90% แบบ Pulak Prasad / Terry Smith ก่อนเสียเวลาเปิด Split-Brain เต็มรูปแบบ:

```text
[MODE B: FAST 3-MINUTE KILL-FILTER SCREENING]
ยึด Phase 1 Kill Filters ใน 01-FORENSIC-ACCOUNTING-MANUAL.md และกฎเหล็กใน 00-START-HERE-SYSTEM-PROMPT.md (Zero Fluff)

ช่วยสแกนหุ้น [ใส่ชื่อหุ้น / Ticker] แบบเร็วแต่คมใน 5 หัวข้อนี้:
1. Kill-Filter Check (ผ่าน/ตก):
   - Net Debt / EBITDA หรือ Net Debt / True FCF เกิน 3.0x–3.5x ไหม?
   - ROCE / ROIC ต่ำกว่า 12% หรือ Cash Conversion ต่ำกว่า 80% ไหม?
   - SBC สูงกว่า 25%–30% ของ OCF หรือ Diluted Share Count โตเรื่อยๆ ไหม?
   - มี M&A ใหญ่เกินตัว, กฎหมาย/รัฐแทรกแซงหนัก, หรือ Guidance cut ซ้ำซ้อนไหม?
2. Quick Forensic Snapshot: ราคาปัจจุบัน, Float-Adj EV (ถ้ามี Float), Clean FCF (หัก SBC), Clean FCF Yield เทียบกับ US 10Y Treasury Yield ล่าสุด
3. Quick Grassroots Pulse (1–2 ย่อหน้า): เสียงใน Reddit / ลูกค้า / พนักงาน มีกลิ่นไม่ดีอะไรที่งบยังไม่โชว์ไหม? (ติดป้าย [Official] vs [Reddit/Board/Scuttlebutt])
4. Rough Reverse DCF / Expectations Check: ราคาตอนนี้ตลาดคาดหวังโตสูงหรือต่ำเกินไปเมื่อเทียบกับการโตจริง?
5. Verdict: [KILL ทิ้งเลย] / [WATCHLIST ไว้ก่อน] / [คุ้มค่าที่จะเปิด Full Split-Brain Debate] — ตอบสั้นๆ ตรงประเด็น
```

---

## MODE C: Head-to-Head Stock Duel Prompt (ดวล 2 หุ้นเทียบกันแบบตัวต่อตัว)

ใช้เมื่อลังเลระหว่าง 2 ตัว (เช่น *"ซื้อ BKNG หรือถือ TCOM เพิ่มดี?"*, *"SYK vs MDT"*, *"ขาย A เพื่อย้ายเข้า B ดีไหม?"*):

```text
[MODE C: HEAD-TO-HEAD INVESTMENT DUEL]
ยึดโมดูล 00, 01, 02, 03, 05 (Zero Fluff)

เปรียบเทียบหุ้น [หุ้น A] vs [หุ้น B] เพื่อตัดสินใจจัดสรรเงินลงทุน (Capital Allocation):

1. ตารางเทียบ Forensic Metrics (Normalized เหมือนกันทั้งคู่):
   - Core Revenue Growth (3Y / TTM), Core GAAP EBIT Margin (เทียบ Pre-COVID 2018–2019)
   - ROCE/ROIC, Clean Economic FCF (หัก SBC & Float), Clean FCF Yield เทียบ US 10Y
   - Net Debt/EBITDA, Net Share Buyback Yield
2. ตารางเทียบ Valuation & 5Y IRR:
   - Reverse DCF Implied 10Y CAGR
   - Base DCF Upside/Downside และ Bear Downside
   - 5Y Zero-Rerating IRR Floor และ Required Growth เพื่อได้ IRR 12%–15%
3. ตารางเทียบ Qualitative & Grassroots Moat:
   - คูเมืองใครกว้างกว่าและมีแนวโน้ม "กว้างขึ้น" หรือ "แคบลง"?
   - เสียงหน้างาน [Reddit/Board/Scuttlebutt] ใครได้เปรียบกว่า?
   - ใครเสี่ยงต่อ AI / Regulation / Recession มากกว่ากัน?
4. Portfolio Decision:
   - ถ้าเลือกได้แค่ตัวเดียว ควรเลือกตัวไหน เพราะอะไร?
   - ถ้าถือคู่กัน ความเสี่ยงซ้อนทับ (Correlation) สูงเกินไปไหม? ควรตั้ง Basket Cap กี่ % ของพอร์ต และแบ่งสัดส่วน A : B เท่าไร?
```

---

## MODE D: Post-Earnings Quarterly Audit Prompt (ตรวจการบ้านหลังงบไตรมาสออก)

ใช้ทุกครั้งที่หุ้นในพอร์ตหรือ Watchlist ประกาศงบ เพื่อเช็กแบบไร้ความลำเอียงว่า **Thesis ยังอยู่ หรือ Thesis แตกแล้ว?**:

```text
[MODE D: POST-EARNINGS QUARTERLY AUDIT]
ยึดโมดูล 00, 01, 02, 05 (Zero Fluff)

หุ้น [ใส่ชื่อหุ้น / Ticker] เพิ่งประกาศงบไตรมาส [เช่น Q4 2026 / Q1 2027]
(แนบไฟล์บทวิเคราะห์เดิม หรือวาง Crucible Variables & Thesis Breakers เดิมตรงนี้:
- Crucible Variables เดิม: [...]
- Thesis Breakers เดิม: [...]
- Flip Conditions เดิม: [...])

ช่วยตรวจการบ้านไตรมาสนี้แบบโหดและตรงไปตรงมา:
1. Actual vs Expectations & Core Quality:
   - รายได้โตเท่าไร (Constant Currency vs Reported)? Organic หรือมาจาก M&A/FX?
   - Core GAAP EBIT Margin, SBC % of Rev, Clean Economic FCF และจำนวนหุ้นลดลงจริงตามแผนไหม?
2. Grading Crucible Variables (ให้เกรดทีละตัว: PASS / WATCH / FAIL):
   - ตัวแปรชี้ชะตาแต่ละข้อดีขึ้นหรือแย่ลง?
3. Management Language & Grassroots Check:
   - ใน Earnings Call ผู้บริหารเปลี่ยนคำพูด เปลี่ยนนิยาม KPI หรือเลี่ยงตอบคำถามนักวิเคราะห์เรื่องอะไรไหม?
   - เสียงลูกค้า/คู่ค้า/บอร์ดในไตรมาสล่าสุดสะท้อนอะไรเพิ่มไหม? ([Official] vs [Reddit/Board/Scuttlebutt])
4. Action Update:
   - Thesis Breakers แตกข้อไหนแล้วหรือยัง?
   - ต้องปรับ Base DCF / 5Y IRR / Entry Zones ใหม่ไหม?
   - สรุปการกระทำ: [HOLD / ADD ON DIP / TRIM / SELL IMMEDIATELY]
```
