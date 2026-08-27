# LinkedIn Post: Wherobots Technical Guest Post Announcement

**Author:** George Chandeep Corea  
**Target Platform:** LinkedIn Feed Post & Article  
**Character Count:** 2,555 characters (Strictly compliant with LinkedIn's 3,000-character maximum feed limit)  
**Live Project:** [AuraSiting Crafter (hunter_spatial_crafter)](https://github.com/GetBack2Basics/hunter_spatial_crafter) | [Interactive National Report](https://national-suitability-report.vercel.app)  

---

### LinkedIn Feed Post Content (Ready to Publish)

I am honored to share our cloud spatial engineering journey on the official Wherobots technical blog: scaling AI data center suitability modeling from a local NSW precinct to 15.91 million national geometries.

What started as personal curiosity testing cloud spatial tools against a local industrial transition in Lake Macquarie quickly expanded into a nationwide engine evaluating 17 candidate brownfield hubs across all 8 Australian jurisdictions.

🌐 Ground-Truth Evidence for National AI Infrastructure
Australia is tackling a vital question: how do we scale energy-hungry AI compute without overloading regional power grids, straining drinking water catchments, or compromising community amenity?

The answer lies in open, auditable spatial evidence across 16 authoritative government portals.

⚡ 4 Key Technical Takeaways:
1. Massive Cloud Spatial Scale: Indexed 15.4M Geoscape parcels, 368k ABS meshblocks, 275k rail corridors, and 241k power grid vectors across the NEM and SWIS grids.
2. 85.2% Storage Compression: Compressed raw vector data from ~2.9 GB to ~430.7 MB with GeoParquet & Havasu (Spatial Iceberg), accelerating continental scans from 18.4s to 3.2s.
3. Sub-3-Second Distributed Joins: Automated ST_MakeValid repairs, 30m riparian buffers, and ST_Difference Net Developable Area (NDA) overlays in 2.4s using Apache Sedona.
4. Decoupled Architecture & ~$36 AUD Spend: By separating heavy geometry joins from lightweight scoring curves, our entire multi-week batch ETL across ~35 pipeline runs cost just US$24.13 (~$36 AUD / ~$1.03 per run).

Interactive What-If scenario simulations and custom weightings run 100% in-browser via DuckDB-WASM at $0.00 cloud compute cost.

🛡️ Practical Cost Management Lessons:
In the spirit of open engineering, we also share cloud cost governance insights: proactive programmatic teardowns (sedona.stop()) are essential to complement platform auto-shutdown safety nets.

A huge thank you to the Wherobots team for the invitation to share this work!

🚀 Explore the Project:
📖 Full Wherobots Blog: https://wherobots.com/blog/
⚡ Interactive Report (Zero-Cost): https://national-suitability-report.vercel.app
📁 GitHub Repo: https://github.com/GetBack2Basics/hunter_spatial_crafter
📖 Engineering Playbook: https://github.com/GetBack2Basics/CheatSheets/blob/main/wherobots_antigravity_playbook.md

I welcome feedback and discussion from planners, energy engineers, and spatial practitioners!

#Geospatial #SpatialSQL #ApacheSedona #Wherobots #DataCenters #AIInfrastructure #EnergyTransition #DuckDB #OpenData #DigitalTwin
