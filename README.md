Hello, this is an information gathering project. The project includes the feature of collecting information from phone numbers and searching for user names. This project should not be used for illegal activities and I am not responsible if it is used.
The project is completely coded in Python language.
Libraries Used
tkinter:

Function: It is a standard library used to create GUI in Python. With Tkinter, windows, buttons, tags, text boxes and other GUI components can be created.
Example Usage: It is used to create and place GUI components.
messagebox:

Function: It is part of Tkinter and is used to create information, warning and error message boxes.
Example Usage: messagebox.showinfo, messagebox.it is used to show information or error messages to the user with showerror functions.
tcc:

Function: It is a module that offers more modern and stylized components of Tkinter.
Example Usage: TCC.Frame, ttc.Button, ttk.It is used to create components such as Entry.
phonenumbers:

Function: It is used to verify phone numbers, format them, and retrieve various information about the phone number.
Example Usage: phonenumbers.parse, phonenumbers.is_valid_number, geocoder.functions such as description_for_number are used for phone number verification and information retrieval.
threading:

Function: Provides the ability to create multiple threads (threads) to be able to perform multiple operations at the same time.
Example Usage: threading.It is used to execute transactions in the background with Thread.
asyncio and aiohttp:

Function: Used for asynchronous programming. In particular, it is useful for reducing waiting times when making network requests.
Example Usage: asyncio.run, aiohttp.It is used to make asynchronous network requests with ClientSession.
json:

Function: Performs data reading and writing operations in JSON format.
Example Usage: json.it is used to save the results to a JSON file with dump.
pyperclip:

Function: Used to copy text to clipboard.
Example Usage: pyperclip.it is used to copy the results to the clipboard with copy.
Important Places and Functions of the Code
get_phone_number_details:

Function: Provide various information about the entered phone number (country, operator, time zone, etc.) takes and returns.
Important Point: It checks the validity of the phone number and returns its information in various formats.
search_user:

Function: Searches for the entered username on social media platforms and returns the found links.
Important Point: It works asyn Decently and searches various social media platforms.
GUI Components:

Function: It is used to create the user interface and get information from the user.
Important Point: It shows the relevant frames according to user choices and manages user interactions.
copy_phone_results and copy_username_results:

Function: Decrypts the phone number or username search results to the clipboard.
Important Point: It allows the user to easily copy the results to the clipboard.
save_results_to_json:

Function: Decrypts the search results to a JSON format file.
Important Point: It offers the user the possibility to save the results as a file.
Purpose of Use of the Code
This code is used for users who want to collect information about phone numbers and usernames. Users can get various information (for example, country, operator, time zone for the phone number; social media profiles for the username) by entering their phone number or username. The application also offers additional October functions such as copying information to the clipboard and saving it as a file. This is especially useful for people doing research or users who want to do phone number or username verification.
