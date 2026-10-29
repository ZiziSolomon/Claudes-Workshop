# Glossary & Technical Terminology Guide
## Consistent Language for Circular Metro Projects

---

## Introduction

This glossary defines terms used throughout the Taipei Metro Circular Line knowledge system. Use it to:
- Ensure consistent terminology across all communications
- Explain complex concepts to non-technical stakeholders
- Understand technical discussions with engineers and consultants
- Avoid miscommunication in planning meetings

Terms are organized by category.

---

## Part 1: Basic Circular Metro Concepts

### Circular Line (or Ring Line)
**Definition:** A rapid transit line that forms a complete or near-complete loop, connecting suburban areas without passing through downtown.

**Example:** Taipei Circular Line (15.4 km loop)

**Why it matters:** Enables suburb-to-suburb travel without downtown transfer, solving transportation problem that radial lines can't.

---

### Radial Line (or Spoke)
**Definition:** A rapid transit line that radiates from downtown to suburbs, like spokes on a wheel.

**Example:** Taipei Metro Lines 1, 2, 3, 4, 5, 6 (all radial)

**Complement vs. competition:** Radial and circular lines are complementary. Radial handles downtown convergence. Circular handles suburban distribution.

---

### Hub-and-Spoke Model
**Definition:** Traditional transit network design where downtown is the hub and suburbs are spokes.

**Characteristics:**
- All lines converge downtown
- Peak directional flow (AM inbound, PM outbound)
- Downtown stations become bottlenecks
- Suburb-to-suburb travel requires downtown transfer

**Limitation:** Doesn't serve post-2000 dispersed urban form (multiple employment centers, suburb-to-suburb commuting).

---

### Polycentric City (or Multi-Center Urban Form)
**Definition:** City with multiple business/employment centers distributed across the metro area, rather than single downtown.

**Examples:** Los Angeles, Bangkok, Mexico City, modern sprawling metros

**Why it matters for circular lines:** Polycentric cities need distributed transit network. Circular lines enable suburb-to-suburb connections in polycentric metros.

---

### Headway
**Definition:** Time interval between consecutive trains at a given location.

**Example:** "3-minute headway" = Train arrives every 3 minutes

**Why it matters:** Lower headway = More frequent service = Better passenger experience

**Typical ranges:**
- Peak: 2-4 minutes (frequent, no schedule-watching needed)
- Off-peak: 5-8 minutes (good service)
- Late night: 10-15 minutes (minimal service)

---

### Load Factor (or Crowding)
**Definition:** Ratio of actual passenger count to train capacity, expressed as percentage.

**Example:** "80% load factor" = Train is 80% full at peak

**Thresholds:**
- <50%: Underutilized (poor revenue)
- 50-80%: Optimal (profitable, comfortable)
- 80-100%: Crowded (acceptable for peak hour)
- >100%: Over-capacity (standing-room only, uncomfortable)

---

### Daily Ridership (or Daily Passenger Volume)
**Definition:** Total number of passenger trips on the line per 24-hour day.

**Example:** Taipei Circular Line: 320,000 daily riders

