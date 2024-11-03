import tkinter as tk
from PIL import Image, ImageTk
from functools import partial

# Initialize global variables
crops = 0
money = 0
cps = 0
cpc = 0
current = " "
land_multiplier = 1  # New: Multiplier based on the amount of land owned


TK_SILENCE_DEPRECATION = 1

# Define upgrades with their properties
upgrades = {
    "Wood Hoe": {
        "base_cost": 10,
        "description": "The basic start to any harvest game.\n(Wood Hoe increases Food Gain by 25%).",
        "multiplier": 1.25,
        "quantity": 0,
        "current_cost": 10
    },
    "Steel Hoe": {
        "base_cost": 25,
        "description": "The Steel Hoe is stronger and can easily tend crops compared to the Wood Hoe.\n(Steel Hoe increases Food Gain by 50%).",
        "multiplier": 1.5,
        "quantity": 0,
        "current_cost": 25
    },
    "Gold Hoe": {
        "base_cost": 50,
        "description": "Stay Golden Ponyboy! Golden Hoe is able to reap better/higher quality crops.\n(Gold Hoe increases Food Gain by 75%).",
        "multiplier": 1.75,
        "quantity": 0,
        "current_cost": 50
    },
    "Cow": {
        "base_cost": 100,
        "description": "Cows can help carry crops to the store, along with fertilizing the field.\n(Cows increase Food Gain by 5x)",
        "multiplier": 1.0,
        "quantity": 0,
        "current_cost": 100
    },
    "Mule": {
        "base_cost": 250,
        "description": "Mules help carry the crops from the field to the store, arguably quicker than Cows!\n(Mules increase food gain by 15x)",
        "multiplier": 1.0,
        "quantity": 0,
        "current_cost": 250
    },
    "Bull": {
        "base_cost": 400,
        "description": "Strong like a Bull! Bulls have the strength to carry the crop load quicker than the other farm animals.\n(Bulls increase food gain by 25x)",
        "multiplier": 1.0,
        "quantity": 0,
        "current_cost": 400
    },
    "'Souvenir Plot'": {
        "base_cost": 200,
        "description": "Commonly sold as a gift...Begin your farming career with the addition of a small plot of land.\n(Land increases food gain by 200%) ",
        "multiplier": 1.0,
        "quantity": 1,
        "current_cost": 200,
    },
    "Acre of Land": {
        "base_cost": 1,
        "description": "Larger than just a plot. Smaller than one Hectare. (Land increases food gain by 300%)",
        "multiplier": 1.0,
        "quantity": 1,
        "current_cost": 500,
    }
}

# Function to calculate money per click, taking into account land multiplier
def calculate_money_per_click():
    global upgrades, visible_plots, land_multiplier
    base_gain = visible_plots  # Start with base gain as visible plots

    # Apply tool upgrades
    for upgrade in upgrades.values():
        base_gain *= (upgrade["multiplier"] ** upgrade["quantity"])

    # Apply land multiplier based on the number of plots owned
    base_gain *= land_multiplier
    return int(base_gain)

# Function to buy an upgrade, including "Acre of Land"
def buy_upgrade(upgrade_name, message_label, cost_label, quantity_label):
    global money, upgrades, cps, visible_plots, land_multiplier, cpc, aps

    upgrade = upgrades[upgrade_name]
    cost = upgrade["current_cost"]

    if money >= cost:
        money -= cost
        upgrade["quantity"] += 1

        # Increase cost by 2.5 for "Acre of Land", otherwise by 1.2 for other upgrades
        if upgrade_name == "Acre of Land":
            upgrade["current_cost"] = int(upgrade["current_cost"] * 2.5)
            land_multiplier = upgrade["quantity"]  # Set multiplier based on land owned
        else:
            upgrade["current_cost"] = int(upgrade["current_cost"] * 1.2)

        message_label.config(text=f"You bought 1 {upgrade_name}!", fg="green")

        # Update cps for any upgrade purchase
        cpc = calculate_money_per_click()
        cps_label.config(text=f"Crops per Click: {cpc}")

    else:
        message_label.config(text=f"Couldn't buy 1 {upgrade_name}. \nNot enough money!", fg="red")

    # Update the money and upgrade display
    money_label.config(text=f"Money: {money}")
    cost_label.config(text=f"Cost: {upgrade['current_cost']}")
    quantity_label.config(text=f"Owned: {upgrade['quantity']}")




