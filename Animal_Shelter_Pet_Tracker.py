#import necessary Libraries
import json #data serialization
import tkinter as tk #GUI elements
from tkinter import messagebox, Toplevel #for pop-up dialogues and and windows
import datetime #handling DOB data

#base class to represent general animal data
class Animal:
    def __init__(self, name, gender, breed, weight, dob, microchip_number, health_notes, description):
        self.animal_type = "animal" #set default animal type
        #basic attributes shared by all animal types
        self.name = name
        self.gender = gender
        self.breed = breed
        self.weight = weight
        self.dob = dob
        self.microchip_number = microchip_number
        self.health_notes = health_notes
        self.description = description

    def to_dict(self):
        """Method converts object to dict format for serialization or display"""
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
        }
#subclass of Animals
class Cat(Animal):
    def __init__(self, name, gender, breed, weight, dob, microchip_number, health_notes, description):
        super().__init__(name, gender, breed, weight, dob, microchip_number, health_notes, description)
        self.animal_type = "cat"

#subclass of Animals
class Dog(Animal):
    def __init__(self, name, gender, breed, weight, dob, microchip_number, health_notes, description):
        super().__init__(name, gender, breed, weight, dob, microchip_number, health_notes, description)
        self.animal_type = "dog"

#subclass of Animals
class Exotic(Animal):
    def __init__(self, name, gender, breed, weight, dob, microchip_number, health_notes, description):
        super().__init__(name, gender, breed, weight, dob, microchip_number, health_notes, description)
        self.animal_type = "exotic"

