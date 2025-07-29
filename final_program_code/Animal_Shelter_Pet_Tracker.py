"""
===============================================================================
    Animal Shelter Pet Tracker
    Developed by: Emma Kaufman, Elizabeth Ehrhardt, and Nicholas Albin
    Last Modified  : July 29, 2025
    Version     : 1.0.0

    Description : 
        A Python-based application to streamline shelter operations including
        pet intake and animal inventory/information management.

    Dependencies:
        - Python 3.10+
        - tkinter            : GUI components, if applicable)
        - json               : Data Storage and serialization
        - datetime           : DOB management
        - os                 : File path manipulation 
        - Pillow (PIL)       : Image handling for pet profiles
        - messagebox, Toplevel, filedialog :UI extensions from tkinter 

===============================================================================
"""
# =============================================================================
# Imports — Standard and third-party libraries
# =============================================================================

import json
import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog
import datetime
import os
from PIL import Image, ImageTk  # Requires Pillow library

# =============================================================================
# Data Models — Object-oriented structure for pets
# =============================================================================

class Animal:
    """
    Base class representing general animal information.

    Attributes:
        animal_type (str)       : Generic type indicator; overridden in subclasses
        name (str)              : Animal’s name
        gender (str)            : Gender (e.g., Male, Female)
        breed (str)             : Breed category
        weight (float)          : Weight of animal in pounds/kilograms
        dob (str)               : Date of birth (expected format: YYYY-MM-DD)
        microchip_number (str)  : Unique identifier for tracking
        health_notes (str)      : Medical or behavioral remarks
        description (str)       : Additional descriptors (e.g., temperament)
        image_path (str)        : File path to profile image (optional)
    """
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
        """
        Converts the instance into a dictionary for serialization.
        """
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

# =============================================================================
# Specific Pet Types — Inherit from Animal and override type
# =============================================================================

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

# =============================================================================
# GUI Controller — Manages application window, layout, and user events
# =============================================================================

class AnimalPortal:
    """
    Initializes the GUI portal with layout configuration and form setup.
    Args:
        root (tk.Tk): Main application window object.
    """
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

# =============================================================================
# GUI Form Setup — Onboarding and Search Interfaces for Pet Data Entry
# =============================================================================

    def create_onboarding_form(self):
        """
        Creates the input form on the left panel of the GUI
        for onboarding new animals into the shelter database.
        """
        tk.Label(self.root, text="Onboard", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='nsew')
        fields = ["Name", "Gender (M/F)", "Type (dog, cat, exotic)", "Breed", "Weight (lb.)", "DOB (YYYY-MM-DD)", "Microchip #", "Health Notes", "Description"]
        self.entries = {} #dictionary to store field references

        #dynamically generate labels and entry boxes for each field
        for i, field in enumerate(fields):
            tk.Label(self.root, text=field + ":").grid(row=i + 1, column=0, sticky='e')
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=1, sticky='ew', padx=5, pady=2)
            entry.config(width=30)
            self.entries[field] = entry
        
        #buttons for image upload and sacing form data
        tk.Button(self.root, text="Upload Image", command=self.upload_image).grid(row=10, column=0, columnspan=2)
        tk.Button(self.root, text="SAVE", command=self.save_animal).grid(row=11, column=1, sticky='e', pady=10)

# -----------------------------------------------------------------------------

    def create_search_form(self):
        """
        Creates the search panel on the right side of the GUI
        to locate animals based on user-input filters.
        """
        tk.Label(self.root, text="Search", font=('Arial', 14, 'bold')).grid(row=0, column=3, columnspan=2, sticky='nsew')
        search_fields = ["Name", "Gender (M/F)", "Type", "Breed", "Microchip #"]
        self.search_entries = {}

        #generate search gields using tkinter Entry widgets
        for i, field in enumerate(search_fields):
            tk.Label(self.root, text=field + ":").grid(row=i + 1, column=3, sticky='e')
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=4, sticky='ew', padx=5, pady=2)
            entry.config(width=30)
            self.search_entries[field] = entry

        #listbox to show results based on search criteria
        self.search_results = tk.Listbox(self.root, height=10)
        self.search_results.grid(row=6, column=3, columnspan=2, rowspan=6, sticky='nsew', padx=5)
        self.search_results.bind("<<ListboxSelect>>", self.show_animal_details)

        tk.Button(self.root, text="SEARCH", command=self.search_animals).grid(row=5, column=4, sticky='e', pady=10)