def upgrade_screen():
    upgrade_screen = tk.Toplevel()  # Use Toplevel instead of Tk
    upgrade_screen.title("Upgrade Screen")
    upgrade_screen.geometry("1000x1000")
    upgrade_screen.configure(bg="black")

    # Message Label for purchase feedback
    message_label = tk.Label(upgrade_screen, text="", fg="yellow", bg="black")
    message_label.grid(row=0, column=2, padx=10, pady=20)

    # Placeholder labels for cost and quantity (will be updated)
    cost_label = tk.Label(upgrade_screen, text="Cost: 0", fg="black", bg="black")
    cost_label.grid(row=1, column=2, padx=10, pady=10)
    quantity_label = tk.Label(upgrade_screen, text="Owned: 0", fg="black", bg="black")
    quantity_label.grid(row=2, column=2, padx=10, pady=10)

    ################################TOOLS################################
    # Tools Section Label
    tools_label = tk.Label(upgrade_screen, text="Tools", fg="white", bg="black")
    tools_label.grid(row=1, column=0, padx=10, pady=5)

    # Function to generate upgrade details text
    def get_upgrade_details(upgrade_name):
        upgrade = upgrades[upgrade_name]
        return (
            f"{upgrade_name}:\n"
            f"Base Cost: {upgrade['base_cost']}\n"
            f"Current Cost: {upgrade['current_cost']}\n"
            f"Description: {upgrade['description']}\n"
            f"Multiplier: {upgrade['multiplier']}\n"
            f"Quantity Owned: {upgrade['quantity']}"
        )
    
    

    # Create Labels for each upgrade
    label_wood = tk.Label(
        upgrade_screen, 
        text=get_upgrade_details("Wood Hoe"), 
        fg="white", bg="black", anchor='w', justify='left', width=75
    )
    label_wood.grid(row=2, column=1)

    label_steel = tk.Label(
        upgrade_screen, 
        text=get_upgrade_details("Steel Hoe"), 
        fg="white", bg="black", anchor='w', justify='left', width=75
    )
    label_steel.grid(row=3, column=1)

    label_gold = tk.Label(
        upgrade_screen, 
        text=get_upgrade_details("Gold Hoe"), 
        fg="white", bg="black", anchor='w', justify='left', width=75
    )
    label_gold.grid(row=4, column=1)

    ################################ANIMALS################################
    # Animals Section Label
    animals_label = tk.Label(upgrade_screen, text="Animals", fg="white", bg="black")
    animals_label.grid(row=5, column=0, padx=10, pady=5)

    label_cow = tk.Label(
        upgrade_screen, 
        text=get_upgrade_details("Cow"), 
        fg="white", bg="black", anchor='w', justify='left', width=75
    )
    label_cow.grid(row=6, column=1)

    label_mule = tk.Label(
        upgrade_screen, 
        text=get_upgrade_details("Mule"), 
        fg="white", bg="black", anchor='w', justify='left', width=75
    )
    label_mule.grid(row=7, column=1)

    label_bull = tk.Label(
        upgrade_screen, 
        text=get_upgrade_details("Bull"), 
        fg="white", bg="black", anchor='w', justify='left', width=75
    )
    label_bull.grid(row=8, column=1)
    ################################ANIMALS################################

    # Load and create images for tools
    try:
        # Wooden Hoe Image
        img = Image.open("Images/wood_hoe.png").resize((90, 90))
        wooden_hoe = ImageTk.PhotoImage(img)
        wooden_hoe_button = tk.Button(
            upgrade_screen, image=wooden_hoe, borderwidth=0,
            command=lambda: buy_upgrade("Wood Hoe", message_label, cost_label, quantity_label)
        )
        wooden_hoe_button.image = wooden_hoe  # Keep a reference
        wooden_hoe_button.grid(row=2, column=0, padx=10, pady=13)

        # Steel Hoe Image
        img2 = Image.open("Images/steel_hoe.png").resize((90, 90))
        steel_hoe = ImageTk.PhotoImage(img2)
        steel_hoe_button = tk.Button(
            upgrade_screen, image=steel_hoe, borderwidth=0,
            command=lambda: buy_upgrade("Steel Hoe", message_label, cost_label, quantity_label)
        )
        steel_hoe_button.image = steel_hoe  # Keep a reference
        steel_hoe_button.grid(row=3, column=0, padx=10, pady=13)

        # Gold Hoe Image
        img3 = Image.open("Images/gold_hoe.png").resize((90, 90))
        gold_hoe = ImageTk.PhotoImage(img3)
        gold_hoe_button = tk.Button(
            upgrade_screen, image=gold_hoe, borderwidth=0,
            command=lambda: buy_upgrade("Gold Hoe", message_label, cost_label, quantity_label)
        )
        gold_hoe_button.image = gold_hoe  # Keep a reference
        gold_hoe_button.grid(row=4, column=0, padx=10, pady=13)

        # Cow Image
        cow_img = Image.open("Images/cow.png").resize((90, 90))
        cow = ImageTk.PhotoImage(cow_img)
        cow_button = tk.Button(
            upgrade_screen, image=cow, borderwidth=0,
            command=lambda: buy_upgrade("Cow", message_label, cost_label, quantity_label)
        )
        cow_button.image = cow  # Keep a reference
        cow_button.grid(row=6, column=0, padx=10, pady=13)

        # Mule Image
        mule_img = Image.open("Images/mule.png").resize((90, 90))
        mule = ImageTk.PhotoImage(mule_img)
        mule_button = tk.Button(
            upgrade_screen, image=mule, borderwidth=0,
            command=lambda: buy_upgrade("Mule", message_label, cost_label, quantity_label)
        )
        mule_button.image = mule  # Keep a reference
        mule_button.grid(row=7, column=0, padx=10, pady=13)

        # Bull Image
        bull_img = Image.open("Images/bull.png").resize((90, 90))
        bull = ImageTk.PhotoImage(bull_img)
        bull_button = tk.Button(
            upgrade_screen, image=bull, borderwidth=0,
            command=lambda: buy_upgrade("Bull", message_label, cost_label, quantity_label)
        )
        bull_button.image = bull  # Keep a reference
        bull_button.grid(row=8, column=0, padx=10, pady=13)
    except Exception as e:
        print(f"Error loading images: {e}")

    # NEW CODE: Display current Crops per Click (cps)
    global cps_label  # Store it globally for updates
    cps_label = tk.Label(upgrade_screen, text=f"Crops per Click: {cps}", fg="white", bg="black")
    cps_label.grid(row=0, column=0, columnspan=2, pady=10)

    ################################TOOLS################################
    ################################ANIMALS################################

    # Function to update all upgrade labels
    def update_labels():
        label_wood.config(text=get_upgrade_details("Wood Hoe"))
        label_steel.config(text=get_upgrade_details("Steel Hoe"))
        label_gold.config(text=get_upgrade_details("Gold Hoe"))
        label_cow.config(text=get_upgrade_details("Cow"))
        label_mule.config(text=get_upgrade_details("Mule"))
        label_bull.config(text=get_upgrade_details("Bull"))
        #cps_label.config(text="CPS: {cps}")
        # Schedule the next update after 1000 milliseconds (1 second)
        upgrade_screen.after(1000, update_labels)

    # Start the label updates
    update_labels()

    # Function to calculate crops per second from animals
