import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from itertools import cycle
import datetime
import random
import requests
import os

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

client = discord.ext.commands.Bot(command_prefix = '>')
TOKEN = 'NDE4MDcwMDE4NDA5MTAzMzcw.DpuzOw.q6pq6HEy0MwMY7PeK9Q4_R0KPPE'
now = datetime.datetime.utcnow().isoformat() + '+03:00'
change = []

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

@client.event
async def on_ready():
    print("Bot is on the server")
    print("Voice ready:",discord.opus.is_loaded())
    print("Name:",client.user.name)
    print("ID:",client.user.id)


@client.event
async def on_member_update(before,after):
    if str(before.status) != str(after.status):
        current_member = {  'name' : str(after.name),
                            'before_status' : str(before.status),
                            'after_status' : str(after.status),
                            'change_time' : str(datetime.datetime.utcnow().isoformat() + '+00:00')
                          }
        if len(change) == 0:
            change.append(current_member)
        else:
            for i in range(0,len(change)):
                changed_member = change[i]
                if str(changed_member['name']) == str(current_member['name']):
                    member_name = str(current_member['name'])
                    clevent = str(current_member['before_status'])
                    start_time = str(changed_member['change_time'])
                    end_time = str(current_member['change_time'])
                    await client.send_message(discord.Object(id='502856854251241482'),str('\n'+member_name+'\n'+
                                                                                               clevent+'\n'+
                                                                                               start_time+'\n'+
                                                                                               end_time))
                    event_body = {
                      'summary': member_name + ' was ' + clevent,
                      'start': {
                        'dateTime': start_time,
                        'timeZone': 'Europe/Moscow',
                      },
                      'end': {
                        'dateTime': end_time,
                        'timeZone': 'Europe/Moscow',
                      }
                    }
                    event = service.events().insert(calendarId='omf4r9khmb7jqj4tc4d1cfvi3c@group.calendar.google.com',
                                                    body=event_body).execute()
                else:
                    change.append(current_member)


client.run(TOKEN)