# =============================================================================
# File Dialog Utility — Upload image for animal profile
# =============================================================================

    def upload_image(self):
        """
        Opens a file dialog for image selection and stores the file path.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
        if filepath:
            self.image_path = filepath

# =============================================================================
# Result Display — Show animal details in pop-up window
# =============================================================================

    def show_animal_details(self, event):
        """
        Displays detailed profile info for a selected animal from the search list.
        Includes name, type, health data, etc. if available.
        """
        selection = self.search_results.curselection()
        if not selection:
            return

        selected_text = self.search_results.get(selection[0]) 
        name = selected_text.split(" (")[0] #parse name from display string

        for idx, animal in enumerate(self.animals):
            if animal.name == name:
                detail_win = Toplevel(self.root)
                detail_win.title(f"Details for {animal.name}")
                detail_win.geometry("500x600")

                #assemble formatted information string
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

                #render information as label
                label = tk.Label(detail_win, text=info, justify='left', anchor='nw')
                label.pack(fill='both', expand=True, padx=10, pady=10)

                #if image path exists and is valid display profile image
                if animal.image_path and os.path.exists(animal.image_path):
                    img = Image.open(animal.image_path)
                    img.thumbnail((300, 300))
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(detail_win, image=img_tk)
                    img_label.image = img_tk  # Keep reference
                    img_label.pack(pady=5)

                # ------------------------------------------------------------------
                # Nested window for updating animal information
                # ------------------------------------------------------------------

                def open_update_window():
                    update_win = Toplevel(detail_win)
                    update_win.title(f"Update {animal.name}")
                    update_win.geometry("400x600")
                    entries = {}
                    fields = ["Name", "Gender (M/F)", "Type (dog, cat, exotic)", "Breed", "Weight (lb.)", "DOB (YYYY-MM-DD)", "Microchip #", "Health Notes", "Description"]
                    
                    #generate entry form with prefilled data
                    for i, field in enumerate(fields):
                        tk.Label(update_win, text=field + ":").grid(row=i, column=0, sticky='e', padx=5, pady=5)
                        ent = tk.Entry(update_win, width=30)
                        ent.grid(row=i, column=1, padx=5, pady=5)
                        entries[field] = ent

                    #Populate fields with existing data
                    entries["Name"].insert(0, animal.name)
                    entries["Gender (M/F)"].insert(0, animal.gender)
                    entries["Type (dog, cat, exotic)"].insert(0, animal.animal_type)
                    entries["Breed"].insert(0, animal.breed)
                    entries["Weight (lb.)"].insert(0, animal.weight)
                    entries["DOB (YYYY-MM-DD)"].insert(0, animal.dob)
                    entries["Microchip #"].insert(0, animal.microchip_number)
                    entries["Health Notes"].insert(0, animal.health_notes)
                    entries["Description"].insert(0, animal.description)

                    #optional image update
                    def upload_new_image():
                        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
                        if path:
                            animal.image_path = path

                    tk.Button(update_win, text="Upload New Image", command=upload_new_image).grid(row=len(fields), column=0, columnspan=2)

                    #save validation and updating logic
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

                        #update object properties with validated values
                        animal.name = entries["Name"].get().strip()
                        animal.gender = gender_val
                        animal.animal_type = entries["Type (dog, cat, exotic)"].get().strip().lower()
                        animal.breed = entries["Breed"].get().strip()
                        animal.weight = entries["Weight (lb.)"].get().strip()
                        animal.dob = dob_input
                        animal.microchip_number = entries["Microchip #"].get().strip()
                        animal.health_notes = entries["Health Notes"].get().strip()
                        animal.description = entries["Description"].get().strip()

                        #commit to persistent storage
                        self.save_animals_to_file()
                        messagebox.showinfo("Success", "Animal updated successfully!")
                        update_win.destroy()
                        detail_win.destroy()
                        self.search_results.delete(0, tk.END)

                    tk.Button(update_win, text="Save Changes", command=save_updates).grid(row=len(fields) + 1, column=1, pady=10)

                tk.Button(detail_win, text="Update Animal", command=open_update_window).pack(pady=5)

                # ------------------------------------------------------------------
                # Option to delete animal record with confirmation prompt
                # ------------------------------------------------------------------

                def delete_animal():
                    if messagebox.askyesno("Confirm Delete", f"Delete {animal.name}?"):
                        self.animals.pop(idx)
                        self.save_animals_to_file()
                        self.search_results.delete(0, tk.END)
                        detail_win.destroy()
                        messagebox.showinfo("Deleted", f"{animal.name} has been deleted.")

                tk.Button(detail_win, text="Delete Animal", fg="red", command=delete_animal).pack(pady=5)
                break

# =============================================================================
# Data Management Functions — Save, Load, and Search Animal Records
#==============================================================================
    def save_animal(self):
        """
        Validates and captures input from onboarding form to create a new animal record.
        Handles type resolution, object instantiation, and data persistence.
        """
        #retrieve and clean input values
        name = self.entries["Name"].get().strip()
        gender = self.entries["Gender (M/F)"].get().strip().upper()
        type_ = self.entries["Type (dog, cat, exotic)"].get().strip().lower()

        #gather remaining inputs into a dictionary for object construction
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

        #validate required fields
        if not name or gender not in ("M", "F") or not type_ or not kwargs["breed"]:
            messagebox.showerror("Error", "Please fill required fields correctly.")
            return

        #validate date format
        if kwargs["dob"]:
            try:
                datetime.datetime.strptime(kwargs["dob"], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format.")
                return

        #resolve class type from input and instantiate object
        cls = {"cat": Cat, "dog": Dog, "exotic": Exotic}.get(type_, Animal)
        animal = cls(**kwargs)
        self.animals.append(animal)  #append to live memory

        #commit update to file
        self.save_animals_to_file()

        #UI feedback and cleanup
        messagebox.showinfo("Success", "Animal added successfully!")
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.image_path = ""  # Reset image

# -----------------------------------------------------------------------------

    def search_animals(self):
        """
        Filters the animal records in memory using user-defined criteria.
        Displays matching entries in the search results listbox.
        """
        self.search_results.delete(0, tk.END) #clear old results

        #retrieve filter values
        name_filter = self.search_entries["Name"].get().lower()
        gender_filter = self.search_entries["Gender (M/F)"].get().upper()
        type_filter = self.search_entries["Type"].get().lower()
        breed_filter = self.search_entries["Breed"].get().lower()
        microchip_filter = self.search_entries["Microchip #"].get()

        #loop through animal records and apply filters
        for animal in self.animals:
            if (name_filter in animal.name.lower() and
                (gender_filter == "" or gender_filter == animal.gender) and
                type_filter in animal.animal_type.lower() and
                breed_filter in animal.breed.lower() and
                microchip_filter in animal.microchip_number):
                #display matched animal
                self.search_results.insert(tk.END, f"{animal.name} ({animal.animal_type}, {animal.breed})")

# -----------------------------------------------------------------------------

    def save_animals_to_file(self):
        """
        Serializes all current animal records to a JSON file for persistence.
        """
        with open("animals.json", "w") as file:
            json.dump([animal.to_dict() for animal in self.animals], file, indent=2)

#------------------------------------------------------------------------------

    def load_animals(self):
        """
        Loads animal records from the local JSON file and reconstructs object instances.
        Handles file absence and decoding errors gracefully.
    
        Returns:
            List of Animal (or subclass) instances
        """
        try:
            with open("animals.json", "r") as file:
                data = json.load(file)
                loaded = []
                for entry in data:
                    #determine appropriate class for deserialization
                    cls = {"cat": Cat, "dog": Dog, "exotic": Exotic}.get(entry.get("type", "animal"), Animal)
                    loaded.append(cls(entry["name"], entry.get("gender", ""), entry["breed"],
                                      entry["weight"], entry["dob"], entry["microchip"],
                                      entry["health_notes"], entry["description"], entry.get("image_path", "")))
                return loaded
        except (FileNotFoundError, json.JSONDecodeError):
            return [] #return empty list upon fialure

# =============================================================================
# Application Entry Point — Launches GUI
# =============================================================================

if __name__ == '__main__':
    root = tk.Tk()
    app = AnimalPortal(root)
    root.mainloop()