def calculate_crops_per_second():
    global upgrades
    crops_per_second = 0

    # Calculate the contribution from each animal
    crops_per_second += upgrades["Cow"]["quantity"] * 5  # Cows contribute 5 CPS
    crops_per_second += upgrades["Mule"]["quantity"] * 15  # Mules contribute 15 CPS
    crops_per_second += upgrades["Bull"]["quantity"] * 25  # Bulls contribute 25 CPS

    return crops_per_second
aps = 0
def click_for_money():
    global money, cps, aps
    money += calculate_money_per_click()  # Increase money based on current multipliers
    money_label.config(text=f"Money: {money}")  # Update the display

# Create the main window
mainscreen = tk.Tk()
mainscreen.title("Happy Harvest")
mainscreen.geometry("400x600")  # Adjusted height to accommodate all buttons

money_label = tk.Label(mainscreen, text=f"Money: {money}",)
money_label.pack(pady=5)


# Function to calculate and apply animal income every second
def calculate_animal_income():
    global money, upgrades

    # Define income rates for each animal type
    income = (
        5 * upgrades["Cow"]["quantity"] +
        15 * upgrades["Mule"]["quantity"] +
        25 * upgrades["Bull"]["quantity"]
    )

    # Increase money by the total income from animals
    money += income
    money_label.config(text=f"Money: {money}")  # Update the money label

    # Schedule the function to run again after 1000 ms (1 second)
    mainscreen.after(1000, calculate_animal_income)

