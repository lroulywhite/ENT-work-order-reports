# Capture requests

Format from `snapshot-spec.md`. Capture at 1920x1080, 100% zoom, no extensions visible, in one session, as a new snapshot version (`enterprise-2026-10-v2`).

```
CAPTURE REQUEST
Product: Enterprise
Screen: Work Orders list
State: default (filter panel open, no rows, nothing selected)
Navigation path: Main Menu > Work Orders > Work Orders
Needed for: ENT | Run a Work Order Report, to start before a row is selected
```

```
CAPTURE REQUEST
Product: Enterprise
Screen: Work Orders list
State: Due Date dropdown open
Navigation path: Work Orders > Filters panel > Due Date unit dropdown
Needed for: ENT | Run a Work Order Report, optional filter step
```

```
CAPTURE REQUEST
Product: Enterprise
Screen: Work Orders list
State: filtered results, no row selected
Navigation path: Work Orders > set Due Date > Apply Filters
Needed for: ENT | Run a Work Order Report, to add a "select a work order" step
```

```
CAPTURE REQUEST
Product: Enterprise
Screen: Report Viewer
State: Save To menu open; also Email Options opened while Tools is already open
Navigation path: Report Prompt > Run Report > Save To / Email Options
Needed for: ENT | Run a Work Order Report, to cover the toolbar fully and confirm menu switching
```
