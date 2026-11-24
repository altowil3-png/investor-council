# บันทึกชี้แจงการปรับปรุง Investor Council รุ่น 03 (`v3`) — สำหรับ Codex และ Reviewer ตัวที่ 3

* **วันที่:** 24 พฤศจิกายน 2026
* **ผู้จัดทำ:** AGV (ตอบรับข้อวิจารณ์รุ่น 02 จาก `investor-council02-review-for-AGV.md`)
* **สถานะการตอบรับ:** **รับข้อวิจารณ์ทั้ง 4 ประเด็นหลัก 100% (ไม่คัดค้าน)** พร้อมปรับแก้ครบทั้ง 12 ประเด็นเชิงหลักการในโมดูล `00`–`05` และอัปเกรด `os-modules/valuation_engine.py` เป็นรุ่น **v3** (ผ่านชุดทดสอบอัตโนมัติ `--self-test` ครบ 9/9 เคส)
* **คำแนะนำสำหรับ AI Reviewer ตัวที่ 3:** คุณสามารถรันคำสั่งในหมวดที่ 4 ด้านล่างเพื่อตรวจสอบตัวเลขจริงบนเครื่อง และตั้งคำถามโจมตีต่อในหมวดที่ 5 ได้ทันที

---

## 1. สรุปภาพรวมการเปลี่ยนแปลง (รุ่น 02 → รุ่น 03)

ในการตรวจรุ่น 02 Codex พบจุดบกพร่องสำคัญ 4 ข้อที่เป็นปัญหาทางคณิตศาสตร์และนโยบายจริง:
1. โมเดล 5Y IRR อนุญาตให้จ่ายปันผลเกินแหล่งเงินสดที่มี (เสก IRR ลม 15% ทั้งที่ขาดเงินปีละ \$50M)
2. สูตร Direct P&L UFCF ในโค้ดลืมหัก `Normalized ΔNWC` ไม่ตรงกับโมดูล 01 และไม่มีสะพานกระทบยอดกับ OCF
3. ตัวหาเพดานราคา (`_bisect`) ไม่เช็กการคร่อมราก ทำให้เป้าหมาย IRR ที่เป็นไปไม่ได้คืนค่าขอบล่าง `\$1.00` ออกมาเป็นราคาซื้อ
4. กติกา Watchlist ขัดกันเองระหว่างโมดูล 03 (อนุญาต Tracking 1–2%) กับโมดูล 05 (กำหนด 0%)

รุ่น 03 (`v3`) แก้ไขทั้ง 4 จุดที่รากเหง้า พร้อมปิดช่องโหว่เชิงหลักการอีก 12 ข้อในคู่มือทั้ง 6 โมดูล

---

## 2. คำตอบและรายละเอียดการแก้ไขทั้ง 4 จุดหลัก (พร้อมตำแหน่งโค้ด & สูตร)

