import mysql.connector
import tkinter as tk
from tkinter import ttk, Spinbox, IntVar
from PIL import Image, ImageTk

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="projectfinal"
    )
    return conn

# Function to display stellar systems with >3 planets
def show_systems():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM starSystem WHERE NoofPlanets > 3")
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "✨ Stellar Systems with more than 3 Planets:\n", "title")

    for row in results:
        output_text.insert(tk.END, f"🌌 ID: {row[0]}\n", "header")
        output_text.insert(tk.END, f"  Name: {row[1]}\n")
        output_text.insert(tk.END, f"  No. of Stars: {row[2]}, No. of Planets: {row[3]}\n")
        output_text.insert(tk.END, f"  Distance: {row[4]:.2f} parsecs\n")
        output_text.insert(tk.END, "  ----------\n", "separator")
    
    output_text.config(state=tk.DISABLED)

# Function to display discoveries after 2000
def show_discoveries():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Discovery WHERE discoveryYear > 2000 ORDER BY discoveryYear")
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "🔭 Discoveries after 2000 (sorted by year):\n", "title")

    for row in results:
        output_text.insert(tk.END, f"🔬 Discovery ID: {row[0]}\n", "header")
        output_text.insert(tk.END, f"  Method: {row[1]}\n")
        output_text.insert(tk.END, f"  Year: {row[2]}\n")
        output_text.insert(tk.END, "  ----------\n", "separator")

    output_text.config(state=tk.DISABLED)

# Function to display total number of planets and stars in the system
def show_total_planets_stars():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(NoofStars), SUM(NoofPlanets) FROM starSystem")
    result = cursor.fetchone()
    conn.close()

    total_stars = result[0]
    total_planets = result[1]

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"🌟 Total Stars: {total_stars}\n", "header")
    output_text.insert(tk.END, f"🌍 Total Planets: {total_planets}\n", "header")
    output_text.config(state=tk.DISABLED)

# to display planets with low eccentricity
def show_low_eccentricity_planets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM planets WHERE eccentricity < 0.2")
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "🌌 Planets with Low Eccentricity (<0.2):\n", "title")

    for row in results:
        output_text.insert(tk.END, f"🌍 Planet ID: {row[0]}\n", "header")
        output_text.insert(tk.END, f"  Name: {row[1]}\n")
        output_text.insert(tk.END, f"  Eccentricity: {row[5]}\n")
        output_text.insert(tk.END, "  ----------\n", "separator")

    output_text.config(state=tk.DISABLED)

# Function to display stellar metallicity levels for stars above a certain threshold
def show_metallicity_levels(min_metallicity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT stellarMetallicity, stellarRatio, StellarName 
        FROM Metallicity 
        JOIN starCharacteristics ON Metallicity.StarID = starCharacteristics.StarID 
        JOIN starSystem ON starCharacteristics.SID = starSystem.SID 
        WHERE stellarMetallicity > %s
    """, (min_metallicity,))
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Stars with Metallicity > {min_metallicity}:\n", "title")

    for row in results:
        output_text.insert(tk.END, f"Star Name: {row[2]}, Metallicity: {row[0]}, Ratio: {row[1]}\n")
        output_text.insert(tk.END, "----------\n", "separator")

    output_text.config(state=tk.DISABLED)

# Function to display planets within a selected orbital period range
def show_planets_by_orbital_period(min_period, max_period):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT planetname, orbitalperiod, SID 
        FROM planets 
        WHERE orbitalperiod BETWEEN %s AND %s
    """, (min_period, max_period))
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Planets with Orbital Period Between {min_period} and {max_period} days:\n", "title")

    for row in results:
        output_text.insert(tk.END, f"Planet Name: {row[0]}, Period: {row[1]} days, System ID: {row[2]}\n")
        output_text.insert(tk.END, "----------\n", "separator")

    output_text.config(state=tk.DISABLED)

# Function to display planets by discovery method
def show_planets_by_discovery_method(method="Transit"):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT planetname, discoveryYear, discoveryMethod 
        FROM planets 
        JOIN Discovery ON planets.SID = Discovery.SID 
        WHERE discoveryMethod = %s
    """, (method,))
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Planets Discovered by {method} Method:\n", "title")

    for row in results:
        output_text.insert(tk.END, f"Planet Name: {row[0]}, Year: {row[1]}, Method: {row[2]}\n")
        output_text.insert(tk.END, "----------\n", "separator")

    output_text.config(state=tk.DISABLED)

# Function to display systems with high eccentricity and long orbital period
def show_high_eccentricity_long_orbit():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT starSystem.StellarName, orbitalPropt.orbitalPeriod, orbitalPropt.eccentricity 
        FROM starSystem 
        JOIN orbitalPropt ON starSystem.SID = orbitalPropt.SID 
        WHERE orbitalPropt.eccentricity > 0.5 AND orbitalPropt.orbitalPeriod > 300
    """)
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Systems with High Eccentricity and Long Orbital Period:\n", "title")

    for row in results:
        output_text.insert(tk.END, f"System Name: {row[0]}, Orbital Period: {row[1]} days, Eccentricity: {row[2]}\n")
        output_text.insert(tk.END, "----------\n", "separator")

    output_text.config(state=tk.DISABLED)

