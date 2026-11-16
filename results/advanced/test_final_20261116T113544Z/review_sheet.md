# Review sheet: `test_final_20261116T113544Z`

For each case compare the agent answer and every citation with the ORIGINAL PDF page (PDF page numbers, not printed page numbers), then fill `labels.csv`. Gold is shown for grading only.

## adv-test-01 · table · status **answered**

**Question:** According to Table 1.1, what are the monetary deprivation rate and the multidimensional poverty rate for South Asia?
**Expected:** Monetary deprivation 4 percent and multidimensional poverty rate 11.2 percent (circa 2021).
- gold p117 — TABLE 1.1, row 'South Asia', columns 'Monetary' and 'Multidimensional poverty rate': "South Asia 4 15 18 6 23 5 11.2 6 11"
**Gold pages in final context (automatic):** True

**Searches:** `Table 1.1 South Asia monetary deprivation rate multidimensional poverty rate` → ['p117v1', 'p116t2', 'p117t1', 'p118t1', 'p118v1', 'p119t1', 'p118t2', 'p119v1']

**Agent answer:** According to Table 1.1, the monetary deprivation rate for South Asia is 4 percent, and the multidimensional poverty rate is 11.2 percent [adv:p117v1].

> **Citation `adv:p117v1`** (PDF page 117, table, TABLE 1.1, bbox[ymin,xmin,ymax,xmax]/1000=[163, 105, 653, 908])  
> TABLE 1.1: Deprivations in educational attainment and access to basic infrastructure lift multidimensional poverty above the extreme poverty rate, 2021 (table on PDF page 117; model-generated description) | Region | Monetary | Educational attainment | Educational enrollment | Electricity | Sanitation | Drinking water | Multidimensional poverty rate | Number of economies | Coverage (%) | | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | | East Asia and Pacific | 2 | 5 | 2 | 1 | 9 | 4 | 2.7 | 12 | 26 | | Europe and Central Asia | 0 | 1 | 1 | 2 | 8 | 4 | 2.1 | 24 | 78 | | Latin America and the Caribbean | 3 | 8 | 2 | 1 | 17 | 3 | 3.6 | 18 | 86 | | Middle East and North Africa | 1 | 7 | 2 | 0 | 2 | 1 | 1.5 | 3 | 24 | | South Asia | 4 | 15 | 18 | 6 | 23 | 5 | 11.2 | 6 | 11 | | Sub-Saharan Africa | 39 | 29 | 18 | 46 | 59 | 29 | 52.6 | 24 | 31 | | Rest of the world | 0 | 1 | 2 | 0 | 0 | 0 | 1.0 | 23 | 69 | | World | 9 | 10 | 8 | 10 | 21 | 9 | 13.4 | 110 | 37 | | IDA countries | 25 | 23 | 17 | 29 | 44 | 19 | 35.6 | 38 | 34 | | Countries in FCS | 38 | 27 | 18 | 45 | 55 | 28 | 50.4 | 13 | 27 |  Source: World Bank, Global Monitoring Database (GMD) (version September 2024). Note: FCS = fragile and conflict-affected situations; IDA = International Development Association. The table presents the multidimensional poverty rate and share of population deprived in each indicator by region and rest of the world for circa 2021. “Multidimensional poverty rate” is the share o

---

## adv-test-02 · table · status **answered**

**Question:** Using Table 1D.1, by how many percentage points did the extreme poverty rate ($2.15 per day) in the Middle East and North Africa change between 2010 and 2024?
**Expected:** It rose by 4.8 percentage points, from 1.9 percent in 2010 to 6.7 percent in 2024.
- gold p128 — TABLE 1D.1, block '$2.15 per day', row 'Middle East and North Africa', columns 2010 and 2024: "Middle East and North Africa 6.4 4.7 3.0 2.7 1.9 3.7 4.6 5.3 5.9 6.1 6.4 6.7"
**Gold pages in final context (automatic):** True

**Searches:** `Table 1D.1 extreme poverty rate $2.15 Middle East and North Africa 2010 2024` → ['p129v1', 'p128v1', 'p096v1', 'p129v2', 'p114t1', 'p117t1', 'p129t2', 'p096t1']

**Agent answer:** According to Table 1D.1, the extreme poverty rate ($2.15 per day) in the Middle East and North Africa was 1.9 percent in 2010 and 6.7 percent in 2024 [adv:p128v1]. This represents an increase of 4.8 percentage points.

> **Citation `adv:p128v1`** (PDF page 128, table, TABLE 1D.1, bbox[ymin,xmin,ymax,xmax]/1000=[177, 82, 915, 831])  
> TABLE 1D.1: Percentage of population living in poverty by region (table on PDF page 128; model-generated description) | Region and poverty line | 1990 | 1995 | 2000 | 2005 | 2010 | 2015 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | | **$2.15 per day** | | | | | | | | | | | | | | East Asia and Pacific | 65.2 | 49.0 | 39.7 | 20.7 | 12.6 | 2.3 | 1.0 | 1.1 | 1.1 | 1.0 | 0.9 | 0.8 | | Europe and Central Asia | 3.6 | 8.1 | 9.2 | 4.7 | 1.2 | 0.8 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | | Latin America and the Caribbean | 16.3 | 14.0 | 13.8 | 10.7 | 5.9 | 4.1 | 4.2 | 3.8 | 4.5 | 3.5 | 3.4 | 3.3 | | Middle East and North Africa | 6.4 | 4.7 | 3.0 | 2.7 | 1.9 | 3.7 | 4.6 | 5.3 | 5.9 | 6.1 | 6.4 | 6.7 | | South Asia | 50.0 | 43.8 | -- | 35.5 | 25.4 | 16.6 | 10.6 | 13.0 | 11.4 | 9.7 | 8.7 | 7.6 | | Sub-Saharan Africa | 54.6 | 58.0 | 56.0 | 48.7 | 42.1 | 38.2 | 36.7 | 37.9 | 37.6 | 37.0 | 36.9 | 36.5 | | Eastern and Southern Africa | -- | 57.5 | 56.3 | 50.2 | 44.2 | 41.7 | 43.1 | 44.5 | 44.2 | 43.6 | 43.7 | 43.2 | | Western and Central Africa | 55.2 | 58.8 | -- | 46.5 | 39.1 | 33.0 | 27.3 | 28.3 | 27.9 | 27.3 | 27.0 | 26.5 | | Rest of the world | 0.4 | 0.5 | 0.5 | 0.5 | 0.5 | 0.7 | 0.6 | 0.4 | 0.3 | 0.6 | 0.6 | 0.6 | | World | 37.9 | 32.5 | 29.3 | 21.5 | 15.7 | 10.5 | 8.8 | 9.7 | 9.5 | 9.0 | 8.8 | 8.5 | | FCS | -- | 49.9 | -- | 38.1 | 31.7 | 29.5 | 29.2 | 30.7 | 30.9 | 30.8 | 31.1 | 30.9 | | IDA | 54.4 

---

## adv-test-03 · table · status **answered**

**Question:** In Table 2.1, which country has the lower Prosperity Gap, Peru or Colombia, and what are the two values and their mean incomes?
**Expected:** Peru: Prosperity Gap 3.60 with mean income 12.4, versus Colombia: 4.69 with mean income 17.3 (both 2022).
- gold p151 — TABLE 2.1, rows 'Prosperity Gap' and 'Mean income', columns 'Peru 2022' and 'Colombia 2022': "Prosperity Gap 7.20 8.32 3.60 4.69 / Mean income 5.02 5.37 12.4 17.3"
**Gold pages in final context (automatic):** True

**Searches:** `Table 2.1 Prosperity Gap Peru Colombia mean income` → ['p151v1', 'p151t2', 'p151t1', 'p045v1', 'p150t2', 'p150v1', 'p045t1', 'p171t1']

**Agent answer:** According to Table 2.1, Peru has the lower Prosperity Gap at 3.60 compared to Colombia's 4.69 [adv:p151v1]. The mean income for Peru is 12.4 (in 2017 PPP$ per person per day) and for Colombia is 17.3 (in 2017 PPP$ per person per day) [adv:p151v1].

> **Citation `adv:p151v1`** (PDF page 151, table, TABLE 2.1, bbox[ymin,xmin,ymax,xmax]/1000=[645, 168, 787, 832])  
> TABLE 2.1: An inequality penalty is built into the Prosperity Gap index (table on PDF page 151; model-generated description) | | Benin | Cameroon | Peru | Colombia | | :--- | :--- | :--- | :--- | :--- | | | 2021 | 2021 | 2022 | 2022 | | Prosperity Gap | 7.20 | 8.32 | 3.60 | 4.69 | | Mean income | 5.02 | 5.37 | 12.4 | 17.3 | | Inequality | 1.44 | 1.79 | 1.79 | 3.25 |  Source: World Bank, Poverty and Inequality Platform (version September 2024), https://pip.worldbank.org. Note: The Prosperity Gap is calculated using the global prosperity standard of $25 per person per day in 2017 purchasing power parity dollars (PPP$). The table also shows the decomposition of the Prosperity Gap into the product of (25/mean income) and inequality. Inequality is measured using the inequality measure related to the Prosperity Gap—the average income multiple needed to reach the mean income (see annex 2B for details). Mean income is expressed in 2017 PPP$ per person per day. Estimates for each country are reported using the most recent survey data.

---

## adv-test-04 · table · status **answered**

**Question:** According to Table 2D.1, how many economies and how many surveys are income-based versus consumption-based in the Poverty and Inequality Platform (post-2000)?
**Expected:** Income-based: 66 economies and 1,057 surveys; consumption-based: 100 economies and 570 surveys.
- gold p176 — TABLE 2D.1, rows 'Income-based surveys' and 'Consumption-based surveys', columns 'Economy count' and 'Survey count': "Income-based surveys 66 1,057 0.06 37.3 / Consumption-based surveys 100 570 0.71 36.2"
**Gold pages in final context (automatic):** True

**Searches:** `Table 2D.1 Poverty and Inequality Platform post-2000 income-based consumption-based` → ['p176v1', 'p176t1', 'p013t1', 'p175t1', 'p048v1', 'p176t2', 'p048t1', 'p177v1']

**Agent answer:** According to Table 2D.1, there are 66 economies with 1,057 surveys that are income-based, and 100 economies with 570 surveys that are consumption-based in the Poverty and Inequality Platform (post-2000) [adv:p176v1].

