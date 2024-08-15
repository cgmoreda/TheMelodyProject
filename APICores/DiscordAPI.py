import discord

from GlobalVariable import ranks


async def assignRole(user_id, ctx, role_name):
    # Fetch the guild (server) object
    guild = ctx.guild
    # Fetch the member by ID
    # 620368287393513493
    member = guild.get_member(int(user_id))
    if member is None:
        await ctx.send(f'User with ID {user_id} not found in this server.')
        return

    for rl in ranks:
        role = discord.utils.get(guild.roles, name=rl)
        if role is not None:
            await member.remove_roles(role)

    role = discord.utils.get(guild.roles, name=role_name)
    # Check if role is found
    if role is None:
        await ctx.send(f'Role `{role_name}` not found.')
        return
    # Check if the bot has permission to manage roles
    if ctx.guild.me.guild_permissions.manage_roles:
        # Check if the role is lower in the hierarchy than the bot's highest role
        if role.position < ctx.guild.me.top_role.position:
            # Assign the role to the member
            await member.add_roles(role)
            await ctx.send(f'Assigned role `{role_name}` to {member.mention}.')
        else:
            await ctx.send('I cannot assign this role because it is higher than my highest role.')
    else:
        await ctx.send('I do not have permission to manage roles.')