# New function to filter stars by temperature range
def show_stars_by_temperature_range():
    min_temp = int(temperature_min_spinbox.get())  # Get min temperature from the spinbox
    max_temp = int(temperature_max_spinbox.get())  # Get max temperature from the spinbox

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT starSystem.StellarName, starCharacteristics.stellarTemp
        FROM starCharacteristics
        JOIN starSystem ON starCharacteristics.SID = starSystem.SID
        WHERE starCharacteristics.stellarTemp BETWEEN %s AND %s
    """, (min_temp, max_temp))
    results = cursor.fetchall()
    conn.close()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Stars with Temperature Between {min_temp} and {max_temp} K:\n", "title")

    for row in results:
        output_text.insert(tk.END, f"Star Name: {row[0]}, Temperature: {row[1]} K\n")
        output_text.insert(tk.END, "----------\n", "separator")

    output_text.config(state=tk.DISABLED)

# Function to insert a new star system
def add_star_system():
    sid = int(entry_sid.get())
    name = entry_name.get()
    stars = int(entry_stars.get())
    planets = int(entry_planets.get())
    distance = float(entry_distance.get())
    ra = entry_ra.get()
    declination = entry_declination.get()

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO starSystem (SID, StellarName, NoofStars, NoofPlanets, Distance, RA, Declination) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (sid, name, stars, planets, distance, ra, declination))
        conn.commit()
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"✅ Star system '{name}' added successfully.\n")
        output_text.config(state=tk.DISABLED)
    except mysql.connector.Error as err:
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"❌ Error: {err}\n")
        output_text.config(state=tk.DISABLED)
    finally:
        conn.close()

# Function to delete a star system by SID
def delete_star_system():
    sid = int(entry_sid.get())
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM starSystem WHERE SID = %s", (sid,))
        conn.commit()
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"🗑️ Star system with SID {sid} deleted successfully.\n")
        output_text.config(state=tk.DISABLED)
    except mysql.connector.Error as err:
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"❌ Error: {err}\n")
        output_text.config(state=tk.DISABLED)
    finally:
        conn.close()

# Function to resize background dynamically
def resize_bg(event):
    new_width = event.width
    new_height = event.height
    resized_image = original_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_photo = bg_photo

# Main window setup
root = tk.Tk()
root.title("Star System Database")
root.geometry("1000x750")
root.minsize(800, 600)

# Load and set up the background image
original_bg_image = Image.open("test1.jpg")  # Your background image path here
bg_photo = ImageTk.PhotoImage(original_bg_image)

# Canvas for the background image
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Bind resize event for background image
root.bind("<Configure>", resize_bg)

# Center frame for all widgets
center_frame = tk.Frame(root, bg="#101521", width=700, height=500)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title label
title_label = tk.Label(center_frame, text="Star System Database", font=("Consolas", 20, "bold"), fg="white", bg="#101521")
title_label.pack(pady=(20, 30))

# Notebook widget for tabs
notebook = ttk.Notebook(center_frame)
notebook.pack(pady=10)

# Tab 1: Action buttons
button_tab = tk.Frame(notebook, bg="#101521")
notebook.add(button_tab, text="Actions")

button_show_systems = ttk.Button(button_tab, text="Show Systems with > 3 Planets", command=show_systems)
button_show_systems.grid(row=0, column=0, padx=15, pady=10)

button_show_discoveries = ttk.Button(button_tab, text="Show Discoveries After 2000", command=show_discoveries)
button_show_discoveries.grid(row=0, column=1, padx=15, pady=10)

button_total_planets_stars = ttk.Button(button_tab, text="Total Planets and Stars", command=show_total_planets_stars)
button_total_planets_stars.grid(row=1, column=0, padx=15, pady=10)

button_high_eccentricity = ttk.Button(button_tab, text="Low Eccentricity Planets", command=show_low_eccentricity_planets)
button_high_eccentricity.grid(row=1, column=1, padx=15, pady=10)

# New button for the 'Show Planets by Discovery Method' function
button_discovery_method = ttk.Button(button_tab, text="Show Planets by Discovery Method", command=show_planets_by_discovery_method)
button_discovery_method.grid(row=2, column=0, padx=15, pady=10, sticky="ew")

# New button for 'Systems with High Eccentricity and Long Orbital Period' function
button_high_eccentricity_long_orbit = ttk.Button(button_tab, text="High Eccentricity & Long Orbit", command=show_high_eccentricity_long_orbit)
button_high_eccentricity_long_orbit.grid(row=2, column=1, padx=15, pady=10, sticky="e")  # Align to the right


# Tab 2: Spinbox for metallicity filter
metallicity_tab = tk.Frame(notebook, bg="#101521")
notebook.add(metallicity_tab, text="Metallicity Filter")

metallicity_spinbox = Spinbox(metallicity_tab, from_=0.1, to=5.0, increment=0.1, width=5)
metallicity_spinbox.pack(pady=10)

button_metallicity = ttk.Button(metallicity_tab, text="Search by Metallicity", command=lambda: show_metallicity_levels(float(metallicity_spinbox.get())))
button_metallicity.pack(pady=10)

# Alternative: Using IntVar to set default values
min_temp_var = IntVar(value=3000)  # Set default value
max_temp_var = IntVar(value=10000)  # Set default value

temperature_min_spinbox = Spinbox(metallicity_tab, from_=1000, to=50000, increment=100, width=5, textvariable=min_temp_var)
temperature_min_spinbox.pack(pady=10)

temperature_max_spinbox = Spinbox(metallicity_tab, from_=1000, to=50000, increment=100, width=5, textvariable=max_temp_var)
temperature_max_spinbox.pack(pady=10)

# Button to trigger the star temperature filter
button_temperature_range = ttk.Button(metallicity_tab, text="Search by Temperature Range", command=show_stars_by_temperature_range)
button_temperature_range.pack(pady=10)

# Tab 3: Sliders for orbital period range filter
orbital_period_tab = tk.Frame(notebook, bg="#101521")
notebook.add(orbital_period_tab, text="Orbital Period Filter")

orbital_min_scale = tk.Scale(orbital_period_tab, from_=1, to=500, orient="horizontal", label="Min Orbital Period (days)", length=200)
orbital_min_scale.pack(pady=10)

orbital_max_scale = tk.Scale(orbital_period_tab, from_=1, to=500, orient="horizontal", label="Max Orbital Period (days)", length=200)
orbital_max_scale.pack(pady=10)

button_orbital_period = ttk.Button(orbital_period_tab, text="Search by Orbital Period", command=lambda: show_planets_by_orbital_period(orbital_min_scale.get(), orbital_max_scale.get()))
button_orbital_period.pack(pady=10)

# Tab 4: Add and Delete Data
manage_data_tab = tk.Frame(notebook, bg="#101521")
notebook.add(manage_data_tab, text="Manage Data")

# Labels and Entry fields for star system attributes
tk.Label(manage_data_tab, text="SID:", bg="#101521", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_sid = tk.Entry(manage_data_tab, width=25)
entry_sid.grid(row=0, column=1, padx=5, pady=5)

tk.Label(manage_data_tab, text="Stellar Name:", bg="#101521", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(manage_data_tab, width=25)
entry_name.grid(row=1, column=1, padx=5, pady=5)

tk.Label(manage_data_tab, text="No. of Stars:", bg="#101521", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_stars = tk.Entry(manage_data_tab, width=25)
entry_stars.grid(row=2, column=1, padx=5, pady=5)

tk.Label(manage_data_tab, text="No. of Planets:", bg="#101521", fg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_planets = tk.Entry(manage_data_tab, width=25)
entry_planets.grid(row=3, column=1, padx=5, pady=5)

tk.Label(manage_data_tab, text="Distance (parsecs):", bg="#101521", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_distance = tk.Entry(manage_data_tab, width=25)
entry_distance.grid(row=4, column=1, padx=5, pady=5)

tk.Label(manage_data_tab, text="RA:", bg="#101521", fg="white").grid(row=5, column=0, padx=5, pady=5, sticky="w")
entry_ra = tk.Entry(manage_data_tab, width=25)
entry_ra.grid(row=5, column=1, padx=5, pady=5)

tk.Label(manage_data_tab, text="Declination:", bg="#101521", fg="white").grid(row=6, column=0, padx=5, pady=5, sticky="w")
entry_declination = tk.Entry(manage_data_tab, width=25)
entry_declination.grid(row=6, column=1, padx=5, pady=5)

# Buttons for Add and Delete operations
button_add = ttk.Button(manage_data_tab, text="Add Star System", command=add_star_system)
button_add.grid(row=7, column=0, padx=5, pady=10)

button_delete = ttk.Button(manage_data_tab, text="Delete Star System", command=delete_star_system)
button_delete.grid(row=7, column=1, padx=5, pady=10)

# Output text box with dark background and light text
output_frame = tk.Frame(center_frame, bg="#2E3B55")
output_frame.pack(pady=(20, 30))

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(output_frame, height=20, width=70, font=("Consolas", 11), wrap="word", yscrollcommand=scrollbar.set, bg="#1E1E1E", fg="#D4D4D4", bd=0, relief="flat")
output_text.pack(padx=15, pady=15)
scrollbar.config(command=output_text.yview)


output_text.tag_configure("header", font=("Consolas", 11, "bold"), foreground="#FFD700")
output_text.tag_configure("separator", font=("Consolas", 8), foreground="#444444")
output_text.tag_configure("title", font=("Consolas", 13, "bold"), foreground="#FFFF00")

root.mainloop()
