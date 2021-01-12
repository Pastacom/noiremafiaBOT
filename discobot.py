# -*- coding: utf8 -*-!
import discord
from discord.ext import commands
import asyncio
import random
import time as tm
from DB import endgame, save_set, load_set, get_settings, change_settings


client = commands.Bot(command_prefix="!")
client.remove_command("help")

roles_num_b = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
tumb = 0
mafia_vote = []
voted = []
gamers = {}
votes = []
already = []
guilty = {}
checker = 0
vn = -1
killed = []
vote_choice = ''
right = None
roles_num = {}
player_roles = {}
player_status = {}
roles_multiplier = [1.4, 1.5, 1.75, 1.75, 1.6, 2, 1.4, 1, 1.8, 1.2, 1.6, 1.5]
sequence = [10, 7, [2, 9, 12], 3, [4, 11], 6, 5]
right_to_chat = []
right_to_act = []
sequence_guild_message = ['Вора 🔐', 'Куртизанки 💋', 'Мафии 🕵️', 'Дона мафии 🥃', 'Комиссара 🚔', 'Маньяка 🔪', 'Доктора 💉']
mafia = []
police = []
roles_definition = {1: 'Мирный житель', 2: 'Мафия', 3: 'Дон', 4: 'Комиссар', 5: 'Доктор', 6: 'Маньяк', 7: 'Куртизанка', 8: 'Бессмертный', 9: 'Двуликий', 10: 'Вор', 11: 'Сержант', 12: 'Оборотень'}
roles_description = {'1': ['Ваша роль - Мирный житель.', 'Ваша задача состоит в том, чтобы вычислить представителей мафии и посадить в тюрьму. Сделать это вы можете только на дневном голосовании.', 'https://w-dog.pw/android-wallpapers/4/15/455401079884056/colton-haynes-guy-men-black-machine-black-and-white.jpg'],
                     '2': ['Ваша роль - Мафия.', 'Вы играете за черных. Ваша задача - избавиться от всех красных игроков в городе. Ночью вы просыпаетесь вместе с другими представителями мафии. Мафия убивает одного игрока за ночь, выбранного общим решением. Если возникают разногласия, то финальное решение принимается Доном мафии. При смерти Дона, убивается цель, за которую проголосовало большее кол-во игроков.', 'https://media.discordapp.net/attachments/713363794138628176/713742967390601277/8011f830f532082c.jpg?width=782&height=519'],
                     '3': ['Ваша роль - Дон мафии.', 'Вы играете за черных. Ваша задача - избавиться от всех красных игроков в городе и обнаружить комиссара, как можно скорее. Ночью вы просыпаетесь дважды, сначала вместе с другими представителями мафии, затем отдельно. Мафия убивает одного игрока за ночь, выбранного общим решением. Если возникают разногласия, то финальное решение принимается вами. Когда вы проснетесь второй раз вы можете указать на любого игрока, если этот игрок - комиссар, то ведущий даст соответсвующий знак.', 'https://media.discordapp.net/attachments/713363794138628176/713742944728907786/f1c3da335e7e8b0f.jpg?width=519&height=519'],
                     '4': ['Ваша роль - Комиссар.', 'Вы играете за красных. Ваша задача - искать мафиози ночью. Когда вы просыпаетесь, вы можете выбрать любого игрока, если это черный игрок, ведущий даст соответсвующий ответ. При проверке маньяка, ведущий скажет, что он играет за мирных. Результаты проверки известны только вам, но вы всегда можете огласить их днем для всех остальных. Просыпается вместе с сержантом, если таковой есть.', 'https://media.discordapp.net/attachments/713363794138628176/713742946112897034/357cb0fc4c2d221d.jpg?width=514&height=519'],
                     '5': ['Ваша роль - Доктор.', 'Вы играете за красных. Ваша задача - спасать от покушения игроков. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока(включая себя), если его пытались убить этой ночью, то он выживает, благодаря вам. Нельзя лечить одного и того же игрока две ночи подряд.', 'https://media.discordapp.net/attachments/713363794138628176/713742942719836250/e5b40f920b837dfb.jpg?width=519&height=519'],
                     '6': ['Ваша роль - Маньяк.', 'Вы играете сами за себя. Ваша задача - остаться одному в игре. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока, которого хотите убить. Если вас проверит комиссар, то он получит результат, что вы мирный.', 'https://media.discordapp.net/attachments/713363794138628176/713742948600119296/14b400af131ac30e.jpg?width=519&height=519'],
                     '7': ['Ваша роль - Куртизанка.', 'Вы играете за красных. Ваша задача - спасать красных. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока. Выбранный игрок не может быть убит в эту ночь, но при этом теряет возможность использовать свою способность в эту ночь, если она у него есть. Нельзя выбирать одного и того же игрока две ночи подряд. Погибает, если выбирает ночным клиентом Маньяка. Если мафиози остается один и вы выбираете его, то мафиози не убивают этой ночью.', 'https://media.discordapp.net/attachments/713363794138628176/713742947987882094/e70bf7c63c141dda.jpg?width=830&height=519'],
                     '8': ['Ваша роль - Бессмертный.', 'Вы играете за красных. Ваша задача - принимать удар черных на себя. Ночью вас не могут убить. Единстевнный способ выйти из игры - это дневное голосование, на котором решат посадить вас.', 'https://media.discordapp.net/attachments/713363794138628176/713743623614758942/5f9244fb10cf04ea280eb6b192b9df7a--baron-samedi-skull-art.png?width=357&height=519'],
                     '9': ['Ваша роль - Двуликий.', 'Вы играете за черных. Ваша задача - найти мафию, как можно скорее. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока. Если этот игрок - мафия, то вы получите право просыпаться вместе с мафией ночью и самостоятельно убивать одну цель независимо от мафии. Если всех мафиози посадят или убьют, до того как вы их найдете, то вы проиграете.', 'https://media.discordapp.net/attachments/713363794138628176/713742942061461504/f5012122151c499d.jpg?width=872&height=472'],
                     '10': ['Ваша роль - Вор.', 'Вы играете за черных. Ваша задача - лишать хода важных игроков красной команды. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока. Выбранный игрок теряет возможность использовать свою способность в эту ночь, если она у него есть.', 'https://reporter64.ru/uploads/content/ala_15808010345e391c0ad5f1b.jpg'],
                     '11': ['Ваша роль - Сержант.', 'Вы играете за красных. Ваша задача - помогать комиссару в поиске мафии. Вы просыпаетесь вместе с комиссаром и знаете статусы проверенных им игроков. Вы проверять не можете, но если Комиссара убьют, то вы становитесь Комиссаром.', 'https://media.discordapp.net/attachments/713714731038539796/713747667217285160/97944_original.png?width=780&height=519'],
                     '12': ['Ваша роль - Оборотень.', 'Вы играете за черных. Ваша задача - избавиться от всех красных игроков в городе. Пока жива мафия, у вас нет никаких способностей, вы просто просыпаетесь вместе с мафией, но в голосовании не участвуете. Проверки комиссара покажут, что вы мирный житель. Когда все мафиози выйдут из игры, то вы сможите просыпаться ночью и убивать игроков.', 'https://media.discordapp.net/attachments/713363794138628176/713748605139419136/scary_werewolf_head_grinning.png?width=722&height=519']
                     }


