# Investment Memo & Split-Brain Council Debate: Alphabet Inc. (NASDAQ: GOOGL)

> [!CAUTION]
> **`[LEGACY v1 — Pending v4 Re-audit]`** — บทวิเคราะห์นี้ทำก่อนกฎ v4: ตัวเลขไม่มีลิงก์แหล่งอ้างอิง ไม่ได้ผูกกับ `valuation_engine.py` และยังใช้เกณฑ์เพดานราคาแบบเก่า (รวมเลนส์ B และข้อยกเว้น "ผ่าน 2 ใน 3") **ห้ามใช้ข้อสรุปหรือโซนราคาในไฟล์นี้ตัดสินใจลงเงิน** จนกว่าจะสร้าง `inputs/TICKER.json` และรันใหม่ด้วย v4 — ตัวเลขในไฟล์นี้ยังไม่ได้แก้ (ตั้งใจไม่เดาเลขใหม่)

**วันที่วิเคราะห์:** 23 พฤศจิกายน 2026 | **โหมดการวิเคราะห์:** แยกสมองจริง 2 Subagents อิสระ (Bull Analyst vs. Bear Risk Analyst — ซักค้าน 2 รอบ, ไม่ใส่อรรถรส) + ประธานสภา (Michael Mauboussin) ตรวจสอบสมการ Reverse DCF และชี้ขาด  
**ราคาอ้างอิง:** **$283.93** *(23 พ.ย. 2026; ปิดศุกร์ 20 พ.ย. $265.29; ปรับฐาน -30% ถึง -35% จากจุดสูงสุด 52 สัปดาห์ ~$404–$408)*  
**แหล่งข้อมูล:** Alphabet SEC Form 8-K/10-Q (Q3 2026 สิ้นสุด 30 ก.ย. 2026), Form 10-K (FY2025), Q3 2026 Earnings Call

---

## 1. บทสรุปคำตัดสินของประธานสภา (Chairman's Verdict — Michael Mauboussin)

