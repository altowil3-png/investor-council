# 03 — Valuation, Reverse DCF & Self-Consistent 5-Year IRR Templates

> **หน้าที่ของโมดูลนี้:** แปลงความจริงจากงบการเงิน (`01-FORENSIC-ACCOUNTING-MANUAL.md`) และข้อมูลหน้างาน (`02-GRASSROOTS-SCUTTLEBUTT-FIELD-GUIDE.md`) ให้เป็น **"ตัวเลขความคาดหวังของตลาด"** และ **"ราคาเข้าซื้อที่มี Margin of Safety จริง"** โดยห้ามเดาเลขในใจ — ทุกสมการในไฟล์นี้มีโค้ดพร้อมรันอยู่ใน `valuation_engine.py`

---

## 1. หลักคิดตั้งต้น: Valuation คือการ "ถอดรหัสความคาดหวัง" ไม่ใช่การเดาอนาคต

อ้างอิงแนวคิดของ **Michael Mauboussin (Expectations Investing)**, **Dev Kantesaria (10Y Treasury Hurdle)** และ **Seth Klarman (Risk-First)**:
1. **อย่าเริ่มจากการตั้งเป้าโตเองแล้วทำ DCF หาเป้าหมายราคา** (เพราะคุณจะเผลอปรับตัวเลขเข้าข้างอคติตัวเอง)
2. **ให้เริ่มจาก "Reverse DCF" เสมอ:** ถามก่อนว่า *"ณ ราคาหุ้นวันนี้ ตลาดกำลัง Price-in ว่าบริษัทต้องโตปีละกี่ % ไปอีก 10 ปี?"*
3. **ห้ามใช้ตัวเลข Base Year ที่ผิดเพี้ยน:** Unlevered FCF ปีฐาน (`UFCF_0`) ต้องคำนวณตรงจาก `Core GAAP EBIT × (1 − Effective Tax Rate) + Depreciation − CapEx − Normalized ΔNWC` (ต้องหักเงินทุนหมุนเวียนดำเนินงานปกติที่ต้องใช้ตามธุรกิจ และกระทบยอดกับ OCF ผ่าน Reconciliation Bridge ในโมดูล `01` §2.3 เพื่อกันการนับซ้ำหรือหักขาด)
4. **จับคู่ Risk-Free Rate กับสกุลเงินและฐานเงินเฟ้อของกระแสเงินสดเสมอ:** สำหรับหุ้นที่กระแสเงินสดเป็น USD ใช้ **US 10Y Treasury Yield** ล่าสุด (เช่น ~4.9% ปลายปี 2026); สำหรับหุ้นสกุลเงินอื่นต้องใช้พันธบัตร 10 ปีของสกุลนั้น (หรือแปลงกระแสเงินสดเป็น USD แล้วบวก Country/FX Risk Spread)

---

## 2. การตั้งค่า Discount Rate (WACC) และ Terminal Multiple อย่างมีวินัย

ห้ามตั้ง WACC ต่ำเกินจริง และห้ามตั้ง Terminal Growth เกิน Nominal GDP ของสกุลเงินนั้น

### ตาราง Calibration: WACC เทียบกับระดับความคาดการณ์ได้ของธุรกิจ (ตัวอย่างฐาน USD เมื่อ US 10Y ≈ 4.9%)
> สูตรตั้งต้น: `WACC ≈ Matched-Currency 10Y Sovereign Yield + Equity Risk Spread (ตามความเสี่ยงธุรกิจ)` ปรับตามโครงสร้างหนี้สุทธิและผู้รับกระแสเงินสด (Unlevered ใช้ WACC, Levered Equity ใช้ Cost of Equity)

| ประเภทความเสี่ยงของธุรกิจ | ตัวอย่าง | Spread เหนือ 10Y Rf | WACC (ฐาน USD ≈ 4.9%) | Terminal Growth (`g_term`) |
| :--- | :--- | :---: | :---: | :---: |
| **Tier 1: Ultra-Predictable Toll-Booth Monopoly** | FICO, Moody's, Visa, Costco | +3.5% – +4.0% | **8.5% – 9.0%** | 3.0% – 3.5% |
| **Tier 2: Wide-Moat Compounder (มี AI / Cyclical Risk บ้าง)** | BKNG, GOOGL, SYK, POOL | +4.0% – +4.6% | **9.0% – 9.5%** | 2.5% – 3.0% |
| **Tier 3: High-Uncertainty Platform / Disruption / Heavy M&A** | UBER (AV Risk), Turnaround | +4.8% – +5.5% | **9.75% – 10.5%** | 2.0% – 2.5% |
| **Tier 4: Emerging Market / Geopolitical / Regulatory Risk** | หุ้นจีน (TCOM), ธุรกิจสัมปทานรัฐ | +6.0% – +7.5% | **11.0% – 12.5%** | 1.5% – 2.5% |