#------------------Bot is online-------------------


@client.event
async def on_ready():
    print("Bot is online.")
    await client.change_presence(status=discord.Status.online)

#-----------------Utility commands------------------


@client.command()
async def unmute(ctx):
    await ctx.author.edit(mute=False)

@client.command()
async def test(ctx):
    None
#-------------------Main body-----------------------


#---------------Additional functions----------------


@client.command()
async def action(ctx, choice):
    global right_to_act, killed, mafia_vote, don_phase
    if ctx.author in right_to_act and ctx.guild == None:
        if player_status[ctx.author][5] == 1:
            await ctx.send('Вы уже сходили')
            return
        try:
            choice = int(choice)
        except:
            return
        if choice > len(members) or choice - 1 < 0:
            await ctx.send('Игрока под номером ' + str(choice) + ' не существует, проголосуйте за другого.')
            return
        elif player_status[members[choice - 1]][0] == 0:
            await ctx.send('Этот игрок уже убит. Выберите другого.')
            return
        else:
            choice-=1
            player_status[ctx.author][5] = 1
            if player_roles[ctx.author] == '10':
                if player_status[ctx.author][4] != choice:
                    player_status[ctx.author][4] = choice
                    player_status[members[choice]][1] = 1
                else:
                    await ctx.send('Нельзя лишать одного и того же игрока хода два раза подряд')
                    return
            elif player_roles[ctx.author] == '7':
                if player_status[ctx.author][4] != choice:
                    if player_roles[members[choice]] != '6':
                        player_status[ctx.author][4] = choice
                        player_status[members[choice]][1] = 2
                    else:
                        killed.append(str(members.index(ctx.author)+1))
                        player_status[members[choice]][1] = 2
                else:
                    await ctx.send('Нельзя лишать одного и того же игрока хода два раза подряд')
                    return
            elif player_roles[ctx.author] == '4' or (player_roles[ctx.author] == '11' and player_status[ctx.author][2] == 3):
                for member in police:
                    if int(player_roles[members[choice]]) in [1, 4, 5, 6, 7, 8, 11, 12]:
                        await member.send('Игрок под номером ' + str(choice+1) + ' играет за команду мирных')
                    else:
                        await member.send('Игрок под номером ' + str(choice+1) + ' играет за команду мафии')
            elif player_roles[ctx.author] == '5':
                if player_status[ctx.author][4] != choice:
                    player_status[ctx.author][4] = choice
                    if str(choice+1) in killed:
                        player_status[members[choice]][0] = 1
                        del killed[killed.index(str(choice+1))]
                else:
                    await ctx.send('Нельзя лечить одного и того игрока два раза подряд')
                    return
            elif player_roles[ctx.author] == '6':
                if player_roles[members[choice]] != '8' and player_status[members[choice]][1] != 2:
                    killed.append(str(choice+1))
            elif player_roles[ctx.author] == '12' and player_status[ctx.author][3] == 6:
                if player_roles[members[choice]] != '8' and player_status[members[choice]][1] != 2:
                    killed.append(str(choice + 1))
            elif player_roles[ctx.author] == '9' and player_status[ctx.author][3] == 6:
                if player_roles[members[choice]] != '8' and player_status[members[choice]][1] != 2:
                    killed.append(str(choice + 1))
            elif player_roles[ctx.author] == '9' and player_status[ctx.author][3] == 1:
                if members[choice] != ctx.author:
                    player_status[ctx.author][4] = choice
                else:
                    await ctx.send('Вам необходимо найти членов мафии. Нельзя выбирать целью себя самого')
                    return
            elif player_roles[ctx.author] == '2':
                mafia_vote.append(str(choice+1))
            elif player_roles[ctx.author] == '3' and don_phase == 1:
                if player_roles[members[choice]] != '8' and player_status[members[choice]][1] != 2:
                    killed.append(str(choice+1))
                don_phase = 2
            elif player_roles[ctx.author] == '3' and don_phase == 2:
                if player_roles[members[choice]] == '4' or player_roles[members[choice]] == '11':
                    await ctx.send('Этот игрок - комиссар или сержант')
                else:
                    await ctx.send('Этот игрок не комиссар и не сержант')
            else:
                await ctx.send('Вы не ходите ночью')
                return
            await ctx.send('Выбор сделан')


async def status_maker(i):
    player_status[i][0], player_status[i][4] = 1, -1
    if player_roles[i] == '4':
        player_status[i][2] = 3
        police.append(i)
    elif player_roles[i] == '11':
        player_status[i][2] = 2
        police.append(i)
    else:
        player_status[i][2] = 0
    if player_roles[i] == '2':
        player_status[i][3] = 4
        mafia.append(i)
    elif player_roles[i] == '3':
        player_status[i][3] = 5
        mafia.append(i)
    elif player_roles[i] == '12':
        player_status[i][3] = 3
        mafia.append(i)
    elif player_roles[i] == '9':
        player_status[i][3] = 1
        mafia.append(i)
    else:
        player_status[i][3] = 0


