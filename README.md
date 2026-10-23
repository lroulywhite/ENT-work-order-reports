# ENT | Run a Work Order Report [Simulation]

Guided click-through simulation for Momentus Enterprise customer education. The learner opens the Reports option for a work order, chooses a report, runs it, and finds the export and email options in Report Viewer.

- **Product:** Momentus Enterprise (never mixed with Elite or MAX)
- **Deliverable:** one self-contained HTML file for the Genially HTML/Code widget
- **Built from:** the Enterprise snapshot `enterprise-2026-10-v1` and the DCS Guided Simulation Template (v2.3)

## Repository layout

```
index.html     Copy of the built simulation, served by GitHub Pages at the site root
simulations/   Built simulation (self-contained HTML, about 3 MB)
src/           template.html (the learning layer) and build.py
assets/snapshots/enterprise-2026-10-v1/
               MANIFEST.json, inventory.json, screens/*.png (the locked product UI)
tests/         verify.py (headless browser checks)
docs/          Capture requests for gaps
```

## Build

```bash
python3 src/build.py
```

`build.py` checks every SHA-256 in `MANIFEST.json` first and stops on a mismatch or missing file. It then embeds the captures unmodified into `src/template.html` and writes `simulations/ENT _ Run a Work Order Report [Simulation].html`.

The file is stored as `ENT _ ...` because Windows file names cannot contain `|`. The page title inside the file is `ENT | Run a Work Order Report [Simulation]`, which is the approved name. Rename the download if you need the pipe.

## GitHub Pages

Publish from the `main` branch, `/ (root)`. The site root opens the simulation (`index.html`). Use that URL as the embed link in Genially. Pages sites are public to anyone with the link, so read the first open item below before sharing it.

## Verify

```bash
pip install -r requirements-dev.txt
playwright install chromium
python3 tests/verify.py
```

It walks the full path at four embed sizes and checks: wrong-report tips loop back, stray clicks show a nudge, Back and Restart reset correctly, the checklist bar count always matches the step, and no guide card or its shadow covers a control the learner must click. Output is `PASS` or a list of problems.

## What the learner does

| Step | Screen | Action |
|---|---|---|
| 1 | Work Orders list | Select Actions |
| 2 | Actions menu | Select Reports |
| 3 | Work Order Reports | Choose Work Order - All Items (the decision point), then confirm with Select |
| 4 | Report Prompt | Select Run Report |
| 5 | Report Viewer | Select Tools, read the export formats, select Email Options, read the email choices, Finish |

Checklist bar ("What you will learn"), checked from the step shown:

| Item | Checks off when the learner reaches |
|---|---|
| Open the Reports option for a work order | Choose the report |
| Choose the report that fits the job | Confirm your choice |
| Run the report | Select Tools |
| Find the export and email options | Email choices |

## Rules this repo follows

- **Product UI is locked.** Every product screen is an unmodified capture from the snapshot. Interactions are hotspots over those captures in the order recorded. Nothing implies behavior that was not captured.
- **Never edit a snapshot folder.** To update the UI, add `enterprise-<YYYY>-<MM>-v2` and rebuild. Keep older versions so existing courses stay traceable.
- **Gaps are requested, not filled.** See `docs/capture-requests.md`.
- **Embed in Genially** at 1920 wide. The stage is 1920x1006: 920 for the product plus the 86px checklist bar. Recommend full-screen mode.

## Open items

1. **Mock data.** The manifest records `mock_data_confirmed_safe: true` on DCS's word. Product/Security confirmation is not recorded. The captures show account, requester and user names. **Keep this repository private until that is confirmed.**
2. **Starting state.** The simulation opens with order 57006 already selected. The Due Date filter and the list before selection were not captured (`docs/capture-requests.md`).
3. **Captures are 1910x915**, not the 1920x1080 standard. They are scaled proportionally, never stretched.
4. **Enterprise font** is not confirmed. Cards use Source Sans Pro per the template. The accent `#4046E0` was sampled from the captures.
5. **Tools and Email Options** are shown as separate steps because opening one while the other is open was not captured.
6. **Capture date, author and demo environment** are not recorded in the manifest (null).
7. **No license** is included. Add one that matches Momentus policy before sharing outside DCS.
