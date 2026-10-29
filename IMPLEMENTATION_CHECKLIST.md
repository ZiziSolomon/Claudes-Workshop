# Circular Metro Implementation Checklist & Workbook
## Practical Step-by-Step Planning Guide for Cities

---

## Introduction

This workbook guides cities through the circular metro planning process with concrete checklists, templates, and worksheets. Use it alongside:
- **DESIGN_PRINCIPLES.md** (design standards)
- **CASE_STUDIES_APPLIED.md** (precedents)
- **Interactive tools** (modeling and testing)

---

## PHASE 1: FEASIBILITY ASSESSMENT (Months 1-6)

### 1.1 Pre-Planning Checklist

**1.1.1 Does Your City Meet Basic Criteria?**

- [ ] Metropolitan population ≥ 5 million (or 3M+ with strong density)
- [ ] Urban form supports circular concept (polycentric, sprawling, not perfectly monocentric)
- [ ] Daily transit ridership projection ≥ 200,000 (use worksheet 1.3)
- [ ] Planning horizon ≥ 10 years (political commitment possible)
- [ ] Funding pathway exists (government, development banks, PPP, or combination)

**If NO to any:** Circular line may not be appropriate. Consider radial extensions first.

**If YES to all:** Proceed to 1.2.

### 1.2 Core Team Assembly

**1.2.1 Establish Project Team**

Required roles and expertise:
- [ ] Project Director (political/administrative authority)
- [ ] Chief Planner (urban planning, long-term vision)
- [ ] Chief Engineer (technical feasibility, construction)
- [ ] Chief Economist (financial modeling, viability)
- [ ] Chief Operator (transit operations, logistics)
- [ ] Community Liaison (stakeholder engagement)

**Assignment document:**
```
Role                     Name           Organization    Contact
─────────────────────────────────────────────────────────────────
Project Director         ________       ________        ________
Chief Planner           ________       ________        ________
Chief Engineer          ________       ________        ________
Chief Economist         ________       ________        ________
Chief Operator          ________       ________        ________
Community Liaison       ________       ________        ________
```

### 1.3 Demand Forecasting Worksheet

**1.3.1 Conservative Ridership Projection**

Use this formula to estimate daily ridership:

```
Daily Riders = Catchment Population × Transit Mode Share × Service Quality Factor

Step 1: Define catchment area
  Assume 1 km walking distance on each side of proposed line
  = Total accessible population within 1 km
  __________ = Catchment population

Step 2: Estimate transit mode share
  Conservative assumption: 15% of catchment uses transit on typical day
  × 0.15 = Transit-dependent population: __________

Step 3: Estimate mode shift from other transport
  If built, % of car/bus/other users who would shift to circle line
  × ___ % = Mode shift riders: __________

Step 4: Adjust for service quality
  Quality factor (0.7-1.0):
    0.7 = Comparable to current transit service
    0.8 = Better than current service
    0.9 = Significantly better
    1.0 = Exceptional service (Taipei standard)
  × ____ = Quality adjustment: __________

CONSERVATIVE DAILY RIDERSHIP ESTIMATE: __________ riders
```

**1.3.2 Three-Scenario Analysis**

Project three scenarios:

| Scenario | Daily Ridership | Assumption | Payback Period |
|----------|-----------------|-----------|-----------------|
| **Conservative** | __________ | 70% of projection, 3-year ramp | __________ years |
| **Base Case** | __________ | 85% of projection, 4-year ramp | __________ years |
| **Optimistic** | __________ | 100% of projection, 2-year ramp | __________ years |

**Decision rule:** Base case payback should be ≤ 20 years. If > 20 years, revisit design.

### 1.4 Initial Viability Assessment

**1.4.1 Quick Feasibility Matrix**

Rate each factor (1=not favorable, 5=highly favorable):

| Factor | Rating | Notes |
|--------|--------|-------|
| **Urban form fit** | ___ | Does circular concept match city topology? |
| **Demand density** | ___ | Are 200k+ daily riders realistic? |
| **Government support** | ___ | Is political commitment likely? |
| **Funding pathway** | ___ | Can city access capital? |
| **Technical feasibility** | ___ | Are there major engineering barriers? |
| **Environmental benefits** | ___ | Clear air quality, emissions reduction? |
| **Integration opportunity** | ___ | Can existing metro lines interconnect? |

**Total score:** ___/35

**Decision rule:**
- 28-35: **Proceed with full feasibility study**
- 21-27: **Proceed, but address weak areas first**
- 14-20: **Consider alternatives (radial extensions, etc.)**
- <14: **Not appropriate at this time**

