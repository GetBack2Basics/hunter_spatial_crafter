# Next Steps: Sensitive Receptor Scoring, PM Energy Analysis & GeoLibre AI Platform

## 1. Social & Sensitive Receptor Spatial Scoring Framework

To ensure responsible AI infrastructure deployment, candidate data center sites will be evaluated against sensitive community receptors to prevent acoustic, thermal, electromagnetic, and visual conflicts.

### A. Receptor Classes & Setback Standards

| Receptor Category | Included Facilities / Datasets | Regulatory / Environmental Guideline | Target Setback & Buffer |
| :--- | :--- | :--- | :--- |
| **Education & Early Childhood** | Primary & Secondary Schools, Preschools, Child Care Centers | NSW EPA Noise Policy for Industry / Child Safety Guidelines | Minimum 500m acoustic buffer zone |
| **Healthcare Facilities** | Public & Private Hospitals, Emergency Care, Aged Care Homes | NSW Health Infrastructure Acoustic Standards (24/7 low-frequency noise limits) | Minimum 500m setback; 1.0km optimal |
| **Residential Density** | ABS Meshblocks (Residential), SA1 Urban Center Boundaries | Local Environmental Plan (LEP) Buffer Controls & Amenity Guidelines | Sigmoidal spatial decay starting at 300m |
| **Workforce Accessibility** | ABS SA2 Population & Employment Hubs | Urban & Regional Transport Commute Modeling | 1.5km to 5.0km optimal commute band |

### B. Multi-Criteria Sigmoidal Spatial Decay Model

The planned sensitive receptor scoring metric will use a continuous sigmoidal penalty and workforce decay function:

$$S_{\text{sensitive}}(d) = \frac{1}{1 + e^{-k (d - d_0)}} \times \psi_{\text{workforce}}(d)$$

Where:
- $d$: Shortest distance from candidate parcel boundary to nearest sensitive receptor ($\text{meters}$).
- $d_0 = 500\text{m}$: Critical acoustic and setback compliance threshold.
- $k = 0.008\text{m}^{-1}$: Sigmoidal steepness parameter.
- $\psi_{\text{workforce}}(d)$: Workforce commute accessibility modifier ($1.0$ for $1.5\text{km} \le d \le 5.0\text{km}$, decaying slightly for $d > 5.0\text{km}$).

```
Distance Band (d)     Sensitivity Score    Land-Use Designation
-----------------------------------------------------------------------------------
d < 300m              0.00                 CRITICAL EXCLUSION (High Noise / EMF Hazard)
300m <= d < 500m      0.25 - 0.50          BUFFER PENALTY (Requires Acoustic Barrier Wall)
500m <= d < 1.5km     0.80 - 1.00          COMPLIANT BUFFER (Ideal Noise Compliance)
1.5km <= d < 5.0km    1.00                 OPTIMAL WORKFORCE & COMMUNITY BALANCE
d >= 5.0km            0.60 - 0.90          REMOTE (Increased Workforce Commute)
```

---

## 2. National Cabinet & PM Speech: AI Energy & Water Data Analysis

In response to the Prime Minister's address and the National Cabinet debate regarding AI data center power demand and regional energy grid security ([AFR August 2026](https://www.afr.com/politics/federal/queensland-sets-up-national-cabinet-showdown-over-ai-data-centre-power-20260823-p60qqg)), this planned spatial framework will provide regulators, utilities, and the public with transparent empirical data.

### A. Empirical Spatial Analysis Modules for Policy & Regulatory Transparency

1. **Substation Headroom & Transmission Grid Co-location**:
   - Will evaluate proximity to 132kV, 330kV, and 500kV bulk transmission lines and substations.
   - Will highlight candidates located adjacent to coal-fired power stations undergoing retirement (e.g. Latrobe Valley, Collie, Gladstone, Hunter Valley) to utilize existing heavy transmission infrastructure without triggering expensive grid upgrades.
2. **Renewable Energy Zone (REZ) & Firming Alignment**:
   - Will map candidates against state Renewable Energy Zones (REZ) and firming assets (Pumped Hydro Energy Storage, Big Batteries / BESS, and Gas Peakers) to evaluate 24/7 clean energy matching.
3. **Potable Water Protection vs. Recycled Water Cooling**:
   - Will restrict cooling water supply strictly to Wastewater Treatment Plants (WWTW) and industrial recycled loops, enforcing 0 points for sites dependent on potable drinking water reserves or vulnerable river aquifers.

### B. Regulatory Compliance & Grid-Readiness Rating Matrix

