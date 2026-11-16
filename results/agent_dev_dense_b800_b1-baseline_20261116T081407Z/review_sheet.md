# Review sheet: `agent_dev_dense_b800_b1-baseline_20261116T081407Z`

Read each case, check the agent answer and every citation against the cited text (and the PDF when needed), then fill `labels.csv`. Gold is shown here only for grading; it never reached the agent.

## dev-q01 · answerable · status **answered**

**Question:** What share of the global population lives in extreme poverty in 2024, and how many people is that?
**Expected answer:** About 8.5 percent of the global population, i.e. 692 million people living on less than $2.15 per person per day.
**Gold evidence (p35):** "About 8.5 percent of the global population lives in extreme poverty in 2024. This means that 692 million people worldwide live on less than $2.15 per person per day"
**Context evidence hit (automatic):** False

**Searches:** `global population extreme poverty share 2024 how many people` → ['p036s0:c000', 'p036s0:c001', 'p036s0:c002'] · `extreme poverty share global population 2024 how many people number` → ['p036s0:c000', 'p036s0:c001', 'p036s0:c002'] · `Extreme poverty share 2024 how many people $2.15` → ['p036s0:c000', 'p036s0:c001', 'p041s0:c000']
**Final context IDs:** ['p036s0:c000']

**Agent answer:** The global extreme poverty rate fell to 8.5 percent in 2024 [B:wb-ppp-2024:p036s0:c000]. However, the provided passages do not specify the exact number of people living in extreme poverty in 2024 [B:wb-ppp-2024:p036s0:c000].

> Citation 1: `B:wb-ppp-2024:p036s0:c000` (page 36)  
> poverty rate fell from 38 percent in 1990 to 8.5 percent in 2024, it has stalled more recently amid lower economic growth and multiple shocks such as the COVID-19 pandemic, high inflation, and increased conflict and fragility. Extreme poverty today is only slightly below the rate observed before the pandemic in 2019 and in many poor settings, poverty rates remain higher than they were five years ago. Using the slightly higher poverty line of $3.65 a day per person (representative of the national poverty lines used in lower-middle-income countries), about 1.7 billion people are living in poverty in 2024 (21.4 percent, or about one-fifth, of the global population).

---

## dev-q02 · answerable · status **answered**

**Question:** Under a scenario where every country grows 2 percent per capita per year, how much faster would poverty be eradicated if each country's Gini index also fell by 2 percent annually?
**Expected answer:** It would take 40 years less: 20 years instead of 60 years.
**Gold evidence (p36):** "under the 2 percent per capita growth scenario, if the Gini index in every country were to also decrease by 2 percent annually, it would take 40 years less to eradicate poverty (20 versus 60 years)."
**Context evidence hit (automatic):** True

**Searches:** `Gini index fell by 2 percent annually poverty eradicated` → ['p036s0:c004', 'p036s0:c000', 'p045s0:c001']
**Final context IDs:** ['p036s0:c004']

**Agent answer:** Under a scenario where every country grows 2 percent per capita per year and each country's Gini index also falls by 2 percent annually, poverty would be eradicated 40 years faster (taking 20 years instead of 60 years) [B:wb-ppp-2024:p036s0:c004].

> Citation 1: `B:wb-ppp-2024:p036s0:c004` (page 36)  
> For example, under the 2 percent per capita growth scenario, if the Gini index in every country were to also decrease by 2 percent annually, it would take 40 years less to eradicate poverty (20 versus 60 years). Poverty rates at $6.85 a day are projected to fall faster under the current growth forecast scenario than extreme poverty rates (figure O.2, panel b). Still, under the current growth forecast, it would take more than a century to reach a poverty rate of less than 3 percent at $6.85 per person per day.

---

## dev-q03 · answerable · status **abstain** (model_abstained)

**Question:** How much in potential lifetime earnings does the current generation of students risk losing, in present value?
**Expected answer:** $21 trillion in potential lifetime earnings in present value, equivalent to 17 percent of today's global GDP.
**Gold evidence (p40):** "This generation of students now risks losing $21 trillion in potential lifetime earnings in present value, or the equivalent of 17 percent of today’s global GDP"
**Context evidence hit (automatic):** False

