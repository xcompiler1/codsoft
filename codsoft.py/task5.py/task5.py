import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("📇 Contact Book")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        # Data file
        self.data_file = "contacts.json"
        self.contacts = self.load_contacts()
        
        # Current selection
        self.current_contact_id = None
        
        # Create UI
        self.create_widgets()
        self.refresh_contact_list()
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg="#4a90e2", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📇 My Contact Book",
            font=("Helvetica", 26, "bold"),
            bg="#4a90e2",
            fg="white"
        ).pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Contact List
        left_frame = tk.Frame(main_container, bg="#f5f5f5")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search bar
        search_frame = tk.Frame(left_frame, bg="#f5f5f5")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Helvetica", 11, "bold"),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_contacts())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Helvetica", 11),
            bg="white",
            relief=tk.SOLID,
            bd=1
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Contact list label
        tk.Label(
            left_frame,
            text="Contact List",
            font=("Helvetica", 12, "bold"),
            bg="#f5f5f5"
        ).pack(anchor=tk.W, pady=(5, 5))
        
        # Contact listbox with scrollbar
        list_container = tk.Frame(left_frame, bg="white", relief=tk.SOLID, bd=1)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contact_listbox = tk.Listbox(
            list_container,
            font=("Helvetica", 11),
            bg="white",
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.contact_listbox.yview)
        
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)
        
        # Contact count
        self.count_label = tk.Label(
            left_frame,
            text="Total Contacts: 0",
            font=("Helvetica", 9),
            bg="#f5f5f5",
            fg="#666"
        )
        self.count_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Right side - Contact Details Form
        right_frame = tk.Frame(main_container, bg="white", relief=tk.SOLID, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Form title
        form_title_frame = tk.Frame(right_frame, bg="#4a90e2")
        form_title_frame.pack(fill=tk.X)
        
        self.form_title = tk.Label(
            form_title_frame,
            text="➕ Add New Contact",
            font=("Helvetica", 14, "bold"),
            bg="#4a90e2",
            fg="white",
            pady=10
        )
        self.form_title.pack()
        
        # Form fields
        form_frame = tk.Frame(right_frame, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Name
        tk.Label(
            form_frame,
            text="Name *",
            font=("Helvetica", 10, "bold"),
            bg="white",
            anchor=tk.W
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.name_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 11),
            bg="#f9f9f9",
            relief=tk.SOLID,
            bd=1
        )
        self.name_entry.grid(row=1, column=0, sticky=tk.EW, pady=(0, 15))
        
        # Phone
        tk.Label(
            form_frame,
            text="Phone Number *",
            font=("Helvetica", 10, "bold"),
            bg="white",
            anchor=tk.W
        ).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.phone_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 11),
            bg="#f9f9f9",
            relief=tk.SOLID,
            bd=1
        )
        self.phone_entry.grid(row=3, column=0, sticky=tk.EW, pady=(0, 15))
        
        # Email
        tk.Label(
            form_frame,
            text="Email",
            font=("Helvetica", 10, "bold"),
            bg="white",
            anchor=tk.W
        ).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        self.email_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 11),
            bg="#f9f9f9",
            relief=tk.SOLID,
            bd=1
        )
        self.email_entry.grid(row=5, column=0, sticky=tk.EW, pady=(0, 15))
        
        # Address
        tk.Label(
            form_frame,
            text="Address",
            font=("Helvetica", 10, "bold"),
            bg="white",
            anchor=tk.W
        ).grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        
        self.address_text = tk.Text(
            form_frame,
            font=("Helvetica", 11),
            bg="#f9f9f9",
            relief=tk.SOLID,
            bd=1,
            height=4,
            wrap=tk.WORD
        )
        self.address_text.grid(row=7, column=0, sticky=tk.EW, pady=(0, 20))
        
        # Configure grid
        form_frame.columnconfigure(0, weight=1)
        
        # Buttons frame
        button_frame = tk.Frame(right_frame, bg="white")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.add_btn = tk.Button(
            button_frame,
            text="➕ Add Contact",
            command=self.add_contact,
            font=("Helvetica", 11, "bold"),
            bg="#5cb85c",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        self.add_btn.pack(fill=tk.X, pady=(0, 8))
        
        self.update_btn = tk.Button(
            button_frame,
            text="💾 Update Contact",
            command=self.update_contact,
            font=("Helvetica", 11, "bold"),
            bg="#f0ad4e",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            state=tk.DISABLED
        )
        self.update_btn.pack(fill=tk.X, pady=(0, 8))
        
        self.delete_btn = tk.Button(
            button_frame,
            text="🗑 Delete Contact",
            command=self.delete_contact,
            font=("Helvetica", 11, "bold"),
            bg="#d9534f",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            state=tk.DISABLED
        )
        self.delete_btn.pack(fill=tk.X, pady=(0, 8))
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🔄 Clear Form",
            command=self.clear_form,
            font=("Helvetica", 11, "bold"),
            bg="#6c757d",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        self.clear_btn.pack(fill=tk.X)
    
    def add_contact(self):
        """Add a new contact"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        
        # Validation
        if not name:
            messagebox.showwarning("Missing Information", "Please enter a name!")
            self.name_entry.focus()
            return
        
        if not phone:
            messagebox.showwarning("Missing Information", "Please enter a phone number!")
            self.phone_entry.focus()
            return
        
        # Check for duplicate phone
        for contact in self.contacts:
            if contact['phone'] == phone:
                messagebox.showwarning(
                    "Duplicate Contact",
                    "A contact with this phone number already exists!"
                )
                return
        
        # Create new contact
        new_contact = {
            'id': self.generate_id(),
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        
        self.contacts.append(new_contact)
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_form()
        
        messagebox.showinfo("Success", f"Contact '{name}' added successfully! ✅")
    
    def update_contact(self):
        """Update existing contact"""
        if self.current_contact_id is None:
            messagebox.showwarning("No Selection", "Please select a contact to update!")
            return
        
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        
        # Validation
        if not name or not phone:
            messagebox.showwarning("Missing Information", "Name and phone are required!")
            return
        
        # Check for duplicate phone (except current contact)
        for contact in self.contacts:
            if contact['phone'] == phone and contact['id'] != self.current_contact_id:
                messagebox.showwarning(
                    "Duplicate Contact",
                    "Another contact with this phone number already exists!"
                )
                return
        
        # Update contact
        for contact in self.contacts:
            if contact['id'] == self.current_contact_id:
                contact['name'] = name
                contact['phone'] = phone
                contact['email'] = email
                contact['address'] = address
                break
        
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_form()
        
        messagebox.showinfo("Success", f"Contact '{name}' updated successfully! ✅")
    
    def delete_contact(self):
        """Delete selected contact"""
        if self.current_contact_id is None:
            messagebox.showwarning("No Selection", "Please select a contact to delete!")
            return
        
        # Get contact name for confirmation
        contact_name = ""
        for contact in self.contacts:
            if contact['id'] == self.current_contact_id:
                contact_name = contact['name']
                break
        
        # Confirm deletion
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{contact_name}'?\n\nThis action cannot be undone!"
        ):
            self.contacts = [c for c in self.contacts if c['id'] != self.current_contact_id]
            self.save_contacts()
            self.refresh_contact_list()
            self.clear_form()
            
            messagebox.showinfo("Success", f"Contact '{contact_name}' deleted! 🗑")
    
    def on_contact_select(self, event):
        """Handle contact selection from list"""
        selection = self.contact_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        contact_info = self.contact_listbox.get(index)
        
        # Extract phone from the display text
        phone = contact_info.split(" | ")[1] if " | " in contact_info else ""
        
        # Find contact by phone
        for contact in self.contacts:
            if contact['phone'] == phone:
                self.load_contact_to_form(contact)
                break
    
    def load_contact_to_form(self, contact):
        """Load contact details into the form"""
        self.current_contact_id = contact['id']
        
        # Clear and populate fields
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, contact['name'])
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, contact['phone'])
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contact.get('email', ''))
        
        self.address_text.delete("1.0", tk.END)
        self.address_text.insert("1.0", contact.get('address', ''))
        
        # Update UI
        self.form_title.config(text="✏️ Edit Contact")
        self.add_btn.config(state=tk.DISABLED)
        self.update_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)
    
    def clear_form(self):
        """Clear all form fields"""
        self.current_contact_id = None
        
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
        
        # Reset UI
        self.form_title.config(text="➕ Add New Contact")
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        
        # Clear listbox selection
        self.contact_listbox.selection_clear(0, tk.END)
    
    def search_contacts(self):
        """Search contacts by name or phone"""
        query = self.search_var.get().lower().strip()
        
        self.contact_listbox.delete(0, tk.END)
        
        if not query:
            # Show all contacts if search is empty
            self.refresh_contact_list()
            return
        
        # Filter contacts
        filtered = [c for c in self.contacts if 
                   query in c['name'].lower() or 
                   query in c['phone']]
        
        # Sort by name
        filtered.sort(key=lambda x: x['name'].lower())
        
        # Display filtered contacts
        for contact in filtered:
            display_text = f"{contact['name']} | {contact['phone']}"
            self.contact_listbox.insert(tk.END, display_text)
        
        # Update count
        self.count_label.config(text=f"Found: {len(filtered)} contacts")
    
    def refresh_contact_list(self):
        """Refresh the contact list display"""
        self.contact_listbox.delete(0, tk.END)
        
        # Sort contacts by name
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        
        for contact in sorted_contacts:
            display_text = f"{contact['name']} | {contact['phone']}"
            self.contact_listbox.insert(tk.END, display_text)
        
        # Update count
        self.count_label.config(text=f"Total Contacts: {len(self.contacts)}")
    
    def generate_id(self):
        """Generate unique ID for new contact"""
        if not self.contacts:
            return 1
        return max(c['id'] for c in self.contacts) + 1
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.contacts, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {str(e)}")
    
    def load_contacts(self):
        """Load contacts from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")
                return []
        return []

def main():
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()

if __name__ == "__main__":
    main()