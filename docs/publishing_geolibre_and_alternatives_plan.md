# Data Publishing & Spatial Analytics Platform: GeoLibre Fork Architecture & Upstream Contribution Plan

## Executive Summary

This document outlines the architecture for publishing spatial datasets (e.g., Hunter Precinct planning and suitability models) using a **cleanly decoupled fork of GeoLibre** ([opengeos/GeoLibre](https://github.com/opengeos/GeoLibre)) deployed on a Unix server.

To maintain open-source best practices and allow every new feature to be contributed back to `opengeos/GeoLibre` via Pull Requests (PRs), the architecture strictly separates:
1. **Data & Pipeline Repository (`hunter_spatial_crafter`)**: Handles spatial ETL, suitability model generation, GeoParquet/PMTiles exports, and project-specific query definitions.
2. **Standalone Frontend Repository (`GeoLibre` Fork)**: A clean fork of `opengeos/GeoLibre` containing generic, modular, reusable GIS features (AI Assistant drawer, Remote SQL Engine connector, Query Catalog panel).
3. **Backend Gateway Service (`geolibre-spatial-gateway`)**: A lightweight API proxy running on the Unix server to manage Wherobots credentials, LLM API calls, and spatial query caching.

---

## 1. System Architecture & Component Separation

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    DECOUPLED REPOSITORY MODEL                                     │
├────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ 1. DATA & ETL PIPELINE         │ 2. GEOLIBRE FORK (STANDALONE)   │ 3. UNIX SERVER DEPLOYMENT      │
│ (hunter_spatial_crafter)       │ (github.com/your-org/GeoLibre) │ (Web & API Server)             │
├────────────────────────────────┼────────────────────────────────┼────────────────────────────────┤
│ • Sedona Spark Spatial ETL     │ • Clean fork of opengeos       │ • Nginx Web Server (GeoLibre)  │
│ • Spatial Suitability Models  │ • Modular Plugin Architecture  │ • FastAPI Gateway (Wherobots)  │
│ • Exports: GeoParquet/PMTiles  │ • NO hardcoded project data    │ • Cloud Data Hosting (Parquet) │
│ • JSON Query Catalog           │ • Submits PRs back to opengeos │ • Docker Compose orchestrator  │
└────────────────────────────────┴────────────────────────────────┴────────────────────────────────┘
```

### Flow Diagram

```
                        ┌─────────────────────────────────────────────────────────┐
                        │                   UNIX WEB SERVER                       │
                        │                                                         │
┌───────────────┐       │  ┌──────────────────┐             ┌──────────────────┐  │       ┌──────────────────────┐
│  Web Browser  │◄─────►│  │ Reverse Proxy    │────────────►│ Standalone       │  │       │  Wherobots Cloud API │
│  (End User)   │       │  │ (Nginx / Caddy)  │             │ GeoLibre App     │  │       │  (Sedona Engine)     │
└───────┬───────┘       │  └────────┬─────────┘             └──────────────────┘  │       └──────────▲───────────┘
        │               │           │                                             │                  │
        │               │           ▼                                             │                  │
        │               │  ┌───────────────────────────────────────────────────┐  │                  │
        └───────────────┼─►│ FastAPI Gateway Service                           │──┼──────────────────┘
                        │  │ - Wherobots Session & Query Proxy                 │  │
                        │  │ - AI Spatial LLM Agent (NL -> Spatial SQL)        │  │       ┌──────────────────────┐
                        │  │ - Dynamic Config & Query Catalog Provider         │──┼──────►│ LLM API (Gemini/OpenAI)│
                        │  └───────────────────────────────────────────────────┘  │       └──────────────────────┘
                        │                                                         │
                        │  ┌───────────────────────────────────────────────────┐  │
                        │  │ Static Data Path (/data/*.parquet, *.pmtiles)     │  │
                        │  └───────────────────────────────────────────────────┘  │
                        └─────────────────────────────────────────────────────────┘
```

---

## 2. Upstream Contribution Strategy for GeoLibre

To ensure every new feature added to GeoLibre can be easily upstreamed to `opengeos/GeoLibre`, all modifications will follow these design rules:

### Rule 1: Zero Hardcoded Domain Logic
GeoLibre core code will **never** contain dataset-specific schema names, table names, or hardcoded API endpoints for `hunter_spatial_crafter`. All capabilities will be parameter-driven via environment variables (`.env`) or runtime configuration files (`config.json`).

### Rule 2: Modular Topic Branches
Features are developed in isolated topic branches on your fork:
1. **`feature/ai-spatial-assistant`**:
   - A generic AI Chat drawer component.
   - Configured via `VITE_AI_ASSISTANT_ENDPOINT`.
   - Sends query history and current table schemas to any OpenAI/Gemini-compatible backend.
   - Includes "Apply SQL to Editor" and "Execute Query" actions.
2. **`feature/remote-sql-provider`**:
   - Extends GeoLibre's DuckDB-WASM engine interface with an abstraction layer: `ISqlEngineProvider`.
   - Adds a generic `RemoteApiSqlProvider` implementation that routes queries to an external REST endpoint returning GeoJSON or Apache Arrow buffers.
3. **`feature/query-catalog-panel`**:
   - A generic "Saved / Pre-built Queries" panel component.
   - Reads catalog items from a local JSON file or a remote configuration URL (`VITE_QUERY_CATALOG_URL`).

### Rule 3: Git Branch Management for PRs
```bash
# Workflow for adding and upstreaming a feature
git remote add upstream https://github.com/opengeos/GeoLibre.git
git fetch upstream

# Create clean topic branch from upstream main
git checkout -b feature/ai-spatial-assistant upstream/main

# Develop feature in isolation...
git commit -m "feat(ui): add AI Spatial Assistant chat drawer component"
git push origin feature/ai-spatial-assistant

# Open Pull Request against opengeos/GeoLibre main!
```

---

## 3. Data Integration & Backend Architecture

Since GeoLibre is kept clean and generic, `hunter_spatial_crafter` connects to GeoLibre strictly as a data provider:

### A. Dataset Publishing Pipeline
1. `hunter_spatial_crafter` executes spatial ETL & suitability models.
2. Output files are published to the web server's static data directory (or S3/GCS bucket):
   - `/data/macquarie_constraints.parquet`
   - `/data/nsw_hydrography.pmtiles`
   - `/data/datacenter_suitability.parquet`
3. Generate a `catalog.json` file defining pre-built queries:
   ```json
   {
     "title": "Hunter Spatial Precinct Planning",
     "queries": [
       {
         "id": "macquarie-nda",
         "name": "Net Developable Zone (Macquarie)",
         "description": "Calculates available developable land after removing environmental & pipeline buffers.",
         "sql": "SELECT *, ST_Area(geometry) as area_sqm FROM read_parquet('https://your-domain.com/data/macquarie_constraints.parquet') WHERE constraint_type = 'NONE'",
         "engine": "duckdb-wasm"
       },
       {
         "id": "datacenter-siting-sedona",
         "name": "National Datacenter Siting Benchmark (Sedona Engine)",
         "description": "Multi-state spatial join across transmission grid & flood hazard zones.",
         "sql": "SELECT precinct_id, suitability_score FROM datacenter_suitability WHERE power_proximity_km < 2.0 AND flood_risk = 0",
         "engine": "wherobots-cloud"
       }
     ]
   }
   ```

### B. Backend Gateway (`geolibre-spatial-gateway`)
A separate, minimal FastAPI repository that handles sensitive credentials and API proxying:
- `POST /api/v1/query/wherobots`: Receives spatial SQL, executes against Wherobots Cloud API using `WHEROBOTS_API_KEY`, handles timeout & session cleanup, returns GeoJSON/Arrow.
- `POST /api/v1/ai/chat`: Accepts user prompt + active dataset schemas, queries LLM (Gemini/OpenAI) using `LLM_API_KEY`, returns generated Spatial SQL + narrative explanation.
- `GET /api/v1/catalog`: Serves the `catalog.json` created by `hunter_spatial_crafter`.

---

## 4. Unix Server Deployment Setup

### Directory Structure on Unix Server
```
/opt/spatial-platform/
├── geolibre/               # Git clone of your GeoLibre fork (built static SPA)
├── gateway/                # Dockerized FastAPI service (Wherobots/LLM Proxy)
├── data/                   # Static GeoParquet, PMTiles, COGs exported from ETL
└── docker-compose.yml      # Container orchestration
```

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  # Nginx serving the compiled GeoLibre static frontend + static spatial data
  web-frontend:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./geolibre/apps/geolibre-desktop/dist:/usr/share/nginx/html
      - ./data:/usr/share/nginx/html/data
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    restart: always

  # FastAPI gateway proxying Wherobots & AI calls
  backend-gateway:
    build: ./gateway
    environment:
      - WHEROBOTS_API_KEY=${WHEROBOTS_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - CATALOG_CONFIG_PATH=/app/data/catalog.json
    volumes:
      - ./data:/app/data:ro
    ports:
      - "8000:8000"
    restart: always
```

---

## 5. Comparison Matrix: Standalone Fork vs Other Options

| Feature | Standalone GeoLibre Fork | Custom React Portal | Streamlit App |
| :--- | :--- | :--- | :--- |
| **Separation of Concerns** | **Perfect** (Clean GIS repo) | High | Low (All Python) |
| **Open Source Contribution** | **Direct PRs to `opengeos`** | None (Custom codebase) | None |
| **Deployment Model** | Docker SPA + Nginx | Docker SPA + Nginx | Docker Python Container |
| **Maintenance & Upstream Sync** | Standard Git Remote tracking | Full ownership | Full ownership |
| **User Query Capabilities** | Local DuckDB + Wherobots | Custom SQL editor | Custom SQL input box |

---

## 6. Implementation Roadmap

1. **Step 1: Setup GeoLibre Fork Repository**
   - Fork `opengeos/GeoLibre` on GitHub.
   - Verify static web build workflow (`npm run build`).

2. **Step 2: Implement Feature Branches for Upstream PRs**
   - Branch `feature/query-catalog-panel`: Build generic catalog component.
   - Branch `feature/ai-spatial-assistant`: Build generic AI chat drawer.
   - Branch `feature/remote-sql-provider`: Build generic remote SQL execution provider.

3. **Step 3: Build Gateway Service & Data Exporter**
   - Create minimal FastAPI gateway container for Wherobots & LLM proxying.
   - Configure `hunter_spatial_crafter` to export GeoParquet/PMTiles and `catalog.json`.

4. **Step 4: Deploy & Verify on Unix Server**
   - Deploy Docker Compose environment on Unix server with SSL certificate.
   - Test pre-built queries, ad-hoc DuckDB queries, AI spatial chat, and Wherobots cloud query execution.
   - Submit Pull Requests to `opengeos/GeoLibre` for new features!