**Searches:** `potential lifetime earnings present value current generation students losing` → ['p040s0:c002', 'p036s0:c004', 'p043s0:c001'] · `lifetime earnings current generation students losing present value` → ['p040s0:c002', 'p040s0:c001', 'p067s0:c002'] · `lifetime earnings present value students risk losing` → ['p040s0:c002', 'p054s0:c004', 'p054s0:c003']
**Final context IDs:** ['p036s0:c004']

**Agent abstained.** Model reason: The available passages do not contain information about the potential lifetime earnings that the current generation of students risks losing in present value.

---

## dev-q04 · answerable · status **abstain** (model_abstained)

**Question:** In the Progress section of the overview, what share of the global extreme poor live in countries eligible for IDA support?  
**Filter:** `{'section': 'progress'}`
**Expected answer:** IDA-eligible countries account for 7 in 10 of the global extreme poor.
**Gold evidence (p41):** "countries eligible for support through the International Development Association (IDA) account for 7 in 10 of the global extreme poor."
**Context evidence hit (automatic):** False

**Searches:** `share of the global extreme poor live in countries eligible for IDA support Progress overview` → ['p041s0:c000', 'p035s0:c003', 'p035s0:c001'] · `IDA support extreme poor progress overview` → ['p041s0:c001', 'p035s0:c003', 'p041s0:c000'] · `extreme poor live in countries eligible for IDA support Progress overview` → ['p041s0:c000', 'p039s0:c000', 'p035s0:c001']
**Final context IDs:** ['p035s0:c003']

**Agent abstained.** Model reason: The provided passage does not contain information about the share of the global extreme poor living in countries eligible for IDA support.

---

## dev-q05 · answerable · status **answered**

**Question:** What is the Global Prosperity Gap and what prosperity standard does it use?
**Expected answer:** It is the average factor by which incomes need to be multiplied to bring everyone in the world to the prosperity standard of $25 per person per day.
**Gold evidence (p41):** "It is the average factor by which incomes need to be multiplied to bring everyone in the world to the prosperity standard of $25 per person per day"
**Gold evidence (p42):** "The Prosperity Gap is defined as the average income multiple needed to reach that $25 standard for every member of that society"
**Context evidence hit (automatic):** False

**Searches:** `Global Prosperity Gap prosperity standard` → ['p044s0:c000', 'p042s0:c000', 'p041s0:c004'] · `Global Prosperity Gap prosperity standard definition` → ['p042s0:c000', 'p041s0:c003', 'p044s0:c000'] · `Global Prosperity Gap standard` → ['p042s0:c000', 'p041s0:c004', 'p044s0:c000']
**Final context IDs:** ['p044s0:c000']

**Agent answer:** The passages do not provide a definition of the Global Prosperity Gap or the specific prosperity standard it uses [B:wb-ppp-2024:p044s0:c000].

> Citation 1: `B:wb-ppp-2024:p044s0:c000` (page 44)  
> Historically, gains in global prosperity have been driven by both overall economic growth and a decline in inequality between countries. Between 1990 and 2024, the Global Prosperity Gap improved at an annual rate of 2.34 percent, with global mean income increasing at an annual rate of 1.48 percent and global inequality declining by 0.86 percent. The decline in global inequality has been driven by a decline in the inequality between countries, which is measured by the disparities in average living standards across countries (Kraay et al. 2023; Lakner and Milanovic 2016).

---

## dev-q06 · answerable · status **answered**

**Question:** At what annual rate did the Global Prosperity Gap improve between 1990 and 2024, and what drove it?
**Expected answer:** 2.34 percent per year, with global mean income rising 1.48 percent per year and global inequality declining by 0.86 percent.
**Gold evidence (p44):** "Between 1990 and 2024, the Global Prosperity Gap improved at an annual rate of 2.34 percent, with global mean income increasing at an annual rate of 1.48 percent and global inequality declining by 0.86 percent."
**Context evidence hit (automatic):** True

**Searches:** `Global Prosperity Gap improve 1990 2024 annual rate drove it` → ['p044s0:c000', 'p044s0:c001', 'p036s0:c000']
**Final context IDs:** ['p044s0:c000']

**Agent answer:** Between 1990 and 2024, the Global Prosperity Gap improved at an annual rate of 2.34 percent, driven by overall economic growth (with global mean income increasing at an annual rate of 1.48 percent) and a decline in global inequality by 0.86 percent [B:wb-ppp-2024:p044s0:c000].

