import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, NumberParseException, PhoneNumberType
import threading
import time
import asyncio
import aiohttp
import json
import pyperclip

# Mock function to simulate fetching owner details
def get_owner_details(number):
    time.sleep(2)  # Simulate network delay
    return {
        "Owner Name": "name",
        "Owner Address": "okyanus collage",
        "Owner Email": "emailadress@example.com",
        "Owner Age": "idontknow",
        "Owner Gender": "Male or Famale"
    }

# Function to get phone number details
def get_phone_number_details(number):
    try:
        phone_number = phonenumbers.parse(number)

        if not phonenumbers.is_valid_number(phone_number):
            return "Invalid phone number."

        country = geocoder.description_for_number(phone_number, "en")
        phone_carrier = carrier.name_for_number(phone_number, "en")
        timezones = timezone.time_zones_for_number(phone_number)
        number_type_str = phonenumbers.number_type(phone_number)
        valid_number = phonenumbers.is_valid_number(phone_number)
        possible_number = phonenumbers.is_possible_number(phone_number)
        national_significant_number = phonenumbers.national_significant_number(phone_number)
        region_code = phonenumbers.region_code_for_number(phone_number)
        length_of_national_number = len(national_significant_number)
        line_type = get_line_type(number_type_str)

        owner_details = get_owner_details(number)

        details = {
            "Country": country,
            "Carrier": phone_carrier,
            "Timezones": ", ".join(timezones),
            "Number Type": line_type,
            "Valid Number": valid_number,
            "Possible Number": possible_number,
            "National Significant Number": national_significant_number,
            "Region Code": region_code,
            "Length of National Number": length_of_national_number,
            "E164 format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164),
            "International format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "National format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL),
            "Country Code": phone_number.country_code,
            "National Number": phone_number.national_number,
            "Region": geocoder.region_code_for_number(phone_number)
        }

        details.update(owner_details)
        return details

    except NumberParseException:
        return "Invalid phone number format."

# Function to get line type based on PhoneNumberType
def get_line_type(number_type):
    if number_type == PhoneNumberType.MOBILE:
        return "Mobile"
    elif number_type == PhoneNumberType.FIXED_LINE:
        return "Fixed Line"
    elif number_type == PhoneNumberType.FIXED_LINE_OR_MOBILE:
        return "Fixed Line or Mobile"
    elif number_type == PhoneNumberType.TOLL_FREE:
        return "Toll Free"
    elif number_type == PhoneNumberType.PREMIUM_RATE:
        return "Premium Rate"
    elif number_type == PhoneNumberType.SHARED_COST:
        return "Shared Cost"
    elif number_type == PhoneNumberType.VOIP:
        return "VoIP"
    elif number_type == PhoneNumberType.PERSONAL_NUMBER:
        return "Personal Number"
    elif number_type == PhoneNumberType.PAGER:
        return "Pager"
    elif number_type == PhoneNumberType.UAN:
        return "UAN"
    elif number_type == PhoneNumberType.VOICEMAIL:
        return "Voicemail"
    else:
        return "Unknown"

# Function to validate phone number input
def validate_phone_number(number):
    try:
        phone_number = phonenumbers.parse(number)
        if not phonenumbers.is_valid_number(phone_number):
            return False
        return True
    except NumberParseException:
        return False

# Function to search username across social networks
async def search_username(username):
    results = {}
    links = {
        "Facebook": "https://www.facebook.com/{}",
        "Twitter": "https://www.twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}",
        "LinkedIn": "https://www.linkedin.com/in/{}",
        "GitHub": "https://www.github.com/{}"
    }
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_status(session, social_network, url.format(username), results)
            for social_network, url in links.items()
        ]
        await asyncio.gather(*tasks)
    return results

# Function to check status of each social network link
async def check_status(session, social_network, url, results):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                results[social_network] = url
    except:
        pass

# Function to save results to a JSON file
def save_results_to_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        messagebox.showinfo("Save Results", f"Results saved to {filename}")

# Function to handle "Get Phone Details" button click
def on_get_phone_details():
    number = entry_phone.get()
    if validate_phone_number(number):
        threading.Thread(target=fetch_phone_number_details, args=(number,)).start()
    else:
        messagebox.showerror("Error", "Invalid phone number format.")

# Function to fetch phone number details in a separate thread
def fetch_phone_number_details(number):
    progressbar_phone.start()  # Start the progress bar

    details = get_phone_number_details(number)
    if isinstance(details, dict):
        result = "\n".join([f"{key}: {value}" for key, value in details.items()])
    else:
        result = details

    result_text_phone.config(state=tk.NORMAL)
    result_text_phone.delete(1.0, tk.END)
    result_text_phone.insert(tk.END, result)
    result_text_phone.config(state=tk.DISABLED)

    progressbar_phone.stop()  # Stop the progress bar

# Function to handle "Search Username" button click
def on_search_username():
    username = entry_username.get()
    if username:
        asyncio.run(search_and_display_username(username))
    else:
        messagebox.showerror("Error", "Please enter a username.")

# Function to search and display username results
async def search_and_display_username(username):
    result_text_username.config(state=tk.NORMAL)
    result_text_username.delete(1.0, tk.END)
    result_text_username.insert(tk.END, "Searching... Please wait.")
    result_text_username.config(state=tk.DISABLED)

    results = await search_username(username)

    result_text_username.config(state=tk.NORMAL)
    result_text_username.delete(1.0, tk.END)
    if results:
        result_text_username.insert(tk.END, "Social Media Links Found:\n")
        for network, link in results.items():
            result_text_username.insert(tk.END, f"{network}: {link}\n")
    else:
        result_text_username.insert(tk.END, "No social media links found.")
    result_text_username.config(state=tk.DISABLED)