> **กฎเหล็ก Terminal Multiple Check:** หลังจากได้ Terminal Value ด้วย Gordon Growth (`UFCF_10 × (1 + g) / (WACC − g)`) ต้องคำนวณย้อนกลับเสมอว่า **`Implied Exit EV/UFCF` = `1 / (WACC − g)`** สมเหตุสมผลไหม
> * เช่น WACC 9.5%, `g = 3.0%` → Implied Exit EV/UFCF = `15.4x` (สมเหตุสมผลสำหรับธุรกิจโตช้าในอีก 10 ปีข้างหน้า)
> * ถ้า WACC 8.0%, `g = 4.0%` → Implied Exit EV/UFCF = `25.0x` (**อันตราย!** แพงเกินจริงสำหรับธุรกิจปีที่ 10)

---

## 3. เครื่องมือที่ 1: Reverse DCF (Market-Implied Expectations)

### คำถามที่ต้องตอบ
*"ณ Float-Adjusted EV ปัจจุบัน ด้วย WACC และ Terminal Growth ที่อนุรักษ์นิยม บริษัทต้องสร้าง 10Y UFCF CAGR (หรือ Revenue CAGR ภายใต้เส้นทางมาร์จิ้นที่ระบุ) กี่ % ต่อปี เพื่อให้มูลค่าวันนี้เท่ากับราคาตลาดพอดี?"*

> [!IMPORTANT]
> **กฎการรายงาน Reverse DCF (Audit v2–v3):** ตัวเลข "ตลาด Price-in โตกี่ %" ห้ามรายงานลอยๆ ต้องบอก 3 อย่างเสมอ
> 1. **ตัวแปรที่โต:** `(a) UFCF CAGR` (ไม่มีการเปลี่ยนมาร์จิ้น) หรือ `(b) Revenue CAGR` (ภายใต้เส้นทางมาร์จิ้นที่ระบุ)
> 2. **เส้นทางมาร์จิ้น:** เช่น "UFCF margin −100 bps ทยอยลดเท่าๆ กันใน 5 ปี แล้วคงที่"
> 3. **เงินสดไหลออกครั้งเดียว:** เช่น "ค่าปรับ EU \$800M ในปีที่ 2" (ระบุยอดและปี)
>
> *ตัวอย่างจากเคส BKNG @ \$146 (`valuation_engine.py` v3):* (a) UFCF CAGR **+2.27%** | (b) Revenue CAGR, มาร์จิ้นคงที่ + EU \$0.8B = **+2.34%** | −100 bps + EU \$0.8B = **+2.77%** | −300 bps + ค่าปรับ \$2.0B = **+3.80%** — สี่ตัวเลขนี้ **ห้ามเอามาเทียบกันตรงๆ** เพราะตั้งสมมติฐานคนละแบบ

### วิธีตีความผลลัพธ์ (Mauboussin Expectations Framework)
* **Market-Implied 10Y CAGR ต่ำ (เช่น < 3%–4% ทั้งที่รายได้ล่าสุดยังโต 8%–12%):**
  * **ห้ามสรุปอัตโนมัติว่าเป็น "หายนะเชิงโครงสร้าง" หรือ "ตลาดโง่"** — อัตราโตที่ถอดได้ต่ำอาจสะท้อนได้หลายสาเหตุ เช่น ตลาดคิด Discount Rate สูงกว่าเรา, ตลาดมองว่ามาร์จิ้นปลายทางจะหดตัว/ต้องอัด CapEx & ΔNWC เพิ่มเพื่อโต, กำลังอยู่จุดพีควัฏจักร, หรือเสี่ยงถูก Disrupt จริง
  * *หน้าที่นักวิเคราะห์:* เปิดโหมด **Howard Marks Devil's Advocate** (โมดูล `05` §1) เพื่อแยกให้ออกว่าตลาดกังวลเรื่องไหน และหลักฐานจริงสนับสนุนฝั่งใด