> Citation 1: `B:wb-ppp-2024:p044s0:c000` (page 44)  
> Historically, gains in global prosperity have been driven by both overall economic growth and a decline in inequality between countries. Between 1990 and 2024, the Global Prosperity Gap improved at an annual rate of 2.34 percent, with global mean income increasing at an annual rate of 1.48 percent and global inequality declining by 0.86 percent. The decline in global inequality has been driven by a decline in the inequality between countries, which is measured by the disparities in average living standards across countries (Kraay et al. 2023; Lakner and Milanovic 2016).

---

## dev-q07 · answerable · status **abstain** (model_abstained)

**Question:** What proportion of people worldwide face a high risk of a severe climate shock they would struggle to recover from?
**Expected answer:** Nearly one in five people (17.9 percent).
**Gold evidence (p49):** "Nearly one in five people (17.9 percent) is at high risk from climate-related hazards globally, meaning they are likely to experience a severe climate shock in their lifetime that they will struggle to recover from."
**Context evidence hit (automatic):** False

**Searches:** `proportion of people worldwide high risk severe climate shock struggle to recover` → ['p049s0:c002', 'p056s0:c002', 'p049s0:c001'] · `worldwide face a high risk of a severe climate shock struggle to recover proportion` → ['p049s0:c002', 'p071s0:c000', 'p049s0:c001'] · `proportion of people worldwide face a high risk of a severe climate shock` → ['p049s0:c002', 'p049s0:c004', 'p051s0:c000']
**Final context IDs:** ['p056s0:c002']

**Agent abstained.** Model reason: The provided passages do not contain information about the worldwide proportion of people facing a high risk of a severe climate shock they would struggle to recover from.

---

## dev-q08 · answerable · status **abstain** (model_abstained)

**Question:** In low-income countries, what share of natural disaster losses was covered by insurance?
**Expected answer:** Less than 10 percent of losses were covered by insurance in low-income countries (compared with about one-third of the $380 billion global natural-disaster losses in 2023), forcing governments to redirect limited development funds toward disaster recovery.
**Gold evidence (p55):** "In 2023, the estimated global economic losses due to natural disasters was $380 billion,15 of which only about one-third were covered by insurance. In low-income countries, less than 10 percent of losses were covered by insurance, forcing governments to redirect limited development funds toward disaster recovery."
**Context evidence hit (automatic):** False

**Searches:** `low income countries share natural disaster losses covered by insurance` → ['p057s0:c000', 'p055s0:c003', 'p052s0:c001'] · `low income countries share natural disaster losses covered insurance` → ['p057s0:c000', 'p055s0:c003', 'p056s0:c000'] · `low-income countries share of natural disaster losses covered by insurance` → ['p055s0:c003', 'p052s0:c001', 'p057s0:c000']
**Final context IDs:** ['p057s0:c000']

**Agent abstained.** Model reason: The provided passages do not contain information about the share of natural disaster losses covered by insurance in low-income countries.

---

## dev-q09 · answerable · status **answered**

**Question:** How many people did Bangladesh evacuate for Cyclone Amphan in 2020, and how many fatalities were there?
**Expected answer:** 2.4 million people were evacuated, with 20 fatalities.
**Gold evidence (p57):** "in 2020, Bangladesh evacuated 2.4 million people for Cyclone Amphan, with 20 fatalities."
**Context evidence hit (automatic):** True

**Searches:** `Bangladesh Cyclone Amphan 2020 evacuated fatalities` → ['p057s0:c001', 'p049s0:c001', 'p040s0:c000']
**Final context IDs:** ['p057s0:c001']

**Agent answer:** For Cyclone Amphan in 2020, Bangladesh evacuated 2.4 million people, and there were 20 fatalities [B:wb-ppp-2024:p057s0:c001].

> Citation 1: `B:wb-ppp-2024:p057s0:c001` (page 57)  
> Since then, investments in resilient infrastructure, road networks, and early warning systems have significantly reduced fatalities. Cyclone Sidr in 2007 resulted in 3,363 deaths, Cyclone Fani in 2019 caused five, and in 2020, Bangladesh evacuated 2.4 million people for Cyclone Amphan, with 20 fatalities. Yet, one-fifth of the world’s population is not covered by an early warning system, even though these systems save lives and greatly reduce climate-related disaster losses in developing countries. 16

