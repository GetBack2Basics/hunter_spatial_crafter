# Draft Email to Wherobots Support & Billing Team

**To:** `billing@wherobots.com`, `support@wherobots.com`  
**Subject:** Request for Invoice Credit / Discount — Org ID `ltq5l3obgb` (Hunter Spatial Crafter Project & Platform Feedback)

---

### Email Body

Hi Wherobots Team,

I hope you’re having a great week!

I am reaching out regarding draft invoice **`INYXGP-DRAFT`** for **GetBack2Basics** (Organization ID: **`ltq5l3obgb`**), totaling **US$397.03** for the period of July 21 – August 3, 2026.

#### 1. Background & Project Context
Over the past few weeks, I’ve been actively testing and building a showcase project called **Hunter Spatial Crafter**—a spatial ETL and data center siting suitability benchmark using Wherobots Cloud, Apache Sedona, and Havasu/Iceberg tables across regional New South Wales datasets (Macquarie Coal Complex Transformation Precinct).

I have been thoroughly impressed with Wherobots' spatial processing power and Spatial SQL capabilities! In fact, I am currently preparing a **LinkedIn technical post / article** showcasing spatial ETL workflows on Wherobots Cloud, demonstrating how Apache Sedona and Wherobots make regional infrastructure siting fast, elegant, and scalable.

#### 2. The Learning Case & Invoice Spike
While setting up our developer environment and experimenting with the Wherobots MCP Server and interactive notebooks, an **Interactive General Purpose SU session** in `aws-us-west-2` was accidentally left running silently in the background over several days. 

Looking at the invoice breakdown:
- **Interactive SUs (`aws-us-west-2`)**: US$336.39 (277.84 SUs)
- **Interactive SUs (`aws-ap-south-1`)**: US$37.07 (29.07 SUs)
- **Automated Batch Jobs (`aws-us-west-2`)**: US$24.13

As you can see, our actual batch execution runs only consumed **$24.13**, while **89% of the invoice ($373.46)** was incurred due to an idle interactive cluster running during our initial developer setup.

#### 3. One-Time Credit / Discount Request
As a startup/independent developer using Wherobots for evaluating technology stack options and producing community content, this unexpected $397 billing blowout is a significant hit to our early-stage budget.

Could you please consider applying a **one-time goodwill credit or discount** to invoice `INYXGP-DRAFT` for the idle interactive compute time? We would deeply appreciate your support as we continue building and sharing our experiences with Wherobots in the spatial community.

#### 4. Product Feedback & Feature Request: Native Budget Guardrails
This setup experience highlighted a feature that would add tremendous value and safety for developer teams on Wherobots:

* **Hard Budget Caps & Spend Notifications**: A native workspace feature allowing users to set a monthly SU dollar limit (e.g., $50/month), sending an emergency email/SMS alert when spending reaches 80%, and optionally auto-pausing interactive clusters if the limit is exceeded.
* **Default Idle Auto-Stop Indicator**: Making auto-shutdown timeouts more prominent or defaulting interactive notebook/MCP sessions to a 5-minute hard shutdown.

Thank you very much for your time, consideration, and support. I look forward to hearing from you and sharing our Wherobots benchmark article with the community soon!

Best regards,

**Corey**  
GetBack2Basics  
Organization ID: `ltq5l3obgb`  
Email: `coreagc@gmail.com`
