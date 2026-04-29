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

        Label(root, text="LIBRARY MANAGEMENT", font=("Arial", 16, "bold")).pack(pady=20)

        label_style = {"font": ("Arial", 10, "bold")}
        input_box_style = { "font": ("Arial", 10)}

        self.fields = {}
        for label_text, var_name in [("Borrower Name", "name"), ("Age", "age"), ("Book Title", "book"), ("ISBN", "isbn")]:
            Label(root, text=label_text, **label_style).pack(anchor="w", padx=50)
            input_box = Entry(root, **input_box_style)
            input_box.pack(fill="x", padx=50, pady=5, ipady=3)
            self.fields[var_name] = input_box

        issue_book_btn = Button(text="Issue Book", command=self.issue_book)
        issue_book_btn.pack(padx=20, pady=20)

        view_borrower_btn = Button(text="View all Borrowers", command=self.view_borrower)
        view_borrower_btn.pack(padx=15, pady=15)

        return_book_btn = Button(text="Return Book", command=self.return_book)
        return_book_btn.pack(padx=15, pady=15)

    def issue_book(self):
        try:
            print("hello")

        except ValueError:
            print("Please, input valid information.")

    def view_borrower(self):
        pass

    def return_book(self):
        pass


if __name__ == "__main__":
    root = Tk()
    LibraryInv(root)
    root.mainloop()