---

## dev-q10 · answerable · status **abstain** (model_abstained)

**Question:** Relative to 2019, how much additional emissions would eradicating extreme poverty entail, and how much would they reach at the $6.85-per-day poverty line?
**Expected answer:** Eradicating extreme poverty would entail 4.7 percent more emissions than in 2019; at $6.85 per person per day, additional emissions would reach 46 percent (with historical emission intensities).
**Gold evidence (p59):** "Eradicating extreme poverty would entail 4.7 percent more emissions than in 2019 (figure O.10). This number becomes larger at higher poverty lines. At $6.85 per person per day, additional emissions would reach 46 percent with historical emission intensities"
**Context evidence hit (automatic):** False

**Searches:** `eradicating extreme poverty additional emissions 2019 6.85 per day` → ['p059s0:c001', 'p059s0:c002', 'p036s0:c002'] · `6.85 per day additional emissions 2019 poverty prosperity and planet report` → ['p036s0:c001', 'p059s0:c001', 'p036s0:c002'] · `emissions extreme poverty 2019 6.85 poverty prosperity and planet report` → ['p059s0:c001', 'p036s0:c002', 'p064s1:c002']
**Final context IDs:** ['p059s0:c002']

**Agent abstained.** Model reason: The provided passages do not contain the specific numerical values for the additional emissions relative to 2019 from eradicating extreme poverty or reaching the $6.85-per-day poverty line.

---

## dev-q11 · answerable · status **answered**

**Question:** Why are cuts in coal production unlikely to hurt national employment much in a major coal exporter like Indonesia?
**Expected answer:** Because the coal industry has a low labor share: in Indonesia it accounts for less than 2 percent of GDP and employs only 0.2 percent of the workforce.
**Gold evidence (p62):** "Reductions in coal production are unlikely to have substantial effects on national employment and output in many economies because of the industry’s low labor share. For example, in Indonesia, the world’s second-largest coal exporter, the coal industry’s share of the GDP is less than 2 percent, and it employs only 0.2 percent of the workforce"
**Context evidence hit (automatic):** True

**Searches:** `Indonesia coal production employment cuts` → ['p062s0:c005', 'p063s0:c001', 'p063s0:c004']
**Final context IDs:** ['p062s0:c005']

**Agent answer:** Reductions in coal production are unlikely to have a substantial effect on national employment in Indonesia because the coal industry has a low labor share, employing only 0.2 percent of the workforce and accounting for less than 2 percent of the GDP [B:wb-ppp-2024:p062s0:c005].

> Citation 1: `B:wb-ppp-2024:p062s0:c005` (page 62)  
> Transitioning to green industries may lead to or accelerate job displacement in traditional industries that rely heavily on fossil fuels. Reductions in coal production are unlikely to have substantial effects on national employment and output in many economies because of the industry’s low labor share. For example, in Indonesia, the world’s second-largest coal exporter, the coal industry’s share of the GDP is less than 2 percent, and it employs only 0.2 percent of the workforce (World Bank Group 2023). However, effects on local communities can be

---

## dev-q12 · answerable · status **abstain** (model_abstained)

**Question:** How large have interest payments on external debt in IDA countries become?
**Expected answer:** They have quadrupled since 2012, reaching an all-time high of $23.6 billion.
**Gold evidence (p64):** "Interest payments on their total external debt stock in IDA countries have quadrupled since 2012, reaching an all-time high of $23.6 billion"
**Context evidence hit (automatic):** False

**Searches:** `interest payments on external debt IDA countries` → ['p064s1:c001', 'p066s0:c001', 'p067s0:c001'] · `interest payments external debt IDA countries` → ['p064s1:c001', 'p066s0:c001', 'p067s0:c001'] · `interest payments on external debt IDA countries 2024 report` → ['p064s1:c001', 'p066s0:c001', 'p067s0:c001']
**Final context IDs:** ['p066s0:c001']

**Agent abstained.** Model reason: The provided passages do not contain information about interest payments on external debt in IDA countries.

---

## dev-q13 · answerable · status **answered**