### 1.5 Key Stakeholder Mapping

**1.5.1 Identify and Engage Stakeholders**

```
Stakeholder Group          Interest Level    Support/Opposition    Engagement Strategy
────────────────────────────────────────────────────────────────────────────────────
Municipal government       H/M/L            +/0/-                 ________________
Regional authorities       H/M/L            +/0/-                 ________________
Existing transit operator  H/M/L            +/0/-                 ________________
Business community         H/M/L            +/0/-                 ________________
Residential communities    H/M/L            +/0/-                 ________________
Environmental groups       H/M/L            +/0/-                 ________________
Labor unions              H/M/L            +/0/-                 ________________
Construction industry     H/M/L            +/0/-                 ________________
Academic institutions     H/M/L            +/0/-                 ________________
International financiers  H/M/L            +/0/-                 ________________
```

**Action:** For any with opposition (-), develop engagement strategy to shift to +/0.

---

## PHASE 2: DESIGN PARAMETERS & FEASIBILITY STUDY (Months 7-24)

### 2.1 Design Parameter Selection Worksheet

**2.1.1 Determine Optimal Circumference**

Reference ranges (from DESIGN_PRINCIPLES.md Part 2):
- 15-50 km depending on city size and topology

**Your city's considerations:**
```
Factor                              Impact on Circumference
──────────────────────────────────────────────────────────
Largest suburban employment centers Need coverage: __ km radius
Major transportation corridors      Must include: ___ km reach
Population density zones            Optimal service: __ km reach
Existing transit interchanges       Must connect: ___ points

RECOMMENDED CIRCUMFERENCE: __________ km
```

**2.1.2 Station Spacing & Count**

Reference standard: 1.2-1.6 km spacing (optimal)

```
Circumference: __________ km ÷ 1.4 km spacing = __________ stations

Check feasibility:
- [ ] Can accommodate this many stations without excessive cost?
- [ ] Does spacing align with urban development patterns?
- [ ] Are all employment centers served?
- [ ] Is pedestrian access adequate (all stations within catchment)?

FINAL STATION COUNT: __________ stations at __________ km average spacing
```

**2.1.3 Core Design Parameters Worksheet**

Complete this table (reference DESIGN_PRINCIPLES.md Part 2):

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Circumference** | ___ km | Urban coverage needs |
| **Station Count** | ___ stations | 1.2-1.6 km spacing |
| **Design Speed** | 80 km/h | Standard (adjustable ±10) |
| **Operating Speed** | ___ km/h | = Circumference ÷ (15 min cycle time) |
| **Peak Headway** | ___ min | 2-4 min typical; 3 min baseline |
| **Off-Peak Headway** | ___ min | Typically 6-8 min |
| **Train Length** | ___ cars | 3-6 cars; match 3-4 min headway requirement |
| **Fleet Size** | ___ trains | = (Circumference ÷ operating speed) + 2-3 spares |
| **Daily Ridership Projection** | __________ | From worksheet 1.3 |
| **Annual Operating Cost** | $__ million | = Fleet size × $5M-8M per year |

### 2.2 Technology Decision Matrix

**2.2.1 Automation Level Assessment**

Should your line be driverless, ATO-capable, or manual?

| Automation Level | Capital Cost | Annual Op. Cost | Payback Impact | Decision |
|---|---|---|---|---|
| **Traditional (Drivers)** | Baseline | Baseline (+40%) | Standard | ☐ |
| **ATO-Capable Design** | +$10M | Baseline (−5%) | Upgrade path | ☐ |
| **Full Driverless (GoA4)** | +$80M-150M | Baseline (−35%) | 7-10 yrs faster | ☐ |

**Your city's constraints:**

```
Question                                               Answer
────────────────────────────────────────────────────────────
Is budget tight (payback must be <15 yrs)?            Y / N
Is ridership projection high (>400k/day)?             Y / N
Is technology expertise available locally?            Y / N
Is operational staff comfortable with automation?     Y / N
Does government prioritize innovation/tech lead?      Y / N
```

**Recommendation:**
- **All Y:** Recommend full driverless (Seoul model)
- **Mix:** Recommend ATO-capable (flexible for future)
- **Mostly N:** Recommend traditional operation

### 2.3 Route Alignment & Interchange Strategy

**2.3.1 Proposed Route & Interchange Points**

Create map showing:
- [ ] Proposed circular alignment (attach map)
- [ ] Current transit lines it will intersect
- [ ] Proposed interchange stations (limit to 3-5 major points)
- [ ] Distance from each interchange to other lines

**Interchange Point Checklist:**