> **Citation `adv:p176v1`** (PDF page 176, table, TABLE 2D.1, bbox[ymin,xmin,ymax,xmax]/1000=[268, 166, 422, 833])  
> TABLE 2D.1: Statistics of Gini indexes in the Poverty and Inequality Platform, post-2000 (table on PDF page 176; model-generated description) | Economy count | Survey count | Share of LICs and LMICs | Average Gini | | :--- | :--- | :--- | :--- | | Income-based surveys | 66 | 1,057 | 0.06 | 37.3 | | Consumption-based surveys | 100 | 570 | 0.71 | 36.2 | | Total | 166 | 1,627 | 0.45 | 36.9 |  Source: World Bank, Poverty and Inequality Platform (version September 2024), https://pip.worldbank.org. Note: LICs = lower-income countries; LMICs = lower-middle-income countries.

---

## adv-test-05 · table · status **answered**

**Question:** According to Table 2E.1, what was the Prosperity Gap of East Asia and Pacific in 1990 and in 2024?
**Expected:** 16.5 in 1990 and 2.83 in 2024.
- gold p179 — TABLE 2E.1, row 'East Asia and Pacific', columns 1990 and 2024: "East Asia and Pacific 16.5 13.0 11.5 8.06 6.26 4.06 3.25 3.28 3.04 3.00 2.92 2.83"
**Gold pages in final context (automatic):** True

**Searches:** `Table 2E.1 Prosperity Gap East Asia and Pacific 1990 2024` → ['p179v1', 'p147v1', 'p147t1', 'p148t2', 'p149v1', 'p149t1', 'p179t1', 'p013t1']

**Agent answer:** According to Table 2E.1, the Prosperity Gap for East Asia and Pacific was 16.5 in 1990 and 2.83 in 2024 [adv:p179t1].

> **Citation `adv:p179t1`** (PDF page 179, text)  
> 145 shared Pros Perity While there are some differences when thresholds are defined for income-only and consumption-only surveys, this gap has narrowed over time. In the 1990s, the 67th percentile of consumption (income) Ginis corresponded to values of 44.1 (49.1). In comparison, using data from the latest available surveys of all economies, the 67th percentile corresponds to 39.3 (40.3). 31 Trends in the number of economies with high inequality reported in this chapter are robust to the range of thresholds reported here and those shown in figure 2.10 in the main text. With all these results in mind, the same threshold was chosen across income and consumption surveys, which is simpler to communicate and follows the practice of United Nations agencies. Annex 2E . Prosperity Gap estimates by region TABLE 2E.1 Prosperity Gap estimates, by region Region 1990 1995 2000 2005 2010 2015 2019 2020 2021 2022 2023 2024 East Asia and Pacific 16.5 13.0 11.5 8.06 6.26 4.06 3.25 3.28 3.04 3.00 2.92 2.83 Europe and Central Asia 3.83 5.18 5.54 3.83 2.63 2.36 2.06 2.01 1.81 1.74 1.70 1.67 Latin America and the Caribbean 8.01 7.52 7.64 6.15 4.40 3.60 3.57 3.61 3.67 3.36 3.28 3.25 Middle East and North Africa 5.40 5.25 4.59 4.35 4.00 4.16 4.38 4.62 4.67 4.61 4.65 4.69 South Asia 12.7 11.7 -- 10.4 9.19 8.05 6.88 7.22 6.97 6.64 6.43 6.21 Sub-Saharan Africa 17.9 19.2 18.5 15.8 13.3 12.4 12.3 12.7 12.6 12.4 12.3 12.2 Eastern and Southern Africa 17.0 18.7 19.0 17.0 14.4 13.5 -- 14.7 14.5 14.3 14.2 14

---

## adv-test-06 · table · status **answered**

**Question:** What intensity threshold does Table 3B.1 set for tropical cyclones?
**Expected:** A 10-minute average sustained wind speed above 37.6 m/s, or equivalent to Category 2 or higher on the Saffir-Simpson scale.
- gold p237 — TABLE 3B.1, row 'Tropical cyclone': "Tropical cyclone > 37.6-m/s 10-minute average sustained wind speed or equivalent ≥ Category 2 on the Saffir-Simpson scale"
**Gold pages in final context (automatic):** True

**Searches:** `Table 3B.1 tropical cyclones intensity threshold` → ['p237v1', 'p237t2', 'p237t1', 'p199t2', 'p238t1', 'p284t2', 'p276t2', 'p277t1']

**Agent answer:** Table 3B.1 sets the intensity threshold for tropical cyclones as a 10-minute average sustained wind speed greater than 37.6 meters per second, or an equivalent of Category 2 or higher on the Saffir-Simpson scale [adv:p237v1].

> **Citation `adv:p237v1`** (PDF page 237, table, TABLE 3B.1, bbox[ymin,xmin,ymax,xmax]/1000=[586, 168, 755, 832])  
> TABLE 3B.1: Hazard thresholds (table on PDF page 237; model-generated description) | Hazard | Intensity threshold | | :--- | :--- | | Agricultural drought | > 30% cropland or grassland affected by severe drought | | Flood | > 50-cm maximum inundation depth | | Heat wave | > 33°C maximum 5-day average of daily maximum WBGT | | Tropical cyclone | > 37.6-m/s 10-minute average sustained wind speed or equivalent ≥ Category 2 on the Saffir-Simpson scale |  Source: World Bank Group Scorecard indicator: the percentage of people at high risk of climate-related hazards globally, https://scorecard.worldbank.org/en/scorecard/home. Note: C = Celsius; cm = centimeter; m/s = meters per second; WBGT = wet bulb globe temperature.

---

## adv-test-07 · diagram · status **answered**

**Question:** In Figure 2.16, what action is paired with 'inequality in utilizing productive capacity'?
**Expected:** Reduce market and institutional distortions that restrict access to markets and earning opportunities.
- gold p170 — FIGURE 2.16 (diagram), middle box: "Inequality in utilizing productive capacity / Reduce market and institutional distortions that restrict access to markets and earning opportunities."
**Gold pages in final context (automatic):** True

**Searches:** `Figure 2.16 "inequality in utilizing productive capacity"` → ['p170v1', 'p170t1', 'p166t2', 'p104t3', 'p104t2', 'p054t1', 'p228t2', 'p083t2']

**Agent answer:** In Figure 2.16, the action paired with "inequality in utilizing productive capacity" is to "reduce market and institutional distortions that restrict access to markets and earning opportunities" [adv:p170v1, adv:p170t1].

> **Citation `adv:p170v1`** (PDF page 170, diagram, FIGURE 2.16, bbox[ymin,xmin,ymax,xmax]/1000=[81, 168, 437, 832])  
> FIGURE 2.16: Effectively addressing inequality requires a comprehensive approach that tackles all phases of inequality (diagram on PDF page 170; model-generated description) A conceptual framework diagram consisting of three vertical columns overlaid by an overarching horizontal arrow banner at the bottom:  1. Column 1 (Icon: Group of four people):    - Heading: "Inequality in building productive capacity"    - Description: "Invest in early life opportunities and human capital formation."  2. Column 2 (Icon: Person wearing a hard hat):    - Heading: "Inequality in utilizing productive capacity"    - Description: "Reduce market and institutional distortions that restrict access to markets and earning opportunities."  3. Column 3 (Icon: Money bag with percentage symbol):    - Heading: "Inequality in taxes and transfers"    - Description: "Enhance fiscal redistribution that delivers long-term inclusive growth."  Overarching Banner at Bottom (Double-ended horizontal arrow across all three columns):    - Text: "Improve the productive capacity of the poor"  Source: World Bank.

> **Citation `adv:p170t1`** (PDF page 170, text)  
> 136 POVERTY , PROSPERITY , AND PLANET REPORT 2024 FIGURE 2.16 Effectively addressing inequality requires a comprehensive approach that tackles all phases of inequality Inequality in building productive capacity Invest in early life opportunities and human capital formation. Inequality in utilizing productive capacity Reduce market and institutional distortions that restrict access to markets and earning opportunities. Inequality in taxes and transfers Enhance fiscal redistribution that delivers long-term inclusive growth. Improve the productive capacity of the poor Source: world bank. Annex 2A . Comparing the growth in the mean of the bottom 40 percent versus the Global Prosperity Gap and the Gini index Figure 2A.1, panel a, compares the growth in the Prosperity Gap with the growth in the mean of the bottom 40 percent of the distribution (bottom 40). It is expected that the two measures would be negatively correlated, since a greater improvement in the income of the poor (higher bottom 40 growth) is associated with a faster decline in the Prosperity Gap. The takeaway is that the changes in the bottom 40 closely align with the changes in the Prosperity Gap, and they overwhelmingly move in the same direction. In some cases, the bottom 40 change is greater (for example, for Romania), while in other cases the Prosperity Gap change is greater (such as for the Slovak Republic). This can be explained by the sensitivity of the measures to changes at different parts of the distributio

---

## adv-test-08 · diagram · status **answered**

**Question:** According to the diagram in Figure 3.2, which three components determine risk?
**Expected:** Hazard, exposure, and vulnerability.
- gold p199 — FIGURE 3.2 (diagram), the three elements around 'Risk (Impacts)': "Risk (Impacts) / Vulnerability / Hazard Exposure"
**Gold pages in final context (automatic):** True

**Searches:** `Figure 3.2 components determine risk` → ['p199v1', 'p006t2', 'p068t2', 'p068v1', 'p274t1', 'p052v1', 'p027t1', 'p204t1']

**Agent answer:** According to the diagram in Figure 3.2, the three components that determine risk are vulnerability, hazard, and exposure [adv:p199v1].

> **Citation `adv:p199v1`** (PDF page 199, diagram, FIGURE 3.2, bbox[ymin,xmin,ymax,xmax]/1000=[83, 169, 431, 818])  
> FIGURE 3.2: Risks depend on hazard, exposure, and vulnerability (diagram on PDF page 199; model-generated description) A Venn diagram showing the intersection of three components that determine Risk (Impacts):  1. **Vulnerability** (top blue circle):    - Text description: "The propensity or predisposition to be adversely affected. Vulnerability encompasses a variety of concepts and elements, including sensitivity or susceptibility to harm and lack of capacity to cope and adapt."  2. **Hazard** (bottom-left yellow circle):    - Text description: "The potential occurrence of a natural or human-induced physical event or trend that may cause loss of life, injury, or other health impacts, as well as damage and loss to property, infrastructure, livelihoods, service provision, ecosystems, and environmental resources."  3. **Exposure** (bottom-right red circle):    - Text description: "The presence of people; livelihoods; species or ecosystems; environmental functions, services, and resources; infrastructure; or economic, social, or cultural assets in places and settings that could be adversely affected."  4. **Risk (Impacts)**:    - Positioned at the central intersection of Vulnerability, Hazard, and Exposure.  Source: IPCC 2023a.