**How calculated:** (# passengers on train A) + (# passengers on train B) + ... = Daily total

**Why it matters:** Predicts revenue and determines viability.

---

### Catchment Area
**Definition:** Geographic area within walking distance of a transit line station, typically 1 km radius (15-minute walk).

**Why it matters:** Ridership comes primarily from catchment area. Poor catchment = Low ridership. Design must align with population density in catchment.

---

## Part 2: Automation & Technology Terms

### Driverless (or Unattended Train Operation)
**Definition:** Trains operate without on-board crew; controlled by automated systems.

**Full term:** GoA4 (Grade of Automation 4 - highest level)

**Examples:**
- Taipei Circular Line (100% driverless since 2020)
- Copenhagen Metro
- Paris Line 14

**Misconception:** "Driverless = Unmanned" — Wrong. Driverless trains have staff (control center, maintenance, customer service). They just don't have on-board drivers.

---

### GoA (Grade of Automation)
**Definition:** International standard (IEC 62290) defining automation levels for rail transit.

**Five levels:**
- **GoA1:** Fully attended (human operator controls train)
- **GoA2:** Semi-automatic (operator assists, automation backup)
- **GoA3:** Driverless (no on-board operator, automated train operation)
- **GoA4:** Unattended (no staff on train, fully automated)
- **GoA5:** (Proposed) No human intervention at any level

**For circular lines:** GoA4 is optimal (no on-board staff, controlled from central operations center)

---

### ATO (Automatic Train Operation)
**Definition:** System that automatically controls train speed, acceleration, braking, and station stops.

**What it does:**
- Maintains optimal speed between stations
- Performs precise station stops
- Adjusts for passenger load
- Responds to signaling commands

**How it works with CBTC:**
- CBTC tells ATO "next signal is green"
- ATO executes speed/braking to reach station safely
- Station dwell time optimized automatically

---

### CBTC (Communications-Based Train Control)
**Definition:** Modern signaling system using radio communication between train and track, replacing traditional fixed-block signals.

**Advantages:**
- Enables closer train spacing (higher frequency)
- More reliable than mechanical signals
- Supports real-time traffic management
- Foundation for automation (provides train location/velocity data to ATO)

**Enabling technology:** Essential for driverless trains. Allows system to know exactly where train is and control it precisely.

---

### Train Signaling
**Definition:** System that ensures safe train operation by controlling speed and spacing.

**Traditional (Fixed-Block):**
- Track divided into sections (blocks)
- One train per block only
- Permits 2-3 minute headway maximum
- Uses mechanical/electrical signals

**Modern (CBTC):**
- Continuous communication between train and control center
- Train location known precisely to meter
- Permits 90-120 second headway
- Uses radio signals, onboard equipment

**For circular lines:** CBTC is standard. Enables 3-minute headway achievable.

---

### Automation Payback Period
**Definition:** Time until cost savings from automation equal its additional capital cost.

**Example:** 
- Driverless costs $100M more upfront
- Saves $3-4M/year in operating costs
- Payback in 7-10 years

**Why it matters:** For short-term projects, traditional is cheaper. For long-term (20+ years), driverless is cheaper overall.

**For circular lines:** Payback typically 7-10 years, making it worthwhile for 20+ year operating horizon.

---

## Part 3: Financial & Economic Terms

### Payback Period
**Definition:** Years required for a project's cumulative operating profit to equal its capital investment.

**Formula:** Payback = Capital Cost ÷ Annual Operating Profit (year 3 onwards)

**Example:**
- Capital cost: $15 billion
- Annual profit year 3+: $80 million
- Payback: 15,000 ÷ 80 = ~19 years

**For infrastructure:** 15-25 years is typical and acceptable. Highways often 30+ years.

---

### Farebox Recovery Ratio
**Definition:** Percentage of operating costs covered by fare revenue.

**Formula:** Farebox Recovery = Annual fare revenue ÷ Annual operating cost

**Example:**
- Fare revenue: $152M/year
- Operating cost: $85M/year
- Recovery: 152 ÷ 85 = 178% (profitable!)

**Industry standards:**
- <70%: Requires subsidy (common in developing countries)
- 70-80%: Typical (most metros)
- 80%+: Strong performance
- 100%+: Profitable (rare, only high-demand metros)

**Taipei Circular:** ~150% (highly profitable, unusual)

---

### Operating Cost per Passenger-km
**Definition:** Annual operating expense divided by total passenger-kilometers traveled.

**Example:** If annual cost is $85M and passengers travel 2.5 billion km/year:
- Cost per km: $85M ÷ 2.5B = $0.034/km
- Cost per trip (8 km avg): $0.27

**Why it matters:** Shows efficiency. Lower = More efficient system.

---

### Capital Cost per km
**Definition:** Total project cost divided by line length.

**Range for circular lines:** $300M-600M per km

**Factors affecting cost:**
- **High:**
  - Dense urban tunneling ($700M+/km)
  - Expensive real estate acquisition
  - Deep underground (geological challenges)
  - Developed country labor costs

- **Low:**
  - At-grade or elevated ($250-400M/km)
  - Minimal land acquisition
  - Developing country labor costs
  - Simple geology

---

### Real Estate Value Capture
**Definition:** Monetizing the increase in property value adjacent to new transit, to help fund the transit project itself.

**Example:**
- Property value near station increases 20% after opening
- City captures 50% of value increase through:
  - Upzoning and selling development rights
  - Tax increment financing
  - Land value tax
  - Joint development agreements

**Potential:** Real estate value capture can fund 20-40% of circular line project.

---

### Mode Shift
**Definition:** Traveler switching from one transportation mode to another.

**Example:** Driver switching from personal car to metro transit

**For circular lines:** Key metric is automobile-to-transit mode shift.

**Typical assumptions:** 30-50% of suburban drivers would shift to metro if service provided (no downtown transfer required).

---

## Part 4: Urban Planning & Design Terms

### Station Spacing
**Definition:** Distance between consecutive stations along the line.

**Optimal for circular lines:** 1.2-1.6 km average

**Implications:**
- <1.0 km: Too frequent, reduces speed, increases dwell delays
- 1.2-1.6 km: Optimal balance of coverage and speed
- >2.0 km: Too sparse, reduces catchment area

---

### Accessibility (or Transit-Oriented Development)
**Definition:** Ability to reach transit station on foot or bicycle within reasonable time.

**Standard walking distance:** 1 km (15 minute walk at average pace)

**Pedestrian accessibility thresholds:**
- Excellent: <500m walk (5 min) — Captures 40-50% of catchment
- Good: 500-1,000m (10 min) — Captures 70-80%
- Acceptable: 1,000-1,500m (15 min) — Captures 85-90%
- Poor: >1,500m (20+ min) — Limited catchment

---

### Mixed-Use Development
**Definition:** Development combining residential, commercial, and sometimes office space in integrated project near transit station.

**Why near transit:** Transit access makes location valuable, justifying higher-density development.

**Benefit:** Mixed-use development generates more ridership (residents + workers + shoppers) than residential-only.

---

### Last-Mile Connectivity
**Definition:** Transportation from home/origin to transit station (first/last leg of journey).

**Modes:** Walking, cycling, feeder bus, ride-share

**For circular lines:** Depends on:
- Station accessibility (1 km walk-ability)
- Feeder bus network (connecting neighborhoods to stations)
- Bike infrastructure (bike parking, safe routes)
- Ride-share availability

**Design principle:** First/last mile must be competitive with driving directly to destination.

---

## Part 5: Environmental & Sustainability Terms

### Carbon Footprint (or CO₂ Emissions)
**Definition:** Total greenhouse gas emissions from a transportation mode, measured in CO₂ equivalent.

**Typical values (per passenger-km):**
- Car: 120 g CO₂/km (including production, maintenance, fuel)
- Diesel bus: 60 g CO₂/km
- Electric metro: 30 g CO₂/km (varies by electricity source)
- Taipei metro: ~20 g CO₂/km (hydro-heavy power supply)

**For circular lines:** 75% reduction vs. cars = Equivalent to planting 1-2 million trees annually.

---

### Mode Shift Impact
**Definition:** Environmental benefit from travelers switching from cars to transit.

**Calculation:**
- Current car commuters: X
- Switch to transit: Y%
- Daily car trips eliminated: X × Y
- CO₂ avoided: (X × Y) × Distance × Emissions-per-km

**Example:**
- 300,000 daily riders
- 70% from cars (210,000 trips)
- Average trip: 8 km
- Emissions avoided: 210,000 × 8 × 90 g = 151,000 kg CO₂/day

---

### Particulate Matter (PM2.5)
**Definition:** Fine air pollution particles (diameter <2.5 micrometers) that lodge in lungs.

**Health impact:** Associated with respiratory disease, cardiovascular disease, reduced life expectancy.

**Metro impact:** Transit reduces road congestion, reducing vehicle emissions, reducing PM2.5 near line.

**Typical reduction:** 15-20% PM2.5 reduction in corridor zone after metro opening.

---

### Life-Cycle Assessment (LCA)
**Definition:** Environmental analysis of a product or system from creation through end-of-life.

**For transit:** Includes:
- Manufacturing (rolling stock, track, stations)
- Operation (electricity, maintenance)
- End-of-life (recycling, disposal)

**Key metric:** Even with manufacturing impact, metro is much cleaner over 50-year operational life vs. cars.

---

## Part 6: Project Management & Implementation Terms

### Phased Opening
**Definition:** Dividing a long transit line into segments, opening each in sequence rather than all at once.

**Example:** Bangkok scenario in case studies:
- Phase 1 (Year 1-2): Segment A (12 km, 8 stations)
- Phase 2 (Year 3-4): Segment B (14 km, 9 stations)
- Phase 3 (Year 5-6): Segment C (8 km, 6 stations)

**Benefits:**
- Spreads capital cost across years
- Tests operations and demand gradually
- Builds business case with real data
- Reduces financial risk

---

### Project Phases (Typical 4-Phase Model)

1. **Planning & Feasibility (2 years)**
   - Demand studies, route selection, environmental assessment
   - Deliverable: Go/no-go decision

2. **Design & Engineering (2 years)**
   - Detailed design, environmental permits, procurement
   - Deliverable: Approved design, contracts signed

3. **Construction (4-5 years)**
   - Build track, stations, systems
   - Deliverable: Completed infrastructure

4. **Operations & Ramp-Up (5+ years)**
   - Operations commence, ridership grows
   - Deliverable: Mature profitable operations

---

### Critical Path
**Definition:** Sequence of project tasks that determine minimum completion time. Delay to critical path delays entire project.

**For circular lines:** Typical critical path:
- Design approval → Procurement → Tunneling/structures → Track → Systems integration → Testing → Opening

**Key:** Procurement and tunneling are usually longest duration tasks.

---

### Contingency (or Buffer)
**Definition:** Percentage of project budget reserved for unexpected costs.

**Typical range:** 15-20% of total capital cost

**Why needed:**
- Geological surprises (underground obstacles)
- Labor/material cost escalation
- Environmental remediation
- Design changes

**Best practice:** Build contingency into budget estimate, not hoped-for savings.

---

### Milestone
**Definition:** Significant event or achievement in project timeline.

**Examples:**
- "30% design complete"
- "Environmental permits approved"
- "Track installation begins"
- "First test run"
- "System certification"
- "Grand opening"

**Value:** Milestones provide checkpoints to verify progress and manage risk.

---

## Part 7: Ridership & Demand Forecasting Terms

### Origin-Destination (OD) Flow
**Definition:** Travel patterns showing where people begin trips (origin) and end (destination).

**Example:** "Morning peak shows 80,000 trips from suburbs to downtown, but only 5,000 suburb-to-suburb"

**Why it matters:** Circular lines are designed for suburb-to-suburb OD flows, which radial lines don't serve well.

---

### Peak Hour vs. Off-Peak
**Definition:** 
- **Peak hour:** Busiest hour of the day (typically 8-9 AM or 5-6 PM)
- **Off-peak:** Lower-demand hours (mid-day, evening, night)

**Peak concentration:** Ratio of peak hour riders to average hour riders

**Example:** 
- Peak hour: 40,000 riders
- Average hour: 12,500 riders
- Peak concentration: 40,000 ÷ 12,500 = 3.2x

**Design implication:** System must handle peak concentration. Design for peak hour, not average hour.

---

### Ramp-Up Curve (or Growth Trajectory)
**Definition:** Pattern of ridership growth from opening through maturity.

**Typical model:**
- Year 1: 60-70% of mature ridership (new system, building awareness)
- Year 2-3: 85-95% of mature (system becoming familiar)
- Year 5+: 100% (stable mature demand)

**Why gradual:** Behavioral change takes time. New transit users must change habits, businesses must adapt, land-use patterns evolve.

---

## Part 8: Network & System Terms

### Network Resilience (or System Robustness)
**Definition:** Ability of transit network to continue functioning under disruption or failure.

**Resilience metric:** Percent of potential trips still feasible if one line fails.

**Example:**
- Radial-only: 40% stranded if one line closes
- With circular line: 12% stranded (80% improvement)

**Why it matters:** Critical for emergency preparedness. Network with alternate routes survives disruption better.

---

### Interchange (or Transfer)
**Definition:** Point where two transit lines connect, allowing passengers to switch lines.

**Design considerations:**
- Physical proximity (ideally <100m walking distance)
- Fare integration (single ticket covers both lines)
- Schedule coordination (minimize wait time)
- Passenger information (clear signage)

**For circular lines:** 3-5 major interchanges with existing lines is optimal.

---

### Crowding Index (or Crowding Level)
**Definition:** Subjective measure of passenger comfort on train.

**Levels:**
- Level 1: Empty (uncomfortable, seems unpopular)
- Level 2: Seats available (comfortable)
- Level 3: Standing room (acceptable)
- Level 4: Crowded (uncomfortable, no personal space)
- Level 5: Packed (intolerable)

**Design target:** Level 2-3 at peak hour (seats for most, acceptable standing)

---

## Part 9: Cost-Related Terms

### Unit Cost per km (or Specific Cost)
**Definition:** Average capital cost per kilometer of line.

**Formula:** Total cost ÷ Line length = Cost per km

**Comparison:**
- Bus rapid transit: $10-50M/km
- Light rail: $50-150M/km
- **Circular metro: $300-600M/km**
- Subway: $500-1,000M/km

**Why circular metro is expensive:** Underground/elevated infrastructure, rolling stock, systems, stations.

---

### CAPEX (Capital Expenditure) vs. OPEX (Operating Expenditure)

**CAPEX:** One-time construction costs
- Examples: Tunneling, stations, vehicles, systems
- Year 0 (mostly) through Year 5
- Amortized over 25-30 year asset life

**OPEX:** Recurring annual operating costs
- Examples: Staff, electricity, maintenance, insurance
- Year 1 onwards indefinitely

**For circular lines:**
- CAPEX: $15B (typical 30 km line)
- OPEX: $80-100M/year

---

### Economic Feasibility
**Definition:** Whether a project's revenue can cover operating costs and achieve acceptable payback period.

**Feasibility test:**
- Payback period: <20 years? (generally acceptable)
- Farebox recovery: >70%? (sustainable)
- NPV (net present value): Positive?
- IRR (internal rate of return): >5-8%?

**For circular lines:** Typically feasible if daily ridership >200,000.

---

## Part 10: Quick Reference Table

| Term | Simple Definition | Example | Why It Matters |
|------|-------------------|---------|----------------|
| **Headway** | Time between trains | "3-minute headway" | Affects passenger convenience |
| **Load factor** | % of train capacity used | "80% load factor" | Indicates revenue performance |
| **Catchment** | Walking distance to station | "1 km radius" | Predicts ridership |
| **Mode shift** | Switch from car to transit | "40% of drivers switch" | Determines ridership and CO₂ savings |
| **Payback** | Years until profit = cost | "15-year payback" | Indicates financial viability |
| **Farebox recovery** | % of costs from fares | "85% recovery" | Indicates financial sustainability |
| **CBTC** | Modern signaling | Enables 3-min headway | Critical for automation |
| **ATO** | Automatic train control | Driverless operation | Reduces cost, improves consistency |
| **GoA4** | Full automation standard | Taipei Circular uses this | Industry standard, proven safe |
| **Mixed-use development** | Residential + commercial | Near stations | Increases ridership |
| **Resilience** | Network survives disruption | Circular provides alternate route | Critical for safety |
| **Phased opening** | Staged segment completion | Phase 1, 2, 3 openings | Spreads cost, tests operations |

---

## Quick Reference: Terms by Audience

### For City Council / Policy Makers
Focus on:
- Payback period
- Farebox recovery
- Environmental impact (CO₂, air quality)
- Job creation
- Economic development

### For Engineers & Technical Staff
Focus on:
- CBTC signaling
- ATO operation
- GoA4 automation
- Headway/capacity
- Load factor

### For Planners
Focus on:
- Catchment area
- Accessibility
- Mixed-use development
- Mode shift
- Interchange design

### For General Public
Focus on:
- Travel time (how much faster)
- Cost (how much cheaper than driving)
- Frequency (how often trains come)
- Environmental (how much cleaner)
- Jobs created

---

## Common Abbreviations Reference

| Abbreviation | Meaning | Context |
|---|---|---|
| **CBTC** | Communications-Based Train Control | Signaling |
| **ATO** | Automatic Train Operation | Automation |
| **GoA** | Grade of Automation | Automation level |
| **OD** | Origin-Destination | Demand analysis |
| **CAPEX** | Capital Expenditure | Budget planning |
| **OPEX** | Operating Expenditure | Budget planning |
| **NPV** | Net Present Value | Financial analysis |
| **IRR** | Internal Rate of Return | Financial analysis |
| **LCA** | Life-Cycle Assessment | Environmental analysis |
| **PM2.5** | Particulate Matter 2.5 micrometers | Air quality |
| **CO₂** | Carbon Dioxide | Emissions |
| **km** | Kilometer | Distance |
| **min** | Minute | Time |

---

## Using This Glossary Effectively

1. **In meetings:** When term is used, confirm understanding with definition
2. **In documents:** Include definition first time term is used
3. **For stakeholders:** Use simple definitions; reference technical definitions in appendix
4. **Consistency:** Use exact terms consistently across all project communications

---

**Document created October 2026 | Terminology guide for circular metro projects**