For each proposed major interchange, verify:
- [ ] Existing station has passenger capacity for 20% growth
- [ ] Physical connection possible (less than 100m walking distance)
- [ ] Fare integration possible with existing system
- [ ] Station complexity manageable (not creating construction bottleneck)

### 2.4 Cost Estimation Framework

**2.4.1 Capital Cost Calculation**

```
Base cost: __________ km × $400M/km = $__________ (base estimate)

Adjustments:
+ Underground (50% of line): +30% = $__________ adjustment
+ Elevated (30% of line): +10% = $__________ adjustment
+ At-grade (20% of line): −5% = $__________ adjustment

+ Dense urban area labor premium: +15% = $__________ adjustment
− Developing economy labor savings: −20% = $__________ adjustment

ESTIMATED CAPITAL COST: $__________ million

Contingency (+15-20%): +$__________ million
────────────────────────────────────
TOTAL WITH CONTINGENCY: $__________ million
```

**2.4.2 Operating Cost Framework**

```
Fleet size: __________ trains

Cost per train per year: $__________ (range: $5M-8M)
× __________ trains = $__________ base operating cost

Maintenance: +15% = $__________ 
Administration: +10% = $__________ 
Power/utilities: +5% = $__________ 
Insurance: +3% = $__________ 

TOTAL ANNUAL OPERATING COST: $__________ million
```

### 2.5 Financial Viability Worksheet

**2.5.1 Revenue Projection**

```
Daily ridership (year 3): __________ riders
Average fare: $__________ per trip
Daily revenue: __________ × $__________ = $__________
Annual revenue (365 days): $__________ million
```

**2.5.2 Payback Period Calculation**

```
Capital cost (with contingency): $__________ million
Annual operating cost: $__________ million
Annual revenue: $__________ million

Year 1: 60% ridership × $__________ = $__________ revenue
        $__________ operating cost
        Net: $__________ (loss)

Year 2: 85% ridership × $__________ = $__________ revenue
        Net: $__________ 

Year 3: 100% ridership × $__________ = $__________ revenue
        Annual surplus: $__________

Payback calculation:
Capital cost: $__________ million
Annual surplus (year 3+): $__________ million
Payback period: __________ ÷ __________ = __________ YEARS

Target: < 20 years
```

### 2.6 Environmental Impact Assessment Framework

**2.6.1 CO₂ Reduction Calculation**

```
Daily ridership (mature): __________ riders
× 2 trips/day = __________ trips/day
× 365 days = __________ annual trips
× 8 km average trip = __________ trip-km/year

Baseline (if traveled by car): 120 g CO₂/km
× __________ trip-km = __________ metric tons CO₂/year

With metro (30 g CO₂/km):
× __________ trip-km = __________ metric tons CO₂/year

CO₂ REDUCTION: __________ metric tons/year
= Planting __________ million trees
= Economic value (at $30/ton): $__________ million/year
```

**2.6.2 Air Quality Benefits**

Estimate particulate matter (PM2.5) reduction near line:
- [ ] Estimate baseline air quality
- [ ] Project 15-20% reduction in PM2.5 within 2 km
- [ ] Calculate health benefits (respiratory illness reduction)
- [ ] Monetize health benefits if possible

---

## PHASE 3: BUSINESS CASE & FUNDING (Months 25-36)

### 3.1 Business Case Development Checklist

Prepare comprehensive business case document including:

- [ ] Executive summary (2 pages)
- [ ] Urban context and need justification (5 pages)
- [ ] Design proposal with maps (10 pages)
- [ ] Financial model (with 3 scenarios) (5 pages)
- [ ] Environmental impact assessment (5 pages)
- [ ] Implementation plan and timeline (5 pages)
- [ ] Risk assessment and mitigation (5 pages)
- [ ] Management and procurement strategy (3 pages)

### 3.2 Funding Strategy Worksheet

**3.2.1 Identify Funding Sources**

```
Source                Amount        Timeline    Status
──────────────────────────────────────────────────────
Government budget     $________      __________  ☐ Confirmed
                                                 ☐ Proposed
                                                 ☐ Uncertain

Development bank      $________      __________  ☐ Applied
(World Bank, ADB)                                ☐ Pending
                                                 ☐ No approach

Climate finance       $________      __________  ☐ Eligible
(Green Fund, etc.)                               ☐ Applied
                                                 ☐ Not pursued

Real estate capture   $________      __________  ☐ Planned
(station development)                           ☐ Under study
                                                 ☐ No plan

PPP/Private sector    $________      __________  ☐ Interest shown
(operator, sponsors)                            ☐ Seeking interest
                                                 ☐ Not interested

Other (bonds, etc.)   $________      __________  ☐ Feasible
                                                 ☐ Studying
                                                 ☐ Not viable
──────────────────────────────────────────────────────
TOTAL FUNDING PLAN    $________      __________
```

