import os
import requests
from pyrogram import Client, filters

# Imgur API Configuration
CLIENT_ID = "1af151af965771d"  # Replace with your Imgur Client ID
UPLOAD_URL = "https://api.imgur.com/3/upload"

# Telegram API Credentials (replace with your own)
API_ID = 17238318  # Replace with your API ID from https://my.telegram.org/auth
API_HASH = "44c77084fdd15c10a6042371fda66630"  # Replace with your API Hash from https://my.telegram.org/auth
API_TOKEN = "7907138425:AAFeqsw6B4eR3J6Cc8BoV1hjgi_WcYNhskg"  # Replace with your Telegram bot API token

# Set up the Pyrogram client
app = Client("imgur_upload_bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)


def upload_image(image_path):

    if not os.path.exists(image_path):
        raise Exception(f"File does not exist at the path: {image_path}")
    
    headers = {
        "Authorization": f"Client-ID {CLIENT_ID}"
    }
    

    with open(image_path, "rb") as file:
        files = {
            "image": file
        }
        
        response = requests.post(UPLOAD_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        data = response.json()
        return data["data"]["link"]
    else:
        raise Exception(f"Failed to upload image. Error: {response.text}")

# Command to handle /start
@app.on_message(filters.command("start"))
async def start(client, message):

    welcome_message = """
    Welcome to the Imgur Upload Bot!

    To use this bot:
    1. Send an image to the bot.
    2. The bot will upload it to Imgur and return the link.

    Enjoy sharing your images!
    """
    await message.reply(welcome_message)

# Command to handle photo uploads from users
@app.on_message(filters.photo)
async def handle_photo(client, message):

    file_id = message.photo.file_id
    
    # Download the photo to a local file
    downloaded_file = await message.download()
    
    try:
        # Upload the image to Imgur
        image_url = upload_image(downloaded_file)
        
        # Send the uploaded image URL back to the user
        await message.reply(f"Image successfully uploaded: {image_url}")
        
    except Exception as e:
        await message.reply(f"Failed to upload image: {str(e)}")
    

    os.remove(downloaded_file)

# Start the bot
if __name__ == "__main__":
    app.run()