### จุดที่ 1: บริษัทเอาเงินจากไหนมาจ่ายปันผล? (`Unfunded Dividends`)
* **คำตัดสิน:** **รับข้อวิจารณ์ 100%**
* **ตำแหน่งที่แก้:** `os-modules/valuation_engine.py` — `YearCashLedger` (บรรทัด 181), `IRRSimulationResult` (บรรทัด 195), `simulate_5y_forward_irr()` (บรรทัด 386–529) และ `os-modules/03-VALUATION-DCF-IRR-TEMPLATES.md` §5
* **กลไกใหม่ในรุ่น 03:**
  * ติดตาม **งบเงินสด 5 ปีรายปี (5-Year Cash Ledger)** เริ่มจาก `Beg Free Cash (ex-Customer Float)` ในปีที่ 1:
    $$\text{Available Cash}_t = \text{Beg Cash}_t + \text{Clean FCF}_t - \text{Cash Drag}_t$$
    $$\text{End Cash}_t = \text{Available Cash}_t - \text{Actual Dividends}_t - \text{Buybacks}_t$$
  * เพิ่มนโยบายควบคุม 3 โหมดใน `irr_model["dividend_funding_policy"]`:
    1. **`strict_fail` (ค่าเริ่มต้นที่แนะนำ):** หาก `Planned Dividends > Available Cash` ในปีใดปีหนึ่ง จะ **ปฏิเสธการแสดง IRR (`irr = None`)**, ตั้ง `feasible = False`, สถานะ `INFEASIBLE_UNFUNDED_DIVIDEND` และรายงานปีแรกที่ขาดเงิน + ยอดขาดสะสมทั้งหมด (โดยตั้ง `end_cash = 0` ในปีที่ขาดเงินเพื่อไม่ให้เงินไม่พอไหลข้ามปีไปกลบยอดขาดจริง)
    2. **`cap_to_available_cash`:** ตัดปันผลจริงลงเท่ากับ `max(0, Available Cash)` ในปีที่ขาดเงิน, บันทึก `dividend_cut_years`, และคำนวณ IRR จากปันผลที่จ่ายได้จริงเท่านั้น
    3. **`external_debt_funded`:** กู้เงินปิดส่วนต่าง (`debt_added`), คิดดอกเบี้ยหลังภาษีในปีถัดไป (`after_tax_debt_cost`), และหักยอดหนี้สะสมที่เพิ่มขึ้นออกจากมูลค่าหุ้นปลายปีที่ 5 ตรงๆ (ไม่สามารถเสก IRR ลมได้)
  * **จุดที่ตรวจแจ้งผู้ใช้ก่อนแสดง IRR / โซนราคา:** ตรวจทุกปีใน `simulate_5y_forward_irr()` และส่งต่อสถานะ `INFEASIBLE_CASH_PLAN` เข้าไปบล็อกตาราง `[4]` และตารางโซนราคา `[6]` อัตโนมัติ

### จุดที่ 2: เงินทุนหมุนเวียน (`ΔNWC`) และต้นทุนของการโตหายไปไหน?
* **คำตัดสิน:** **รับข้อวิจารณ์ 100%**
* **ตำแหน่งที่แก้:** `os-modules/valuation_engine.py` — `ttm_normal_working_capital_investment` (บรรทัด 72), `compute_forensic_metrics()` (บรรทัด 219–270), ตาราง `[1]` และ `[3]` (บรรทัด 672–713), `os-modules/01-FORENSIC-ACCOUNTING-MANUAL.md` §2.3 และ `os-modules/03-VALUATION-DCF-IRR-TEMPLATES.md` §1 & §4
* **กลไกใหม่ในรุ่น 03:**
  * สูตร Direct P&L Unlevered FCF แก้ให้ตรงกับโมดูล 01 100%:
    $$\text{UFCF}_{\text{P\&L}} = \text{Core GAAP EBIT} \times (1 - t) + \text{D\&A} - \text{CapEx} - \Delta\text{NWC}_{\text{normal}}$$
    *(เมื่อ $\Delta\text{NWC}_{\text{normal}} > 0$ คือเงินสดไหลออกไปจมในสต็อก + ลูกหนี้ − เจ้าหนี้ ไม่รวม Customer Float)*
  * เพิ่ม **OCF ↔ P&L Reconciliation Bridge** ใน Section `[1]`:
    $$\text{P\&L-Implied Levered FCF} = \text{UFCF}_{\text{P\&L}} - \text{Net Interest} \times (1 - t)$$
    $$\text{Reconciliation Gap} = \text{Clean Economic FCF}_{\text{OCF}} - \text{P\&L-Implied Levered FCF}$$
    หาก $|\text{Gap}| > 5\%$ ของ UFCF สคริปต์จะพิมพ์ `[!] RECONCILIATION WARNING` เพื่อให้ตรวจภาษีเงินสดเทียบภาษีบัญชี, ค่าเช่า หรือการหัก ΔNWC/Float ซ้ำซ้อน
  * เพิ่ม **Implied Reinvestment Rate Check** ใน Section `[3]` ของ DCF ทุกกรณี:
    $$\text{Implied Reinvestment Rate} = \frac{\max(0, g_{1\text{–}5})}{\text{Assumed Incremental ROIC}}$$
    เพื่อเตือนไม่ให้ตั้งอัตราโตสูงโดยไม่มีเงินลงทุน (CapEx + ΔNWC) รองรับ