**Question:** In the Priorities section of the overview, what share of the global poor are current IDA countries projected to account for in 2030?  
**Filter:** `{'section': 'priorities'}`
**Expected answer:** 82 percent of the global poor in 2030 (and 90 percent of the global extreme poor in 2050), with currently projected growth rates.
**Gold evidence (p66):** "Current IDA countries will comprise 82 percent of the global poor in 2030 with the currently projected growth rates, and 90 percent of the global extreme poor in 2050."
**Context evidence hit (automatic):** True

**Searches:** `global poor IDA countries 2030 Priorities overview` → ['p066s0:c001', 'p066s0:c000', 'p072s0:c002']
**Final context IDs:** ['p066s0:c001']

**Agent answer:** Under currently projected growth rates, current IDA countries are projected to account for 82 percent of the global poor in 2030 [B:wb-ppp-2024:p066s0:c001].

> Citation 1: `B:wb-ppp-2024:p066s0:c001` (page 66)  
> Current IDA countries will comprise 82 percent of the global poor in 2030 with the currently projected growth rates, and 90 percent of the global extreme poor in 2050.

---

## dev-q14 · answerable · status **answered**

**Question:** What shares of global CO2 emissions and of the global population do high-income and upper-middle-income countries account for?
**Expected answer:** High-income countries: 32 percent of global CO2 emissions and 15 percent of the population; upper-middle-income countries: 52 percent of emissions and 35 percent of the population.
**Gold evidence (p69):** "High-income countries and upper-middle-income countries respectively account for 32 percent and 52 percent of global CO2 emissions, while accounting only for 15 percent and 35 percent of the global population."
**Context evidence hit (automatic):** True

**Searches:** `high-income upper-middle-income global CO2 emissions population shares` → ['p069s0:c003', 'p064s1:c003', 'p070s0:c000']
**Final context IDs:** ['p069s0:c003']

**Agent answer:** High-income countries account for 32 percent of global CO2 emissions and 15 percent of the global population, while upper-middle-income countries account for 52 percent of global CO2 emissions and 35 percent of the global population [B:wb-ppp-2024:p069s0:c003].

> Citation 1: `B:wb-ppp-2024:p069s0:c003` (page 69)  
> High-income and upper-middle-income countries: Accelerate mitigation while managing transition costs  High-income countries and upper-middle-income countries respectively account for 32 percent and 52 percent of global CO2 emissions, while accounting only for 15 percent and 35 percent of the global population. Ten economies emit two-thirds of global emissions annually (figure O.15, panel a). The next 30 economies, by total emissions, contribute 24 percent of global emissions. The 140 least-emitting economies, which comprise 12 percent of the total population, produce less than 5 percent of GHG emissions.30

---

## dev-q15 · answerable · status **abstain** (model_abstained)

**Question:** Which country is cited as an example of a country with significant renewable potential that can fully decarbonize its power system without higher costs?
**Expected answer:** Brazil: countries with significant renewable potential, like Brazil, can fully decarbonize their power systems without higher costs or compromising resilience.
**Gold evidence (p71):** "Recent evidence indicates that countries with significant renewable potential, like Brazil, can fully decarbonize their power systems without higher costs or compromising resilience"
**Context evidence hit (automatic):** False

**Searches:** `fully decarbonize its power system without higher costs renewable potential country` → ['p060s0:c001', 'p071s0:c001', 'p072s0:c000'] · `fully decarbonize its power system without higher costs renewable potential country` → ['p060s0:c001', 'p071s0:c001', 'p072s0:c000'] · `decarbonize its power system without higher costs renewable potential country` → ['p060s0:c001', 'p071s0:c001', 'p072s0:c000']
**Final context IDs:** ['p060s0:c001']

**Agent abstained.** Model reason: The provided passage mentions Uzbekistan and Côte d'Ivoire as countries where transforming power systems to renewable energy is cost-efficient due to decreasing gas supplies and rising demand, but it does not cite a country as an example of having significant renewable potential that can fully decarbonize its power system without higher costs.

---

## dev-q16 · answerable · status **abstain** (model_abstained)

**Question:** How has the count of high-inequality economies (Gini above 40) changed over the past decade?
**Expected answer:** It fell from 66 economies a decade earlier to 49 in the most recent year.
**Gold evidence (p46):** "The number of economies with high inequality has fallen, from 66 a decade earlier to 49 in the most recent year."
**Context evidence hit (automatic):** False

