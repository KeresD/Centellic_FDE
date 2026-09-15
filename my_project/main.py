max_tasks = 10

def add_tasks(tasks, description):
    """add new task, return false if list is already full"""
    if tasks >= max_tasks:
        return False
    tasks.append({"description": description, "done": False})
    return True