| หัวข้อ | ตัวเลขจริง / ข้อสรุป |
| :--- | :--- |
| **Market Cap (Diluted 12.368B) / Standard EV** | **$3,511.6B** / **$3,390.6B** *(Cash & Mkt Sec $265.1B รวม SpaceX $75.2B; LT Debt $125.1B + Conv Pref $19.0B)* |
| **Core Operating EV (หัก Haircut Non-Core)** | **~$3,218.6B** *(หัก Anthropic หลัง IPO สุทธิภาษี ~$107B + Waymo หลัง Haircut 35% ~$65B)* |
| **TTM Revenue / GAAP EBIT (Q3'26)** | **$471.1B** / **$157.0B** *(Margin 33.3%; Normalized Operating NOPAT ~$127.9B)* |
| **Normalized Operating P/E / Core EV/EBIT** | **27.4x** *(GAAP P/E ~14–15x เป็นภาพลวงตาจาก Paper Gains $127B!)* / **20.5x Core EBIT** |
| **FY2026E CapEx Guidance / TTM True FCF** | **$195B–$205B (~40% ของรายได้)** / **TTM True FCF (หัก SBC $30.4B) = -$10.7B** *(FY26E ~-$47B ถึง -$57B)* |
| **Explicit 10Y DCF Fair Value (Chairman Base)** | **$282.10** *(-0.6% จาก $283.93 — WACC 9.0%, Terminal g 3.5%, รับรู้ FCF ติดลบ FY26–27 เต็มรูป)* |
| **Chairman 5-Year Forward IRR (จาก $283.93)** | **Bear: -5.4%** (25%) \| **Base: +8.5%** (50%) \| **Bull: +18.3%** (25%) → *Expected IRR ~+7.5%* |
| **มติชี้ขาด (Verdict)** | **WATCHLIST / WAIT (ยังไม่ไล่ซื้อที่ $284; ไม้แรก Starter 2% ที่ ≤ $255–$260, จัดหนัก Core ที่ ≤ $230–$245)** — *ราคาปัจจุบันสะท้อน Base Case ไปครบแล้ว ไม่มี Margin of Safety เพียงพอสำหรับช่วง CapEx พีคปี 2027 (FCF ติดลบต่ออีกปี) และความเสี่ยง Dilution จากวงเงินขายหุ้น ATM ที่เหลืออีก $27.6B* |

---

## 2. สรุปการปะทะกันจริงระหว่าง 2 สมองอิสระ (Split-Brain Cross-Examination Record)

### ประเด็นที่ 1: AI CapEx ($200B/ปี), CIP $145B, หนี้สิน & หน้าผาค่าเสื่อมราคา
* **ข้อโต้แย้งฝั่ง Bull:**
  * Google Cloud Q3'26 โต **+103% YoY สู่ Run-rate $122.8B** พร้อม Operating Margin **36.2%** (Incremental Margin 48.4%) และมี **Contracted Backlog $560.8B** (>55% รับรู้ใน 24 เดือน)
  * สินทรัพย์ถาวร **$145.3B (39% ของ Net P&E)** เป็น Construction-in-Progress ที่ยังไม่เปิดใช้งาน เมื่อวัดเฉพาะสินทรัพย์ที่เปิดใช้แล้ว **In-Service ROIIC = 63.2%** (Gross ROIIC 24.0%)
  * การหยุด Buyback และระดมทุน (Debt + ATM Equity) เพื่อล็อกตลาด $500B+ โดยยังคง Strict Liquid Net Cash +$30.6B (S&P Leverage 0.0x) คือการตัดสินใจแบบ Principal; True FCF จะพลิกบวกปี **FY28 ($27.5B)** และแตะ **~$99B ปี FY29**
  * ฝ่าย Bear ติดกับดัก **Static Denominator Fallacy**: เมื่อรายได้ขยายสู่ $755B–$835B (FY29–30) ค่าเสื่อม/รายได้จะเพิ่มแค่ +730–750 bps ไม่ใช่ -1,250 bps และ Google ทำ **Workload Cascading** ย้าย TPU เก่าไปรัน Ads/Serving ยาว 5–6 ปีจริง ส่วน TPU ที่ขายออกนอก ($13.3B Inventory) ตัดเป็น COGS ทันที
* **ข้อหักล้างฝั่ง Bear:**
  * **$145.3B CIP คือระเบิดเวลาของ Margin:** ที่ Cloud Margin ดูสวย 36.2% เพราะงบกำไรขาดทุน *ยังไม่ได้ตัดค่าเสื่อมของก้อน $145.3B* (CFO เตือนเองว่า Q4 Cloud Margin จะถูกกดดัน) เมื่อ CIP + CapEx FY26–27 ($435B+) เข้าใช้งาน ค่าเสื่อม GAAP จะพุ่งจาก $21.1B (FY25) สู่ **~$115B/ปี ในปี 2029** (หรือ $143B บนอายุเศรษฐกิจชิป 4 ปี)
  * **Backlog ชะลอแรง -78.6%:** ยอดเพิ่ม Backlog รายไตรมาสทรุดจาก **+$220B (Q1) → +$54B (Q2) → +$47B (Q3)** กระจุกใน AI Labs ที่ขาดทุน ท่ามกลาง Hyperscaler CapEx รวม **$730B/ปี** (เสี่ยง Overbuild แบบ Telecom 2000)
  * **เงินสดไม่โกหก:** 9M 2026 Alphabet ขาดดุลเงินสดก่อนระดมทุน **-$88.66B**, หยุดซื้อหุ้นคืน ($0), ต้องขายหุ้นเพิ่มทุน **ATM $42.87B** (เหลือรอขายอีก $27.6B!), ออก Preferred 6.25% $19.06B, และกู้หนี้สุทธิ $76.34B (Total ROCE ร่วงจาก 31.1% → **18.1%** หลุดเกณฑ์ 20% ของ Terry Smith)
* **คำวินิจฉัยของประธานสภา (ประเด็นที่ 1):** **เสมอ (Bull ชนะเรื่อง Demand จริงจาก Backlog $561B / Bear ชนะเรื่องความเสี่ยง Margin & Dilution ปี 2027)** — ตัวเลขชี้ชัดว่านี่ไม่ใช่การเผาเงินไร้จุดหมายแบบ Metaverse แต่ความเสี่ยงด้านจังหวะเวลา (FY27 Peak CapEx -$48B ถึง -$57B True FCF + ATM overhang) ยังไม่จบ

---

### ประเด็นที่ 2: คูเมือง Search, AI Mode Monetization & มายากลบัญชี Segment Margin
* **ข้อโต้แย้งฝั่ง Bull:**
  * Q3'26 Search โต **+12% YoY ($63.35B)**, Paid Clicks +8%, CPC +4%, Query Growth สูงสุดในรอบ 5 ปี, และ **Google Services Margin พุ่งเป็น 40.7%** (+215 bps YoY)
  * Organic CTR -58% กระทบ Publishers ไม่ใช่ Google; ต้นทุน Serving Gemini ลดลง **-78%** ในปี 2025 และ AI Mode Queries ยาวกว่าเดิม 3 เท่า ทำให้ Monetization Lag เป็นเพียงช่วงเปลี่ยนผ่านคล้าย Mobile Shift (2012–2014)
* **ข้อหักล้างฝั่ง Bear (หมัดน็อกเชิงบัญชี!):**
  * **พบการโยกต้นทุน AI ออกนอก Services Segment (SEC Q3'26 Footnote):** เหตุผลที่ Services Margin ดูพุ่งขึ้น 40.7% เป็นเพราะขาดทุนในบรรทัด **"Alphabet-level activities" พุ่งขึ้น +71.4% YoY** จาก -$4.47B เป็น **-$7.66B** (+$3.19B ในไตรมาสเดียว!) หากจัดสรรต้นทุน AI ส่วนเพิ่มเพียง 70% กลับเข้า Services **Adjusted Services Margin จริงหดตัว -17 bps (38.51% → 38.34%)**
  * **AI Mode แย่กว่า Mobile Shift เชิงโครงสร้าง:** (1) ต้นทุน Compute/Query แพงกว่า Blue-Link 5–10 เท่า, (2) CBO Philipp Schindler ยอมรับเองบน Q3 Call ว่า *"AI Mode's lower monetization slowed Search ad growth"* (ชะลอจาก +17% Q4'25 → +12% Q3'26), และ (3) เกิด **Multi-Homing จริง** (US Search Share เหลือ 85.45%, OpenAI เผย ChatGPT มี Search-like Queries แตะ ~20% ของ Google + เปิด ChatGPT Ads, Amazon Ads แตะ Run-rate ~$80B/ปี)
* **คำวินิจฉัยของประธานสภา (ประเด็นที่ 2):** **Bear ได้เปรียบเชิงคุณภาพหลักฐาน** — การขุดเจอ "Alphabet-level activities" (-$7.66B/ไตรมาส) หักล้างข้ออ้างว่า Services Margin ขยายตัวจริงได้อย่างสมบูรณ์ อย่างไรก็ตาม Paid Clicks +8% / CPC +4% แสดงว่า Search ยังไม่พังทลาย เพียงแต่กำลังเข้าสู่โหมด "โตช้าลง + ต้นทุนสูงขึ้น"

---

### ประเด็นที่ 3: Valuation, SOTP Hidden Assets, คดีผูกขาด & พันธบัตร 4.93%
* **ข้อโต้แย้งฝั่ง Bull:**
  * ที่ $283.93 หุ้นร่วงแล้ว -29.8% จาก ATH; เมื่อหัก Cash/SpaceX ($75B) + Anthropic หลัง IPO (~$147B+) + Waymo (~$100B) ออก Core Google เทรดเพียง **~19.5x–20.5x EBIT** ทั้งที่ EBIT โต +30% YoY และ Berkshire Hathaway ถือรวม ~$28B เป็น Top 3 Holding
  * ศาลชั้นต้นปฏิเสธการสั่งขาย Chrome แล้ว ส่วนภาษี EU DST 3% กระทบ EBIT <2.5%
* **ข้อหักล้างฝั่ง Bear:**
  * **SOTP ต้องหักภาษีและส่วนลดสภาพคล่อง:** Deferred Tax Liabilities พุ่งเป็น **$27.8B** แล้ว, SpaceX เพิ่งถูก Markdown -$8.7B ใน Q3, และ Other Bets/Waymo ยังเผาเงินสด **-$2.05B/ไตรมาส** (+43.5% YoY) หลังหัก Haircut 32% Core Google ยังเทรด **22.9x–25.2x After-Tax Core NOPAT** (Yield 4.0%–4.4% แพ้พันธบัตร 10 ปี 4.93%)
  * **ไร้ Capitulation & คดีอุทธรณ์ยังค้าง:** Wall Street ยังให้ **53 Buy / 0 Sell**, ขณะที่ **D.C. Circuit Appeal** ยังรอตัดสินคำขอ DOJ ให้สั่งแบน Apple TAC ($26B+/ปี) และคำสั่งศาล AdTech (ก.ย. 2026) บีบ Take Rate ของ AdX ด้วย Open-Source Header Bidding
* **คำวินิจฉัยของประธานสภา (ประเด็นที่ 3):** **Bear ชนะด้าน Margin of Safety** — ที่ราคา $283.93 (Core EV/NOPAT 25.2x, Explicit 10Y DCF Fair Value $282.10) ตลาดไม่ได้ให้ส่วนลดเผื่อความผิดพลาดมากพอเมื่อเทียบกับพันธบัตร 4.93% และความเสี่ยงที่ปี 2027 FCF จะยังติดลบหนัก

---

## 2.5 การถกเชิงคุณภาพ 5 มิติ (Deep Qualitative & Scuttlebutt Autopsy — Li Lu / Nick Sleep / Russo / Dorsey)

> *นอกจากงบการเงินแล้ว ความเปลี่ยนแปลงเชิงคุณภาพของ Alphabet ในช่วงปี 2026 มีน้ำหนักชี้ขาดต่อภาพ 10 ปีไม่แพ้ตัวเลข CapEx:*

| มิติเชิงคุณภาพ | ฝั่ง Bull (หลักฐานบวก) | ฝั่ง Bear (หลักฐานลบ / รอยร้าว) | ประธานสภาวินิจฉัย |
| :--- | :--- | :--- | :---: |
| **1. Leadership & Talent War (ผู้นำและสงครามคนเก่ง)** | **Sergey Brin** กลับมานั่งทำงานร่วมกับทีมวิศวกรช่วยทลายกำแพงระบบราชการและผ่าตัดองค์กรรวม DeepMind เข้ากับ Search จนส่ง AI Mode + Gemini 4 ออกมาได้ทันเกม | **สมองไหลระดับตำนาน (ส.ค. 2026):** 4 ตำนานผู้สร้าง Google ได้แก่ **Jeff Dean, Sanjay Ghemawat, Oriol Vinyals และ Quoc Le** ลาออกพร้อมกันไปตั้งสตาร์ทอัพ AI เอง! พร้อมข่าว **Demis Hassabis** ก้าวลงจาก CEO DeepMind (ขยับเป็น Chair / Chief Scientist) สะท้อนแรงตึงเครียดภายในและภาวะเสียแกนสมองยุคบุกเบิก | **Bear ชนะ** *(ความเสี่ยงสมองไหลสูงขึ้นชัด)* |
| **2. Culture & Execution Speed (วัฒนธรรมองค์กร)** | ปรับโครงสร้างองค์กรได้ดีขึ้นมากเมื่อเทียบยุค "Code Red" ปี 2023 และใช้ Gemini ช่วยเขียนโค้ดภายในเพิ่มความเร็วส่งมอบงาน +35% | วัฒนธรรมแบบ **Consensus-driven & Peer Review** ขององค์กรใหญ่ 200,000+ คน ยังช้ากว่าความดุดันของ OpenAI (ที่ไล่ซื้อ 6 บริษัทใน Q1 2026 เช่น Astral เครื่องมือ Python) และความโฟกัสของ Anthropic | **ก้ำกึ่ง (เหลือง)** |
| **3. Scuttlebutt: ลูกค้าองค์กร & นักพัฒนา (*Li Lu*)** | **จุดแข็งที่ CFO องค์กรชอบ:** Google Cloud + **Gemini Enterprise** เสนอราคาแบบ **Fixed-Cost / Budget Predictability** คุมงบได้ และลงทุน $750M ใน Partner Ecosystem (120,000 พาร์ทเนอร์) ต่างจาก OpenAI ที่มีแรงกดดันต้องรีดรายได้และเปลี่ยนทิศทางบ่อย | 81% ของ Global 2000 ใช้กลยุทธ์ **Multi-Vendor** (ไม่ผูกขาดกับ Google); **Anthropic (Claude)** ครองใจสาย Enterprise/Coding และเพิ่ง IPO มูลค่า $1.5T (พ.ย. 2026) ทำให้ CIO มั่นใจย้ายงานขึ้น Claude มากขึ้น ส่วน **OpenAI** ล็อกนักพัฒนาผ่านเครื่องมือ Local Dev (Codex + Astral) | **เสมอ** *(ตลาดองค์กรแบ่งเค้กกัน ไม่กินรวบ)* |
| **4. Scuttlebutt: ผู้ลงโฆษณา & Publishers** | การเปลี่ยนผ่านสู่ **Journey-Based Monetization (AI Mode + UCP Checkout)** ทำให้ Google กินรวบตั้งแต่ต้นทางค้นหา → เปรียบเทียบ → จ่ายเงิน (เพิ่ม Conversion ให้แบรนด์ใหญ่) | **แรงต้านจากผู้ลงโฆษณา (พ.ย. 2026):** นักการตลาด PPC และ B2B หงุดหงิดเรื่อง **Loss of Control** จากระบบอัตโนมัติ (AI Max / Auto-generated Assets) ที่ยิงโฆษณาหลุดกลุ่มเป้าหมายและปรับข้อความไม่ตรงแบรนด์ (Search Engine Land พ.ย. 2026 รายงานผู้ลงโฆษณาบางส่วนเริ่มหั่นงบ) + **Publishers/SEO ต่อต้านหนัก** เพราะ AI Overviews ดูดคลิก -58% | **Bear ได้เปรียบ** *(ความสัมพันธ์กับ Ecosystem โฆษณาและเว็บเปิดตึงเครียดขึ้น)* |
| **5. 10-Year Destination, Spawner DNA & แรงต้านสังคม** | เป็นบริษัทเดียวในโลกที่มี **Full-Stack AI ครบทุกชั้น** (Custom TPU + Cloud + Frontier Model + Distribution พันล้านคนบน Android/Chrome/YouTube + Waymo 15 เมือง) — อำนาจ Distribution ทำให้ **Augmentation ชนะ Substitution** ได้ง่ายกว่าคู่แข่งที่ต้องบังคับคนเปลี่ยนนิสัย | ผลเลือกตั้งกลางเทอมสหรัฐฯ **3 พ.ย. 2026** สะท้อนกระแสสังคมต่อต้าน **AI และ AI Data Centers** (ค่าไฟ/พลังงาน/การแย่งงาน) เพิ่มสูงขึ้นอย่างชัดเจน เป็นความเสี่ยงเชิงการเมืองต่อการสร้าง Data Center แสนล้านดอลลาร์ในสหรัฐฯ และยุโรป | **Bull ชนะด้าน Distribution / Bear ชนะด้านแรงต้านสังคม** |

> **ข้อสรุปเชิงคุณภาพ:** แม้ Alphabet จะยังคงเป็น **Full-Stack Distribution Monster** ที่ได้เปรียบด้านช่องทางเข้าถึงผู้ใช้ (Android/Chrome/YouTube/Workspace) และต้นทุน TPU แต่ **การลาออกพร้อมกันของ Jeff Dean + Sanjay Ghemawat + Oriol Vinyals + Quoc Le และการขยับบทบาทของ Demis Hassabis ในเดือน ส.ค. 2026** รวมถึงแรงต้านจากผู้ลงโฆษณา/สังคมเรื่อง Data Center ยิ่งตอกย้ำคำตัดสินเดิมว่า **ไม่ควรไล่ซื้อที่ $284 โดยไม่มี Margin of Safety — ต้องรอส่วนลดราคาโซน ≤ $230–$245 หรือรอพิสูจน์ว่าผู้นำ AI รุ่นใหม่ของ Google ยังรักษาความเป็นผู้นำโมเดลไว้ได้จริง**

---

## 3. ตัวแปรชี้ขาด & แผนปฏิบัติการ (Crucible Variables, Sizing & Flip Conditions)

### 3.1 ตัวแปรชี้ขาด 2 ข้อที่จะตัดสินว่า Bull หรือ Bear ถูกใน 12–24 เดือนข้างหน้า
1. **Cloud Margin & Backlog Quality Test (2027):** เมื่อ CIP $145B เข้าตัดค่าเสื่อมจริงในปี 2027 Google Cloud รักษา Operating Margin ให้อยู่ **≥ 30%** และหยุดการชะลอตัวของยอดเพิ่ม Backlog รายไตรมาส (>$50B+/ไตรมาส) ได้หรือไม่? *(ถ้าหลุด <28% 2 ไตรมาสติด = Bear ชนะ)*
2. **Search + Corporate Consolidated Margin Test:** เมื่อรวม Alphabet-level activities เข้ามาด้วยแล้ว Consolidated Operating Margin ยืนเหนือ **30%** และ Search Revenue โต **≥ 8%–10% YoY** หลังเปิดขาย AI Mode Ads เต็มรูปแบบได้หรือไม่? *(ถ้า Search หลุด <6% = Bear ชนะ)*

### 3.2 แผนการเข้าซื้อ & การให้น้ำหนัก (Position Sizing)
* **สถานะปัจจุบันที่ $283.93:** **WATCHLIST / WAIT** *(Fair Value Base Case = $282, Base 5Y IRR +8.5%)*
* **โซน Starter Position (2%–3%):** **≤ $255 – $260** *(Base IRR ~10.5%–11%)*
* **โซน Core Position (5%–8%):** **≤ $230 – $245** *(Core EV/NOPAT ~19–20x, Base IRR ≥ 12%–13%+)* — มีโอกาสเกิดในช่วงตลาดผันผวนรับข่าว Peak CapEx ปี 2027 หรือข่าวศาลอุทธรณ์ D.C. Circuit
* **Thesis Breakers (ถ้าซื้อแล้วต้องขายเมื่อ):** (1) Cloud Margin หลุด <28% 2 ไตรมาสติดขณะ CapEx >$50B/ไตรมาส, (2) Search โต <6% YoY พร้อม Paid Clicks/CPC ติดลบ, (3) ออกหุ้นเพิ่มทุน ATM ต่อเนื่องเกินวงเงินเดิมโดยไร้เส้นทางกลับสู่ Positive True FCF ภายในปี 2028
