# 01 — Forensic Accounting & Quality Autopsy Manual (50% Quantitative)

*กรอบหลัก: Terry Smith (Fundsmith) • Dev Kantesaria (Valley Forge) • Pulak Prasad (Nalanda) • Michael Mauboussin (Counterpoint Global)*

---

## 1. ด่านคัดทิ้ง 5 นาทีแรก (Phase 1 — Darwinian Kill Filters)
ก่อนเสียเวลาทำโมเดล DCF ให้ตรวจ 5 ข้อนี้ — **หากตก Governance หรือตก ≥ 2 ข้อ ให้ PASS ทันที:**

| ด่านตรวจ | เกณฑ์ผ่าน (Pass Criteria) | สัญญาณคัดทิ้งทันที (Instant Kill — เคสจริง) |
| :--- | :--- | :--- |
| **1. งบดุล & หนี้สิน** | `Net Debt (รวม Operating Leases) / EBITDA < 2.5x` หรือ `Interest Coverage > 8x` | หนี้พุ่ง >3.5x หลังกู้เงินทำ M&A ก้อนโต + เรตติ้งติด Negative Outlook *(เคสจริง: `BSX` หลังดีล Penumbra \$14.5B)* |
| **2. คุณภาพกำไร & ROCE** | `GAAP ROCE ≥ 20%` (หรือ Core Operating ROCE ≥ 25% สำหรับธุรกิจที่มีเงินสด/เงินลงทุนก้อนใหญ่) | ROCE < 12% ต่อเนื่อง, Margin ผันผวนหนักตามสินค้าโภคภัณฑ์, หรือต้องอัด CapEx >15% ของรายได้เพื่อรักษาฐานเดิม |
| **3. ไม่พึ่งปาฏิหาริย์** | โตได้ด้วย Organic Core + Reinvestment ปกติ | ต้องพึ่ง Turnaround, ปรับโครงสร้างซ้ำซาก, หรือ Serial Roll-Up M&A ที่ซ่อนการเติบโตจริง |
| **4. ธรรมาภิบาล (Governance)** | ผู้บริหารโปร่งใส ไม่ปั้น Adjusted EBITDA กลบขาดทุนจริง ไม่แจก SBC เอาเปรียบ | เปลี่ยนคำนิยาม Non-GAAP ไปมา, หั่นเป้ารายได้/กำไร 3 รอบติด, ผู้บริหารลาออกกะทันหันโดยไม่ชี้แจงพร้อมเลื่อน Investor Day |
| **5. 10-Year Predictability** | มองภาพโครงสร้างอุตสาหกรรมอีก 7–10 ปีออก | ธุรกิจถูกเทคโนโลยีใหม่ขนาบจนคาดเดาส่วนแบ่งตลาด/Take Rate ไม่ได้เลย (Too Hard Pile) |

---

### 1.1 ด่านบังคับ v4: กำแพงหนี้ครบกำหนด 3–5 ปี (Debt Maturity Wall)
อัตราส่วนหนี้ต่อ EBITDA บอกแค่ขนาดหนี้ ไม่บอกว่า **ต้องหาเงินมาคืนเมื่อไหร่และที่ดอกเบี้ยเท่าไร** — ทุกบทวิเคราะห์ต้องมีตารางนี้ (ข้อมูลอยู่ในหมายเหตุประกอบงบเรื่องหนี้ใน 10-K/10-Q):

| ปี | หนี้ครบกำหนด ($M) | ดอกเบี้ยเดิม | ดอกเบี้ยถ้ารีไฟแนนซ์วันนี้ | FCF + เงินสดที่ใช้คืนได้ | ต้องรีไฟแนนซ์ไหม |
| :---: | :---: | :---: | :---: | :---: | :---: |
| ปี 1–5 | | | | | |

