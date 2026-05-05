import json
from tkinter import *
from tkinter import messagebox


class Borrower:
    def __init__(self, name, age, book, isbn):
        self.name = name
        self.age = age
        self.book = book
        self.isbn = isbn

    def todict(self):
        return{
            "name": self.name,
            "age": self.age,
            "book": self.book,
            "isbn": self.isbn,
        }


class LibraryInv:
    def __init__(self, root):
        self.root = root
        self.root.title("Newa's Library")
        self.root.geometry("450x600")
        self.root.configure(bg="#2c3e50")

        self.data_file = "library_data.json"
        self.loans = self.load_data()

        label_style = {"font": ("Arial", 10, "bold")}
        input_box_style = { "font": ("Arial", 10)}
        
        Label(root, text="LIBRARY MANAGEMENT", font=("Arial", 16, "bold")).pack(pady=20)

        self.fields = {}
        field_configs = [("Borrower Name", "name"), ("Age", "age"), ("Book Title", "book"), ("Book ISBN", "isbn")]

        for label_text, internal_name in field_configs:
            Label(root, text=label_text, **label_style).pack(anchor="w", padx=50)
            input_box = Entry(root, **input_box_style)
            input_box.pack(fill="x", padx=50, pady=5, ipady=3)
            self.fields[internal_name] = input_box

        issue_book_btn = Button(text="Issue Book", command=self.issue_book)
        issue_book_btn.pack(fill="x", padx=50, pady=5, ipady=5)

        view_borrower_btn = Button(text="View all Borrowers", command=self.view_borrowers)
        view_borrower_btn.pack(fill="x", padx=50, pady=5, ipady=5)

        return_book_btn = Button(text="Return Book", command=self.return_book)
        return_book_btn.pack(fill="x", padx=50, pady=5, ipady=5)

    def load_data(self):
        try:
            with open(self.data_file, "r") as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def save_data(self):
        with open(self.data_file, "w") as json_file:
            json.dump(self.loans, json_file, indent=4)

    def issue_book(self):
        form_data = {field_name: widget.get().strip() for field_name, widget in self.fields.items()}
        if not all(form_data.values()):
            messagebox.showerror("Error", "All the fields must be filled.")
            return

        try:
            age_value = int(form_data["age"])
            if not (5 <= age_value <= 120):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age (5-120).")
            return
        
        if form_data["isbn"] in self.loans:
            messagebox.showerror("Error", "This book is already issued to someone else.")
            return
        
        new_borrower = Borrower(form_data['name'], age_value, form_data['book'], form_data['isbn'])
        self.loans[form_data['isbn']] = new_borrower.todict()
        self.save_data()
        messagebox.showinfo("Success", f"'{form_data['book']}' has been issued to {form_data['name']} successfully.")
        self.clear_fields()

    def view_borrowers(self):
        if not self.loans:
            messagebox.showinfo('Empty, no active borrowers.')
            return

        borrower_list = []
        for isbn, details in self.loans.items():
            borrower_list.append(f'ISBN: {isbn} | {details['book']} -> {details['name']}')
        
        messagebox.showinfo('Current Borrowers', '\n'.join(borrower_list))

    def return_book(self):
        check_isbn = self.fields['isbn'].get().strip()

        if check_isbn in self.loans:
            del self.loans[check_isbn]
            self.save_data()
            messagebox.showinfo("Success", "Book returned.")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Invalid ISBN or book not issued.")

    def clear_fields(self):
        for input_box in self.fields.values():
            input_box.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    LibraryInv(root)
    root.mainloop()
