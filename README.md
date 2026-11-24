# สภานักลงทุนปัจจัยพื้นฐาน (Fundamental Investor Council — Deep-Dive Edition)

คลังความรู้และระบบปฏิบัติการทางความคิด (Mental Models & Institutional Playbooks) ของ **17 นักลงทุนและนักคิดสายปัจจัยพื้นฐานระดับโลก** ออกแบบมาโดยเฉพาะเพื่อใช้เป็น **"สภาช่วยคิดวิเคราะห์หุ้น"** ที่ลงลึกถึงระดับแผลเป็นในสนามจริง, สูตรการคำนวณและปรับงบการเงิน, เคสชนะระดับตำนานและเคสพลาดจริง, วินัยการให้น้ำหนักพอร์ตและกฎการขาย, ไปจนถึงคู่มือสวมหมวกคิดทีละขั้น (Step-by-Step Mental Simulation)

---

## เริ่มต้นใช้งานตรงไหน?

### 1. ชุด Modular Portable Investing OS (`os-modules/` — แนะนำสูงสุดสำหรับโยนเข้าแอป AI อื่น)
ชุดไฟล์แยกโมดูลที่ออกแบบมาเพื่อนำไปใช้งานบน **Claude Projects, ChatGPT Projects, Gemini Gems, Cursor, Obsidian หรือ NotebookLM** โดยไม่เกิด Context Dilution:
* [00-START-HERE-SYSTEM-PROMPT.md](./os-modules/00-START-HERE-SYSTEM-PROMPT.md) — **Master System Prompt & Router** (ก๊อปปี้ไปใส่ช่อง Custom Instructions)
* [01-FORENSIC-ACCOUNTING-MANUAL.md](./os-modules/01-FORENSIC-ACCOUNTING-MANUAL.md) — คู่มือผ่าตัดงบการเงิน, Kill Filters, สูตร Clean FCF / Float-Adj EV / Direct P&L UFCF และ **10 กับดักบัญชีจากสนามจริง**
* [02-GRASSROOTS-SCUTTLEBUTT-FIELD-GUIDE.md](./os-modules/02-GRASSROOTS-SCUTTLEBUTT-FIELD-GUIDE.md) — คู่มือขุดข้อมูลนอก Official (`Reddit`, เว็บบอร์ดสายอาชีพ, Glassdoor/Blind, Trustpilot) พร้อม Query แยกรายอุตสาหกรรม + 5 Qualitative Pillars
* [03-VALUATION-DCF-IRR-TEMPLATES.md](./os-modules/03-VALUATION-DCF-IRR-TEMPLATES.md) — WACC Calibration, Reverse DCF, 4-Scenario 10Y DCF, Self-Consistent 5Y IRR (Zero-Rerating Floor) และตาราง **Required Growth**
* [04-SPLIT-BRAIN-DEBATE-PROMPTS.md](./os-modules/04-SPLIT-BRAIN-DEBATE-PROMPTS.md) — ชุด Prompt สำเร็จรูปสำหรับ **Cross-App Split-Brain Debate 3 รอบ**, สแกนเร็ว 3 นาที, ดวลหุ้นตัวต่อตัว และตรวจงบหลังประกาศผล
* [05-PORTFOLIO-SIZING-RISK-SELL-DISCIPLINE.md](./os-modules/05-PORTFOLIO-SIZING-RISK-SELL-DISCIPLINE.md) — Howard Marks Devil's Advocate Check (*"ทำไมตัวเลขถึงดูดีเกินจริง?"*), Position Sizing, Correlation Cap, 5Y Pre-Mortem และกฎขาย 4 ข้อ
* [valuation_engine.py](./os-modules/valuation_engine.py) — สคริปต์ Python สำเร็จรูป (Zero Dependencies) สำหรับรันตัวเลข Valuation ทั้งหมดแบบตรวจสอบได้ 100%
* [inputs/](./inputs/) — **(v4)** ไฟล์ตัวเลขของแต่ละหุ้น (`TICKER.json`) ตัวเลขทุกตัวมีแหล่งอ้างอิง วันที่ และสถานะการตรวจ เป็นแหล่งความจริงเดียวของตัวเลขในบทวิเคราะห์
* [tools/sync_summaries.py](./tools/sync_summaries.py) — **(v4)** เขียนบล็อกสรุปจากสคริปต์ลงบทวิเคราะห์/README/INDEX และใช้ใน CI เพื่อจับตัวเลขที่ไม่ตรงกัน (`--check`)
* *(หรือฉบับสรุปรวม 1 ไฟล์อ่านเร็ว: [INVESTOR-THINKING-OS.md](./INVESTOR-THINKING-OS.md))*

