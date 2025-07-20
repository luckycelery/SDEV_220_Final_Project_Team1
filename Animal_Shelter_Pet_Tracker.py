import json
import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog
import datetime
import os
from PIL import Image, ImageTk  # Requires Pillow library

# base class to represent general animal data
class Animal:
    def __init__(self, name, gender, breed, weight, dob, microchip_number, health_notes, description, image_path=None):
        self.animal_type = "animal"
        self.name = name
        self.gender = gender
        self.breed = breed
        self.weight = weight
        self.dob = dob
        self.microchip_number = microchip_number
        self.health_notes = health_notes
        self.description = description
        self.image_path = image_path or ""

    def to_dict(self):
        return {
            "type": self.animal_type,
            "name": self.name,
            "gender": self.gender,
            "breed": self.breed,
            "weight": self.weight,
            "dob": self.dob,
            "microchip": self.microchip_number,
            "health_notes": self.health_notes,
            "description": self.description,
            "image_path": self.image_path,
        }

class Cat(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animal_type = "cat"

class Dog(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animal_type = "dog"

class Exotic(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animal_type = "exotic"

class AnimalPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Almost Home Humane Society Portal")
        self.root.geometry("900x500")
        self.root.columnconfigure(tuple(range(6)), weight=1)
        self.root.rowconfigure(tuple(range(12)), weight=1)

        self.animals = self.load_animals()
        self.image_path = ""  # Temporarily store uploaded image path

        self.create_onboarding_form()
        self.create_search_form()

    def create_onboarding_form(self):
        tk.Label(self.root, text="Onboard", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='nsew')
        fields = ["Name", "Gender (M/F)", "Type (dog, cat, exotic)", "Breed", "Weight (lb.)", "DOB (YYYY-MM-DD)", "Microchip #", "Health Notes", "Description"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(self.root, text=field + ":").grid(row=i + 1, column=0, sticky='e')
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=1, sticky='ew', padx=5, pady=2)
            entry.config(width=30)
            self.entries[field] = entry

        tk.Button(self.root, text="Upload Image", command=self.upload_image).grid(row=10, column=0, columnspan=2)
        tk.Button(self.root, text="SAVE", command=self.save_animal).grid(row=11, column=1, sticky='e', pady=10)

    def create_search_form(self):
        tk.Label(self.root, text="Search", font=('Arial', 14, 'bold')).grid(row=0, column=3, columnspan=2, sticky='nsew')
        search_fields = ["Name", "Gender (M/F)", "Type", "Breed", "Microchip #"]
        self.search_entries = {}

        for i, field in enumerate(search_fields):
            tk.Label(self.root, text=field + ":").grid(row=i + 1, column=3, sticky='e')
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=4, sticky='ew', padx=5, pady=2)
            entry.config(width=30)
            self.search_entries[field] = entry

        self.search_results = tk.Listbox(self.root, height=10)
        self.search_results.grid(row=6, column=3, columnspan=2, rowspan=6, sticky='nsew', padx=5)
        self.search_results.bind("<<ListboxSelect>>", self.show_animal_details)
        tk.Button(self.root, text="SEARCH", command=self.search_animals).grid(row=5, column=4, sticky='e', pady=10)

    def upload_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
        if filepath:
            self.image_path = filepath

    def show_animal_details(self, event):
        selection = self.search_results.curselection()
        if not selection:
            return

        selected_text = self.search_results.get(selection[0])
        name = selected_text.split(" (")[0]

        for idx, animal in enumerate(self.animals):
            if animal.name == name:
                detail_win = Toplevel(self.root)
                detail_win.title(f"Details for {animal.name}")
                detail_win.geometry("500x600")

                info = (
                    f"Name: {animal.name}\n"
                    f"Gender: {animal.gender}\n"
                    f"Type: {animal.animal_type}\n"
                    f"Breed: {animal.breed}\n"
                    f"Weight: {animal.weight} lbs\n"
                    f"DOB: {animal.dob}\n"
                    f"Microchip #: {animal.microchip_number}\n"
                    f"Health Notes: {animal.health_notes}\n"
                    f"Description: {animal.description}"
                )

                label = tk.Label(detail_win, text=info, justify='left', anchor='nw')
                label.pack(fill='both', expand=True, padx=10, pady=10)

                if animal.image_path and os.path.exists(animal.image_path):
                    img = Image.open(animal.image_path)
                    img.thumbnail((300, 300))
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(detail_win, image=img_tk)
                    img_label.image = img_tk  # Keep reference
                    img_label.pack(pady=5)

                def open_update_window():
                    update_win = Toplevel(detail_win)
                    update_win.title(f"Update {animal.name}")
                    update_win.geometry("400x600")
                    entries = {}
                    fields = ["Name", "Gender (M/F)", "Type (dog, cat, exotic)", "Breed", "Weight (lb.)", "DOB (YYYY-MM-DD)", "Microchip #", "Health Notes", "Description"]

                    for i, field in enumerate(fields):
                        tk.Label(update_win, text=field + ":").grid(row=i, column=0, sticky='e', padx=5, pady=5)
                        ent = tk.Entry(update_win, width=30)
                        ent.grid(row=i, column=1, padx=5, pady=5)
                        entries[field] = ent

                    entries["Name"].insert(0, animal.name)
                    entries["Gender (M/F)"].insert(0, animal.gender)
                    entries["Type (dog, cat, exotic)"].insert(0, animal.animal_type)
                    entries["Breed"].insert(0, animal.breed)
                    entries["Weight (lb.)"].insert(0, animal.weight)
                    entries["DOB (YYYY-MM-DD)"].insert(0, animal.dob)
                    entries["Microchip #"].insert(0, animal.microchip_number)
                    entries["Health Notes"].insert(0, animal.health_notes)
                    entries["Description"].insert(0, animal.description)

                    def upload_new_image():
                        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
                        if path:
                            animal.image_path = path

                    tk.Button(update_win, text="Upload New Image", command=upload_new_image).grid(row=len(fields), column=0, columnspan=2)

                    def save_updates():
                        if not entries["Name"].get().strip():
                            messagebox.showerror("Error", "Name is required.")
                            return
                        gender_val = entries["Gender (M/F)"].get().strip().upper()
                        if gender_val not in ("M", "F"):
                            messagebox.showerror("Error", "Gender must be M or F.")
                            return
                        dob_input = entries["DOB (YYYY-MM-DD)"].get().strip()
                        if dob_input:
                            try:
                                datetime.datetime.strptime(dob_input, "%Y-%m-%d")
                            except ValueError:
                                messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format.")
                                return

                        animal.name = entries["Name"].get().strip()
                        animal.gender = gender_val
                        animal.animal_type = entries["Type (dog, cat, exotic)"].get().strip().lower()
                        animal.breed = entries["Breed"].get().strip()
                        animal.weight = entries["Weight (lb.)"].get().strip()
                        animal.dob = dob_input
                        animal.microchip_number = entries["Microchip #"].get().strip()
                        animal.health_notes = entries["Health Notes"].get().strip()
                        animal.description = entries["Description"].get().strip()

                        self.save_animals_to_file()
                        messagebox.showinfo("Success", "Animal updated successfully!")
                        update_win.destroy()
                        detail_win.destroy()
                        self.search_results.delete(0, tk.END)

                    tk.Button(update_win, text="Save Changes", command=save_updates).grid(row=len(fields) + 1, column=1, pady=10)

                tk.Button(detail_win, text="Update Animal", command=open_update_window).pack(pady=5)

                def delete_animal():
                    if messagebox.askyesno("Confirm Delete", f"Delete {animal.name}?"):
                        self.animals.pop(idx)
                        self.save_animals_to_file()
                        self.search_results.delete(0, tk.END)
                        detail_win.destroy()
                        messagebox.showinfo("Deleted", f"{animal.name} has been deleted.")

                tk.Button(detail_win, text="Delete Animal", fg="red", command=delete_animal).pack(pady=5)
                break

    def save_animal(self):
        name = self.entries["Name"].get().strip()
        gender = self.entries["Gender (M/F)"].get().strip().upper()
        type_ = self.entries["Type (dog, cat, exotic)"].get().strip().lower()

        kwargs = {
            "name": name,
            "gender": gender,
            "breed": self.entries["Breed"].get().strip(),
            "weight": self.entries["Weight (lb.)"].get().strip(),
            "dob": self.entries["DOB (YYYY-MM-DD)"].get().strip(),
            "microchip_number": self.entries["Microchip #"].get().strip(),
            "health_notes": self.entries["Health Notes"].get().strip(),
            "description": self.entries["Description"].get().strip(),
            "image_path": self.image_path
        }

        if not name or gender not in ("M", "F") or not type_ or not kwargs["breed"]:
            messagebox.showerror("Error", "Please fill required fields correctly.")
            return

        if kwargs["dob"]:
            try:
                datetime.datetime.strptime(kwargs["dob"], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format.")
                return

        cls = {"cat": Cat, "dog": Dog, "exotic": Exotic}.get(type_, Animal)
        animal = cls(**kwargs)
        self.animals.append(animal)
        self.save_animals_to_file()

        messagebox.showinfo("Success", "Animal added successfully!")
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.image_path = ""  # Reset image

    def search_animals(self):
        self.search_results.delete(0, tk.END)
        name_filter = self.search_entries["Name"].get().lower()
        gender_filter = self.search_entries["Gender (M/F)"].get().upper()
        type_filter = self.search_entries["Type"].get().lower()
        breed_filter = self.search_entries["Breed"].get().lower()
        microchip_filter = self.search_entries["Microchip #"].get()

        for animal in self.animals:
            if (name_filter in animal.name.lower() and
                (gender_filter == "" or gender_filter == animal.gender) and
                type_filter in animal.animal_type.lower() and
                breed_filter in animal.breed.lower() and
                microchip_filter in animal.microchip_number):
                self.search_results.insert(tk.END, f"{animal.name} ({animal.animal_type}, {animal.breed})")

    def save_animals_to_file(self):
        with open("animals.json", "w") as file:
            json.dump([animal.to_dict() for animal in self.animals], file, indent=2)

    def load_animals(self):
        try:
            with open("animals.json", "r") as file:
                data = json.load(file)
                loaded = []
                for entry in data:
                    cls = {"cat": Cat, "dog": Dog, "exotic": Exotic}.get(entry.get("type", "animal"), Animal)
                    loaded.append(cls(entry["name"], entry.get("gender", ""), entry["breed"],
                                      entry["weight"], entry["dob"], entry["microchip"],
                                      entry["health_notes"], entry["description"], entry.get("image_path", "")))
                return loaded
        except (FileNotFoundError, json.JSONDecodeError):
            return []

# launch GUI
if __name__ == '__main__':
    root = tk.Tk()
    app = AnimalPortal(root)
    root.mainloop()