* **Market-Implied 10Y CAGR 6%–10%:**
  * ราคาแฟร์ตามการเติบโตปกติ — ต้องชนะด้วย Execution หรือความคาดการณ์ได้สูงมาก
* **Market-Implied 10Y CAGR > 13%–15%:**
  * ตลาดคาดหวังสูงมาก (Priced for Perfection) — Base Rate ของบริษัทขนาดใหญ่ที่โต >15% ต่อเนื่อง 10 ปีต่ำมากตามข้อมูล Mauboussin → **มักให้รอ (Watchlist) หรือ Pass**

---

## 4. เครื่องมือที่ 2: Explicit 10-Year DCF (4 Scenarios + Reinvestment & Cash Drags)

ทุกหุ้นต้องรัน **4 Scenarios** เพื่อเห็นทั้งความไม่สมมาตร (Asymmetry) และจุดแตกหัก โดยทุกกรณีต้องระบุชัดว่า **Revenue, Margin และ Reinvestment (CapEx + ΔNWC)** ตัวไหนเป็นคนขับเคลื่อนอัตราโตของ UFCF:

| Scenario | น้ำหนักแนวคิด | ตัวแปรที่ต้องปรับลด/เพิ่ม |
| :--- | :--- | :--- |
| **1. Bear / Structural Disruption** | ความเสี่ยงขาลงที่เกิดได้จริง (เช่น AI Agent บีบ Take Rate, AV แย่งส่วนแบ่ง, Recession ยาว) | กด Revenue CAGR, กด EBIT Margin ลงสู่ระดับต่ำสุดในอดีต, เพิ่ม Extra CapEx / ΔNWC / Legal Fines |
| **2. Conservative / Floor** | ชะลอตัวชัดเจนกว่าอดีต แต่คูเมืองไม่พัง | โตครึ่งหนึ่งของ Base Rate + มาร์จิ้นหดตัวเล็กน้อย |
| **3. Base Case (Audited)** | สมมติฐานที่อิง Outside View + ข้อเท็จจริงจาก Scuttlebutt + Normalized Margin ที่มีเหตุผลรองรับ | โตตาม Base Rate จริง หักผลกระทบ M&A/Regulatory/CapEx ที่เกิดขึ้นแล้ว |
| **4. Bull Case (Thesis Realized)** | กลยุทธ์หลักสำเร็จ (เช่น Direct Mix สูงขึ้น, AI ลดต้นทุนจริง, Operating Leverage ทำงาน) | โตตามเป้าผู้บริหารแต่ยังไม่เกิน Base Rate โครงสร้างอุตสาหกรรม |

### กฎเหล็ก Reinvestment & Explicit Cash Drags
1. **Growth Cannot Be Free (Implied Reinvestment Sanity Check):** ทุก Scenario ต้องเช็ก `Implied Reinvestment Rate = g / Assumed Incremental ROIC` (รันให้อัตโนมัติใน `valuation_engine.py`) — หากธุรกิจ ROIIC 15% แต่อยากโต 12%/ปี แปลว่าต้องนำกำไรถึง 80% กลับไปลง CapEx + ΔNWC (ห้ามโมเดลว่าโต 12% โดยไม่ต้องเพิ่มทุนหมุนเวียนหรือ CapEx!)
2. **Pending M&A Cash Outflow:** หากบริษัทประกาศซื้อกิจการด้วยเงินสด/หนี้เพิ่มแล้วแต่ยังไม่ปิดดีล ต้องหักเงินสดจ่ายสุทธิ (หรือเพิ่ม Net Debt) ทันที — *ระวังอย่าหักซ้ำทั้งใน EV และ `pv_cash_drag`*
3. **Regulatory Fines / Litigation Settlement:** ใส่เป็น `One-time Cash Outflow` ในปีที่คาดว่าจะจ่ายจริง (ถ้าใส่ใน Float-Adj EV แล้ว ห้ามหักซ้ำใน `pv_cash_drag`)
4. **AI / Maintenance CapEx Surge:** ใช้ CapEx Run-Rate ใหม่ที่เกิดขึ้นจริง ไม่ใช่ค่าเฉลี่ยอดีต
5. **มูลค่าปลายทางแยกตาม Scenario (v4):** ห้ามใช้การโตตลอดไป 2.5% เท่ากันทุกกรณีโดยอัตโนมัติ — ใน `inputs/TICKER.json` แต่ละ scenario กำหนด `terminal_growth` หรือ `exit_ev_ufcf_multiple` ของตัวเองได้ (เลือกอย่างใดอย่างหนึ่ง) เช่น กรณีหมีของธุรกิจที่เสี่ยงถูก AI ตัดตอนใช้โต 0% หรือตัวคูณ 8–10 เท่า
   * **ห้ามฮาร์ดโค้ดกรณีหมี = −50% เท่ากันทุกหุ้น:** ความลึกของกรณีหมีต้องมาจากกลไกของธุรกิจนั้น (margin, หนี้, มูลค่าปลายทาง) ไม่เช่นนั้นอัตราได้ต่อเสียจะแยกหุ้นคุณภาพออกจากหุ้นหนี้สูงไม่ได้ — ตัวเลข −50% ใช้ใน pre-mortem (โมดูล `05` §4) เพื่อหาสาเหตุที่พัง ไม่ใช่ใส่เป็นค่าคงที่ในโมเดล

