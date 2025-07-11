# from discord.ext import commands, tasks
# from googleapiclient.discovery import build
# from datetime import datetime, timezone, timedelta
# import discord
# from GlobalVariable import YOUTUBE_API_KEY
# from GlobalVariable import CHANNEL_ID
#
# youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
# last_video_id = None
#
#
# @tasks.loop(minutes=5)
# async def check_new_video(bot: commands.Bot):
#     global last_video_id
#
#     # Fetch videos from the channel
#     request = youtube.search().list(
#         part="snippet", channelId=CHANNEL_ID, maxResults=1, order="date"
#     )
#     response = request.execute()
#     response = response["items"][0]
#     video_id = response["id"]["videoId"]
#     video_title = response["snippet"]["title"]
#     video_url = f"https://www.youtube.com/watch?v={video_id}"
#     publisheAt = response["snippet"]["publishedAt"]
#
#     if last_video_id == video_id:
#         return
#     last_video_id = video_id
#     # Convert published_at to a datetime object
#     publisheAtDate = datetime.strptime(publisheAt, "%Y-%m-%dT%H:%M:%SZ")
#     publisheAtDate = publisheAtDate.replace(tzinfo=timezone.utc)
#
#     # Get the current time in UTC
#     timeNow = datetime.now(timezone.utc)
#
#     # Check if the video is new (published in the last 30 minutes)
#     if (timeNow - publisheAtDate) <= timedelta(minutes=30):
#         channel = bot.get_channel(1272994154405957656)
#         if channel and isinstance(channel, discord.TextChannel):
#             await channel.send(f"New video on the channel: {video_title}\n{video_url}")
#         else:
#             print("Channel not found")
#             print(channel)
