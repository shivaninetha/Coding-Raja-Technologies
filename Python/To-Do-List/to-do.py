from datetime import datetime

class Task:
    def __init__(self, title, priority, due_date, completed=False):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def to_string(self):
        return f"{self.title},{self.priority},{self.due_date.strftime('%Y-%m-%d') if self.due_date else ''},{self.completed}\n"

    #classmethod
    def from_string(cls, task_str):
        task_data = task_str.strip().split(',')
        title, priority, due_date_str, completed = task_data
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        return cls(title, int(priority), due_date, completed == 'True')

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def mark_completed(self, task):
        task.completed = True

    def list_tasks(self):
        return self.tasks

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for task in self.tasks:
                file.write(task.to_string())

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.tasks = [Task.from_string(line) for line in lines]
            print("Tasks loaded from file.")
        except FileNotFoundError:
            print("No previous tasks found.")

def display_menu():
    print("\n===== To-Do List App =====")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Completed")
    print("4. List Tasks")
    print("5. Save and Quit")

def get_task_details():
    title = input("Enter task title: ")
    priority = input("Enter priority (integer): ")
    due_date_str = input("Enter due date (YYYY-MM-DD) or press Enter for none: ")

    try:
        priority = int(priority)
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        return Task(title, priority, due_date)
    except ValueError:
        print("Invalid input. Priority should be an integer, and date should be in the format YYYY-MM-DD.")
        return None

def main():
    todo_list = TodoList()

    todo_list.load_from_file('tasks.txt')

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            task = get_task_details()
            if task:
                todo_list.add_task(task)
                print("Task added successfully.")
        elif choice == '2':
            tasks = todo_list.list_tasks()
            if not tasks:
                print("No tasks to remove.")
            else:
                print("Select a task to remove:")
                for i, task in enumerate(tasks):
                    print(f"{i + 1}. {task.title}")
                try:
                    task_index = int(input()) - 1
                    todo_list.remove_task(tasks[task_index])
                    print("Task removed successfully.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid task number.")
        elif choice == '3':
            tasks = [task for task in todo_list.list_tasks() if not task.completed]
            if not tasks:
                print("No incomplete tasks to mark as completed.")
            else:
                print("Select a task to mark as completed:")
                for i, task in enumerate(tasks):
                    print(f"{i + 1}. {task.title}")
                try:
                    task_index = int(input()) - 1
                    todo_list.mark_completed(tasks[task_index])
                    print("Task marked as completed.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid task number.")
        elif choice == '4':
            tasks = todo_list.list_tasks()
            if not tasks:
                print("No tasks to display.")
            else:
                print("\n===== Task List =====")
                for i, task in enumerate(tasks):
                    status = "Completed" if task.completed else "Pending"
                    due_date = task.due_date.strftime('%Y-%m-%d') if task.due_date else "None"
                    print(f"{i + 1}. Title: {task.title} | Priority: {task.priority} | Due Date: {due_date} | Status: {status}")
        elif choice == '5':
            todo_list.save_to_file('tasks.txt')
            print("Tasks saved to file. Quitting.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
