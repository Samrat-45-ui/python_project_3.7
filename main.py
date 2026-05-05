"""A simple library inventory management system using Tkinter for the GUI and JSON for data storage."""

import json  # JSON read/write file handling
from tkinter import *  # GUI widgets
from tkinter import messagebox  # dialog boxes


class Borrower:
    """A simple class to represent a borrower and their loan details."""

    def __init__(self, name, age, book, isbn):
        """Initialize a Borrower instance with the provided details."""
        self.name = name
        self.age = age
        self.book = book
        self.isbn = isbn

    def todict(self):
        """Return the borrower data as a dictionary."""
        return {
            "name": self.name,
            "age": self.age,
            "book": self.book,
            "isbn": self.isbn,
        }


class LibraryInv:
    """Library inventory GUI app."""

    def __init__(self, root):
        """Set up the main window and load saved loans."""
        self.root = root
        self.root.title("Newa's Library")
        self.root.geometry("450x600")
        self.root.configure(bg="#2c3e50")

        self.data_file = "library_data.json"
        self.loans = self.load_data()

        label_style = {"bg": "#2c3e50", "fg": "#ecf0f1", "font": ("Arial", 10, "bold")}
        input_box_style = {"bg": "#34495e", "fg": "white", "insertbackground": "white", "relief": "flat", "font": ("Arial", 10)}

        Label(root, text="LIBRARY MANAGEMENT", bg="#2c3e50", fg="#3498db", font=("Arial", 16, "bold")).pack(pady=20)

        self.fields = {}
        field_configs = [("Borrower Name", "name"), ("Age", "age"), ("Book Title", "book"), ("Book ISBN", "isbn")]

        for label_text, internal_name in field_configs:
            Label(root, text=label_text, **label_style).pack(anchor="w", padx=50)
            input_box = Entry(root, **input_box_style)
            input_box.pack(fill="x", padx=50, pady=5, ipady=3)
            self.fields[internal_name] = input_box

        issue_book_btn = Button(text="Issue Book", command=self.issue_book, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
        issue_book_btn.pack(fill="x", padx=50, pady=5, ipady=5)

        view_borrower_btn = Button(text="View all Borrowers", command=self.view_borrowers, bg="#3498db", fg="white", font=("Arial", 10, "bold"), cursor="hand2")  # button to show all borrowers
        view_borrower_btn.pack(fill="x", padx=50, pady=5, ipady=5)

        return_book_btn = Button(text="Return Book", command=self.return_book, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), cursor="hand2")  # button to return a book
        return_book_btn.pack(fill="x", padx=50, pady=5, ipady=5)

    def load_data(self):
        """Load existing loans from the JSON file or returns an empty dictionary if file doesn't exist."""
        try:  # read saved loan data if available
            with open(self.data_file, "r") as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):  # missing or invalid file, it will start with an empty borrower record
            return {}

    def save_data(self):
        """Write the current state of self.loans into the JSON file."""
        with open(self.data_file, "w") as json_file:  # save current loans by writing to JSON file
            json.dump(self.loans, json_file, indent=4)

    def issue_book(self):
        """Validate inputs and adds a new loan record. Also checks for duplicate ISBNs and valid age."""
        form_data = {field_name: widget.get().strip() for field_name, widget in self.fields.items()}  # gather form data from input fields
        if not all(form_data.values()):
            messagebox.showerror("Error", "All the fields must be filled.")  # check for empty fields
            return

        try:
            age_value = int(form_data["age"])  # convert age to integer
            if not (5 <= age_value <= 120):  # enforce reasonable age range
                raise ValueError
        except ValueError:  # invalid age input
            messagebox.showerror("Error", "Please enter a valid age (5-120).")
            return

        if form_data["isbn"] in self.loans:  # prevent duplicate issued ISBNs or already issued books
            messagebox.showerror("Error", "This book is already issued to someone else.")
            return
        
        if len(form_data["isbn"]) != 13:  # check if the ISBN is 13 characters long
            messagebox.showerror("Error", "Please enter a valid 13-character ISBN.")
            return
        
        if len(form_data["book"]) < 2:  # check if the book title is at least 2 characters long
            messagebox.showerror("Error", "Please enter a valid book title (at least 2 characters).")
            return

        if form_data["name"].isnumeric():  # check if the name is not numeric
            messagebox.showerror("Error", "Please enter a valid name (non numeric).")
            return
        
        if form_data["isbn"].isalpha():  # check if the ISBN is not purely alphabetic
            messagebox.showerror("Error", "Please enter a valid ISBN (not purely alphabetic).")
            return

        new_borrower = Borrower(form_data['name'], age_value, form_data['book'], form_data['isbn'])  # create borrower record by instantiating the Borrower class
        self.loans[form_data['isbn']] = new_borrower.todict()  # store loan under ISBN by converting borrower data to a dictionary
        self.save_data()  # persist data
        messagebox.showinfo("Success", f"'{form_data['book']}' has been issued to {form_data['name']} successfully.")
        self.clear_fields()

    def view_borrowers(self):
        """Display a formatted list of all current borrowers."""
        if not self.loans:  # no active loans to show
            messagebox.showinfo('Empty, no active borrowers.')
            return

        borrower_list = []
        for isbn, details in self.loans.items():  # build borrower list by iterating through current loans and formatting the output
            borrower_list.append(f'ISBN: {isbn} | {details['book']} -> {details['name']}')

        messagebox.showinfo('Current Borrowers', '\n'.join(borrower_list))  # show current borrowers in a message box

    def return_book(self):
        """Remove a loan record based on the provided ISBN. Validates the ISBN and checks if it exists."""
        check_isbn = self.fields['isbn'].get().strip()

        if check_isbn in self.loans:  # if book is issued and ISBN is valid, remove the loan record
            del self.loans[check_isbn]
            self.save_data()  # update storage by saving the modified loans
            messagebox.showinfo("Success", "Book returned.")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Invalid ISBN or book not issued.")  # ISBN not found in current loans or invalid input

    def clear_fields(self):
        """Clear all input fields."""
        for input_box in self.fields.values():  # clear each input field by deleting its content
            input_box.delete(0, END)


if __name__ == "__main__":  # entry point of the application, creates the main window and starts the GUI event loop
    root = Tk()
    LibraryInv(root)
    root.mainloop()