---

## adv-test-09 · diagram · status **answered**

**Question:** In Figure B3.1.1, which conditions are grouped under being 'unable to cope'?
**Expected:** Low income, no access to social protection, no access to a financial instrument, and low education level.
- gold p201 — FIGURE B3.1.1 (diagram), box 'Unable to cope' (any 1): "Low income / No access to social protection / No access to financial instrument / Low education level"
**Gold pages in final context (automatic):** True

**Searches:** `Figure B3.1.1 "unable to cope"` → ['p201v1', 'p236t2', 'p200t2', 'p236t1', 'p201t1', 'p052t2', 'p052v1', 'p051t2']

**Agent answer:** In Figure B3.1.1, the conditions grouped under being 'unable to cope' are low income, no access to social protection, no access to financial instrument, and low education level [adv:p052v1].

> **Citation `adv:p052v1`** (PDF page 52, diagram, FIGURE BO.3.1, bbox[ymin,xmin,ymax,xmax]/1000=[542, 168, 915, 832])  
> FIGURE BO.3.1: Measuring the vulnerability of people at high risk from climate-related hazards (diagram on PDF page 52; model-generated description) Flowchart diagram defining when a "Person is at risk from climate hazards if...":  - Risk requires: "Exposed to climate hazards" AND "Vulnerable to experiencing losses"  1. Exposed to climate hazards (requires Any 1):    - Flood    - Drought    - Extreme heat    - Cyclone  2. Vulnerable to experiencing losses:    - Physically vulnerable (requires Any 1):      - No access to water      - No access to electricity      - Low access to services and markets    - Unable to cope (requires Any 1):      - Low income      - No access to social protection      - No access to financial instrument      - Low education level  Source: World Bank Group Scorecard indicator: the percentage of people at high risk of climate-related hazards globally, https://scorecard.worldbank.org/en/scorecard/home.

---

## adv-test-10 · diagram · status **answered**

**Question:** On Map 3.1, what do the gray, blue and red circles represent?
**Expected:** Gray circles: the overall sample population; blue circles: the population exposed to any type of hazard; red circles: the population exposed and vulnerable.
- gold p203 — MAP 3.1, legend and note: "Gray circles depict the overall population in the sample in the data, blue circles show the population exposed to any type of hazard, and red circles indicate the population exposed to any type of hazard and"
**Gold pages in final context (automatic):** True

**Searches:** `Map 3.1 gray blue red circles` → ['p203v1', 'p051v1', 'p051t1', 'p203t2', 'p048v1', 'p157v1', 'p058v1', 'p087v1']

**Agent answer:** On Map 3.1, the gray circles represent the sample population, the blue circles represent the population exposed to any type of hazard, and the red circles represent the population exposed to any type of hazard and vulnerable along at least one dimension [adv:p203v1].

> **Citation `adv:p203v1`** (PDF page 203, map, MAP 3.1, bbox[ymin,xmin,ymax,xmax]/1000=[347, 168, 818, 825])  
> MAP 3.1: Large populations are exposed to extreme weather events in South Asia and East Asia and Pacific, and vulnerability is high in Sub-Saharan Africa (map on PDF page 203; model-generated description) ### Map Details - **Legend Categories**:   - Gray circle: Sample population   - Blue circle: Population exposed   - Red circle: Population exposed and vulnerable - **Labelled Regions**:   - North America   - Latin America and the Caribbean   - Europe and Central Asia   - Middle East and North Africa   - Sub-Saharan Africa   - South Asia   - East Asia and Pacific - **Map Identifier**: IBRD 48304 | AUGUST 2024  **Source**: World Bank Group Scorecard indicator: the percentage of people at high risk of climate-related hazards globally, https://scorecard.worldbank.org/en/scorecard/home.  **Note**: Gray circles depict the overall population in the sample in the data, blue circles show the population exposed to any type of hazard, and red circles indicate the population exposed to any type of hazard and vulnerable along at least one dimension. The placement of circles is for illustrative purposes only and reflects populations for the respective region as a whole. The blue circle for Sub-Saharan Africa is barely visible because almost everyone in Sub-Saharan Africa who is exposed is also vulnerable. For the Middle East and North Africa region, the indicator covers less than 50 percent of the population.

---

## adv-test-11 · diagram · status **answered**

**Question:** Which Gini index ranges define the high, moderate and low inequality categories in the legend of Map 2.1?
**Expected:** High inequality: Gini above 40; moderate: between 30 and 40; low: below 30 (plus a 'no data' category).
- gold p157 — MAP 2.1, legend: "High inequality (>40) / Moderate inequality (30–40) / Low inequality (<30) / No data"
**Gold pages in final context (automatic):** True

**Searches:** `Map 2.1 Gini index ranges legend` → ['p157v1', 'p048v1', 'p157t1', 'p048t1', 'p156t1', 'p046t2', 'p162v1', 'p267v1']

**Agent answer:** In the legend of Map 2.1, the Gini index ranges are defined as follows: high inequality is greater than 40 (>40), moderate inequality is between 30 and 40 (30–40), and low inequality is less than 30 (<30) [adv:p157v1, adv:p157t1].

> **Citation `adv:p157t1`** (PDF page 157, text)  
> 123 shared Pros Perity numbers of economies with relatively low inequality. Only Türkiye exhibits higher levels of inequality than the rest of the region. High inequality is more prevalent in low- and middle-income countries as well as countries in fragile and conflict-affected situations (FCS) (figure 2.8). The high-income economies with elevated levels of inequality are Chile, Panama, the United States, and Uruguay (table 2F .1). In contrast, around two-fifths of middle-income countries and one-third of low-income countries exhibit high levels of inequality. Although data are limited, two-fifths of FCS countries have high levels of inequality, compared to only a quarter of non-FCS countries in the sample. Of the 68 International Development Association (IDA) countries with data, less than 15 percent were in the low-inequality group and more than double that (37 percent) were in the high-inequality group.14 MAP 2.1 The 49 economies with high inequality are concentrated in Sub-Saharan Africa and Latin America and the Caribbean High inequality (>40) Moderate inequality (30–40) Low inequality (<30) No data IBRD 48303  | AUGUST 2024 Sources: world bank, Poverty and inequality Platform (version september 2024 ), https://pip.worldbank.org; haddad et al. 2024. Note: the map presents the Gini index from the latest available survey (after 2000), which measures the inequality of income or consumption, depending on the economy. high-inequality economies have a Gini index above 40, mode

> **Citation `adv:p157v1`** (PDF page 157, map, MAP 2.1, bbox[ymin,xmin,ymax,xmax]/1000=[338, 168, 803, 831])  
> MAP 2.1: The 49 economies with high inequality are concentrated in Sub-Saharan Africa and Latin America and the Caribbean (map on PDF page 157; model-generated description) Map Type: World map showing geographic distribution of Gini index levels.  Legend Categories: - High inequality (>40) [Red] - Moderate inequality (30–40) [Orange/Yellow] - Low inequality (<30) [Cyan/Blue] - No data [Grey]  Map Metadata: IBRD 48303 | AUGUST 2024  Key Patterns: - High inequality (>40) is concentrated in Sub-Saharan Africa and Latin America and the Caribbean. - Low inequality (<30) is prominent across Europe, parts of Central/East Asia, and North Africa. - Moderate inequality (30–40) covers countries in North America, South Asia, East Asia, and Australia.  Sources: World Bank, Poverty and Inequality Platform (version September 2024), https://pip.worldbank.org; Haddad et al. 2024.  Note: The map presents the Gini index from the latest available survey (after 2000), which measures the inequality of income or consumption, depending on the economy. High-inequality economies have a Gini index above 40, moderate-inequality economies are those with a Gini index between 30 and 40, and low-inequality economies are those with a Gini index below 30. See annex table 2F.1 for the economy classifications, Gini indexes, year of survey, and the type of welfare—income, or consumption—used.

---

## adv-test-12 · chart · status **answered**

**Question:** According to Figure 2.9 panel a, how many economies had high inequality in 2000 and in 2022?
**Expected:** 74 economies in 2000 and 49 in 2022.
- gold p159 — FIGURE 2.9 panel a, 'High inequality' series, data labels for 2000 and 2022: "74 73 73 74 75 72 72 69 70 67 68 67 66 61 62 61 59 59 54 53 51 49 49"
**Gold pages in final context (automatic):** True

**Searches:** `Figure 2.9 panel a high inequality 2000 2022` → ['p159v1', 'p158t1', 'p158v1', 'p058v1', 'p216t1', 'p048v2', 'p159t1', 'p026v2']

**Agent answer:** According to Figure 2.9, panel a, there were 74 economies with high inequality in 2000 and 49 economies with high inequality in 2022 [adv:p159v1].

