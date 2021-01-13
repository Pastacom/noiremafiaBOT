# -*- coding: utf8 -*-!
import discord
from discord.ext import commands
import asyncio
import random
import time as tm
from DB import endgame, save_set, load_set, get_settings, change_settings


client = commands.Bot(command_prefix="!")
client.remove_command("help")


game_sessions = {}
setting_sessions = {}
roles_num_b = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
roles_multiplier = [1.4, 1.5, 1.75, 1.75, 1.6, 2, 1.4, 1, 1.8, 1.2, 1.6, 1.5]
sequence = [10, 7, [2, 9, 12], 3, [4, 11], 6, 5]
sequence_guild_message = ['Вора 🔐', 'Куртизанки 💋', 'Мафии 🕵️', 'Дона мафии 🥃', 'Комиссара 🚔', 'Маньяка 🔪', 'Доктора 💉']
roles_definition = {1: 'Мирный_житель', 2: 'Мафия', 3: 'Дон', 4: 'Комиссар', 5: 'Доктор', 6: 'Маньяк', 7: 'Куртизанка', 8: 'Бессмертный', 9: 'Двуликий', 10: 'Вор', 11: 'Сержант', 12: 'Оборотень'}
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
#------------------Classes-------------------


class Game:
    def __init__(self, tumb=0, mafia_vote=[], voted=[], gamers={}, votes=[], already=[], guilty={},
                 checker=0, vn=-1, killed=[], vote_choice='', right=None, right_to_vote=None,
                 roles_num={}, player_roles={}, player_status={}, right_to_chat=[], right_to_act=[],
                 mafia=[], police=[], members=[], don_phase=1, guil=None, ind=None,
                 red=0, black=0, two_faced=0, maniac=0, game_settings={}, count=0, gl=None):
        self.tumb = tumb
        self.mafia_vote = mafia_vote
        self.voted = voted
        self.gamers = gamers
        self.votes = votes
        self.already = already
        self.guilty = guilty
        self.checker = checker
        self.vn = vn
        self.killed = killed
        self.vote_choice = vote_choice
        self.right = right
        self.right_to_vote = right_to_vote
        self.roles_num = roles_num
        self.player_roles = player_roles
        self.player_status = player_status
        self.right_to_chat = right_to_chat
        self.right_to_act = right_to_act
        self.mafia = mafia
        self.police = police
        self.members = members
        self.don_phase = don_phase
        self.guil = guil
        self.ind = ind
        self.red = red
        self.black = black
        self.two_faced = two_faced
        self.maniac = maniac
        self.game_settings = game_settings
        self.count = count
        self.gl = gl


class Settings:
    def __init__(self, vn, right_to_change, setgs, messages):
        self.vn = vn
        self.right_to_change = right_to_change
        self.setgs = setgs
        self.messages = messages

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
    print(game_sessions[ctx.channel].player_roles)
#-------------------Main body-----------------------


#---------------Additional functions----------------


@client.command()
async def action(ctx, choice):
    if ctx.author in game_sessions[ctx.channel].right_to_act and ctx.guild == None:
        if game_sessions[ctx.channel].player_status[ctx.author][5] == 1:
            await ctx.send('Вы уже сходили')
            return
        try:
            choice = int(choice)
        except:
            return
        if choice > len(game_sessions[ctx.channel].members) or choice - 1 < 0:
            await ctx.send('Игрока под номером ' + str(choice) + ' не существует, проголосуйте за другого.')
            return
        elif game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice - 1]][0] == 0:
            await ctx.send('Этот игрок уже убит. Выберите другого.')
            return
        else:
            choice -= 1
            game_sessions[ctx.channel].player_status[ctx.author][5] = 1
            if game_sessions[ctx.channel].player_roles[ctx.author] == '10':
                if game_sessions[ctx.channel].player_status[ctx.author][4] != choice:
                    game_sessions[ctx.channel].player_status[ctx.author][4] = choice
                    game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][1] = 1
                else:
                    await ctx.send('Нельзя лишать одного и того же игрока хода два раза подряд')
                    return
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '7':
                if game_sessions[ctx.channel].player_status[ctx.author][4] != choice:
                    if game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]] != '6':
                        game_sessions[ctx.channel].player_status[ctx.author][4] = choice
                        game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][1] = 2
                    else:
                        game_sessions[ctx.channel].killed.append(str(game_sessions[ctx.channel].members.index(ctx.author)+1))
                        game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][1] = 2
                else:
                    await ctx.send('Нельзя лишать одного и того же игрока хода два раза подряд')
                    return
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '4' or (game_sessions[ctx.channel].player_roles[ctx.author] == '11' and game_sessions[ctx.channel].player_status[ctx.author][2] == 3):
                for member in game_sessions[ctx.channel].police:
                    if int(game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]]) in [1, 4, 5, 6, 7, 8, 11, 12]:
                        await member.send('Игрок под номером ' + str(choice+1) + ' играет за команду мирных')
                    else:
                        await member.send('Игрок под номером ' + str(choice+1) + ' играет за команду мафии')
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '5':
                if game_sessions[ctx.channel].player_status[ctx.author][4] != choice:
                    game_sessions[ctx.channel].player_status[ctx.author][4] = choice
                    if str(choice+1) in game_sessions[ctx.channel].killed:
                        game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][0] = 1
                        del game_sessions[ctx.channel].killed[game_sessions[ctx.channel].killed.index(str(choice+1))]
                else:
                    await ctx.send('Нельзя лечить одного и того игрока два раза подряд')
                    return
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '6':
                if game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]] != '8' and game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][1] != 2:
                    game_sessions[ctx.channel].killed.append(str(choice+1))
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '12' and game_sessions[ctx.channel].player_status[ctx.author][3] == 6:
                if game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]] != '8' and game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][1] != 2:
                    game_sessions[ctx.channel].killed.append(str(choice + 1))
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '9' and game_sessions[ctx.channel].player_status[ctx.author][3] == 6:
                if game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]] != '8' and game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][1] != 2:
                    game_sessions[ctx.channel].killed.append(str(choice + 1))
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '9' and game_sessions[ctx.channel].player_status[ctx.author][3] == 1:
                if game_sessions[ctx.channel].members[choice] != ctx.author:
                    game_sessions[ctx.channel].player_status[ctx.author][4] = choice
                else:
                    await ctx.send('Вам необходимо найти членов мафии. Нельзя выбирать целью себя самого')
                    return
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '2':
                game_sessions[ctx.channel].mafia_vote.append(str(choice+1))
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '3' and game_sessions[ctx.channel].don_phase == 1:
                if game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]] != '8' and game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice]][1] != 2:
                    game_sessions[ctx.channel].killed.append(str(choice+1))
                game_sessions[ctx.channel].don_phase = 2
            elif game_sessions[ctx.channel].player_roles[ctx.author] == '3' and game_sessions[ctx.channel].don_phase == 2:
                if game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]] == '4' or game_sessions[ctx.channel].player_roles[game_sessions[ctx.channel].members[choice]] == '11':
                    await ctx.send('Этот игрок - комиссар или сержант')
                else:
                    await ctx.send('Этот игрок не комиссар и не сержант')
            else:
                await ctx.send('Вы не ходите ночью')
                return
            await ctx.send('Выбор сделан')