### 3.3 Funding Gap Analysis

```
Total capital cost: $__________ million
Identified funding: $__________ million
FUNDING GAP: $__________ million (__________ %)

Gap closure strategy:
1. ☐ Seek additional government allocation
2. ☐ Reduce scope (shorter line, fewer stations)
3. ☐ Extend timeline (spread capital cost)
4. ☐ Pursue PPP/private investment
5. ☐ Explore climate/development finance
6. ☐ Implement value capture strategy
7. ☐ Delay start until funding available
```

---

## PHASE 4: COMMUNITY ENGAGEMENT & APPROVALS (Months 24-48)

### 4.1 Community Engagement Plan

**4.1.1 Engagement Phases**

| Phase | Timeline | Activities | Success Metrics |
|-------|----------|-----------|-----------------|
| **Awareness** | Months 12-18 | Briefings, media, website | 60% public aware |
| **Input** | Months 18-30 | Public meetings, surveys | 1000+ comments received |
| **Response** | Months 30-40 | Show how feedback shaped design | 70% feel heard |
| **Support** | Months 40-48 | Build coalition for approval | Political consensus |

### 4.2 Approval Checklist

Required government approvals (varies by country):

- [ ] Urban planning authority approval
- [ ] Environmental impact assessment approval
- [ ] Local/regional government authorization
- [ ] Transit regulatory approval (if separate)
- [ ] Land acquisition authority approval
- [ ] Financial/budget authority approval
- [ ] Safety & standards approval
- [ ] Parliamentary/congressional approval (if required)

---

## PHASE 5: DETAILED DESIGN & PROCUREMENT (Months 37-60)

### 5.1 Design Development Checklist

- [ ] 30% design completed and reviewed
- [ ] Preliminary cost estimates from design
- [ ] 60% design completed; cost refined
- [ ] Environmental permits on track
- [ ] Land acquisition strategy finalized
- [ ] 90% design completed
- [ ] Final cost estimate (within ±10%)
- [ ] Ready for procurement

### 5.2 Procurement Strategy

**5.2.1 Major Procurements Required**

```
Item                              Quantity  Est. Cost    Timeline
──────────────────────────────────────────────────────────────────
Rolling stock (trains)            __ sets   $__________  __ months
Signaling system (CBTC/ATO)       1 system  $__________  __ months
Power systems & substations       __ units  $__________  __ months
Construction (tunnels/structures) __ km     $__________  __ years
Civil works (stations, etc.)      __ items  $__________  __ years
Systems integration               1         $__________  __ months
Operations & maintenance          Contract  $__________  __ years
```

---

## PHASE 6: CONSTRUCTION & DELIVERY (Months 61-120)

### 6.1 Construction Milestones

```
Milestone                              Target Date    Status    % Complete
─────────────────────────────────────────────────────────────────────────
Construction contract awarded          __________     ☐        ____%
Major station excavation complete      __________     ☐        ____%
Tunnel boring complete (50%)           __________     ☐        ____%
Track installation 75% complete        __________     ☐        ____%
Signaling installation 50% complete    __________     ☐        ____%
Rolling stock arrival (50%)            __________     ☐        ____%
Systems integration testing begins     __________     ☐        ____%
Tunnel boring 100% complete            __________     ☐        ____%
Track installation 100% complete       __________     ☐        ____%
Rolling stock 100% delivered           __________     ☐        ____%
Full systems testing begins            __________     ☐        ____%
Safety certification obtained          __________     ☐        ____%
Line opening/inauguration              __________     ☐        ____%
```

### 6.2 Cost & Schedule Tracking

**6.2.1 Monthly Status Report Template**

```
Period: __________ to __________

Budget Status:
- Budget allocated: $__________ million
- Expenditures to date: $__________ million (____ %)
- Forecast final cost: $__________ million
- Variance: +$__________ or −$__________ million

Schedule Status:
- Milestones on track: ___ of ___
- Major delays: ____________________
- Recovery plan: ____________________

Key Issues:
1. ____________________________________________
   Risk level: High / Medium / Low
   Mitigation: ____________________________

2. ____________________________________________
   Risk level: High / Medium / Low
   Mitigation: ____________________________
```

---

## PHASE 7: OPERATIONS & RAMP-UP (Year 5+)

### 7.1 Opening Readiness Checklist