```
Rating Tier             Grid & Water Criteria                                               Regulatory Status
--------------------------------------------------------------------------------------------------------------------
TIER 1: GRID-READY      Co-located with retired thermal plant / REZ; WWTW recycled water     Fast-Track Eligible
TIER 2: CONDITIONAL     < 2km to 330kV transmission; requires BESS firming storage          Standard Assessment
TIER 3: CONSTRAINED     High grid congestion region or reliant on potable water reserves    High Regulatory Scrutiny
```

---

## 3. GeoLibre Open-Source AI Spatial Platform Integration

To allow the public and decision-makers to explore these spatial models interactively, `hunter_spatial_crafter` will integrate directly with [opengeos/GeoLibre](https://github.com/opengeos/GeoLibre).

### A. Cloud Architecture on Google Cloud Platform (GCP)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                GOOGLE CLOUD PLATFORM (GCP)                              │
│                                                                                         │
│   ┌────────────────────────────────┐                 ┌──────────────────────────────┐   │
│   │ Google Cloud Storage (GCS)     │                 │ GCP Cloud Run (Serverless)   │   │
│   │                                │                 │                              │   │
│   │ • GeoParquet Suitability Data  │◄────────────────┤ • FastAPI Spatial AI Proxy   │   │
│   │ • PMTiles Vector Layers        │ (Direct HTTP)   │ • Scale-to-Zero Container    │   │
│   │ • Static GeoLibre App UI       │                 │ • Gemini & OpenRouter Client │   │
│   └───────────────▲────────────────┘                 └──────────────▲───────────────┘   │
└───────────────────┼─────────────────────────────────────────────────┼───────────────────┘
                    │                                                 │
                    │ static assets & byte-range queries              │ Prompts & AI SQL
                    ▼                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                END-USER WEB BROWSER                                     │
│                                                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ GeoLibre Web Application (Free Web Platform)                                    │   │
│   │                                                                                 │   │
│   │  ┌─────────────────────────────┐           ┌─────────────────────────────────┐  │   │
│   │  │ Client-Side DuckDB-WASM     │           │ AI Spatial Chat Drawer          │  │   │
│   │  │ (Zero-Cost In-Browser SQL)  │           │ (Free Tier + BYOK OpenRouter)   │  │   │
│   │  └─────────────────────────────┘           └─────────────────────────────────┘  │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### B. Shared Cloud Data Storage Architecture (Wherobots & GeoLibre Integration)

Rather than maintaining separate file servers or copying data onto local web server disk storage, GeoLibre and Wherobots will share the exact same cloud-native dataset repository:

1. **Zero-Duplication Central Data Layer**:
   - Wherobots Cloud (Apache Sedona Spark) will output suitability modeling layers directly into a central Google Cloud Storage (GCS) / S3 bucket as **GeoParquet** and **PMTiles**.
   - GeoLibre will query these exact same files in GCS without needing any dataset conversion or server duplication.

2. **HTTP Range-Request Querying**:
   - GeoLibre’s in-browser DuckDB-WASM engine will fetch only the required byte ranges and spatial row groups via HTTP range requests (`read_parquet('https://storage.googleapis.com/.../datacenter_candidates.parquet')`).
   - This eliminates the need to download large files to the client or maintain expensive local web server NVMe storage drives.

3. **Cloud-Native Storage Tradeoff Analysis**:

```
Architecture Model         Data Sync / Duplication    Storage & Server Cost        Scalability
---------------------------------------------------------------------------------------------------------
Shared Cloud Storage (GCS) Zero Duplication (Unified)  Near-Zero (~$0.02/GB/mo)     Infinite Public Scale
Local Web Server Storage   High Duplication Needed     Expensive Server Disks       Constrained by VM I/O
```

### C. Free Tier & OpenRouter Bring-Your-Own-Key (BYOK) Model

Inspired by [GetBack2Basics/LivePersonaCrafter](https://github.com/GetBack2Basics/LivePersonaCrafter), GeoLibre will provide a dual-model LLM access tier:
- **Free Default Tier**: Powered by Google Cloud Gemini API (hosted on Cloud Run), allowing the public to ask natural language questions for free without creating accounts.
- **OpenRouter BYOK Tier**: Users will be able to enter their own OpenRouter API key directly in the GeoLibre settings drawer to unlock premium or specialized models (e.g., Claude 3.5 Sonnet, GPT-4o, DeepSeek-R1, Llama 3) for advanced spatial reasoning.

### D. Planned Conversational AI Queries ("Ask AI")

- *"Show me all candidate sites in NSW within 2km of 330kV transmission lines that are at least 1km away from schools and child care centers."*
- *"Which sites in Latrobe Valley or Gladstone score highest for recycled water availability without impacting residential meshblocks?"*
- *"Find data center parcels co-located within Renewable Energy Zones that have over 15 hectares of developable land."*
