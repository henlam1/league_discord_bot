# bot.py
import sys
import discord
import os

sys.path.append('../discord_bot')

from datetime import datetime
from create_images.skill_priority_image import create_skill_priority_image
from create_images.runes_image import create_rune_image
from create_images.starting_items_image import create_starting_items_image
from create_images.build_image import create_build_image
from create_images.final_image import build_final_image
from create_images.summoner_spells_image import create_summoner_spells_image
from create_embed import embed
from data_scrape.get_information import get_information
from utils import delete_files

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

"""
INPUT: User messages from a discord channel
OUTPUT: Outputs discord embeds for the champion build
DESCRIPTION: Recognizes messages starting with "8=D" and gets the recommended build of the champion requested in the message.
"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message.content 
    # initial command
    if command.startswith('/build'):
        try: 
            roles = ['top', 'jungle', 'mid', 'middle', 'adc', 'support', 'aram']
            champion_and_role = command.split('/build')[1].strip()
            champion_and_role = champion_and_role.split(" ")
            words = len(champion_and_role)
            champion_and_role = " ".join(champion_and_role)
            
            if words >= 3:
                champion_and_role = champion_and_role.rsplit(" ", 1)
            else:
                if any(role in champion_and_role for role in roles):
                    champion_and_role = champion_and_role.split(" ")
                else:
                    champion_and_role = [champion_and_role]
            champion = champion_and_role[0]

            role = ""
            # role might not be specified
            try:
                role = champion_and_role[1]
                if role == 'mid':
                    role = 'middle'
                build = get_information(champion, role)
            except IndexError:
                build = get_information(champion)

            #First Embed - Title, Champion Thumbnail, Runes, Summoner Spells
            embedVar = embed(champion, role, build)

            runes = create_rune_image(build.runes)
            runes.save('runes.png')

            summoners = create_summoner_spells_image(build.summoners)
            summoners.save("summoners.png")

            starting_items = create_starting_items_image(build.starting_items)
            starting_items.save("starting_items.png")

            final_build = create_build_image(build.build)
            final_build.save("final_build.png")

            skill_priority = create_skill_priority_image(build.skill_priority)
            skill_priority.save('skill_priority.png')

            # combine all the images into one
            final_image = build_final_image(['runes.png', 'summoners.png', 'starting_items.png', 'final_build.png', 'skill_priority.png'])
            final_image.save('final_image.png')

            file = discord.File("final_image.png", filename = "final_image.png")
            embedVar.set_image(url = "attachment://final_image.png")
            
            print(f"start: {datetime.now()}")
            await message.channel.send(embed = embedVar, file = file)
            print(f"end: {datetime.now()}")

            # delete all the files
            all_files = ['runes.png', 'summoners.png', 'starting_items.png', 'final_build.png', 'skill_priority.png', 'final_image.png']
            delete_files(all_files)

        except Exception as err:
            await message.channel.send(f"u dum dum do champ name and role, {err}")

if __name__ == "__main__":
    client.run(TOKEN)