async def status_maker(i, mess):
    game_sessions[mess.channel].player_status[i][0], game_sessions[mess.channel].player_status[i][4] = 1, -1
    if game_sessions[mess.channel].player_roles[i] == '4':
        game_sessions[mess.channel].player_status[i][2] = 3
        game_sessions[mess.channel].police.append(i)
    elif game_sessions[mess.channel].player_roles[i] == '11':
        game_sessions[mess.channel].player_status[i][2] = 2
        game_sessions[mess.channel].police.append(i)
    else:
        game_sessions[mess.channel].player_status[i][2] = 0
    if game_sessions[mess.channel].player_roles[i] == '2':
        game_sessions[mess.channel].player_status[i][3] = 4
        game_sessions[mess.channel].mafia.append(i)
    elif game_sessions[mess.channel].player_roles[i] == '3':
        game_sessions[mess.channel].player_status[i][3] = 5
        game_sessions[mess.channel].mafia.append(i)
    elif game_sessions[mess.channel].player_roles[i] == '12':
        game_sessions[mess.channel].player_status[i][3] = 3
        game_sessions[mess.channel].mafia.append(i)
    elif game_sessions[mess.channel].player_roles[i] == '9':
        game_sessions[mess.channel].player_status[i][3] = 1
        game_sessions[mess.channel].mafia.append(i)
    else:
        game_sessions[mess.channel].player_status[i][3] = 0


async def night_echo(mess):
    if game_sessions[mess.channel].player_status[mess.author][2] > 1 and game_sessions[mess.channel].player_status[mess.author][1] == 0:
        for member in game_sessions[mess.channel].police:
            if member != mess.author and game_sessions[mess.channel].player_status[member][2] > 0 and game_sessions[mess.channel].player_status[member][1] == 0:
                await member.send(str(mess.author)[:-5] + ': ' + mess.content)
    elif game_sessions[mess.channel].player_status[mess.author][3] > 2 and game_sessions[mess.channel].player_status[mess.author][1] == 0:
        for member in game_sessions[mess.channel].mafia:
            if member != mess.author and game_sessions[mess.channel].player_status[member][3] > 1 and game_sessions[mess.channel].player_status[member][1] == 0:
                await member.send(str(mess.author)[:-5] + ': ' + mess.content)


async def after_game(mess):
    sd = ''
    ft = ''
    i = 0
    for member in game_sessions[mess.channel].player_roles:
        i += 1
        x = str(roles_definition[int(game_sessions[mess.channel].player_roles[member])])
        ft += str(i) + ') ' + str(member)[:-5] + '\n'
        sd += str(i) + ') ' + x + '\n'
    emb = discord.Embed(title='Роли игроков:', colour=discord.Color.darker_grey())
    emb.add_field(name='Игрок', value=ft, inline=True)
    emb.add_field(name='Роль', value=sd, inline=True)
    await mess.channel.send(embed=emb)


async def preparation_of_results(mode, message):
    for member in game_sessions[message.channel].player_status:
        if mode == 1:
            if game_sessions[message.channel].player_roles[member] == '6':
                game_sessions[message.channel].gamers[str(member.id)] = [1, roles_multiplier[int(game_sessions[message.channel].player_roles[member])-1], game_sessions[message.channel].player_status[member][0], roles_definition[int(game_sessions[message.channel].player_roles[member])]]
            else:
                game_sessions[message.channel].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel].player_roles[member]) - 1], game_sessions[message.channel].player_status[member][0], roles_definition[int(game_sessions[message.channel].player_roles[member])]]
        elif mode == 2:
            if int(game_sessions[message.channel].player_roles[member]) in [2, 3, 9, 10, 12]:
                game_sessions[message.channel].gamers[str(member.id)] = [1, roles_multiplier[int(game_sessions[message.channel].player_roles[member])-1], game_sessions[message.channel].player_status[member][0], roles_definition[int(game_sessions[message.channel].player_roles[member])]]
            else:
                game_sessions[message.channel].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel].player_roles[member]) - 1], game_sessions[message.channel].player_status[member][0], roles_definition[int(game_sessions[message.channel].player_roles[member])]]
        elif mode == 3:
            if int(game_sessions[message.channel].player_roles[member]) in [1, 4, 5, 7, 8, 11]:
                game_sessions[message.channel].gamers[str(member.id)] = [1, roles_multiplier[int(game_sessions[message.channel].player_roles[member]) - 1], game_sessions[message.channel].player_status[member][0], roles_definition[int(game_sessions[message.channel].player_roles[member])]]
            else:
                game_sessions[message.channel].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel].player_roles[member]) - 1], game_sessions[message.channel].player_status[member][0], roles_definition[int(game_sessions[message.channel].player_roles[member])]]
        else:
            game_sessions[message.channel].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel].player_roles[member]) - 1], game_sessions[message.channel].player_status[member][0], roles_definition[int(game_sessions[message.channel].player_roles[member])]]
    endgame(game_sessions[message.channel].gamers)



async def win_condition(message):
    if game_sessions[message.channel].maniac > 0 and game_sessions[message.channel].red + game_sessions[message.channel].black + game_sessions[message.channel].two_faced == 0:
        await message.channel.send('Игра окончена! Победа маньяка 🔪')
        await preparation_of_results(1, message)
        await after_game(message)
        return True
    elif game_sessions[message.channel].maniac == 0 and ((game_sessions[message.channel].black >= game_sessions[message.channel].red and game_sessions[message.channel].black > 0) or (game_sessions[message.channel].red + game_sessions[message.channel].black == 0 and game_sessions[message.channel].two_faced > 0)):
        await message.channel.send('Игра окончена! Победа мафии 🕵️')
        await preparation_of_results(2, message)
        await after_game(message)
        return True
    elif game_sessions[message.channel].maniac == 0 and game_sessions[message.channel].black == 0 and game_sessions[message.channel].red > 0:
        await message.channel.send('Игра окончена! Победа мирного города 👥')
        await preparation_of_results(3, message)
        await after_game(message)
        return True
    elif game_sessions[message.channel].maniac + game_sessions[message.channel].black + game_sessions[message.channel].two_faced + game_sessions[message.channel].red == 0:
        await message.channel.send('Игра окончена! Ничья. В городе не осталось живых ☠')
        await preparation_of_results(4, message)
        await after_game(message)
        return True


async def reduction_role_condition(i, mess):
    if int(game_sessions[mess.channel].player_roles[game_sessions[mess.channel].members[i]]) in [2, 3, 10, 12]:
        game_sessions[mess.channel].black -= 1
    elif int(game_sessions[mess.channel].player_roles[game_sessions[mess.channel].members[i]]) == 6:
        game_sessions[mess.channel].maniac -= 1
    elif int(game_sessions[mess.channel].player_roles[game_sessions[mess.channel].members[i]]) == 9:
        game_sessions[mess.channel].two_faced -= 1
    else:
        game_sessions[mess.channel].red -= 1
    game_sessions[mess.channel].player_status[game_sessions[mess.channel].members[i]][0] = 0

async def add_role(num, ctx):
    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    response = await ctx.bot.wait_for('message', check=check)
    try:
        request = response.content
        if request == '!reset':
            return True
        if int(request[:request.find(' ')]) not in [1, 2]:
            if game_sessions[ctx.channel].roles_num[request[:request.find(' ')]]+int(request[request.find(' ')+1:]) > 1:
                await ctx.send('Такой персонаж может быть только один')
                if await add_role(num, ctx) == True:
                    return True
            else:
                game_sessions[ctx.channel].roles_num[request[:request.find(' ')]] += int(request[request.find(' ')+1:])
                if num - int(request[request.find(' ') + 1:]) > 0:
                    if await add_role(num - int(request[request.find(' ') + 1:]), ctx) == True:
                        return True
        else:
            if int(request[request.find(' ')+1:]) <= num:
                game_sessions[ctx.channel].roles_num[request[:request.find(' ')]] += int(request[request.find(' ')+1:])
                if num - int(request[request.find(' ') + 1:]) > 0:
                    if await add_role(num - int(request[request.find(' ') + 1:]), ctx) == True:
                        return True
            else:
                await ctx.send('Количество ролей превышает количество игроков. Попробуйте снова.')
                if await add_role(num, ctx) == True:
                    return True
    except:
        if await add_role(num, ctx) == True:
            return True