async def night_echo(mess):
    if player_status[mess.author][2] > 1 and player_status[mess.author][1] == 0:
        for member in police:
            if member != mess.author and player_status[member][2] > 0 and player_status[member][1] == 0:
                await member.send(str(mess.author)[:-5] + ': ' + mess.content)
    elif player_status[mess.author][3] > 2 and player_status[mess.author][1] == 0:
        for member in mafia:
            if member != mess.author and player_status[member][3] > 1 and player_status[member][1] == 0:
                await member.send(str(mess.author)[:-5] + ': ' + mess.content)


async def after_game(mess):
    sd = ''
    ft = ''
    i = 0
    for member in player_roles:
        i += 1
        x = str(roles_definition[int(player_roles[member])])
        ft += str(i) + ') ' + str(member)[:-5] + '\n'
        sd += str(i) + ') ' + x + '\n'
    emb = discord.Embed(title='Роли игроков:', colour=discord.Color.darker_grey())
    emb.add_field(name='Игрок', value=ft, inline=True)
    emb.add_field(name='Роль', value=sd, inline=True)
    await mess.channel.send(embed=emb)


async def preparation_of_results(mode):
    roles_definition[1] = 'Мирный_житель'
    for member in player_status:
        if mode == 1:
            if player_roles[member] == '6':
                gamers[str(member.id)] = [1, roles_multiplier[int(player_roles[member])-1], player_status[member][0], roles_definition[int(player_roles[member])]]
            else:
                gamers[str(member.id)] = [0, roles_multiplier[int(player_roles[member]) - 1], player_status[member][0], roles_definition[int(player_roles[member])]]
        elif mode == 2:
            if int(player_roles[member]) in [2, 3, 9, 10, 12]:
                gamers[str(member.id)] = [1, roles_multiplier[int(player_roles[member])-1], player_status[member][0], roles_definition[int(player_roles[member])]]
            else:
                gamers[str(member.id)] = [0, roles_multiplier[int(player_roles[member]) - 1], player_status[member][0], roles_definition[int(player_roles[member])]]
        elif mode == 3:
            if int(player_roles[member]) in [1, 4, 5, 7, 8, 11]:
                gamers[str(member.id)] = [1, roles_multiplier[int(player_roles[member]) - 1], player_status[member][0], roles_definition[int(player_roles[member])]]
            else:
                gamers[str(member.id)] = [0, roles_multiplier[int(player_roles[member]) - 1], player_status[member][0], roles_definition[int(player_roles[member])]]
        else:
            gamers[str(member.id)] = [0, roles_multiplier[int(player_roles[member]) - 1], player_status[member][0], roles_definition[int(player_roles[member])]]
    endgame(gamers)
    roles_definition[1] = 'Мирный житель'



async def win_condition(message):
    global red, black, two_faced, maniac
    if maniac > 0 and red + black + two_faced == 0:
        await message.channel.send('Игра окончена! Победа маньяка 🔪')
        await preparation_of_results(1)
        await after_game(message)
        return True
    elif maniac == 0 and ((black >= red and black > 0) or (red + black == 0 and two_faced > 0)):
        await message.channel.send('Игра окончена! Победа мафии 🕵️')
        await preparation_of_results(2)
        await after_game(message)
        return True
    elif maniac == 0 and black == 0 and red > 0:
        await message.channel.send('Игра окончена! Победа мирного города 👥')
        await preparation_of_results(3)
        await after_game(message)
        return True
    elif maniac + black + two_faced + red == 0:
        await message.channel.send('Игра окончена! Ничья. В городе не осталось живых ☠')
        await preparation_of_results(4)
        await after_game(message)
        return True


async def reduction_role_condition(i):
    global red, black, two_faced, maniac
    if int(player_roles[members[i]]) in [2, 3, 10, 12]:
        black -= 1
    elif int(player_roles[members[i]]) == 6:
        maniac -= 1
    elif int(player_roles[members[i]]) == 9:
        two_faced -= 1
    else:
        red -= 1
    player_status[members[i]][0] = 0

async def add_role(num, ctx):
    def check(m):
        return m.author.id == ctx.author.id
    response = await ctx.bot.wait_for('message', check=check)
    try:
        request = response.content
        if int(request[:request.find(' ')]) not in [1, 2]:
            if roles_num[request[:request.find(' ')]]+int(request[request.find(' ')+1:]) > 1:
                await ctx.send('Такой персонаж может быть только один')
                await add_role(num, ctx)
            else:
                roles_num[request[:request.find(' ')]]+=int(request[request.find(' ')+1:])
                if num - int(request[request.find(' ') + 1:]) > 0:
                    await add_role(num - int(request[request.find(' ') + 1:]), ctx)
        else:
            if int(request[request.find(' ')+1:]) <= num:
                roles_num[request[:request.find(' ')]]+=int(request[request.find(' ')+1:])
                if num - int(request[request.find(' ') + 1:]) > 0:
                    await add_role(num - int(request[request.find(' ') + 1:]), ctx)
            else:
                await ctx.send('Количество ролей превышает количество игроков. Попробуйте снова.')
                await add_role(num, ctx)
    except:
        await add_role(num, ctx)

async def timer(time,mess,member,vt):
    if vt == 0:
        await mess.channel.send('Ваш ход ' + str(member)[:-5])
        global time_message
        time_message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
        await time_message.add_reaction('⛔')
        for i in range(time - 1, -1, -1):
            if checker == 1:
                break
            time_break = tm.time()
            while True:
                if checker == 1:
                    break
                elif tm.time() - time_break > 1.0:
                    time_break = tm.time()
                    try:
                        await time_message.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
                        break
                    except:
                        pass
        try:
            await time_message.delete()
        except:
            pass
    elif vt == 1 or vt == 2:
        if vt == 1:
            await mess.channel.send('Кто голосует за игрока  ' + str(member)[:-5]+'?')
            time_message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
            await time_message.add_reaction('✅')
        elif vt == 2:
            time_message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
            await time_message.add_reaction('✅')
            await time_message.add_reaction('⛔')
        for i in range(time - 1, -1, -1):
            time_break = tm.time()
            while True:
                if tm.time() - time_break > 1.0:
                    time_break = tm.time()
                    try:
                        await time_message.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
                        break
                    except:
                        pass
        try:
            await time_message.delete()
        except:
            pass
    elif vt == 3:
        time_message_1 = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
        mafia_time = []
        for i in member:
            if player_status[i][0] != 0:
                time_message_2 = await i.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
                mafia_time.append(time_message_2)
        for i in range(time - 1, -1, -1):
            time_break = tm.time()
            while True:
                if tm.time() - time_break > 1.0:
                    time_break = tm.time()
                    try:
                        await time_message_1.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
                        for j in mafia_time:
                                await j.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
                        break
                    except:
                        pass
        try:
            await time_message_1.delete()
        except:
            pass
        for i in mafia_time:
            try:
                await i.delete()
            except:
                pass


