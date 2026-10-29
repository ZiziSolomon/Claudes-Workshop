# Taipei Metro Circular Line: An Interactive Exploration

This project contains a comprehensive collection of interactive tools and analyses exploring the Taipei Metro Circular Line and the broader Taipei Metro system.

## 📋 Contents

### Interactive Tools

1. **taipei-metro-circular.html** — *Static Information Map*
   - Clean, gradient-themed visualization of the Circular Line
   - 14 stations arranged in a circular layout
   - Key statistics: length, capacity, opening date
   - Timeline of development from planning to present
   - **Best for:** Quick reference and aesthetic overview

2. **taipei-metro-interactive.html** — *Interactive Explorer*
   - Modern dark-theme interface with animated train
   - Real-time train movement around the circular route
   - Hover-interactive station details
   - Comprehensive line characteristics and fleet information
   - **Best for:** Learning about the system and its operations

3. **taipei-metro-simulator.html** — *Transit Operations Simulator*
   - Real-time simulation of train movements, passenger flow, and system efficiency
   - Adjustable parameters: simulation speed, train count, dwell time, passenger demand
   - Live metrics: headway, capacity utilization, efficiency rating
   - **Controls:**
     - Simulation Speed: 1x (real-time) to 30x (accelerated)
     - Active Trains: 5-17 (currently 17 operational)
     - Station Dwell Time: 20-60 seconds
     - Passenger Demand: Low, Normal, High, Peak Hours
   - **Best for:** Understanding transit operations and how variables interact

4. **taipei-metro-full-system.html** — *Complete Network Map*
   - Visualization of all 6 lines (Red, Green, Blue, Brown, Orange, Circular)
   - Major interchange stations highlighted
   - Line characteristics and system-wide statistics
   - **Best for:** Understanding how the Circular Line integrates with the full network

5. **taipei-metro-station-finder.html** — *Interactive Station Search*
   - Search stations by name (English or Chinese)
   - Filter by metro line
   - Station codes, native language names, and line affiliations
   - **Best for:** Finding specific stations and their details

### Reference Materials

6. **CIRCULAR_METRO_ANALYSIS.md** — *Comprehensive Global Analysis*
   - Examines circular line topology worldwide
   - Case studies: Moscow, Paris, London, Beijing, Shanghai, Taipei
   - Advantages and disadvantages of circular topology
   - Why automation (driverless operations) suits circular lines
   - Design framework for optimal circular line parameters
   - Future projections for multi-ring systems
   - **Reading time:** 15-20 minutes
   - **Best for:** Understanding the bigger picture of circular transit

7. **taipei-metro-data.json** — *Complete System Database*
   - Structured data for all 6 lines and 107 stations
   - Detailed Circular Line specifications
   - Fleet information from Hitachi Rail Italy
   - Historical dates and current metrics
   - Interchange and future expansion plans
   - **Best for:** Data analysis and system integration

8. **README_TAIPEI_METRO.md** (this file)
   - Project overview and navigation guide

## 🎯 Key Facts: Taipei Circular Line

| Metric | Value |
|--------|-------|
| **Opened** | January 31, 2020 |
| **Current Stations** | 14 |
| **Track Length** | 15.4 km |
| **Configuration** | Complete circular loop (phase 1) |
| **Operator** | New Taipei Metro Corporation |
| **Fleet Size** | 17 trains × 4 cars |
| **Automation Level** | GoA 4 (Unattended Train Operation) |
| **Manufacturer** | Hitachi Rail Italy (SiRa platform) |
| **Headway (Peak)** | 2-3 minutes |
| **Headway (Off-peak)** | 5-8 minutes |
| **Service Hours** | 6:00 - 23:30 |
| **Daily Ridership** | ~320,000 (estimated 2026) |
| **On-time Performance** | 99.2% |
| **System Design Life** | 100+ years |

## 🚇 The Circular Line Concept

The Taipei Metro Circular Line represents a modern approach to urban transit:

### Why Circular?

**Traditional metro systems** use radial lines converging downtown:
- ✓ Efficient for downtown-centric cities
- ✗ Concentrates congestion at center
- ✗ Suburban-to-suburban travel requires downtown transfer

**Circular systems** distribute capacity around the periphery:
- ✓ Reduces downtown congestion
- ✓ Enables direct peripheral-to-peripheral travel
- ✓ Supports polycentric urban growth
- ✗ Longer travel times for some routes
- ✗ Harder to optimize for peak-hour directionality

Taipei's Circular Line connects New Taipei's suburban areas directly to Taipei without forcing all traffic through downtown, complementing the existing radial Red, Green, and Blue lines.

### Why Driverless?

The Circular Line is **100% driverless** — the first major metro system to operate at full scale without crews. This works particularly well for circular topology because:

1. **Symmetric Operations** — No need to optimize one direction over another; automation provides consistency everywhere
2. **Headway Precision** — Maintains exact 2-3 minute headways ±5 seconds, impossible with crew-operated trains
3. **Cost Efficiency** — Crew costs eliminated; payback period ~7-10 years for this line length
4. **Future-Proofing** — Designed for 100+ year lifespan; automation will only improve

## 🎮 Using the Tools

### For System Overview
1. Start with **taipei-metro-circular.html** for beautiful, clear information
2. Then explore **taipei-metro-full-system.html** to see integration
3. Read the key facts above

### For Learning Transit Operations
1. Open **taipei-metro-simulator.html**
2. Start a simulation with default settings
3. Experiment: increase train count, adjust demand, change speed
4. Notice how headway, capacity, and efficiency metrics interact

### For Detailed Analysis
1. Read **CIRCULAR_METRO_ANALYSIS.md** for global context
2. Check **taipei-metro-data.json** for complete specifications
3. Review the automation and fleet details

### For Specific Information
1. Use **taipei-metro-station-finder.html** to search for stations
2. Look up codes and line connections
3. Find transit information for specific areas

## 📊 System Statistics

**Full Taipei Metro Network (2026):**
- **Total Lines:** 6 (Red, Green, Blue, Brown, Orange, Circular)
- **Total Stations:** 107
- **Total Network:** 128.2 km
- **Daily Ridership:** 2.1 million
- **Annual Ridership:** 766.5 million

**Circular Line Snapshot:**
- **Lines Connected:** Primary connector between New Taipei and Taipei
- **Major Interchanges:** Taipei Main Station, Songshan, Nanjing Fuxing
- **Capacity:** 480,000 passengers/day designed capacity
- **Efficiency:** 99.2% on-time since opening (Feb 2020 - Oct 2026)

## 🔮 Future Expansion

The Circular Line is planned for expansion:
- **Phase 1 (Complete):** 14 stations, 15.4 km (opened 2020)
- **Phase 2 (2027-2030):** +8-10 stations
- **Full Circle (Target 2030):** ~30 km, 25+ stations

When complete, the full circle will provide comprehensive coverage around the Taipei metropolitan area, with multiple branches and connections to all existing lines.

## 🛠️ Technical Stack

These tools are built with:
- **HTML5 / CSS3 / JavaScript** — Pure web standards, no dependencies
- **SVG Graphics** — Scalable vector visualization
- **Responsive Design** — Works on desktop, tablet, mobile
- **Open Data** — All tools use publicly available Taipei Metro information

No external libraries required. All tools can be opened directly in any modern web browser.

## 📚 Data Sources

- Taipei Rapid Transit Corporation (TRTC) official statistics
- New Taipei Metro Corporation press releases and reports
- Hitachi Rail Italy technical specifications for SiRa platform
- Taiwan Ministry of Transportation official data
- Published performance reports (2020-2026)

## 🎓 Learning Outcomes

Using these tools, you'll understand:

1. **How circular metro topology differs from radial design**
2. **Why driverless automation suits circular lines**
3. **How Taipei's system fits into global transit evolution**
4. **Real-time operations metrics and system performance**
5. **Future trends in automated, distributed transit networks**

## 🌍 Global Context

The Taipei Circular Line is part of a global trend:

- **Moscow** has pioneered circular design with the famous Ring Line (1952)
- **Beijing** operates 3 concentric rings, proving the multi-circle concept
- **Shanghai** built a massive outer ring (32.5 km, 21 stations)
- **Taipei** adds the first fully-driverless circular line at scale

This project explores what makes Taipei's approach significant: it combines proven circular topology with cutting-edge automation technology, creating a model that other cities worldwide will likely study and replicate.

## 💡 Key Insights

1. **Circular lines solve a different problem than radial lines** — they're optimized for distributed, polycentric city growth, not downtown concentration.

2. **Driverless automation isn't just cost-cutting** — it fundamentally changes what's operationally optimal. For circular lines, it enables perfect consistency everywhere.

3. **The Taipei Circular Line proves driverless rapid transit works at full scale** — with 320,000 daily riders and 99.2% on-time performance since 2020.

4. **Future metros will likely use hybrid topologies** — combining radial lines (for downtown focus) with circular lines (for peripheral distribution).

---

## 📖 How to Navigate

- **Quick Overview?** → Open `taipei-metro-circular.html`
- **Want to Play?** → Open `taipei-metro-simulator.html`
- **Looking for Deep Knowledge?** → Read `CIRCULAR_METRO_ANALYSIS.md`
- **Need Specific Data?** → Check `taipei-metro-data.json`
- **Searching for a Station?** → Use `taipei-metro-station-finder.html`
- **See Everything Together?** → View `taipei-metro-full-system.html`

---

**Built October 2026 | Taipei Metro Data Current Through Q3 2026**

*All tools are open-source and use publicly available data. For current information, visit the official Taipei Rapid Transit Corporation and New Taipei Metro Corporation websites.*
