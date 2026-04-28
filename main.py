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
        self.root.title("Jaydon's Library")
        self.root.geometry("450x600")
        self.root.configure(bg="#2c3e50")

        Label(root, text="LIBRARY MANAGEMENT", font=("Arial", 16, "bold")).pack(pady=20)

        self.fields = {}



if __name__ == "__main__":
    root = Tk()
    LibraryInv(root)
    root.mainloop()
        

        

        