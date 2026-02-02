# Armagdon Prep - System Manual

This repository contains your personal accountability system, designed as a minimalist static site. It serves as the "High Definition" mirror to your daily tracking spreadsheet.

## 1. The Core Philosophy
*   **Visibility over Willpower:** The goal isn't to force behavior, but to make your actions visible.
*   **Mirror, Don't Replace:** Your Google Sheet is for quick entry. This site is for reflection and history.
*   **Observer View:** A specific page designed for your partner to see your consistency without micromanaging you.

## 2. Folder Structure (Where to Edit)

All content lives in the `content/` directory.

### `content/daily/`
**What:** Daily logs, checklists, and brief notes.
**When:** Create one every evening (or morning after).
**Format:**
```markdown
---
title: "Daily Log - YYYY-MM-DD"
date: YYYY-MM-DD
status: "Complete"
---
- [x] Task 1
- [ ] Task 2
*Notes on the day...*
```

### `content/weekly/` & `content/monthly/`
**What:** Higher-level reviews.
**When:** Sundays (Weekly) and End of Month (Monthly).
**Purpose:** To spot trends (e.g., "I always miss Tuesdays").

### `content/philosophy/`
**What:** Permanent notes, principles, and mental models.
**Purpose:** To remind yourself *why* you are doing this.

### `content/observer.md`
**What:** The page your partner sees.
**Edit:** Rarely. It automatically pulls data from your logs (in a future automated version) or serves as a static explanation of the system rules.

## 3. How to Run the Site

1.  **Start the Server:**
    Open your terminal in this directory and run:
    ```bash
    hugo server
    ```
2.  **View:**
    Open `http://localhost:1313` in your browser.

## 4. Customizing the Look

*   **Styles:** Edit `themes/earth-focus/static/css/style.css`.
*   **Layouts:** Edit HTML files in `themes/earth-focus/layouts/`.
    *   `_default/baseof.html`: The main wrapper (HTML head, body).
    *   `_default/list.html`: How lists of posts look.
    *   `_default/single.html`: How a single post looks.
    *   `page/observer.html`: The special observer view layout.

## 5. Deployment (Optional)

To publish this site to the web (e.g., GitHub Pages, Netlify):
1.  Run `hugo` (without `server`) to build the static files into the `public/` folder.
2.  Upload the `public/` folder to your host.
