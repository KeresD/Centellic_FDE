max_tasks = 10

def add_tasks(tasks, description):
    """add new task, return false if list is already full"""
    if len(tasks) >= max_tasks:
        return False
    tasks.append({"description": description, "done": False})
    return True

def complete_task(tasks, index):
    """Mark a test as done, by its position in the list"""
    if index < 0 or index >= len(tasks):
        return False
    tasks[index]["done"] = True
    return True

# make two functions 1. to remove a task -> committed, 2. list all tasks -> committed
def remove_task(tasks, index):
    """Remove a task by its position in the list, return False if index is invalid"""
    if index < 0 or index >= len(tasks):
        return False
    tasks.pop(index)
    return True

def list_tasks(tasks):
    """Return all tasks in the list"""
    return tasks

def main():
    tasks = []
    add_tasks(tasks, "Do Git Walkthrough")
    add_tasks(tasks, "Review the Pull Requests")
    add_tasks(tasks, "Merge to main")
    complete_task(tasks, 0)

    print("Current tasks: ")
    for i, task in enumerate(list_tasks(tasks)):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}: {task['description']}")
    
if __name__ == "__main__":
    main()