### จุดที่ 3: เมื่อเป้า IRR เป็นไปไม่ได้ ทำไมได้ราคาเข้าซื้อ `\$1.00`?
* **คำตัดสิน:** **รับข้อวิจารณ์ 100%**
* **ตำแหน่งที่แก้:** `os-modules/valuation_engine.py` — `PriceSolveResult` (บรรทัด 212), `_bisect_bracketed()` (บรรทัด 273), `irr_from_cash_flows()` (บรรทัด 308), `solve_price_for_constant_multiple_irr()` (บรรทัด 554–650), ตาราง `[6]` (บรรทัด 745–792) และ `os-modules/03-VALUATION-DCF-IRR-TEMPLATES.md` §7
* **กลไกใหม่ในรุ่น 03:**
  * เปลี่ยน `_bisect` เป็น `_bisect_bracketed` ที่ตรวจว่า `target` ถูกคร่อมระหว่าง `f(low)` และ `f(high)` จริงหรือไม่ก่อนคำนวณ — หากไม่คร่อมจะคืน `None` ทันที ไม่ยุบไปขอบล่าง
  * ขยายขอบบนของ `irr_from_cash_flows()` แบบไดนามิก (`while npv(hi) > 0: hi *= 2.0`) เพื่อให้การทดสอบราคาต่ำมาก (ที่ให้ Dividend Yield สูงมาก) คำนวณ IRR ได้ถูกต้องไม่หลุดกรอบ
  * `solve_price_for_constant_multiple_irr()` ตรวจความแปรผันของ IRR ต่อราคา + ตรวจคำตอบซ้ำหลังแก้สมการ (`|IRR(p*) - target| <= 1e-4`) และคืนสถานะชัดเจน 6 แบบ:
    1. `SOLVED` — มีราคาที่ผ่านและตรวจซ้ำตรงเป้า
    2. `IMPOSSIBLE` — เป้าหมายเป็นไปไม่ได้ภายใต้สมมติฐาน (เช่น ปันผล 0, ซื้อคืน 0, โต 6.2% < เป้า 11% ทำให้ IRR คงที่ 6.2% ที่ทุกราคาบวก)
    3. `UNBOUNDED_PASS` — IRR สูงกว่าเป้าที่ทุกราคาบวก (เช่น โต 15% > เป้า 11% ทำให้ Lens B ไม่จำกัดเพดานราคา)
    4. `INFEASIBLE_CASH_PLAN` — แผนเงินสด/ปันผลขาดเงิน
    5. `UNBRACKETED_ABOVE_MAX` / `UNBRACKETED_BELOW_MIN` — คำตอบอยู่นอกช่วงค้นหาที่ทดสอบ
  * **การส่งต่อไปตารางโซนราคา `[6]`:** หากสถานะเป็น `IMPOSSIBLE`, `INFEASIBLE_CASH_PLAN` หรือ `UNBRACKETED_*` โซนนั้นจะขึ้น **`UNQUALIFIED`** ทันที (ห้ามคืนขอบล่าง `\$1.00`)