---

## 5. เครื่องมือที่ 3: Self-Consistent 5-Year Forward IRR (Dated Cash Flows + Cash Ledger)

นี่คือเครื่องมือชี้ชะตาของ **François Rochon** (เป้า 2x ใน 5 ปี ≈ 15% CAGR) และ **Dev Kantesaria** เพราะบังคับให้เห็น **3 เครื่องยนต์ของผลตอบแทน** แยกจากกันชัดเจน:

$$\text{Price}_5 = \underbrace{\text{FCF/Share}_0 \times \left(1 + g_{\text{FCF}}\right)^5}_{\text{1. Fundamental Growth}} \times \underbrace{\left(\frac{S_0}{S_5}\right)}_{\text{2. Net Share Reduction}} \times \underbrace{M_{\text{Exit}}}_{\text{3. Exit Multiple}}$$

$$0 = -P_0 + \sum_{t=1}^{5} \frac{D_t}{(1+\text{IRR})^t} + \frac{\text{Price}_5}{(1+\text{IRR})^5}$$

> [!WARNING]
> **กฎเหล็ก 2 ข้อจาก External Audit (v2–v3):**
> 1. **ห้ามรวบปันผลไปปลายปีที่ 5:** ต้องคำนวณ IRR จากกระแสเงินสดลงวันที่ตามปลายปีที่ได้รับปันผลจริงเสมอ
> 2. **บังคับตรวจ 5-Year Cash Ledger (ห้ามจ่ายปันผลลอยๆ เกินแหล่งเงิน!):** ทุกปีต้องไล่งบเงินสด `Beg Free Cash (ex-Float) + Clean FCF − Cash Drag − Dividends − Buybacks = End Free Cash`
>    * นโยบายเริ่มต้น (`strict_fail`): หากปันผลที่วางแผนไว้เกินเงินสดที่มี (ต้นปี + FCF สุทธิ) โมเดลต้อง **ปฏิเสธการแสดง IRR** และแจ้ง `INFEASIBLE_UNFUNDED_DIVIDEND` พร้อมยอดเงินขาดทันที
>    * หากต้องการทดสอบกรณีบริษัทตัดปันผลให้เลือก `cap_to_available_cash` หรือหากยอมกู้เงินจ่ายปันผลให้เลือก `external_debt_funded` (ซึ่งจะบวกหนี้เพิ่ม + ดอกเบี้ย และหักออกจากมูลค่าหุ้นปลายปีที่ 5 ตรงๆ)

### กฎเหล็ก 3 ข้อของ Self-Consistent 5Y IRR
1. **Self-Funded Buybacks Only (ห้ามกู้เงินมาซื้อหุ้นคืน):**
   * เงินซื้อหุ้นคืนต้องมาจากเงินสดส่วนเกินรายปีหลังหักปันผลและ Cash Drags แล้วเท่านั้น (`Clean FCF` ที่หัก SBC แล้ว) และคำนวณจำนวนหุ้นลดลงแบบ **Geometric Year-by-Year** ตามเส้นทางราคาในอนาคต
