# Review sheet: `agent_test_hybrid_rrf_b2700_test-selected_20261116T090045Z`

Read each case, check the agent answer and every citation against the cited text (and the PDF when needed), then fill `labels.csv`. Gold is shown here only for grading; it never reached the agent.

## test-a1 · answerable · status **answered**

**Question:** What share of people in low-income countries are in extreme poverty in 2024?
**Expected answer:** 43 percent of people in low-income countries are in extreme poverty in 2024.
**Gold evidence (p39):** "In 2024, 43 percent of people in low-income countries are in extreme poverty."
**Context evidence hit (automatic):** True

**Searches:** `low income countries extreme poverty 2024 share` → ['p041s0:c000', 'p039s0:c000', 'p066s0:c000']
**Final context IDs:** ['p041s0:c000', 'p039s0:c000', 'p066s0:c000']

**Agent answer:** In 2024, 43 percent of people in low-income countries are in extreme poverty [B:wb-ppp-2024:p039s0:c000].

> Citation 1: `B:wb-ppp-2024:p039s0:c000` (page 39)  
> The poorest countries have still not recovered from the poverty increase caused by the COVID-19 pandemic  The poorest countries still have higher poverty rates than before the pandemic. In low-income countries, the extreme poverty rate rose in 2020 and 2021 and has not fallen much since (figure O.3). In 2024, 43 percent of people in low-income countries are in extreme poverty. Lower-middle-income countries managed to recover from the COVID-19 shock only in 2022. In contrast, upper-middle-income countries continued to make progress in 2021 and 2022 against poverty (as measured against the $6.85 line, which is more relevant in these settings).

---

## test-a2 · answerable · status **answered**

**Question:** Which welfare measure, income, consumption or wealth, tends to be distributed the most unequally?
**Expected answer:** Wealth: its distribution tends to be much more unequal than either income or consumption.
**Gold evidence (p47):** "The distribution of wealth tends to be much more unequal than either income or consumption."
**Context evidence hit (automatic):** True

**Searches:** `welfare measure income consumption wealth distributed unequally` → ['p047s0:c000', 'p047s0:c001', 'p047s0:c002']
**Final context IDs:** ['p047s0:c000', 'p047s0:c001', 'p047s0:c002']

**Agent answer:** The distribution of wealth tends to be much more unequal than either income or consumption [B:wb-ppp-2024:p047s0:c001].

> Citation 1: `B:wb-ppp-2024:p047s0:c001` (page 47)  
> This implies that the distribution of consumption tends to be more equal than the distribution of income (see annex 2D and chapter 4 for further detail). Whereas income and consumption both represent the flow of resources—that is, how much one earns or spends in a given time frame, typically a year— wealth represents a stock of resource such as accumulated assets, including property, corporate stock holdings, or savings, as well as other investments that can be inherited or acquired. For example, a house (or stock) is wealth, and the rent (or dividends) is the income generated from this asset. The distribution of wealth tends to be much more unequal than either income or consumption. a  These concepts are interlinked.

---

## test-a3 · answerable · status **abstain** (model_abstained)

**Question:** How many countries does the indicator of people at high risk from climate-related hazards cover, and what share of the world population do they represent?
**Expected answer:** A sample of 103 countries with data on all vulnerability dimensions, covering 86 percent of the world population.
**Gold evidence (p52):** "The indicator is based on a sample of 103 countries with data on all vulnerability dimensions and covers 86 percent of the world population."
**Context evidence hit (automatic):** False

**Searches:** `indicator of people at high risk from climate-related hazards cover share world population` → ['p049s0:c002', 'p049s0:c003', 'p051s0:c000'] · `indicator of people at high risk from climate-related hazards countries share world population` → ['p049s0:c002', 'p049s0:c003', 'p051s0:c000'] · `indicator of people at high risk from climate-related hazards covers countries share` → ['p049s0:c002', 'p049s0:c003', 'p051s0:c000']
**Final context IDs:** ['p049s0:c002', 'p049s0:c003', 'p051s0:c000']