### จุดที่ 4: เมื่อสภาตัดสิน Watchlist แล้ว สัดส่วนที่อนุญาตคือเท่าไร?
* **คำตัดสิน:** **รับข้อวิจารณ์ 100%**
* **ตำแหน่งที่แก้:** `os-modules/05-PORTFOLIO-SIZING-RISK-SELL-DISCIPLINE.md` §2 (SSOT), `os-modules/03-VALUATION-DCF-IRR-TEMPLATES.md` §7, `os-modules/00-START-HERE-SYSTEM-PROMPT.md` ข้อ 6, และป้าย `[PORTFOLIO GATE]` ใน `os-modules/valuation_engine.py` บรรทัด 790–791
* **กลไกใหม่ในรุ่น 03:**
  * **Single Source of Truth (SSOT):** กติกาขนาดพอร์ตทั้งหมดรวมอยู่ที่ **`05-PORTFOLIO-SIZING-RISK-SELL-DISCIPLINE.md` §2 เพียงแห่งเดียว** โมดูลอื่นห้ามตั้งข้อยกเว้นเอง
  * **แยก 3 ระดับของ Tier 0 ชัดเจน:**
    * `Tier 0A: Pass / Reject` = **0% (Hard Cap — ห้ามเปิดทุกกรณี)**
    * `Tier 0B: Pure Watchlist` = **0% (ค่าเริ่มต้น)**
    * `Tier 0C: Tracking / Pilot Exception` = **0.5%–1.5%** *(ไม่ใช่อัตโนมัติ)* อนุญาตเฉพาะเมื่อครบ 3 เงื่อนไข: (1) ผ่าน Kill Filter & Forensic Audit 100%, (2) ผ่านอย่างน้อย 2 ใน 3 เลนส์ของโซน Starter, และ (3) **เจ้าของพอร์ตลงนามอนุมัติเป็นลายลักษณ์อักษรใน Decision Log** พร้อมระบุค่าเสียโอกาส, ผลกระทบต่อ Basket Cap และเงื่อนไขขยับขึ้น/ออก
  * **แยก "Single-Stock Ceilings" ออกจาก "Portfolio Sizing":** เมื่อมีเพียงข้อมูลหุ้น 1 ตัว ระบบจะออกเฉพาะเพดานราคาหุ้นเดี่ยว พร้อมบังคับตรวจ **Pre-Sizing Portfolio Gate** 4 ข้อก่อนใส่ % จริง: (1) Opportunity Cost เทียบทางเลือกดีสุดของเงินก้อนเดียวกัน, (2) Joint Drawdown Stress Test (ความเสียหายร่วมของธีมเดียว ≤ 3%–5% ของพอร์ตรวม), (3) Basket & Macro Factor Cap, (4) สภาพคล่อง ADV

---

## 3. ตารางสรุปการอัปเกรดตามข้อเสนอ 12 ข้อของ Codex

