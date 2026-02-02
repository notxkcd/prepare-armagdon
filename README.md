# Armagdon Prep - System Manual

This repository contains your personal accountability system, designed as a minimalist static site. It serves as the "High Definition" mirror to your daily tracking spreadsheet.

## ⚡ Quick Start

1.  **Log Today's Entry:**
    ```bash
    ./log-today.sh
    ```
    *(Creates a pre-filled file in `content/daily/`)*

2.  **Add a Normal Task:**
    ```bash
    ./log-task.sh "Buy groceries"
    ```
    *(Appends a checkbox to today's log)*

3.  **View the Site:**
    ```bash
    make serve
    ```
    *(Opens http://localhost:1313)*

## 1. The Core Philosophy
*   **Visibility over Willpower:** The goal isn't to force behavior, but to make your actions visible.
*   **Mirror, Don't Replace:** Your Google Sheet is for quick entry. This site is for reflection and history.
*   **Observer View:** A specific page designed for your partner to see your consistency without micromanaging you.

## 2. Folder Structure (Where to Edit)

All content lives in the `content/` directory.

### `content/daily/`
**What:** Daily logs, checklists, and brief notes.
**When:** Create one every evening (or morning after).
**Command:** `./log-today.sh`

## 3. Faith-based Protocol (Recurrence Rules)

The system is built on binary adherence to these recurring tasks:

*   **Salah:** 5/5 daily completion is required for a "Complete" status.
*   **Surah Al-Baqarah:** Minimum cadence of once every 3 days.
*   **Salatul Tahajjud:** Minimum cadence of once every 3 days (Wake-up: 04:00).

Treat these as recurring ritual rules, not optional goals. Visibility of these tasks is the primary trust metric in the **Observer View**.

## 4. Command Reference & Visual Guide

Here is exactly what the helper scripts generate, so you know what to expect.

### A. The Daily Logger (`./log-today.sh`)
**Action:** Creates a new file in `content/daily/YYYY-MM-DD.md`.
**Generated Content:**
```markdown
---
title: "Daily Log - 2026-02-02 (Monday)"
date: 2026-02-02
status: "Pending"
# Metrics (Enter hours as decimals)
focus_hours: 0     # Deep Work
learning_hours: 0  # Coding / Interview Prep
physical_hours: 0  # Ruck / Gym
---

## 1. Faith Protocol (The Non-Negotiables)
### Salah (5/5 Required)
- [ ] [Dawn] Fajr
- [ ] [Noon] Dhuhr
...

### Recurring Rituals
- [ ] [04:00] Salatul Tahajjud (Wake Up)
- [ ] [04:30] Surah Al-Baqarah (If due today)

## 2. Daily Discipline (The Grind)
- [ ] [05:30] Morning Meditation
- [ ] [07:00] Deep Work (Target: 2 Hours)
...
```

### B. The Task Logger (`./log-task.sh "Buy Milk"`)
**Action:** Finds today's file and **appends** the task to the bottom.
**Visual Result:**
```markdown
## 4. Tasks
<!-- Add normal daily tasks below -->
- [ ] Buy Milk    <-- Appended automatically
```

### C. The Note Creator (`./new-note.sh "Title" "section"`)
**Action:** Creates a clean markdown file in the specified section (tech/essays/philosophy).
**Example:** `./new-note.sh "Learning Rust" "tech"`
**Generated Content (`content/tech/learning-rust.md`):**
```markdown
---
title: "Learning Rust"
date: 2026-02-02T10:00:00+00:00
draft: false
---

```

## 5. How to Run the Site

1.  **Start the Server:**
    Open your terminal in this directory and run:
    ```bash
    hugo server
    ```
2.  **View:**
    Open `http://localhost:1313` in your browser.

## 6. Customizing the Look

*   **Styles:** Edit `themes/earth-focus/static/css/style.css`.
*   **Layouts:** Edit HTML files in `themes/earth-focus/layouts/`.
    *   `_default/baseof.html`: The main wrapper (HTML head, body).
    *   `_default/list.html`: How lists of posts look.
    *   `_default/single.html`: How a single post looks.
    *   `_default/observer.html`: The special observer view layout.

## 7. Maintenance & Customization (Tutorial)

### How to add new Recurring Tasks
If you want to add a new daily requirement (e.g., "Read 10 pages"):
1.  Open `archetypes/daily.md`.
2.  Add a new checkbox under the relevant section:
    ```markdown
    - [ ] Read 10 pages
    ```
3.  From now on, every time you run `./log-today.sh`, this new task will be included.

### How to modify the Protocol Rules
The rules are purely a mental model and a template. To change your wake-up time or cadence:
1.  Edit the text in `archetypes/daily.md`.
2.  Update the "Faith-based Protocol" section in this `README.md` for consistency.

### How the Charts/Heatmap work
*   **Heatmap (Observer View):** It looks for the `status` field in your daily logs. Values should be `Complete`, `Partial`, or `Fail`.
*   **Workload Chart (Observer View):** It looks for the `focus_hours` field in the frontmatter. 
    *   *Tip:* The chart is scaled to 8 hours. If you consistently work 12 hours, edit `themes/earth-focus/layouts/_default/observer.html` and change the `calc( {{ $val }} / 8 )` to `12`.
*   **Time Distribution (Weekly View):** This chart aggregates data from **all daily logs within that week (Mon-Sun)**.
    *   **Work:** Sum of `focus_hours`.
    *   **Learn:** Sum of `learning_hours`.
    *   **Body:** Sum of `physical_hours`.
    *   *Note:* If you don't log hours in your daily files, this chart will be empty.

### Script Logic
*   `./log-today.sh`: Uses `hugo new` which triggers the `daily.md` archetype.
*   `./log-task.sh`: Uses `grep` and `sed` to find the "Tasks" header and append text. If you rename the "## 4. Tasks" header in the archetype, you **must** update the header name in `log-task.sh` as well.

## 8. Deployment (Optional)

To publish this site to the web (e.g., GitHub Pages, Netlify):
1.  Run `hugo` (without `server`) to build the static files into the `public/` folder.
2.  Upload the `public/` folder to your host.

## 9. Offline Usage
You can browse the site entirely offline (without internet) using the local server:
1.  Run `make serve`
2.  Open `http://localhost:1313`

*Note: Double-clicking HTML files directly from the file explorer is not supported to ensure maximum compatibility with the server features.*

## 9. Offline Usage
You can browse the site entirely offline (without internet) using the local server:
1.  Run `make serve`
2.  Open `http://localhost:1313`

*Note: Double-clicking HTML files directly from the file explorer is not supported to ensure maximum compatibility with the server features.*