### 2. คู่มือ 6 เฟส, โปรไฟล์นักลงทุน 17 ท่าน และคลังบทวิเคราะห์จริง
* **ต้องการวิเคราะห์หุ้นจริง 1 ตัวแบบครบ 6 เฟส:** เปิด [master-playbook-stock-analysis.md](./master-playbook-stock-analysis.md)
* **ต้องการสวมหมวกคิดแบบนักลงทุนคนใดคนหนึ่งแบบเจาะลึก:** เลือกจาก 17 ไฟล์ในโฟลเดอร์ `profiles/` ด้านล่าง (ทุกไฟล์แบ่งโครงสร้างมาตรฐาน 10 หมวดครบถ้วน)
* **คลังบทวิเคราะห์หุ้นจริง (`analyses/` — แบ่งตามตลาด `us/`, `th/`, `global/`):** ดูภาพรวมทั้งหมดที่ [analyses/INDEX.md](./analyses/INDEX.md)

**บทวิเคราะห์รุ่น v4** — ตัวเลขสร้างอัตโนมัติจาก `inputs/TICKER.json` ผ่าน `valuation_engine.py` ห้ามแก้ด้วยมือ (CI ตรวจทุก PR):

<!-- AUTO-SUMMARY:README:START -->
* [BKNG — Booking Holdings Inc.](./analyses/us/BKNG-booking-holdings.md) *(v4 ณ 2026-11-23 ที่ $146 — สถานะ: **Watchlist**; เพดาน Starter ~$120 (ช่วง $115–$125); ผลตอบแทน 5 ปี 13.3%)*
* [MDT — Medtronic plc](./analyses/us/MDT-medtronic.md) *(v4 ณ 2026-11-24 ที่ $96.68 — สถานะ: **Watchlist**; เพดาน Starter ~$53 (ช่วง $50–$55); ผลตอบแทน 5 ปี 10.2%)*
<!-- AUTO-SUMMARY:README:END -->

**บทวิเคราะห์รุ่นเก่า** — ทำก่อนกฎ v4 ตัวเลขและข้อสรุปยังไม่ผ่านการตรวจ ห้ามใช้ตัดสินใจลงเงินจนกว่าจะรันใหม่ผ่าน `inputs/TICKER.json`:

* [UBER — Uber Technologies, Inc.](./analyses/us/UBER-uber-technologies.md) `[LEGACY v1 — Pending v4 Re-audit]` *(วิเคราะห์ 23 พ.ย. 2026 — Split-Brain Debate — Verdict: Small Starter Buy 2%–3% ที่ $60–$64 / Core ≤ $55–$58 — Base DCF $89.82 แต่คุมขนาดรับความเสี่ยง AV & Delivery Hero)*
* [POOL — Pool Corporation](./analyses/us/POOL-pool-corp.md) `[LEGACY v1 — Pending v4 Re-audit]` *(วิเคราะห์ 23 พ.ย. 2026 — Split-Brain Debate — Verdict: Watchlist / Wait ที่ $208.23; Starter ≤ $180–$188, Core ≤ $155–$170)*
* [GOOGL — Alphabet Inc.](./analyses/us/GOOGL-alphabet.md) `[LEGACY v1 — Pending v4 Re-audit]` *(วิเคราะห์ 23 พ.ย. 2026 — Split-Brain Debate — Verdict: Watchlist / Wait ที่ $284; Starter ≤ $255–$260, Core ≤ $230–$245)*
* [BKNG (v2) — ฉบับ AGV เก็บไว้เทียบ](./analyses/us/BKNG-booking-holdings-v2-agv.md) `[LEGACY v1 — Pending v4 Re-audit]` *(ข้อสรุปเดิม BUY $137–$148 ถูกแทนที่ด้วยฉบับ v4 ด้านบน)*
* [SYK — Stryker Corporation](./analyses/us/SYK-stryker.md) `[LEGACY v1 — Pending v4 Re-audit]` *(วิเคราะห์ 23 พ.ย. 2026 — Verdict: Starter Buy / ทยอยสะสม $295–$310, Core ≤ $275–$285 — ชนะ MDT ชัดเจนในตารางเทียบ)* ⚠️ *ข้อสรุปเดิมนี้ขัดกฎ v4 เอง: ผลตอบแทนกรณีฐาน ~10% ต่ำกว่าด่านขั้นต่ำ 11% ของ Starter*
* [MDT (v1) — ฉบับ AGV เก็บไว้เทียบ](./analyses/us/MDT-medtronic-v1-agv.md) `[LEGACY v1 — Pending v4 Re-audit]` *(ข้อสรุปเดิม Watchlist ≤ $78–$82 เขียนก่อนงบ Q2 FY27 — ถูกแทนที่ด้วยฉบับ v4 ด้านบน)*
* [BSX — Boston Scientific Corporation](./analyses/us/BSX-boston-scientific.md) `[LEGACY v1 — Pending v4 Re-audit]` *(วิเคราะห์ 23 พ.ย. 2026 — Verdict: PASS / อย่ารับมีดที่ $42 — ติด Kill Filter หนี้ >3.6x จากดีล Penumbra $14.5B + หั่นเป้า 3 รอบ)*

