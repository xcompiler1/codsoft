import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # File to store tasks
        self.data_file = "tasks.json"
        self.tasks = self.load_tasks()
        
        # Configure style
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Load existing tasks
        self.refresh_task_list()
    
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4a90e2"
        self.success_color = "#5cb85c"
        self.danger_color = "#d9534f"
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.primary_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="📝 My To-Do List",
            font=("Helvetica", 24, "bold"),
            bg=self.primary_color,
            fg="white",
            pady=15
        )
        title_label.pack()
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            input_frame,
            text="Task:",
            font=("Helvetica", 12),
            bg=self.bg_color
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.task_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            width=40
        )
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        tk.Label(
            input_frame,
            text="Priority:",
            font=("Helvetica", 12),
            bg=self.bg_color
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            font=("Helvetica", 10),
            width=15
        )
        priority_menu.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Add Button
        add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg=self.success_color,
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        add_btn.grid(row=1, column=2, padx=5)
        
        # Filter Frame
        filter_frame = tk.Frame(self.root, bg=self.bg_color)
        filter_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            filter_frame,
            text="Filter:",
            font=("Helvetica", 11),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="All")
        for filter_option in ["All", "Pending", "Completed"]:
            tk.Radiobutton(
                filter_frame,
                text=filter_option,
                variable=self.filter_var,
                value=filter_option,
                command=self.refresh_task_list,
                bg=self.bg_color,
                font=("Helvetica", 10),
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
        
        # Task List Frame
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 11),
            height=15,
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            bg="white",
            selectbackground=self.primary_color
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=15, padx=20)
        
        complete_btn = tk.Button(
            btn_frame,
            text="✓ Complete",
            command=self.complete_task,
            bg=self.success_color,
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2"
        )
        complete_btn.grid(row=0, column=0, padx=5)
        
        delete_btn = tk.Button(
            btn_frame,
            text="✕ Delete",
            command=self.delete_task,
            bg=self.danger_color,
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2"
        )
        delete_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = tk.Button(
            btn_frame,
            text="🗑 Clear Completed",
            command=self.clear_completed,
            bg="#f0ad4e",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2"
        )
        clear_btn.grid(row=0, column=2, padx=5)
        
        # Stats Frame
        self.stats_frame = tk.Frame(self.root, bg=self.bg_color)
        self.stats_frame.pack(pady=10)
        
        self.stats_label = tk.Label(
            self.stats_frame,
            text="",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg="#555"
        )
        self.stats_label.pack()
        
        self.update_stats()
    
    def add_task(self):
        """Add a new task to the list"""
        task_text = self.task_entry.get().strip()
        
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "text": task_text,
            "priority": self.priority_var.get(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_task_list()
        self.task_entry.delete(0, tk.END)
        self.update_stats()
        
        messagebox.showinfo("Success", "Task added successfully!")
    
    def complete_task(self):
        """Mark selected task as completed"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            filtered_tasks = self.get_filtered_tasks()
            task = filtered_tasks[selected_index]
            
            # Find the task in the main list and toggle completion
            for t in self.tasks:
                if t["id"] == task["id"]:
                    t["completed"] = not t["completed"]
                    break
            
            self.save_tasks()
            self.refresh_task_list()
            self.update_stats()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def delete_task(self):
        """Delete selected task"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            filtered_tasks = self.get_filtered_tasks()
            task = filtered_tasks[selected_index]
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
                self.tasks = [t for t in self.tasks if t["id"] != task["id"]]
                self.save_tasks()
                self.refresh_task_list()
                self.update_stats()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def clear_completed(self):
        """Clear all completed tasks"""
        completed_count = sum(1 for task in self.tasks if task["completed"])
        
        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
        
        if messagebox.askyesno("Confirm", f"Delete {completed_count} completed task(s)?"):
            self.tasks = [task for task in self.tasks if not task["completed"]]
            self.save_tasks()
            self.refresh_task_list()
            self.update_stats()
    
    def get_filtered_tasks(self):
        """Get tasks based on current filter"""
        filter_value = self.filter_var.get()
        
        if filter_value == "Pending":
            return [task for task in self.tasks if not task["completed"]]
        elif filter_value == "Completed":
            return [task for task in self.tasks if task["completed"]]
        else:
            return self.tasks
    
    def refresh_task_list(self):
        """Refresh the task listbox with current tasks"""
        self.task_listbox.delete(0, tk.END)
        
        filtered_tasks = self.get_filtered_tasks()
        
        for task in filtered_tasks:
            priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            status = "✓" if task["completed"] else "○"
            display_text = f"{status} {priority_emoji[task['priority']]} {task['text']}"
            
            self.task_listbox.insert(tk.END, display_text)
            
            # Strikethrough for completed tasks
            if task["completed"]:
                self.task_listbox.itemconfig(tk.END, fg="gray")
    
    def update_stats(self):
        """Update statistics display"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        pending = total - completed
        
        self.stats_label.config(
            text=f"Total: {total} | Pending: {pending} | Completed: {completed}"
        )
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
                return []
        return []

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()