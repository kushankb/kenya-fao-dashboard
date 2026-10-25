# Kenya FAO Policy Mapping Dashboard

An interactive dashboard for exploring Kenya's policy alignment with the FAO Global Roadmap.

## Features

- **10 FAO Domains**: Visualized as an interactive ring of official FAO Roadmap domain icons
- **129 Roadmap Actions**: Detailed breakdown by domain
- **2,322 Policy Linkages**: Linked to policy documents with source references
- **828 Targets**: Target, baseline, and target year data
- **Smart Search**: Find actions, policy linkages, or targets by keyword across all domains
- **Responsive**: Works on desktop and phones

## Domain Statistics

- **Clean Energy**: 18 actions, 16 unique policies (84 linkages), 56 targets
- **Crops**: 14 actions, 26 unique policies (159 linkages), 89 targets
- **Data**: 12 actions, 28 unique policies (103 linkages), 68 targets
- **Enabling Healthy Diets for All**: 11 actions, 29 unique policies (394 linkages), 71 targets
- **Fisheries and Aquaculture**: 10 actions, 21 unique policies (348 linkages), 120 targets
- **Food Loss and Waste**: 10 actions, 21 unique policies (285 linkages), 82 targets
- **Forests and Wetlands**: 14 actions, 16 unique policies (83 linkages), 66 targets
- **Inclusive Policies**: 15 actions, 41 unique policies (592 linkages), 122 targets
- **Livestock**: 10 actions, 26 unique policies (136 linkages), 92 targets
- **Soil and Water**: 15 actions, 36 unique policies (138 linkages), 62 targets

## How to Use

1. **Explore Domains**: Hover over a domain icon in the ring to see its statistics
2. **Drill Down**: Click on any domain icon to view its roadmap actions
3. **View Details**: Select a roadmap action to see associated targets and policy linkages
4. **Search**: Use the search tabs to find specific actions, linkages, or targets by keyword

## Data Source

FAO Kenya Policy Document Analysis. Last updated: October 2026.

Generated from `Database_Kenya_dashboard.xlsx` (included in this repo) via `build_data.py`,
which produces `dashboard_data.js`. Both policy linkages and targets join to roadmap actions
by **full description** (clean 1:1). To refresh: update the spreadsheet and re-run
`python3 build_data.py`.

### Notes

- The vast majority of policy linkages and targets resolve to a catalogued document with a
  clickable source link (FAOLEX / weblink). A small number do not: ~22 linkages reference 2
  documents not yet in the Policy Documents sheet, and ~19 targets reference 1 document that
  has no URL — these show the document name without a clickable link.
- Policy Actions has no `linkage type` / `policy instrument type` columns, so those badges do
  not appear on linkage cards (cosmetic only; `build_data.py` uses them automatically if added).

## Technical Details

- Built with React 18 and Tailwind CSS; domain ring uses the official FAO Roadmap icons (`icons/`)
- `@babel/standalone` pinned to `7.25.6` (classic JSX runtime) for in-browser transform
- No backend required - runs entirely in the browser