async def timer(time,mess,member,vt):
    if vt == 0:
        await mess.channel.send('Ваш ход ' + str(member)[:-5])
        time_message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
        await time_message.add_reaction('⛔')
        for i in range(time - 1, -1, -1):
            if game_sessions[mess.channel].checker == 1:
                break
            time_break = tm.time()
            while True:
                if game_sessions[mess.channel].checker == 1:
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
            if game_sessions[mess.channel].player_status[i][0] != 0:
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
    if reaction.message.channel in list(game_sessions.keys()):
        if reaction.emoji == '⛔' and user == game_sessions[reaction.message.channel].right and game_sessions[reaction.message.channel].vn == 0:
            game_sessions[reaction.message.channel].checker = 1
        elif reaction.emoji == '⛔' and user != reaction.message.author and game_sessions[reaction.message.channel].vn == 3 and user in game_sessions[reaction.message.channel].members:
            if game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] == 0 and game_sessions[reaction.message.channel].player_status[user][0] != 0:
                game_sessions[reaction.message.channel].count -= 1
                game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] = 1
        elif reaction.emoji == '✅' and user != reaction.message.author and game_sessions[reaction.message.channel].vn == 1 and user in game_sessions[reaction.message.channel].members:
            if game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] == 0 and game_sessions[reaction.message.channel].player_status[user][0] != 0:
                game_sessions[reaction.message.channel].votes[game_sessions[reaction.message.channel].members.index(game_sessions[reaction.message.channel].gl)] += 1
                game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] = 1
        elif reaction.emoji == '✅' and user != reaction.message.author and game_sessions[reaction.message.channel].vn == 2 and user in game_sessions[reaction.message.channel].members:
            if game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] == 0 and game_sessions[reaction.message.channel].player_status[user][0] != 0:
                game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] = 1
                game_sessions[reaction.message.channel].guilty[game_sessions[reaction.message.channel].ind] += 1
        elif reaction.emoji == '✅' and user != reaction.message.author and game_sessions[reaction.message.channel].vn == 3 and user in game_sessions[reaction.message.channel].members:
            if game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] == 0 and game_sessions[reaction.message.channel].player_status[user][0] != 0:
                game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] = 1
                game_sessions[reaction.message.channel].count += 1
        elif reaction.emoji == '💤' and user != reaction.message.author and user in game_sessions[reaction.message.channel].members:
            if game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] == 0 and game_sessions[reaction.message.channel].player_status[user][0] != 0:
                game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] = 1
                game_sessions[reaction.message.channel].count -= 1
                if game_sessions[reaction.message.channel].count == 0:
                    await reaction.message.delete()
                    await reaction.message.channel.send('Наступает ночь 🌃')
        elif reaction.emoji == '⏰' and user != reaction.message.author and user in game_sessions[reaction.message.channel].members:
            if game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] == 0 and game_sessions[reaction.message.channel].player_status[user][0] != 0:
                game_sessions[reaction.message.channel].already[game_sessions[reaction.message.channel].members.index(user)] = 1
                game_sessions[reaction.message.channel].count -= 1
                if game_sessions[reaction.message.channel].count == 0:
                    await reaction.message.delete()
                    await reaction.message.channel.send('Наступает день 🌇')
    elif user in list(setting_sessions.keys()):
        if user != reaction.message.author and setting_sessions[user].vn == 4 and setting_sessions[user].right_to_change == user:
            if reaction.emoji == '🤵':
                setting_sessions[user].setgs['mode'] = 'non-auto'
                await setting_sessions[user].messages[0].edit(content=setting_sessions[user].messages[0].content[:setting_sessions[user].messages[0].content.find(':') + 2] + str(setting_sessions[user].setgs['mode']))
                await reaction.message.remove_reaction('🤖', user)
            elif reaction.emoji == '🤖':
                setting_sessions[user].setgs['mode'] = 'auto'
                await setting_sessions[user].messages[0].edit(content=setting_sessions[user].messages[0].content[:setting_sessions[user].messages[0].content.find(':') + 2] + str(setting_sessions[user].setgs['mode']))
                await reaction.message.remove_reaction('🤵', user)
            elif reaction.emoji == '🔊':
                setting_sessions[user].setgs['mute'] = 'off'
                await setting_sessions[user].messages[1].edit(content=setting_sessions[user].messages[1].content[:setting_sessions[user].messages[1].content.find(':') + 2] + str(setting_sessions[user].setgs['mute']))
                await reaction.message.remove_reaction('🔇', user)
            elif reaction.emoji == '🔇':
                setting_sessions[user].setgs['mute'] = 'on'
                await setting_sessions[user].messages[1].edit(content=setting_sessions[user].messages[1].content[:setting_sessions[user].messages[1].content.find(':') + 2] + str(setting_sessions[user].setgs['mute']))
                await reaction.message.remove_reaction('🔊', user)
            elif reaction.emoji == '✅':
                print(setting_sessions[user])
                change_settings(user.id, setting_sessions[user].setgs)
                await reaction.message.channel.send('Сохранено')
                for message in setting_sessions[user].messages:
                    await message.delete()
                del setting_sessions[user]
            elif reaction.emoji == '❌':
                for message in setting_sessions[user].messages:
                    await message.delete()
                del setting_sessions[user]
            elif reaction.emoji == '🔄':
                setting_sessions[user].setgs = {'mode': 'auto', 'mute': 'on', 'time': [60, 45, 15, 60, 40, 90]}
                await reaction.message.remove_reaction('🔄', user)
                await setting_sessions[user].messages[0].edit(content=setting_sessions[user].messages[0].content[:setting_sessions[user].messages[0].content.find(':')+2] + str(setting_sessions[user].setgs['mode']))
                await setting_sessions[user].messages[1].edit(content=setting_sessions[user].messages[1].content[:setting_sessions[user].messages[1].content.find(':') + 2] + str(setting_sessions[user].setgs['mute']))
                for i in range(2, 8):
                    await setting_sessions[user].messages[i].edit(content=setting_sessions[user].messages[i].content[:setting_sessions[user].messages[i].content.find(':') + 2] + str(setting_sessions[user].setgs['time'][i-2]) + ' сек')
            else:
                d = reaction.message.id
                for i in range(len(setting_sessions[user].messages)):
                    if setting_sessions[user].messages[i].id == d:
                        if reaction.emoji == '⏩':
                            setting_sessions[user].setgs['time'][i - 2] += 15
                            await reaction.message.remove_reaction('⏩', user)
                        elif reaction.emoji == '➡️':
                            setting_sessions[user].setgs['time'][i - 2] += 5
                            await reaction.message.remove_reaction('➡️', user)
                        elif reaction.emoji == '⬅️':
                            setting_sessions[user].setgs['time'][i - 2] -= 5
                            await reaction.message.remove_reaction('⬅️', user)
                        elif reaction.emoji == '⏪':
                            setting_sessions[user].setgs['time'][i - 2] -= 15
                            await reaction.message.remove_reaction('⏪', user)
                        break
                if setting_sessions[user].setgs['time'][i - 2] > 300:
                    setting_sessions[user].setgs['time'][i - 2] = 300
                elif setting_sessions[user].setgs['time'][i - 2] < 0:
                    setting_sessions[user].setgs['time'][i - 2] = 0
                await reaction.message.edit(content=reaction.message.content[:reaction.message.content.find(':')+2] + str(setting_sessions[user].setgs['time'][i-2]) + ' сек')

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
        if ctx.author.id == game_sessions[ctx.channel].right_to_vote.id and type(ctx.channel) != discord.channel.DMChannel:
            try:
                choice = int(choice)
            except:
                return
            if choice > len(game_sessions[ctx.channel].members) or choice - 1 < 0:
                await ctx.send('Игрока под номером ' + str(choice) + ' не существует, проголосуйте за другого.')
            elif choice-1 in game_sessions[ctx.channel].voted and sum(game_sessions[ctx.channel].votes) == 0:
                await ctx.send('Этот игрок уже выставлен на голосование. Выберите другого.')
            elif game_sessions[ctx.channel].player_status[game_sessions[ctx.channel].members[choice-1]][0] == 0:
                await ctx.send('Этот игрок уже убит. Выберите другого.')
            else:
                game_sessions[ctx.channel].vote_choice = choice
                await ctx.send('Принято!')
    except:
        pass