@client.event
async def on_reaction_add(reaction, user):
    global count, checker, nm, gl, setgs, right_to_change
    if reaction.emoji == '⛔' and user == right and vn == 0:
        checker = 1
    elif reaction.emoji == '⛔' and user!=reaction.message.author and vn == 3 and user in members:
        if already[members.index(user)] == 0 and player_status[user][0] != 0:
            count -= 1
            already[members.index(user)] = 1
    elif reaction.emoji == '✅' and user!=reaction.message.author and vn == 1 and user in members:
        if already[members.index(user)] == 0 and player_status[user][0] != 0:
            votes[members.index(gl)] += 1
            already[members.index(user)] = 1
    elif reaction.emoji == '✅' and user != reaction.message.author and vn == 2 and user in members:
        if already[members.index(user)] == 0 and player_status[user][0] != 0:
            already[members.index(user)] = 1
            guilty[ind] += 1
    elif reaction.emoji == '✅' and user != reaction.message.author and vn == 3 and user in members:
        if already[members.index(user)] == 0 and player_status[user][0] != 0:
            already[members.index(user)] = 1
            count += 1
    elif reaction.emoji == '💤' and user != reaction.message.author and user in members:
        if already[members.index(user)] == 0 and player_status[user][0] != 0:
            already[members.index(user)] = 1
            nm-=1
            if nm == 0:
                await reaction.message.delete()
                await reaction.message.channel.send('Наступает ночь 🌃')
    elif reaction.emoji == '⏰' and user != reaction.message.author and user in members:
        if already[members.index(user)] == 0 and player_status[user][0] != 0:
            already[members.index(user)] = 1
            nm-=1
            if nm == 0:
                await reaction.message.delete()
                await reaction.message.channel.send('Наступает день 🌇')
    elif user != reaction.message.author and vn == 4 and right_to_change == user:
        if reaction.emoji == '🤵':
            setgs['mode'] = 'non-auto'
            await messages[0].edit(content=messages[0].content[:messages[0].content.find(':') + 2] + str(setgs['mode']))
            await reaction.message.remove_reaction('🤖', user)
        elif reaction.emoji == '🤖':
            setgs['mode'] = 'auto'
            await messages[0].edit(content=messages[0].content[:messages[0].content.find(':') + 2] + str(setgs['mode']))
            await reaction.message.remove_reaction('🤵', user)
        elif reaction.emoji == '🔊':
            setgs['mute'] = 'off'
            await messages[1].edit(content=messages[1].content[:messages[1].content.find(':') + 2] + str(setgs['mute']))
            await reaction.message.remove_reaction('🔇', user)
        elif reaction.emoji == '🔇':
            setgs['mute'] = 'on'
            await messages[1].edit(content=messages[1].content[:messages[1].content.find(':') + 2] + str(setgs['mute']))
            await reaction.message.remove_reaction('🔊', user)
        elif reaction.emoji == '✅':
            change_settings(user.id, setgs)
            await reaction.message.channel.send('Сохранено')
            for message in messages:
                await message.delete()
        elif reaction.emoji == '❌':
            for message in messages:
                await message.delete()
        elif reaction.emoji == '🔄':
            setgs = {'mode': 'auto', 'mute': 'on', 'time': [60, 45, 15, 60, 40, 90]}
            await reaction.message.remove_reaction('🔄', user)
            await messages[0].edit(content=messages[0].content[:messages[0].content.find(':')+2] + str(setgs['mode']))
            await messages[1].edit(content=messages[1].content[:messages[1].content.find(':') + 2] + str(setgs['mute']))
            for i in range(2, 8):
                await messages[i].edit(content=messages[i].content[:messages[i].content.find(':') + 2] + str(setgs['time'][i-2]) + ' сек')
        else:
            d = reaction.message.id
            for i in range(len(messages)):
                if messages[i].id == d:
                    if reaction.emoji == '⏩':
                        setgs['time'][i-2] += 15
                        await reaction.message.remove_reaction('⏩', user)
                    elif reaction.emoji == '➡️':
                        setgs['time'][i - 2] += 5
                        await reaction.message.remove_reaction('➡️', user)
                    elif reaction.emoji == '⬅️':
                        setgs['time'][i - 2] -= 5
                        await reaction.message.remove_reaction('⬅️', user)
                    elif reaction.emoji == '⏪':
                        setgs['time'][i - 2] -= 15
                        await reaction.message.remove_reaction('⏪', user)
                    break
            await reaction.message.edit(content=reaction.message.content[:reaction.message.content.find(':')+2] + str(setgs['time'][i-2]) + ' сек')


# SHORTCUTS
@client.command()
async def v(ctx, choice):
    await vote(ctx, choice)


@client.command()
async def a(ctx, choice):
    await action(ctx, choice)


@client.command()
async def s(ctx, name=None):
    await start(ctx, name)


@client.command()
async def c(ctx):
    await create(ctx)


@client.command()
async def p(ctx):
    await pool(ctx)

# SHORTCUTS

@client.command()
async def vote(ctx, choice):
    try:
        if ctx.author.id == right_to_vote.id and type(ctx.channel) != discord.channel.DMChannel:
            global vote_choice
            try:
                choice = int(choice)
            except:
                return
            global tumb
            if choice > len(members) or choice - 1 < 0:
                await ctx.send('Игрока под номером ' + str(choice) + ' не существует, проголосуйте за другого.')
            elif choice-1 in voted and sum(votes) == 0:
                await ctx.send('Этот игрок уже выставлен на голосование. Выберите другого.')
            elif player_status[members[choice-1]][0] == 0:
                await ctx.send('Этот игрок уже убит. Выберите другого.')
            else:
                vote_choice = choice
                await ctx.send('Принято!')
    except:
        pass

