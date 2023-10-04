
import os
import discord
from discord import app_commands
import pymongo
import asyncio
import re
from datetime import datetime, timedelta
from fpdf import FPDF
import pytz 

client = discord.Client(intents=discord.Intents.all())

linkedin_pattern = r"(https?://www\.linkedin\.com/[^\s]+)"
twitter_pattern = r"(https?://twitter\.com/[^\s]+)"
streaks = {}
cluster = pymongo.MongoClient("mongodb+srv://root:toor@quest.ngjpxct.mongodb.net/?retryWrites=true&w=majority")

db = cluster["Userdata"]
# print(db.list_collection_names())
collection = db["Userdata"]
# collection.insert_one({"test": "document", "hello": "world"})
@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author != client.user and client.user is not None:
      # Check if the bot is mentioned in the message
      
        # Extract the message content excluding bot mention
        bot_mention = f'<@{client.user.id}>'
        if bot_mention in message.content:
          message_content = message.content.replace(bot_mention, '').strip()
      
        message_content = message.content
        linkedin_match = re.search(linkedin_pattern, message_content)
        twitter_match = re.search(twitter_pattern, message_content)
        if linkedin_match or twitter_match:
            user_id = message.author.id
            if user_id not in streaks:
              streaks[user_id] = 1

        # Check if the message is posted within the last 24 hours
            ist = pytz.timezone('Asia/Kolkata')

        # Make one_day_ago a timezone-aware datetime object in UTC
            one_day_ago = datetime.now(ist) - timedelta(days=1)

        # Convert message.created_at to UTC (assuming Discord timestamps are in UTC)
            message_time = message.created_at.astimezone(ist)

        # Compare message creation time with one day ago
              
            if message_time > one_day_ago:
            # Update the user's streak count if they posted a message within the last 24 hours
               streaks[user_id] += 1
            else:
            # If the user didn't post a message within the last 24 hours, reset their streak
               streaks[user_id] = 0
            if streaks[user_id] ==30:
            # User successfully completed the challenge, handle the completion here
              print(f'User {user_id} completed the 30-day challenge!')
              export_to_pdf()
        print(f'hello')
        if linkedin_match:
                    print(f'hello')
                    linkedin_link = linkedin_match.group()
                    post = {"type": "LinkedIn", "link": linkedin_link}
                    participant_id = message.author.id
                    try:
                        update_participant_entry(participant_id, post)
                        await message.channel.send(f'LinkedIn data inserted for user {participant_id}: {linkedin_link}')
                    except Exception as e:
                        print(f'Error inserting LinkedIn data: {e}')

        if twitter_match:
                    print(f'hello')
                    twitter_link = twitter_match.group()
                    post = {"type": "Twitter", "link": twitter_link}
                    participant_id = message.author.id
                    try:
                        update_participant_entry(participant_id, post)
                        await message.channel.send(f'Twitter data inserted for user {participant_id}: {twitter_link}')
                    except Exception as e:
                        print(f'Error inserting Twitter data: {e}')
    # except Exception as e:
    #     print(f'Error processing message: {e}')

def update_participant_entry(participant_id, post):
    try:
        # Check if the participant document exists in the collection
        existing_participant = collection.find_one({"_id": participant_id})
        if existing_participant:
            entries = existing_participant.get("entries", [])
            entries.append(post)
            # Update the participant's document with the new entry
            collection.update_one({"_id": participant_id}, {"$set": {"entries": entries}})
        else:
            # Create a new participant document if it doesn't exist
            new_participant = {"_id": participant_id, "entries": [post]}
            collection.insert_one(new_participant)
    except Exception as e:
        print(f'Error updating participant entry: {e}')


def export_to_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="List of Eligible Participants", ln=True, align='C')

    for user_id in streaks:
      if streaks[user_id] ==30:
        pdf.cell(200, 10, txt=f"User ID: {user_id}, Streak: {streaks[user_id]}", ln=True, align='L')

    pdf.output("eligible_participants.pdf")

for user_id, streak_count in streaks.items():
    print(f"User ID: {user_id}, Streak: {streak_count}")    

my_secret = os.environ["TOKEN"]
client.run(my_secret)