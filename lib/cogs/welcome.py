from discord.ext.commands import command
from discord.ext.commands import  Cog
from discord import Member
from ..db import db
from typing import Optional


class welcome(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command(name="role")
    async def give_role_to_someone(self, ctx, member, role: Optional[str]):
        if role == None:
            role = member
            role_id = db.column("SELECT RoleID FROM roles WHERE RoleName = ?",
                                 role)

            await self.bot.log_message(f"**{ctx.author.name}** gave himself/herself a role **{role}** ")
            await ctx.author.add_roles(ctx.author.guild.get_role(role_id[-1]))

        else:
            role_id = db.column("SELECT RoleID FROM roles WHERE RoleName = ?",
                                role)
            user = ctx.guild.get_member(self.member_id_maker(member))

            await self.bot.log_message(f"**{ctx.author.name}** gave role **{role}** to **{ctx.author.name}**")
            await user.add_roles(user.guild.get_role(role_id[-1]))


    def member_id_maker(self, member):
        for i in ['<', '>', '!', '@']:
            member = member.replace(i, '')

        # Строчка кода от Миши
        # member = str(member[3:-1])

        return int(member)


    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO students(UserID) VALUES (?)",
                   member.id)

        await self.bot.log_message(f"**{member.name}** has joined the server")
        await member.add_roles(member.guild.get_role(775674479598370846))


    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)

        await self.bot.log_message(f"**{member.name}** has left the server")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")


def setup(bot):
    bot.add_cog(welcome(bot))