* **สัญญาณอันตราย:** หนี้ครบกำหนดใน 3 ปีเกิน 1.5 เท่าของ FCF รายปี, ดอกเบี้ยรีไฟแนนซ์สูงกว่าเดิม 2 จุดขึ้นไปจนกำไรต่อหุ้นหาย ≥ 5%, หรือมีภาระเงินลูกค้า (float) ที่อาจไหลออกพร้อมกันในขาลง
* **ผลต่อโมเดล:** ส่วนต่างดอกเบี้ยหลังรีไฟแนนซ์ต้องใส่เป็นต้นทุนใน `inputs/TICKER.json` (เช่น ผ่าน `pv_cash_drag` หรือ `ttm_net_interest_expense` ปรับใหม่) ไม่ใช่แค่เขียนเป็นข้อสังเกต

---

## 2. สูตรคำนวณมาตรฐานเชิงนิติเวช (Mandatory Forensic Formulas)

### 2.1 Enterprise Value แบบปรับปรุงเต็มรูปแบบ (Float-Adjusted EV)
```text
Diluted Market Cap    = Stock Price × Latest Diluted Shares Outstanding
Total Debt & Leases   = Short-Term Debt + Long-Term Debt + Current & Non-Current Operating Leases
Standard EV           = Diluted Market Cap + Total Debt & Leases + Non-Controlling Interests (NCI) − Unrestricted Cash & ST Investments

Float-Adjusted EV     = Standard EV
                        + Customer/Partner Float ในเงินสด (เช่น Deferred Merchant Bookings, Unfunded Insurance Reserve Gap)
                        + หนี้ค่าปรับ/เงินชดเชยทางกฎหมายที่ตั้งสำรองแล้วรอจ่ายเงินสดจริง (เช่น FTC/SAMR/EU Fine)
                        − Non-Operating Strategic Equity Stakes (หัก Haircut 25%–30% สำหรับภาษีและสภาพคล่อง — ห้ามหักหุ้นที่เป็นเงินมัดจำดีล M&A!)
```

### 2.2 กระแสเงินสดอิสระที่แท้จริง (True FCF & Clean Economic FCF)
```text
Reported FCF          = Operating Cash Flow (OCF) − Capital Expenditures (CapEx)
True FCF              = Reported FCF − Stock-Based Compensation (SBC) − Finance Lease Principal Repayments
Clean Economic FCF    = True FCF − Non-Sustainable Working Capital / Customer Float Windfalls
                        (เช่น ยอดเพิ่มของ Accrued Insurance Reserves, Excess Deferred Merchant Bookings, หรือการระบายสต็อกครั้งเดียว)
```

### 2.3 True Unlevered FCF & สะพานกระทบยอดบัญชี (OCF ↔ P&L Reconciliation Bridge)
```text
ฝั่ง P&L (ใช้ใน 10Y DCF & Reverse DCF — ตรงกับ valuation_engine.py v3):
Core GAAP EBIT        = Reported Operating Income ± เฉพาะรายการครั้งเดียวจริงๆ (เช่น ค่าปรับ FTC, Impairment)
                        *หมายเหตุ: GAAP EBIT หัก SBC และ D&A ไว้ครบแล้ว*
NOPAT                 = Core GAAP EBIT × (1 − Normalized Effective Cash Tax Rate)
True Unlevered FCF    = NOPAT + Depreciation (ex-acquisition amortization) − CapEx − Normalized ΔNWC
                        *Normalized ΔNWC = การเพิ่มขึ้นสุทธิของสต็อก + ลูกหนี้การค้า − เจ้าหนี้การค้า (ไม่รวม Customer Float)*

สะพานกระทบยอดบังคับ (Mandatory Reconciliation Bridge):
1. ฝั่งงบกระแสเงินสด (Cash-Flow Path): Clean Economic FCF = OCF − CapEx − SBC − Float/WC Windfall
   *(จำไว้ว่า OCF หัก −ΔNWC_normal, ดอกเบี้ยจ่ายสุทธิ และภาษีเงินสดไว้แล้ว)*
2. ฝั่ง P&L (Implied Levered FCF):    P&L Levered FCF    = True Unlevered FCF − (Net Interest Expense × (1 − Tax Rate))
3. ส่วนต่าง (Reconciliation Gap):     Gap = Clean Economic FCF − P&L Levered FCF
   *ถ้า |Gap| > 5% ของ UFCF ต้องไล่ชี้แจงที่มาทุกบรรทัด (Cash vs Book Tax, Deferred Tax, Lease Principal, หรือการหัก ΔNWC/Float ซ้ำซ้อน!)*
```

