import os
from quart import Quart, request
from threading import Thread
import contextlib
import io
from traceback import format_exception
import textwrap
import json
from discord_webhook import DiscordWebhook
import discord
import urllib.parse
from datetime import datetime, timezone

app = Quart(__name__)

async def _eval(code):
  local_variables = {
      "discord" : discord,
      "test" : "[print(i) for i in range(10)]"
    }

  stdout = io.StringIO()

  try:
      with contextlib.redirect_stdout(stdout):
          exec(
              f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
          )

          obj = await local_variables["func"]()
          result = f"{stdout.getvalue()}\n> {obj}\n"
          return result
  except Exception as e:
      result = "".join(format_exception(e, e, e.__traceback__))
      return result

@app.route("/api/check", methods=["GET", "POST"])
async def check():
  with open("listings.txt", "r") as E:
    if request.headers.get("ID") in E.readlines():
      return {"message" : "403 User not authorized."}
  with open("./logs/users.txt", "a") as E:
    E.write("")
    return "REXEC Server detected"


@app.route("/api/run", methods=['GET', 'POST'])
async def evaluate():
    author_name = request.headers.get('author_info')
    webhook = request.headers.get("webhook")
    code_bytes = await request.get_data()
    code_uc = code_bytes.decode("utf-8")
    code_ic = code_uc.replace("+", " ")
    code = urllib.parse.unquote(code_ic)
    with open("code-logs.txt", "a") as E:
        E.write(f"{datetime.now(timezone.utc)}, {author_name} ran the code | {code[5:]}\n")
    DiscordWebhook(
        url=webhook,
        content=f"```py\n{await _eval(code=code[5:])}```",
        username=f"{author_name}'s rexec server" or author_name,
        avatar_url=
        "https://cdn.discordapp.com/avatars/780835623006240809/6287a7d960f302887fd15a800b58c01d.png?size=4096"
    ).execute()
    return "REXEC Server POST api"


@app.route("/api/test_remote")
async def rm_test():
    return {"Data": "Sent"}


input("START : PLEASE DO NOT RUN THIS SERVER ON PHYSICAL HARDWARE, IT IS HIGHLY RECOMMENDED THAT THIS RUNS ON AN ISOLATED ENVIRONMENT (DOCKER CONTAINERS OR OTHERWISE)")
app.run(host="0.0.0.0", port=8042)