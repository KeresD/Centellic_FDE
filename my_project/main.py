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