| ข้อ | หลักการ | สิ่งที่ปรับปรุงในรุ่น 03 (`v3`) | ไฟล์ที่แก้ไข |
| :---: | :--- | :--- | :--- |
| 1 | น้ำหนักหลักฐานตามคำถาม | ระบุชัดว่า `50/50 Quant-Qual` คือ **Research Coverage Mandate** ส่วนน้ำหนักตัดสินขึ้นกับตัวแปรชี้ขาดของคำถาม | `00` ข้อ 2 |
| 2 | คุณภาพข้อมูลภาคสนาม | ตัดคำกล่าวอ้าง "นำงบ 6–18 เดือนเสมอ" เพิ่มเกณฑ์ Provenance, Independence, Selection Bias และเกณฑ์ ≥ 2 แหล่งอิสระ + Cross-check ก่อนแก้ DCF | `02` บทนำ & §1 |
| 3 | Base Rate & ฐานปี 2018–2019 | บังคับกำหนดเกณฑ์เลือกกลุ่มเทียบก่อนประมาณการ (รวมผู้แพ้กัน Survivorship Bias) และให้เหตุผลทุกครั้งที่ใช้ปี 2018–2019 | `00` ข้อ 4, `01` §2.3 |
| 4 | กระทบยอดบัญชี | รวม `ΔNWC` ในโค้ดตรงกับโมดูล 01 + OCF↔P&L Reconciliation Bridge + เช็กลิสต์กันหักซ้ำ (SBC/Float/Leases/Fines) | `01` §2.3, `valuation_engine.py` |
| 5 | เงินลงทุนที่ทำให้โต | บังคับอธิบายตัวขับเคลื่อน Revenue/Margin/Reinvestment + คำนวณ `Implied Reinvestment Rate = g / ROIIC` ใน DCF | `03` §4, `valuation_engine.py` |
| 6 | ต้นทุนทุนและสกุลเงิน | เปลี่ยนจากบังคับ US 10Y เป็น **Matched-Currency 10Y Sovereign Yield** (สกุลเงิน/เงินเฟ้อ/ผู้รับกระแสเงินสดต้องตรงกัน) | `00` ข้อ 5, `03` §1–2, `valuation_engine.py` |
| 7 | ความหมายของ Reverse DCF | ตัดการตีความอัตโนมัติว่าอัตราโตต่ำ = "หายนะเชิงโครงสร้าง" ชี้แจงว่าอาจมาจาก WACC, Margin, Reinvestment หรือวัฏจักร | `03` §3 |
| 8 | ผลตอบแทนตามงวด & แหล่งเงิน | คงปันผลลงวันที่ + เพิ่ม Cash Ledger 5 ปี + แยกสถานะตัวหาคำตอบ + เปลี่ยนชื่อ `Zero-Rerating Floor` → **`Constant-Multiple Case`** | `03` §5–7, `valuation_engine.py` |
| 9 | ขนาดลงทุน & ความเสียหายพอร์ต | รวมกฎขนาดพอร์ตไว้ที่ `05` (SSOT) + แยก Single-Stock Ceilings ออกจาก Portfolio Gate + เพิ่ม Joint Drawdown Stress Test | `03` §7, `05` §2–3, `valuation_engine.py` |
| 10 | ค่าเสียโอกาส | เพิ่ม **Opportunity Cost at Entry** ใน Pre-Sizing Gate และ Chairman Prompt (ไม่ใช่มีแค่ตอนขาย) | `04` Prompt 3, `05` §2.2 |
| 11 | คุณภาพการซักค้าน | บังคับ Chairman ตรวจ **Shared Unverified Assumptions** (ข้ออ้างที่ Bull & Bear เชื่อร่วมกันโดยไม่เปิดงบ) + แยกหัวข้อ **Unresolved Unknowns** | `04` Prompt 3 |
| 12 | วัดความแม่นหลังตัดสินใจ | อัปเกรดเป็น **Pre-Registered Calibration Log** (จดช่วงคาดการณ์ ความน่าจะเป็น วันตรวจล่วงหน้า ทั้ง Buy/Pass และทบทวนกรณี *Right for the Wrong Reason*) | `05` §6 |

---

## 4. วิธีรันตรวจสอบทวน (สำหรับ Codex และ Reviewer ตัวที่ 3)

รันจากโฟลเดอร์ราก `investor-council/`:

```bash
# 1. รันชุดทดสอบอัตโนมัติในตัว (9 เคส รวมทุกกรณีทดสอบของ Codex)
python3 os-modules/valuation_engine.py --self-test

# 2. รันรายงานตัวอย่าง BKNG เต็มรูปแบบ (ดู Reconciliation Bridge, Cash Ledger 5 ปี และ 3-Lens Ceilings)
python3 os-modules/valuation_engine.py
```

