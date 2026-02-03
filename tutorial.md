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

### 2. Track Real-Time (The Input)
Open the generated file. You will see two critical sections:

**A. The Metrics (Frontmatter)**
At the very top of the file, you track **Volume**:
```yaml
focus_hours: 4.5    # How long did you do Deep Work?
learning_hours: 2   # How long did you study/interview prep?
physical_hours: 1   # How long did you Ruck/Gym?
status: "Pending"   # Change to "Complete", "Partial", or "Fail" at end of day

# Targets (Optional: Customize your daily goals)
focus_target: 8
learning_target: 4
physical_target: 2
```
*These numbers feed the charts in the Weekly Dashboard and the progress bars in the Archive views.*

**B. The Protocol (Checklists)**
The body of the file contains your "Non-Negotiables".
*   **Faith:** 5/5 Salah + Baqarah + Tahajjud.
*   **Discipline:** Meditation, Deep Work, etc.
*   **Schedule:** Each task has a default time (e.g., `[04:00]`).

### 3. Add Ad-Hoc Tasks
If you need to remember to "Buy Milk" or "Email Boss", do not clutter the protocol. Run:
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
*(Replace XX with week number, e.g., week-06-2026)*

### 2. Analyze the Dashboard
Run `make serve` and go to `http://localhost:1313/weekly/week-XX-YYYY/`.
You will see:
*   **3 Big Cards:** Total hours spent on Work, Learning, and Body.
*   **Time Distribution Chart:** A breakdown of where your hours went.
*   **Daily Rhythm Chart:** Your total output per day (shows consistency).
*   **Ritual Adherence:** Automatically tracks how many times you checked off "Fajr", "Dhuhr", "Exercise", etc. during the week.

**Monthly View:**
At the end of the month, go to your monthly review to see:
*   **Monthly Composition:** A donut chart showing the percentage breakdown of your total effort for the month.
*   **Activity Calendar:** An interactive grid showing which days you were active.
    *   **Clickable Dates:** Days with content are highlighted in green. Clicking a date scrolls you to the "Daily Evidence" for that specific day.
*   **Daily Evidence Breakdown:** A deep-dive list at the bottom of the monthly page that groups every file you wrote (logs, tech notes, essays) by their category for each day.

---

## Part 4: The Partner Protocol (The "Trust" Loop)

This is for your girlfriend/partner.

### 1. The Link
Send her the link to the **Observer View**:
`http://localhost:1313/observer/`

### 2. How to Read It
She looks for two things:
1.  **The Heatmap:**
    *   **Green Squares:** You are safe. The system is working.
    *   **Grey/Empty Squares:** Slippage.
    *   **Hovering:** She can hover over a square to see the exact status ("Complete", "Fail").
2.  **The Workload Trend:**
    *   A bar chart showing your Deep Work intensity over the last 7 days.

### 3. The Rule
She does **not** check this daily. She checks it weekly (Sunday). If she sees Green, she says nothing. If she sees Red/Empty, she asks: *"Is the system broken, or are you?"*

---

## Part 5: Knowledge Management

Don't let insights get lost in daily logs.

### Create a Note
If you learn something about "Rust Memory Safety" or have a "Stoic Reflection", run:
```bash
make note
```
*(Alternative: `./new-note.sh "Title" "Section"`)*
*   **Arguments:** Title, Section (`tech`, `essays`, `philosophy`).
*   **Result:** A new file in `content/tech/rust-ownership.md`.

---

## Part 6: Maintenance & Customization

### Changing the "Default" Day
If your wake-up time changes from 04:00 to 05:00:
1.  Edit `archetypes/daily.md`.
2.  Change `[04:00] Salatul Tahajjud` to `[05:00] ...`.
3.  *Future* logs will use this new time. Past logs remain unchanged.

### Adjusting Chart Scales
*   **Observer Chart:** Currently scales to **8 hours**.
    *   *Edit:* `themes/earth-focus/layouts/_default/observer.html`
    *   *Find:* `calc( {{ $val }} / 8 )` -> Change `8` to your max daily capacity.
*   **Weekly Chart:** Scales automatically based on the total hours of that week. No adjustment needed.

### Backup
Everything is text.
1.  Run `git add .`
2.  Run `git commit -m "daily logs"`
3.  Run `git push`

---

## Part 8: The Pomodoro System (Focus Execution)

To bridge the gap between "planning" and "doing," the system includes a **Task-Aware Pomodoro Timer**.

### 1. Start a Session
Run this command in your terminal:
```bash
make pomo
```

### 2. How it works
1.  **Task Selection:** The script scans your current Daily Log and presents a list of all your checkboxes (`- [ ]`).
2.  **Focus Selection:** Type the number of the task you are about to work on.
3.  **Dynamic Scheduling:** The script automatically finds that task in your log and replaces the default time (e.g., `[05:45]`) with your **actual start time**.
4.  **The Timer:** A beautiful, theme-colored progress bar will appear. Each session is **25 minutes**.
5.  **Multi-Cycle Mode:** If the task name contains "2 Hours," the script automatically sets up **4 sessions** with breaks in between.
6.  **Audio Alerts:** A system alarm will sound when the timer reaches zero, signaling the start or end of a focus session/break.

### 3. Automatic Logging
When a session finishes:
*   **Metric Update:** Your `focus_hours`, `learning_hours`, or `physical_hours` (detected automatically) will increment by **0.42** (25 minutes).
*   **Visual Proof:** A `🍅` is appended to the task line in your Markdown file for every session you complete.

---

## Part 9: Troubleshooting

**Q: My checkboxes aren't green!**
A: Ensure the status in the frontmatter is set to "Complete". Also, check `status: "Pending"` doesn't override it.

**Q: The Weekly Chart is empty.**
A: You likely left `focus_hours: 0` in your daily logs. The chart needs data to render.

**Q: I missed a day. Can I backfill?**
A: Yes.
```bash
hugo new content/daily/YYYY-MM-DD.md
```
Use the specific date you missed. The system will slot it into the correct place in history.