# Review sheet: `agent_test_dense_b800_test-baseline_20261116T085657Z`

Read each case, check the agent answer and every citation against the cited text (and the PDF when needed), then fill `labels.csv`. Gold is shown here only for grading; it never reached the agent.

## test-a1 · answerable · status **abstain** (model_abstained)

**Question:** What share of people in low-income countries are in extreme poverty in 2024?
**Expected answer:** 43 percent of people in low-income countries are in extreme poverty in 2024.
**Gold evidence (p39):** "In 2024, 43 percent of people in low-income countries are in extreme poverty."
**Context evidence hit (automatic):** False

**Searches:** `low-income countries extreme poverty 2024 share` → ['p036s0:c000', 'p041s0:c000', 'p036s0:c002'] · `low-income countries extreme poverty share 2024` → ['p036s0:c000', 'p041s0:c000', 'p036s0:c002'] · `low-income countries extreme poverty 2024 share poverty rate` → ['p036s0:c000', 'p041s0:c000', 'p036s0:c001']
**Final context IDs:** ['p036s0:c000']

**Agent abstained.** Model reason: The provided passages do not contain the specific share of people in extreme poverty in low-income countries in 2024.

---

## test-a2 · answerable · status **answered**

**Question:** Which welfare measure, income, consumption or wealth, tends to be distributed the most unequally?
**Expected answer:** Wealth: its distribution tends to be much more unequal than either income or consumption.
**Gold evidence (p47):** "The distribution of wealth tends to be much more unequal than either income or consumption."
**Context evidence hit (automatic):** False

**Searches:** `income consumption wealth distributed unequally welfare measure` → ['p047s0:c001', 'p047s0:c000', 'p063s0:c005'] · `wealth inequality income consumption most unequally welfare space` → ['p047s0:c000', 'p047s0:c001', 'p046s0:c005'] · `wealth consumption income distributed inequality most unequally welfare space` → ['p047s0:c001', 'p047s0:c000', 'p046s0:c005']
**Final context IDs:** ['p047s0:c000']

**Agent answer:** The provided passages do not contain information on which welfare measure tends to be distributed the most unequally [B:wb-ppp-2024:p047s0:c000].

> Citation 1: `B:wb-ppp-2024:p047s0:c000` (page 47)  
> BOX O.2  Concepts of welfare and differences in measured inequality  The level of inequality depends on the underlying concept of welfare that is captured. Economic inequality is generally captured in three different welfare spaces—income, consumption, or wealth—each reflecting different aspects of welfare and different observed levels of inequality. Whereas income signals an individual’s or family’s potential buying power, consumption expenditure is the realization of that buying power. Households generally do not consume all their income. What is left over, that is, savings, tends to be greater for the richer households compared with poorer households.

---

## test-a3 · answerable · status **abstain** (model_abstained)

**Question:** How many countries does the indicator of people at high risk from climate-related hazards cover, and what share of the world population do they represent?
**Expected answer:** A sample of 103 countries with data on all vulnerability dimensions, covering 86 percent of the world population.
**Gold evidence (p52):** "The indicator is based on a sample of 103 countries with data on all vulnerability dimensions and covers 86 percent of the world population."
**Context evidence hit (automatic):** False

**Searches:** `people at high risk from climate-related hazards countries share of world population` → ['p049s0:c002', 'p051s0:c000', 'p049s0:c003'] · `countries indicator people at high risk from climate-related hazards share of the world population` → ['p049s0:c003', 'p049s0:c002', 'p051s0:c000'] · `indicator of people at high risk from climate related hazards countries share world population` → ['p049s0:c002', 'p049s0:c003', 'p051s0:c000']
**Final context IDs:** ['p051s0:c000']

**Agent abstained.** Model reason: The passages explain how the indicator is calculated globally as a share of the global population, but do not provide the number of countries covered or their share of the world population.

---

## test-a4 · answerable · status **answered**