#-----------------Main commands---------------------

async def meeting_day(mess):
    await mess.channel.send('Начинается день знакомств 🤝')
    game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
    game_sessions[mess.channel].vn = 0
    game_sessions[mess.channel].tumb = 0
    for member in game_sessions[mess.channel].members:
        game_sessions[mess.channel].right = member
        game_sessions[mess.channel].checker = 0
        await timer(game_sessions[mess.channel].game_settings['time'][0], mess, member, 0)
    game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
    ms = await mess.channel.send('Город засыпает 💤')
    await ms.add_reaction('💤')
    game_sessions[mess.channel].count = 0
    for i in list(game_sessions[mess.channel].player_status.values()):
        if i[0] != 0:
            game_sessions[mess.channel].count += 1


async def day(mess):
    if game_sessions[mess.channel].killed != []:
        await mess.channel.send('Ночью были убиты игроки под номерами: ' + (', ').join(game_sessions[mess.channel].killed))
    else:
        await mess.channel.send('Ночью никто не был убит')
    game_sessions[mess.channel].vn = 0
    for person in game_sessions[mess.channel].killed:
        await reduction_role_condition(int(person)-1, mess)
        try:
            await game_sessions[mess.channel].members[int(person)-1].edit(
                nick=str(person) + '. ' + str(game_sessions[mess.channel].members[int(person)-1])[:-5] + ' ☠')
        except:
            pass
    if await win_condition(mess) == True:
        for member in game_sessions[mess.channel].members:
            try:
                await member.edit(nick=member.name)
            except:
                pass
        return
    await mess.channel.send('Начинается обсуждение и выставление кандидатур на голосование 🗣️')
    game_sessions[mess.channel].voted = []
    game_sessions[mess.channel].votes = [0 for i in range(len(game_sessions[mess.channel].members))]
    game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
    game_sessions[mess.channel].guilty.clear()
    game_sessions[mess.channel].killed.clear()
    for i in list(game_sessions[mess.channel].player_roles.keys()):
        if game_sessions[mess.channel].player_status[i][0] != 0:
            game_sessions[mess.channel].checker = 0
            game_sessions[mess.channel].vote_choice = ''
            member = i
            game_sessions[mess.channel].right = member
            game_sessions[mess.channel].right_to_vote = member
            await timer(game_sessions[mess.channel].game_settings['time'][0], mess, member, 0)
            if game_sessions[mess.channel].vote_choice == '':
                pass
            elif game_sessions[mess.channel].vote_choice - 1 not in game_sessions[mess.channel].voted:
                game_sessions[mess.channel].voted.append(game_sessions[mess.channel].vote_choice - 1)
    game_sessions[mess.channel].right_to_vote = None
    if len(game_sessions[mess.channel].voted) == 0:
        await mess.channel.send('Было принято решение никого не сажать в тюрьму 🚫')
        game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
        ms = await mess.channel.send('Город засыпает 💤')
        await ms.add_reaction('💤')
        game_sessions[mess.channel].count = 0
        for i in list(game_sessions[mess.channel].player_status.values()):
            if i[0] != 0:
                game_sessions[mess.channel].count += 1
    else:
        m = []
        for i in range(len(game_sessions[mess.channel].voted)):
            m.append(str(game_sessions[mess.channel].voted[i] + 1))
        await mess.channel.send('Обвиняются игроки под номерами: ' + (', ').join(m))
        await mess.channel.send('Обвиняемым предоставляется оправдательная речь 👨‍⚖️')
        for i in game_sessions[mess.channel].voted:
            game_sessions[mess.channel].checker = 0
            member = game_sessions[mess.channel].members[i]
            game_sessions[mess.channel].right = member
            await timer(game_sessions[mess.channel].game_settings['time'][1], mess, member, 0)
        await mess.channel.send('Начинается голосование 📢')
        game_sessions[mess.channel].tumb = 1
        game_sessions[mess.channel].right = None
        game_sessions[mess.channel].vn = 1
        for i in game_sessions[mess.channel].voted:
            member = game_sessions[mess.channel].members[i]
            game_sessions[mess.channel].gl = member
            await timer(game_sessions[mess.channel].game_settings['time'][2], mess, member, 1)
        for i in list(game_sessions[mess.channel].player_roles.keys()):
            if game_sessions[mess.channel].player_status[i][0] != 0 and game_sessions[mess.channel].already[game_sessions[mess.channel].members.index(i)] == 0:
                game_sessions[mess.channel].votes[game_sessions[mess.channel].voted[-1]] += 1
        await mess.channel.send('Голосование окончено')
        if game_sessions[mess.channel].votes.count(max(game_sessions[mess.channel].votes)) == 1:
            game_sessions[mess.channel].guil = game_sessions[mess.channel].votes.index(max(game_sessions[mess.channel].votes))
            game_sessions[mess.channel].vn = 0
            game_sessions[mess.channel].right = game_sessions[mess.channel].members[game_sessions[mess.channel].guil]
            game_sessions[mess.channel].checker = 0
            await mess.channel.send('Приговоренному дается право произнести последнюю речь 👨‍⚖️')
            await timer(game_sessions[mess.channel].game_settings['time'][4], mess, game_sessions[mess.channel].members[game_sessions[mess.channel].guil], 0)
            await reduction_role_condition(game_sessions[mess.channel].guil, mess)
            try:
                await game_sessions[mess.channel].members[game_sessions[mess.channel].guil].edit(nick=str(game_sessions[mess.channel].guil + 1) + '. ' + str(game_sessions[mess.channel].members[game_sessions[mess.channel].guil])[:-5] + ' ☠')
            except:
                pass
            await mess.channel.send(str(game_sessions[mess.channel].members[game_sessions[mess.channel].guil])[:-5] + ' был посажен за решетку 👮')
            if await win_condition(mess) == True:
                for member in game_sessions[mess.channel].members:
                    try:
                        await member.edit(nick=member.name)
                    except:
                        pass
                return
        else:
            for i in range(len(game_sessions[mess.channel].voted)):
                if game_sessions[mess.channel].votes[game_sessions[mess.channel].voted[i]] == max(game_sessions[mess.channel].votes):
                    game_sessions[mess.channel].guilty[game_sessions[mess.channel].voted[i] + 1] = 0
            await mess.channel.send(
                'Обвиняемым ' + str(game_sessions[mess.channel].guilty.keys())[11:-2] + ' предоставляются дополнительные оправдательные речи 👨‍⚖️')
            game_sessions[mess.channel].guilty.clear()
            game_sessions[mess.channel].right = None
            game_sessions[mess.channel].vn = 0
            for i in range(len(game_sessions[mess.channel].voted)):
                if game_sessions[mess.channel].votes[game_sessions[mess.channel].voted[i]] == max(game_sessions[mess.channel].votes):
                    game_sessions[mess.channel].checker = 0
                    game_sessions[mess.channel].guilty[game_sessions[mess.channel].voted[i]] = 0
                    member = game_sessions[mess.channel].members[game_sessions[mess.channel].voted[i]]
                    game_sessions[mess.channel].right = member
                    await timer(game_sessions[mess.channel].game_settings['time'][0], mess, member, 0)
            await mess.channel.send('Начинается повторное голосование 📢')
            game_sessions[mess.channel].right = None
            game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
            for i in range(len(game_sessions[mess.channel].guilty)):
                game_sessions[mess.channel].vn = 2
                member = game_sessions[mess.channel].members[list(game_sessions[mess.channel].guilty.keys())[i]]
                game_sessions[mess.channel].ind = list(game_sessions[mess.channel].guilty.keys())[i]
                await timer(game_sessions[mess.channel].game_settings['time'][2], mess, member, 1)
            for i in list(game_sessions[mess.channel].player_roles.keys()):
                if game_sessions[mess.channel].player_status[i][0] != 0 and game_sessions[mess.channel].already[game_sessions[mess.channel].members.index(i)] == 0:
                    game_sessions[mess.channel].guilty[list(game_sessions[mess.channel].guilty.keys())[-1]] += 1
            if list(game_sessions[mess.channel].guilty.values()).count(max(game_sessions[mess.channel].guilty.values())) == 1:
                game_sessions[mess.channel].vn = 0
                for i in list(game_sessions[mess.channel].guilty.keys()):
                    if game_sessions[mess.channel].guilty[i] == max(game_sessions[mess.channel].guilty.values()):
                        game_sessions[mess.channel].checker = 0
                        game_sessions[mess.channel].right = members[list(guilty.keys())[i]]
                        await mess.channel.send('Приговоренному дается право произнести последнюю речь 👨‍⚖️')
                        await timer(game_sessions[mess.channel].game_settings['time'][3], mess, game_sessions[mess.channel].members[list(game_sessions[mess.channel].guilty.keys())[i]], 0)

                        try:
                            await game_sessions[mess.channel].members[i].edit(nick=str(i + 1) + '. ' + str(game_sessions[mess.channel].members[i])[:-5] + ' ☠')
                        except:
                            pass
                            await mess.channel.send(str(game_sessions[mess.channel].members[i])[:-5] + ' был посажен за решетку 👮')
                        break
                if await win_condition(mess) == True:
                    for member in game_sessions[mess.channel].members:
                        try:
                            await member.edit(nick=member.name)
                        except:
                            pass
                    return
            else:
                for i in list(game_sessions[mess.channel].guilty.keys()):
                    if game_sessions[mess.channel].guilty[i] != max(game_sessions[mess.channel].guilty.values()):
                        del game_sessions[mess.channel].guilty[i]
                await mess.channel.send(
                    'По-прежнему остались игроки с одинаковым количеством голосов, поэтому принимается решение: выгнать или оставить всех\n✅ - выгнать, ⛔ - оставить')
                game_sessions[mess.channel].count = 0
                game_sessions[mess.channel].vn = 3
                game_sessions[mess.channel].right = None
                game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
                game_sessions[mess.channel].checker = 0
                await timer(ggame_sessions[mess.channel].ame_settings['time'][2], mess, member, 2)
                for i in list(game_sessions[mess.channel].player_roles.keys()):
                    if game_sessions[mess.channel].player_status[i][0] != 0 and game_sessions[mess.channel].already[game_sessions[mess.channel].members.index(i)] == 0:
                        game_sessions[mess.channel].count -= 1
                if game_sessions[mess.channel].count > 0:
                    await mess.channel.send('Приговоренным дается право произнести последнюю речь 👨‍⚖️')
                    game_sessions[mess.channel].vn = 0
                    for i in list(game_sessions[mess.channel].guilty.keys()):
                        game_sessions[mess.channel].checker = 0
                        game_sessions[mess.channel].right = game_sessions[mess.channel].members[list(game_sessions[mess.channel].guilty.keys())[i]]
                        await timer(game_sessions[mess.channel].game_settings['time'][2], mess, game_sessions[mess.channel].members[list(game_sessions[mess.channel].guilty.keys())[i]], 0)
                        await reduction_role_condition(i, mess)
                        try:
                            await game_sessions[mess.channel].members[i].edit(nick=str(i + 1) + '. ' + str(game_sessions[mess.channel].members[i])[:-5] + ' ☠')
                        except:
                            pass
                        await mess.channel.send(str(game_sessions[mess.channel].members[i])[:-5] + ' был посажен за решетку 👮')
                    if await win_condition(mess) == True:
                        for member in game_sessions[mess.channel].members:
                            try:
                                await member.edit(nick=member.name)
                            except:
                                pass
                        return
                else:
                    await mess.channel.send('Было принято решение никого не сажать в тюрьму 🚫')
        game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
        ms = await mess.channel.send('Город засыпает 💤')
        await ms.add_reaction('💤')
        game_sessions[mess.channel].count = 0
        for i in list(player_status.values()):
            if i[0] != 0:
                game_sessions[mess.channel].count += 1