**Agent abstained.** Model reason: The provided passages do not state the number of countries covered by the indicator of people at high risk from climate-related hazards.

---

## test-a4 · answerable · status **answered**

**Question:** In Sub-Saharan Africa, what share of the population has access to electricity and to basic drinking water?
**Expected answer:** Only 50 percent has access to electricity and 65 percent has access to basic drinking water.
**Gold evidence (p53):** "only 50 percent of the population in Sub-Saharan Africa has access to electricity, and 65 percent has access to basic drinking water."
**Context evidence hit (automatic):** True

**Searches:** `Sub-Saharan Africa access to electricity basic drinking water share population` → ['p053s0:c001', 'p041s0:c004', 'p041s0:c000']
**Final context IDs:** ['p053s0:c001', 'p041s0:c004', 'p041s0:c000']

**Agent answer:** In Sub-Saharan Africa, 50 percent of the population has access to electricity and 65 percent has access to basic drinking water [B:wb-ppp-2024:p053s0:c001].

> Citation 1: `B:wb-ppp-2024:p053s0:c001` (page 53)  
> To summarize, comparisons between exposure and risk show that risks can be mitigated by reducing vulnerability. While exposure in Sub-Saharan Africa is not as high as in other regions, high levels of vulnerability keep people at high risk. The availability in the region of factors that are important for resilience, such as access to basic infrastructure services (for example, water and electricity), income, education, and financial services, is limited. For instance, only 50 percent of the population in Sub-Saharan Africa has access to electricity, and 65 percent has access to basic drinking water.11 These deprivations make people more vulnerable to adverse shocks.

---

## test-a5 · answerable · status **answered**

**Question:** What proportion of Sub-Saharan Africans facing severe climate hazards fall outside social protection systems?
**Expected answer:** 71.2 percent of the people exposed to severe cyclones, floods, droughts and heatwaves are neither covered nor contributing to social protection.
**Gold evidence (p56):** "in Sub-Saharan Africa, 71.2 percent of the people exposed to severe cyclones, floods, droughts, and heatwaves are neither covered nor contributing to social protection"
**Context evidence hit (automatic):** True

**Searches:** `Sub Saharan Africans severe climate hazards social protection systems proportion` → ['p056s0:c002', 'p049s0:c004', 'p057s0:c000']
**Final context IDs:** ['p056s0:c002', 'p049s0:c004', 'p057s0:c000']

**Agent answer:** In Sub-Saharan Africa, 71.2 percent of people exposed to severe cyclones, floods, droughts, and heatwaves are neither covered nor contributing to social protection [B:wb-ppp-2024:p056s0:c002].

> Citation 1: `B:wb-ppp-2024:p056s0:c002` (page 56)  
> Yet, in Sub-Saharan Africa, 71.2 percent of the people exposed to severe cyclones, floods, droughts, and heatwaves are neither covered nor contributing to social protection and are unlikely to receive public support when one of these severe events occurs (figure O.8). Additionally, not all of those covered will have their climate risk fully covered by public safety nets.

---

## test-a6 · answerable · status **answered**

**Question:** According to simulations, what would combined investment in renewable energy and energy efficiency do to the additional emissions that come with the growth needed to reduce poverty?
**Expected answer:** It would lower those additional emissions by more than half.
**Gold evidence (p60):** "Simulations indicate that investing in renewable energy and energy efficiency combined would in fact lower the additional emissions that accompany the economic growth needed to reduce poverty by more than half"
**Context evidence hit (automatic):** True

**Searches:** `combined investment renewable energy energy efficiency additional emissions growth reduce poverty simulations` → ['p060s0:c001', 'p060s0:c000', 'p057s0:c004']
**Final context IDs:** ['p060s0:c001', 'p060s0:c000', 'p057s0:c004']

**Agent answer:** Simulations indicate that combined investment in renewable energy and energy efficiency would lower the additional emissions accompanying the economic growth needed to reduce poverty by more than half [B:wb-ppp-2024:p060s0:c001].