# Function to save results to a text file
def save_results():
    result_phone_details = result_text_phone.get(1.0, tk.END).strip()
    result_username_details = result_text_username.get(1.0, tk.END).strip()

    if result_phone_details or result_username_details:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                if result_phone_details:
                    file.write("Phone Number Details:\n")
                    file.write(result_phone_details + "\n\n")
                if result_username_details:
                    file.write("Username Search Results:\n")
                    file.write(result_username_details)
                messagebox.showinfo("Save Results", f"Results saved to {file_path}")

# Function to copy phone results to clipboard
def copy_phone_results():
    result_phone_details = result_text_phone.get(1.0, tk.END).strip()
    if result_phone_details:
        pyperclip.copy(result_phone_details)
        messagebox.showinfo("Copy Results", "Phone results copied to clipboard.")

# Function to copy username results to clipboard
def copy_username_results():
    result_username_details = result_text_username.get(1.0, tk.END).strip()
    if result_username_details:
        pyperclip.copy(result_username_details)
        messagebox.showinfo("Copy Results", "Username results copied to clipboard.")

# Function to handle platform choice
def on_platform_choice(choice):
    platform_frame.pack_forget()
    root.geometry("300x200")
    show_choice_frame()

# Function to handle user choice between phone and username search
def on_user_choice(choice):
    choice_frame.pack_forget()
    if choice == "phone":
        show_phone_search()
    else:
        show_username_search()

# Function to handle exit button
def on_exit():
    phone_frame.pack_forget()
    username_frame.pack_forget()
    root.geometry("300x200")
    show_choice_frame()

# Function to show platform choice frame
def show_platform_frame():
    platform_frame.pack(pady=20)

# Function to show user choice frame
def show_choice_frame():
    choice_frame.pack(pady=20)

# Function to show phone search frame
def show_phone_search():
    phone_frame.pack(pady=20)

# Function to show username search frame
def show_username_search():
    username_frame.pack(pady=20)

# Create main application window
root = tk.Tk()
root.title("Information Fetcher")
root.geometry("300x200")

# Create platform choice frame
platform_frame = ttk.Frame(root)

label_platform = tk.Label(platform_frame, text="Select Platform:")
label_platform.pack(pady=10)

button_phone = ttk.Button(platform_frame, text="Phone", command=lambda: on_platform_choice("phone"))
button_phone.pack(pady=10)

button_desktop = ttk.Button(platform_frame, text="Desktop", command=lambda: on_platform_choice("desktop"))
button_desktop.pack(pady=10)

# Create user choice frame
choice_frame = ttk.Frame(root)

label_choice = tk.Label(choice_frame, text="Select Action:")
label_choice.pack(pady=10)

button_phone_info = ttk.Button(choice_frame, text="Get Phone Information", command=lambda: on_user_choice("phone"))
button_phone_info.pack(pady=10)

button_username_search = ttk.Button(choice_frame, text="Search Username", command=lambda: on_user_choice("username"))
button_username_search.pack(pady=10)

# Create phone search frame
phone_frame = ttk.Frame(root)

# Phone search widgets
label_phone = tk.Label(phone_frame, text="Enter the phone number (e.g., +1234567890):")
label_phone.pack(pady=10)

entry_phone = ttk.Entry(phone_frame, width=30)
entry_phone.pack(pady=10)

button_get_phone_details = ttk.Button(phone_frame, text="Get Phone Details", command=on_get_phone_details)
button_get_phone_details.pack(pady=10)

button_save_results_phone = ttk.Button(phone_frame, text="Save Results", command=save_results)
button_save_results_phone.pack(pady=10)

button_copy_results_phone = ttk.Button(phone_frame, text="Copy Results", command=copy_phone_results)
button_copy_results_phone.pack(pady=10)

progressbar_phone = ttk.Progressbar(phone_frame, mode='indeterminate')
progressbar_phone.pack(pady=10)

result_text_phone = tk.Text(phone_frame, height=10, width=40, state=tk.DISABLED, wrap=tk.WORD)
result_text_phone.pack(pady=10)

# Create exit button for phone tab
exit_button_phone = ttk.Button(phone_frame, text="Exit", command=on_exit)
exit_button_phone.pack(pady=10)

# Create username search frame
username_frame = ttk.Frame(root)

# Username search widgets
label_username = tk.Label(username_frame, text="Enter the username:")
label_username.pack(pady=10)

entry_username = ttk.Entry(username_frame, width=30)
entry_username.pack(pady=10)

button_search_username = ttk.Button(username_frame, text="Search Username", command=on_search_username)
button_search_username.pack(pady=10)

button_save_results_username = ttk.Button(username_frame, text="Save Results", command=save_results)
button_save_results_username.pack(pady=10)

button_copy_results_username = ttk.Button(username_frame, text="Copy Results", command=copy_username_results)
button_copy_results_username.pack(pady=10)

result_text_username = tk.Text(username_frame, height=10, width=40, state=tk.DISABLED, wrap=tk.WORD)
result_text_username.pack(pady=10)

# Create exit button for username tab
exit_button_username = ttk.Button(username_frame, text="Exit", command=on_exit)
exit_button_username.pack(pady=10)

# Start by showing the platform choice frame
show_platform_frame()

# Start the main event loop
root.mainloop()