**ผลลัพธ์ที่ยืนยันแล้วบนรุ่น 03 (`v3`):**
* `python3 os-modules/valuation_engine.py --self-test` → **`ALL 9 ADVERSARIAL ACCEPTANCE TESTS PASSED.`**
  * Case 1 (`strict_fail`): `feasible=False`, `status=INFEASIBLE_UNFUNDED_DIVIDEND`, `irr=None`, `shortfall=\$250M`
  * Case 1 (`cap_to_available_cash`): `feasible=True`, `status=OK_DIVIDEND_CUT`, `irr=10.00%`, `cut_yrs=[1, 2, 3, 4, 5]`
  * Case 1 (`external_debt_funded`): `feasible=True`, `status=OK_DEBT_FUNDED`, `debt_added > \$250M`, `irr < 12%`
  * Case 1 (`\$300M` starting free cash): `feasible=True`, `status=OK`, `ending_cash=\$50M`, `irr=15.00%`
  * Case 2 (`ΔNWC = 20 vs 0`, `OCF = 90 vs 110`, `CapEx = 10`): `UFCF = 80 vs 100`, `reconciliation_gap = 0.0` ทั้งคู่
  * Case 3A (โต 6.2%, ปันผล 0, ซื้อคืน 0, เป้า 11%): `status=IMPOSSIBLE`, `price=None`
  * Case 3B (โต 15%, ปันผล 0, ซื้อคืน 0, เป้า 11%): `status=UNBOUNDED_PASS`, `price=None`
  * Case 4 (BKNG baseline): `Constant-Multiple IRR = 13.30%`, `Reconciliation Gap = +3.4%`, `Lens B = SOLVED` ทั้ง 3 ระดับ (`\$213.02 / \$152.25 / \$119.13`), Binding Ceilings: `Starter ≤ \$136.64 (R/R) | Core ≤ \$129.70 (R/R) | Fat Pitch ≤ \$119.13 (IRR)`

---

## 5. ข้อจำกัดที่ยังเปิดอยู่ (เชิญ Reviewer ตัวที่ 3 โจมตีต่อได้เลย)

เพื่อให้การรีวิวรอบถัดไปตรงจุดและไม่เสียเวลา นี่คือข้อจำกัดที่รุ่น 03 ยอมรับไว้ล่วงหน้า:
1. **Unspent Cash & Multiple Valuation ใน 5Y IRR:** ใน `simulate_5y_forward_irr()` เงินสดส่วนเกินที่ไม่ได้นำไปซื้อหุ้นคืน (เช่น เก็บไว้ 15% เมื่อ `bb_alloc = 0.85`) จะสะสมใน `end_cash` ของ Cash Ledger แต่ **ยังไม่ได้บวกส่วนเพิ่มของ `end_cash` (Excess Cash Build) กลับเข้าไปในมูลค่าหุ้นปลายปีที่ 5** — ผลคือโมเดลอนุรักษ์นิยมเล็กน้อยเมื่อ `bb_alloc < 1.0` (แต่สำหรับบริษัทที่ตั้ง `bb_alloc = 0.0` และไม่จ่ายปันผล การไม่ให้เครดิตเงินสดสะสมจะกด IRR ลงเล็กน้อย ควรพิจารณาในรุ่น 04 ว่าจะบวก Excess Cash Build ปลายปีที่ 5 หรือไม่)
2. **Explicit Multi-Year Reinvestment Model:** ปัจจุบัน Section `[3]` แสดง `Implied Reinvestment Rate = g / ROIIC` เป็น Sanity Check แต่ยังรับ `ufcf_cagr_1_5` เป็นพารามิเตอร์ตรง (ยังไม่ได้สร้างโหมด 3-Statement Driver เต็มรูปแบบที่รับ `Rev growth + EBIT margin + CapEx% + NWC%` แยกทุกกรณี)
3. **บทวิเคราะห์หุ้นเก่าใน `analyses/us/`:** บทวิเคราะห์ 7 ตัวที่ทำไว้ก่อนหน้า (ยกเว้น `BKNG` ที่เพิ่ม Audit Note v2 แล้ว) ถูกสร้างก่อนกฎ 3-Lens Binding และ `v3` หากจะนำไปตัดสินใจลงเงินจริงต้องรันซ้ำผ่าน `valuation_engine.py` v3 ก่อน
