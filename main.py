import tkinter as tk
from tkinter import ttk, messagebox
import os

class HomeworkManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Homework Manager")
        self.root.geometry("700x500")
        
        self.root.resizable(True, True)
        
        # Create file if it doesn't exist
        self.file_path = "homework.txt"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "a"):
                pass
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and place widgets
        self.create_widgets(main_frame)
        
        # Load assignments
        self.load_assignments()
    
    def create_widgets(self, parent):
        # Left side - Assignment list
        list_frame = ttk.LabelFrame(parent, text="Assignments", padding="10")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Scrollable assignment list
        self.tree = ttk.Treeview(list_frame, columns=("Name", "Due Date", "Course"), show="headings")
        self.tree.heading("Name", text="Assignment Name")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Course", text="Course")
        self.tree.column("Name", width=150)
        self.tree.column("Due Date", width=100)
        self.tree.column("Course", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right side - Controls
        control_frame = ttk.Frame(parent, padding="10")
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        
        # Add Assignment Frame
        add_frame = ttk.LabelFrame(control_frame, text="Add Assignment", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Name input
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5, padx=5)
        
        # Due date input
        ttk.Label(add_frame, text="Due Date:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.due_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.due_var, width=30).grid(row=1, column=1, pady=5, padx=5)
        
        # Course input
        ttk.Label(add_frame, text="Course:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.course_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.course_var, width=30).grid(row=2, column=1, pady=5, padx=5)
        
        # Add button
        ttk.Button(add_frame, text="Add Assignment", command=self.add_assignment).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Button Frame
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Remove button
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_assignment).pack(fill=tk.X, pady=5)
        
        # Refresh button
        ttk.Button(button_frame, text="Refresh List", command=self.load_assignments).pack(fill=tk.X, pady=5)
    
    def add_assignment(self):
        name = self.name_var.get().strip()
        due = self.due_var.get().strip()
        course = self.course_var.get().strip()
        
        if not name or not due or not course:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Add to file
        with open(self.file_path, "a") as file:
            file.write(f"{name}, {due}, {course}\n")
        
        # Clear inputs
        self.name_var.set("")
        self.due_var.set("")
        self.course_var.set("")
        
        # Refresh list
        self.load_assignments()
        messagebox.showinfo("Success", "Assignment added successfully!")
    
    def remove_assignment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No assignment selected!")
            return
        
        # Get the assignment text from the selected item
        values = self.tree.item(selected_item[0], "values")
        selected_assignment = f"{values[0]}, {values[1]}, {values[2]}"
        
        # Read all assignments
        with open(self.file_path, "r") as file:
            assignments = file.readlines()
        
        # Write back all except the selected one
        with open(self.file_path, "w") as file:
            for assignment in assignments:
                if assignment.strip() != selected_assignment:
                    file.write(assignment)
        
        # Refresh list
        self.load_assignments()
        messagebox.showinfo("Success", "Assignment removed successfully!")
    
    def load_assignments(self):
        # Clear current view
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Read from file
        try:
            with open(self.file_path, "r") as file:
                assignments = file.readlines()
            
            # Add to treeview
            for assignment in assignments:
                assignment = assignment.strip()
                if assignment:
                    parts = assignment.split(", ")
                    if len(parts) >= 3:
                        self.tree.insert("", tk.END, values=(parts[0], parts[1], parts[2]))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load assignments: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeworkManagerApp(root)
    root.mainloop()