2. **บังคับรายงาน "Constant-Multiple Case (Exit Multiple = Entry Multiple)":**
   * *(เปลี่ยนชื่อจาก "Zero-Rerating Floor" ใน v3 เพื่อไม่ให้เข้าใจผิดว่าเป็นพื้นขาลงที่รับประกัน — Multiple ยังหดตัวลงต่อได้เสมอ)*
   * คือกรณีสมมติว่า **ตลาดให้ Multiple ปีที่ 5 เท่ากับ Multiple ที่คุณจ่าย ณ วันเข้าซื้อพอดี** เพื่อวัดว่าผลตอบแทนจากการเติบโต + ซื้อหุ้นคืน + ปันผลเพียงพอชนะพันธบัตร 10 ปีโดยไม่ต้องพึ่งการ Re-rate หรือไม่
3. **แยก Multiple De-rating Case:**
   * ทดสอบเสมอว่าถ้า Multiple หดตัวอีก 15%–25% ผลตอบแทน 5 ปียังรับได้ไหม

---

## 6. เครื่องมือที่ 4: "Required Growth Table" (ตารางตอบคำถาม: ซื้อวันนี้ต้องโตกี่ %?)

เวลาจะตัดสินใจกดซื้อจริง นักลงทุนต้องการคำตอบตรงไปตรงมาว่า:
> **"ณ ราคาวันนี้ ถ้าฉันต้องการผลตอบแทน 10%, 12% หรือ 15% ต่อปีในอีก 5 ปีข้างหน้า — บริษัทต้องทำ Clean FCF และ Revenue โตปีละกี่ %?"**

ให้สร้างตารางมาตรฐานนี้ทุกครั้งก่อนสรุป Action Plan (รันอัตโนมัติได้จาก `valuation_engine.py`):

| กรณี Exit Multiple ในปีที่ 5 | เป้า 5Y IRR = **10%/ปี** (Bare Minimum) | เป้า 5Y IRR = **12%/ปี** (Institutional Target) | เป้า 5Y IRR = **15%/ปี** (Rochon Double in 5Y) |
| :--- | :--- | :--- | :--- |
| **De-rating (−15% Multiple)** | ต้องโต FCF `X%` (Rev `Y%`) | ต้องโต FCF `X%` (Rev `Y%`) | ต้องโต FCF `X%` (Rev `Y%`) |
| **Constant-Multiple Case (1.00x)** | ต้องโต FCF `X%` (Rev `Y%`) | ต้องโต FCF `X%` (Rev `Y%`) | ต้องโต FCF `X%` (Rev `Y%`) |
| **Mild Re-rating (+15% Multiple)** | ต้องโต FCF `X%` (Rev `Y%`) | ต้องโต FCF `X%` (Rev `Y%`) | ต้องโต FCF `X%` (Rev `Y%`) |

---

## 7. เพดานราคาเข้าซื้อหุ้นเดี่ยว (Single-Stock Entry Ceilings — v4: 2 เลนส์ราคา + ด่านผลตอบแทน)

> [!IMPORTANT]
> **ขอบเขตของหมวดนี้:** กำหนดเฉพาะ **"เพดานราคาของหุ้น 1 ตัว"** — **ไม่กำหนดสัดส่วน % พอร์ต** กติกาขนาดพอร์ตทั้งหมดยึด **[05-PORTFOLIO-SIZING-RISK-SELL-DISCIPLINE.md](./05-PORTFOLIO-SIZING-RISK-SELL-DISCIPLINE.md) §2** เพียงแห่งเดียว

> [!WARNING]
> **ทำไม v4 ถอดเลนส์ B ออกจากเพดานราคา:** ผลตอบแทน 5 ปีแบบตัวคูณคงที่แทบไม่ขึ้นกับราคาซื้อ (ตัวอย่าง BKNG รุ่นทดสอบ: ซื้อ \$146 ได้ 13.3%, ซื้อ \$200 ยังได้ 11.3%) มันจึงวัด "อัตราโต" ไม่ใช่ "ราคา" — เมื่อใช้เป็นเพดาน อัตราโตเปลี่ยนแค่ ±1 จุด เพดานไม้แรกแกว่งจาก \$176 ถึง \$270 และยังทำให้ข้อยกเว้น "ผ่าน 2 ใน 3 เลนส์" กลายเป็นช่องโหว่ เพราะเลนส์ B แทบผ่านเสมอ

