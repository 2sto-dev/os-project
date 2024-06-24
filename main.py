import tkinter as tk
import csv
import os
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from playsound import playsound
import requests
import webbrowser
from io import BytesIO
import spoonacular as sp
import pandas as pd

BUTTON_CLICK_SOUND = "clicks.wav"
WINDOW_TITLE = "Recipe App"
RECIPE_IMAGE_WIDTH = 350
RECIPE_IMAGE_HEIGHT = 350
ERROR_IMAGE_WIDTH = 100
ERROR_IMAGE_HEIGHT = 100

class RecipeApp(object):

    def __init__(self, recipe_app_key):
        self.recipe_app_key = recipe_app_key
        self.window = tk.Tk()
        self.window.configure(bg="#FBF3D5")
        self.window.geometry("800x600")
        self.window.configure(bg="#9CAFAA")
        self.window.title(WINDOW_TITLE)

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=1, fill="both")

        self.search_frame = tk.Frame(self.notebook, bg="#FBF3D5")
        self.add_frame = tk.Frame(self.notebook, bg="#FBF3D5")
        self.view_frame = tk.Frame(self.notebook, bg="#FBF3D5")
        self.suggestions_frame = tk.Frame(self.notebook, bg="#FBF3D5")

        self.notebook.add(self.search_frame, text="Search Recipe")
        self.notebook.add(self.add_frame, text="Add Recipe")
        self.notebook.add(self.view_frame, text="View Recipes")
        self.notebook.add(self.suggestions_frame, text="Suggestions")

        self.titles = self.load_titles()

        self.setup_search_frame()
        self.setup_add_frame()
        self.setup_view_frame()
        self.setup_suggestions_frame()

    def setup_search_frame(self):
        self.search_label = tk.Label(self.search_frame, text="Search Recipe", bg="#EFBC9B")
        self.search_label.grid(column=0, row=0, padx=5)

        self.search_entry = tk.Entry(master=self.search_frame, width=40)
        self.search_entry.grid(column=1, row=0, padx=5, pady=10)

        self.cuisine_label = tk.Label(self.search_frame, text="Preferred Cuisine", bg="#EFBC9B")
        self.cuisine_label.grid(column=0, row=1, padx=5)

        self.cuisine_var = tk.StringVar(self.search_frame)
        self.cuisine_var.set('Select Cuisine')
        self.cuisine_menu = tk.OptionMenu(self.search_frame, self.cuisine_var, 'British', 'Italian', 'Mexican', 'Indian', 'Chinese')
        self.cuisine_menu.grid(column=1, row=1, padx=5, pady=10)

        self.diet_label = tk.Label(self.search_frame, text="Dietary Requirements", bg="#EFBC9B")
        self.diet_label.grid(column=0, row=2, padx=5)

        self.diet_var = tk.StringVar(self.search_frame)
        self.diet_var.set('Select Dietary Requirement')
        self.diet_menu = tk.OptionMenu(self.search_frame, self.diet_var, 'Vegetarian', 'Vegan', 'Alcohol-Free', 'Gluten-Free')
        self.diet_menu.grid(column=1, row=2, padx=5, pady=10)

        self.search_button = tk.Button(self.search_frame, text="Search",  bg="#9CAFAA", highlightbackground="#EFBC9B",
                                       command=self.__run_search_query)
        self.search_button.grid(column=2, row=2, padx=5)

        self.image_label = tk.Label(self.search_frame, bg="#9CAFAA")
        self.image_label.grid(column=1, row=5, pady=10)

    def setup_add_frame(self):
        title_label = tk.Label(self.add_frame, text="Recipe Title", bg = "#EFBC9B")
        title_label.grid(row=0, column=0, padx=10, pady=10)

        self.recipe_textbox = tk.Entry(self.add_frame)
        self.recipe_textbox.grid(row=0, column=1, padx=10, pady=10)

        ingredients_label = tk.Label(self.add_frame, text="Ingredients", bg = "#EFBC9B")
        ingredients_label.grid(row=1, column=0, padx=10, pady=10)

        self.ingredients_textbox = tk.Entry(self.add_frame)
        self.ingredients_textbox.grid(row=1, column=1, padx=10, pady=10)

        instructions_label = tk.Label(self.add_frame, text="Instructions", bg = "#EFBC9B")
        instructions_label.grid(row=2, column=0, padx=10, pady=10)

        self.instructions_textbox = tk.Text(self.add_frame, height=10, width=40)
        self.instructions_textbox.grid(row=2, column=1, padx=10, pady=10)

        add_button = tk.Button(self.add_frame, text="Add Recipe", bg="#9CAFAA",  command=self.add_recipe)
        add_button.grid(row=3, column=0, padx=10, pady=10)

        clear_button = tk.Button(self.add_frame, text="Clear", bg="#9CAFAA",  command=self.clear_textboxes)
        clear_button.grid(row=3, column=1, padx=10, pady=10)

    def load_titles(self):
        if os.path.exists("recipes.csv"):
            df = pd.read_csv("recipes.csv")
            titles = df['Recipe Title'].tolist()
            return titles
        else:
            return []

    def get_recipe_details(self, recipe_title, ingredients, instructions):
        recipe_details_window = tk.Toplevel(self.view_frame)
        recipe_details_window.title(recipe_title)

        title_label = tk.Label(recipe_details_window, text=recipe_title, font=("Arial", 20))
        title_label.pack(pady=10)

        ingredients_label = tk.Label(recipe_details_window, text="Ingredients", font=("Arial", 12))
        ingredients_label.pack(pady=5)
        ingredients_text = tk.Text(recipe_details_window, height=10, width=50)
        ingredients_text.pack(pady=5)
        ingredients_text.insert(tk.END, ingredients)
        ingredients_text.config(state=tk.DISABLED)

        instructions_label = tk.Label(recipe_details_window, text="Instructions", font=("Arial", 12))
        instructions_label.pack(pady=5)
        instructions_text = tk.Text(recipe_details_window, height=10, width=50)
        instructions_text.pack(pady=5)
        instructions_text.insert(tk.END, instructions)
        instructions_text.config(state=tk.DISABLED)
    def on_search_button_clicked(self):
        playsound(BUTTON_CLICK_SOUND)
        selected_title = self.title_var.get()
        if selected_title != 'Select Title':
            if os.path.exists("recipes.csv"):
                df = pd.read_csv("recipes.csv")
                recipe = df[df['Recipe Title'] == selected_title]
                if not recipe.empty:
                    ingredients = recipe.iloc[0]['Ingredients']
                    instructions = recipe.iloc[0]['Instructions']
                    self.get_recipe_details(selected_title, ingredients, instructions)
                else:
                    messagebox.showerror("Error", "Recipe details not found.")
            else:
                messagebox.showerror("Error", "Recipe file not found.")
        else:
            messagebox.showerror("Error", "Please select a title.")

    def setup_view_frame(self):
        self.title_label = tk.Label(self.view_frame, text="Look for a title", bg="#EFBC9B")
        self.title_label.grid(column=0, row=0, padx=10, pady=20)

        self.title_var = tk.StringVar(self.view_frame)
        self.title_var.set('Select Title')
        self.recipe_titles = tk.OptionMenu(self.view_frame, self.title_var, *self.titles)
        self.recipe_titles.grid(column=1, row=0, padx=10, pady=10)

        self.search_button = tk.Button(self.view_frame, text="Search", bg="#9CAFAA", highlightbackground="#EFBC9B",
                                       command=self.on_search_button_clicked)
        self.search_button.grid(column=2, row=0, padx=5)


    def setup_suggestions_frame(self):
        suggestion_label = tk.Label(self.suggestions_frame, text="Suggestions", font=("Arial", 18), bg="#EFBC9B")
        suggestion_label.pack(pady=10)

        sweet_var = tk.BooleanVar()
        salty_var = tk.BooleanVar()

        sweet_checkbox = tk.Checkbutton(self.suggestions_frame, text="Sweet", variable=sweet_var, bg="#FBF3D5")
        sweet_checkbox.pack(pady=5)

        salty_checkbox = tk.Checkbutton(self.suggestions_frame, text="Salty", variable=salty_var, bg="#FBF3D5")
        salty_checkbox.pack(pady=5)

        def on_ok():
            if sweet_var.get():
                self.sweet_suggestion()
            if salty_var.get():
                self.salty_suggestion()

        ok_button = tk.Button(self.suggestions_frame, text="OK", bg="#9CAFAA", command=on_ok)
        ok_button.pack(pady=10)

    def add_recipe(self):
        playsound(BUTTON_CLICK_SOUND)
        recipe_title = self.recipe_textbox.get()
        ingredients = self.ingredients_textbox.get()
        instructions = self.instructions_textbox.get("1.0", tk.END).strip()

        file_exists = os.path.exists("recipes.csv")

        with open("recipes.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Recipe Title", "Ingredients", "Instructions"])
            writer.writerow([recipe_title, ingredients, instructions])

        self.clear_textboxes()

    def clear_textboxes(self):
        playsound(BUTTON_CLICK_SOUND)
        self.recipe_textbox.delete(0, tk.END)
        self.ingredients_textbox.delete(0, tk.END)
        self.instructions_textbox.delete("1.0", tk.END)

    def sweet_suggestion(self):
        sweet_window = tk.Toplevel(self.suggestions_frame)
        sweet_window.title("Sweet Options")

        option_label = tk.Label(sweet_window, text="What would you like to have in it?")
        option_label.grid(row=0, column=0, padx=10, pady=10)

        walnut_var = tk.BooleanVar()
        carrot_var = tk.BooleanVar()
        chocolate_var = tk.BooleanVar()

        walnut_checkbox = tk.Checkbutton(sweet_window, text="Walnut", variable=walnut_var)
        carrot_checkbox = tk.Checkbutton(sweet_window, text="Carrot", variable=carrot_var)
        chocolate_checkbox = tk.Checkbutton(sweet_window, text="Chocolate", variable=chocolate_var)

        walnut_checkbox.grid(row=1, column=0, padx=10, pady=10)
        carrot_checkbox.grid(row=2, column=0, padx=10, pady=10)
        chocolate_checkbox.grid(row=3, column=0, padx=10, pady=10)

        def on_sweet_ok():
            options = []
            if walnut_var.get():
                options.append("Walnut")
            if carrot_var.get():
                options.append("Carrot")
            if chocolate_var.get():
                options.append("Chocolate")
            messagebox.showinfo("Suggestion", f"Here's a sweet recipe suggestion with {', '.join(options)}.")

            if "Walnut" in options:
                messagebox.showinfo("Suggestions", f"You can try Walnuts cookies. Go to recipes or add a new one")
            if "Carrot" in options:
                messagebox.showinfo("Suggestions", f"You can try Carrot Cake. Go to recipes or add a new one")
            if "Chocolate" in options:
                messagebox.showinfo("Suggestions", f"You can try Lava Cake. Go to recipes, or add a new one.")

        sweet_ok_button = tk.Button(sweet_window, text="OK", command=on_sweet_ok)
        sweet_ok_button.grid(row=4, column=0, padx=10, pady=10)

    def salty_suggestion(self):
        sweet_window = tk.Toplevel(self.suggestions_frame)
        sweet_window.title("Sweet Options")

        option_label = tk.Label(sweet_window, text="What would you like to have in it?")
        option_label.grid(row=0, column=0, padx=10, pady=10)

        walnut_var = tk.BooleanVar()
        carrot_var = tk.BooleanVar()
        chocolate_var = tk.BooleanVar()

        walnut_checkbox = tk.Checkbutton(sweet_window, text="Lettuce", variable=walnut_var)
        carrot_checkbox = tk.Checkbutton(sweet_window, text="Avocado", variable=carrot_var)
        chocolate_checkbox = tk.Checkbutton(sweet_window, text="Parmesan Cheese", variable=chocolate_var)

        walnut_checkbox.grid(row=1, column=0, padx=10, pady=10)
        carrot_checkbox.grid(row=2, column=0, padx=10, pady=10)
        chocolate_checkbox.grid(row=3, column=0, padx=10, pady=10)

        def on_salty_ok():
            options = []
            if walnut_var.get():
                options.append("Lettuce")
            if carrot_var.get():
                options.append("Avocado")
            if chocolate_var.get():
                options.append("Parmesan Cheese")
            messagebox.showinfo("Suggestion", f"Here's a salty recipe suggestion with {', '.join(options)}.")

            if "Lettuce" in options:
                messagebox.showinfo("Suggestions", f"You can try Caesar Salad. Go to recipes or add a new one")
            if "Avocado" in options:
                messagebox.showinfo("Suggestions", f"You can try Guacamole. Go to recipes or add a new one")
            if "Parmesan Cheese" in options:
                messagebox.showinfo("Suggestions", f"You can try Spaghetti Carbonara. Go to recipes, or add a new one.")

        sweet_ok_button = tk.Button(sweet_window, text="OK", command=on_salty_ok)
        sweet_ok_button.grid(row=4, column=0, padx=10, pady=10)

    def __run_search_query(self):
        playsound(BUTTON_CLICK_SOUND)
        query = self.search_entry.get()
        cuisine = self.cuisine_var.get()
        diet = self.diet_var.get()

        # Create a search query string incorporating cuisine and diet if provided
        query_string = query
        if cuisine.lower() != 'select cuisine':
            query_string += f" {cuisine}"
        if diet.lower() != 'select dietary requirement':
            query_string += f" {diet}"

        # Make API call to spoonacular
        try:
            api = sp.API(self.recipe_app_key)
            response = api.search_recipes_complex(query_string)
            data = response.json()
            recipes = data['results']

            if recipes:
                first_recipe = recipes[0]
                recipe_id = first_recipe['id']
                recipe_details = api.get_recipe_information(recipe_id).json()

                title = recipe_details['title']
                image_url = recipe_details['image']
                ingredients = ', '.join([ingredient['name'] for ingredient in recipe_details['extendedIngredients']])
                instructions = recipe_details['instructions']

                self.show_recipe_details(title, image_url, ingredients, instructions)
            else:
                self.show_error_image("No recipes found")
        except Exception as e:
            self.show_error_image("Error occurred while fetching recipes")
            print(f"Error: {e}")

    def show_recipe_details(self, title, image_url, ingredients, instructions):
        response = requests.get(image_url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image = image.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection

        details_window = tk.Toplevel(self.search_frame)
        details_window.title(title)

        title_label = tk.Label(details_window, text=title, font=("Arial", 20))
        title_label.pack(pady=10)

        ingredients_label = tk.Label(details_window, text="Ingredients")
        ingredients_label.pack(pady=5)
        ingredients_text = tk.Text(details_window, height=10, width=50)
        ingredients_text.pack(pady=5)
        ingredients_text.insert(tk.END, ingredients)
        ingredients_text.config(state=tk.DISABLED)

        instructions_label = tk.Label(details_window, text="Instructions")
        instructions_label.pack(pady=5)
        instructions_text = tk.Text(details_window, height=10, width=50)
        instructions_text.pack(pady=5)
        instructions_text.insert(tk.END, instructions)
        instructions_text.config(state=tk.DISABLED)

    def show_error_image(self, error_message):
        image = Image.open("error.jpg")
        image = image.resize((ERROR_IMAGE_WIDTH, ERROR_IMAGE_HEIGHT), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection
        self.image_label.configure(text=error_message, compound=tk.CENTER, font=("Arial", 20))

    def run_app(self):
        self.window.mainloop()

if __name__ == "__main__":
    API_KEY = "8132ca85339840f49be1266085869104"
    recipe_app = RecipeApp(API_KEY)
    recipe_app.run_app()
