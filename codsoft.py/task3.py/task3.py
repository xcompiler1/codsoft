import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator 🔐")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        
        # Password history
        self.password_history = []
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the UI elements"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🔐 Password Generator",
            font=("Helvetica", 24, "bold"),
            bg="#1e1e2e",
            fg="#00d9ff"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Create strong, secure passwords in seconds!",
            font=("Helvetica", 11),
            bg="#1e1e2e",
            fg="#a6adc8"
        )
        subtitle_label.pack()
        
        # Password Length Section
        length_frame = tk.Frame(self.root, bg="#1e1e2e")
        length_frame.pack(pady=20)
        
        tk.Label(
            length_frame,
            text="Password Length:",
            font=("Helvetica", 12, "bold"),
            bg="#1e1e2e",
            fg="white"
        ).pack()
        
        # Length slider
        self.length_var = tk.IntVar(value=16)
        self.length_label = tk.Label(
            length_frame,
            text="16",
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2e",
            fg="#00d9ff"
        )
        self.length_label.pack(pady=5)
        
        length_slider = tk.Scale(
            length_frame,
            from_=4,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            command=self.update_length_label,
            bg="#313244",
            fg="white",
            highlightthickness=0,
            length=300,
            troughcolor="#45475a"
        )
        length_slider.pack()
        
        # Complexity Options
        options_frame = tk.Frame(self.root, bg="#1e1e2e")
        options_frame.pack(pady=15)
        
        tk.Label(
            options_frame,
            text="Include:",
            font=("Helvetica", 12, "bold"),
            bg="#1e1e2e",
            fg="white"
        ).pack()
        
        # Checkboxes for character types
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        checkbox_style = {"font": ("Helvetica", 11), "bg": "#1e1e2e", "fg": "white", 
                         "selectcolor": "#313244", "activebackground": "#1e1e2e", 
                         "activeforeground": "white"}
        
        tk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.uppercase_var, **checkbox_style).pack(anchor=tk.W, padx=50)
        tk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.lowercase_var, **checkbox_style).pack(anchor=tk.W, padx=50)
        tk.Checkbutton(options_frame, text="Numbers (0-9)", variable=self.numbers_var, **checkbox_style).pack(anchor=tk.W, padx=50)
        tk.Checkbutton(options_frame, text="Symbols (!@#$%...)", variable=self.symbols_var, **checkbox_style).pack(anchor=tk.W, padx=50)
        
        # Generate Button
        generate_btn = tk.Button(
            self.root,
            text="🎲 Generate Password",
            command=self.generate_password,
            font=("Helvetica", 14, "bold"),
            bg="#00d9ff",
            fg="#1e1e2e",
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2",
            activebackground="#00b8d4"
        )
        generate_btn.pack(pady=15)
        # Password Display
        
        password_frame = tk.Frame(self.root, bg="#313244", relief=tk.SOLID, bd=2)
        password_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.password_display = tk.Entry(
            password_frame,
            font=("Courier", 14, "bold"),
            bg="#313244",
            fg="#00d9ff",
            bd=0,
            justify=tk.CENTER,
            state="readonly"
        )
        self.password_display.pack(pady=15, padx=10, fill=tk.X)
        
        # Strength Indicator
        self.strength_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 11, "bold"),
            bg="#1e1e2e",
            fg="white"
        )
        self.strength_label.pack()
        
        # Action Buttons
        action_frame = tk.Frame(self.root, bg="#1e1e2e")
        action_frame.pack(pady=15)
        
        copy_btn = tk.Button(
            action_frame,
            text="📋 Copy",
            command=self.copy_password,
            font=("Helvetica", 11, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        copy_btn.grid(row=0, column=0, padx=5)
        
        new_btn = tk.Button(
            action_frame,
            text="🔄 Generate New",
            command=self.generate_password,
            font=("Helvetica", 11, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        new_btn.grid(row=0, column=1, padx=5)
        
        # Tips
        tips_label = tk.Label(
            self.root,
            text="💡 Tip: Use 16+ characters with all options for maximum security!",
            font=("Helvetica", 9),
            bg="#1e1e2e",
            fg="#a6adc8",
            wraplength=400
        )
        tips_label.pack(pady=10)
    
    def update_length_label(self, value):
        """Update the length display label"""
        self.length_label.config(text=str(value))
    
    def generate_password(self):
        """Generate a random password based on user preferences"""
        length = self.length_var.get()
        
        # Build character pool based on selections
        char_pool = ""
        
        if self.uppercase_var.get():
            char_pool += string.ascii_uppercase
        if self.lowercase_var.get():
            char_pool += string.ascii_lowercase
        if self.numbers_var.get():
            char_pool += string.digits
        if self.symbols_var.get():
            char_pool += string.punctuation
        
        # Check if at least one option is selected
        if not char_pool:
            messagebox.showwarning(
                "No Options Selected",
                "Please select at least one character type!"
            )
            return
        
        # Generate password
        password = ''.join(random.choice(char_pool) for _ in range(length))
        
        # Update display
        self.password_display.config(state="normal")
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, password)
        self.password_display.config(state="readonly")
        
        # Add to history
        self.password_history.append(password)
        
        # Update strength indicator
        self.update_strength_indicator(password)
    
    def update_strength_indicator(self, password):
        """Display password strength"""
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        
        # Calculate strength score
        score = 0
        if length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_symbol:
            score += 1
        
        # Determine strength level
        if score >= 6:
            strength = "💪 Very Strong"
            color = "#a6e3a1"
        elif score >= 4:
            strength = "🔒 Strong"
            color = "#89b4fa"
        elif score >= 3:
            strength = "⚠️ Medium"
            color = "#f9e2af"
        else:
            strength = "❌ Weak"
            color = "#f38ba8"
        
        self.strength_label.config(text=f"Strength: {strength}", fg=color)
    
    def copy_password(self):
        """Copy password to clipboard"""
        password = self.password_display.get()
        
        if not password:
            messagebox.showinfo("No Password", "Please generate a password first!")
            return
        
        # Use tkinter's built-in clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()
        messagebox.showinfo("Copied!", "Password copied to clipboard! ✅")

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()