**Question:** In Sub-Saharan Africa, what share of the population has access to electricity and to basic drinking water?
**Expected answer:** Only 50 percent has access to electricity and 65 percent has access to basic drinking water.
**Gold evidence (p53):** "only 50 percent of the population in Sub-Saharan Africa has access to electricity, and 65 percent has access to basic drinking water."
**Context evidence hit (automatic):** True

**Searches:** `Sub-Saharan Africa access to electricity and basic drinking water share` → ['p053s0:c001', 'p056s0:c002', 'p067s0:c003']
**Final context IDs:** ['p053s0:c001']

**Agent answer:** In Sub-Saharan Africa, 50 percent of the population has access to electricity, and 65 percent has access to basic drinking water [B:wb-ppp-2024:p053s0:c001].

> Citation 1: `B:wb-ppp-2024:p053s0:c001` (page 53)  
> To summarize, comparisons between exposure and risk show that risks can be mitigated by reducing vulnerability. While exposure in Sub-Saharan Africa is not as high as in other regions, high levels of vulnerability keep people at high risk. The availability in the region of factors that are important for resilience, such as access to basic infrastructure services (for example, water and electricity), income, education, and financial services, is limited. For instance, only 50 percent of the population in Sub-Saharan Africa has access to electricity, and 65 percent has access to basic drinking water.11 These deprivations make people more vulnerable to adverse shocks.

---

## test-a5 · answerable · status **answered**

**Question:** What proportion of Sub-Saharan Africans facing severe climate hazards fall outside social protection systems?
**Expected answer:** 71.2 percent of the people exposed to severe cyclones, floods, droughts and heatwaves are neither covered nor contributing to social protection.
**Gold evidence (p56):** "in Sub-Saharan Africa, 71.2 percent of the people exposed to severe cyclones, floods, droughts, and heatwaves are neither covered nor contributing to social protection"
**Context evidence hit (automatic):** True

**Searches:** `Sub Saharan Africans severe climate hazards social protection systems proportion` → ['p056s0:c002', 'p053s0:c001', 'p049s0:c004']
**Final context IDs:** ['p056s0:c002']

**Agent answer:** In Sub-Saharan Africa, 71.2 percent of people exposed to severe climate hazards such as cyclones, floods, droughts, and heatwaves are neither covered nor contributing to social protection [B:wb-ppp-2024:p056s0:c002].

> Citation 1: `B:wb-ppp-2024:p056s0:c002` (page 56)  
> Yet, in Sub-Saharan Africa, 71.2 percent of the people exposed to severe cyclones, floods, droughts, and heatwaves are neither covered nor contributing to social protection and are unlikely to receive public support when one of these severe events occurs (figure O.8). Additionally, not all of those covered will have their climate risk fully covered by public safety nets.

---

## test-a6 · answerable · status **answered**

**Question:** According to simulations, what would combined investment in renewable energy and energy efficiency do to the additional emissions that come with the growth needed to reduce poverty?
**Expected answer:** It would lower those additional emissions by more than half.
**Gold evidence (p60):** "Simulations indicate that investing in renewable energy and energy efficiency combined would in fact lower the additional emissions that accompany the economic growth needed to reduce poverty by more than half"
**Context evidence hit (automatic):** True

**Searches:** `combined investment renewable energy energy efficiency additional emissions growth poverty simulations` → ['p060s0:c001', 'p060s0:c000', 'p069s0:c002']
**Final context IDs:** ['p060s0:c001']

**Agent answer:** Simulations indicate that combined investments in renewable energy and energy efficiency would lower the additional emissions accompanying the economic growth needed to reduce poverty by more than half [B:wb-ppp-2024:p060s0:c001].

