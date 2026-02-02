# Armagdon Prep - System Manual

This repository contains your personal accountability system, designed as a minimalist static site. It serves as the "High Definition" mirror to your daily tracking spreadsheet.

## ⚡ Quick Start

1.  **Log Today's Entry:**
    ```bash
    ./log-today.sh
    ```
    *(Creates a pre-filled file in `content/daily/`)*

2.  **View the Site:**
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
**Command:**
```bash
./log-today.sh
```
**Format:** Automatically generated with your ritual checklist (Salah, Baqarah, Tahajjud).

## 3. Faith-based Protocol (Recurrence Rules)

The system is built on binary adherence to these recurring tasks:

*   **Salah:** 5/5 daily completion is required for a "Complete" status.
*   **Surah Al-Baqarah:** Minimum cadence of once every 3 days.
*   **Salatul Tahajjud:** Minimum cadence of once every 3 days (Wake-up: 04:00).

Treat these as recurring ritual rules, not optional goals. Visibility of these tasks is the primary trust metric in the **Observer View**.

## 4. How to Run the Site

1.  **Start the Server:**
    Open your terminal in this directory and run:
    ```bash
    hugo server
    ```
2.  **View:**
    Open `http://localhost:1313` in your browser.

## 5. Customizing the Look

*   **Styles:** Edit `themes/earth-focus/static/css/style.css`.
*   **Layouts:** Edit HTML files in `themes/earth-focus/layouts/`.
    *   `_default/baseof.html`: The main wrapper (HTML head, body).
    *   `_default/list.html`: How lists of posts look.
    *   `_default/single.html`: How a single post looks.
    *   `_default/observer.html`: The special observer view layout.

## 6. Deployment (Optional)

To publish this site to the web (e.g., GitHub Pages, Netlify):
1.  Run `hugo` (without `server`) to build the static files into the `public/` folder.
2.  Upload the `public/` folder to your host.
