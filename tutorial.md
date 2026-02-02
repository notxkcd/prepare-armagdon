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
This generates a file for today (e.g., `content/daily/2026-02-03.md`) pre-filled with your protocol.

### 2. Track Real-Time (The Input)
Open the generated file. You will see two critical sections:

**A. The Metrics (Frontmatter)**
At the very top of the file, you track **Volume**:
```yaml
focus_hours: 4.5    # How long did you do Deep Work?
learning_hours: 2   # How long did you study/interview prep?
physical_hours: 1   # How long did you Ruck/Gym?
status: "Pending"   # Change to "Complete", "Partial", or "Fail" at end of day
```
*These numbers feed the charts in the Weekly Dashboard.*

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
*   **Distribution Chart:** A stacked bar chart showing where your time went.

**If the chart is empty:** You forgot to enter numbers in the `focus_hours` fields of your daily logs. Go back and fill them in.

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

## Part 7: Troubleshooting

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