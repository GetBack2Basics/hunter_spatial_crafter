---
name: wherobots-spatial-sql
description: Expert guidance on Wherobots Cloud, SedonaContext, Spatial SQL queries, and the Wherobots MCP Server.
---
# Wherobots Spatial SQL & MCP Skill

This skill provides guidelines and best practices for writing Wherobots Spatial SQL, initializing `SedonaContext`, executing spatial ETL workflows, and configuring the Wherobots MCP Server.

## 1. Sedona & Wherobots Context Initialization
Always initialize the `SedonaContext` to compile spatial SQL functions:
```python
from sedona.spark import *
spark = SedonaContext.create(SedonaContext.builder().getOrCreate())
```

## 2. Configuring the Wherobots MCP Server
To configure the Wherobots MCP server manually in your editor:
1. Open the Command Palette and run **MCP: Add Server**.
2. Choose **HTTP (HTTP or Server-Sent Events)**.
3. Use the URL: `https://api.cloud.wherobots.com/mcp/`
4. Set the name to `wherobots-mcp-server`.
5. Add your Wherobots API Key in `mcp.json` headers:
   ```json
   "headers": {
     "x-api-key": "<YOUR_WHEROBOTS_API_KEY>"
   }
   ```

## 3. Spatial SQL Best Practices
- **CRS Reprojections**: Ensure geometries are in a projected coordinate system (e.g., `EPSG:7856` GDA2020 / MGA Zone 56) before executing metric buffers (`ST_Buffer`) or calculating area (`ST_Area`). Use `ST_Transform(geom, 'EPSG:4326', 'EPSG:7856')`.
- **Prevalent Functions**:
  - `ST_Point(x, y)`: Construct points from coordinates.
  - `ST_Buffer(geom, distance)`: Buffer geometries in coordinate units.
  - `ST_Contains(a, b)`, `ST_Intersects(a, b)`: Perform spatial predicate checks.
  - `ST_Area(geom)`: Computes metric or degree area.

## 4. Resource Management
- **Tiny Runtime**: The Wherobots MCP server runs on a Tiny runtime by default. Sessions terminate after 5 minutes of inactivity.
- **Stopping Server**: Stop the server via **MCP: List Servers** -> **Stop Server** when not active to minimize Spatial Unit (SU) consumption.
