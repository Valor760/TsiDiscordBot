from ..db import db
from discord.ext.commands import Bot as BotBase
from  apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown
from discord.errors import HTTPException, Forbidden
from discord import Intents
from asyncio import sleep
from glob import glob


PREFIX = "!"
OWNER_IDS = [309641768310407168]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"> {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.Prefix = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents = Intents.all()
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"- {cog} cog is loaded")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO students (UserID) VALUES (?)",
                     ((member.id,) for member in self.guild.members if not member.bot))

        db.multiexec("INSERT OR IGNORE INTO roles (RoleName) VALUES (?)",
                     ((role.name,) for role in self.guild.roles))

        for role in self.guild.roles:
            db.execute("UPDATE roles SET RoleID = ? WHERE RoleName = ?",
                        role.id, role.name)

        to_remove = []

        stored_members = db.column("SELECT UserID FROM students")
        for id_ in stored_members:
            if not self.guild.get_member(id_):
                to_remove.append(id_)

        db.multiexec("DELETE FROM students WHERE UserID = ?",
                     ((id_,) for id_ in to_remove))
        db.commit()

    def run(self):
        print("RUNNING SETUP....")
        self.setup()

        with open("./lib/bot/token.txt", "r", encoding="utf-8") as f:
            self.TOKEN = f.read()

        print("RUNNING BOT....")
        super().run(self.TOKEN, reconnect=True)


        async def on_connect(self):
            print("Bot connected!")

    async def on_disconnect(self):
        print("Bot disconnected!")

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more arguments are missing")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Command on cooldown! Wait {exc.retry_after:,.2f} seconds!")

        elif hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                await ctx.send("Unable to send message")

            elif isinstance(exc, Forbidden):
                await ctx.send("I don't have permission to do that!")

            else:
                raise exc.original


    async def on_ready(self):
        if not self.ready:

            self.guild = self.get_guild(713016278411116594)
            self.update_db()

            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print(">>Bot Ready<<")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

    async def log_message(self, log_text):
        channel = self.guild.get_channel(779243885779222538)
        await channel.send(log_text)


bot = Bot()