#-----------------Main commands---------------------

async def meeting_day(mess):
    await mess.channel.send('Начинается день знакомств 🤝')
    global already, time, tumb, right, checker, vn, nm
    already = [0 for i in range(len(members))]
    vn = 0
    tumb = 0
    for member in members:
        right = member
        checker = 0
        await timer(game_settings['time'][0], mess, member, 0)
    already = [0 for i in range(len(members))]
    ms = await mess.channel.send('Город засыпает 💤')
    await ms.add_reaction('💤')
    nm = 0
    for i in list(player_status.values()):
        if i[0] != 0:
            nm += 1


async def day(mess):
    global already, time, tumb, right, checker, vn, black, red, maniac, two_faced, voted, votes, nm, right_to_vote, guilty
    await mess.channel.send('Ночью были убиты игроки под номерами: ' + (', ').join(killed))
    vn = 0
    for person in killed:
        await reduction_role_condition(int(person)-1)
        try:
            await members[int(person)-1].edit(nick=str(person) + '. ' + str(members[int(person)-1])[:-5] + ' ☠')
        except:
            pass
    if await win_condition(mess) == True:
        for member in members:
            try:
                await member.edit(nick=member.name)
            except:
                pass
        return
    await mess.channel.send('Начинается обсуждение и выставление кандидатур на голосование 🗣️')
    voted = []
    votes = [0 for i in range(len(members))]  # колличественные голоса за игроков
    already = [0 for i in range(len(members))]
    guilty.clear()
    killed.clear()
    global vote_choice
    for i in list(player_roles.keys()):
        if player_status[i][0] != 0:
            checker = 0
            vote_choice = ''
            member = i
            right = member
            right_to_vote = member
            await timer(game_settings['time'][0], mess, member, 0)
            if vote_choice == '':
                pass
            elif vote_choice - 1 not in voted:
                voted.append(vote_choice - 1)
    right_to_vote = None
    if len(voted) == 0:
        await mess.channel.send('Было принято решение никого не сажать в тюрьму 🚫')
        already = [0 for i in range(len(members))]
        ms = await mess.channel.send('Город засыпает 💤')
        await ms.add_reaction('💤')
        nm = 0
        for i in list(player_status.values()):
            if i[0] != 0:
                nm += 1
    else:
        m = []
        for i in range(len(voted)):
            m.append(str(voted[i] + 1))
        await mess.channel.send('Обвиняются игроки под номерами: ' + (', ').join(m))
        await mess.channel.send('Обвиняемым предоставляется оправдательная речь 👨‍⚖️')
        for i in voted:
            checker = 0
            member = members[i]
            right = member
            await timer(game_settings['time'][1], mess, member, 0)
        await mess.channel.send('Начинается голосование 📢')
        tumb = 1
        right = None
        vn = 1
        for i in voted:
            member = members[i]
            global gl
            gl = member
            await timer(game_settings['time'][2], mess, member, 1)
        for i in list(player_roles.keys()):
            if player_status[i][0] != 0 and already[members.index(i)] == 0:
                votes[voted[-1]] += 1
        await mess.channel.send('Голосование окончено')
        if votes.count(max(votes)) == 1:
            guil = votes.index(max(votes))
            vn = 0
            right = members[guil]
            checker = 0
            await mess.channel.send('Приговоренному дается право произнести последнюю речь 👨‍⚖️')
            await timer(game_settings['time'][4], mess, members[guil], 0)
            await reduction_role_condition(guil)
            try:
                await members[guil].edit(nick=str(guil + 1) + '. ' + str(members[guil])[:-5] + ' ☠')
            except:
                pass
            await mess.channel.send(str(members[guil])[:-5] + ' был посажен за решетку 👮')
            if await win_condition(mess) == True:
                for member in members:
                    try:
                        await member.edit(nick=member.name)
                    except:
                        pass
                return
        else:
            for i in range(len(voted)):
                if votes[voted[i]] == max(votes):
                    guilty[voted[i] + 1] = 0
            await mess.channel.send(
                'Обвиняемым ' + str(guilty.keys())[11:-2] + ' предоставляются дополнительные оправдательные речи 👨‍⚖️')
            guilty.clear()
            right = None
            vn = 0
            for i in range(len(voted)):
                if votes[voted[i]] == max(votes):
                    checker = 0
                    guilty[voted[i]] = 0
                    member = members[voted[i]]
                    right = member
                    await timer(game_settings['time'][0], mess, member, 0)
            await mess.channel.send('Начинается повторное голосование 📢')
            right = None
            already = [0 for i in range(len(members))]
            for i in range(len(guilty)):
                vn = 2
                member = members[list(guilty.keys())[i]]
                global ind
                ind = list(guilty.keys())[i]
                await timer(game_settings['time'][2], mess, member, 1)
            for i in list(player_roles.keys()):
                if player_status[i][0] != 0 and already[members.index(i)] == 0:
                    guilty[list(guilty.keys())[-1]] += 1
            if list(guilty.values()).count(max(guilty.values())) == 1:
                vn = 0
                for i in list(guilty.keys()):
                    if guilty[i] == max(guilty.values()):
                        checker = 0
                        right = members[list(guilty.keys())[i]]
                        await mess.channel.send('Приговоренному дается право произнести последнюю речь 👨‍⚖️')
                        await timer(game_settings['time'][3], mess, members[list(guilty.keys())[i]], 0)

                        try:
                            await members[i].edit(nick=str(i + 1) + '. ' + str(members[i])[:-5] + ' ☠')
                        except:
                            pass
                            await mess.channel.send(str(members[i])[:-5] + ' был посажен за решетку 👮')
                        break
                if await win_condition(mess) == True:
                    for member in members:
                        try:
                            await member.edit(nick=member.name)
                        except:
                            pass
                    return
            else:
                for i in list(guilty.keys()):
                    if guilty[i] != max(guilty.values()):
                        del guilty[i]
                await mess.channel.send(
                    'По-прежнему остались игроки с одинаковым количеством голосов, поэтому принимается решение: выгнать или оставить всех\n✅ - выгнать, ⛔ - оставить')
                global count
                count = 0
                vn = 3
                right = None
                already = [0 for i in range(len(members))]
                checker = 0
                await timer(game_settings['time'][2], mess, member, 2)
                for i in list(player_roles.keys()):
                    if player_status[i][0] != 0 and already[members.index(i)] == 0:
                        count -= 1
                if count > 0:
                    await mess.channel.send('Приговоренным дается право произнести последнюю речь 👨‍⚖️')
                    vn = 0
                    for i in list(guilty.keys()):
                        checker = 0
                        right = members[list(guilty.keys())[i]]
                        await timer(game_settings['time'][2], mess, members[list(guilty.keys())[i]], 0)
                        await reduction_role_condition(i)
                        try:
                            await members[i].edit(nick=str(i + 1) + '. ' + str(members[i])[:-5] + ' ☠')
                        except:
                            pass
                        await mess.channel.send(str(members[i])[:-5] + ' был посажен за решетку 👮')
                    if await win_condition(mess) == True:
                        for member in members:
                            try:
                                await member.edit(nick=member.name)
                            except:
                                pass
                        return
                else:
                    await mess.channel.send('Было принято решение никого не сажать в тюрьму 🚫')
        already = [0 for i in range(len(members))]
        ms = await mess.channel.send('Город засыпает 💤')
        await ms.add_reaction('💤')
        nm = 0
        for i in list(player_status.values()):
            if i[0] != 0:
                nm += 1