**Searches:** `high inequality economies Gini above 40 past decade` → ['p046s0:c003', 'p046s0:c004', 'p045s0:c001'] · `high-inequality economies Gini above 40 count change past decade` → ['p046s0:c003', 'p046s0:c004', 'p045s0:c001'] · `count of high inequality economies Gini above 40 past decade change` → ['p046s0:c003', 'p046s0:c004', 'p045s0:c001']
**Final context IDs:** ['p046s0:c003']

**Agent abstained.** Model reason: The provided passages define the high-inequality threshold (Gini above 40) but do not provide any information regarding how the count of high-inequality economies has changed over the past decade.

---

## dev-q17 · answerable · status **abstain** (model_abstained)

**Question:** How has the share of global emissions covered by carbon taxes and emission trading systems changed since 1990?
**Expected answer:** It increased from 0.15 percent of global emissions in 1990 to 24 percent in 2024.
**Gold evidence (p58):** "The coverage of carbon taxes and emission trading systems (ETS) has increased from 0.15 percent of global emissions in 1990 to 24 percent in 2024."
**Context evidence hit (automatic):** False

**Searches:** `share of global emissions carbon taxes emission trading systems 1990` → ['p058s0:c000', 'p069s0:c003', 'p070s0:c000'] · `share of global emissions covered by carbon taxes and emission trading systems` → ['p069s0:c003', 'p058s0:c000', 'p069s0:c001'] · `global emissions carbon taxes emission trading systems` → ['p058s0:c000', 'p069s0:c003', 'p064s1:c003']
**Final context IDs:** ['p069s0:c003']

**Agent abstained.** Model reason: The provided passages do not contain information about the share of global emissions covered by carbon taxes and emission trading systems.

---

## dev-q18 · answerable · status **abstain** (model_abstained)

**Question:** In the Pathways section of the overview, what global health cost is attributed to air pollution?  
**Filter:** `{'section': 'pathways'}`
**Expected answer:** A global health cost equal to 6.1 percent of global GDP in 2019.
**Gold evidence (p61):** "Air pollution today carries a global health cost representing 6.1 percent of global GDP in 2019"
**Context evidence hit (automatic):** False

**Searches:** `air pollution global health cost pathways overview` → ['p061s0:c000', 'p061s0:c001', 'p058s0:c000'] · `air pollution global health cost pathways overview` → ['p061s0:c000', 'p061s0:c001', 'p058s0:c000'] · `air pollution global health cost pathways overview` → ['p061s0:c000', 'p061s0:c001', 'p058s0:c000']
**Final context IDs:** ['p061s0:c001']

**Agent abstained.** Model reason: The provided passage discusses air pollution in South Asia and does not mention a global health cost in the Pathways section.

---

## dev-q19 · answerable · status **abstain** (model_abstained)

**Question:** In the Priorities section of the overview, what share of the population in IDA countries is exposed to extreme weather hazards, and what share is at risk?  
**Filter:** `{'section': 'priorities'}`
**Expected answer:** Of the IDA-country population covered by the report's extreme-weather risk data, 56 percent are exposed and 47 percent are at risk, so 84 percent of those exposed are also at risk.
**Gold evidence (p67):** "For example, of the population in IDA countries covered by the data on risks from extreme weather events used for this report, 56 percent are exposed to extreme weather hazards and 47 percent are at risk. This means that 84 percent of those who are exposed are also at risk."
**Context evidence hit (automatic):** False

**Searches:** `share of population IDA countries extreme weather hazards at risk Priorities` → ['p067s0:c004', 'p066s0:c001', 'p067s0:c003'] · `IDA countries exposed extreme weather hazards Priorities overview` → ['p067s0:c004', 'p066s0:c001', 'p072s0:c002'] · `IDA countries extreme weather hazards Priorities overview percentage share population` → ['p067s0:c004', 'p066s0:c001', 'p067s0:c003']
**Final context IDs:** ['p066s0:c001']

**Agent abstained.** Model reason: The provided passages do not contain information about the share of the population in IDA countries exposed to or at risk from extreme weather hazards.

---

## dev-q20 · answerable · status **abstain** (model_abstained)