async def night(mess):
    game_sessions[mess.channel].vn = -1
    for member in game_sessions[mess.channel].player_roles:
        if game_sessions[mess.channel].player_status[member][2] > 1 and game_sessions[mess.channel].player_status[member][0] == 0:
            game_sessions[mess.channel].player_status[member][2] = 1
        elif game_sessions[mess.channel].player_status[member][3] > 2 and game_sessions[mess.channel].player_status[member][0] == 0:
            game_sessions[mess.channel].player_status[member][3] = 2
        game_sessions[mess.channel].player_status[member][1] = 0
        game_sessions[mess.channel].player_status[member][5] = 0
        if game_sessions[mess.channel].player_roles[member] == '9':
            if game_sessions[mess.channel].player_status[member][4] != -1 and game_sessions[mess.channel].members[game_sessions[mess.channel].player_status[member][4]] in game_sessions[mess.channel].mafia:
                game_sessions[mess.channel].player_status[member][3] = 6
                game_sessions[mess.channel].two_faced -= 1
                game_sessions[mess.channel].black += 1
        elif game_sessions[mess.channel].player_roles[member] == '11':
            for j in game_sessions[mess.channel].player_roles:
                if game_sessions[mess.channel].player_roles[j] == '4' and game_sessions[mess.channel].player_status[j][0] == 0:
                    game_sessions[mess.channel].player_status[member][2] = 3
        elif game_sessions[mess.channel].player_roles[member] == '12':
            count = 0
            for j in game_sessions[mess.channel].player_roles:
                if int(game_sessions[mess.channel].player_roles[j]) in [2, 3] and game_sessions[mess.channel].player_status[j][0] == 1:
                    count += 1
            if count == 0:
                game_sessions[mess.channel].player_status[member][3] = 6
            del count
    for i in range(len(sequence)):
        if type(sequence[i]) == int:
            for j in list(game_sessions[mess.channel].player_roles.keys()):
                if int(game_sessions[mess.channel].player_roles[j]) == sequence[i]:
                    if game_sessions[mess.channel].player_status[j][0] != 0 and game_sessions[mess.channel].player_status[j][1] == 0:
                        game_sessions[mess.channel].right_to_act = [j]
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif game_sessions[mess.channel].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    if i != 3:
                        await timer(game_sessions[mess.channel].game_settings['time'][4], mess, [j], 3)
                    elif i == 3:
                        game_sessions[mess.channel].right_to_chat = game_sessions[mess.channel].mafia.copy()
                        await timer(game_sessions[mess.channel].game_settings['time'][4], mess, [j], 3)
                        if game_sessions[mess.channel].don_phase == 1 and game_sessions[mess.channel].player_status[j][0] != 0 and game_sessions[mess.channel].player_status[j][1] == 0 and vote_results.count(max(vote_results)) == 1 and sum(vote_results) != 0:
                            game_sessions[mess.channel].killed.append(str(vote_results.index(max(vote_results))+1))
                    game_sessions[mess.channel].right_to_act.clear()
                    game_sessions[mess.channel].right_to_chat.clear()
        elif type(sequence[i]) == list and i == 4:
            game_sessions[mess.channel].right_to_chat =  game_sessions[mess.channel].police.copy()
            for j in list(game_sessions[mess.channel].player_roles.keys()):
                if int(game_sessions[mess.channel].player_roles[j]) == 4 and game_sessions[mess.channel].player_status[j][0] != 0:
                    if game_sessions[mess.channel].player_status[j][1] == 0:
                        game_sessions[mess.channel].right_to_act = [j]
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif game_sessions[mess.channel].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    await timer(game_sessions[mess.channel].game_settings['time'][4], mess, [j], 3)
                    game_sessions[mess.channel].right_to_act.clear()
                    break
                elif int(game_sessions[mess.channel].player_roles[j]) == 11 and game_sessions[mess.channel].player_status[j][0] != 0:
                    if game_sessions[mess.channel].player_status[j][1] == 0:
                        game_sessions[mess.channel].right_to_act = [j]
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif game_sessions[mess.channel].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    await timer(game_sessions[mess.channel].game_settings['time'][4], mess, [j], 3)
                    game_sessions[mess.channel].right_to_act.clear()
                    break
            game_sessions[mess.channel].right_to_chat.clear()
        elif type(sequence[i]) == list and i == 2:
            game_sessions[mess.channel].right_to_chat = game_sessions[mess.channel].mafia.copy()
            game_sessions[mess.channel].right_to_act = []
            game_sessions[mess.channel].mafia_vote = []
            for j in list(game_sessions[mess.channel].player_roles.keys()):
                if int(game_sessions[mess.channel].player_roles[j]) == 9 and game_sessions[mess.channel].player_status[j][0] != 0:
                    if game_sessions[mess.channel].player_status[j][1] == 0:
                        game_sessions[mess.channel].right_to_act.append(j)
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif game_sessions[mess.channel].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                elif int(game_sessions[mess.channel].player_roles[j]) == 12 and game_sessions[mess.channel].player_status[j][0] != 0:
                    count = 0
                    for member in list(game_sessions[mess.channel].player_roles.keys()):
                        if int(game_sessions[mess.channel].player_roles[member]) in [2, 3] and game_sessions[mess.channel].player_status[member][0] != 0:
                            count += 1
                    if game_sessions[mess.channel].player_status[j][1] == 0 and count == 0:
                        game_sessions[mess.channel].right_to_act.append(j)
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif game_sessions[mess.channel].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                elif int(game_sessions[mess.channel].player_roles[j]) == 2 and game_sessions[mess.channel].player_status[j][0] != 0:
                    if game_sessions[mess.channel].player_status[j][1] == 0:
                        game_sessions[mess.channel].right_to_act.append(j)
                        await j.send('⚠️ ВАШ ХОД ⚠️')
                    elif game_sessions[mess.channel].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
            await mess.channel.send('Ход ' + sequence_guild_message[i])
            await timer(game_sessions[mess.channel].game_settings['time'][5], mess, game_sessions[mess.channel].right_to_act, 3)
            game_sessions[mess.channel].right_to_act.clear()
            vote_results = []
            for j in range(1, len(game_sessions[mess.channel].members)+1):
                vote_results.append(game_sessions[mess.channel].mafia_vote.count(str(j)))
            for j in list(game_sessions[mess.channel].player_roles.keys()):
                if game_sessions[mess.channel].player_roles[j] == '3' and game_sessions[mess.channel].player_status[j][0] != 0 and game_sessions[mess.channel].player_status[j][1] == 0:
                    game_sessions[mess.channel].right_to_act = [j]
                    if sum(vote_results) != 0:
                        for l in range(len(vote_results)):
                            if vote_results[l] != 0:
                                await j.send(str(vote_results[l]) + ' проголосовал(-о) за убийство ' + str(l+1))
                    else:
                        await j.send('Мафия не выбрала ни одной цели для убийства')
                elif game_sessions[mess.channel].player_roles[j] == '3' and (game_sessions[mess.channel].player_status[j][0] == 0 or game_sessions[mess.channel].player_status[j][1] != 0) or list(game_sessions[mess.channel].player_roles.values()).count('3') == 0:
                    if sum(vote_results) != 0:
                        k = vote_results.index(max(vote_results))
                        if vote_results.count(max(vote_results)) == 1 and game_sessions[mess.channel].player_roles[game_sessions[mess.channel].members[k]] != '8' and game_sessions[mess.channel].player_status[game_sessions[mess.channel].members[k]][1] != 2:
                            game_sessions[mess.channel].killed.append(str(k+1))
            game_sessions[mess.channel].don_phase = 1
        game_sessions[mess.channel].killed = list(set(game_sessions[mess.channel].killed))
        game_sessions[mess.channel].killed.sort()

    for i in game_sessions[mess.channel].killed:
        try:
            game_sessions[mess.channel].player_status[game_sessions[mess.channel].members[int(i)-1]][0] = 0
        except:
            pass
    game_sessions[mess.channel].already = [0 for i in range(len(game_sessions[mess.channel].members))]
    ms = await mess.channel.send('Город просыпается ⏰')
    await ms.add_reaction('⏰')
    game_sessions[mess.channel].right_to_act.clear()
    game_sessions[mess.channel].count = 0
    for i in list(game_sessions[mess.channel].player_status.values()):
        if i[0] != 0:
            game_sessions[mess.channel].count += 1
    if game_sessions[mess.channel].count == 0:
        await ms.delete()
        await mess.channel.send('Наступает день 🌇')