# Start the animal income calculation loop
calculate_animal_income()


# Load and configure the click button image (using hay.png)
try:
    click_img = Image.open("Images/hay.png")  # Use the hay.png image file
    click_img = click_img.resize((100, 100))  # Resize the image as needed
    hay_icon = ImageTk.PhotoImage(click_img)
except Exception as e:
    print(f"Error loading click image: {e}")
    hay_icon = None

# Create the click button with the hay image
click_button = tk.Button(mainscreen, image=hay_icon, command=click_for_money, borderwidth=0)
click_button.image = hay_icon  # Keep a reference to prevent garbage collection
click_button.pack(pady=20)

# Create the upgrade button
upgrade_button = tk.Button(mainscreen, text="Upgrade", command=upgrade_screen, bg="green")
upgrade_button.pack(pady=20)

# Land Screen function with hidden plots
# Farm Land Screen function with hidden plots
# Farm Land Screen function with hidden plots
# Global variables to keep track of the land_screen and purchased labels
land_screen = None  # Initialize to None
purchased_labels = []  # To keep track of purchased plot labels
visible_plots = 1  # To track the number of visible plots
first_plot_revealed = False  # Track if the first plot has been revealed




def farm_land_screen():
    global visible_plots, land_screen, purchased_labels, first_plot_revealed  # Ensure we can access and modify the necessary variables
    rows = 10  # Number of rows
    cols = 10  # Number of columns
    global max_plots
    max_plots = rows * cols  # Total number of plots

    if land_screen is None or not land_screen.winfo_exists():  # Check if the land_screen is not open
        land_screen = tk.Toplevel()  # Create a new Toplevel window
        land_screen.title("Farm Land Screen")
        land_screen.geometry("800x800")
        land_screen.configure(bg="black")

        # Load the land image
        image_path = "Images/land.png"  # Make sure the path is correct
        try:
            img = Image.open(image_path).resize((50, 50))  # Resize to fit in the grid
            photo = ImageTk.PhotoImage(img)  # Convert to PhotoImage for Tkinter
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        # Create a 10x10 grid of image labels
        plot_labels = []  # To keep track of plot labels
        for row in range(rows):
            row_labels = []  # Keep track of the row's labels
            for col in range(cols):
                label = tk.Label(land_screen, image=photo, bg="black")
                label.image = photo  # Keep a reference to the image to avoid garbage collection
                label.grid(row=row, column=col, padx=2, pady=2)  # Adjust padding as needed
                label.grid_remove()  # Initially hide all plots
                row_labels.append(label)
            plot_labels.append(row_labels)  # Store the row labels

        # Restore purchased labels
        for idx in range(len(purchased_labels)):
            row = idx // cols
            col = idx % cols
            if idx < max_plots:  # Ensure we don't exceed the number of plots
                plot_labels[row][col].grid()  # Show previously purchased plots

        # Automatically reveal the first plot only once
        if not first_plot_revealed and visible_plots < max_plots:
            plot_labels[0][0].grid()  # Show the first plot
            purchased_labels.append(plot_labels[0][0])  # Keep track of purchased labels
            visible_plots += 1  # Increment visible plots count
            first_plot_revealed = True  # Set the flag to True after revealing the first plot

        # Create Labels for cost and quantity of Acre of Land
        cost_label = tk.Label(land_screen, text=f"Cost: {upgrades['Acre of Land']['current_cost']}", fg="yellow", bg="black")
        cost_label.grid(row=1, column=11, padx=10, pady=10, sticky='e')  # Align to the right (east)
        quantity_label = tk.Label(land_screen, text=f"Owned: {upgrades['Acre of Land']['quantity']}", fg="yellow", bg="black")
        quantity_label.grid(row=2, column=11, padx=10, pady=10, sticky='e')  # Align to the right (east)
        message_label = tk.Label(land_screen, text="", fg="yellow", bg="black")
        message_label.grid(row=3, column=11, padx=10, pady=10, sticky='e')  # Align to the right (east)

        # Function to buy land
        def buy_land():
            upgrade_name = "Acre of Land"
            upgrade = upgrades[upgrade_name]  # Get the upgrade details
            # Check if enough money is available to buy the land
            if money >= upgrade["current_cost"]:
                buy_upgrade(upgrade_name, message_label, cost_label, quantity_label)  # Purchase land
                reveal_plot()  # Reveal the next plot after purchasing
            else:
                message_label.config(text="Not enough money to buy Acre of Land!", fg="red")

        # Create the button to buy land
        buy_land_button = tk.Button(land_screen, text="Buy Acre of Land", command=buy_land, bg="green")
        buy_land_button.grid(row=4, column=11, padx=10, pady=10, sticky="e")  # Position it below the message label

        # Function to reveal plots based on the number of acres owned
        def reveal_plot():
            global visible_plots, purchased_labels
            # Calculate the maximum number of plots that can be revealed
            max_plots_to_reveal = upgrades["Acre of Land"]["quantity"] * 10
            if visible_plots < max_plots_to_reveal and visible_plots < max_plots:  # Ensure we don't exceed max plots
                # Reveal the next plot
                row = visible_plots // cols
                col = visible_plots % cols
                plot_labels[row][col].grid()  # Show the next plot
                purchased_labels.append(plot_labels[row][col])  # Keep track of purchased labels
                visible_plots += 1  # Increment visible plots count
            else:
                message_label.config(text="All plots are revealed!", fg="yellow")

        # Function to update cost and quantity labels
        def update_land_labels():
            cost_label.config(text=f"Cost: {upgrades['Acre of Land']['current_cost']}")
            quantity_label.config(text=f"Owned: {upgrades['Acre of Land']['quantity']}")
            land_screen.after(1000, update_land_labels)  # Update every second

        update_land_labels()  # Start updating labels
    else:
        land_screen.lift()  # Bring the existing land_screen to the front

    # Function to update cost and quantity labels
    def update_land_labels():
        cost_label.config(text=f"Cost: {upgrades['Acre of Land']['current_cost']}")
        quantity_label.config(text=f"Owned: {upgrades['Acre of Land']['quantity']}")
        land_screen.after(1000, update_land_labels)  # Update every second

    update_land_labels()  # Start updating labels





# Farm Land Button
land_button = tk.Button(mainscreen, text="Farm Land Upgrade", command=farm_land_screen, bg="green")
land_button.pack(pady=20)
def exit_application():
    mainscreen.destroy()  # This will close the main application window

# Create an exit button
exit_button = tk.Button(mainscreen, text="Exit", command=exit_application, fg="red")
exit_button.pack(pady=20)
# Start the main loop
mainscreen.mainloop()