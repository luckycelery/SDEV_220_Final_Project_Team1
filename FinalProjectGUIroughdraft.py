import tkinter as tk
from tkinter import messagebox

class Animal:
    def __init__(self, name, type_, breed, weight, dob, microchip, health_notes, description):
        self.name = name
        self.type = type_
        self.breed = breed
        self.weight = weight
        self.dob = dob
        self.microchip = microchip
        self.health_notes = health_notes
        self.description = description

class AnimalPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Almost Home Humane Society Portal")
        self.animals = []

        # Onboarding form
        self.create_onboarding_form()

        # Search form
        self.create_search_form()

    def create_onboarding_form(self):
        tk.Label(self.root, text="Onboard").grid(row=0, column=0, columnspan=2)
        fields = ["Name", "Type", "Breed", "Weight (lbs)", "DOB (mm/dd/yyyy)", "Microchip #", "Health Notes", "Description"]
        self.entries = {}
        for i, field in enumerate(fields):
            tk.Label(self.root, text=field+":").grid(row=i+1, column=0)
            entry = tk.Entry(self.root)
            entry.grid(row=i+1, column=1)
            self.entries[field] = entry

        tk.Button(self.root, text="SAVE", command=self.save_animal).grid(row=9, column=1)

    def create_search_form(self):
        tk.Label(self.root, text="Search").grid(row=0, column=3, columnspan=2)
        search_fields = ["Name", "Type", "Breed", "Microchip #"]
        self.search_entries = {}
        for i, field in enumerate(search_fields):
            tk.Label(self.root, text=field+":").grid(row=i+1, column=3)
            entry = tk.Entry(self.root)
            entry.grid(row=i+1, column=4)
            self.search_entries[field] = entry

        self.search_results = tk.Listbox(self.root, height=10, width=40)
        self.search_results.grid(row=6, column=3, columnspan=2)

        tk.Button(self.root, text="SEARCH", command=self.search_animals).grid(row=5, column=4)

    def save_animal(self):
        animal = Animal(
            self.entries["Name"].get(),
            self.entries["Type"].get(),
            self.entries["Breed"].get(),
            self.entries["Weight (lbs)"].get(),
            self.entries["DOB (mm/dd/yyyy)"].get(),
            self.entries["Microchip #"].get(),
            self.entries["Health Notes"].get(),
            self.entries["Description"].get(),
        )
        self.animals.append(animal)
        messagebox.showinfo("Success", "Animal added successfully!")
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def search_animals(self):
        self.search_results.delete(0, tk.END)
        for animal in self.animals:
            if (self.search_entries["Name"].get().lower() in animal.name.lower() and
                self.search_entries["Type"].get().lower() in animal.type.lower() and
                self.search_entries["Breed"].get().lower() in animal.breed.lower() and
                self.search_entries["Microchip #"].get() in animal.microchip):
                self.search_results.insert(tk.END, f"{animal.name} ({animal.type}, {animal.breed})")

if __name__ == '__main__':
    root = tk.Tk()
    app = AnimalPortal(root)
    root.mainloop()