| ระดับเพดานราคา | Lens A: ส่วนเผื่อความปลอดภัยเทียบมูลค่ากรณีฐาน | Lens C: อัตราได้ต่อเสีย (ขึ้นถึงกรณีฐาน : ลงถึงกรณีหมี) | ด่านผลตอบแทน 5 ปี ณ ราคาวันนี้ (ตัวคูณคงที่) | ต่อยอดสู่โมดูล `05` |
| :--- | :---: | :---: | :---: | :--- |
| **Watchlist** | ไม่ผ่านเพดาน Starter หรือไม่ผ่านด่านผลตอบแทน | — | — | `Tier 0` (0%) |
| **Starter** | **≥ 15%** | **≥ 2.0 : 1** | **≥ 11%** | `Tier 1–2` |
| **Core** | **≥ 25%** | **≥ 3.0 : 1** | **≥ 13%** | `Tier 3` |
| **Fat Pitch** | **≥ 35%** | **≥ 4.0 : 1** | **≥ 15%** | `Tier 4` |

### กฎผูกมัด (v4)
1. **เพดานราคา = `min(Lens A, Lens C)`** — 2 เลนส์ที่ขึ้นกับราคาจริงเท่านั้น และต้องบอกเสมอว่าเลนส์ไหนผูกมัด
2. สูตร Lens C ปิดรูป: `ราคาเพดาน = (มูลค่ากรณีฐาน + k × มูลค่ากรณีหมี) / (1 + k)` เมื่อ `k` = อัตราได้ต่อเสียขั้นต่ำ
3. **ด่านผลตอบแทน (Quality/Growth Hurdle Gate):** ผลตอบแทน 5 ปีแบบตัวคูณคงที่ **ณ ราคาวันนี้** ต้องไม่ต่ำกว่าเกณฑ์ของขั้นนั้น — ถ้าต่ำกว่า 11% ไม่ผ่าน Starter แม้ราคาจะต่ำกว่าเพดาน (กันกรณีราคาถูกแต่ธุรกิจหดตัว = กับดักมูลค่า) ตาราง Cash Ledger 5 ปีและตาราง Required Growth ยังต้องรายงานทุกครั้ง
4. **ห้ามประกาศเพดานราคาระดับเซนต์:** ต้องรายงานเป็น **ช่วงราคาปัดเศษ** (อัตราโตกรณีฐาน ±1 จุด) พร้อม **ตารางความอ่อนไหว ±1 และ ±2 จุด** ซึ่ง `valuation_engine.py` v4 สร้างให้อัตโนมัติ
5. **ไม่มีข้อยกเว้น "ผ่าน 2 ใน 3 เลนส์" อีกต่อไป** — ไม่ผ่าน = Watchlist (0%)
6. ฟังก์ชัน `solve_price_for_constant_multiple_irr()` (สถานะ `SOLVED / IMPOSSIBLE / UNBOUNDED_PASS / INFEASIBLE_CASH_PLAN`) ยังเก็บไว้ใช้ตอบคำถาม "ราคาเท่าไรถึงได้ IRR x%" แต่ **ห้ามนำผลไปเป็นเพดานราคา**

---

## 8. วิธีใช้งานคู่กับ `valuation_engine.py` (v4)

1. **ตัวเลขทุกตัวอยู่ใน `inputs/TICKER.json`** (ตัวอย่างต้นแบบ: `inputs/BKNG.json`) — ข้อเท็จจริงทุกตัวต้องมี `as_of_date` + (`source_url` หรือ `filing_ref`) + `verification` (`verified` / `partially_verified` / `carried_over_unverified`) และสมมติฐานทุกตัวต้องมี `rationale` ไม่ครบ = สคริปต์ไม่ยอมรัน
2. รันรายงาน: `python3 os-modules/valuation_engine.py --input inputs/BKNG.json`
3. สร้างบล็อกสรุปลงบทวิเคราะห์/README/INDEX: `python3 tools/sync_summaries.py --write` — **ห้ามพิมพ์ตัวเลขสรุปเองด้วยมือ** CI จะรัน `--check` และไม่ให้ผ่านถ้าตัวเลขไม่ตรงกับสคริปต์
4. รันชุดทดสอบ: `python3 os-modules/valuation_engine.py --self-test` (9 เคสเดิมจาก v3 + เคส v4)
5. หากใช้งานบน **AI ที่รัน Python ไม่ได้**: ให้คัดลอกสูตรจาก `valuation_engine.py` สั่งให้ AI แสดงวิธีทำทีละบรรทัด แล้วตรวจทานบนเครื่องตัวเองก่อนสร้าง JSON