> **เช็กลิสต์กันหักซ้ำ (No Double-Counting Audit — ไล่จากงบถึงมูลค่าต่อหุ้น):**
> * **SBC:** หักใน `Core GAAP EBIT` แล้ว (ฝั่ง P&L) → **ห้าม** หักซ้ำอีกตอนคำนวณ UFCF; แต่ต้องหักออก 100% จาก `OCF` (ฝั่ง Cash-Flow) เพราะ OCF บวกกลับ SBC ไว้
> * **Customer Float:** หักยอดเพิ่มรายปีออกจาก `OCF` (ฝั่ง Clean FCF) และกันเงินสดคงค้างออกจาก `Free Cash` (ใน Float-Adj EV) — แต่ **ห้าม** เอาไปใส่ใน `Normalized ΔNWC` ซ้ำอีก
> * **Operating Leases:** หากรวมหนี้เช่าไว้ใน `Total Debt` (EV) แล้ว ต้องตรวจไม่ให้นับค่าเช่าซ้ำทั้งใน EV และ Cash Flow
> * **One-Off Fines (เช่น FTC/EU):** หากบวกเป็นหนี้รอจ่ายใน `Float-Adj EV` แล้ว **ห้าม** หักซ้ำอีกใน `pv_cash_drag` ของ DCF
> * **ฐานอ้างอิง & Base Rate:** ก่อนตั้งประมาณการต้องกำหนดเกณฑ์เลือกกลุ่มเทียบ (รวมคู่แข่งที่ล้มเหลว/ถูก Disrupt เพื่อเลี่ยง Survivorship Bias) และหากใช้ปี 2018–2019 เป็นฐานมาร์จิ้นต้องระบุเหตุผลว่าทำไมโครงสร้างต้นทุน/ส่วนผสมสินค้ายุคปัจจุบันจึงเทียบกับปีนั้นได้

### 2.4 คุณภาพผลตอบแทนต่อทุน (ROCE & ROIC)
```text
Capital Employed      = Total Assets − Total Current Liabilities
GAAP ROCE             = GAAP EBIT / Average Capital Employed
Tangible ROCE         = Core EBIT / (Capital Employed − Goodwill − Acquired Intangibles)
All-in ROIC           = NOPAT / (Total Equity + Total Debt + Operating Leases − Unrestricted Cash)
Cash Conversion       = OCF / Net Income (เกณฑ์ Terry Smith: ≥ 95% เฉลี่ย 3–5 ปี)
```
*หมายเหตุเรื่อง Negative Equity:* หุ้นที่ซื้อหุ้นคืนหนักจน Stockholders' Equity ติดลบ (เช่น `BKNG`, `HLT`, `MCD`) จะทำให้ ROE ไร้ความหมายและ ROCE ดูสูงเว่อร์ → ให้ดู **Cash Conversion, EBIT Margin และ Incremental ROIC** ประกอบเสมอ

---

## 3. 10 กับดักบัญชีที่เจอบ่อยที่สุดในสนามจริง (Battle-Tested Traps)