@client.command()
async def gencl(ctx):
    if type(ctx.channel) != discord.channel.DMChannel:
        if ctx.channel not in list(game_sessions.keys()):
            game_sessions[ctx.channel] = Game()
        else:
            await ctx.send('В данном канале уже создается список или идет игра')
            return
        game_sessions[ctx.channel].roles_num = roles_num_b.copy()
        game_sessions[ctx.channel].members = ctx.message.author.voice.channel.members
        #amount = len(game_sessions[ctx.channel].members)
        amount = 5
        if amount > 3 and amount < 11:
                game_sessions[ctx.channel].roles_num['2'], game_sessions[ctx.channel].roles_num['3'], game_sessions[ctx.channel].roles_num['4'] = amount//3 - 1, 1, 1
                game_sessions[ctx.channel].roles_num['1'] = amount - sum(list(game_sessions[ctx.channel].roles_num.values()))
                await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" +
                               "Мирных жителей: " + str(game_sessions[ctx.channel].roles_num['1']) + "\n" +
                               "Мафий: " + str(game_sessions[ctx.channel].roles_num['2']) + "\n" +
                               "Донов мафии: " + str(game_sessions[ctx.channel].roles_num['3']) + "\n" +
                               "Комиссаров: " + str(game_sessions[ctx.channel].roles_num['4']))
        else:
            await ctx.send('Классический режим для доступен при команде от 3 до 10 игроков')

@client.command()
async def genex(ctx):
    if ctx.channel not in list(game_sessions.keys()):
        game_sessions[ctx.channel] = Game()
    else:
        await ctx.send('В данном канале уже создается список или идет игра')
        return
    global roles_num
    global members
    global roles_num_b
    if type(ctx.channel) != discord.channel.DMChannel:
        roles_num = roles_num_b.copy()
        members = ctx.message.author.voice.channel.members
        amount = len(members)


