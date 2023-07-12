import tkinter as tk
from PIL import ImageTk, Image
import random
import requests
from bs4 import BeautifulSoup
import os
from gtts import gTTS
import pygame

stoic_website_url = "https://iep.utm.edu/stoicism/"
# The URL of the Stoic website from which quotes will be fetched

image_url = "https://dailystoic.com/wp-content/uploads/2016/07/marcusaureliusdailystoic-scaled.jpg"
# The URL of the image to be displayed alongside the Stoic quote

image_path = os.path.join(os.getcwd(), "download (2)")
# The local path where the downloaded image will be saved

def get_stoic_quotes():
    # Send a GET request to the Stoic website
    response = requests.get(stoic_website_url)

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
    else:
        # If the request fails, print an error message and return an empty list
        print("Failed to retrieve Stoic quotes. Status code:", response.status_code)
        return []

def download_image():
    # Download the image from the given URL
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # If the download is successful, save the image to the specified path
        with open(image_path, "wb") as file:
            file.write(response.content)
        return True
    else:
        # If the download fails, print an error message with the status code
        print("Failed to download image. Status code:", response.status_code)
        return False

def text_to_speech(text, filename):
    # Convert the given text to speech and save it as an audio file
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

def play_audio(filename):
    # Play the audio file
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def display_stoic_popup():
    quotes = get_stoic_quotes()  # Fetch Stoic quotes
    if quotes:
        quote = random.choice(quotes)  # Select a random quote from the retrieved quotes
    else:
        quote = "No Stoic quotes found."

    def update_quote():
        # Update the displayed quote with a new random quote
        new_quote = random.choice(quotes)
        quote_text.configure(state="normal")
        quote_text.delete("1.0", tk.END)
        quote_text.insert(tk.END, new_quote)
        quote_text.configure(state="disabled")

    def read_out_loud():
        # Convert the quote to speech and play it
        filename = "quote_audio.mp3"
        text_to_speech(quote, filename)
        play_audio(filename)

    root = tk.Tk()
    root.title("Stoic Quote")
    root.geometry("800x700")  # Adjust the window size as needed

    if download_image():
        # If the image download is successful, open and display the image
        image = Image.open(image_path)
        image = image.resize((500, 500), Image.LANCZOS)

        image_label = tk.Label(root)
        image_label.pack(pady=20)

        button_frame = tk.Frame(root)
        button_frame.pack()

        read_button = tk.Button(button_frame, text="Read Out Loud", command=read_out_loud)
        read_button.pack(side=tk.LEFT, padx=5, pady=10)

        make_another_button = tk.Button(button_frame, text="Make Another Quote", command=update_quote)
        make_another_button.pack(side=tk.LEFT, padx=5, pady=10)

        quote_frame = tk.Frame(root)
        quote_frame.pack(pady=20)

        quote_text = tk.Text(quote_frame, wrap="word", font=("Serif", 16))
        quote_text.pack(side=tk.LEFT, fill=tk.Y)

        quote_scroll = tk.Scrollbar(quote_frame, command=quote_text.yview)
        quote_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        quote_text.configure(yscrollcommand=quote_scroll.set)
        quote_text.insert(tk.END, quote)
        quote_text.configure(state="disabled")

        image_tk = ImageTk.PhotoImage(image)
        image_label.config(image=image_tk)
        image_label.image = image_tk

    else:
        # If the image download fails, display only the quote
        quote_label = tk.Label(root, text=quote, font=("Serif", 16), wraplength=600)
        quote_label.pack(pady=20)

        button_frame = tk.Frame(root)
        button_frame.pack()

        read_button = tk.Button(button_frame, text="Read Out Loud", command=read_out_loud)
        read_button.pack(side=tk.LEFT, padx=5, pady=10)

        make_another_button = tk.Button(button_frame, text="Make Another Quote", command=update_quote)
        make_another_button.pack(side=tk.LEFT, padx=5, pady=10)

    root.mainloop()

# Initialize the pygame mixer
pygame.mixer.init()

# Display Stoic quote pop-up
display_stoic_popup()