| # | กับดักบัญชี (Forensic Trap) | วิธีจับผิด (How to Catch It) | บทเรียนจากเคสจริง |
| :---: | :--- | :--- | :--- |
| **1** | **Adjusted EBITDA Mirage** | เทียบ GAAP Operating Income กับ Adj. EBITDA — ถ้าช่องว่าง >25%–30% ให้ชำแหละว่าตัดอะไรออกบ้าง (SBC? Legal settlements ที่เกิดซ้ำทุกปี?) | `UBER`: Adj. EBITDA สูงกว่า GAAP EBIT ถึง +53% เพราะตัด SBC \$2.1B + ค่าปรับกฎหมายที่เกิดซ้ำทุกปี |
| **2** | **Insurance / Customer Float Distortion** | ขุดบรรทัด Changes in Operating Assets & Liabilities ในงบกระแสเงินสดว่า OCF โป่งจากเงินมัดจำลูกค้าหรือสำรองประกันภัยกี่ % | `UBER`: Insurance Reserve Float เคยคิดเป็น 39.5% ของ OCF (FY24) และสำรองรวม (\$13.7B) ทะลุ Restricted Assets (\$11.4B) ไปแล้ว \$2.34B |
| **3** | **Cherry-Picking Working Capital** | ห้ามดูแค่บรรทัด Inventory หรือ Deferred Revenue บรรทัดเดียว! ต้องรวมทุกบรรทัด Working Capital (AR + Inv + AP + Accrued) เพื่อดู **Net WC** จริง | `POOL`: Inventory ลดลง +\$265M ดูเหมือนโป่ง OCF แต่ถูกหักกลบด้วย AP (-\$225M) และ AR (-\$134M) จน Net WC จริงติดลบ -\$11.6M! |
| **4** | **Double-Counting M&A Down Payments in EV** | ห้ามหักมูลค่าหุ้นพันธมิตรออกจาก EV หากหุ้นนั้นเป็น **"เงินวางมัดจำ"** เพื่อเทกโอเวอร์บริษัทนั้นทั้งก้อน | `UBER`: หุ้น+TRS Delivery Hero มูลค่า \$4.85B คือเงินมัดจำดีลซื้อ \$14.8B ห้ามหักเป็น Excess Investments |
| **5** | **Gross vs. Net Interest Double-Counting** | บริษัทที่ถือเงินสดมหาศาลจะมี Interest Income สูง หากบวกกลับ Gross Interest Expense เข้า Levered FCF จะทำให้ Unlevered FCF โป่งเกินจริง | `BKNG`: ถือเงินสด \$15.8B ได้ดอกเบี้ยรับ ~\$815M/ปี (Net Interest แค่ ~\$300M ไม่ใช่ \$1,113M) การบวก Gross Interest ทำให้ Reverse DCF เพี้ยนจาก 2.7% เหลือ 1.25% |
| **6** | **Pre-COVID Margin Anchoring** | เช็ก Operating Margin ปี **2018–2019** เสมอ อย่าหลงนึกว่ามาร์จิ้นวันนี้ที่ต่ำกว่าจุดพีคโควิด (2021–2022) คือ "จุดต่ำสุดของวัฏจักร" | `POOL`: EBIT Margin ปี 2026 (10.7%) ต่ำกว่าพีคโควิด (16.6%) แต่แท้จริง **10.7% คือ Record สูงสุดตลอดกาลยุคก่อนโควิด (ปี 2019)!** |
| **7** | **Hidden Holding / Unallocated Losses** | ในบริษัทหลายกลุ่มธุรกิจ อย่าดูแค่ Segment Margin หน้างาน ให้เปิดหมายเหตุ 10-Q ดูบรรทัด **Corporate / Unallocated / Alphabet-level Losses** | `GOOGL`: Services Margin โชว์สวย 40.7% แต่หมายเหตุ 10-Q Q3'26 โชว์ขาดทุน Alphabet-level activities พุ่ง +71.4% เป็น -\$7.66B |
| **8** | **Buyback Illusion & Capital Destruction** | คำนวณ `เงินซื้อหุ้นคืนรวม ÷ จำนวนหุ้น Diluted ที่ลดลงสุทธิ` = ต้นทุนจริงต่อ 1 หุ้นที่ลดได้ แล้วเทียบราคาตลาดวันนี้ | `POOL` ซื้อคืนเฉลี่ย ~\$355 (ขาดทุน MTM -41%); `BKNG` ซื้อเฉลี่ย \$177–\$198; `UBER` จ่าย \$118.57 ต่อ 1 หุ้นที่ลดได้สุทธิ |
| **9** | **CapEx & Depreciation Lag (AI / Asset-Heavy Creep)** | เช็ก CapEx ที่พุ่งแรงในปีนี้ เพราะค่าเสื่อม (Depreciation) จะไล่ตามมาทุบ GAAP EBIT ในอีก 1–3 ปีข้างหน้า และเช็กว่าบริษัทเปลี่ยนอายุการใช้งานเซิร์ฟเวอร์หรือไม่ | `GOOGL` / Hyperscalers (AI CapEx โป่ง); `UBER` เริ่มรับรถ AV ยุคแรกขึ้นงบดุล |
| **10** | **Receivables & Allowance Divergence** | หากลูกหนี้การค้าโตเร็วกว่ายอดขาย >1.5x–2x และ Allowance for Doubtful Accounts พุ่ง >20% YoY = สัญญาณลูกค้าเริ่มขาดสภาพคล่องหรืออัดยอด (Channel Stuffing) | `POOL` Q3'26: ลูกหนี้โต +7.9% (2 เท่าของยอดขาย +3.7%) และ Allowance พุ่ง +24.1% YoY |