**Question:** If warming exceeds 2°C, how high could adaptation costs in Africa rise by the 2070s?
**Expected answer:** Up to $200 billion per year by the 2070s (current adaptation costs in Africa are estimated at $7-$15 billion per year).
**Gold evidence (p73):** "Current adaptation costs in Africa are estimated to be in the range of $7–$15 billion per year, with projections suggesting these could rise to $35 billion annually by the 2040s and up to $200 billion per year by the 2070s if warming exceeds 2°C."
**Context evidence hit (automatic):** False

**Searches:** `adaptation costs Africa 2°C 2070s` → ['p073s0:c002', 'p073s0:c001', 'p062s0:c004'] · `adaptation costs in Africa 2070s 2 degrees` → ['p073s0:c002', 'p073s0:c001', 'p062s0:c004'] · `adaptation costs Africa 2070s warming exceeds 2C` → ['p073s0:c002', 'p073s0:c001', 'p062s0:c004']
**Final context IDs:** ['p073s0:c001']

**Agent abstained.** Model reason: The provided passage does not contain information about adaptation costs in Africa by the 2070s if warming exceeds 2°C.

---

## dev-u1 · UNANSWERABLE · status **answered**

**Question:** What was Vietnam's extreme poverty rate in 2024?
**Why unanswerable:** Vietnam is not mentioned anywhere in the indexed Overview; poverty rates are given only globally, by region or by income group.

**Searches:** `Vietnam extreme poverty rate 2024` → ['p036s0:c000', 'p036s0:c002', 'p041s0:c000'] · `Vietnam extreme poverty rate 2024 poverty, Prosperity, and Planet Report` → ['p036s0:c000', 'p036s0:c002', 'p035s0:c003'] · `Vietnam poverty rate 2024 Poverty Prosperity and Planet Report` → ['p036s0:c000', 'p035s0:c002', 'p035s0:c003']
**Final context IDs:** ['p036s0:c000']

**Agent answer:** The provided passages do not specify Vietnam's extreme poverty rate in 2024; they only mention a general poverty rate falling to 8.5 percent in 2024 [B:wb-ppp-2024:p036s0:c000].

> Citation 1: `B:wb-ppp-2024:p036s0:c000` (page 36)  
> poverty rate fell from 38 percent in 1990 to 8.5 percent in 2024, it has stalled more recently amid lower economic growth and multiple shocks such as the COVID-19 pandemic, high inflation, and increased conflict and fragility. Extreme poverty today is only slightly below the rate observed before the pandemic in 2019 and in many poor settings, poverty rates remain higher than they were five years ago. Using the slightly higher poverty line of $3.65 a day per person (representative of the national poverty lines used in lower-middle-income countries), about 1.7 billion people are living in poverty in 2024 (21.4 percent, or about one-fifth, of the global population).

---

## dev-u2 · UNANSWERABLE · status **abstain** (model_abstained)

**Question:** How much funding did the IDA21 replenishment raise?
**Why unanswerable:** IDA countries are discussed at length, but the Overview never mentions IDA21 or any replenishment amount.

**Searches:** `IDA21 replenishment funding raised amount` → ['p072s0:c002', 'p067s0:c001', 'p066s0:c001'] · `IDA21 replenishment raised billion` → ['p067s0:c001', 'p072s0:c002', 'p066s0:c001'] · `IDA21 replenishment billion` → ['p067s0:c001', 'p072s0:c002', 'p066s0:c001']
**Final context IDs:** ['p067s0:c001']

**Agent abstained.** Model reason: The provided passages do not contain information about the funding raised by the IDA21 replenishment.

---

## dev-u3 · UNANSWERABLE · status **abstain** (model_abstained)

**Question:** What carbon price per ton of CO2 does the report recommend?
**Why unanswerable:** Page 58 discusses carbon pricing coverage (0.15 to 24 percent of emissions) and the global total carbon price trend, but gives no price level per ton and no recommended price.

**Searches:** `carbon price per ton of CO2 recommend` → ['p058s0:c000', 'p069s0:c002', 'p064s0:c000'] · `carbon price per ton` → ['p058s0:c000', 'p064s0:c000', 'p062s0:c004'] · `carbon price per ton recommendation` → ['p058s0:c000', 'p069s0:c002', 'p064s0:c000']
**Final context IDs:** ['p069s0:c002']

**Agent abstained.** Model reason: The provided passages do not mention a recommended carbon price per ton of CO2.

---
