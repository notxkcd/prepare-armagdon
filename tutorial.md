# Armagdon Prep: The Complete Field Manual

**Welcome.** This document is the operating manual for your life's accountability system. It covers every tool, workflow, and philosophy built into this repository.

---

## Part 1: The Philosophy

This system is built on **Visibility, not Willpower**.
1.  **Faith is Binary:** You either prayed 5 times or you didn't. There is no "partial credit" for the obligatory.
2.  **Work is Analog:** Deep work is measured in hours. It fluctuates. We track the trend, not just the checkmark.
3.  **Trust is Data:** Your partner doesn't need to ask "Did you do it?" They just look at the Observer View.

---

## Part 2: The Daily Workflow (The "Do" Loop)

This is the only thing you *must* do every single day.

### 1. Start the Day (The Log)
Run this command in your terminal:
```bash
make log
```
*(Alternative: `./log-today.sh`)*
This generates a file for today (e.g., `content/daily/2026-02-03.md`).
**Note:** The file title will automatically include the day of the week (e.g., `Daily Log - 2026-02-03 (Tuesday)`).

### 2. Check Your Progress
At any time, run:
```bash
make show
```
This displays a beautiful dashboard in your terminal showing your metrics (hours) and which tasks are still pending for today.

### 3. Interactive Toggling
Instead of opening the file, you can mark tasks as done by running:
```bash
make check
```
Type the ID of the task to toggle it `[x]` or `[ ]`.

### 4. Fleet Capture (The Scratchpad)
If you have a quick idea during deep work, run:
```bash
make scratch
```
It will prompt for your thought, timestamp it, and append it to your reflections in today's log.

### 5. Track Real-Time (The Input)
Open the generated file for deep reflections. You will see two critical sections:

**A. The Metrics (Frontmatter)**
At the very top of the file, you track **Volume**:
```yaml
focus_hours: 4.5    # How long did you do Deep Work?
learning_hours: 2   # How long did you study/interview prep?
physical_hours: 1   # How long did you Ruck/Gym?
status: "Pending"   # Change to "Complete", "Partial", or "Fail" at end of day
```

**B. The Protocol (Checklists)**
The body of the file contains your "Non-Negotiables".
*   **Faith:** 5/5 Salah + Baqarah + Tahajjud.
*   **Discipline:** Meditation, Deep Work, etc.
*   **Schedule:** Each task has a default time (e.g., `[04:00]`).

### 6. Add Ad-Hoc Tasks
Run:
```bash
make task
```
*(Alternative: `./log-task.sh "Buy Milk"`)*
This appends a checkbox to the bottom of today's file under `## 5. Ad-hoc Tasks`.

---

## Part 3: The Weekly Ritual (The "Review" Loop)

On Sunday evenings, you zoom out.

### 1. Generate the Review
Create a new file for the week:
```bash
hugo new content/weekly/week-XX-YYYY.md
```

### 2. Analyze the Dashboard
Run `make serve` and go to `http://localhost:1313/weekly/week-XX-YYYY/`.
You will see:
*   **Time Distribution Chart:** A breakdown of where your hours went.
*   **Peak Hours Chart:** A new chart showing **when** you were most productive during the day (parses your Pomodoro timestamps).

---

## Part 4: The Partner Protocol (The "Trust" Loop)

This is for your girlfriend/partner.

### 1. The Link
Send her the link to the **Observer View**:
`http://localhost:1313/observer/`

### 2. How to Read It
She looks for the **Heatmap** and the **Workload Trend**.

---

## Part 5: Knowledge Management & Search

Don't let insights get lost.

### 1. Create a Note
```bash
make note
```

### 2. Search Your Mind
Your archive is searchable.
1.  **Index the site:** Run `make build`.
2.  **Search:** Use the search bar in the header of your website. It works offline and is incredibly fast.

---

## Part 6: The Pomodoro System (Focus Execution)

### 1. Start a Session
Run:
```bash
make pomo
```

### 2. Features
*   **Task Selection:** Choose from your current day's protocol.
*   **Auto-Update:** Replaces default schedule times with your **actual start time**.
*   **Auto-Log:** Increments focus/learning/physical hours by **0.42** per session.
*   **Audio Alerts:** Sounds a system alarm when sessions end.
*   **Visual Proof:** Appends a `🍅` to the task in your daily log.

---

## Part 12: Learning Scripts (Bash & Lua)

For educational purposes, equivalent versions of the system's core tools have been implemented in **Bash** and **Lua**. These are located in the `scripts/` directory.

### 1. Bash Versions
Navigate to `scripts/bash/` to see how the system can be built using standard Linux utilities like `grep`, `sed`, and `bc`.
*   `make show` (Bash version)
*   `make pomo` (Bash version)

### 2. Lua Versions
Navigate to `scripts/lua/` to explore a version built with a lightweight, embedded language known for its fast pattern matching and simple file I/O.
*   `make show` (Lua version)
*   `make pomo` (Lua version)

These versions are focused on code readability and demonstrate different programming paradigms.

---

## Part 13: Spirituality Dashboard

The **Spirituality** section (formerly Dialogue) is the core of your faith tracking.
1.  **Automated Metrics:** It automatically counts your Salah completions across all logs.
2.  **Visual Adherence:** Shows a 7-day grid of your prayer consistency.
3.  **Spiritual Records:** List of your reflections and dialogues with the Divine.

---

## Part 14: Troubleshooting

**Q: Search isn't working.**
A: Run `make build` to index your files.

**Q: My checkboxes aren't green.**
A: Ensure the status in the frontmatter is set to "Complete".