---

## 4. เช็กลิสต์บัญชีเฉพาะตามประเภทอุตสาหกรรม (Sector-Specific Audit)

* **Platforms / Marketplaces / OTAs (`UBER`, `BKNG`, `ABNB`, `TCOM`):** ตรวจ Gross Bookings vs Revenue (Take Rate trend + การเปลี่ยนบัญชี Agency→Merchant/VAT), Customer Float (Deferred Bookings / Insurance Reserves), Marketing % of Gross Bookings (Organic vs Paid), และ SBC/FCF
* **Big Tech / Cloud / AI (`GOOGL`, `MSFT`, `AMZN`):** ตรวจ AI CapEx % of OCF, การยืดอายุค่าเสื่อม (Useful Life extension), Unallocated Corporate R&D/AI losses, SBC Dilution จริง, และ ROIC บนเงินลงทุน AI ก้อนใหม่ (Incremental ROIC)
* **Distributors & Industrials (`POOL`, `FAST`, `FERG`):** ตรวจ Price vs Volume growth breakdown, Pre-COVID Operating Margin ceiling, Inventory Turns, Receivables/Allowance, และ Operating Lease Liabilities
* **MedTech & Healthcare (`SYK`, `MDT`, `BSX`, `ISRG`):** ตรวจ Organic Constant-Currency Growth (แยก M&A ออก), Acquisition-related Amortization & Restructuring charges ที่เกิดซ้ำทุกปี (ห้ามมองข้ามเป็น Non-recurring), Net Debt/EBITDA หลังดีล M&A, และ R&D % of Sales
* **Asset-Light Hotel Franchisors (`MAR`, `HLT`, `IHG`, `WH`, `CHH`, `ATAT`):** แยก **Fee Revenue** ออกจาก **Reimbursed Cost Revenue** (ซึ่ง Margin = 0%), ตรวจ Net Unit Growth (NUG), RevPAR, Negative Equity / Leverage Ratio, และ Key Money (เงินอุดหนุนเจ้าของโรงแรม)
* **Hard-Asset Monopolies / Airports (`ASR`, `PAC`, `AENA`):** ตรวจ Concession Expiration Year, Regulated Aeronautical Tariff Cap vs High-Margin Commercial/Duty-Free Revenue per Passenger, Maintenance vs Expansion CapEx (Master Development Program), และ FX / Political Risk
