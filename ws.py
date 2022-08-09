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

app = Quart(__name__)
async def _eval(code):
  local_variables = {
      "discord" : discord,
      "token" : ""
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

@app.route("/api/check")
async def check():
    return "hello there"

@app.route("/api/run", methods=['GET', 'POST'])
async def evaluate():
  author_id = request.headers.get("id")
  webhook = request.headers.get("webhook")
  code = request.headers.get("code")
  webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1005731999237021756/ESwGUt_BguKCDFtKrb3he39_dTi3a9vlWzE_iLXWO9MORVyB-86jModTHa-tw9qKPszA", content=f"```py\n{await _eval(code=code)}```").execute()
  return "hello"
  


@app.route("/api/test_remote")
async def rm_test():
    return {"Data" : "Sent"}

app.run(host="192.168.1.110", port=8042)