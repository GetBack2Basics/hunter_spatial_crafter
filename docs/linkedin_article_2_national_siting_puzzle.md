# LinkedIn Long-Form Article (Part 2)

**Title:** From a Local Council Proposal to a National Evidence Base: How I Built AuraSiting Crafter to Solve the AI Siting Puzzle  
**Author:** George Chandeep Corea  
**Tags:** `#AIInfrastructure` `#EnergyTransition` `#DataCenters` `#SpatialData` `#NationalCabinet` `#RegionalDevelopment` `#CleanTech`  

---

A few months ago, I started a personal learning project with a simple question:  
*Can we use modern spatial data to objectively evaluate local infrastructure proposals before public money and grid capacity are committed?*

I began by looking at a local council industrial rezoning proposal in Lake Macquarie, testing whether claims about buildable land stood up once environmental setbacks, pipelines, and flood overlays were subtracted.

As I explored cloud-native spatial tools, something clicked. The pipeline ran so quickly that expanding the model across NSW—and then scaling it nationally across every state and territory—became entirely feasible.

I call this project **AuraSiting Crafter** (*The Australian Regional & AI Infrastructure Siting Engine*), and it has landed right as the national conversation reaches a turning point.

---

### The National Dilemma: Growth vs. Community & Grid Stability

Following the Prime Minister’s National Cabinet meeting, Australia has committed to legislating mandatory national standards for AI data centres by early 2027. The core challenge is straightforward:

* **Grid Protection**: We need massive digital compute, but data centres cannot push up household electricity bills or destabilise local grids.
* **Water Security**: Hyperscale cooling cannot compete with community drinking water.
* **Community Siting**: Facilities must respect acoustic buffers, local neighbourhoods, and environmental zones.

Meeting these standards requires moving away from static site marketing and subjective planning debates toward transparent, verifiable spatial evidence.

---

### How AuraSiting Crafter Works

Built as an independent, data-first project, the engine evaluates sites across four balanced priorities:

1. **Power & Former Industrial Assets (40%)**: Prioritising direct connection to high-voltage lines and retired coal-fired power station substations—delivering firm power where the grid can handle it.
2. **Sensitive Community Protection (25%)**: Applying an acoustic buffer model that excludes sites within 300 metres of residential areas, schools, and hospitals while maintaining manageable workforce commute distances.
3. **Recycled Water Circuits (20%)**: Focusing cooling demand exclusively on wastewater treatment plants and industrial recycled loops to protect potable water.
4. **True Net Developable Space (15%)**: Automatically stripping away riparian corridors, easements, and hazard overlays to identify real buildable ground.

---

### From Deep Compute to an Interactive "Map in a Box"

I didn't want the findings locked away in a specialist GIS system. The engine compiles the entire national analysis into an interactive, zero-dependency HTML document.

Anyone can open the report in a web browser, search candidate sites by street address or cadastral Lot/Plan, and use the **What-If Sandbox** to adjust ranking weights in real time—instantly seeing how site rankings change across Australia with zero server latency.

---

### Read the Technical Breakdown & Explore the Data

I have documented the complete engineering journey—including how the system queried 4.92 million spatial geometries in 200.6 seconds on Wherobots Cloud—in my partner technical blog:

* 🌐 **Interactive National Siting Dashboard**: [Explore the Live Report](https://github.com/GetBack2Basics/hunter_spatial_crafter/blob/main/runner/national_suitability_report.html)
* 📄 **Technical Data & Provenance Report**: [View Data Verification Audit](https://github.com/GetBack2Basics/hunter_spatial_crafter/blob/main/runner/data_verification_technical_report.html)
* 🛠️ **Open Source Project Repository**: [hunter_spatial_crafter on GitHub](https://github.com/GetBack2Basics/hunter_spatial_crafter)

I believe transparent spatial data can help bridge the gap between national AI ambition, grid reliability, and community trust. I welcome your thoughts and feedback in the comments below!

*For additional context on the policy debates surrounding the Commonwealth's data centre framework, listen to [The gaps in the prime minister's big AI speech](https://www.youtube.com/watch?v=pRgQ1pub2IY). This analysis examines the regulatory and infrastructure challenges Australia faces as it scales sovereign artificial intelligence.*
