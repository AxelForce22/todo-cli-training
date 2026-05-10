# Todo CLI App

A simple terminal to-do list app written in Python. You can add tasks, mark them as done, delete them, and your tasks are saved automatically so they're still there next time you open the app.

---

## What the app does

- Add a new task
- List all your tasks with a done/not-done status
- Mark a task as done
- Delete a task
- Tasks are saved to a file so nothing is lost when you close the app

---

## How to run it

Make sure you have Python 3 installed. Then open a terminal and run:

```
python3 todo.py
```

You'll see a menu like this:

```
Welcome to the Todo App!

What would you like to do?
  1. Add task
  2. List tasks
  3. Mark task as done
  4. Delete task
  5. Quit
```

Type a number and press Enter to choose an option.

---

## What files exist

| File | What it does |
|---|---|
| `todo.py` | The main program — all the code lives here |
| `tasks.json` | Where your tasks are saved — created automatically when you add your first task |

---

## How tasks are saved

Tasks are stored in a file called `tasks.json`. JSON is a simple text format that Python can read and write easily.

Each task is saved like this:

```json
[
  {"name": "Buy milk", "done": false},
  {"name": "Walk the dog", "done": true}
]
```

Every task has two pieces of information:
- `name` — the text you typed when adding the task
- `done` — `true` if you marked it done, `false` if not

The file is updated automatically every time you add, complete, or delete a task.

---

## Project structure explained

All the code is in `todo.py`. It's split into small functions so each one does just one job:

| Function | What it does |
|---|---|
| `load_tasks()` | Opens `tasks.json` and returns your saved tasks. Returns an empty list if the file doesn't exist yet or is corrupted. |
| `save_tasks()` | Writes your current tasks back to `tasks.json` after every change. |
| `list_tasks()` | Prints all tasks to the screen with numbers and a done/not-done marker. |
| `add_task()` | Asks you to type a task name and adds it to the list. |
| `complete_task()` | Shows the list, asks you to pick a number, and marks that task as done. |
| `delete_task()` | Shows the list, asks you to pick a number, and removes that task. |
| `get_task_number()` | A helper that asks for a number and keeps asking until you enter a valid one. |
| `main()` | Shows the menu and keeps the app running until you choose Quit. |