Before opening:
- [ ] All staff trained (operators, maintenance, management)
- [ ] Safety systems certified and tested
- [ ] Emergency response procedures established
- [ ] Ticketing/payment system operational
- [ ] Customer information systems ready
- [ ] Integration with existing transit complete
- [ ] Feeder bus routes established and running
- [ ] Marketing campaign launched (4 weeks pre-opening)

### 7.2 Ramp-Up Management

**7.2.1 Ridership Projection vs. Actual**

```
Year 1 Target: __________ riders/day (60% of mature)
Year 1 Actual: __________ riders/day
Variance: __________ % (__________ riders short or excess)
Analysis/Actions: _____________________________

Year 2 Target: __________ riders/day (85% of mature)
Year 2 Actual: __________ riders/day

Year 3 Target: __________ riders/day (100% mature)
Year 3 Actual: __________ riders/day
```

### 7.3 Operations Excellence Targets

During first 5 years, establish metrics:

- [ ] On-time performance: 98%+ (Taipei standard: 99.2%)
- [ ] System availability: 99%+ daily
- [ ] Customer satisfaction: 4.0+/5.0
- [ ] Safety record: Zero fatalities (industry standard)
- [ ] Cost per passenger-km: Competitive vs. existing transit

---

## KEY DOCUMENTS & REFERENCES

### Tools Referenced in This Checklist

| Tool | URL | When to Use |
|------|-----|-----------|
| **Design Tool** | circular-line-design-tool.html | Worksheet 2.1 (design parameters) |
| **Economic Model** | taipei-metro-economic-model.html | Worksheet 2.4-2.5 (costs & revenue) |
| **Capacity Analyzer** | taipei-metro-capacity-analyzer.html | Stress-test with your demand |
| **Accessibility Analyzer** | taipei-metro-accessibility-analyzer.html | Verify coverage (worksheet 2.1) |
| **Environmental Calculator** | taipei-metro-environmental-impact.html | Worksheet 2.6 (environmental benefits) |
| **Resilience Analyzer** | taipei-metro-resilience-analyzer.html | Risk assessment (phase 3) |

### Supporting Documents

| Document | Purpose |
|----------|---------|
| **DESIGN_PRINCIPLES.md** | Reference all design parameters and technical standards |
| **CASE_STUDIES_APPLIED.md** | See how Bangkok, Seoul, Mexico City, Singapore, Manila approached this |
| **CIRCULAR_METRO_ANALYSIS.md** | Deep technical analysis and global precedents |
| **QUICK_START_GUIDES.md** | Guidance for different user roles (planner path recommended) |

---

## NOTES FOR YOUR CITY

Use this section to record decisions, constraints, and rationales specific to your context:

```
City name: __________________________
Planning authority: __________________________
Preparation date: __________________________

Key constraints:
1. ___________________________________
2. ___________________________________
3. ___________________________________

Strategic advantages:
1. ___________________________________
2. ___________________________________
3. ___________________________________

Critical success factors:
1. ___________________________________
2. ___________________________________
3. ___________________________________

Stakeholder support level: High / Medium / Low
(Rate and note key supporters/opponents)

Next steps:
1. ___________________________________
2. ___________________________________
3. ___________________________________
```

---

## FINAL DECISION GATE: IS YOUR CITY READY?

Before committing resources, answer these questions:

**1. Urban fit:** Does circular topology make sense for your city's urban form?
   - [ ] Yes, strong fit
   - [ ] Moderate fit (with design optimization)
   - [ ] Weak fit (consider alternatives)

**2. Demand:** Is 200k+ daily ridership realistic?
   - [ ] Yes, confident projection
   - [ ] Marginal (175-200k, requires optimization)
   - [ ] Below threshold, risky

**3. Funding:** Is capital cost fundable?
   - [ ] Yes, pathway clear
   - [ ] Probably (need external financing)
   - [ ] Uncertain (requires additional work)

**4. Government:** Is political commitment likely for 10+ years?
   - [ ] Yes, strong support
   - [ ] Moderate, subject to elections
   - [ ] Weak or uncertain

**5. Timeline:** Can your city commit to 10-15 year delivery?
   - [ ] Yes, priority
   - [ ] Possible, secondary priority
   - [ ] No, other priorities first

**Decision:**
- **4-5 "Yes" answers:** Proceed with full feasibility study
- **2-3 "Yes" answers:** Proceed with feasibility, but address weak areas
- **0-1 "Yes" answers:** Not ready now; revisit in 5-10 years

---

**Document created October 2026 | Use alongside DESIGN_PRINCIPLES.md and interactive tools**