> Citation 1: `B:wb-ppp-2024:p060s0:c001` (page 60)  
> For example, in countries such as Uzbekistan and Côte d’Ivoire, where gas supplies are decreasing and electricity demand is rising, transforming power systems to renewable energy is the most cost-efficient solution (World Bank Group 2023). These investments are also synergistic in the sense that they can ease the trade-off between economic growth, poverty reduction, and emissions. Simulations indicate that investing in renewable energy and energy efficiency combined would in fact lower the additional emissions that accompany the economic growth needed to reduce poverty by more than half (figure O.11) (Wollburg, Hallegatte, and Mahler 2023).

---

## test-a7 · answerable · status **answered**

**Question:** What kind of policy instrument is the Carbon Border Adjustment Mechanism, and which exports does it penalize?
**Expected answer:** A carbon tariff that penalizes high-carbon exports to the European Union.
**Gold evidence (p63):** "the Carbon Border Adjustment Mechanism (CBAM), a carbon tariff that penalizes high-carbon exports to the European Union."
**Context evidence hit (automatic):** True

**Searches:** `Carbon Border Adjustment Mechanism policy instrument exports penalize` → ['p063s0:c001', 'p063s0:c002', 'p069s0:c002']
**Final context IDs:** ['p063s0:c001']

**Agent answer:** The Carbon Border Adjustment Mechanism (CBAM) is a carbon tariff that penalizes high-carbon exports to the European Union [B:wb-ppp-2024:p063s0:c001].

> Citation 1: `B:wb-ppp-2024:p063s0:c001` (page 63)  
> There are also major gender differences in green employment across all major occupation groups, with women tending to have browner jobs (World Bank 2022d). Workers in carbon-intensive sectors can be affected not only by local energy transition policies but also by the global consequences of carbon mitigation policies on trade flows. Changes in goods and labor demands may originate from abroad. Take, for example, the Carbon Border Adjustment Mechanism (CBAM), a carbon tariff that penalizes high-carbon exports to the European Union.

---

## test-a8 · answerable · status **answered**

**Question:** As of 2022, what share of all historical CO2 emissions were high-income and upper-middle-income countries responsible for, and how much of that came from high-income countries?
**Expected answer:** 90 percent of all historical CO2 emissions, of which high-income countries make up roughly two-thirds.
**Gold evidence (p70):** "In 2022, high-income countries and upper-middle-income countries were responsible for 90 percent of all historical CO2 emissions, of which emissions from high-income countries make up roughly two-thirds."
**Context evidence hit (automatic):** True

**Searches:** `historical CO2 emissions high income upper middle income 2022` → ['p070s0:c000', 'p069s0:c004', 'p064s1:c003']
**Final context IDs:** ['p070s0:c000']

**Agent answer:** In 2022, high-income and upper-middle-income countries were responsible for 90 percent of all historical CO2 emissions, with roughly two-thirds of that coming from high-income countries [B:wb-ppp-2024:p070s0:c000].

> Citation 1: `B:wb-ppp-2024:p070s0:c000` (page 70)  
> stock of GHG emissions in the atmosphere is what matters for warming (Eyring et al. 2021; IPCC 2022a). Today’s high-income countries started emitting large amounts of CO2 in the mid-nineteenth century, and upper-middle-income countries have caught up quickly over the past 40 years (figure O.15, panel c). In 2022, high-income countries and upper-middle-income countries were responsible for 90 percent of all historical CO2 emissions, of which emissions from high-income countries make up roughly two-thirds.

---

## test-a9 · answerable · status **abstain** (model_abstained)

**Question:** In the Priorities section of the overview, how many IDA countries had a household survey available in 2020 or later?  
**Filter:** `{'section': 'priorities'}`
**Expected answer:** Less than half of IDA countries had a household survey available in 2020 or later.
**Gold evidence (p72):** "less than half of IDA countries had a household survey available in 2020 or later."
**Context evidence hit (automatic):** False

