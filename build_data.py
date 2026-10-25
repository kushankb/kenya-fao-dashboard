#!/usr/bin/env python3
"""Generate dashboard_data.js for Kenya from Database_Kenya_dashboard.xlsx.

Clean 4-sheet workbook. Both policy linkages and targets join to roadmap actions
by FULL DESCRIPTION (unique 1:1):
  - Roadmap Actions   -> backbone (domain, number, brief, full desc)
  - Policy Actions    -> policy linkages (join on col4 = roadmap full description)
  - Metrics           -> targets       (join on col3 = roadmap full description)
  - Policy Documents  -> document metadata (year, FAOLEX URL / weblink) by name

Schema mirrors the Denmark/Viet Nam dashboards so index.html is unchanged apart from branding.
"""
import json, openpyxl, datetime, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Database_Kenya_dashboard.xlsx")
OUT = "dashboard_data.js"

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)

def rows(name):
    return [r for r in wb[name].iter_rows(min_row=2, values_only=True)]

def s(v):
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.year
    return v

DOMAIN_ORDER = ["Data", "Livestock", "Crops", "Fisheries and Aquaculture",
                "Soil and Water", "Forests and Wetlands", "Clean Energy",
                "Food Loss and Waste", "Enabling Healthy Diets for All",
                "Inclusive Policies"]

# ---- Policy Documents lookup (by name) ----
pd_lookup = {}
for r in rows("Policy Documents"):
    name = s(r[0])
    if not name:
        continue
    faolex = s(r[6])   # FAOLEX URL
    weblink = s(r[7])  # Weblink
    pd_lookup[name] = {
        "document_link": faolex or weblink,
        "document_year": s(r[2]),
    }

# ---- Roadmap Actions backbone (keyed by full description) ----
actions_by_full = {}
domain_actions = {}
for r in rows("Roadmap Actions"):
    number = s(r[1])
    if not number:
        continue
    domain = s(r[0])
    full = s(r[3])
    action = {
        "number": number,
        "brief": s(r[2]),
        "long_description": full,
        "policies": [],
        "metrics": [],
        "policy_count": 0,
        "metric_count": 0,
    }
    actions_by_full[full] = action
    domain_actions.setdefault(domain, []).append(action)

# ---- Policy Actions -> policies (join by full description, col4) ----
unmatched_pa = 0
for r in rows("Policy Actions"):
    desc = s(r[0])
    if not desc:
        continue
    action = actions_by_full.get(s(r[4]))
    if action is None:
        unmatched_pa += 1
        continue
    doc = s(r[1])
    meta = pd_lookup.get(doc, {})
    action["policies"].append({
        "description": desc,
        "long_description": s(r[3]) or desc,
        "policy_document": doc,
        "document_link": meta.get("document_link", ""),
        "document_year": meta.get("document_year", ""),
        "linkage_type": "",       # not present in Morocco workbook
        "instrument_type": "",    # not present in Morocco workbook
        "page_number": s(r[2]),
    })

# ---- Metrics -> targets (join by full description, col3) ----
unmatched_m = 0
for r in rows("Metrics"):
    desc = s(r[0])
    if not desc:
        continue
    action = actions_by_full.get(s(r[3]))
    if action is None:
        unmatched_m += 1
        continue
    doc = s(r[1])
    meta = pd_lookup.get(doc, {})
    action["metrics"].append({
        "description": desc,
        "long_description": s(r[5]) or desc,
        "target": s(r[6]),
        "baseline": s(r[7]),
        "units": s(r[8]),
        "target_year": s(r[10]),
        "baseline_year": s(r[11]),
        "policy_document": doc,
        "document_link": meta.get("document_link", ""),
        "document_year": meta.get("document_year", ""),
        "page_number": s(r[4]),
    })

# ---- Assemble domains ----
present = [d for d in DOMAIN_ORDER if d in domain_actions]
for d in domain_actions:
    if d not in present:
        present.append(d)

domains = []
for dname in present:
    acts = domain_actions[dname]
    for a in acts:
        a["policy_count"] = len(a["policies"])
        a["metric_count"] = len(a["metrics"])
    unique_docs = set()
    for a in acts:
        for p in a["policies"]:
            if p["policy_document"]:
                unique_docs.add(p["policy_document"])
    domains.append({
        "name": dname,
        "actions": acts,
        "total_actions": len(acts),
        "unique_policies": len(unique_docs),
        "total_policies": sum(a["policy_count"] for a in acts),
        "total_metrics": sum(a["metric_count"] for a in acts),
    })

with open(OUT, "w", encoding="utf-8") as f:
    f.write("window.dashboardData = ")
    json.dump({"domains": domains}, f, ensure_ascii=False, indent=2)
    f.write(";\n")

# ---- Report ----
print(f"Wrote {OUT}")
tot_a = sum(d['total_actions'] for d in domains)
tot_p = sum(d['total_policies'] for d in domains)
tot_m = sum(d['total_metrics'] for d in domains)
print(f"Domains: {len(domains)} | Actions: {tot_a} | Policy linkages: {tot_p} | Targets: {tot_m}")
print(f"Unmatched policy actions: {unmatched_pa} | Unmatched targets: {unmatched_m}")
for d in domains:
    print(f"   {d['name']:35} A={d['total_actions']:3} P={d['total_policies']:3} "
          f"uP={d['unique_policies']:3} M={d['total_metrics']:3}")
