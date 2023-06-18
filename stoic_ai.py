#!/usr/bin/env python3

"A program to fetch stoic quotations and display them"

import random
import os
import tkinter as tk
from PIL import ImageTk, Image
import requests
from bs4 import BeautifulSoup

# The URL of the Stoic website from which quotes will be fetched
STOIC_WEBSITE_URL = "https://iep.utm.edu/stoicism/"

# The URL of the image to be displayed alongside the Stoic quote
IMAGE_URL = "https://dailystoic.com/wp-content/uploads/2016/07/marcusaureliusdailystoic-scaled.jpg"

# The local path where the downloaded image will be saved
image_path = os.path.join(os.getcwd(), "download (2)")


def get_stoic_quotes():
    "Fetch quotations from the web and extract them to a list"

    # Send a GET request to the Stoic website
    response = requests.get(STOIC_WEBSITE_URL)

    if response.status_code == 200:
        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific element containing the Stoic quotes
        content_element = soup.find('div', class_='entry-content')

        # Find all <p> elements within the content element
        quotes = content_element.find_all('p', recursive=False)

        # Extract the text from each quote and remove any leading or trailing whitespace
        quotes = [quote.get_text(strip=True) for quote in quotes]

        # Return the list of Stoic quotes
        return quotes

    # If the request fails, print an error message and return an empty list
    print("Failed to retrieve Stoic quotes. Status code:", response.status_code)
    return []


def download_image():
    "Download the image"
    # Download the image from the given URL
    response = requests.get(IMAGE_URL, stream=True)
    if response.status_code == 200:
        # If the download is successful, save the image to the specified path
        with open(image_path, "wb") as file:
            file.write(response.content)
        return True

    # If the download fails, print an error message with the status code
    print("Failed to download image. Status code:", response.status_code)
    return False


def display_stoic_popup():
    "Display the image"
    quotes = get_stoic_quotes()  # Fetch Stoic quotes
    if quotes:
        quote = random.choice(quotes)  # Select a random quote from the retrieved quotes
    else:
        quote = "No Stoic quotes found."

    root = tk.Tk()
    root.title("Stoic Quote")
    root.geometry("800x700")  # Adjust the window size as needed

    if download_image():
        # If the image download is successful, open and display the image
        image = Image.open(image_path)
        image = image.resize((500, 500), Image.ANTIALIAS)

        # Create an empty label widget for displaying an image
        image_label = tk.Label(root)

        # Pack the image label widget into the main window with some vertical padding
        image_label.pack(pady=20)

        # Create a label widget for displaying a quote with specified font and wrap length
        quote_label = tk.Label(root, text=quote, font=("Serif", 16), wraplength=600)

        # Pack the quote label widget into the main window with some vertical padding
        quote_label.pack(pady=20)

        def update_quote():
            # Update the displayed quote with a new random quote
            quote_label.config(text=random.choice(quotes))
            root.after(60000, update_quote)  # Update the quote every 60 seconds

        update_quote()

        # Create a Tkinter-compatible photo image from the loaded image
        image_tk = ImageTk.PhotoImage(image)

        # Configure the image label widget to display the photo image
        image_label.config(image=image_tk)

        # Store a reference to the photo image in the image label
        # widget to prevent it from being garbage collected

        image_label.image = image_tk

    else:
        # If the image download fails, display only the quote
        quote_label = tk.Label(root, text=quote, font=("Serif", 16), wraplength=600)
        quote_label.pack(pady=20)

    root.mainloop()


# Display Stoic quote pop-up
display_stoic_popup()
