
import pytz 
ist = pytz.timezone("Asia/Kolkata")
def update_streaks(streaks_collection,message_time,user_name,participant):
    ist = pytz.timezone("Asia/Kolkata")

    if not participant :
      streaks_collection.insert_one(
    {"_id": user_name, "streak": 1,
    "last_post": message_time})

    if participant and (message_time-participant.get("last_post").astimezone(ist)).total_seconds()/60 >= 1440:

      streaks_collection.update_one(
    {"_id": user_name},
    {
        "$inc": {
            "streak": 1
        },
        "$set": {

            "last_post": message_time
        }
    })

    else:
  # If the user didn't post a message within the last 24 hours, reset their streak

     streaks_collection.update_one(
    {"_id": user_name},
    {
        "$set": {
          "streak": 1,
          "last_post": message_time

        }
    })