> Citation 1: `B:wb-ppp-2024:p060s0:c001` (page 60)  
> For example, in countries such as Uzbekistan and Côte d’Ivoire, where gas supplies are decreasing and electricity demand is rising, transforming power systems to renewable energy is the most cost-efficient solution (World Bank Group 2023). These investments are also synergistic in the sense that they can ease the trade-off between economic growth, poverty reduction, and emissions. Simulations indicate that investing in renewable energy and energy efficiency combined would in fact lower the additional emissions that accompany the economic growth needed to reduce poverty by more than half (figure O.11) (Wollburg, Hallegatte, and Mahler 2023).

---

## test-a7 · answerable · status **answered**

**Question:** What kind of policy instrument is the Carbon Border Adjustment Mechanism, and which exports does it penalize?
**Expected answer:** A carbon tariff that penalizes high-carbon exports to the European Union.
**Gold evidence (p63):** "the Carbon Border Adjustment Mechanism (CBAM), a carbon tariff that penalizes high-carbon exports to the European Union."
**Context evidence hit (automatic):** True

**Searches:** `Carbon Border Adjustment Mechanism policy instrument exports penalize` → ['p063s0:c001', 'p064s0:c000', 'p058s0:c000']
**Final context IDs:** ['p063s0:c001', 'p064s0:c000', 'p058s0:c000']

**Agent answer:** The Carbon Border Adjustment Mechanism (CBAM) is a carbon tariff that penalizes high-carbon exports to the European Union [B:wb-ppp-2024:p063s0:c001].

> Citation 1: `B:wb-ppp-2024:p063s0:c001` (page 63)  
> There are also major gender differences in green employment across all major occupation groups, with women tending to have browner jobs (World Bank 2022d). Workers in carbon-intensive sectors can be affected not only by local energy transition policies but also by the global consequences of carbon mitigation policies on trade flows. Changes in goods and labor demands may originate from abroad. Take, for example, the Carbon Border Adjustment Mechanism (CBAM), a carbon tariff that penalizes high-carbon exports to the European Union.

---

## test-a8 · answerable · status **answered**

**Question:** As of 2022, what share of all historical CO2 emissions were high-income and upper-middle-income countries responsible for, and how much of that came from high-income countries?
**Expected answer:** 90 percent of all historical CO2 emissions, of which high-income countries make up roughly two-thirds.
**Gold evidence (p70):** "In 2022, high-income countries and upper-middle-income countries were responsible for 90 percent of all historical CO2 emissions, of which emissions from high-income countries make up roughly two-thirds."
**Context evidence hit (automatic):** True

**Searches:** `share of all historical CO2 emissions high-income upper-middle-income countries 2022` → ['p070s0:c000', 'p069s0:c003', 'p069s0:c004']
**Final context IDs:** ['p070s0:c000', 'p069s0:c003', 'p069s0:c004']

**Agent answer:** In 2022, high-income and upper-middle-income countries were responsible for 90 percent of all historical CO2 emissions [B:wb-ppp-2024:p070s0:c000]. Of those historical emissions, roughly two-thirds came from high-income countries [B:wb-ppp-2024:p070s0:c000].

> Citation 1: `B:wb-ppp-2024:p070s0:c000` (page 70)  
> stock of GHG emissions in the atmosphere is what matters for warming (Eyring et al. 2021; IPCC 2022a). Today’s high-income countries started emitting large amounts of CO2 in the mid-nineteenth century, and upper-middle-income countries have caught up quickly over the past 40 years (figure O.15, panel c). In 2022, high-income countries and upper-middle-income countries were responsible for 90 percent of all historical CO2 emissions, of which emissions from high-income countries make up roughly two-thirds.

---

## test-a9 · answerable · status **answered**

**Question:** In the Priorities section of the overview, how many IDA countries had a household survey available in 2020 or later?  
**Filter:** `{'section': 'priorities'}`
**Expected answer:** Less than half of IDA countries had a household survey available in 2020 or later.
**Gold evidence (p72):** "less than half of IDA countries had a household survey available in 2020 or later."
**Context evidence hit (automatic):** True

