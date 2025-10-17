import tkinter as tk
from tkinter import messagebox
import requests


from main import fetch_documents

API_URL = "http://your-api-endpoint/documents"  # Replace with your actual endpoint

class DocumentSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Document Selector")

        # Create buttons
        self.fetch_button = tk.Button(self, text="Fetch Documents", command=self.fetch_documents)
        self.fetch_button.pack(pady=5)

        self.process_button = tk.Button(self, text="Process Selected Document", command=self.process_document, state=tk.DISABLED)
        self.process_button.pack(pady=5)

        self.post_button = tk.Button(self, text="Post Documents", command=self.post_documents, state=tk.DISABLED)
        self.post_button.pack(pady=5)

        # Create a listbox to display documents
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, height=15, width=50)
        self.listbox.pack(pady=10)

        self.documents = []  # To store fetched documents

    def fetch_documents(self):
        try:
            documents = fetch_documents()  # Call the function from main.py
            if not documents:
                raise ValueError("No documents returned from the API.")
            self.documents = documents
            self.listbox.delete(0, tk.END)  # Clear the listbox
            for doc in self.documents:
                self.listbox.insert(tk.END, str(doc))
            self.process_button.config(state=tk.NORMAL)
            self.post_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch documents:\n{e}")

    def process_document(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a document to process.")
            return
        selected_doc = self.listbox.get(selected[0])
        # Add your processing logic here
        messagebox.showinfo("Processing", f"Processing document: {selected_doc}")

    def post_documents(self):
        try:
            # Example logic for posting documents
            response = requests.post(API_URL, json=self.documents)
            response.raise_for_status()
            messagebox.showinfo("Success", "Documents posted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to post documents:\n{e}")

if __name__ == "__main__":
    app = DocumentSelector()
    app.mainloop()