#!/usr/bin/env python3
#
# Copyright 2020 Mark "Grandy" Bishop (Grandy#0243)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to  use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import discord
from discord.ext import commands
from mgz.summary import Summary
from myconsts import CIVS
from io import BytesIO
import zipfile

class AoE2Bot(discord.Client):
	async def on_ready(self):
		print('Connected!')
		print('Username: {0.name}\nID: {0.id}'.format(self.user))

	async def on_message(self, message):
		if message.attachments:
			# Check if right file type
			for attachment in message.attachments:
				if attachment.filename.endswith('aoe2record'):
					print(".aoe2record file received: " + attachment.filename)
					await message.add_reaction('☑️')
					await message.channel.send(embed=await self.get_embed_from_attachment(attachment))
				elif attachment.filename.endswith('zip'):
					print(".zip file received: " + attachment.filename)
					for bytes in (await self.get_bytes_from_zip(attachment)):
						await message.channel.send(embed=await self.get_embed_from_bytes(bytes))
					await message.add_reaction('☑️')
				else:
					print("Invalid file received: " + attachment.filename)

		elif message.content.startswith('!ageofrecs'):
			embedVar = discord.Embed(title="AgeOfRecs, an AoE2 rec games parser Discord bot")
			embedVar.set_thumbnail(url="https://media.discordapp.net/attachments/791024017837522955/791685521046110229/icon.png")
			embedVar.description = "Created in python by Mark 'Grandy' Bishop (Grandy#0243), using:"

			embedVar.add_field(name="Discord.py (discord lib)", value="https://discordpy.readthedocs.io/en/latest/api.html", inline=False)
			embedVar.add_field(name="MGZ (AoE2 rec game parser by happyleavesaoc)", value="https://github.com/happyleavesaoc/aoc-mgz", inline=False)
			await message.channel.send(embed = embedVar)

	# returns list of bytes, one per .aoe2record file found within the root level of the zip
	# note: this doesn't recurse; it only checks the root level, not directories beneath it
	async def get_bytes_from_zip(self, attachment):
		print("Getting files from zip.")
		buffer = BytesIO(await attachment.read())
		z = zipfile.ZipFile(buffer)
		print(z.infolist())
		files = []
		for info in z.infolist():
			if info.filename.endswith('aoe2record'):
				print ("Found .aoe2record within zip: " + info.filename)
				fi = z.open(info)
				files.append(fi)
		return files

	# generate a resulting embed from the byte stream
	async def get_embed_from_bytes(self, bytes):
		s = Summary(bytes)
		embedVar = discord.Embed()
		winner = ""

		i = 0
		for player in s.get_players():
			name = player['name']

			playerLine = name + " ||*(" + CIVS[player['civilization']] + ")*||";
			embedVar.add_field(name="Team " + str(i+1), value=playerLine, inline=True)
			print(playerLine)

			if player['winner']:
				winner = name
			i += 1

		winner = "||" + winner + "||" if winner else "*(none detected)*";
		embedVar.title = "Map: ||" + s.get_map()['name'] + "|| | Winner: " + winner
		return embedVar

	# generate a resulting embed from an attachment; converts to byte stream and uses above
	async def get_embed_from_attachment(self, attachment):
		print("Getting embed for attachment.")
		return await self.get_embed_from_bytes(BytesIO(await attachment.read()))

client = AoE2Bot()
client.run('YOUR_TOKEN_HERE')