async def night(mess):
    global vn, nm, already, right_to_act, killed, don_phase, right_to_chat, mafia_vote, two_faced, black
    vn = 4
    for member in player_roles:
        if player_status[member][2] > 1 and player_status[member][0] == 0:
            player_status[member][2] = 1
        elif player_status[member][3] > 2 and player_status[member][0] == 0:
            player_status[member][3] = 2
        player_status[member][1] = 0
        player_status[member][5] = 0
        if player_roles[member] == '9':
            if player_status[member][4] != -1 and members[player_status[member][4]] in mafia:
                player_status[member][3] = 6
                two_faced-=1
                black+=1
        elif player_roles[member] == '11':
            for j in player_roles:
                if player_roles[j] == '4' and player_status[j][0] == 0:
                    player_status[member][2] = 3
        elif player_roles[member] == '12':
            count = 0
            for j in player_roles:
                if int(player_roles[j]) in [2, 3] and player_status[j][0] == 1:
                    count += 1
                    count += 1
            if count == 0:
                player_status[member][3] = 6
            del count
    for i in range(len(sequence)):
        if type(sequence[i]) == int:
            for j in list(player_roles.keys()):
                if int(player_roles[j]) == sequence[i]:
                    if player_status[j][0] != 0 and player_status[j][1] == 0:
                        right_to_act = [j]
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    if i != 3:
                        await timer(game_settings['time'][4], mess, [j], 3)
                    elif i == 3:
                        right_to_chat = mafia.copy()
                        await timer(game_settings['time'][4], mess, [j], 3)
                        if don_phase == 1 and player_status[j][0] != 0 and player_status[j][1] == 0 and vote_results.count(max(vote_results)) == 1 and sum(vote_results) != 0:
                            killed.append(str(vote_results.index(max(vote_results))+1))
                    right_to_act.clear()
                    right_to_chat.clear()
        elif type(sequence[i]) == list and i == 4:
            right_to_chat = police.copy()
            for j in list(player_roles.keys()):
                if int(player_roles[j]) == 4 and player_status[j][0] != 0:
                    if player_status[j][1] == 0:
                        right_to_act = [j]
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    await timer(game_settings['time'][4], mess, [j], 3)
                    right_to_act.clear()
                    break
                elif int(player_roles[j]) == 11 and player_status[j][0] != 0:
                    if player_status[j][1] == 0:
                        right_to_act = [j]
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    await timer(game_settings['time'][4], mess, [j], 3)
                    right_to_act.clear()
                    break
            right_to_chat.clear()
        elif type(sequence[i]) == list and i == 2:
            right_to_chat = mafia.copy()
            right_to_act = []
            mafia_vote = []
            for j in list(player_roles.keys()):
                if int(player_roles[j]) == 9 and player_status[j][0] != 0:
                    if player_status[j][1] == 0:
                        right_to_act.append(j)
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                elif int(player_roles[j]) == 12 and player_status[j][0] != 0:
                    count=0
                    for member in list(player_roles.keys()):
                        if int(player_roles[member]) in [2, 3] and player_status[member][0] != 0:
                            count+=1
                    if player_status[j][1] == 0 and count == 0:
                        del count
                        right_to_act.append(j)
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                elif int(player_roles[j]) == 2 and player_status[j][0] != 0:
                    if player_status[j][1] == 0:
                        right_to_act.append(j)
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
            await mess.channel.send('Ход ' + sequence_guild_message[i])
            await timer(game_settings['time'][5], mess, right_to_act, 3)
            right_to_act.clear()
            vote_results = []
            for j in range(1, len(members)+1):
                vote_results.append(mafia_vote.count(str(j)))
            for j in list(player_roles.keys()):
                if player_roles[j] == '3' and player_status[j][0] != 0 and player_status[j][1] == 0:
                    right_to_act = [j]
                    if sum(vote_results) != 0:
                        for l in range(len(vote_results)):
                            if vote_results[l] != 0:
                                await j.send(str(vote_results[l]) + ' проголосовал(-о) за убийство ' + str(l+1))
                    else:
                        await j.send('Мафия не выбрала ни одной цели для убийства')
                elif player_roles[j] == '3' and (player_status[j][0] == 0 or player_status[j][1] != 0) or list(player_roles.values()).count('3') == 0:
                    if sum(vote_results) != 0:
                        k = vote_results.index(max(vote_results))
                        if vote_results.count(max(vote_results)) == 1 and player_roles[members[k]] != '8' and player_status[members[k]][1] != 2:
                            killed.append(str(k+1))
            don_phase = 1
        killed = list(set(killed))
        killed.sort()

    for i in killed:
        try:
            player_status[members[int(i)-1]][0] = 0
        except:
            pass
    already = [0 for i in range(len(members))]
    ms = await mess.channel.send('Город просыпается ⏰')
    await ms.add_reaction('⏰')
    right_to_act.clear()
    nm = 0
    for i in list(player_status.values()):
        if i[0] != 0:
            nm += 1
    if nm == 0:
        await ms.delete()
        await mess.channel.send('Наступает день 🌇')