---

## สารบัญสภานักลงทุนทั้ง 17 ท่าน (แบ่งตามหมวดและบทบาทในสภา)

### หมวดที่ 1: สายถือกระจุกตัวสุดขีด, ธุรกิจผูกขาด และ Constructive Activism (`profiles/01-monopoly-activism/`)
| # | นักลงทุน / กองทุน | บทบาทในสภา | แก่นความคิด & อาวุธลับ | ไฟล์เจาะลึก |
| :---: | :--- | :--- | :--- | :--- |
| 01 | **Chris Hohn** (TCI Fund Management) | นักล่าธุรกิจผูกขาด & Hard Assets | จักรวาลหุ้น ~200 ตัว, ถือเฉลี่ย 8 ปี, High Barriers to Entry, Pricing Power, Aftermarket Monopolies, Constructive Activism (Alphabet, GE Aerospace, CN Rail) | [01-chris-hohn.md](./profiles/01-monopoly-activism/01-chris-hohn.md) |
| 02 | **Bill Ackman** (Pershing Square) | กฎเหล็ก 8 ข้อ & นักปลดล็อกมูลค่า | บัญญัติ 8 ประการ (Stone-Tablet Rules), ธุรกิจเรียบง่ายสร้าง FCF, Permanent Capital (PSH), Asymmetric Macro Hedging, บทเรียน Valeant/Netflix vs Chipotle/UMG | [02-bill-ackman.md](./profiles/01-monopoly-activism/02-bill-ackman.md) |
| 03 | **Dev Kantesaria** (Valley Forge Capital) | ด่านเก็บเงิน (Toll-Booth) & Predictability | ความคาดการณ์ได้ 10 ปีเป็นดาวเหนือ, สระตกปลา ~50 บริษัท, ถือ 7–12 ตัว, Asset-Light Monopoly (FICO, Moody's, S&P Global, Visa), เทียบ FCF Yield กับ 10Y Treasury | [03-dev-kantesaria.md](./profiles/01-monopoly-activism/03-dev-kantesaria.md) |
| 04 | **ValueAct Capital** (Jeff Ubben & Mason Morfit) | Activist หลังบ้านในห้องบอร์ด | Constructivist Activism (ไม่ทะเลาะออกสื่อ แต่นั่งบอร์ดพลิกโฉมธุรกิจ), SaaS "Valley of Death" Accounting Bridge (Microsoft, Adobe, Salesforce) | [04-valueact-capital.md](./profiles/01-monopoly-activism/04-valueact-capital.md) |

---

### หมวดที่ 2: สาย Pure Quality & เครื่องจักรทบต้นระยะยาว (`profiles/02-pure-quality-compounding/`)
| # | นักลงทุน / กองทุน | บทบาทในสภา | แก่นความคิด & อาวุธลับ | ไฟล์เจาะลึก |
| :---: | :--- | :--- | :--- | :--- |
| 05 | **Terry Smith** (Fundsmith) | ตำรวจตรวจคุณภาพงบการเงิน | *Accounting for Growth*, 3 กฎทอง, ROCE สูงต่อเนื่อง (ไม่ใช่ ROE), Cash Conversion ≥ 95%, ชำแหละ SBC / Adjusted EBITDA / Buybacks ทำลายมูลค่า | [05-terry-smith.md](./profiles/02-pure-quality-compounding/05-terry-smith.md) |
| 06 | **Nick Sleep & Qais Zakaria** (Nomad) | นักมองปลายทาง 10–20 ปี | **Scale Economies Shared (SES)**, **Destination Analysis**, Information Shelf-Life, Principal vs Agent, พอร์ตปลายทาง 3 ตัว (Amazon, Costco, Berkshire) | [06-nick-sleep.md](./profiles/02-pure-quality-compounding/06-nick-sleep.md) |
| 07 | **Chuck Akre** (Akre Capital) | เจ้าพ่อเครื่องจักรทบต้น | **เก้าอี้ 3 ขา (Three-Legged Stool)**, สูตร `Reinvestment Rate × Incremental ROIC`, Bottleneck Businesses, *The Art of (Not) Selling* (American Tower, Mastercard) | [07-chuck-akre.md](./profiles/02-pure-quality-compounding/07-chuck-akre.md) |
| 08 | **Thomas Russo** (Gardner Russo & Quinn) | ผู้เชี่ยวชาญแบรนด์โลก & ธุรกิจตระกูล | **Capacity to Reinvest** & **Capacity to Suffer** (Nestlé ยอมขาดทุน Nespresso 10 ปี), แก้ปัญหา Agency Cost ด้วย Family Stewardship, Tax-Deferred Compounding | [08-thomas-russo.md](./profiles/02-pure-quality-compounding/08-thomas-russo.md) |

---

### หมวดที่ 3: สายตรง Munger, นักล่าความไม่สมมาตร, วิวัฒนาการดาร์วิน & คูเมือง (`profiles/03-munger-asymmetry-moat/`)
| # | นักลงทุน / กองทุน | บทบาทในสภา | แก่นความคิด & อาวุธลับ | ไฟล์เจาะลึก |
| :---: | :--- | :--- | :--- | :--- |
| 09 | **Li Lu** (Himalaya Capital) | สายตรง Charlie Munger & นักสืบ Scuttlebutt | สวมวิญญาณนักข่าวสืบสวนลงพื้นที่จริง, Circle of Competence, มุมมองประวัติศาสตร์ Civilization 3.0, ซื้อ BYD ตั้งแต่ปี 2008 | [09-li-lu.md](./profiles/03-munger-asymmetry-moat/09-li-lu.md) |
| 10 | **Mohnish Pabrai** (Pabrai Funds) | นักล่าเดิมพันไม่สมมาตร & Spawners | กฎ **Dhandho** 9 ข้อ (*ออกหัวชนะใหญ่ ออกก้อยเจ็บน้อย*), Low Risk vs High Uncertainty, Shameless Cloning, **5 ประเภทของ Spawners**, Kelly Sizing | [10-mohnish-pabrai.md](./profiles/03-munger-asymmetry-moat/10-mohnish-pabrai.md) |
| 11 | **Pulak Prasad** (Nalanda Capital) | นักคัดทิ้งสายชีววิทยาดาร์วิน | *What I Learned About Investing from Darwin*, 3 ขั้นตอน (เลี่ยงความเสี่ยงใหญ่ก่อน → ซื้อ High ROCE ราคาแฟร์ → ขี้เกียจให้สุดๆ), ไม่ทำ DCF, คัดทิ้ง 95%+ | [11-pulak-prasad.md](./profiles/03-munger-asymmetry-moat/11-pulak-prasad.md) |
| 12 | **Pat Dorsey** (Dorsey Asset Management) | ศัลยแพทย์ผ่าตัดคูเมือง (Economic Moats) | แยก **4 แหล่งที่มาของคูเมืองแท้** ออกจาก **4 คูเมืองปลอม (Mistaken Moats)**, Moat Trend (กว้างขึ้น vs ถูกกัดเซาะ), Reinvestment Moat vs Legacy Moat | [12-pat-dorsey.md](./profiles/03-munger-asymmetry-moat/12-pat-dorsey.md) |

---

### หมวดที่ 4: ฝ่ายค้านคุมความเสี่ยง, วัฏจักร, 100-Baggers และเครื่องมือวิเคราะห์ความคาดหวัง (`profiles/04-risk-cycle-valuation/`)
| # | นักลงทุน / กองทุน | บทบาทในสภา | แก่นความคิด & อาวุธลับ | ไฟล์เจาะลึก |
| :---: | :--- | :--- | :--- | :--- |
| 13 | **Howard Marks** (Oaktree Capital) | ฝ่ายค้านคุมสติ & วัฏจักรตลาด | **Second-Level Thinking**, Market Pendulum & Temperature Check, *Buying Well vs Buying Good Things*, Risk = โอกาสสูญเงินถาวร, *Sea Change* | [13-howard-marks.md](./profiles/04-risk-cycle-valuation/13-howard-marks.md) |
| 14 | **Seth Klarman** (Baupost Group) | เจ้าพ่อ Margin of Safety & ขาลง | Risk-First Return-Second, Forced Sellers & Institutional Imperatives (Spin-offs, Index Deletions, Distressed), Catalysts, เงินสดคือ Call Option | [14-seth-klarman.md](./profiles/04-risk-cycle-valuation/14-seth-klarman.md) |
| 15 | **François Rochon** (Giverny Capital) | วินัย Buffett ยุคใหม่ & เจ้าของ Podium of Errors | **Rule of Three**, ติดตาม Owner's Earnings เทียบราคาหุ้นทุกปี, มอบเหรียญความผิดพลาดตัวเองทุกปี (*Podium of Errors*), เป้าโต 2 เท่าใน 5 ปี (~15% CAGR) | [15-francois-rochon.md](./profiles/04-risk-cycle-valuation/15-francois-rochon.md) |
| 16 | **Chris Mayer** (Woodlock House / *100 Baggers*) | นักล่าหุ้น 100 เด้ง | **Twin Engines** (Earnings Growth + P/E Expansion), Owner-Operators, High ROIC + Long Runway, **Coffee Can Portfolio** (ซื้อแล้วล็อกเก็บ 10 ปี+) | [16-chris-mayer.md](./profiles/04-risk-cycle-valuation/16-chris-mayer.md) |
| 17 | **Michael Mauboussin** (Counterpoint Global) | สถาปนิกเครื่องมือประเมินมูลค่า | **Expectations Investing (Reverse DCF)**, **Base Rates (Outside View)**, ROIIC, Capital Allocation Framework, Value Stick (WTP/WTS), การปรับงบ Intangibles | [17-michael-mauboussin.md](./profiles/04-risk-cycle-valuation/17-michael-mauboussin.md) |

---

## โครงสร้างมาตรฐานภายในทุกไฟล์ (`profiles/01` – `17`)

ทุกไฟล์ถูกเขียนลงลึกครบทั้ง **10 หมวด**:
1. **ข้อมูลพื้นฐาน & บทบาทในสภา** (กองทุน, จำนวนหุ้น, ระยะเวลาถือ, สไตล์)
2. **วิวัฒนาการทางความคิด & แผลเป็นในสนามจริง** (จุดเปลี่ยนและบทเรียนราคาแพงที่หล่อหลอมวิธีคิด)
3. **แก่นปรัชญาและกรอบความคิดหลัก** (Mental Models พร้อมกลไกการทำงาน)
4. **เกณฑ์คัดเลือกเชิงปริมาณและคุณภาพ** (ตัวเลขชี้วัดจริงและเหตุผลเบื้องหลัง)
5. **วิธีประเมินมูลค่าและการปรับงบการเงิน** (สูตรคำนวณ, Hurdle Rate, การปรับ SBC/CapEx/Intangibles)
6. **สิ่งที่ตัดทิ้งทันที (Anti-Portfolio / Red Flags)**
7. **การบริหารพอร์ต, การให้น้ำหนัก และวินัยการขาย (Sizing & Sell Discipline)**
8. **เจาะลึกเคสศึกษาจริง** (ทั้งเคสชนะระดับตำนาน 3+ เคส และเคสพลาดจริงพร้อมบทเรียน 1–2 เคส)
9. **คู่มือสวมหมวกคิดแบบคนนี้** (Step-by-Step Analysis Flow + 8–10 Killer Questions)
10. **จุดบอด, คู่ถ่วงดุลในสภา และแหล่งศึกษาต่อ** (หนังสือ, จดหมายประจำปี, บทสัมภาษณ์)

---

## ตารางจับคู่ "สภาจำลอง" ตามประเภทหุ้นที่คุณกำลังดู

| ประเภทหุ้นที่กำลังวิเคราะห์ | ชุดแว่นตาที่ควรเรียกมาวิเคราะห์ร่วมกัน |
| :--- | :--- |
| **หุ้นกึ่งผูกขาด / โครงสร้างพื้นฐาน / Data / Payment** | Chris Hohn + Dev Kantesaria + Pat Dorsey + Howard Marks |
| **หุ้นแพลตฟอร์ม / E-commerce / Retail ที่กดมาร์จินเพื่อโต** | Nick Sleep + Thomas Russo + Michael Mauboussin + Terry Smith |
| **หุ้น Compounder ขนาดกลางที่หวังโตหลายเด้ง (Multi-Bagger)** | Chuck Akre + Chris Mayer + François Rochon + Pulak Prasad |
| **หุ้นดีที่ราคาตกลงมาแรงจากวิกฤตหรือปัญหาผู้บริหาร** | Bill Ackman + ValueAct Capital + Mohnish Pabrai + Seth Klarman |
| **หุ้นตลาดเกิดใหม่ / เอเชีย / ธุรกิจตระกูล** | Li Lu + Pulak Prasad + Thomas Russo + Seth Klarman |