@client.command()
async def settings(ctx):
    setting_sessions[ctx.author] = Settings(4, ctx.author, get_settings(ctx.author.id), [])
    setting_sessions[ctx.author].messages.append(await ctx.send('Режим: ' + str(setting_sessions[ctx.author].setgs['mode'])))
    await setting_sessions[ctx.author].messages[0].add_reaction('🤵')
    await setting_sessions[ctx.author].messages[0].add_reaction('🤖')
    setting_sessions[ctx.author].messages.append(await ctx.send('Мут: ' + str(setting_sessions[ctx.author].setgs['mute'])))
    await setting_sessions[ctx.author].messages[1].add_reaction('🔊')
    await setting_sessions[ctx.author].messages[1].add_reaction('🔇')
    setting_sessions[ctx.author].messages.append(await ctx.send('Дневная речь: ' + str(setting_sessions[ctx.author].setgs['time'][0]) + ' сек'))
    setting_sessions[ctx.author].messages.append(await ctx.send('Оправдательная речь: ' + str(setting_sessions[ctx.author].setgs['time'][1]) + ' сек'))
    setting_sessions[ctx.author].messages.append(await ctx.send('Время голосования: ' + str(setting_sessions[ctx.author].setgs['time'][2]) + ' сек'))
    for i in range(2, 5):
        await setting_sessions[ctx.author].messages[i].add_reaction('⏪')
        await setting_sessions[ctx.author].messages[i].add_reaction('⬅️')
        await setting_sessions[ctx.author].messages[i].add_reaction('➡️')
        await setting_sessions[ctx.author].messages[i].add_reaction('⏩')
    setting_sessions[ctx.author].messages.append(await ctx.send('Речь приговоренного: ' + str(setting_sessions[ctx.author].setgs['time'][3]) + ' сек'))
    setting_sessions[ctx.author].messages.append(await ctx.send('Ночное время одиночной роли: ' + str(setting_sessions[ctx.author].setgs['time'][4]) + ' сек'))
    setting_sessions[ctx.author].messages.append(await ctx.send('Ночное время мафии: ' + str(setting_sessions[ctx.author].setgs['time'][5]) + ' сек'))
    for i in range(5, 8):
        await setting_sessions[ctx.author].messages[i].add_reaction('⏪')
        await setting_sessions[ctx.author].messages[i].add_reaction('⬅️')
        await setting_sessions[ctx.author].messages[i].add_reaction('➡️')
        await setting_sessions[ctx.author].messages[i].add_reaction('⏩')
    setting_sessions[ctx.author].messages.append(await ctx.send('Сохранить?'))
    await setting_sessions[ctx.author].messages[-1].add_reaction('✅')
    await setting_sessions[ctx.author].messages[-1].add_reaction('❌')
    await setting_sessions[ctx.author].messages[-1].add_reaction('🔄')

@client.command()
async def reset(ctx):
    if ctx.channel in list(game_sessions.keys()):
        del game_sessions[ctx.channel]
        await ctx.send('Список обнулен')
    else:
        await ctx.send('Список не задан')

@client.command()
async def create(ctx):
    if ctx.channel not in list(game_sessions.keys()):
        game_sessions[ctx.channel] = Game()
    else:
        await ctx.send('В данном канале уже создается список или идет игра')
        return 
    game_sessions[ctx.channel].game_settings = get_settings(ctx.author.id)
    if game_sessions[ctx.channel].game_settings['mode'] == "non-auto" and type(ctx.channel) != discord.channel.DMChannel:
        await ctx.send("Перед началом удостоверьтесь, все ли желающие подключены к Вашему голосовому каналу, в противном случае не все роли смогут выдаться.\nЕсли всё готово, можно приступать к настройке игровой сессии.")
        game_sessions[ctx.channel].roles_num = roles_num_b.copy()

        def check(m):
            return m.author.id == ctx.author.id

        game_sessions[ctx.channel].members = ctx.message.author.voice.channel.members
        for member in game_sessions[ctx.channel].members:
            if member.bot:
                game_sessions[ctx.channel].members.remove(member)
        await ctx.send("Выберите ведущего.")
        response = await ctx.bot.wait_for('message', check=check)
        for member in game_sessions[ctx.channel].members:
            if member.mentioned_in(response):
                emb = discord.Embed(title="Вас назначили ведущим игры.", colour=discord.Color.darker_grey())
                emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713750207623331880/AATXAJxHckd0XbeQRXnekTtsXFQ0vgyIRvtCrntQeQs900-c-k-c0xffffffff-no-rj-mo.png?width=519&height=519")
                await member.send(embed=emb)
                game_master = member
                game_sessions[ctx.channel].members.remove(game_master)
                break
        await ctx.send("Задайте роли.")
        await ctx.send("1. Мирный житель " + "\n" + "2. Мафия " + "\n" + "3. Дон мафии " + "\n" + "4. Комиссар " + "\n"
                       + "5. Доктор " + "\n" + "6. Маньяк " + "\n" + "7. Куртизанка " + "\n" + "8. Бессмертный " + "\n"
                       + "9. Двуликий " + "\n" + "10. Вор " + "\n" + "11. Сержант " + "\n" + "12. Оборотень")
        if await add_role(len(game_sessions[ctx.channel].members), ctx) == True:
            return
        await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" + 
                       "Мирных жителей: " + str(game_sessions[ctx.channel].roles_num['1']) + "\n" + 
                       "Мафий: " + str(game_sessions[ctx.channel].roles_num['2']) + "\n" + 
                       "Донов мафии: " + str(game_sessions[ctx.channel].roles_num['3']) + "\n" + 
                       "Комиссаров: " + str(game_sessions[ctx.channel].roles_num['4']) + "\n" + 
                       "Докторов: " + str(game_sessions[ctx.channel].roles_num['5']) + "\n" + 
                       "Маньяков: " + str(game_sessions[ctx.channel].roles_num['6']) + "\n" + 
                       "Куртизанок: " + str(game_sessions[ctx.channel].roles_num['7']) + "\n" + 
                       "Бессмертных: " + str(game_sessions[ctx.channel].roles_num['8']) + "\n" + 
                       "Двуликих: " + str(game_sessions[ctx.channel].roles_num['9']) + "\n" + 
                       "Воров: " + str(game_sessions[ctx.channel].roles_num['10']) + "\n" + 
                       "Сержантов: " + str(game_sessions[ctx.channel].roles_num['11']) + "\n" + 
                       "Оборотней: " + str(game_sessions[ctx.channel].roles_num['12']))
    elif game_sessions[ctx.channel].game_settings['mode'] == 'auto' and type(ctx.channel) != discord.channel.DMChannel:
        await ctx.send(
            "Перед началом удостоверьтесь, все ли желающие подключены к Вашему голосовому каналу, в противном случае не"
            " все роли смогут выдаться.\nЕсли всё готово, можно приступать к настройке игровой сессии.")
        game_sessions[ctx.channel].roles_num = roles_num_b.copy()
        game_sessions[ctx.channel].members = ctx.message.author.voice.channel.members
        for member in game_sessions[ctx.channel].members:
            if member.bot:
                game_sessions[ctx.channel].members.remove(member)
        await ctx.send("Задайте роли.")
        await ctx.send(
            "1. Мирный житель " + "\n" + "2. Мафия " + "\n" + "3. Дон мафии " + "\n" + "4. Комиссар " + "\n" + 
            "5. Доктор " + "\n" + "6. Маньяк " + "\n" + "7. Куртизанка " + "\n" + "8. Бессмертный " + "\n" + 
            "9. Двуликий " + "\n" + "10. Вор " + "\n" + "11. Сержант " + "\n" + "12. Оборотень")
        if await add_role(len(game_sessions[ctx.channel].members), ctx) == True:
            return
        await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" +
                       "Мирных жителей: " + str(game_sessions[ctx.channel].roles_num['1']) + "\n" +
                       "Мафий: " + str(game_sessions[ctx.channel].roles_num['2']) + "\n" +
                       "Донов мафии: " + str(game_sessions[ctx.channel].roles_num['3']) + "\n" +
                       "Комиссаров: " + str(game_sessions[ctx.channel].roles_num['4']) + "\n" +
                       "Докторов: " + str(game_sessions[ctx.channel].roles_num['5']) + "\n" +
                       "Маньяков: " + str(game_sessions[ctx.channel].roles_num['6']) + "\n" +
                       "Куртизанок: " + str(game_sessions[ctx.channel].roles_num['7']) + "\n" +
                       "Бессмертных: " + str(game_sessions[ctx.channel].roles_num['8']) + "\n" +
                       "Двуликих: " + str(game_sessions[ctx.channel].roles_num['9']) + "\n" +
                       "Воров: " + str(game_sessions[ctx.channel].roles_num['10']) + "\n" +
                       "Сержантов: " + str(game_sessions[ctx.channel].roles_num['11']) + "\n" +
                       "Оборотней: " + str(game_sessions[ctx.channel].roles_num['12']))


