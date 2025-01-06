#import python, tkinter, mysql libraries
import re
from tkinter import *
from tkinter import filedialog
import mysql.connector as myconn
import tkinter.messagebox as msg
import tkinter.ttk as ttk
import datetime
import time
import os
import sys
from PIL import ImageTk, Image
from fpdf import FPDF


#connect to database

database = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'rf'
}

#create connection to database
connector = myconn.connect(**database)

create_sql_queries = '''

CREATE TABLE IF NOT EXISTS USER (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS RECIPE (
    recipeID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    title VARCHAR(100) NOT NULL,
    cuisine VARCHAR(50),
    recipe_image VARCHAR(255),
    rating float DEFAULT 0,
    vegetarian BOOLEAN DEFAULT 0,
    recipe_video VARCHAR(255),
    FOREIGN KEY (userID) REFERENCES USER(userID)
);

CREATE TABLE IF NOT EXISTS INGREDIENT (
    ingredientID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS RECIPE_INGREDIENT (
    recipe_ingredientID INT AUTO_INCREMENT PRIMARY KEY,
    recipeID INT,
    ingredientID INT,
    FOREIGN KEY (recipeID) REFERENCES RECIPE(recipeID),
    FOREIGN KEY (ingredientID) REFERENCES INGREDIENT(ingredientID)
);
'''

#run the command
with connector.cursor() as cursor:
    cursor.execute(create_sql_queries)
    print("Database created successfully")