async def genc(ctx):
    global roles_num
    global members
    global roles_num_b
    if type(ctx.channel) != discord.channel.DMChannel:
        roles_num = roles_num_b.copy()
        members = ctx.message.author.voice.channel.members
        amount = len(members)
        #amount = 5
        if amount > 3 and amount < 11:
                roles_num['2'], roles_num['3'], roles_num['4'] = amount//3 - 1, 1, 1
                roles_num['1'] = amount - sum(list(roles_num.values()))
                await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" + "Мирных жителей: " + str(
                roles_num['1']) + "\n" + "Мафий: " + str(roles_num['2']) + "\n" + "Донов мафии: " + str(
                roles_num['3']) + "\n" + "Комиссаров: " + str(roles_num['4']))
        else:
            await ctx.send('Классический режим для доступен при команде от 3 до 10 игроков')


async def gene(ctx):
    global roles_num
    global members
    global roles_num_b
    if type(ctx.channel) != discord.channel.DMChannel:
        roles_num = roles_num_b.copy()
        members = ctx.message.author.voice.channel.members
        amount = len(members)


@client.command()
async def settings(ctx):
    global vn, setgs, messages, right_to_change
    vn = 4
    right_to_change = ctx.author
    setgs = get_settings(ctx.author.id)
    messages = []
    messages.append(await ctx.send('Режим: ' + str(setgs['mode'])))
    await messages[0].add_reaction('🤵')
    await messages[0].add_reaction('🤖')
    messages.append(await ctx.send('Мут: ' + str(setgs['mute'])))
    await messages[1].add_reaction('🔊')
    await messages[1].add_reaction('🔇')
    messages.append(await ctx.send('Дневная речь: ' + str(setgs['time'][0]) + ' сек'))
    messages.append(await ctx.send('Оправдательная речь: ' + str(setgs['time'][1]) + ' сек'))
    messages.append(await ctx.send('Время голосования: ' + str(setgs['time'][2]) + ' сек'))
    messages.append(await ctx.send('Речь приговоренного: ' + str(setgs['time'][3]) + ' сек'))
    messages.append(await ctx.send('Ночное время одиночной роли: ' + str(setgs['time'][4]) + ' сек'))
    messages.append(await ctx.send('Ночное время мафии: ' + str(setgs['time'][5]) + ' сек'))
    for i in range(2, 8):
        await messages[i].add_reaction('⏪')
        await messages[i].add_reaction('⬅️')
        await messages[i].add_reaction('➡️')
        await messages[i].add_reaction('⏩')
    messages.append(await ctx.send('Сохранить?'))
    await messages[-1].add_reaction('✅')
    await messages[-1].add_reaction('❌')
    await messages[-1].add_reaction('🔄')



@client.command()
async def create(ctx):
    global roles_num
    global members
    global roles_num_b
    global game_settings
    game_settings = get_settings(ctx.author.id)
    if game_settings['mode'] == "non-auto" and type(ctx.channel) != discord.channel.DMChannel:
        await ctx.send("Перед началом удостоверьтесь, все ли желающие подключены к Вашему голосовому каналу, в противном случае не все роли смогут выдаться.\nЕсли всё готово, можно приступать к настройке игровой сессии.")
        roles_num = roles_num_b.copy()

        def check(m):
            return m.author.id == ctx.author.id

        members = ctx.message.author.voice.channel.members
        for member in members:
            if member.bot:
                members.remove(member)
        await ctx.send("Выберите ведущего.")
        response = await ctx.bot.wait_for('message', check=check)
        for member in members:
            if member.mentioned_in(response):
                emb = discord.Embed(title="Вас назначили ведущим игры.", colour=discord.Color.darker_grey())
                emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713750207623331880/AATXAJxHckd0XbeQRXnekTtsXFQ0vgyIRvtCrntQeQs900-c-k-c0xffffffff-no-rj-mo.png?width=519&height=519")
                await member.send(embed=emb)
                game_master = member
                members.remove(game_master)
                break
        await ctx.send("Задайте роли.")
        await ctx.send("1. Мирный житель " + "\n" + "2. Мафия " + "\n" + "3. Дон мафии " + "\n" + "4. Комиссар " + "\n" + "5. Доктор " + "\n" + "6. Маньяк " + "\n" + "7. Куртизанка " + "\n" + "8. Бессмертный " + "\n" + "9. Двуликий " + "\n" + "10. Вор " + "\n" + "11. Сержант " + "\n" + "12. Оборотень")
        await add_role(len(members), ctx)
        await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" + "Мирных жителей: " + str(roles_num['1']) + "\n" + "Мафий: " + str(roles_num['2']) + "\n" + "Донов мафии: " + str(roles_num['3']) + "\n" + "Комиссаров: " + str(roles_num['4']) + "\n" + "Докторов: " + str(roles_num['5']) + "\n" + "Маньяков: " + str(roles_num['6']) + "\n" + "Куртизанок: " + str(roles_num['7']) + "\n" + "Бессмертных: " + str(roles_num['8']) + "\n" + "Двуликих: " + str(roles_num['9']) + "\n" + "Воров: " + str(roles_num['10']) + "\n" + "Сержантов: " + str(roles_num['11']) + "\n" + "Оборотней: " + str(roles_num['12']))
    elif game_settings['mode'] == 'auto' and type(ctx.channel) != discord.channel.DMChannel:
        await ctx.send(
            "Перед началом удостоверьтесь, все ли желающие подключены к Вашему голосовому каналу, в противном случае не все роли смогут выдаться.\nЕсли всё готово, можно приступать к настройке игровой сессии.")
        roles_num = roles_num_b.copy()
        members = ctx.message.author.voice.channel.members
        for member in members:
            if member.bot:
                members.remove(member)
        await ctx.send("Задайте роли.")
        await ctx.send(
            "1. Мирный житель " + "\n" + "2. Мафия " + "\n" + "3. Дон мафии " + "\n" + "4. Комиссар " + "\n" + "5. Доктор " + "\n" + "6. Маньяк " + "\n" + "7. Куртизанка " + "\n" + "8. Бессмертный " + "\n" + "9. Двуликий " + "\n" + "10. Вор " + "\n" + "11. Сержант " + "\n" + "12. Оборотень")
        await add_role(len(members), ctx)
        await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" + "Мирных жителей: " + str(
            roles_num['1']) + "\n" + "Мафий: " + str(roles_num['2']) + "\n" + "Донов мафии: " + str(
            roles_num['3']) + "\n" + "Комиссаров: " + str(roles_num['4']) + "\n" + "Докторов: " + str(
            roles_num['5']) + "\n" + "Маньяков: " + str(roles_num['6']) + "\n" + "Куртизанок: " + str(
            roles_num['7']) + "\n" + "Бессмертных: " + str(
            roles_num['8']) + "\n" + "Двуликих: " + str(roles_num['9']) + "\n" + "Воров: " + str(
            roles_num['10']) + "\n" + "Сержантов: " + str(roles_num['11']) + "\n" + "Оборотней: " + str(
            roles_num['12']))