@client.command()
async def pool(ctx):
    if type(ctx.channel) != discord.channel.DMChannel:
        if ctx.channel in list(game_sessions.keys()):
            await ctx.send("1. Мирных жителей: " + str(game_sessions[ctx.channel].roles_num['1']) + "\n" + 
                           "2. Мафий: " + str(game_sessions[ctx.channel].roles_num['2']) + "\n" + 
                           "3. Донов мафии: " + str(game_sessions[ctx.channel].roles_num['3']) + "\n" + 
                           "4. Комиссаров: " + str(game_sessions[ctx.channel].roles_num['4']) + "\n" + 
                           "5. Докторов: " + str(game_sessions[ctx.channel].roles_num['5']) + "\n" + 
                           "6. Маньяков: " + str(game_sessions[ctx.channel].roles_num['6']) + "\n" + 
                           "7. Куртизанок: " + str(game_sessions[ctx.channel].roles_num['7']) + "\n" + 
                           "8. Бессмертных: " + str(game_sessions[ctx.channel].roles_num['8']) + "\n" + 
                           "9. Двуликих: " + str(game_sessions[ctx.channel].roles_num['9']) + "\n" + 
                           "10. Воров: " + str(game_sessions[ctx.channel].roles_num['10']) + "\n" + 
                           "11. Сержантов: " + str(game_sessions[ctx.channel].roles_num['11']) + "\n" + 
                           "12. Оборотней: " + str(game_sessions[ctx.channel].roles_num['12']) + "\n\n" + 
                           "Оставшихся мест: " + str(len(game_sessions[ctx.channel].members) -
                                                     int(sum(list(game_sessions[ctx.channel].roles_num.values())))))
        else:
            await ctx.send('Необходимо создать список ролей')

@client.command()
async def save(ctx, name=None):
    if name != None:
        if ctx.channel in list(game_sessions.keys()):
            if game_sessions[ctx.channel].roles_num != {}:
                await ctx.send('Список сохранен под названием {}'.format(name))
                save_set(ctx.author.id, name, game_sessions[ctx.channel].roles_num)
            else:
                await ctx.send('Сохранить список ролей можно только до начала игры')
        else:
            await ctx.send('Необходимо создать список ролей')
    else:
        await ctx.send('Необходимо задать имя списка')


@client.command()
async def start(ctx, name=None):
    if ctx.channel not in list(game_sessions.keys()):
        game_sessions[ctx.channel] = Game()
    elif ctx.channel in list(game_sessions.keys()) and name != None:
        await ctx.send('В данном канале уже создается список или идет игра')
        return
    game_sessions[ctx.channel].game_settings = get_settings(ctx.author.id)
    if name != None and name != 'cl' and name != 'ex':
        new_set = load_set(ctx.author.id, name)
        game_sessions[ctx.channel].members = ctx.message.author.voice.channel.members
        if new_set == {}:
            await ctx.send('Такого списка ролей не существует')
            del game_sessions[ctx.channel]
            return
        else:
            game_sessions[ctx.channel].roles_num = new_set
            del new_set
    elif name == 'cl':
        await gencl(ctx)
    elif name == 'ex':
        await genex(ctx)
    if type(ctx.channel) != discord.channel.DMChannel:
        for role in game_sessions[ctx.channel].roles_num.copy():
            if game_sessions[ctx.channel].roles_num[role] == 0:
                if role in game_sessions[ctx.channel].roles_num:
                    del game_sessions[ctx.channel].roles_num[role]
        if game_sessions[ctx.channel].roles_num == {}:
            await ctx.send("Вы не задали роли")
            del game_sessions[ctx.channel]
            return
        elif sum(list(game_sessions[ctx.channel].roles_num.values())) != len(game_sessions[ctx.channel].members):
            await ctx.send('Данный список ролей не подходит для текущего количества игроков')
            del game_sessions[ctx.channel]
            return
        else:
            roles_num_list = []
            while game_sessions[ctx.channel].roles_num != {}:
                for role in game_sessions[ctx.channel].roles_num.copy():
                    if role in game_sessions[ctx.channel].roles_num:
                        for i in range(0, game_sessions[ctx.channel].roles_num[role]):
                            roles_num_list.append(role)
                        del game_sessions[ctx.channel].roles_num[role]
            counter = 1
            for member in game_sessions[ctx.channel].members:
                counter += 1
                random.seed(random.randint(0, 100))
                index_of_giving_role = random.randint(0, len(roles_num_list) - 1)
                giving_role = roles_num_list[index_of_giving_role]
                roles_num_list.pop(index_of_giving_role)
                game_sessions[ctx.channel].player_roles[member] = giving_role
                emb = discord.Embed(title=roles_description[giving_role][0], colour=discord.Color.darker_grey())
                emb.add_field(name="Описание роли:", value=roles_description[giving_role][1])
                emb.set_image(url=roles_description[giving_role][2])
                await member.send(embed=emb)
        if game_sessions[ctx.channel].game_settings['mode'] == 'non-auto':
            pass
        else:
            try:
                for i in range(len(game_sessions[ctx.channel].members)):
                    try:
                        await game_sessions[ctx.channel].members[i].edit(nick=(str(i+1)+'. '+str(game_sessions[ctx.channel].members[i])[:-5]))
                    except:
                        pass
                for i in list(game_sessions[ctx.channel].player_roles.values()):
                    if int(i) in [2, 3, 10, 12]:
                        game_sessions[ctx.channel].black += 1
                    elif int(i) == 6:
                        game_sessions[ctx.channel].maniac += 1
                    elif int(i) == 9:
                        game_sessions[ctx.channel].two_faced += 1
                    else:
                        game_sessions[ctx.channel].red += 1
                game_sessions[ctx.channel].player_status = {game_sessions[ctx.channel].members[x]: [0 for i in range(6)] for x in range(len(game_sessions[ctx.channel].members))}
                for i in list(game_sessions[ctx.channel].player_roles.keys()):
                    await status_maker(i, ctx)
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
        if mess.author in game_sessions[mess.channel].members and mess.content[0] != '!' and mess.author in game_sessions[mess.channel].right_to_chat:
            await night_echo(mess)
    await client.process_commands(mess)

#---------------------Token-------------------------

token = 'NzEzMzczNTg4ODYxODc4MzQz.XsfK7Q.IigCNgypVztyU5cOg_Bg2tgOYsI'
client.run(token)