class rf:
    #constructor class constructor
    def __init__(self,app) :
        self.app=app
        #give title
        self.app.title("Recipe Finder")

        #set window size
        self.app.geometry("600x700")

        self.database = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'rf'
        }

        #open bg.jpg file
        # open bidmaster image
        self.openimage = Image.open('images/bg.jpg')
        # resize to dimensions
        self.openimage = self.openimage.resize((600, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #cox cuisine title Century Gothic
        self.title = Label(self.app, text="Recipe Finder", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=200, y=300)


        self.all_ingrediants = []
        self.my_ingrediants = []
        self.all_recipes = []
        self.my_selected_receipes = []

        #get all ingrediants
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM INGREDIENT")
        self.all_ingrediants = cursor.fetchall()

        #get all recipes
        cursor.execute("SELECT * FROM RECIPE")
        self.all_recipes = cursor.fetchall()

        self.my_selected_receipes = self.all_recipes[:]

        #open after 4 seconds
        self.app.after(2000, self.login)

    #login function
    def login(self):
        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

        
        #set window size
        self.app.geometry("600x700")

        #load image
        self.openimage = Image.open('images/bg.jpg') 
        self.openimage = self.openimage.resize((600, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #place login details 
        self.title = Label(self.app, text="Login", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=250, y=150)

        #username label
        self.username_label = Label(self.app, text="Username", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.username_label.place(x=150, y=250)

        #username entry
        self.username_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.username_entry.place(x=250, y=250)

        #password label
        self.password_label = Label(self.app, text="Password", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.password_label.place(x=150, y=300)

        #password entry
        self.password_entry = Entry(self.app, font=("Century Gothic", 15, "bold"), show="*")
        self.password_entry.place(x=250, y=300)

        #eye image
        self.eye=Image.open("images/eye.jpg")
        self.eye=self.eye.resize((20, 20), Image.LANCZOS)
        self.eye=ImageTk.PhotoImage(self.eye)
        self.eye_button=Button(self.app, image=self.eye, bg="#f8f9fb", command=self.eye_click)
        self.eye_button.image=self.eye
        self.eye_button.place(x=470, y=300)



        #login button
        self.login_button = Button(self.app, text="Login", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.login_user)
        self.login_button.place(x=250, y=350)

        #register button
        self.register_button = Button(self.app, text="Register", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.register)
        self.register_button.place(x=350, y=350)

        #forgot_password_button = Button(self.app, text="For
        self.forgot_password_button = Button(self.app, text="Forgot Password", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.forgot_password)
        self.forgot_password_button.place(x=250, y=400)

    #forgot password function
    def forgot_password(self):
         #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

        #load image
        self.openimage = Image.open('images/bg.jpg')
        self.openimage = self.openimage.resize((600, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #place register details
        self.title = Label(self.app, text="Forgot Password", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=150, y=150)

        #email label
        self.email_label = Label(self.app, text="Email", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.email_label.place(x=150, y=250)

        #email entry
        self.email_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.email_entry.place(x=250, y=250)

        #password label
        self.password_label = Label(self.app, text="New Password", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.password_label.place(x=80, y=300)

        #password entry
        self.password_entry = Entry(self.app, font=("Century Gothic", 15, "bold"), show="*")
        self.password_entry.place(x=250, y=300)

        #register button
        self.register_button = Button(self.app, text="Update Password", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.update_password)
        self.register_button.place(x=250, y=350)

        #login button
        self.login_button = Button(self.app, text="Login", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.login)
        self.login_button.place(x=250, y=400)

    #update_password
    def update_password(self):
        #take input
        email = self.email_entry.get()
        password = self.password_entry.get()

        #check if email and password are empty
        if email == "" or password == "":
            msg.showerror("Error", "Please fill in all fields")
        else:
           #check if email is alredy registered
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()
            cursor.execute("SELECT * FROM USER WHERE email=%s", (email,))
            user = cursor.fetchone()
            if user:
                #update password
                self.connector = myconn.connect(**self.database)
                cursor = self.connector.cursor()
                cursor.execute("UPDATE USER SET password=%s WHERE email=%s", (password, email))
                self.connector.commit()
                msg.showinfo("Success", "Password updated successfully")
                self.login()
            else:
                msg.showerror("Error", "Email not registered")
        


    
    #event handler for eye button
    def eye_click(self):
        if self.password_entry.config()['show'][4] == '*':
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    #login user function
    def login_user(self):
        #get username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        #if admin
        if username == "admin" and password == "admin":
            self.admin_menu()
            self.curremt_user = "admin"
            return


        #check if username and password are empty
        if username == "" or password == "":
            msg.showerror("Error", "Please fill in all fields")
        else:
            #check if user exists
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()
            cursor.execute("SELECT * FROM USER WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()

            #if user exists
            if user:
                #open main menu
                self.main_menu()
                self.current_user = 'user'
                self.user_id = user[0]
                self.user_name = user[1]
                self.user_email = user[2]


            else:
                msg.showerror("Error", "Invalid username or password")


    #admin_menu
    def admin_menu(self):
        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

       #dimensions 1000x600
        self.app.geometry("1000x600")

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #left vertical frame for notebook
        self.left_frame = Frame(self.app, bg="#f8f9fb")
        self.left_frame.place(x=100, y=100, width=400, height=430)

        #scrollbar to left frame
        self.scrollbar = Scrollbar(self.left_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        #Indian button text color 04af8f
        self.indian_button = Button(self.left_frame, text="Add Recipe", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.add_recipe_page)
        self.indian_button.pack(pady=10)

        #Italian button text color 04af8f
        # self.italian_button = Button(self.left_frame, text="Update Recipe", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.update_recipe_page)
        # self.italian_button.pack(pady=10)

        #Chinese button text color 04af8f
        self.chinese_button = Button(self.left_frame, text="Add Ingredient", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.add_ingredient_page)
        self.chinese_button.pack(pady=10)
        #delete recipe 
        self.delete_recipe_button = Button(self.left_frame, text="Delete Recipe", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.delete_recipe)
        self.delete_recipe_button.pack(pady=10)

        #download reports
        self.download_report_button = Button(self.left_frame, text="Recipe Reports", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.download_recipe_report)
        self.download_report_button.pack(pady=10)

        #download ingredients reports
        self.download_ingredient_report_button = Button(self.left_frame, text="Ingredient Reports", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.download_ingredient_report)
        self.download_ingredient_report_button.pack(pady=10)

        #logout
        self.logout_button = Button(self.left_frame, text="Logout", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.login)
        self.logout_button.pack(pady=10)
        
        #right frame
        self.right_frame = Frame(self.app, bg="#f8f9fb")
        self.right_frame.place(x=400, y=100, width=500, height=600)
        
        #treeview of all recipes
        self.treeview = ttk.Treeview(self.right_frame, columns=("title", "cuisine", "rating", "vegetarian"))

        self.treeview['show'] = 'headings'


        self.treeview.heading("#1", text="Title")
        self.treeview.heading("#2", text="Cuisine")
        self.treeview.heading("#3", text="Rating")
        self.treeview.heading("#4", text="Vegetarian")
        self.treeview.column("#1", width=100)
        self.treeview.column("#2", width=100)
        self.treeview.column("#3", width=100)
        self.treeview.column("#4", width=100)

        self.treeview.pack()

        #get all recipes
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM RECIPE")
        self.all_recipes = cursor.fetchall()
        for i,recipe in enumerate(self.all_recipes):
            recipe_name = recipe[2]
            recipe_cuisine = recipe[3]
            recipe_rating = recipe[5]
            recipe_vegetarian = recipe[6]
            self.treeview.insert("", "end", values=(recipe_name, recipe_cuisine, recipe_rating, recipe_vegetarian))

        self.connector.commit()

    #download report function
    def download_recipe_report(self):
        #get all recipes and print to pdf file
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM RECIPE")
        recipes = cursor.fetchall()
        self.connector.commit()
        #print recipes to  as  table column rows format
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        #todays date and time
        #top left corner
        pdf.cell(200, 10, txt="Date: " + str(datetime.datetime.now()), ln=True)

        #add title to page
        pdf.cell(200, 10, txt="Recipes Report", ln=1, align="C")

        #add header to table
        pdf.cell(50, 10, txt="Title", border=1)
        pdf.cell(50, 10, txt="Cuisine", border=1)
        pdf.cell(50, 10, txt="Rating", border=1)
        pdf.cell(50, 10, txt="Vegetarian", border=1)
        pdf.ln()

        #add ride data to table
        for recipe in recipes:
            recipe_title = recipe[2]
            recipe_cuisine = recipe[3]
            recipe_rating = str(recipe[5])
            recipe_vegetarian = str(recipe[6])

            pdf.cell(50, 10, txt=recipe_title, border=1)
            pdf.cell(50, 10, txt=recipe_cuisine, border=1)
            pdf.cell(50, 10, txt=recipe_rating, border=1)
            pdf.cell(50, 10, txt=recipe_vegetarian, border=1)
    
            pdf.ln()

        #output pdf file
        pdf.output("recipes.pdf")

        #message
        msg.showinfo("Success", "Recipe Report downloaded successfully")
        self.admin_menu()

    #download ingredient report function
    def download_ingredient_report(self):
        #get all recipes and print to pdf file
        
        #ingredients reports
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()    
        cursor.execute("SELECT * FROM INGREDIENT")
        ingredients = cursor.fetchall()
        self.connector.commit()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        #add date and time
        pdf.cell(200, 10, txt="Date: " + str(datetime.datetime.now()), ln=True)

        #add title
        pdf.cell(200, 10, txt="Ingredients Report", ln=True)
        pdf.ln()
        #add header
        pdf.cell(50, 10, txt="Ingredient", border=1)
        pdf.ln()
        #add data
        for ingredient in ingredients:
            ingredient_name = ingredient[1]
            pdf.cell(50, 10, txt=ingredient_name, border=1)
            pdf.ln()
        pdf.output("ingredients.pdf")
        msg.showinfo("Success", "Ingredients Report downloaded successfully")
        self.admin_menu()


    #delete recipe function
    def delete_recipe(self):
        #get selected recipe
        selected_recipe = self.treeview.item(self.treeview.selection())['values']

        if selected_recipe:
            #delete recipe from database
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()

            #get id of selected recipe
            cursor.execute("SELECT recipeID FROM RECIPE WHERE title=%s", (selected_recipe[0],))
            recipe_id = cursor.fetchone()
            recipe_id = recipe_id[0]

            #from recipe ingredients delete all where recipeID = recipe_id
            cursor.execute("DELETE FROM RECIPE_INGREDIENT WHERE recipeID=%s", (recipe_id,))

            cursor.execute("DELETE FROM RECIPE WHERE recipeID=%s", (recipe_id,))

            self.connector.commit()

            msg.showinfo("Success", "Recipe deleted successfully")
            self.admin_menu()
        else:
            msg.showerror("Error", "Please select a recipe to delete")

    #add ingredient page
    def add_ingredient_page(self):
        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

        #dimensions 1000x600
        self.app.geometry("1000x600")

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #place add ingredient details
        self.title = Label(self.app, text="Add Ingredient", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=250, y=50)

        #ingredient label
        self.ingredient_label = Label(self.app, text="Ingredient", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.ingredient_label.place(x=150, y=150)

        #ingredient entry
        self.ingredient_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.ingredient_entry.place(x=350, y=150)

        #add ingredient button
        self.add_ingredient_button = Button(self.app, text="Add Ingredient", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.add_ingredient_bd)
        self.add_ingredient_button.place(x=250, y=200)

        #back
        self.back_button = Button(self.app, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.admin_menu)
        self.back_button.place(x=450, y=200)

        #frame for treeview
        self.frame = Frame(self.app, bg="#f8f9fb")
        self.frame.place(x=250, y=250)

        #treeview
        self.treeview_ingredient = ttk.Treeview(self.frame, columns=("name",), show="headings")
        self.treeview_ingredient.heading("name", text="Ingredient")
        self.treeview_ingredient.pack(fill="both", expand=True)

        #get data from database
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM INGREDIENT")
        ingredients = cursor.fetchall()
        self.connector.commit()

        #add data to treeview_ingredient
        for ingredient in ingredients:
            self.treeview_ingredient.insert("", "end", text=ingredient[1], values=(ingredient[1],))

        #update ingredient button
        self.update_ingredient_button = Button(self.app, text="Update Ingredient", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.update_ingredient_page)
        self.update_ingredient_button.place(x=550, y=200)

        #delete ingredient button
        self.delete_ingredient_button = Button(self.app, text="Delete Ingredient", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.delete_ingredient_bd)
        self.delete_ingredient_button.place(x=550, y=250)


    #delete ingredient function
    def delete_ingredient_bd(self):
        #get selected ingredient
        selected_ingredient = self.treeview_ingredient.item(self.treeview_ingredient.selection())['values']
        if selected_ingredient:
            try:
                #delete ingredient from database
                self.connector = myconn.connect(**self.database)
                cursor = self.connector.cursor()
                cursor.execute("DELETE FROM INGREDIENT WHERE name=%s", (selected_ingredient[0],))
                self.connector.commit()
                msg.showinfo("Success", "Ingredient deleted successfully")
                self.admin_menu()
            except Exception as e:
                msg.showerror("Error", str(e))
                #messagebox cannot delete ingredient as it is linked to a recipe
                msg.showerror("Error", "Cannot delete ingredient as it is linked to a recipe")
        else:
            msg.showerror("Error", "Please select an ingredient to delete")


    #add ingredient function
    def add_ingredient_bd(self):
        #get ingredient
        ingredient = self.ingredient_entry.get()

        #check if ingredient is empty
        if ingredient == "":
            msg.showerror("Error", "Please fill in all fields")
        else:
            try:
                #insert ingredient into database
                self.connector = myconn.connect(**self.database)
                cursor = self.connector.cursor()
                cursor.execute("INSERT INTO INGREDIENT (name) VALUES (%s)", (ingredient,))
                self.connector.commit()
                msg.showinfo("Success", "Ingredient added successfully")
                self.admin_menu()
            except Exception as e:
                #messagebox ingredient already exists
                msg.showerror("Error", "Ingredient already exists")

    #update ingredient page
    def update_ingredient_page(self):

        #get selection from treeview_ingredient
        selected_ingredient = self.treeview_ingredient.item(self.treeview_ingredient.selection())['values']

        #get ingredient id from name
        ingredient_name = selected_ingredient[0]
        
        #connect to database
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM INGREDIENT WHERE name=%s", (ingredient_name,))
        ingredient = cursor.fetchone()
        self.connector.commit()

        self.current_ingredient_id = ingredient[0]



        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

        #dimensions 1000x600
        self.app.geometry("1000x600")

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #place update ingredient details
        self.title = Label(self.app, text="Update Ingredient", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=250, y=50)

        #ingredient label
        self.ingredient_label = Label(self.app, text="Ingredient", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.ingredient_label.place(x=150, y=150)

        #ingredient entry
        self.ingredient_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.ingredient_entry.place(x=350, y=150)
        self.ingredient_entry.insert(0, ingredient_name)

        #update ingredient button
        self.update_ingredient_button = Button(self.app, text="Update Ingredient", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.update_ingredient)
        self.update_ingredient_button.place(x=250, y=200)

        #back
        self.back_button = Button(self.app, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.admin_menu)
        self.back_button.place(x=450, y=200)

    #update ingredient function
    def update_ingredient(self):
        #get ingredient
        ingredient = self.ingredient_entry.get()

        #check if ingredient is empty
        if ingredient == "":
            msg.showerror("Error", "Please fill in all fields")
        else:
            #update ingredient in database
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()
            cursor.execute("UPDATE INGREDIENT SET name=%s WHERE ingredientID=%s", (ingredient, self.current_ingredient_id))
            self.connector.commit()
            msg.showinfo("Success", "Ingredient updated successfully")
            self.admin_menu()

    #update recipe page
    def update_recipe_page(self):
        #get selected recipe
        selected_recipe = self.treeview.item(self.treeview.selection())['values']
        if selected_recipe:
            #destroy previous window
            for i in self.app.winfo_children():
                i.destroy()

            #dimensions 1000x600
            self.app.geometry("1000x600")

            #get selected recipeid from db
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()
            cursor.execute("SELECT * FROM RECIPE WHERE title=%s", (selected_recipe[0],))
            selected_recipe = cursor.fetchone()
            self.connector.commit()
            recipe_id = selected_recipe[1]
            self.filename = selected_recipe[4]
            self.recipe_video_link= selected_recipe[7]


            #load image
            self.openimage = Image.open('images/menu_bg.jpg')
            self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
            self.image = ImageTk.PhotoImage(self.openimage)
            self.label = Label(self.app, image=self.image)
            self.label.pack()

            #place update recipe details
            self.title = Label(self.app, text="Update Recipe", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
            self.title.place(x=250, y=50)

            #title label
            self.title_label = Label(self.app, text="Title", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            self.title_label.place(x=150, y=150)

            #title entry
            self.title_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
            self.title_entry.place(x=350, y=150)
            self.title_entry.insert(0, selected_recipe[2])

            #cuisine label
            self.cuisine_label = Label(self.app, text="Cuisine", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            self.cuisine_label.place(x=150, y=200)

            #cuisine entry
            self.cuisine_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
            self.cuisine_entry.place(x=350, y=200)
            self.cuisine_entry.insert(0, selected_recipe[3])

            #rating label
            self.rating_label = Label(self.app, text="Rating", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            self.rating_label.place(x=150, y=250)

            #rating entry
            self.rating_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
            self.rating_entry.place(x=350, y=250)
            self.rating_entry.insert(0, selected_recipe[5])

            #vegetarian label
            self.vegetarian_label = Label(self.app, text="Vegetarian", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            self.vegetarian_label.place(x=150, y=300)
            self.vegetarian_var = IntVar()
            self.vegetarian_var.set(selected_recipe[6])

            #vegetarian entry
            self.vegetarian_entry = Checkbutton(self.app, variable=self.vegetarian_var, font=("Century Gothic", 15, "bold"))
            self.vegetarian_entry.place(x=350, y=300)

            #recipe video label
            self.recipe_video_label = Label(self.app, text="Recipe Video", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            self.recipe_video_label.place(x=150, y=350)

            #recipe video entry
            self.recipe_video_entry = Entry(self.app ,font=("Century Gothic", 15, "bold"))
            self.recipe_video_entry.place(x=350, y=350)
            self.recipe_video_entry.insert(0, self.recipe_video_link)

            #recipe image label
            self.recipe_image_label = Label(self.app, text="Recipe Image", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            self.recipe_image_label.place(x=650, y=200)

            #recipe image button
            self.recipe_image_button = Button(self.app, text="Upload", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.upload_image)
            self.recipe_image_button.place(x=650, y=250)

            #select ingredients
            self.add_ingredients_button = Button(self.app, text="Select Ingredients", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.select_ingredients)
            self.add_ingredients_button.place(x=650, y=350)
            self.ingredients_label = Label(self.app, text="Ingredients", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            self.ingredients_label.place(x=650, y=400)

            #add recipe button
            self.add_recipe_button = Button(self.app, text="Update Recipe", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.update_recipe)
            self.add_recipe_button.place(x=350, y=450)

            #back
            self.back_button = Button(self.app, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.admin_menu)
            self.back_button.place(x=550, y=450)
        else:
            msg.showerror("Error", "Please select a recipe to update")

    #update recipe function
    def update_recipe(self):
        #get title, cuisine, rating, vegetarian, recipe image and recipe video
        title = self.title_entry.get()
        cuisine = self.cuisine_entry.get()
        rating = self.rating_entry.get()
        vegetarian = self.vegetarian_var.get()
        recipe_video = self.recipe_video_entry.get()

        #get recipe id
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT recipeID FROM RECIPE WHERE title=%s", (title,))
        recipe_id = cursor.fetchone()
        recipe_id = recipe_id[0]

        #check if title, cuisine, rating, vegetarian, recipe image and recipe video are empty
        if title == "" or cuisine == "" or rating == "" or vegetarian == "" or recipe_video == "":
            msg.showerror("Error", "Please fill in all fields")
        else:
            #update recipe in database
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()
            cursor.execute("UPDATE RECIPE SET title=%s, cuisine=%s, rating=%s, vegetarian=%s, recipe_image=%s, recipe_video=%s WHERE title=%s", (title, cuisine, rating, vegetarian, self.filename, recipe_video, title))
            self.connector.commit()
            msg.showinfo("Success", "Recipe updated successfully")
            #insert ingredients into database
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()
            for ingredient in self.selected_ingredients:
                #insert only if not exists in recipe_ingredient table
                cursor.execute("SELECT ingredientID FROM RECIPE_INGREDIENT WHERE recipeID=%s AND ingredientID=%s", (recipe_id, ingredient))
                ingredient_id = cursor.fetchone()
                ingredient_id = ingredient_id[0]
                if ingredient_id == None:
                    cursor.execute("INSERT INTO RECIPE_INGREDIENT (recipeID, ingredientID) VALUES (%s, %s)", (recipe_id, ingredient))
                else:
                    #messagebox ingredient already exists
                    msg.showerror("Error", "Ingredient already exists in recipe, so skipping inserting", ingredient)
            self.connector.commit()

            self.admin_menu()

    #add recipe page
    def add_recipe_page(self):
        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

       #dimensions 1000x600
        self.app.geometry("1000x600")

        self.selected_ingredients = []

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #place add recipe details
        self.title = Label(self.app, text="Add Recipe", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=250, y=50)

        #title label
        self.title_label = Label(self.app, text="Title", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.title_label.place(x=150, y=150)

        #title entry
        self.title_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.title_entry.place(x=350, y=150)

        #cuisine label
        self.cuisine_label = Label(self.app, text="Cuisine", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.cuisine_label.place(x=150, y=200)

        #cuisine entry
        self.cuisine_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.cuisine_entry.place(x=350, y=200)

        #rating label
        self.rating_label = Label(self.app, text="Rating", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.rating_label.place(x=150, y=250)

        #rating entry
        self.rating_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.rating_entry.place(x=350, y=250)

        #vegetarian label
        self.vegetarian_label = Label(self.app, text="Vegetarian", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.vegetarian_label.place(x=150, y=300)

        #vegetarian entry
        self.vegetarian_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.vegetarian_entry.place(x=350, y=300)

        #recipe video label
        self.recipe_video_label = Label(self.app, text="Recipe Video", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.recipe_video_label.place(x=150, y=350)

        #recipe video entry
        self.recipe_video_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.recipe_video_entry.place(x=350, y=350)

        #recipe image label
        self.recipe_image_label = Label(self.app, text="Recipe Image", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.recipe_image_label.place(x=650, y=200)

        #recipe image button
        self.recipe_image_button = Button(self.app, text="Upload", font=("Century Gothic", 15, "bold"), bg="#f8f9fb",command=self.upload_image)
        self.recipe_image_button.place(x=650, y=250)

        #select ingredients
        self.add_ingredients_button = Button(self.app, text="Select Ingredients", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.select_ingredients)
        self.add_ingredients_button.place(x=650, y=350)

        #add recipe button
        self.add_recipe_button = Button(self.app, text="Add Recipe", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.add_recipe)
        self.add_recipe_button.place(x=350, y=400)

        #back
        self.back_button = Button(self.app, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.admin_menu)
        self.back_button.place(x=550, y=400)

    #select ingredients function
    def select_ingredients(self):
        #toplevel window
        self.ingredient_window = Toplevel(self.app)
        self.ingredient_window.title("Select Ingredients")
        self.ingredient_window.geometry("600x600")

        #get all ingredients data from database
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM INGREDIENT")
        self.all_ingredients = cursor.fetchall()
        self.connector.commit()

        self.selected_ingredients = []

        for i, ingredient in enumerate(self.all_ingredients):
            #create a checkbutton for each ingredient
            ingredient = list(ingredient)
            ingredient_id = ingredient[0]
            ingredient_name = ingredient[1]

            x,y=0,0

            #button 'Select' 
            if i < 10:
                x = 100
                y = 100 + i * 50
            else:
                x = 300
                y = 100 + (i - 10) * 50

            self.select_ingredient_button = Button(self.ingredient_window, text=ingredient_name, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda ingredient_id=ingredient_id,ingredient_name=ingredient_name: self.select_ingredient_add(ingredient_id,ingredient_name))
            self.select_ingredient_button.place(x=x, y=y)

            #if selected add to selected ingredients

        #confirm button
        self.confirm_button = Button(self.ingredient_window, text="Confirm", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.ingredient_window.destroy)
        self.confirm_button.pack()
    
    #select ingredient function
    def select_ingredient_add(self, ingredient_id,ingredient_name):
        #messagebox selected ingredient name
        msg.showinfo("Selected Ingredient", ingredient_name)

        if ingredient_id not in self.selected_ingredients:
            self.selected_ingredients.append(ingredient_id)
        else:
            #ask want's to remove
            if msg.askyesno("Remove Ingredient", "Are you sure you want to remove this ingredient?"):
                self.selected_ingredients.remove(ingredient_id)

        print(self.selected_ingredients)
        




    #upload image function
    def upload_image(self):
        #open file dialog
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.image = Image.open(self.filename)

        print(self.filename)

        #message
        msg.showinfo("Success", "Image uploaded successfully")


    #add recipe function
    def add_recipe(self):
        #get title, cuisine, rating, vegetarian, recipe image and recipe video
        title = self.title_entry.get()
        cuisine = self.cuisine_entry.get()
        rating = self.rating_entry.get()
        vegetarian = self.vegetarian_entry.get()
        recipe_video = self.recipe_video_entry.get()

        #check if title, cuisine, rating, vegetarian, recipe image and recipe video are empty
        if title == "" or cuisine == "" or rating == "" or vegetarian == "" or recipe_video == "":
            msg.showerror("Error", "Please fill in all fields")
        else:
            #insert recipe into database
            if self.curremt_user == "admin":
                user_id = 1
            else:
                user_id = self.user_id
            self.connector = myconn.connect(**self.database)
            cursor = self.connector.cursor()
            cursor.execute("INSERT INTO RECIPE (userID,title, cuisine, rating, vegetarian, recipe_image, recipe_video) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id,title, cuisine, rating, vegetarian, self.filename, recipe_video))
            self.connector.commit()

            #get recent recipe id
            cursor.execute("SELECT * FROM RECIPE WHERE title=%s", (title,))
            recipe = cursor.fetchone()
            recipe_id = recipe[0]
            print(recipe_id,title)
            msg.showinfo("Success", "Recipe added successfully")

            #print selected ingredients
            print(self.selected_ingredients)
            #insert selected ingredients into database
            for ingredient in self.selected_ingredients:
                cursor.execute("INSERT INTO RECIPE_INGREDIENT (recipeID, ingredientID) VALUES (%s, %s)", (recipe_id, ingredient))
                self.connector.commit()

            self.admin_menu()

    






    #register function
    def register(self):
        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

        #load image
        self.openimage = Image.open('images/bg.jpg')
        self.openimage = self.openimage.resize((600, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #place register details
        self.title = Label(self.app, text="Register", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=250, y=150)

        #username label
        self.username_label = Label(self.app, text="Username", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.username_label.place(x=150, y=250)

        #username entry
        self.username_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.username_entry.place(x=250, y=250)

        #email label
        self.email_label = Label(self.app, text="Email", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.email_label.place(x=150, y=300)

        #email entry
        self.email_entry = Entry(self.app, font=("Century Gothic", 15, "bold"))
        self.email_entry.place(x=250, y=300)

        #password label
        self.password_label = Label(self.app, text="Password", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.password_label.place(x=150, y=350)

        #password entry
        self.password_entry = Entry(self.app, font=("Century Gothic", 15, "bold"), show="*")
        self.password_entry.place(x=250, y=350)

        #register button
        self.register_button = Button(self.app, text="Register", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.register_user)
        self.register_button.place(x=250, y=400)

        #login button
        self.login_button = Button(self.app, text="Login", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.login)
        self.login_button.place(x=350, y=400)

    #register user function
    def register_user(self):
        #get username, email and password
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        #check if username, email and password are empty
        if username == "" or email == "" or password == "":
            msg.showerror("Error", "Please fill in all fields")
        #validate email
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg.showerror("Error", "Invalid email")
        #validate password
        elif len(password) < 6:
            msg.showerror("Error", "Password must be atleast 6 characters")
            self.password_entry.delete(0, END)
        #validate password with atleast one uppercase, one lowercase, one digit and one special character
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$", password):
            msg.showerror("Error", "Password must contain atleast one uppercase, one lowercase, one digit and one special character")
            self.password_entry.delete(0, END)
        else:
            #check if user exists
            self.connector=myconn.connect(**self.database)
            #check if the self.connection is successful


            with self.connector.cursor() as cursor:
                cursor.execute("SELECT * FROM USER WHERE username=%s", (username,))
                user = cursor.fetchone()

                #if user exists
                if user:
                    msg.showerror("Error", "Username already exists")
                else:
                    cursor.execute("INSERT INTO USER (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                    self.connector.commit()
                    msg.showinfo("Success", "User registered successfully")
                    self.login()


    #main menu function
    def main_menu(self):
        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

       #dimensions 1000x600
        self.app.geometry("1000x600")

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #logout button
        self.logout_button = Button(self.app, text="Logout", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.login)
        self.logout_button.place(x=100, y=50)


        #search bar frame
        self.search_frame = Frame(self.app, bg="#eff2f7")
        self.search_frame.place(x=250, y=50)

        #search bar entry
        self.search_entry = Entry(self.search_frame, font=("Century Gothic", 15, "bold"))
        self.search_entry.grid(row=0, column=1)

        #search bar button
        self.search_button = Button(self.search_frame, text="Search", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.search)
        self.search_button.grid(row=0, column=2)

        #search by ingredients button
        self.ingredients_button = Button(self.search_frame, text="Search by Ingredients", font=("Century Gothic", 15, "bold"), bg="#f8f9fb",command=self.search_by_ingredients)
        self.ingredients_button.grid(row=0, column=3)

        #clear filter button
        self.clear_filter_button = Button(self.search_frame, text="Clear Filter", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.main_menu)
        self.clear_filter_button.grid(row=0, column=4)

        #logout
        self.logout_button = Button(self.app, text="Logout", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.login_user)
        self.logout_button.place(x=350, y=400)

        #left vertical frame for notebook
        self.left_frame = Frame(self.app, bg="#f8f9fb")
        self.left_frame.place(x=100, y=100, width=150, height=430)

        #scrollbar to left frame
        self.scrollbar = Scrollbar(self.left_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        #Indian button text color 04af8f
        self.indian_button = Button(self.left_frame, text="Indian", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.indian)
        self.indian_button.pack(pady=10)

        #Italian button text color 04af8f
        self.italian_button = Button(self.left_frame, text="Italian", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.italian)
        self.italian_button.pack(pady=10)

        #Chinese button text color 04af8f
        self.chinese_button = Button(self.left_frame, text="Chinese", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.chinese)
        self.chinese_button.pack(pady=10)

        #American button text color 04af8f
        self.american_button = Button(self.left_frame, text="American", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.american)
        self.american_button.pack(pady=10)

        #continental button text color
        self.continental_button = Button(self.left_frame, text="Continental", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.continental)
        self.continental_button.pack(pady=10)

        #Vegan button text color
        self.vegan_button = Button(self.left_frame, text="Vegan", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.vegan)
        self.vegan_button.pack(pady=10)

        #Non-Veg button text color
        self.non_veg_button = Button(self.left_frame, text="Non-Veg", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.non_veg)
        self.non_veg_button.pack(pady=10)

        #New Arrival button text color
        self.new_arrival_button = Button(self.left_frame, text="New Arrival", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.new_arrival)
        self.new_arrival_button.pack(pady=10)


        #right canvas for displaying recipes
        self.right_canvas = Canvas(self.app, bg="#f8f9fb")
        self.right_canvas.place(x=260, y=100, width=600, height=430)




        #if recipes found
        if self.all_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.all_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")

        #support screen button
        self.support_button = Button(self.app, text="Support", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.support)
        self.support_button.place(x=350, y=550)

    #support function
    def support(self):
        #destroy right canvas
        for i in self.app.winfo_children():
            i.destroy()

        #dimensions 1000x600
        self.app.geometry("1000x600")

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #welcome to support screen
        self.welcome_label = Label(self.app, text="Welcome to Support", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.welcome_label.place(x=100, y=100)

        #Email label
        self.email_label = Label(self.app, text="Email : ", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.email_label.place(x=100, y=200)

        #email details label
        #support@recipefinder.com
        self.email_details_label = Label(self.app, text="support@recipefinder.com", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.email_details_label.place(x=300, y=200)

        #phone label
        self.phone_label = Label(self.app, text="Phone: ", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.phone_label.place(x=100, y=250)

        #phone number label
        self.phone_number_label = Label(self.app, text="+91 9876543210", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.phone_number_label.place(x=300, y=250)

        #website label
        self.website_label = Label(self.app, text="Website: ", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.website_label.place(x=100, y=300)

        #website link label
        self.website_link_label = Label(self.app, text="www.recipefinder.com", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.website_link_label.place(x=300, y=300)

        #Thanks for using recipefinder
        self.thanks_label = Label(self.app, text="Thanks for using recipefinder", font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
        self.thanks_label.place(x=300, y=400)

        #back
        self.back_button = Button(self.app, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.main_menu)
        self.back_button.place(x=300, y=450)







    #indian function
    def indian(self):
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all indian recipes
        self.indian_recipes = [recipe for recipe in self.my_selected_receipes if recipe[3].lower()=="indian"]
        print(self.indian_recipes)

        #if recipes found
        if self.indian_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.indian_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/4)
                col=i%4

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")

    #italian function
    def italian(self):
        
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all italian recipes
        self.italian_recipes = [recipe for recipe in self.my_selected_receipes if recipe[3].lower()=="italian"]

        #if recipes found
        if self.italian_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.italian_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")

        


    #chinese function
    def chinese(self):
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all chinese recipes
        self.chinese_recipes = [recipe for recipe in self.my_selected_receipes if recipe[3].lower()=="chinese"]

        #if recipes found
        if self.chinese_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.chinese_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")


    #american function
    def american(self):
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all american recipes
        self.american_recipes = [recipe for recipe in self.my_selected_receipes if recipe[3].lower()=="american"]

        #if recipes found
        if self.american_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.american_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")

    #continental function
            
    def continental(self):
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all continental recipes
        self.continental_recipes = [recipe for recipe in self.my_selected_receipes if recipe[3].lower()=="continental"]

        #if recipes found
        if self.continental_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.continental_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")


    #vegan function
    def vegan(self):
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all vegan recipes
        self.vegan_recipes = [recipe for recipe in self.my_selected_receipes if recipe[4]==0]

        #if recipes found
        if self.vegan_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.vegan_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")

        
    #non-veg function
    def non_veg(self):
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all non-veg recipes
        self.non_veg_recipes = [recipe for recipe in self.my_selected_receipes if recipe[4]==1]

        #if recipes found
        if self.non_veg_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.non_veg_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")



    #new arrival function
    def new_arrival(self):
        #destroy right canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        #from my selected list get all new arrival recipes
        self.new_arrival_recipes = [recipe for recipe in self.my_selected_receipes if recipe[5]==0]

        #if recipes found
        if self.new_arrival_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.new_arrival_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")

    #search_by_ingredients
    def search_by_ingredients(self):
        #destroy previous window
        for i in self.app.winfo_children():
            i.destroy()

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)
        self.label.pack()

        #search by ingredients label
        self.title = Label(self.app, text="Search by Ingredients", font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=300, y=40)

        #clear filter button top right
        self.clear_filter_button = Button(self.app, text="Clear Filter", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.search_by_ingredients)
        self.clear_filter_button.place(x=750, y=50)

        #left vertical frame for notebook
        self.left_frame = Frame(self.app, bg="#f8f9fb")
        self.left_frame.place(x=100, y=100, width=150, height=430)

        #scrollbar to left frame
        self.scrollbar = Scrollbar(self.left_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        #Indian button text color 04af8f
        self.indian_button = Button(self.left_frame, text="Indian", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.indian)
        self.indian_button.pack(pady=10)

        #Italian button text color 04af8f
        self.italian_button = Button(self.left_frame, text="Italian", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.italian)
        self.italian_button.pack(pady=10)

        #Chinese button text color 04af8f
        self.chinese_button = Button(self.left_frame, text="Chinese", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.chinese)
        self.chinese_button.pack(pady=10)

        #American button text color 04af8f
        self.american_button = Button(self.left_frame, text="American", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.american)
        self.american_button.pack(pady=10)

        #continental button text color
        self.continental_button = Button(self.left_frame, text="Continental", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.continental)
        self.continental_button.pack(pady=10)

        #Vegan button text color
        self.vegan_button = Button(self.left_frame, text="Vegan", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.vegan)
        self.vegan_button.pack(pady=10)

        #Non-Veg button text color
        self.non_veg_button = Button(self.left_frame, text="Non-Veg", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.non_veg)
        self.non_veg_button.pack(pady=10)

        #New Arrival button text color
        self.new_arrival_button = Button(self.left_frame, text="New Arrival", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", fg="#04af8f", command=self.new_arrival)
        self.new_arrival_button.pack(pady=10)


                #right canvas for displaying recipes
        self.right_canvas = Canvas(self.app, bg="#f8f9fb")
        self.right_canvas.place(x=260, y=100, width=600, height=430)

        #if recipes found
        if self.all_recipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.all_recipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")


        #add ingredients button bottom left
        self.add_ingredients_button = Button(self.app, text="Add Ingredients", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.add_ingredients)
        self.add_ingredients_button.place(x=270, y=550)


        #remove ingredients button bottom right
        self.remove_ingredients_button = Button(self.app, text="Remove Ingredients", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.remove_ingredients)
        self.remove_ingredients_button.place(x=500, y=550)

        #back button top of left frame
        self.back_button = Button(self.app, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.main_menu)
        self.back_button.place(x=140, y=50)


    #add ingredients function
    def add_ingredients(self):
        #clear self.right_canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        # display all ingredients in four columns and 7 rows
        for i, ingredient in enumerate(self.all_ingrediants):
            ingredient=list(ingredient)
            ingredient_id=ingredient[0]
            ingredient_name=ingredient[1]

            row=int(i/4)
            col=i%4
            
            #display if the ingredient is not in my ingredients
            if ingredient not in self.my_ingrediants:
                #ingredient button
                ingredient_button = Button(self.right_canvas, text=ingredient_name, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda ingredient=ingredient: self.add_ingredient(ingredient))
                ingredient_button.grid(row=row, column=col, padx=10, pady=10)
        

    #add ingredient function
    def add_ingredient(self, ingredient):
        #add it to my ingredients
        self.my_ingrediants.append(ingredient)
        print(self.my_ingrediants)

        #display recipes that has my ingredients
                #right canvas for displaying recipes
        self.right_canvas = Canvas(self.app, bg="#f8f9fb")
        self.right_canvas.place(x=260, y=100, width=600, height=430)




        #get recipe ids from recipe_ingredient table that has my ingredients
        recipe_ids = self.get_recipe_ids(self.my_ingrediants)
        print(recipe_ids,'current recipe ids')

        print(len(self.my_selected_receipes))

        self.my_selected_receipes = [recipe for recipe in self.all_recipes if recipe[0] in recipe_ids]

        self.my_selected_receipes=list(set(self.my_selected_receipes))

        print(self.my_selected_receipes)

        #if recipes found
        if self.my_selected_receipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.my_selected_receipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/4)
                col=i%4

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            msg.showerror("Error", "No recipes found")

    #get recipe ids function
    def get_recipe_ids(self, my_ingrediants):
        my_ingrediants_data = [i[0] for i in my_ingrediants]
        recipe_ingredient_dict = {}
        recipe_ids = []
        #get recipeids and ingredientids from recipe_ingredient table as key value pairs
        self.connector = myconn.connect(**self.database)
        self.db = self.connector.cursor()
        self.db.execute("SELECT recipeID, ingredientID FROM recipe_ingredient")
        recipe_ingredient = self.db.fetchall()
        for row in recipe_ingredient:
            if row[0] in recipe_ingredient_dict:
                recipe_ingredient_dict[row[0]].append(row[1])
            else:
                recipe_ingredient_dict[row[0]] = [row[1]]

        #now find the subset of recipe_ingredient_dict that has all my ingredients
        for recipe_id in recipe_ingredient_dict:
            print(recipe_id)
            if set(my_ingrediants_data).issubset(set(recipe_ingredient_dict[recipe_id])):
                recipe_ids.append(recipe_id)
    
        return recipe_ids

    #view_recipe
    def view_recipe(self, recipe):
        #clear window
        for i in self.app.winfo_children():
            i.destroy()

        #load image
        self.openimage = Image.open('images/menu_bg.jpg')
        self.openimage = self.openimage.resize((1000, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.openimage)
        self.label = Label(self.app, image=self.image)  

        self.label.pack()

        #recipe title
        self.title = Label(self.app, text=recipe[2], font=("Century Gothic", 30, "bold"), bg="#f8f9fb")
        self.title.place(x=400, y=50)

        #left frame for image
        self.left_frame = Frame(self.app, bg="#f8f9fb")
        self.left_frame.place(x=100, y=100, width=300, height=300)

        #open recipe image
        recipe_image = Image.open(recipe[4])
        recipe_image = recipe_image.resize((300, 300), Image.LANCZOS)
        recipe_image = ImageTk.PhotoImage(recipe_image)
        self.recipe_image = Label(self.left_frame, image=recipe_image)
        self.recipe_image.image = recipe_image
        self.recipe_image.pack()

        #right frame for Recipe details
        self.right_frame = Frame(self.app, bg="#f8f9fb")
        self.right_frame.place(x=500, y=100, width=300, height=300)

        #cusine label
        self.cuisine_label = Label(self.right_frame, text=f"Cuisine: {recipe[3]}", font=("Century Gothic", 20, "bold"), bg="#f8f9fb")
        self.cuisine_label.pack(pady=10)

        #rating label
        self.rating_label = Label(self.right_frame, text=f"Rating: {recipe[5]}", font=("Century Gothic", 20, "bold"), bg="#f8f9fb")
        self.rating_label.pack(pady=10)

        #prep video link
        self.video_link = Button(self.right_frame, text="Preparation Video", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.prep_video(recipe))
        self.video_link.pack(pady=10)
        

        #see all ingredients button
        self.set_ingredients_button = Button(self.right_frame, text="See Ingredients", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.see_ingredients(recipe))
        self.set_ingredients_button.pack(pady=10)

        #back button
        self.back_button = Button(self.right_frame, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=self.main_menu)
        self.back_button.pack(pady=10)


    #def prep_video
    def prep_video(self, recipe_id):
        #play video link
        recipe_video=recipe_id[7]
        print(recipe_video)

        #check if video link is empty
        if recipe_video == "":
            msg.showerror("Error", "No video found")
        else:
            #open video link
            os.system(f"start {recipe_video}")



    #see ingredients function
    def see_ingredients(self,recipe):
        #dsiplay ingredients in right frame
        #right canvas for displaying recipes
        self.right_canvas = Canvas(self.app, bg="#f8f9fb")
        self.right_canvas.place(x=460, y=100, width=400, height=430)

        #get ingredients from recipe_ingredient table
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        cursor.execute("SELECT ingredientID FROM RECIPE_INGREDIENT WHERE recipeID=%s", (recipe[0],))
        ingredient_ids = cursor.fetchall()
        print(ingredient_ids)

        #get ingredients from ingredient table
        ingredients = []
        for ingredient_id in ingredient_ids:
            cursor.execute("SELECT * FROM INGREDIENT WHERE ingredientID=%s", (ingredient_id))
            ingredients.extend(cursor.fetchall())

        print(ingredients)

        #display ingredients in right frame
        for i, ingredient in enumerate(ingredients):
            ingredient=list(ingredient)
            ingredient_id=ingredient[0]
            ingredient_name=ingredient[1]

            row=int(i/4)
            col=i%4

            #ingredient button
            ingredient_button = Button(self.right_canvas, text=ingredient_name, font=("Century Gothic", 15, "bold"), bg="#f8f9fb")
            ingredient_button.grid(row=row, column=col, padx=10, pady=10)

        #back button
        self.back_button = Button(self.right_canvas, text="Back", font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe))
        self.back_button.place(x=300, y=300)






    #remove ingredients function
    def remove_ingredients(self):
        #clear self.right_canvas
        for i in self.right_canvas.winfo_children():
            i.destroy()

        # display my ingredients in four columns and 7 rows
        for i, ingredient in enumerate(self.my_ingrediants):
            ingredient=list(ingredient)
            ingredient_id=ingredient[0]
            ingredient_name=ingredient[1]

            row=int(i/4)
            col=i%4

            #ingredient button
            ingredient_button = Button(self.right_canvas, text=ingredient_name, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda ingredient=ingredient: self.remove_ingredient(ingredient))
            ingredient_button.grid(row=row, column=col, padx=10, pady=10)


    #remove ingredient function
    def remove_ingredient(self, ingredient):
        #remove it from my ingredients
        self.my_ingrediants.remove(ingredient)
        print(self.my_ingrediants)

        #display recipes that has my ingredients
                #right canvas for displaying recipes
        self.right_canvas = Canvas(self.app, bg="#f8f9fb")
        self.right_canvas.place(x=260, y=100, width=600, height=430)




        #get recipe ids from recipe_ingredient table that has my ingredients
        recipe_ids = []
        #connect to database
        self.connector = myconn.connect(**self.database)
        cursor = self.connector.cursor()
        for ingredient in self.my_ingrediants:
            cursor.execute("SELECT recipeID FROM RECIPE_INGREDIENT WHERE ingredientID=%s", (ingredient[0],))
            recipe_ids.extend(cursor.fetchall())


        recipe_ids = [recipe_id[0] for recipe_id in recipe_ids]
        print(recipe_ids)
        #get recipes from recipe table that has my ingredients 
        self.my_selected_receipes = [] 
        for recipe_id in recipe_ids:
            cursor.execute("SELECT * FROM RECIPE WHERE recipeID=%s", (recipe_id,))
            self.my_selected_receipes.extend(cursor.fetchall())
        print(self.my_selected_receipes)

        #if recipes found
        if self.my_selected_receipes:
            pass
            # #load recipes into convas and place 3 in row
            for i, recipe in enumerate(self.my_selected_receipes):
                recipe=list(recipe)
                recipe_id=recipe[0]
                recipe_title=recipe[2]
                recipe_cuisine=recipe[3]
                recipe_image=recipe[4]

            #     #open recipe image
                recipeImage=Image.open(recipe_image)
                recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                rimage=ImageTk.PhotoImage(recipeImage)
                row=int(i/3)
                col=i%3

                #recipe button
                recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                recipe_button.image=rimage
                recipe_button.grid(row=row, column=col, padx=10, pady=10)
        else:
            #open search by ingredients
            self.search_by_ingredients()




    #search from recipe table
    def search(self):
        #get search query
        search = self.search_entry.get()

        #check if search query is empty
        if search == "":
            msg.showerror("Error", "Please enter a search query")
        else:
            #search in recipe table
            recipes=[]
            self.connector = myconn.connect(**self.database)
            with self.connector.cursor() as cursor:
                cursor.execute("SELECT * FROM RECIPE WHERE title LIKE %s", (f"%{search}%",))
                recipes = cursor.fetchall()

            #display recipes in right frame
            #right canvas for displaying recipes
            self.right_canvas = Canvas(self.app, bg="#f8f9fb")
            self.right_canvas.place(x=260, y=100, width=600, height=430)

            print(recipes)

            #if recipes found
            if recipes:
                pass
                # #load recipes into convas and place 3 in row
                for i, recipe in enumerate(recipes):
                    recipe=list(recipe)
                    recipe_id=recipe[0]
                    recipe_title=recipe[2]
                    recipe_cuisine=recipe[3]
                    recipe_image=recipe[4]

                #     #open recipe image
                    recipeImage=Image.open(recipe_image)
                    recipeImage=recipeImage.resize((120, 120), Image.LANCZOS)
                    rimage=ImageTk.PhotoImage(recipeImage)
                    row=int(i/3)
                    col=i%3

                    #recipe button
                    recipe_button = Button(self.right_canvas, text=recipe_title, font=("Century Gothic", 15, "bold"), bg="#f8f9fb", command=lambda recipe=recipe: self.view_recipe(recipe),image=rimage, compound=TOP)
                    recipe_button.image=rimage
                    recipe_button.grid(row=row, column=col, padx=10, pady=10)
            else:
                msg.showerror("Error", "No recipes found")

    #search results function






#starter code
if __name__ == "__main__":


    #create window
    app = Tk()
    cc = rf(app)
    #run app
    app.mainloop()
    