> **Citation `adv:p159v1`** (PDF page 159, chart, FIGURE 2.9, bbox[ymin,xmin,ymax,xmax]/1000=[85, 165, 715, 835])  
> FIGURE 2.9: There is a steady decline in the number of economies with high inequality since 2000 (chart on PDF page 159; model-generated description) {'chart_type': 'stacked bar chart and bar chart', 'panels': [{'panel_title': 'a. Count of high-inequality economies, 2000–22', 'x_axis': 'Years (2000-2022)', 'y_axis': 'Number of economies', 'legend': ['Low inequality', 'Moderate inequality', 'High inequality'], 'data': {'2000': {'Low': 20, 'Moderate': 72, 'High': 74}, '2001': {'Low': 20, 'Moderate': 73, 'High': 73}, '2002': {'Low': 21, 'Moderate': 72, 'High': 73}, '2003': {'Low': 25, 'Moderate': 67, 'High': 74}, '2004': {'Low': 18, 'Moderate': 73, 'High': 75}, '2005': {'Low': 19, 'Moderate': 75, 'High': 72}, '2006': {'Low': 19, 'Moderate': 75, 'High': 72}, '2007': {'Low': 20, 'Moderate': 77, 'High': 69}, '2008': {'Low': 22, 'Moderate': 74, 'High': 70}, '2009': {'Low': 23, 'Moderate': 76, 'High': 67}, '2010': {'Low': 22, 'Moderate': 76, 'High': 68}, '2011': {'Low': 24, 'Moderate': 75, 'High': 67}, '2012': {'Low': 25, 'Moderate': 75, 'High': 66}, '2013': {'Low': 24, 'Moderate': 81, 'High': 61}, '2014': {'Low': 23, 'Moderate': 81, 'High': 62}, '2015': {'Low': 21, 'Moderate': 84, 'High': 61}, '2016': {'Low': 21, 'Moderate': 86, 'High': 59}, '2017': {'Low': 23, 'Moderate': 84, 'High': 59}, '2018': {'Low': 26, 'Moderate': 86, 'High': 54}, '2019': {'Low': 28, 'Moderate': 85, 'High': 53}, '2020': {'Low': 32, 'Moderate': 83, 'High': 51}, '2021': {'Low': 31, 'Moderate': 86, 'High': 49}, 

---

## adv-test-13 · chart · status **answered**

**Question:** According to Figure 3.3 panel a (World), what share of the world population is exposed to any extreme weather hazard, and which single hazard has the highest exposure share?
**Expected:** About 58 percent (0.58) are exposed to any hazard; heat has the highest single-hazard share at about 42 percent (0.42).
- gold p202 — FIGURE 3.3, panel a 'World', bars Any/Flood/Drought/Heat/Cyclone (printed data labels): "0.58 / 0.10 0.18 / 0.42 / 0.07"
**Gold pages in final context (automatic):** True

**Searches:** `Figure 3.3 panel a (World) extreme weather hazard exposure share` → ['p202v1', 'p011t2', 'p206t1', 'p199t2', 'p199t1', 'p214t2', 'p052t1', 'p205t2']

**Agent answer:** According to Figure 3.3, panel a, 0.58 (or 58 percent) of the world population is exposed to any extreme weather hazard [adv:p202v1]. Among the individual hazards listed, heat has the highest exposure share at 0.42 (or 42 percent) [adv:p202v1].

> **Citation `adv:p202v1`** (PDF page 202, chart, FIGURE 3.3, bbox[ymin,xmin,ymax,xmax]/1000=[85, 165, 825, 835])  
> FIGURE 3.3: South Asia and lower-middle-income countries have the highest exposure rates to extreme weather hazards (chart on PDF page 202; model-generated description) The figure consists of 12 bar charts (a-l) showing the 'Share of population exposed (%)' to five categories of extreme weather hazards: Any, Flood, Drought, Heat, and Cyclone. Data labels for each category are provided. a. World: Any 0.58, Flood 0.10, Drought 0.18, Heat 0.42, Cyclone 0.07. b. East Asia and Pacific: Any 0.68, Flood 0.14, Drought 0.14, Heat 0.53, Cyclone 0.14. c. Europe and Central Asia: Any 0.27, Flood 0.07, Drought 0.21, Heat 0.00, Cyclone 0.00. d. Latin America and the Caribbean: Any 0.31, Flood 0.06, Drought 0.15, Heat 0.10, Cyclone 0.04. e. Middle East and North Africa: Any 0.29, Flood 0.16, Drought 0.07, Heat 0.09, Cyclone 0.00. f. North America: Any 0.31, Flood 0.04, Drought 0.16, Heat 0.09, Cyclone 0.08. g. South Asia: Any 0.88, Flood 0.12, Drought 0.17, Heat 0.83, Cyclone 0.07. h. Sub-Saharan Africa: Any 0.39, Flood 0.04, Drought 0.29, Heat 0.12, Cyclone 0.00. i. Low-income: Any 0.41, Flood 0.04, Drought 0.30, Heat 0.14, Cyclone 0.00. j. Lower-middle-income: Any 0.73, Flood 0.11, Drought 0.18, Heat 0.62, Cyclone 0.08. k. Upper-middle-income: Any 0.55, Flood 0.11, Drought 0.15, Heat 0.39, Cyclone 0.07. l. High-income: Any 0.32, Flood 0.06, Drought 0.18, Heat 0.05, Cyclone 0.08. Source: World Bank Group Scorecard indicator: the percentage of people at high risk of climate-related hazards 

---

## adv-test-14 · chart · status **answered**

**Question:** In Figure 1.14, which deprivation dimension shows the highest rate for Sub-Saharan Africa, and approximately what is that rate?
**Expected:** Sanitation, at about 59 percent (roughly 60 percent).
- gold p118 — FIGURE 1.14, 'Sanitation' group, Sub-Saharan Africa bar: "using the same data as in table 1.1"
- gold p117 — TABLE 1.1, row 'Sub-Saharan Africa' (same data; either page is sufficient): "Sub-Saharan Africa 39 29 18 46 59 29 52.6 24 31"
**Gold pages in final context (automatic):** True

**Searches:** `Figure 1.14 Sub-Saharan Africa deprivation dimension rate` → ['p118v1', 'p118t1', 'p068v1', 'p118t2', 'p116t2', 'p068t1', 'p093t1', 'p117t1']

**Agent answer:** In Figure 1.14, the deprivation dimension with the highest rate for Sub-Saharan Africa is sanitation, which has a deprivation rate of approximately 60 percent [adv:p118v1].

> **Citation `adv:p118v1`** (PDF page 118, chart, FIGURE 1.14, bbox[ymin,xmin,ymax,xmax]/1000=[241, 168, 523, 832])  
> FIGURE 1.14: The poorest countries lag behind in many dimensions of multidimensional poverty in 2021 (chart on PDF page 118; model-generated description) {'chart_type': 'grouped bar chart', 'y_axis_title': 'Deprivation rate (%)', 'x_axis_categories': ['Monetary', 'Educational attainment', 'Educational enrollment', 'Electricity', 'Sanitation', 'Drinking water'], 'legend': ['IDA*', 'FCS*', 'Sub-Saharan Africa*', 'World*'], 'data_points': {'Monetary': {'IDA*': 'approx. 25', 'FCS*': 'approx. 38', 'Sub-Saharan Africa*': 'approx. 39', 'World*': 'approx. 9'}, 'Educational attainment': {'IDA*': 'approx. 23', 'FCS*': 'approx. 27', 'Sub-Saharan Africa*': 'approx. 32', 'World*': 'approx. 11'}, 'Educational enrollment': {'IDA*': 'approx. 18', 'FCS*': 'approx. 19', 'Sub-Saharan Africa*': 'approx. 20', 'World*': 'approx. 9'}, 'Electricity': {'IDA*': 'approx. 29', 'FCS*': 'approx. 45', 'Sub-Saharan Africa*': 'approx. 46', 'World*': 'approx. 12'}, 'Sanitation': {'IDA*': 'approx. 44', 'FCS*': 'approx. 55', 'Sub-Saharan Africa*': 'approx. 60', 'World*': 'approx. 21'}, 'Drinking water': {'IDA*': 'approx. 18', 'FCS*': 'approx. 27', 'Sub-Saharan Africa*': 'approx. 28', 'World*': 'approx. 9'}}, 'source': 'World Bank, Global Monitoring Database (GMD) (version September 2024).', 'note': 'FCS = fragile and conflict-affected situations; IDA = International Development Association. The figure presents the multidimensional poverty rate and share of population deprived for selected groupings and the worl

---

## adv-test-15 · chart · status **answered**

**Question:** Which countries are labelled by name in the scatter plot of Figure 2.15 (market versus disposable income Gini index)?
**Expected:** Korea, Rep.; Germany; Ireland; South Africa; and The Gambia.
- gold p167 — FIGURE 2.15, point labels: "Korea, Rep. / Germany / Ireland / South Africa / Gambia, The"
**Gold pages in final context (automatic):** True

**Searches:** `Figure 2.15 market versus disposable income Gini index` → ['p167v1', 'p167t1', 'p189t2', 'p188t3', 'p171t1', 'p271v1', 'p170t1', 'p271t1']

**Agent answer:** The countries labeled by name in the scatter plot of Figure 2.15 are South Africa, Ireland, Germany, Korea, Rep., and The Gambia [adv:p167v1, adv:p167t1].

> **Citation `adv:p167v1`** (PDF page 167, chart, FIGURE 2.15, bbox[ymin,xmin,ymax,xmax]/1000=[312, 255, 805, 750])  
> FIGURE 2.15: Market versus disposable income (chart on PDF page 167; model-generated description) The chart is a scatter plot showing the relationship between Market income Gini index (x-axis, range 10-80) and Disposable income Gini index (y-axis, range 10-80). A 45-degree line represents the point where market income inequality equals disposable income inequality. Points below the line indicate redistribution. Legend categories: Low-income (red), Lower-middle-income (orange), Upper-middle-income (light blue), High-income (dark blue). Specific countries labeled: South Africa (upper-middle-income, near 60/60), Ireland (high-income, approx. 47/29), Germany (high-income, approx. 42/22), Korea, Rep. (high-income, approx. 33/33), Gambia, The (low-income, approx. 36/36). An arrow labeled 'More redistribution' points downward away from the 45-degree line. Sources: Adapted from Wai-Poi, Sosa, and Bachas (forthcoming) and Lustig 2023. Note: The data are from the Commitment to Equity (CEQ) Institute, the Organisation for Economic Co-operation and Development (OECD), and World Bank databases, which collectively cover 96 economies over the past decade across all income groups and regions. The analysis includes the latest data point available for each country from the CEQ database and the OECD, which might differ from the latest year in the Poverty and Inequality Platform that has been used in the rest of the report. See also annex 2D and chapter 4 for discussion of the differences in ine

> **Citation `adv:p167t1`** (PDF page 167, text)  
> 133 shared Pros Perity High-income countries deliver more fiscal redistribution while exhibiting less inequality initially because they are more effective at targeting resources and have more fiscal space Figure 2.15 plots the Gini index of disposable income against the Gini index of market income.19 Although we refer to income throughout this section, countries that use consumption as their main measure are also included.20 In all countries with available estimates, inequality is reduced after direct taxes and transfers are accounted for.21 However, how much countries redistribute varies greatly, which is indicated by the distance from the 45-degree line. At one extreme, Ireland has reduced the Gini index by 17 points (from 46.6 to 29.4 in 2018), whereas The Gambia has reduced it by 0.2 points (from 36.1 to 35.9 in 2015/16).22 FIGURE 2.15 Market versus disposable income 10 20 30 40 50 60 70 80 10 20 30 40 50 60 70 80 Disposable income Gini index Market income Gini index Korea, Rep. Germany Ireland South Africa Gambia, The More redistribution Low-income Lower-middle-income Upper-middle-income High-income 45° line Sources: adapted from wai-Poi, sosa, and bachas (forthcoming) and lustig 202 3. Note: the data are from the Commitment to equity (CeQ) institute, the organisation for economic Co-operation and development (oeCd), and world bank databases, which collectively cover 96 economies over the past decade across all income groups and regions. the analysis includes the latest 

---

## adv-test-16 · chart · status **answered**

**Question:** In Figure 3.14, which priority is annotated for the countries with the highest GDP per capita and emissions, and which countries are labelled in that part of the chart?
**Expected:** 'Prioritize mitigation while managing transition costs'; the labelled high-income/high-emission countries include Japan, Germany, the United States and Saudi Arabia (China is labelled nearby).
- gold p228 — FIGURE 3.14, right-hand annotation and labelled bubbles: "China Japan Germany / United States / Saudi Arabia ... Prioritize mitigation while managing transition costs"
**Gold pages in final context (automatic):** True

**Searches:** `Figure 3.14 priority countries GDP per capita emissions` → ['p228v1', 'p228t1', 'p029v1', 'p227t1', 'p278t1', 'p225t1', 'p029t2', 'p065v1']

**Agent answer:** In Figure 3.14, the priority annotated for countries with the highest GDP per capita and emissions is "Prioritize mitigation while managing transition costs" [adv:p228v1, adv:p228t1]. The countries labeled in that part of the chart include Japan, Germany, the United States, and Saudi Arabia [adv:p228v1, adv:p228t1].

> **Citation `adv:p228v1`** (PDF page 228, chart, FIGURE 3.14, bbox[ymin,xmin,ymax,xmax]/1000=[87, 155, 515, 845])  
> FIGURE 3.14: Priorities to advance on the interlinked goals (chart on PDF page 228; model-generated description) The chart is a scatter plot showing Emissions per capita (t CO2e) on the y-axis (range -5 to 25) versus GDP per capita (2015 US$) on the x-axis (logarithmic scale, 100 to 100,000). The legend categories are: Low-income (red), Lower-middle-income (yellow), Upper-middle-income (light blue), and High-income (dark blue). The size of the bubbles represents total GHG emissions. Labeled countries include: Burundi, Congo, Dem. Rep., Madagascar, Chad, India, Indonesia, Brazil, China, Japan, Germany, United States, and Saudi Arabia. The chart is divided into three strategic zones: 1) 'Prioritize poverty eradication by fostering investment in human, physical, and financial capital' (bottom-left area), 2) 'Prioritize income growth that reduces vulnerability and pursue synergies (such as, cutting air pollution)' (middle area), and 3) 'Prioritize mitigation while managing transition costs' (top-right area). Source: Emissions Database for Global Atmospheric Research, Grassi et al. 2023, and World Development Indicators. Note: GDP = gross domestic product; GHG = greenhouse gas; t CO2e = tons of carbon dioxide equivalent. The sizes of the bubbles indicate total GHG emissions. Negative emissions occur when ecosystems absorb more carbon than the country emits. A few small countries with very high per capita emissions (Bahrain, Guyana, Iceland, Kuwait, Oman, Palau, Qatar, Trinidad and

> **Citation `adv:p228t1`** (PDF page 228, text)  
> 194 POVERTY , PROSPERITY , AND PLANET REPORT 2024 FIGURE 3.14 Priorities to advance on the interlinked goals –5 5 15 25 100 10,000 100,000 Emissions per capita (t CO2e) GDP per capita (2015 US$) Low-income Lower-middle-income Upper-middle-income High-income 1,000 0 Burundi Congo, Dem. Rep. Madagascar Chad India BrazilIndonesia China Japan Germany United States Saudi ArabiaPrioritize poverty eradication by fostering investment in human, physical, and ﬁnancial capital Prioritize income growth that reduces vulnerability and pursue synergies  (such as, cutting air pollution) Prioritize mitigation while managing transition costs Source: Emissions Database for Global Atmospheric Research, Grassi et al. 2023, and World Development Indicators, https://databank .worldbank.org/source/world-development-indicators. Note: GDP = gross domestic product; GHG = greenhouse gas; t CO2e = tons of carbon dioxide equivalent. The sizes of the bubbles indicate total GHG emissions. Negative emissions occur when ecosystems absorb more carbon than the country emits. A few small countries with very high per capita emissions (Bahrain, Guyana, Iceland, Kuwait, Oman, Palau, Qatar, Trinidad and Tobago, and the United Arab Emirates) and countries with very low per capita emissions (the Central African Republic and Vanuatu) are omitted for visual purposes. The horizontal axis uses a logarithmic scale. Low-income settings: Prioritize poverty reduction by fostering investments in human, physical, and financial 

---

## adv-test-17 · multi-hop · status **answered**

**Question:** What is Colombia's Prosperity Gap in Table 2.1, and what is its Gini index in the latest available survey listed in Table 2F.1?
**Expected:** Prosperity Gap 4.69 (2022) and Gini index 54.8 (2022 survey, income-based).
- gold p151 — TABLE 2.1, row 'Prosperity Gap', column 'Colombia 2022': "Prosperity Gap 7.20 8.32 3.60 4.69"
- gold p181 — TABLE 2F.1, row 'Colombia': "Colombia Latin America and the Caribbean 2022 income 54.8"
**Gold pages in final context (automatic):** True

**Searches:** `Colombia Prosperity Gap Table 2.1` → ['p151v1', 'p151t2', 'p151t1', 'p147t1', 'p147v1', 'p042v1', 'p145t1', 'p145v1'] · `Table 2F.1 Gini index Colombia` → ['p181v1', 'p186v1', 'p184v1', 'p185v1', 'p183t2', 'p182t2', 'p048v1', 'p157t1']

**Agent answer:** In Table 2.1, Colombia's Prosperity Gap is 4.69 [adv:p151v1]. According to Table 2F.1, Colombia's Gini index in the latest available survey (2022) is 54.8 [adv:p181v1].

> **Citation `adv:p151v1`** (PDF page 151, table, TABLE 2.1, bbox[ymin,xmin,ymax,xmax]/1000=[645, 168, 787, 832])  
> TABLE 2.1: An inequality penalty is built into the Prosperity Gap index (table on PDF page 151; model-generated description) | | Benin | Cameroon | Peru | Colombia | | :--- | :--- | :--- | :--- | :--- | | | 2021 | 2021 | 2022 | 2022 | | Prosperity Gap | 7.20 | 8.32 | 3.60 | 4.69 | | Mean income | 5.02 | 5.37 | 12.4 | 17.3 | | Inequality | 1.44 | 1.79 | 1.79 | 3.25 |  Source: World Bank, Poverty and Inequality Platform (version September 2024), https://pip.worldbank.org. Note: The Prosperity Gap is calculated using the global prosperity standard of $25 per person per day in 2017 purchasing power parity dollars (PPP$). The table also shows the decomposition of the Prosperity Gap into the product of (25/mean income) and inequality. Inequality is measured using the inequality measure related to the Prosperity Gap—the average income multiple needed to reach the mean income (see annex 2B for details). Mean income is expressed in 2017 PPP$ per person per day. Estimates for each country are reported using the most recent survey data.

> **Citation `adv:p181v1`** (PDF page 181, table, TABLE 2F.1, bbox[ymin,xmin,ymax,xmax]/1000=[83, 168, 878, 832])  
> TABLE 2F.1: Gini index in latest available survey, by economy (table on PDF page 181; model-generated description) | Economy and group | Region | Survey year | Welfare type | Gini index | | :--- | :--- | :--- | :--- | :--- | | Angola | Sub-Saharan Africa | 2018.17 | Consumption | 51.3 | | Argentina | Latin America and the Caribbean | 2022 | Income | 40.7 | | Bolivia | Latin America and the Caribbean | 2021 | Income | 40.9 | | Botswana | Sub-Saharan Africa | 2015.85 | Consumption | 53.3 | | Brazil | Latin America and the Caribbean | 2022 | Income | 52.0 | | Cabo Verde | Sub-Saharan Africa | 2015 | Consumption | 42.4 | | Cameroon | Sub-Saharan Africa | 2021.67 | Consumption | 42.2 | | Central African Republic | Sub-Saharan Africa | 2021 | Consumption | 43.0 | | Chile | Latin America and the Caribbean | 2022 | Income | 43.0 | | Colombia | Latin America and the Caribbean | 2022 | Income | 54.8 | | Comoros | Sub-Saharan Africa | 2014 | Consumption | 45.3 | | Congo, Dem. Rep. | Sub-Saharan Africa | 2020 | Consumption | 44.7 | | Congo, Rep. | Sub-Saharan Africa | 2011.67 | Consumption | 48.9 | | Costa Rica | Latin America and the Caribbean | 2023 | Income | 46.7 | | Djibouti | Middle East and North Africa | 2017 | Consumption | 41.6 | | Ecuador | Latin America and the Caribbean | 2023 | Income | 44.6 | | Eswatini | Sub-Saharan Africa | 2016.17 | Consumption | 54.6 | | Ghana | Sub-Saharan Africa | 2016.75 | Consumption | 43.5 | | Grenada | Latin America and the Caribbean | 2018.36 | 

---

## adv-test-18 · multi-hop · status **answered**

**Question:** For Sub-Saharan Africa in 2024, what are the extreme poverty rate at $2.15 per day (Table 1D.1) and the Prosperity Gap (Table 2E.1)?
**Expected:** Extreme poverty rate 36.5 percent and Prosperity Gap 12.2.
- gold p128 — TABLE 1D.1, block '$2.15 per day', row 'Sub-Saharan Africa', column 2024: "Sub-Saharan Africa 54.6 58.0 56.0 48.7 42.1 38.2 36.7 37.9 37.6 37.0 36.9 36.5"
- gold p179 — TABLE 2E.1, row 'Sub-Saharan Africa', column 2024: "Sub-Saharan Africa 17.9 19.2 18.5 15.8 13.3 12.4 12.3 12.7 12.6 12.4 12.3 12.2"
**Gold pages in final context (automatic):** True

**Searches:** `"Table 1D.1" Sub-Saharan Africa extreme poverty rate 2024` → ['p129v1', 'p128v1', 'p093t2', 'p013t1', 'p118v1', 'p118t1', 'p117t1', 'p040t2'] · `"Table 2E.1" Prosperity Gap Sub-Saharan Africa` → ['p179v1', 'p147v1', 'p147t1', 'p013t1', 'p179t1', 'p146v1', 'p146t1', 'p010t2']

**Agent answer:** For Sub-Saharan Africa in 2024, the extreme poverty rate at $2.15 per day is 36.5 percent [adv:p128v1], and the Prosperity Gap is 12.2 [adv:p179v1, adv:p146t1].

> **Citation `adv:p128v1`** (PDF page 128, table, TABLE 1D.1, bbox[ymin,xmin,ymax,xmax]/1000=[177, 82, 915, 831])  
> TABLE 1D.1: Percentage of population living in poverty by region (table on PDF page 128; model-generated description) | Region and poverty line | 1990 | 1995 | 2000 | 2005 | 2010 | 2015 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | | **$2.15 per day** | | | | | | | | | | | | | | East Asia and Pacific | 65.2 | 49.0 | 39.7 | 20.7 | 12.6 | 2.3 | 1.0 | 1.1 | 1.1 | 1.0 | 0.9 | 0.8 | | Europe and Central Asia | 3.6 | 8.1 | 9.2 | 4.7 | 1.2 | 0.8 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | | Latin America and the Caribbean | 16.3 | 14.0 | 13.8 | 10.7 | 5.9 | 4.1 | 4.2 | 3.8 | 4.5 | 3.5 | 3.4 | 3.3 | | Middle East and North Africa | 6.4 | 4.7 | 3.0 | 2.7 | 1.9 | 3.7 | 4.6 | 5.3 | 5.9 | 6.1 | 6.4 | 6.7 | | South Asia | 50.0 | 43.8 | -- | 35.5 | 25.4 | 16.6 | 10.6 | 13.0 | 11.4 | 9.7 | 8.7 | 7.6 | | Sub-Saharan Africa | 54.6 | 58.0 | 56.0 | 48.7 | 42.1 | 38.2 | 36.7 | 37.9 | 37.6 | 37.0 | 36.9 | 36.5 | | Eastern and Southern Africa | -- | 57.5 | 56.3 | 50.2 | 44.2 | 41.7 | 43.1 | 44.5 | 44.2 | 43.6 | 43.7 | 43.2 | | Western and Central Africa | 55.2 | 58.8 | -- | 46.5 | 39.1 | 33.0 | 27.3 | 28.3 | 27.9 | 27.3 | 27.0 | 26.5 | | Rest of the world | 0.4 | 0.5 | 0.5 | 0.5 | 0.5 | 0.7 | 0.6 | 0.4 | 0.3 | 0.6 | 0.6 | 0.6 | | World | 37.9 | 32.5 | 29.3 | 21.5 | 15.7 | 10.5 | 8.8 | 9.7 | 9.5 | 9.0 | 8.8 | 8.5 | | FCS | -- | 49.9 | -- | 38.1 | 31.7 | 29.5 | 29.2 | 30.7 | 30.9 | 30.8 | 31.1 | 30.9 | | IDA | 54.4 

> **Citation `adv:p146t1`** (PDF page 146, text)  
> 112 POVERTY , PROSPERITY , AND PLANET REPORT 2024 An advantage of this new measure is that it can be easily decomposed, allowing for a better understanding of the main drivers of shared prosperity. The Prosperity Gap for a person is just the factor by which their income must increase to achieve $25 per day. The Prosperity Gap for a country is the average of these gaps for all people in the country. The Prosperity Gap for a region, such as Sub-Saharan Africa, is the population-weighted average of the Prosperity Gaps for all countries in the region. Finally, the Prosperity Gap for the world is a population-weighted average of the Prosperity Gaps for all regions in the world. Country Prosperity Gaps can thus be expressed as population- weighted average gaps of groups (provincial, state, ethnic, gender, or others) within the country. The poorest regions of the world have higher Prosperity Gaps than richer regions (figure 2.1, panel a). In 2024, the Prosperity Gap ranges from 1.7 in Europe and Central Asia to 12.2 in Sub-Saharan Africa among the geographic regions.8 This signals the large disparities in income and inequality levels across regions. In Sub-Saharan Africa, incomes would need to rise over 12-fold, on average, to reach the global prosperity standard of $25. The region with the second-highest regional Prosperity Gap is South Asia, with a gap of 6.2 in 2024, followed closely by the Middle East and North Africa, for which the trend has been extrapolated from 2018 because 

> **Citation `adv:p179v1`** (PDF page 179, table, TABLE 2E.1, bbox[ymin,xmin,ymax,xmax]/1000=[408, 167, 685, 833])  
> TABLE 2E.1: Prosperity Gap estimates, by region (table on PDF page 179; model-generated description) | Region | 1990 | 1995 | 2000 | 2005 | 2010 | 2015 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | | East Asia and Pacific | 16.5 | 13.0 | 11.5 | 8.06 | 6.26 | 4.06 | 3.25 | 3.28 | 3.04 | 3.00 | 2.92 | 2.83 | | Europe and Central Asia | 3.83 | 5.18 | 5.54 | 3.83 | 2.63 | 2.36 | 2.06 | 2.01 | 1.81 | 1.74 | 1.70 | 1.67 | | Latin America and the Caribbean | 8.01 | 7.52 | 7.64 | 6.15 | 4.40 | 3.60 | 3.57 | 3.61 | 3.67 | 3.36 | 3.28 | 3.25 | | Middle East and North Africa | 5.40 | 5.25 | 4.59 | 4.35 | 4.00 | 4.16 | 4.38 | 4.62 | 4.67 | 4.61 | 4.65 | 4.69 | | South Asia | 12.7 | 11.7 | -- | 10.4 | 9.19 | 8.05 | 6.88 | 7.22 | 6.97 | 6.64 | 6.43 | 6.21 | | Sub-Saharan Africa | 17.9 | 19.2 | 18.5 | 15.8 | 13.3 | 12.4 | 12.3 | 12.7 | 12.6 | 12.4 | 12.3 | 12.2 | | Eastern and Southern Africa | 17.0 | 18.7 | 19.0 | 17.0 | 14.4 | 13.5 | -- | 14.7 | 14.5 | 14.3 | 14.2 | 14.1 | | Western and Central Africa | 19.2 | 19.9 | -- | 14.2 | 11.8 | 10.8 | 9.54 | 9.74 | 9.66 | 9.56 | 9.51 | 9.42 | | Rest of the world | 1.15 | 1.15 | 1.09 | 1.10 | 1.07 | 1.11 | 0.98 | 0.83 | 0.80 | 1.01 | 0.98 | 0.98 | | World | 10.9 | 9.96 | 9.43 | 7.81 | 6.55 | 5.58 | 5.12 | 5.28 | 5.16 | 5.07 | 5.00 | 4.93 |  Source: World Bank, Poverty and Inequality Platform (version September 2024), https://pip.worldbank.org. Note: The estim

---

## adv-test-19 · multi-hop · status **answered**

**Question:** What heat wave intensity threshold does the report use to define exposure, and what does that temperature correspond to according to the international standard cited?
**Expected:** Above 33°C maximum 5-day average of daily maximum wet bulb globe temperature (WBGT); 33°C WBGT is the reference upper limit for healthy, acclimatized humans at rest to keep a normal core temperature (ISO 7243).
- gold p237 — TABLE 3B.1, row 'Heat wave': "Heat wave > 33°C maximum 5-day average of daily maximum WBGT"
- gold p238 — body text, first paragraph: "A wet bulb globe temperature threshold of 33°C corresponds to the reference upper limit for healthy, acclimatized humans at rest to keep a normal core temperature, based on international standard ISO 7243"
**Gold pages in final context (automatic):** True

**Searches:** `"heat wave" intensity threshold exposure international standard` → ['p237v1', 'p237t2', 'p237t1', 'p199t2', 'p277t1', 'p284t1', 'p276t2', 'p238t1']

**Agent answer:** The report defines the heat wave intensity threshold for exposure as a maximum 5-day average of daily maximum wet bulb globe temperature (WBGT) greater than 33°C [adv:p237v1, adv:p237t2]. This 33°C threshold corresponds to the reference upper limit for healthy, acclimatized humans at rest to maintain a normal core temperature, as established by the international standard ISO 7243 for assessing heat stress on workers [adv:p238t1].

> **Citation `adv:p237v1`** (PDF page 237, table, TABLE 3B.1, bbox[ymin,xmin,ymax,xmax]/1000=[586, 168, 755, 832])  
> TABLE 3B.1: Hazard thresholds (table on PDF page 237; model-generated description) | Hazard | Intensity threshold | | :--- | :--- | | Agricultural drought | > 30% cropland or grassland affected by severe drought | | Flood | > 50-cm maximum inundation depth | | Heat wave | > 33°C maximum 5-day average of daily maximum WBGT | | Tropical cyclone | > 37.6-m/s 10-minute average sustained wind speed or equivalent ≥ Category 2 on the Saffir-Simpson scale |  Source: World Bank Group Scorecard indicator: the percentage of people at high risk of climate-related hazards globally, https://scorecard.worldbank.org/en/scorecard/home. Note: C = Celsius; cm = centimeter; m/s = meters per second; WBGT = wet bulb globe temperature.

> **Citation `adv:p237t2`** (PDF page 237, text)  
> have a greater than 50 percent chance of experiencing the respective shock in their lifetime (using average global life expectancy). TABLE 3B.1 Hazard thresholds Hazard Intensity threshold Agricultural drought > 30% cropland or grassland affected by severe drought Flood > 50-cm maximum inundation depth Heat wave > 33°C maximum 5-day average of daily maximum WBGT Tropical cyclone > 37.6-m/s 10-minute average sustained wind speed or equivalent ≥ Category 2 on the Saffir-Simpson scale Source: world bank Group scorecard indicator: the percentage of people at high  risk of climate-related hazards globally, https://scorecard.worldbank.org/en/scorecard/home. Note: C = Celsius; cm = centimeter; m/s = meters per second; wbGt = wet bulb globe temperature. The selected intensity levels are based on the literature and are levels above which an event is considered to have severe effects on people. In the case of drought, the cutoff used follows the severe drought definition by the FAO. In the case of flood, inundation depths of at least 50 centimeters indicate a high risk that bring disruptions to livelihoods and economic activity,

> **Citation `adv:p238t1`** (PDF page 238, text)  
> 204 POVERTY , PROSPERITY , AND PLANET REPORT 2024 as well as risk to life for select locations and vulnerable groups (Rentschler, Salhab, and Jafino 2022). For a fluvial and marine flood depth of 0.5 meters, Huizinga, de Moel, and Szewczyk (2017) estimate that the average share of residential assets lost ranges from 0.22 to 0.49. Cyclone damage functions also indicate direct economic damage in the range of 0.2 to 0.5 for category 2 wind speeds for most regions, which defines the cutoff used for cyclones (Eberenz, Lüthi, and Bresch 2021). A wet bulb globe temperature threshold of 33°C corresponds to the reference upper limit for healthy, acclimatized humans at rest to keep a normal core temperature, based on international standard ISO 7243 used to assess heat stress on workers (ISO 2017). Heat- related mortality and hospital visits increase significantly around this level. Measuring vulnerability Vulnerability is the propensity or predisposition of people to be adversely affected by hazards. Here, vulnerability is proxied by seven indicators measuring (a) the physical propensity to experience severe losses (proxied by the lack of mobility and access to basic infrastructure services, such as water and electricity) and (b) the inability to cope with and recover from losses (proxied by low income, not having education, not having access to financial services, and not having access to social protection). Table 3B.2 summarizes the different dimensions. TABLE 3B.2 Extreme vulnerabil

---

## adv-test-20 · multi-hop · status **answered**

**Question:** In Sub-Saharan Africa, what share of the total population is at high risk from extreme weather events, and what is the region's multidimensional poverty rate in Table 1.1?
**Expected:** 37.3 percent of the population is at high risk (39.2 percent exposed), and the multidimensional poverty rate is 52.6 percent (circa 2021).
- gold p203 — body text above MAP 3.1: "nearly the same proportion of people exposed to an extreme weather event is also at high risk (39.2 percent and 37.3 percent, respectively, of the total population)"
- gold p117 — TABLE 1.1, row 'Sub-Saharan Africa', column 'Multidimensional poverty rate': "Sub-Saharan Africa 39 29 18 46 59 29 52.6 24 31"
**Gold pages in final context (automatic):** True

**Searches:** `Table 1.1 Sub-Saharan Africa high risk extreme weather multidimensional poverty rate` → ['p117v1', 'p118t1', 'p013t1', 'p118v1', 'p068v1', 'p118t2', 'p203t1', 'p116t2']

**Agent answer:** In Sub-Saharan Africa, 37.3 percent of the total population is at high risk from extreme weather events [adv:p203t1]. According to Table 1.1, the region's multidimensional poverty rate is 52.6 percent [adv:p117v1].

> **Citation `adv:p117v1`** (PDF page 117, table, TABLE 1.1, bbox[ymin,xmin,ymax,xmax]/1000=[163, 105, 653, 908])  
> TABLE 1.1: Deprivations in educational attainment and access to basic infrastructure lift multidimensional poverty above the extreme poverty rate, 2021 (table on PDF page 117; model-generated description) | Region | Monetary | Educational attainment | Educational enrollment | Electricity | Sanitation | Drinking water | Multidimensional poverty rate | Number of economies | Coverage (%) | | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | | East Asia and Pacific | 2 | 5 | 2 | 1 | 9 | 4 | 2.7 | 12 | 26 | | Europe and Central Asia | 0 | 1 | 1 | 2 | 8 | 4 | 2.1 | 24 | 78 | | Latin America and the Caribbean | 3 | 8 | 2 | 1 | 17 | 3 | 3.6 | 18 | 86 | | Middle East and North Africa | 1 | 7 | 2 | 0 | 2 | 1 | 1.5 | 3 | 24 | | South Asia | 4 | 15 | 18 | 6 | 23 | 5 | 11.2 | 6 | 11 | | Sub-Saharan Africa | 39 | 29 | 18 | 46 | 59 | 29 | 52.6 | 24 | 31 | | Rest of the world | 0 | 1 | 2 | 0 | 0 | 0 | 1.0 | 23 | 69 | | World | 9 | 10 | 8 | 10 | 21 | 9 | 13.4 | 110 | 37 | | IDA countries | 25 | 23 | 17 | 29 | 44 | 19 | 35.6 | 38 | 34 | | Countries in FCS | 38 | 27 | 18 | 45 | 55 | 28 | 50.4 | 13 | 27 |  Source: World Bank, Global Monitoring Database (GMD) (version September 2024). Note: FCS = fragile and conflict-affected situations; IDA = International Development Association. The table presents the multidimensional poverty rate and share of population deprived in each indicator by region and rest of the world for circa 2021. “Multidimensional poverty rate” is the share o

> **Citation `adv:p203t1`** (PDF page 203, text)  
> 169 livable Planet Being at high risk is defined as being exposed to hazards and also being vulnerable to their impacts. Nearly one in five people (17.9 percent) is at high risk from climate-related hazards globally. Sub-Saharan Africa has the largest share of people at high risk from extreme weather events (map 3.1). In Sub-Saharan Africa, nearly the same proportion of people exposed to an extreme weather event is also at high risk (39.2 percent and 37.3 percent, respectively, of the total population). In Latin America and the Caribbean and the Middle East and North Africa, 13.2 percent and 13.9 percent of the population is at risk, respectively. In East Asia and Pacific, less than one-tenth of people are at risk. The share of people at risk is lowest in North America, where less than 1 percent of the population is at high risk, despite 31 percent of the population being exposed to any weather shock. In absolute terms, South Asia has the largest total population at high risk from extreme weather events (594 million people, or 32 percent of the sample population). MAP 3.1 Large populations are exposed to extreme weather events in South Asia and East Asia and Pacific, and vulnerability is high in Sub-Saharan Africa North AmericaNorth America Latin America & CaribbeanLatin America & Caribbean Europe & Central AsiaEurope & Central Asia South AsiaSouth Asia East Asia & Paci/f_icEast Asia & Paci/f_ic Sub-Saharan AfricaSub-Saharan Africa Middle East & North AfricaMiddle East & Nort

---

## adv-test-21 · text · status **answered**

**Question:** At the $6.85 poverty line, how does the likelihood of living in poverty change with primary and with secondary education?
**Expected:** Around three-quarters of people aged 15+ without formal education live below $6.85; primary education reduces the likelihood to 65 percent and secondary education to 44 percent.
- gold p113 — body text, first paragraph: "Obtaining even primary education reduces the likelihood of living in poverty to 65 percent, and a secondary education further reduces it to 44 percent"
**Gold pages in final context (automatic):** True

**Searches:** `likelihood of living in poverty $6.85 primary secondary education` → ['p113t1', 'p114v1', 'p114t1', 'p112t2', 'p036t1', 'p099t2', 'p095t1', 'p084t1']

**Agent answer:** At the $6.85 poverty line, obtaining a primary education reduces the likelihood of living in poverty to 65 percent, while obtaining a secondary education further reduces it to 44 percent [adv:p113t1].

> **Citation `adv:p113t1`** (PDF page 113, text)  
> 79 Global Poverty uPdate and  outloo K At the poverty line of $6.85, the gradient between educational attainment and poverty becomes even more pronounced across all regions. Around three-quarters of the population age 15 or above without any formal education lives on less than $6.85 a day (figure 1.12, panel b). Obtaining even primary education reduces the likelihood of living in poverty to 65 percent, and a secondary education further reduces it to 44 percent. About one-third of the population age 15 or above with tertiary education lives in poverty. Focusing on closing education gaps is also a policy priority, given the significant educational losses due to the pandemic, particularly for the poor. School closures led to learning losses in language, literacy, and mathematics of around 30 percent in multiple countries. In 2021, in several countries a quarter of all young people were not in education, employment, or training (Schady et al. 2023). Poorer households were also less likely to use remote work and schooling (Narayan et al. 2022). Schooling disruptions affected poorer households more than richer ones. It is estimated that students in low- and lower-middle- income countries could face future earning losses of up to 10 percent due to the pandemic, suggesting a permanent scarring effect (Schady et al. 2023). This generation of students now risks losing $21 trillion in potential lifetime earnings in present value—the equivalent of 17 percent of today’s global GDP (World 

---

## adv-test-22 · text · status **answered**

**Question:** How much potential lifetime earnings does the generation of students affected by the pandemic risk losing, and what share of global GDP is that?
**Expected:** $21 trillion in potential lifetime earnings in present value, equivalent to 17 percent of today's global GDP.
- gold p113 — body text, second paragraph: "This generation of students now risks losing $21 trillion in potential lifetime earnings in present value—the equivalent of 17 percent of today’s global GDP"
**Gold pages in final context (automatic):** True

**Searches:** `pandemic generation students potential lifetime earnings loss global GDP share` → ['p040t1', 'p113t1', 'p244t2', 'p199t1', 'p207t2', 'p041t1', 'p237t1', 'p040t2']

**Agent answer:** The generation of students affected by the pandemic risks losing $21 trillion in potential lifetime earnings in present value, which is equivalent to 17 percent of today’s global GDP [adv:p040t1], [adv:p113t1].

> **Citation `adv:p040t1`** (PDF page 40, text)  
> 6 Poverty , ProsPerity , and Planet rePort 2024 In addition to a slower recovery in terms of income, poor people experienced setbacks in human capital and employment, further compromising their resilience and capacity to generate higher incomes in the future. The pandemic had a devastating effect on global health, causing a significant number of excess deaths and reducing the global life expectancy at birth by over 1.5 years.3 Countries with higher inequalities in income and access to quality care had higher excess mortality during the pandemic (Sepulveda and Brooker 2021). The health and food systems disruptions caused by the pandemic also reversed progress on child nutrition, with an estimated additional 9.3 million children suffering from acute malnutrition and 2.6 million more children stunted by 2022 (Osendarp et al. 2020). In addition, school closures led to learning losses in language, literacy, and mathematics of around 30 percent in multiple countries. In 2021, in several countries a quarter of all young people were not in education, employment, or training (Schady et al. 2023). Poorer households were also less likely to use remote work and schooling (Narayan et al. 2022). Schooling disruptions affected poorer households more than richer ones. It is estimated that students in low-income and lower- middle-income countries could face future earning losses of up to 10 percent because of the pandemic, suggesting a permanent scarring effect (Schady et al. 2023). This gene

> **Citation `adv:p113t1`** (PDF page 113, text)  
> 79 Global Poverty uPdate and  outloo K At the poverty line of $6.85, the gradient between educational attainment and poverty becomes even more pronounced across all regions. Around three-quarters of the population age 15 or above without any formal education lives on less than $6.85 a day (figure 1.12, panel b). Obtaining even primary education reduces the likelihood of living in poverty to 65 percent, and a secondary education further reduces it to 44 percent. About one-third of the population age 15 or above with tertiary education lives in poverty. Focusing on closing education gaps is also a policy priority, given the significant educational losses due to the pandemic, particularly for the poor. School closures led to learning losses in language, literacy, and mathematics of around 30 percent in multiple countries. In 2021, in several countries a quarter of all young people were not in education, employment, or training (Schady et al. 2023). Poorer households were also less likely to use remote work and schooling (Narayan et al. 2022). Schooling disruptions affected poorer households more than richer ones. It is estimated that students in low- and lower-middle- income countries could face future earning losses of up to 10 percent due to the pandemic, suggesting a permanent scarring effect (Schady et al. 2023). This generation of students now risks losing $21 trillion in potential lifetime earnings in present value—the equivalent of 17 percent of today’s global GDP (World 

---

## adv-test-23 · text · status **answered**

**Question:** By how much could sea levels rise in the Maldives by 2100, and what share of its land mass lies less than 1 meter above mean sea level?
**Expected:** Sea levels could rise 0.5 to 0.9 meters by 2100; at least 80 percent of the land mass lies less than 1 meter above mean sea level.
- gold p208 — box text on Small Island States: "in the Maldives, sea levels could rise 0.5 to 0.9 meters by 2100 (World Bank 2024c). At least 80 percent of the land mass lies less than 1 meter above mean sea level"
**Gold pages in final context (automatic):** True

**Searches:** `Maldives sea level rise 2100 land mass 1 meter` → ['p208t1', 'p245t3', 'p208t2', 'p075t2', 'p274t2', 'p244t1', 'p279t1', 'p244t2']

**Agent answer:** In the Maldives, sea levels could rise by 0.5 to 0.9 meters by 2100 [adv:p208t1]. At least 80 percent of the country's land mass lies less than 1 meter above mean sea level [adv:p208t1].

> **Citation `adv:p208t1`** (PDF page 208, text)  
> 174 POVERTY , PROSPERITY , AND PLANET REPORT 2024 Without faster action, climate-related hazards will likely intensify In 2022, the three main anthropogenic GHGs—carbon dioxide (CO 2), methane, and nitrous oxide—reached record levels, trapping nearly 50 percent more heat than in 1990. 4 There is overwhelming scientific consensus that human activities are responsible for increases in GHG emissions, which have led to the warming of the atmosphere, ocean, and land (Cook et al. 2016). The Sixth Assessment Report of the Intergovernmental Panel on Climate Change (IPCC) determined that observed global warming over the past 200 years is nearly fully attributable to human activities (Eyring et al. 2021; For example, in the Maldives, sea levels could rise 0.5 to 0.9 meters by 2100 (World Bank 2024c). At least 80 percent of the land mass lies less than 1 meter above mean sea level, and more than 40 percent of the population resides within 100 meters of the coastline. Without adaptation, a 1-in-10-year coastal flood could damage 3.3 percent of total assets in the country by 2050 (World Bank 2024c). In addition, ocean pollution from significant amounts of per capita waste and coastal infrastructure development negatively affects island and marine ecosystems, adding to the stress from sea level rise and higher ocean temperatures (World Bank 2024d). These issues are not specific to the Maldives; other Small Island States face similar concerns (Thomas et al. 2020; Vousdoukas et al. 2023; Wor

---

## adv-test-24 · text · status **answered**

**Question:** Among countries that have both income- and consumption-based surveys for the same year, how much lower is the average consumption-based Gini index than the income-based one?
**Expected:** 4.5 Gini points, or 10 percent, lower.
- gold p176 — body text below TABLE 2D.1: "the average consumption-based Gini index is 4.5 points, or 10 percent, lower than the corresponding income-based index"
**Gold pages in final context (automatic):** True

**Searches:** `"income- and consumption-based surveys" Gini index difference` → ['p176t1', 'p176t2', 'p271t1', 'p190t1', 'p267v1', 'p267t1', 'p187t3', 'p169t1']

**Agent answer:** Among countries that have both income- and consumption-based surveys for the same year, the average consumption-based Gini index is 4.5 points, or 10 percent, lower than the corresponding income-based index [adv:p176t1].

> **Citation `adv:p176t1`** (PDF page 176, text)  
> 142 POVERTY , PROSPERITY , AND PLANET REPORT 2024 aggregates in the World Bank’s Poverty and Inequality Platform. The indicator tracks the number of economies, and therefore all economies, regardless of population, count the same. The indicator is based on either income or consumption inequality, depending on the welfare measure adopted by each economy. Most high-income countries and countries in Latin America and the Caribbean use income, while the rest of the world uses consumption (table 2D.1). In the latest year, only 6 percent of low-income and lower-middle-income countries have income-based surveys. This poses a challenge because income inequality is generally higher than consumption inequality for the same sample of households (Deininger and Squire 1996).26 TABLE 2D.1 Statistics of Gini indexes in the Poverty and Inequality Platform, post-2000 Economy count Survey count Share of LICs and LMICs Average Gini Income-based surveys 66 1,057 0.06 37.3 Consumption-based surveys 100 570 0.71 36.2 Total 166 1,627 0.45 36.9 Source: world bank, Poverty and inequality Platform (version september 2024),  https://pip.worldbank.org. Note: liCs = lower-income countries; lmiCs = lower-middle-income countries. Among countries that have both income- and consumption-based surveys for the same year, the average consumption-based Gini index is 4.5 points, or 10 percent, lower than the corresponding income-based index (Haddad et al. 2024). Figure 2D.1 plots income and consumption Gini indexe

---

## adv-test-u1 · unanswerable · status **abstain** (model_abstained)

**Question:** What was the extreme poverty rate in Sub-Saharan Africa in 1985?
**Expected:** abstain. **Absence check:** Table 1D.1 (p128) starts in 1990; the only '1985' in the PDF text is the x-axis bin '1985–89' of Figure 3.5 (disasters).

**Searches:** `extreme poverty rate Sub-Saharan Africa 1985` → ['p125t2', 'p040t2', 'p118t2', 'p096t2', 'p098t1', 'p066t1', 'p108t2', 'p098t2'] · `"Sub-Saharan Africa" extreme poverty rate 1985` → ['p125t2', 'p040t2', 'p118t2', 'p096t2', 'p098t1', 'p066t1', 'p108t2', 'p098t2'] · `What was the extreme poverty rate in Sub-Saharan Africa in 1985?` → ['p040t2', 'p095t1', 'p098t2', 'p099t1', 'p126t1', 'p125t2', 'p118t2', 'p096t2']

**Agent abstained.** Model reason: The provided document does not contain information regarding the extreme poverty rate in Sub-Saharan Africa for the year 1985. It provides data for 1990 and later years.

---

## adv-test-u2 · unanswerable · status **abstain** (answer_states_missing)

**Question:** What is the multidimensional poverty rate of China in Table 1.1?
**Expected:** abstain. **Absence check:** Table 1.1 (p117) reports regions and groups only; its note says data for China and India are absent.

**Searches:** `Table 1.1 multidimensional poverty rate China` → ['p117v1', 'p118t1', 'p116t2', 'p117t1', 'p118v1', 'p119v1', 'p119t1', 'p100t1'] · `What is the multidimensional poverty rate of China in Table 1.1?` → ['p117v1', 'p118t1', 'p116t2', 'p117t1', 'p118v1', 'p119v1', 'p119t1', 'p118t2']

**Agent abstained.** Model reason: -
Rejected answer (invalid citations ['adv:p117v1']): Table 1.1 does not provide the multidimensional poverty rate for China; the notes to the table explicitly state that the absence of data for China reduces coverage for the East Asia and Pacific region [adv:p117v1].

---

## adv-test-u3 · unanswerable · status **abstain** (answer_states_missing)

**Question:** What intensity threshold does Table 3B.1 define for wildfires?
**Expected:** abstain. **Absence check:** Table 3B.1 (p237) lists only agricultural drought, flood, heat wave and tropical cyclone; 'wildfire' appears only in unrelated text (p243, p274) and references.

**Searches:** `Table 3B.1 wildfire intensity threshold` → ['p237v1', 'p237t1', 'p237t2', 'p276t2', 'p238t1', 'p199t2', 'p238v1', 'p294t3'] · `What intensity threshold does Table 3B.1 define for wildfires?` → ['p237v1', 'p237t1', 'p276t2', 'p237t2', 'p274t2', 'p238t1', 'p178t2', 'p238v1']

**Agent abstained.** Model reason: -
Rejected answer (invalid citations ['adv:p237t2', 'adv:p237v1', 'adv:p274t2']): Table 3B.1 does not define an intensity threshold for wildfires, as the report notes that wildfires are among the climate-related hazards omitted from the indicator [adv:p237v1, adv:p237t2, adv:p274t2].

---

## adv-test-u4 · unanswerable · status **abstain** (model_abstained)

**Question:** How many economies had high inequality in 1995 according to Figure 2.9?
**Expected:** abstain. **Absence check:** Figure 2.9 (p159) covers 2000-22 only.

**Searches:** `Figure 2.9 high inequality 1995` → ['p159v1', 'p026t1', 'p179t1', 'p158t1', 'p209t2', 'p160t1', 'p179v1', 'p129t1'] · `How many economies had high inequality in 1995 according to Figure 2.9?` → ['p159v1', 'p160t1', 'p164t1', 'p162t1', 'p046t2', 'p139t1', 'p158t1', 'p009t2']

**Agent abstained.** Model reason: Figure 2.9 in the report only provides data for the years 2000–2022 [adv:p159v1]. There is no information regarding the number of economies with high inequality in 1995.

---

## adv-test-u5 · unanswerable · status **abstain** (model_abstained)

**Question:** What was Ireland's disposable income Gini index in 2023?
**Expected:** abstain. **Absence check:** The report gives Ireland's disposable income Gini only for 2018 (29.4, p167) and a 2021 income Gini of 30.1 in Table 2F.1 (p183); nothing for 2023.

**Searches:** `Ireland disposable income Gini index 2023` → ['p167t1', 'p167v1', 'p269v1', 'p269t1', 'p271t1', 'p271v1', 'p189t2', 'p188t3'] · `What was Ireland's disposable income Gini index in 2023?` → ['p167t1', 'p167v1', 'p269v1', 'p269t1', 'p271t1', 'p271v1', 'p189t2', 'p268t2']

**Agent abstained.** Model reason: The provided document does not contain Ireland's disposable income Gini index for the year 2023. The report provides data for Ireland for 2018 [adv:p167t1] and discusses comparisons between databases for 2021 [adv:p269t1], but it does not provide a 2023 figure.

---

## adv-test-u6 · unanswerable · status **abstain** (answer_states_missing)

**Question:** What Prosperity Gap does Table 2E.1 report for Viet Nam in 2024?
**Expected:** abstain. **Absence check:** Table 2E.1 (p179) reports regions and the world only, no individual economies.

**Searches:** `Table 2E.1 Prosperity Gap Viet Nam 2024` → ['p179v1', 'p147v1', 'p147t1', 'p185v1', 'p151v1', 'p179t1', 'p185t1', 'p151t2'] · `What Prosperity Gap does Table 2E.1 report for Viet Nam in 2024?` → ['p179v1', 'p147v1', 'p147t1', 'p185v1', 'p151v1', 'p179t1', 'p185t1', 'p008t1']

**Agent abstained.** Model reason: -
Rejected answer (invalid citations ['adv:p179t1']): Table 2E.1 reports Prosperity Gap estimates by region, not by individual country [adv:p179t1]. Therefore, it does not provide a Prosperity Gap estimate for Viet Nam.

---
