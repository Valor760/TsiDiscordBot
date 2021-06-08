from discord.ext.commands import Cog
from discord.ext.commands import command
from ..db import db
from asyncio import run_coroutine_threadsafe



class creatorOnly(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.user_id = user_id
        # self.st_code = st_code
        # self.st_name = st_name
        # self.guild = self.bot.get_guild(713016278411116594)

    def process_data(self, user_id, st_code, st_name):

        if "st" in st_code.lower():
            st_code = st_code.lower().replace("st", '')

        isThereCode = db.column("SELECT StudentCode FROM studentDB WHERE StudentCode = ?",
                                st_code)

        if isThereCode:
            if st_name == '':
                std_name = db.column("SELECT StudentName FROM studentDB WHERE StudentCode = ?",
                                     st_code)
                student_name = std_name[0]
            else:
                student_name = st_name

            student_group = db.column("SELECT GroupNum FROM studentDB WHERE StudentCode = ?",
                                      st_code)

            db.execute("UPDATE students SET StudentCode = ?, StudentName = ?, GroupNum = ? WHERE UserID = ?",
                       int(st_code), student_name, student_group[0], user_id)
            db.commit()


            # run(self.change_display_name(st_name, user_id))

            ch_d_name = run_coroutine_threadsafe(self.change_display_name(st_name, user_id), client_loop)
            return True

        else:
            return False


    @command(name="wipe")
    async def wipe_server(self, ctx):
        if ctx.author.id == 309641768310407168:
            for member in ctx.guild.members:
                if not member.bot:
                    for role in member.roles:
                        if role.name == "@everyone":
                            continue
                        await member.remove_roles(ctx.guild.get_role(role.id))
                    await member.add_roles(ctx.guild.get_role(775674479598370846))

        else:
            await ctx.send("You don't have permission to do that!")


    @command(name="update")
    async def update_data_base(self, ctx):
        if ctx.author.id == 309641768310407168:
            with open("./data/db/codes.txt", "r") as f:

                db.multiexec("INSERT OR IGNORE INTO studentDB (StudentCode) VALUES (?)",
                             ((st_code.split("|")[1],) for st_code in f))

            with open("./data/db/codes.txt", "r") as f:
                for line in f:
                    ln = line.split("|")

                    group = ln[0]
                    st_code = ln[1]
                    st_name = ln[2]
                    st_name = st_name.replace("\n", '')

                    db.execute("UPDATE studentDB SET StudentName = ?, GroupNum = ? WHERE StudentCode = ?",
                                st_name, group, st_code)
        else:
            await ctx.send("You don't have permission to do that!")


    @command(name="bot")
    async def get_bot_object(self, ctx):
        print(self.bot)




    async def change_display_name(self, st_name, user_id):
        print(self.bot)
        print(user_id)
        guild = self.bot.guild
        print(guild)
        member = guild.get_member(int(user_id))
        print(member)
        new_nickname = member.name + '(' + st_name + ')'
        print(new_nickname)
        await member.edit(nick=new_nickname)


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("creatorOnly")


def setup(bot):
    bot.add_cog(creatorOnly(bot))