#manages GUI for onboarding and searching animals
class AnimalPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Almost Home Humane Society Portal") #window title
        self.root.geometry("900x500") #fixed window size

        #grid layout for responsive design
        self.root.columnconfigure(tuple(range(6)), weight=1)
        self.root.rowconfigure(tuple(range(12)), weight=1)

        self.animals = self.load_animals() #load existing animal records
        self.create_onboarding_form() #create UI section for onboarding animals
        self.create_search_form() #create UI section for searching animals

    #create onboarding section UI
    def create_onboarding_form(self):
        tk.Label(self.root, text="Onboard", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='nsew')

        #define fields for anboarding danimal data
        fields = ["Name", "Gender (M/F)", "Type (dog, cat, exotic)", "Breed", "Weight (lb.)", "DOB (YYYY-MM-DD)", "Microchip #", "Health Notes", "Description"]
        self.entries = {}

        #dynamically create labels and entry boxes for each field
        for i, field in enumerate(fields):
            tk.Label(self.root, text=field + ":").grid(row=i + 1, column=0, sticky='e')
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=1, sticky='ew', padx=5, pady=2)
            entry.config(width=30)
            self.entries[field] = entry

        #button to save new animal entry
        tk.Button(self.root, text="SAVE", command=self.save_animal).grid(row=10, column=1, sticky='e', pady=10)

    #create search section UI
    def create_search_form(self):
        tk.Label(self.root, text="Search", font=('Arial', 14, 'bold')).grid(row=0, column=3, columnspan=2, sticky='nsew')
        
        #define fields to filer search results 
        search_fields = ["Name", "Gender (M/F)", "Type", "Breed", "Microchip #"]
        self.search_entries = {}

        #dynamically create labels and entry fields for search criteria
        for i, field in enumerate(search_fields):
            tk.Label(self.root, text=field + ":").grid(row=i + 1, column=3, sticky='e')
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=4, sticky='ew', padx=5, pady=2)
            entry.config(width=30)
            self.search_entries[field] = entry #store references for search

        #listbox to show search results
        self.search_results = tk.Listbox(self.root, height=10)
        self.search_results.grid(row=6, column=3, columnspan=2, rowspan=6, sticky='nsew', padx=5)

        #bind selection even to show animal details if clicked
        self.search_results.bind("<<ListboxSelect>>", self.show_animal_details)

        #button that triggers search
        tk.Button(self.root, text="SEARCH", command=self.search_animals).grid(row=5, column=4, sticky='e', pady=10)
    #display details of the selected animal from search results
    def show_animal_details(self, event):
        selection = self.search_results.curselection()
        if not selection:
            return #exit it nothing is selected

        selected_text = self.search_results.get(selection[0])
        name = selected_text.split(" (")[0] #extract animal name

        #locate selected animal by object name
        for idx, animal in enumerate(self.animals):
            if animal.name == name:
                #create window to show specific animal's info
                detail_win = Toplevel(self.root)
                detail_win.title(f"Details for {animal.name}")
                detail_win.geometry("500x550")

                #formal animal info display
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

                #display info in label
                label = tk.Label(detail_win, text=info, justify='left', anchor='nw')
                label.pack(fill='both', expand=True, padx=10, pady=10)

                #function to open update window for editing animal details
                def open_update_window():
                    update_win = Toplevel(detail_win)
                    update_win.title(f"Update {animal.name}")
                    update_win.geometry("400x550")

                    #define fields and create entry weidgets
                    fields = ["Name", "Gender (M/F)", "Type (dog, cat, exotic)", "Breed", "Weight (lb.)", "DOB (YYYY-MM-DD)", "Microchip #", "Health Notes", "Description"]
                    entries = {}

                    #populate the update form with current values
                    for i, field in enumerate(fields):
                        tk.Label(update_win, text=field + ":").grid(row=i, column=0, sticky='e', padx=5, pady=5)
                        ent = tk.Entry(update_win, width=30)
                        ent.grid(row=i, column=1, padx=5, pady=5)
                        entries[field] = ent

                    # Pre-fill current values
                    entries["Name"].insert(0, animal.name)
                    entries["Gender (M/F)"].insert(0, animal.gender)
                    entries["Type (dog, cat, exotic)"].insert(0, animal.animal_type)
                    entries["Breed"].insert(0, animal.breed)
                    entries["Weight (lb.)"].insert(0, animal.weight)
                    entries["DOB (YYYY-MM-DD)"].insert(0, animal.dob)
                    entries["Microchip #"].insert(0, animal.microchip_number)
                    entries["Health Notes"].insert(0, animal.health_notes)
                    entries["Description"].insert(0, animal.description)

                    #save updated details to animal object
                    def save_updates():
                        # Validation: Required fields
                        if not entries["Name"].get().strip():
                            messagebox.showerror("Error", "Name is required.")
                            return
                        gender_val = entries["Gender (M/F)"].get().strip().upper()
                        if gender_val not in ("M", "F"):
                            messagebox.showerror("Error", "Gender must be M or F.")
                            return
                        if not entries["Type (dog, cat, exotic)"].get().strip():
                            messagebox.showerror("Error", "Type is required.")
                            return
                        if not entries["Breed"].get().strip():
                            messagebox.showerror("Error", "Breed is required.")
                            return

                        # Validate DOB format
                        dob_input = entries["DOB (YYYY-MM-DD)"].get().strip()
                        if dob_input:
                            try:
                                datetime.datetime.strptime(dob_input, "%Y-%m-%d")
                            except ValueError:
                                messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format (e.g., 2024-07-15).")
                                return

                        # Update animal attributes to selected animal
                        animal.name = entries["Name"].get().strip()
                        animal.gender = gender_val
                        animal.animal_type = entries["Type (dog, cat, exotic)"].get().strip().lower()
                        animal.breed = entries["Breed"].get().strip()
                        animal.weight = entries["Weight (lb.)"].get().strip()
                        animal.dob = dob_input
                        animal.microchip_number = entries["Microchip #"].get().strip()
                        animal.health_notes = entries["Health Notes"].get().strip()
                        animal.description = entries["Description"].get().strip()

                        self.save_animals_to_file() #persist changes
                        messagebox.showinfo("Success", "Animal updated successfully!")
                        update_win.destroy()
                        detail_win.destroy()
                        self.search_results.delete(0, tk.END) #refresh result

                    #save button to save new animal info
                    save_btn = tk.Button(update_win, text="Save Changes", command=save_updates)
                    save_btn.grid(row=len(fields), column=1, pady=10)

                #update button that populates update window to update animal info
                update_btn = tk.Button(detail_win, text="Update Animal", command=open_update_window)
                update_btn.pack(pady=5)

                #function to delete selectd animal
                def delete_animal():
                    confirm = messagebox.askyesno("Confirm Delete", f"Delete {animal.name}?")
                    if confirm:
                        self.animals.pop(idx)
                        self.save_animals_to_file()
                        self.search_results.delete(0, tk.END)
                        detail_win.destroy()
                        messagebox.showinfo("Deleted", f"{animal.name} has been deleted.")

                #add button to delete animal
                delete_btn = tk.Button(detail_win, text="Delete Animal", fg="red", command=delete_animal)
                delete_btn.pack(pady=5)

                break #exit loop after finding correct animal
    
    #save new animal entry from onboarding form
    def save_animal(self):
        name = self.entries["Name"].get().strip()
        gender = self.entries["Gender (M/F)"].get().strip().upper()
        type_ = self.entries["Type (dog, cat, exotic)"].get().strip().lower()

        #additional fields stored in dictionary
        kwargs = {
            "name": name,
            "gender": gender,
            "breed": self.entries["Breed"].get().strip(),
            "weight": self.entries["Weight (lb.)"].get().strip(),
            "dob": self.entries["DOB (YYYY-MM-DD)"].get().strip(),
            "microchip_number": self.entries["Microchip #"].get().strip(),
            "health_notes": self.entries["Health Notes"].get().strip(),
            "description": self.entries["Description"].get().strip()
        }

        # Validation: Required fields
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return
        if gender not in ("M", "F"):
            messagebox.showerror("Error", "Gender must be M or F.")
            return
        if not type_:
            messagebox.showerror("Error", "Type is required.")
            return
        if not kwargs["breed"]:
            messagebox.showerror("Error", "Breed is required.")
            return

        # Validate DOB format
        dob_input = kwargs["dob"]
        if dob_input:
            try:
                datetime.datetime.strptime(dob_input, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format (e.g., 2024-07-15).")
                return
        #create instance of the correct animal subclass
        cls = {"cat": Cat, "dog": Dog, "exotic": Exotic}.get(type_, Animal)
        animal = cls(**kwargs)

        #add to internal list and persist data
        self.animals.append(animal)
        self.save_animals_to_file()

        #inform user and reset form
        messagebox.showinfo("Success", "Animal added successfully!")
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    #serach for animals based on user-defined filters
    def search_animals(self):
        self.search_results.delete(0, tk.END) #clear previous results

        #gather filters from search form
        name_filter = self.search_entries["Name"].get().lower()
        gender_filter = self.search_entries["Gender (M/F)"].get().upper()
        type_filter = self.search_entries["Type"].get().lower()
        breed_filter = self.search_entries["Breed"].get().lower()
        microchip_filter = self.search_entries["Microchip #"].get()

        #iterate through animals and match filters
        for animal in self.animals:
            if (name_filter in animal.name.lower() and
                (gender_filter == "" or gender_filter == animal.gender) and
                type_filter in animal.animal_type.lower() and
                breed_filter in animal.breed.lower() and
                microchip_filter in animal.microchip_number):
                self.search_results.insert(tk.END, f"{animal.name} ({animal.animal_type}, {animal.breed})")

    #persist animal data to a local JSON file
    def save_animals_to_file(self):
        with open("animals.json", "w") as file:
            json.dump([animal.to_dict() for animal in self.animals], file, indent=2)

    #load saved animal data from JSON file
    def load_animals(self):
        try:
            with open("animals.json", "r") as file:
                data = json.load(file)
                loaded = []

                #reconstruct animal objects from dictionary data
                for entry in data:
                    cls = {"cat": Cat, "dog": Dog, "exotic": Exotic}.get(entry.get("type", "animal"), Animal)
                    loaded.append(cls(entry["name"], entry.get("gender", ""),
                                      entry["breed"], entry["weight"], entry["dob"],
                                      entry["microchip"], entry["health_notes"], entry["description"]))
                return loaded
        except (FileNotFoundError, json.JSONDecodeError):
            return [] #return empty list if file doesn't exist or is corrupt

#launch GUI
if __name__ == '__main__':
    root = tk.Tk()
    app = AnimalPortal(root)
    root.mainloop()
