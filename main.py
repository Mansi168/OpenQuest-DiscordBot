
import os
import discord
from discord import app_commands
import pymongo
import asyncio
import re
from datetime import datetime, timedelta
import pytz 
from export import export_to_pdf
from update_entry import update_participant_entry

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

        # Make one_day_ago a timezone-aware datetime object in IST
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
              export_to_pdf(streaks)
        
            hashtag_pattern = r'#\w+'
            hashtags = re.findall(hashtag_pattern, message_content)
        
        # Check if the message contains a screenshot attachment
            has_screenshot = any(attachment.width and attachment.height for attachment in message.attachments)

        # Validate format (for example: check for hashtags and screenshot)
            if not hashtags or not has_screenshot:
            # Warn the user about incorrect format
              user_mention=message.author
              await message.channel.send(f"Hello{user_mention.mention}, please make sure to include proper hashtags and attach a screenshot.")

        if linkedin_match:
          linkedin_link = linkedin_match.group()
          post = {"type": "LinkedIn", "link": linkedin_link}
          participant_id = message.author.id
          post_added = update_participant_entry(participant_id, post,collection)
      
          if post_added:
              await message.channel.send(f"Hello {message.author.mention}, Thank you for participating in the challenge, make sure to maintain your streak and get a chance to win exciting rewards😎")
          else:
              await message.channel.send(f'Hello {message.author.mention}, you have already posted this LinkedIn link. Please provide a new one.')
      
        if twitter_match:
            twitter_link = twitter_match.group()
            post = {"type": "Twitter", "link": twitter_link}
            participant_id = message.author.id
            post_added = update_participant_entry(participant_id, post,collection)
        
            if post_added:
                await message.channel.send(f"Hello {message.author.mention}, Thank you for participating in the challenge, make sure to maintain your streak and get a chance to win exciting rewards😎")
            else:
                await message.channel.send(f'Hello {message.author.mention}, you have already posted this Twitter link. Please provide a new one.')
        
  

for user_id, streak_count in streaks.items():
    print(f"User ID: {user_id}, Streak: {streak_count}")    

my_secret = os.environ["TOKEN"]
client.run(my_secret)