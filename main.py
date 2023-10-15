
import os
import discord
from discord import app_commands
from discord.message import Message
import pymongo
import asyncio
import re
from datetime import datetime, timedelta
import pytz 
from export import export_to_pdf
from update_entry import update_participant_entry
from update_streaks import update_streaks
from wrapper import ApiWrapper
import tatsu.data_structures

client = discord.Client(intents=discord.Intents.all())

linkedin_pattern = r"(https?://www\.linkedin\.com/[^\s]+)"
twitter_pattern = r"(https?://twitter\.com/[^\s]+)"
cluster = pymongo.MongoClient("mongodb+srv://root:toor@quest.ngjpxct.mongodb.net/?retryWrites=true&w=majority")

db = cluster["Userdata"]

collection = db["Userdata"]
db1= cluster["Streaks"]
streaks_collection= db1["Streaks"] # for storing users' streaks

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    if message.author != client.user and client.user is not None:
      # Check if the bot is mentioned in the message

        # Extract the message content excluding bot mention

        bot_mention = f'<@{client.user.id}>'

        if message.content.startswith('!rank'):
                # Fetch the user's rank card
                id=message.author.id
                wrapper = ApiWrapper(key="rxkLxig1Fx-7dQD5Y7kZQLOWzBMWwpPVf")
                ranki = await wrapper.get_member_ranking(1158657622069760060, message.author.id)  # Await the function to get the result
                await message.channel.send(ranki.rank)

        if message.content.startswith('!get_pdf') and message.author.id == message.guild.owner.id:
          users_data = streaks_collection.find({"streak": 2})
          pdf_filename = export_to_pdf(users_data)
          await message.channel.send("Pdf has been exported")



        if bot_mention in message.content:
          message_content = message.content.replace(bot_mention, '').strip()

        message_content = message.content
        linkedin_match = re.search(linkedin_pattern, message_content)
        twitter_match = re.search(twitter_pattern, message_content)
        user_name=message.author.name
        participant=streaks_collection.find_one({"_id": user_name})  
        if linkedin_match or twitter_match:

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
              ist = pytz.timezone("Asia/Kolkata")
              update_streaks(streaks_collection, datetime.now(ist), user_name, participant)
          else:
              await message.channel.send(f'Hello {message.author.mention}, you have already posted this LinkedIn link. Please provide a new one.')

        if twitter_match:
            twitter_link = twitter_match.group()
            post = {"type": "Twitter", "link": twitter_link}
            participant_id = message.author.id
            post_added = update_participant_entry(participant_id, post,collection)

            if post_added:
                await message.channel.send(f"Hello {message.author.mention}, Thank you for participating in the challenge, make sure to maintain your streak and get a chance to win exciting rewards😎") 
                ist = pytz.timezone("Asia/Kolkata")
                update_streaks(streaks_collection, datetime.now(ist), user_name, participant)
            else:
                await message.channel.send(f'Hello {message.author.mention}, you have already posted this Twitter link. Please provide a new one.')




my_secret = os.environ["TOKEN"]
client.run(my_secret)