@client.command()
async def pool(ctx):
    if type(ctx.channel) != discord.channel.DMChannel:
        await ctx.send("1. Мирных жителей: " + str(roles_num['1']) + "\n" + "2. Мафий: " + str(roles_num['2']) + "\n" + "3. Донов мафии: " + str(roles_num['3']) + "\n" + "4. Комиссаров: " + str(roles_num['4']) + "\n" + "5. Докторов: " + str(roles_num['5']) + "\n" + "6. Маньяков: " + str(roles_num['6']) + "\n" + "7. Куртизанок: " + str(roles_num['7']) + "\n" + "8. Бессмертных: " + str(roles_num['8']) + "\n" + "9. Двуликих: " + str(roles_num['9']) + "\n" + "10. Воров: " + str(roles_num['10']) + "\n" + "11. Сержантов: " + str(roles_num['11']) + "\n" + "12. Оборотней: " + str(roles_num['12']) + "\n\n" + "Оставшихся мест: " + str(len(members) - int(roles_num['1']) - int(roles_num['2']) - int(roles_num['3']) - int(roles_num['4']) - int(roles_num['5']) - int(roles_num['6']) - int(roles_num['7']) - int(roles_num['8']) - int(roles_num['9']) - int(roles_num['10']) - int(roles_num['11']) - int(roles_num['12'])))


@client.command()
async def save(ctx, name):
    if roles_num != {}:
        await ctx.send('Список сохранен под названием {}'.format(name))
        save_set(ctx.author.id, name, roles_num)
    else:
        await ctx.send('Сохранить список ролей можно только до начала игры')


@client.command()
async def start(ctx, name=None):
    global roles_num
    global members
    global game_settings
    game_settings = get_settings(ctx.author.id)
    if name != None and name != 'cl' and name != 'ex':
        new_set = load_set(ctx.author.id, name)
        members = ctx.message.author.voice.channel.members
        if new_set == {}:
            await ctx.send('Такого списка ролей не существует')
            return
        else:
            roles_num = new_set
            del new_set
    elif name == 'cl':
        await genc(ctx)
    elif name == 'ex':
        await gene(ctx)
    if type(ctx.channel) != discord.channel.DMChannel:
        for role in roles_num.copy():
            if roles_num[role] == 0:
                if role in roles_num:
                    del roles_num[role]
        if roles_num == {}:
            await ctx.send("Вы не задали роли")
            return
        elif sum(list(roles_num.values())) != len(members):
            await ctx.send('Данный список ролей не подходит для текущего количества игроков')
            return
        else:
            roles_num_list = []
            while roles_num != {}:
                for role in roles_num.copy():
                    if role in roles_num:
                        for i in range(0, roles_num[role]):
                            roles_num_list.append(role)
                        del roles_num[role]
            counter = 1
            for member in members:
                counter += 1
                random.seed(random.randint(0, 100))
                index_of_giving_role = random.randint(0, len(roles_num_list) - 1)
                giving_role = roles_num_list[index_of_giving_role]
                roles_num_list.pop(index_of_giving_role)
                global player_roles
                player_roles[member] = giving_role
                emb = discord.Embed(title=roles_description[giving_role][0], colour=discord.Color.darker_grey())
                emb.add_field(name="Описание роли:", value=roles_description[giving_role][1])
                emb.set_image(url=roles_description[giving_role][2])
                await member.send(embed=emb)
        if game_settings['mode'] == 'non-auto':
            pass
        else:
            try:
                for i in range(len(members)):
                    try:
                        await members[i].edit(nick=(str(i+1)+'. '+str(members[i])[:-5]))
                    except:
                        pass
                global black, red, two_faced, maniac, player_status
                black, red, two_faced, maniac = 0, 0, 0, 0
                for i in list(player_roles.values()):
                    if int(i) in [2, 3, 10, 12]:
                        black += 1
                    elif int(i) == 6:
                        maniac += 1
                    elif int(i) == 9:
                        two_faced += 1
                    else:
                        red += 1
                player_status = {members[x]: [0 for i in range(6)] for x in range(len(members))}
                for i in list(player_roles.keys()):
                    await status_maker(i)
                await ctx.send('💠 ИГРА НАЧАЛАСЬ 💠')
            except:
                await ctx.send('Необходимо сначала задать список ролей для игры.')


@client.event
async def on_message(mess):
    if mess.author == client.user and mess.guild != None:
        if mess.content == '💠 ИГРА НАЧАЛАСЬ 💠':
            await meeting_day(mess)
        if mess.content == 'Наступает день 🌇':
            await day(mess)
        if mess.content == 'Наступает ночь 🌃':
            await night(mess)
    elif mess.guild == None and mess.author != client.user:
        global right_to_chat
        if mess.author in members and mess.content[0] != '!' and mess.author in right_to_chat:
            await night_echo(mess)
    await client.process_commands(mess)

#---------------------Token-------------------------

token = 'NzEzMzczNTg4ODYxODc4MzQz.XsfK7Q.IigCNgypVztyU5cOg_Bg2tgOYsI'
client.run(token)