**Searches:** `Priorities household survey 2020 IDA countries` → ['p072s0:c002', 'p067s0:c001', 'p066s0:c001']
**Final context IDs:** ['p072s0:c002', 'p067s0:c001', 'p066s0:c001']

**Agent answer:** Less than half of IDA countries had a household survey available in 2020 or later [B:wb-ppp-2024:p072s0:c002].

> Citation 1: `B:wb-ppp-2024:p072s0:c002` (page 72)  
> Across the board, more and better data are needed to design solutions that can address these complex policy issues and monitor their effects on vulnerable populations. Data provide the infrastructure for policy. This is essential to both designing and targeting interventions as well as monitoring progress. While data availability has improved in many countries, less than half of IDA countries had a household survey available in 2020 or later. Making progress on these interlinked global challenges requires a solid foundation of evidence. More investment is needed to produce reliable, granular, and timely information. This requires foundational efforts to strengthen national statistical systems and innovative approaches to advance the frontier of data and modeling for welfare analysis.

---

## test-u1 · UNANSWERABLE · status **abstain** (model_abstained)

**Question:** How many households did the Philippines' Pantawid Pamilyang Pilipino Program support after Typhoon Yolanda in 2013?
**Why unanswerable:** Page 56 says the program supported recipients hit by the typhoon but gives no number; the household counts in the same chunk (100,000 and 200,000) belong to Kenya's Hunger Safety Net Programme.

**Searches:** `Philippines Pantawid Pamilyang Pilipino Program Typhoon Yolanda 2013 households` → ['p056s0:c001', 'p063s0:c005', 'p040s0:c003'] · `Pantawid Pamilyang Pilipino Program Typhoon Yolanda households` → ['p056s0:c001', 'p063s0:c005', 'p055s0:c002'] · `Pantawid Pamilyang Pilipino Program Typhoon Yolanda households number` → ['p056s0:c001', 'p063s0:c005', 'p051s0:c000']
**Final context IDs:** ['p056s0:c001', 'p063s0:c005', 'p040s0:c003', 'p055s0:c002']

**Agent abstained.** Model reason: The provided passages mention that the Philippines supported recipients of the Pantawid Pamilyang Pilipino Program after Typhoon Yolanda in 2013, but they do not state the exact number of households supported.

---

## test-u2 · UNANSWERABLE · status **abstain** (model_abstained)

**Question:** What is the youth unemployment rate in Sub-Saharan Africa?
**Why unanswerable:** The Overview discusses jobs and labor markets but never mentions unemployment or youth.

**Searches:** `youth unemployment rate in Sub Saharan Africa` → ['p041s0:c004', 'p040s0:c004', 'p041s0:c001'] · `youth unemployment rate Sub Saharan Africa` → ['p041s0:c004', 'p040s0:c004', 'p041s0:c001'] · `youth unemployment rate Sub-Saharan Africa` → ['p041s0:c004', 'p041s0:c001', 'p040s0:c004']
**Final context IDs:** ['p041s0:c004', 'p040s0:c004', 'p041s0:c001']

**Agent abstained.** Model reason: The provided passages do not contain information about the youth unemployment rate in Sub-Saharan Africa.

---

## test-u3 · UNANSWERABLE · status **abstain** (model_abstained)

**Question:** What share of Indonesia's coal production is exported?
**Why unanswerable:** Page 62 calls Indonesia the world's second-largest coal exporter and gives the coal industry's GDP and employment shares, but not the share of production exported.

**Searches:** `Indonesia coal production exported share percentage` → ['p062s0:c005', 'p049s0:c003', 'p051s0:c000'] · `Indonesia coal production exported share` → ['p062s0:c005', 'p049s0:c003', 'p058s0:c001'] · `Indonesia coal export share percentage production` → ['p062s0:c005', 'p049s0:c003', 'p051s0:c000']
**Final context IDs:** ['p062s0:c005', 'p049s0:c003', 'p051s0:c000', 'p058s0:c001']

**Agent abstained.** Model reason: The provided passages do not contain information about the share of Indonesia's coal production that is exported.

---