**Searches:** `IDA countries household survey available in 2020 or later` → ['p072s0:c002', 'p066s0:c001', 'p067s0:c001'] · `IDA countries household survey available in 2020 or later` → ['p072s0:c002', 'p066s0:c001', 'p067s0:c001'] · `IDA countries household survey available in 2020 or later priorities` → ['p072s0:c002', 'p066s0:c001', 'p065s0:c001']
**Final context IDs:** ['p066s0:c001', 'p065s0:c001']

**Agent abstained.** Model reason: The retrieved passages do not contain information about the number of IDA countries that had a household survey available in 2020 or later.

---

## test-u1 · UNANSWERABLE · status **answered**

**Question:** How many households did the Philippines' Pantawid Pamilyang Pilipino Program support after Typhoon Yolanda in 2013?
**Why unanswerable:** Page 56 says the program supported recipients hit by the typhoon but gives no number; the household counts in the same chunk (100,000 and 200,000) belong to Kenya's Hunger Safety Net Programme.

**Searches:** `Pantawid Pamilyang Pilipino Program Typhoon Yolanda 2013 households` → ['p056s0:c001', 'p063s0:c005', 'p049s0:c001'] · `Pantawid Pamilyang Pilipino Program Typhoon Yolanda 2013 households number` → ['p056s0:c001', 'p063s0:c005', 'p072s0:c002'] · `Pantawid Pamilyang Pilipino Program Yolanda households number 2013` → ['p056s0:c001', 'p063s0:c005', 'p072s0:c002']
**Final context IDs:** ['p056s0:c001']

**Agent answer:** The passages do not mention the exact number of households that the Philippines' Pantawid Pamilyang Pilipino Program supported after Typhoon Yolanda in 2013 [B:wb-ppp-2024:p056s0:c001].

> Citation 1: `B:wb-ppp-2024:p056s0:c001` (page 56)  
> For example, the Philippines supported recipients of its flagship social safety net program, the Pantawid Pamilyang Pilipino Program, when they were hit by Typhoon Y olanda in 2013 (World Bank 2022c). In Kenya, the Hunger Safety Net Programme provided aid to over 100,000 additional households in response to droughts during 2015 and issued a special transfer to 200,000 households in anticipation of expected droughts (Hallegatte et al. 2016). Anticipatory cash transfers before the traditional humanitarian response would normally arrive can have a significant additional welfare effect (Pople et al. 2021).

---

## test-u2 · UNANSWERABLE · status **abstain** (model_abstained)

**Question:** What is the youth unemployment rate in Sub-Saharan Africa?
**Why unanswerable:** The Overview discusses jobs and labor markets but never mentions unemployment or youth.

**Searches:** `youth unemployment rate Sub-Saharan Africa` → ['p041s0:c004', 'p056s0:c002', 'p041s0:c001'] · `youth unemployment rate Sub-Saharan Africa 2024 report` → ['p056s0:c002', 'p041s0:c004', 'p041s0:c001'] · `youth unemployment rate Sub-Saharan Africa percent` → ['p056s0:c002', 'p041s0:c004', 'p046s0:c005']
**Final context IDs:** ['p041s0:c004']

**Agent abstained.** Model reason: The provided passages do not contain information about the youth unemployment rate in Sub-Saharan Africa.

---

## test-u3 · UNANSWERABLE · status **abstain** (model_abstained)

**Question:** What share of Indonesia's coal production is exported?
**Why unanswerable:** Page 62 calls Indonesia the world's second-largest coal exporter and gives the coal industry's GDP and employment shares, but not the share of production exported.

**Searches:** `Indonesia coal production exported share percentage` → ['p062s0:c005', 'p049s0:c003', 'p069s0:c003'] · `Indonesia coal production exported share percentage` → ['p062s0:c005', 'p049s0:c003', 'p069s0:c003'] · `Indonesia coal production exported share` → ['p062s0:c005', 'p058s0:c001', 'p049s0:c003']
**Final context IDs:** ['p062s0:c005']

**Agent abstained.** Model reason: The provided passages do not contain information on the share of Indonesia's coal production that is exported.

---
