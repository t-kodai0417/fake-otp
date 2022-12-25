import requests
import disnake
from disnake.ext import commands

TOKEN = "token"
OTP_API_URL = "localhost:5000"#example

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!?", intents=intents)

@bot.event
async def on_message(message):
    if message.content == "!panel":
        buttons = [
            disnake.ui.Button(label="1", style=disnake.ButtonStyle.primary,custom_id="1"),
            disnake.ui.Button(label="2", style=disnake.ButtonStyle.primary,custom_id="2"),
            disnake.ui.Button(label="3", style=disnake.ButtonStyle.primary,custom_id="3")
        ]
        actionrow1 = disnake.ui.ActionRow()
        for i in buttons:
            actionrow1.append_item(i)

        buttons = [
            disnake.ui.Button(label="4", style=disnake.ButtonStyle.primary,custom_id="4"),
            disnake.ui.Button(label="5", style=disnake.ButtonStyle.primary,custom_id="5"),
            disnake.ui.Button(label="6", style=disnake.ButtonStyle.primary,custom_id="6")
        ]
        actionrow2 = disnake.ui.ActionRow()
        for i in buttons:
            actionrow2.append_item(i)
        
        buttons = [
            disnake.ui.Button(label="7", style=disnake.ButtonStyle.primary,custom_id="7"),
            disnake.ui.Button(label="8", style=disnake.ButtonStyle.primary,custom_id="8"),
            disnake.ui.Button(label="9", style=disnake.ButtonStyle.primary,custom_id="9")
        ]
        actionrow3 = disnake.ui.ActionRow()
        for i in buttons:
            actionrow3.append_item(i)
        
        buttons = [
            disnake.ui.Button(label=" ", style=disnake.ButtonStyle.secondary,custom_id="a",disabled=True),
            disnake.ui.Button(label="0", style=disnake.ButtonStyle.primary,custom_id="0"),
            disnake.ui.Button(label=" ", style=disnake.ButtonStyle.secondary,custom_id="aa",disabled=True)
        ]
        actionrow4 = disnake.ui.ActionRow()
        for i in buttons:
            actionrow4.append_item(i)
        
        components = [actionrow1,actionrow2,actionrow3,actionrow4]
        await message.channel.send(components=components)
        
        
@bot.event
async def on_button_click(inter):
    try:
        await inter.response.send_message("",ephemeral=True)
    except:
        None
    requests.get(f"http://{OTP_API_URL}/api",params={"phone":f"{inter.author.id}","number":inter.data.custom_id})
    

if __name__ == "__main__":
    bot.run(TOKEN)
