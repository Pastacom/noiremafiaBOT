# -*- coding: utf8 -*-!
import discord
from discord.ext import commands
import asyncio
import random
import time as tm
from DB import endgame, save_set, load_set, get_settings, change_settings, get_all_sets, change_set

client = commands.Bot(command_prefix="!")
client.remove_command("help")

game_sessions = {}
setting_sessions = {}
night_ids = {}
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
    def __init__(self):
        self.tumb = 0
        self.mafia_vote = []
        self.voted = []
        self.gamers = {}
        self.votes = []
        self.already = {}
        self.guilty = {}
        self.checker = 0
        self.vn = -1
        self.killed = []
        self.vote_choice = ''
        self.right = None
        self.right_to_vote = None
        self.roles_num = {}
        self.player_roles = {}
        self.player_status = {}
        self.right_to_chat = []
        self.right_to_act = []
        self.mafia = []
        self.police = []
        self.members = []
        self.don_phase = 1
        self.guil = None
        self.ind = None
        self.red = 0
        self.black = 0
        self.two_faced = 0
        self.maniac = 0
        self.game_settings = {}
        self.count = 0
        self.gl = None
        self.running = False
        self.game_mode = 'classic'
        self.context = None


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
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="The Godfather"))
    counter = 0
    my_max = 0
    guild = client.get_guild(713353831706263573)
    for chan in guild.channels:
        if type(chan) == discord.channel.CategoryChannel and 'Игровая' in chan.name:
            counter += 1
    for i in range(len(guild.roles)):
        role = guild.roles[i]
        if role.name[0:10] == 'game_room_':
            if my_max < int(role.name[-1]):
                my_max = int(role.name[-1])
    for i in range(my_max+1, counter+1):
        role = await guild.create_role(name='game_room_'+str(i), colour=discord.Colour(0xFF0000))
        for cat in guild.channels:
            if type(cat) == discord.channel.CategoryChannel and 'Игровая' in cat.name:
                if int(cat.name[cat.name.find('(')-2]) == i:
                    await cat.set_permissions(role, connect=True, add_reactions=True, read_messages=True,
                                              send_messages=True, speak=True, stream=True, view_channel=True,
                                              use_voice_activation=True)


#-----------------Utility commands------------------


@client.event
async def on_voice_state_update(user, before, after):
    if after.channel != None:
        if after.channel.id == 804735640859705404:
            for chan in after.channel.guild.channels:
                if type(chan) == discord.channel.VoiceChannel:
                    if chan.user_limit == 10 and len(chan.members) < 10:
                        for role in after.channel.guild.roles:
                            if role.name == 'game_room_'+chan.name[-1]:
                                await user.add_roles(role)
                                await user.move_to(chan)
                                break
                        break
        elif after.channel.id == 713363182135279640:
            for chan in after.channel.guild.channels:
                if type(chan) == discord.channel.VoiceChannel:
                    if chan.user_limit > 10 and len(chan.members) < 20:
                        for role in after.channel.guild.roles:
                            if role.name == 'game_room_' + chan.name[-1]:
                                await user.add_roles(role)
                                await user.move_to(chan)
                                break
                        break
    if before.channel != None:
        if 'Комната' in before.channel.name:
            for role in before.channel.guild.roles:
                if role.name == 'game_room_' + before.channel.name[-1]:
                    await user.remove_roles(role)
                    break


async def blank_message(number, ctx):
    for i in range(number):
        await ctx.send('_ _')


async def unmute(mess, member):
    if game_sessions[mess.channel.id].game_settings['mute'] == 'on':
        try:
            await member.edit(mute=False)
        except:
            pass


async def mute(mess, member):
    if game_sessions[mess.channel.id].game_settings['mute'] == 'on':
        try:
            await member.edit(mute=True)
        except:
            pass

@client.command()
async def help(ctx):
    user = ctx.message.author
    emb = discord.Embed(title="Доступные команды:", colour= discord.Color.from_rgb(199, 109, 13))
    emb.add_field(name="!settings (!st)", value="Изменить личные преднастройки игры. В появившемся сообщении бота нажимайте на реакции, чтобы изменить параметры.\n\n⏪ / ⏩ - Изменить время на 15 секунд назад/вперёд.\n⬅ / ➡ - Изменить время на 5 секунд назад/вперёд.\n🤵 / 🤖 - Изменить режим игры. 🤵 - с ведущим, выбирается один человек на роль ведущего, который будет проводить игру сам. 🤖 - без ведущего, бот будет проводить игру автоматически.\n🔊 / 🔇 - Выключить/включить отключение микрофона игрокам, когда они не ходят.\nПосле изменений нажмите ✅, чтобы сохранить настройки, ❌ чтобы отменить и 🔄, чтобы выставить настройки по умолчанию.\n\n_", inline=False)
    emb.add_field(name="!reset (!r)", value="Пишется после, или во время создания списка ролей, если вы хотите отменить создание игры.\n\n_", inline=False)
    emb.add_field(name="!start (!s)", value="Начинает игру. Вы можете добавить название вашего сохранённого списка ролей, посмотреть которые можно командой !sets.\n\nПример:\nВы хотите создать игру по сценарию из вашего набора под названием game1: `!start game1`\n\n_", inline=False)
    emb.add_field(name="!save", value="Сохранить преднастройку ролей. Пишется после создания списка ролей. После команды следует указать произвольное название набора. При одинаковых названиях набор перезаписывается\n\nПример:\nВы создали игру и хотите сохранить настройки списка ролей для последующих игр: `!save game1`\n\n_", inline=False)
    emb.add_field(name="!sets", value="Вывести список ваших личных преднастроек игры, сохранённых командой `!save`. Всего у вас 5 мест для различных наборов.\n\n_", inline=False)
    emb.add_field(name="!action (!a)", value="Пишется в личные сообщения боту, когда он объявляет о начале вашего хода в ночное время. После команды следует указать номер игрока, указывая цель вашего хода.\n\nПримеры:\nИграя за Мафию вы хотите проголосовать за игрока под номером №7: `!action 7`\nИграя за Комиссара вы хотите проверить игрока под номером №3: `!action 3`\n\n_", inline=False)
    emb.add_field(name="!vote (!v)", value="Пишется в чат, где началась ваша игра, после объявления вашего хода, в дневное время. После команды следует указать номер игрока через пробел, чтобы выставить этого игрока на дневное голосование.\n\nПример:\nВы подозреваете игрока №5 и хотите выставить его на голосование: `!vote 5`", inline=False)
    await user.send(embed=emb)
    await ctx.send("Список команд был отправлен вам в личные сообщения.")
#-------------------Main body-----------------------


#---------------Additional functions----------------


@client.command()
async def action(ctx, choice):
    if ctx.author in game_sessions[night_ids[ctx.channel.id]].right_to_act and ctx.guild == None:
        if game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][5] == 1:
            await ctx.send('Вы уже сходили')
            return
        try:
            choice = int(choice)
        except:
            return
        if choice > len(game_sessions[night_ids[ctx.channel.id]].members) or choice - 1 < 0:
            await ctx.send('Игрока под номером ' + str(choice) + ' не существует, проголосуйте за другого.')
            return
        elif game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice - 1]][0] == 0:
            await ctx.send('Этот игрок уже убит. Выберите другого.')
            return
        else:
            choice -= 1
            if game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '3' and game_sessions[night_ids[ctx.channel.id]].don_phase == 1:
                None
            else:
                game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][5] = 1
            if game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '10':
                if game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][4] != choice:
                    game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][4] = choice
                    game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][1] = 1
                else:
                    await ctx.send('Нельзя лишать одного и того же игрока хода два раза подряд')
                    return
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '7':
                if game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][4] != choice:
                    if game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]] != '6':
                        game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][4] = choice
                        game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][1] = 2
                    else:
                        game_sessions[night_ids[ctx.channel.id]].killed.append(str(game_sessions[night_ids[ctx.channel.id]].members.index(ctx.author)+1))
                        game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][1] = 2
                else:
                    await ctx.send('Нельзя лишать одного и того же игрока хода два раза подряд')
                    return
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '4' or (game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '11' and game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][2] == 3):
                for member in game_sessions[night_ids[ctx.channel.id]].police:
                    if int(game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]]) in [1, 4, 5, 6, 7, 8, 11, 12]:
                        await member.send('Игрок под номером ' + str(choice+1) + ' играет за команду мирных')
                    else:
                        await member.send('Игрок под номером ' + str(choice+1) + ' играет за команду мафии')
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '5':
                if game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][4] != choice:
                    game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][4] = choice
                    if str(choice+1) in game_sessions[night_ids[ctx.channel.id]].killed:
                        game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][0] = 1
                        del game_sessions[night_ids[ctx.channel.id]].killed[game_sessions[night_ids[ctx.channel.id]].killed.index(str(choice+1))]
                else:
                    await ctx.send('Нельзя лечить одного и того игрока два раза подряд')
                    return
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '6':
                if game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]] != '8' and game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][1] != 2:
                    game_sessions[night_ids[ctx.channel.id]].killed.append(str(choice+1))
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '12' and game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][3] == 6:
                if game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]] != '8' and game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][1] != 2:
                    game_sessions[night_ids[ctx.channel.id]].killed.append(str(choice + 1))
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '9' and game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][3] == 6:
                if game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]] != '8' and game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][1] != 2:
                    game_sessions[night_ids[ctx.channel.id]].killed.append(str(choice + 1))
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '9' and game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][3] == 1:
                if game_sessions[night_ids[ctx.channel.id]].members[choice] != ctx.author:
                    game_sessions[night_ids[ctx.channel.id]].player_status[ctx.author][4] = choice
                else:
                    await ctx.send('Вам необходимо найти членов мафии. Нельзя выбирать целью себя самого')
                    return
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '2':
                game_sessions[night_ids[ctx.channel.id]].mafia_vote.append(str(choice+1))
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '3' and game_sessions[night_ids[ctx.channel.id]].don_phase == 1:
                if game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]] != '8' and game_sessions[night_ids[ctx.channel.id]].player_status[game_sessions[night_ids[ctx.channel.id]].members[choice]][1] != 2:
                    game_sessions[night_ids[ctx.channel.id]].killed.append(str(choice+1))
                    await ctx.send('Мафия выбрала цель для убийства')
                    await ctx.send('Теперь вы можете выбрать цель для проверки')
                game_sessions[night_ids[ctx.channel.id]].don_phase = 2
            elif game_sessions[night_ids[ctx.channel.id]].player_roles[ctx.author] == '3' and game_sessions[night_ids[ctx.channel.id]].don_phase == 2:
                if game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]] == '4' or game_sessions[night_ids[ctx.channel.id]].player_roles[game_sessions[night_ids[ctx.channel.id]].members[choice]] == '11':
                    await ctx.send('Этот игрок - комиссар или сержант')
                else:
                    await ctx.send('Этот игрок не комиссар и не сержант')
            else:
                await ctx.send('Вы не ходите ночью')
                return
            await ctx.send('Выбор сделан')


async def status_maker(i, mess):
    game_sessions[mess.channel.id].player_status[i][0], game_sessions[mess.channel.id].player_status[i][4] = 1, -1
    if game_sessions[mess.channel.id].player_roles[i] == '4':
        game_sessions[mess.channel.id].player_status[i][2] = 3
        game_sessions[mess.channel.id].police.append(i)
    elif game_sessions[mess.channel.id].player_roles[i] == '11':
        game_sessions[mess.channel.id].player_status[i][2] = 2
        game_sessions[mess.channel.id].police.append(i)
    else:
        game_sessions[mess.channel.id].player_status[i][2] = 0
    if game_sessions[mess.channel.id].player_roles[i] == '2':
        game_sessions[mess.channel.id].player_status[i][3] = 4
        game_sessions[mess.channel.id].mafia.append(i)
    elif game_sessions[mess.channel.id].player_roles[i] == '3':
        game_sessions[mess.channel.id].player_status[i][3] = 5
        game_sessions[mess.channel.id].mafia.append(i)
    elif game_sessions[mess.channel.id].player_roles[i] == '12':
        game_sessions[mess.channel.id].player_status[i][3] = 3
        game_sessions[mess.channel.id].mafia.append(i)
    elif game_sessions[mess.channel.id].player_roles[i] == '9':
        game_sessions[mess.channel.id].player_status[i][3] = 1
        game_sessions[mess.channel.id].mafia.append(i)
    else:
        game_sessions[mess.channel.id].player_status[i][3] = 0


async def night_echo(mess):
    if game_sessions[night_ids[mess.channel.id]].player_status[mess.author][2] > 1 and game_sessions[night_ids[mess.channel.id]].player_status[mess.author][1] == 0:
        for member in game_sessions[night_ids[mess.channel.id]].police:
            if member != mess.author and game_sessions[night_ids[mess.channel.id]].player_status[member][2] > 0 and game_sessions[night_ids[mess.channel.id]].player_status[member][1] == 0:
                await member.send(str(mess.author)[:-5] + ': ' + mess.content)
    elif game_sessions[night_ids[mess.channel.id]].player_status[mess.author][3] > 2 and game_sessions[night_ids[mess.channel.id]].player_status[mess.author][1] == 0:
        for member in game_sessions[night_ids[mess.channel.id]].mafia:
            if member != mess.author and game_sessions[night_ids[mess.channel.id]].player_status[member][3] > 1 and game_sessions[night_ids[mess.channel.id]].player_status[member][1] == 0:
                await member.send(str(mess.author)[:-5] + ': ' + mess.content)


async def after_game(mess):
    sd = ''
    ft = ''
    i = 0
    for member in game_sessions[mess.channel.id].player_roles:
        del night_ids[member.dm_channel.id]
        i += 1
        x = str(roles_definition[int(game_sessions[mess.channel.id].player_roles[member])])
        if x == 'Мирный_житель':
            x = 'Мирный житель'
        ft += str(i) + ') ' + str(member)[:-5] + '\n'
        sd += str(i) + ') ' + x + '\n'
    emb = discord.Embed(title='Роли игроков:', colour= discord.Color.from_rgb(255, 150, 31))
    emb.add_field(name='Игрок', value=ft, inline=True)
    emb.add_field(name='Роль', value=sd, inline=True)
    await mess.channel.send(embed=emb)


async def preparation_of_results(mode, message):
    if message.channel.guild.id == 713353831706263573:
        if 'Комната' in message.channel.name:
            for role in message.channel.guild.roles:
                if role.name == 'game_room_' + message.channel.name[-1]:
                    break
        for member in game_sessions[message.channel.id].player_status:
            await member.remove_roles(role)
        if mode == 1:
            if game_sessions[message.channel.id].player_roles[member] == '6':
                game_sessions[message.channel.id].gamers[str(member.id)] = [1, roles_multiplier[int(game_sessions[message.channel.id].player_roles[member])-1], game_sessions[message.channel.id].player_status[member][0], roles_definition[int(game_sessions[message.channel.id].player_roles[member])]]
            else:
                game_sessions[message.channel.id].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel.id].player_roles[member]) - 1], game_sessions[message.channel.id].player_status[member][0], roles_definition[int(game_sessions[message.channel.id].player_roles[member])]]
        elif mode == 2:
            if int(game_sessions[message.channel.id].player_roles[member]) in [2, 3, 9, 10, 12]:
                game_sessions[message.channel.id].gamers[str(member.id)] = [1, roles_multiplier[int(game_sessions[message.channel.id].player_roles[member])-1], game_sessions[message.channel.id].player_status[member][0], roles_definition[int(game_sessions[message.channel.id].player_roles[member])]]
            else:
                game_sessions[message.channel.id].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel.id].player_roles[member]) - 1], game_sessions[message.channel.id].player_status[member][0], roles_definition[int(game_sessions[message.channel.id].player_roles[member])]]
        elif mode == 3:
            if int(game_sessions[message.channel.id].player_roles[member]) in [1, 4, 5, 7, 8, 11]:
                game_sessions[message.channel.id].gamers[str(member.id)] = [1, roles_multiplier[int(game_sessions[message.channel.id].player_roles[member]) - 1], game_sessions[message.channel.id].player_status[member][0], roles_definition[int(game_sessions[message.channel.id].player_roles[member])]]
            else:
                game_sessions[message.channel.id].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel.id].player_roles[member]) - 1], game_sessions[message.channel.id].player_status[member][0], roles_definition[int(game_sessions[message.channel.id].player_roles[member])]]
        else:
            game_sessions[message.channel.id].gamers[str(member.id)] = [0, roles_multiplier[int(game_sessions[message.channel.id].player_roles[member]) - 1], game_sessions[message.channel.id].player_status[member][0], roles_definition[int(game_sessions[message.channel.id].player_roles[member])]]
    endgame(game_sessions[message.channel.id].gamers, game_sessions[message.channel.id].game_mode)


async def win_condition(message):
    if game_sessions[message.channel.id].maniac > 0 and game_sessions[message.channel.id].red + game_sessions[message.channel.id].black + game_sessions[message.channel.id].two_faced == 0:
        await blank_message(1, message.channel)
        await message.channel.send('Игра окончена! Победа маньяка 🔪')
        await preparation_of_results(1, message)
        await after_game(message)
        return True
    elif game_sessions[message.channel.id].maniac == 0 and ((game_sessions[message.channel.id].black >= game_sessions[message.channel.id].red and game_sessions[message.channel.id].black > 0) or (game_sessions[message.channel.id].red + game_sessions[message.channel.id].black == 0 and game_sessions[message.channel.id].two_faced > 0)):
        await blank_message(1, message.channel)
        await message.channel.send('Игра окончена! Победа мафии 🕵️')
        await preparation_of_results(2, message)
        await after_game(message)
        return True
    elif game_sessions[message.channel.id].maniac == 0 and game_sessions[message.channel.id].black == 0 and game_sessions[message.channel.id].red > 0:
        await blank_message(1, message.channel)
        await message.channel.send('Игра окончена! Победа мирного города 👥')
        await preparation_of_results(3, message)
        await after_game(message)
        return True
    elif game_sessions[message.channel.id].maniac + game_sessions[message.channel.id].black + game_sessions[message.channel.id].two_faced + game_sessions[message.channel.id].red == 0:
        await blank_message(1, message.channel)
        await message.channel.send('Игра окончена! Ничья. В городе не осталось живых 💀')
        await preparation_of_results(4, message)
        await after_game(message)
        return True


async def reduction_role_condition(i, mess):
    if int(game_sessions[mess.channel.id].player_roles[game_sessions[mess.channel.id].members[i]]) in [2, 3, 10, 12]:
        game_sessions[mess.channel.id].black -= 1
    elif int(game_sessions[mess.channel.id].player_roles[game_sessions[mess.channel.id].members[i]]) == 6:
        game_sessions[mess.channel.id].maniac -= 1
    elif int(game_sessions[mess.channel.id].player_roles[game_sessions[mess.channel.id].members[i]]) == 9:
        game_sessions[mess.channel.id].two_faced -= 1
    else:
        game_sessions[mess.channel.id].red -= 1
    game_sessions[mess.channel.id].player_status[game_sessions[mess.channel.id].members[i]][0] = 0


async def timer(time,mess,member,vt):
    if vt == 0:
        message = await mess.channel.send('Ваш ход ' + str(member)[:-5] + ' (Нажми ⛔, чтобы закончить свой ход)')
        time_message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
        await time_message.add_reaction('⛔')
        for i in range(time - 1, -1, -1):
            if game_sessions[mess.channel.id].checker == 1:
                break
            await asyncio.sleep(1)
            await time_message.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
        try:
            await time_message.delete()
        except:
            pass
        try:
            await message.delete()
        except:
            pass
    elif vt == 1 or vt == 2:
        if vt == 1:
            message = await mess.channel.send('Кто голосует за игрока  ' + str(member)[:-5]+'?' + ' (Нажми ✅, чтобы проголосовать против игрока)')
            time_message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
            await time_message.add_reaction('✅')
        elif vt == 2:
            time_message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
            await time_message.add_reaction('✅')
            await time_message.add_reaction('⛔')
        for i in range(time - 1, -1, -1):
            await asyncio.sleep(1)
            await time_message.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
        try:
            await time_message.delete()
        except:
            pass
        try:
            await message.delete()
        except:
            pass
    elif vt == 3:
        time_message_1 = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
        mafia_time = []
        for i in member:
            if game_sessions[mess.channel.id].player_status[i][0] != 0:
                time_message_2 = await i.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
                mafia_time.append(time_message_2)
        for i in range(time - 1, -1, -1):
            await asyncio.sleep(1)
            await time_message_1.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
            for j in mafia_time:
                await j.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
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
    if reaction.message.channel.id in list(game_sessions.keys()):
        if reaction.emoji == '⛔' and user == game_sessions[reaction.message.channel.id].right and game_sessions[reaction.message.channel.id].vn == 0:
            game_sessions[reaction.message.channel.id].checker = 1
        elif reaction.emoji == '⛔' and user != reaction.message.author and game_sessions[reaction.message.channel.id].vn == 3 and user in game_sessions[reaction.message.channel.id].members:
            if game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] == 0 and game_sessions[reaction.message.channel.id].player_status[user][0] != 0:
                game_sessions[reaction.message.channel.id].count -= 1
                game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] = 1
        elif reaction.emoji == '✅' and user != reaction.message.author and game_sessions[reaction.message.channel.id].vn == 1 and user in game_sessions[reaction.message.channel.id].members:
            if game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] == 0 and game_sessions[reaction.message.channel.id].player_status[user][0] != 0:
                game_sessions[reaction.message.channel.id].votes[game_sessions[reaction.message.channel.id].members.index(game_sessions[reaction.message.channel.id].gl)] += 1
                game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] = 1
        elif reaction.emoji == '✅' and user != reaction.message.author and game_sessions[reaction.message.channel.id].vn == 2 and user in game_sessions[reaction.message.channel.id].members:
            if game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] == 0 and game_sessions[reaction.message.channel.id].player_status[user][0] != 0:
                game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] = 1
                game_sessions[reaction.message.channel.id].guilty[game_sessions[reaction.message.channel.id].ind] += 1
        elif reaction.emoji == '✅' and user != reaction.message.author and game_sessions[reaction.message.channel.id].vn == 3 and user in game_sessions[reaction.message.channel.id].members:
            if game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] == 0 and game_sessions[reaction.message.channel.id].player_status[user][0] != 0:
                game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] = 1
                game_sessions[reaction.message.channel.id].count += 1
        elif reaction.emoji == '💤' and user != reaction.message.author and user in game_sessions[reaction.message.channel.id].members:
            if game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] == 0 and game_sessions[reaction.message.channel.id].player_status[user][0] != 0:
                game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] = 1
                game_sessions[reaction.message.channel.id].count -= 1
                if game_sessions[reaction.message.channel.id].count == 0:
                    await reaction.message.delete()
                    for i in range(len(game_sessions[reaction.message.channel.id].members)):
                        try:
                            await game_sessions[reaction.message.channel.id].members[i].edit(
                                nick=(str(i + 1) + '. ' + str(game_sessions[reaction.message.channel.id].members[i])[:-5]))
                        except:
                            pass
                    await reaction.message.channel.send('Наступает ночь 🌃 (Просьба игрокам с активными ролями перейти в личные сообщения с ботом)')
                else:
                    await reaction.message.remove_reaction('💤', user)
                    x = user.nick[0:2]
                    if x != user.name[0:2]:
                        await user.edit(nick=x + user.name + '😴')
                    del x
        elif reaction.emoji == '⏰' and user != reaction.message.author and user in game_sessions[reaction.message.channel.id].members:
            if game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] == 0 and game_sessions[reaction.message.channel.id].player_status[user][0] != 0:
                game_sessions[reaction.message.channel.id].already[game_sessions[reaction.message.channel.id].members.index(user)] = 1
                game_sessions[reaction.message.channel.id].count -= 1
                if game_sessions[reaction.message.channel.id].count == 0:
                    await reaction.message.delete()
                    for i in range(len(game_sessions[reaction.message.channel.id].members)):
                        try:
                            await game_sessions[reaction.message.channel.id].members[i].edit(
                                nick=(str(i + 1) + '. ' + str(game_sessions[reaction.message.channel.id].members[i])[:-5]))
                        except:
                            pass
                    await reaction.message.channel.send('Наступает день 🌇')
                else:
                    await reaction.message.remove_reaction('⏰', user)
                    x = user.nick[0:2]
                    if x != user.name[0:2]:
                        await user.edit(nick=x + user.name + '🙂')
                    del x
        elif reaction.emoji == '✅' and user != reaction.message.author and game_sessions[
            reaction.message.channel.id].vn == 5 and user in game_sessions[reaction.message.channel.id].members:
            game_sessions[reaction.message.channel.id].already[
                game_sessions[reaction.message.channel.id].members.index(user)] = 1
            try:
                await user.edit(nick=user.name + ' ✅')
            except:
                pass
            if sum(list(game_sessions[reaction.message.channel.id].already.values())) == len(game_sessions[reaction.message.channel.id].members):
                await reaction.message.delete()
                await user_rename(reaction.message)
                await blank_message(1, reaction.message.channel)
                await reaction.message.channel.send('💠 **ИГРА НАЧАЛАСЬ** 💠')
                game_sessions[reaction.message.channel.id].running = True
            else:
                await reaction.message.remove_reaction('✅', user)
        elif reaction.emoji == '❌' and user != reaction.message.author and game_sessions[
            reaction.message.channel.id].vn == 5 and user in game_sessions[reaction.message.channel.id].members:
            game_sessions[reaction.message.channel.id].already[
                game_sessions[reaction.message.channel.id].members.index(user)] = 0
            try:
                await user.edit(nick=user.name + ' ❌')
            except:
                pass
            await reaction.message.remove_reaction('❌', user)
        elif reaction.emoji == '1️⃣' and user != reaction.message.author and game_sessions[
            reaction.message.channel.id].vn == 6 and game_sessions[reaction.message.channel.id].right == user:
            game_sessions[reaction.message.channel.id].vn = -1
            game_sessions[reaction.message.channel.id].right = None
            game_sessions[reaction.message.channel.id].game_settings = {'mode': 'auto', 'mute': 'on', 'time': [60, 45, 15, 60, 40, 90]}
            await reaction.message.delete()
            await genclassic(game_sessions[reaction.message.channel.id].context)
        elif reaction.emoji == '2️⃣' and user != reaction.message.author and game_sessions[
            reaction.message.channel.id].vn == 6 and game_sessions[reaction.message.channel.id].right == user:
            game_sessions[reaction.message.channel.id].vn = -1
            game_sessions[reaction.message.channel.id].right = None
            game_sessions[reaction.message.channel.id].game_mode = 'custom'
            game_sessions[reaction.message.channel.id].game_settings = get_settings(user.id)
            await reaction.message.delete()
            await create(game_sessions[reaction.message.channel.id].context)
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
                change_settings(user.id, setting_sessions[user].setgs)
                await reaction.message.channel.send('Сохранено ✅')
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
async def r(ctx):
    await reset(ctx)


@client.command()
async def st(ctx):
    await settings(ctx)

# SHORTCUTS

@client.command()
async def vote(ctx, choice):
    try:
        if ctx.author.id == game_sessions[ctx.channel.id].right_to_vote.id and type(ctx.channel) != discord.channel.DMChannel:
            try:
                choice = int(choice)
            except:
                return
            if choice > len(game_sessions[ctx.channel.id].members) or choice - 1 < 0:
                await ctx.send('Игрока под номером ' + str(choice) + ' не существует, проголосуйте за другого.')
            elif choice-1 in game_sessions[ctx.channel.id].voted and sum(game_sessions[ctx.channel.id].votes) == 0:
                await ctx.send('Этот игрок уже выставлен на голосование. Выберите другого.')
            elif game_sessions[ctx.channel.id].player_status[game_sessions[ctx.channel.id].members[choice-1]][0] == 0:
                await ctx.send('Этот игрок уже убит. Выберите другого.')
            else:
                game_sessions[ctx.channel.id].vote_choice = choice
                await ctx.send('Принято!')
    except:
        pass

#-----------------Main commands---------------------


async def meeting_day(mess):
    await mess.channel.send('Начинается день знакомств 🤝')
    game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
    game_sessions[mess.channel.id].vn = 0
    game_sessions[mess.channel.id].tumb = 0
    for member in game_sessions[mess.channel.id].members:
        await mute(mess, member)
    for member in game_sessions[mess.channel.id].members:
        game_sessions[mess.channel.id].right = member
        game_sessions[mess.channel.id].checker = 0
        await unmute(mess, member)
        await timer(game_sessions[mess.channel.id].game_settings['time'][0], mess, member, 0)
        await mute(mess, member)
    game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
    ms = await mess.channel.send('Город засыпает 💤 (Выключите камеру и после этого нажмите 💤, чтобы подтвердить готовность к ночи)')
    await ms.add_reaction('💤')
    for i in range(len(game_sessions[mess.channel.id].members)):
        try:
            await game_sessions[mess.channel.id].members[i].edit(
                nick=(str(i + 1) + '. ' + str(game_sessions[mess.channel.id].members[i])[:-5]) + ' 🙂')
        except:
            pass
    game_sessions[mess.channel.id].count = 0
    for i in list(game_sessions[mess.channel.id].player_status.values()):
        if i[0] != 0:
            game_sessions[mess.channel.id].count += 1


async def day(mess):
    if game_sessions[mess.channel.id].killed != []:
        await mess.channel.send('Ночью были убиты игроки под номерами: ' + (', ').join(game_sessions[mess.channel.id].killed))
    else:
        await mess.channel.send('Ночью никто не был убит 🚫')
    game_sessions[mess.channel.id].vn = 0
    for person in game_sessions[mess.channel.id].killed:
        await reduction_role_condition(int(person)-1, mess)
        try:
            await game_sessions[mess.channel.id].members[int(person)-1].edit(
                nick=str(person) + '. ' + str(game_sessions[mess.channel.id].members[int(person)-1])[:-5] + ' 💀')
        except:
            pass
    if await win_condition(mess) == True:
        for member in game_sessions[mess.channel.id].members:
            await unmute(mess, member)
            try:
                await member.edit(nick=member.name)
            except:
                pass
        del game_sessions[mess.channel.id]
        return
    await mess.channel.send('Начинается обсуждение и выставление кандидатур на голосование 🗣️ (Напишите `!vote` *номер_игрока* в свой ход, чтобы выставить его на голосование)')
    game_sessions[mess.channel.id].voted = []
    game_sessions[mess.channel.id].votes = [0 for i in range(len(game_sessions[mess.channel.id].members))]
    game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
    game_sessions[mess.channel.id].guilty.clear()
    game_sessions[mess.channel.id].killed.clear()
    for i in list(game_sessions[mess.channel.id].player_roles.keys()):
        if game_sessions[mess.channel.id].player_status[i][0] != 0:
            game_sessions[mess.channel.id].checker = 0
            game_sessions[mess.channel.id].vote_choice = ''
            member = i
            game_sessions[mess.channel.id].right = member
            game_sessions[mess.channel.id].right_to_vote = member
            await unmute(mess, member)
            await timer(game_sessions[mess.channel.id].game_settings['time'][0], mess, member, 0)
            await mute(mess, member)
            if game_sessions[mess.channel.id].vote_choice == '':
                pass
            elif game_sessions[mess.channel.id].vote_choice - 1 not in game_sessions[mess.channel.id].voted:
                game_sessions[mess.channel.id].voted.append(game_sessions[mess.channel.id].vote_choice - 1)
    game_sessions[mess.channel.id].right_to_vote = None
    if len(game_sessions[mess.channel.id].voted) == 0:
        await mess.channel.send('Было принято решение никого не сажать в тюрьму 🚫')
        game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
        ms = await mess.channel.send('Город засыпает 💤 (Выключите камеру и после этого нажмите 💤, чтобы подтвердить готовность к ночи)')
        await ms.add_reaction('💤')
        for i in range(len(game_sessions[mess.channel.id].members)):
            try:
                await game_sessions[mess.channel.id].members[i].edit(
                    nick=(str(i + 1) + '. ' + str(game_sessions[mess.channel.id].members[i])[:-5]) + ' 🙂')
            except:
                pass
        game_sessions[mess.channel.id].count = 0
        for i in list(game_sessions[mess.channel.id].player_status.values()):
            if i[0] != 0:
                game_sessions[mess.channel.id].count += 1
    else:
        m = []
        for i in range(len(game_sessions[mess.channel.id].voted)):
            m.append(str(game_sessions[mess.channel.id].voted[i] + 1))
        await mess.channel.send('Обвиняются игроки под номерами: ' + (', ').join(m))
        await mess.channel.send('Обвиняемым предоставляется оправдательная речь 👨‍⚖️')
        for i in game_sessions[mess.channel.id].voted:
            game_sessions[mess.channel.id].checker = 0
            member = game_sessions[mess.channel.id].members[i]
            game_sessions[mess.channel.id].right = member
            await unmute(mess, member)
            await timer(game_sessions[mess.channel.id].game_settings['time'][1], mess, member, 0)
            await mute(mess, member)
        await mess.channel.send('Начинается голосование 📢')
        game_sessions[mess.channel.id].tumb = 1
        game_sessions[mess.channel.id].right = None
        game_sessions[mess.channel.id].vn = 1
        for i in game_sessions[mess.channel.id].voted:
            member = game_sessions[mess.channel.id].members[i]
            game_sessions[mess.channel.id].gl = member
            await timer(game_sessions[mess.channel.id].game_settings['time'][2], mess, member, 1)
        for i in list(game_sessions[mess.channel.id].player_roles.keys()):
            if game_sessions[mess.channel.id].player_status[i][0] != 0 and game_sessions[mess.channel.id].already[game_sessions[mess.channel.id].members.index(i)] == 0:
                game_sessions[mess.channel.id].votes[game_sessions[mess.channel.id].voted[-1]] += 1
        await mess.channel.send('Голосование окончено')
        if game_sessions[mess.channel.id].votes.count(max(game_sessions[mess.channel.id].votes)) == 1:
            game_sessions[mess.channel.id].guil = game_sessions[mess.channel.id].votes.index(max(game_sessions[mess.channel.id].votes))
            game_sessions[mess.channel.id].vn = 0
            game_sessions[mess.channel.id].right = game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].guil]
            game_sessions[mess.channel.id].checker = 0
            await mess.channel.send('Приговоренному дается право произнести последнюю речь 👨‍⚖️')
            await unmute(mess, game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].guil])
            await timer(game_sessions[mess.channel.id].game_settings['time'][4], mess, game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].guil], 0)
            await mute(mess, game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].guil])
            await reduction_role_condition(game_sessions[mess.channel.id].guil, mess)
            try:
                await game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].guil].edit(nick=str(game_sessions[mess.channel.id].guil + 1) + '. ' + str(game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].guil])[:-5] + ' 💀')
            except:
                pass
            await mess.channel.send(str(game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].guil])[:-5] + ' был посажен за решетку 👮')
            if await win_condition(mess) == True:
                for member in game_sessions[mess.channel.id].members:
                    await unmute(mess, member)
                    try:
                        await member.edit(nick=member.name)
                    except:
                        pass
                del game_sessions[mess.channel.id]
                return
        else:
            for i in range(len(game_sessions[mess.channel.id].voted)):
                if game_sessions[mess.channel.id].votes[game_sessions[mess.channel.id].voted[i]] == max(game_sessions[mess.channel.id].votes):
                    game_sessions[mess.channel.id].guilty[game_sessions[mess.channel.id].voted[i] + 1] = 0
            await mess.channel.send(
                'Обвиняемым ' + str(game_sessions[mess.channel.id].guilty.keys())[11:-2] + ' предоставляются дополнительные оправдательные речи 👨‍⚖️')
            game_sessions[mess.channel.id].guilty.clear()
            game_sessions[mess.channel.id].right = None
            game_sessions[mess.channel.id].vn = 0
            for i in range(len(game_sessions[mess.channel.id].voted)):
                if game_sessions[mess.channel.id].votes[game_sessions[mess.channel.id].voted[i]] == max(game_sessions[mess.channel.id].votes):
                    game_sessions[mess.channel.id].checker = 0
                    game_sessions[mess.channel.id].guilty[game_sessions[mess.channel.id].voted[i]] = 0
                    member = game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].voted[i]]
                    game_sessions[mess.channel.id].right = member
                    await unmute(mess, member)
                    await timer(game_sessions[mess.channel.id].game_settings['time'][0], mess, member, 0)
                    await mute(mess, member)
            await mess.channel.send('Начинается повторное голосование 📢')
            game_sessions[mess.channel.id].right = None
            game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
            for i in range(len(game_sessions[mess.channel.id].guilty)):
                game_sessions[mess.channel.id].vn = 2
                member = game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys())[i]]
                game_sessions[mess.channel.id].ind = list(game_sessions[mess.channel.id].guilty.keys())[i]
                await timer(game_sessions[mess.channel.id].game_settings['time'][2], mess, member, 1)
            for i in list(game_sessions[mess.channel.id].player_roles.keys()):
                if game_sessions[mess.channel.id].player_status[i][0] != 0 and game_sessions[mess.channel.id].already[game_sessions[mess.channel.id].members.index(i)] == 0:
                    game_sessions[mess.channel.id].guilty[list(game_sessions[mess.channel.id].guilty.keys())[-1]] += 1
            if list(game_sessions[mess.channel.id].guilty.values()).count(max(game_sessions[mess.channel.id].guilty.values())) == 1:
                game_sessions[mess.channel.id].vn = 0
                for i in list(game_sessions[mess.channel.id].guilty.keys()):
                    if game_sessions[mess.channel.id].guilty[i] == max(game_sessions[mess.channel.id].guilty.values()):
                        game_sessions[mess.channel.id].checker = 0
                        game_sessions[mess.channel.id].right = members[list(guilty.keys())[i]]
                        await mess.channel.send('Приговоренному дается право произнести последнюю речь 👨‍⚖️')
                        await unmute(mess, game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys())[i]])
                        await timer(game_sessions[mess.channel.id].game_settings['time'][3], mess, game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys())[i]], 0)
                        await mute(mess, game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys())[i]])
                        try:
                            await game_sessions[mess.channel.id].members[i].edit(nick=str(i + 1) + '. ' + str(game_sessions[mess.channel.id].members[i])[:-5] + ' 💀')
                        except:
                            pass
                            await mess.channel.send(str(game_sessions[mess.channel.id].members[i])[:-5] + ' был посажен за решетку 👮')
                        break
                if await win_condition(mess) == True:
                    for member in game_sessions[mess.channel.id].members:
                        await unmute(mess, member)
                        try:
                            await member.edit(nick=member.name)
                        except:
                            pass
                    del game_sessions[mess.channel.id]
                    return
            else:
                for i in list(game_sessions[mess.channel.id].guilty.keys()):
                    if game_sessions[mess.channel.id].guilty[i] != max(game_sessions[mess.channel.id].guilty.values()):
                        del game_sessions[mess.channel.id].guilty[i]
                await mess.channel.send(
                    'По-прежнему остались игроки с одинаковым количеством голосов, поэтому принимается решение: выгнать или оставить всех\nНажмите ✅, если голосуете за \"выгнать\", Нажмите ⛔, если голосуете за \"оставить\"')
                game_sessions[mess.channel.id].count = 0
                game_sessions[mess.channel.id].vn = 3
                game_sessions[mess.channel.id].right = None
                game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
                game_sessions[mess.channel.id].checker = 0
                await timer(game_sessions[mess.channel.id].game_settings['time'][2], mess, member, 2)
                for i in list(game_sessions[mess.channel.id].player_roles.keys()):
                    if game_sessions[mess.channel.id].player_status[i][0] != 0 and game_sessions[mess.channel.id].already[game_sessions[mess.channel.id].members.index(i)] == 0:
                        game_sessions[mess.channel.id].count -= 1
                if game_sessions[mess.channel.id].count > 0:
                    await mess.channel.send('Приговоренным дается право произнести последнюю речь 👨‍⚖️')
                    game_sessions[mess.channel.id].vn = 0
                    for i in list(game_sessions[mess.channel.id].guilty.keys()):
                        game_sessions[mess.channel.id].checker = 0
                        game_sessions[mess.channel.id].right = game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys()).index(i)]
                        await unmute(mess, game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys()).index(i)])
                        await timer(game_sessions[mess.channel.id].game_settings['time'][2], mess, game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys()).index(i)], 0)
                        await mute(mess, game_sessions[mess.channel.id].members[list(game_sessions[mess.channel.id].guilty.keys()).index(i)])
                        await reduction_role_condition(i, mess)
                        try:
                            await game_sessions[mess.channel.id].members[i].edit(nick=str(i + 1) + '. ' + str(game_sessions[mess.channel.id].members[i])[:-5] + ' 💀')
                        except:
                            pass
                        await mess.channel.send(str(game_sessions[mess.channel.id].members[i])[:-5] + ' был посажен за решетку 👮')
                    if await win_condition(mess) == True:
                        for member in game_sessions[mess.channel.id].members:
                            await unmute(mess, member)
                            try:
                                await member.edit(nick=member.name)
                            except:
                                pass
                        del game_sessions[mess.channel.id]
                        return
                else:
                    await mess.channel.send('Было принято решение никого не сажать в тюрьму 🚫')
        game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
        ms = await mess.channel.send('Город засыпает 💤 (Выключите камеру и после этого нажмите 💤, чтобы подтвердить готовность к ночи)')
        await ms.add_reaction('💤')
        for i in range(len(game_sessions[mess.channel.id].members)):
            try:
                await game_sessions[mess.channel.id].members[i].edit(
                    nick=(str(i + 1) + '. ' + str(game_sessions[mess.channel.id].members[i])[:-5]) + ' 🙂')
            except:
                pass
        game_sessions[mess.channel.id].count = 0
        for i in list(game_sessions[mess.channel.id].player_status.values()):
            if i[0] != 0:
                game_sessions[mess.channel.id].count += 1


async def night(mess):
    game_sessions[mess.channel.id].vn = -1
    for member in game_sessions[mess.channel.id].player_roles:
        if game_sessions[mess.channel.id].player_status[member][2] > 1 and game_sessions[mess.channel.id].player_status[member][0] == 0:
            game_sessions[mess.channel.id].player_status[member][2] = 1
        elif game_sessions[mess.channel.id].player_status[member][3] > 2 and game_sessions[mess.channel.id].player_status[member][0] == 0:
            game_sessions[mess.channel.id].player_status[member][3] = 2
        game_sessions[mess.channel.id].player_status[member][1] = 0
        game_sessions[mess.channel.id].player_status[member][5] = 0
        if game_sessions[mess.channel.id].player_roles[member] == '9':
            if game_sessions[mess.channel.id].player_status[member][4] != -1 and game_sessions[mess.channel.id].members[game_sessions[mess.channel.id].player_status[member][4]] in game_sessions[mess.channel.id].mafia:
                game_sessions[mess.channel.id].player_status[member][3] = 6
                game_sessions[mess.channel.id].two_faced -= 1
                game_sessions[mess.channel.id].black += 1
        elif game_sessions[mess.channel.id].player_roles[member] == '11':
            for j in game_sessions[mess.channel.id].player_roles:
                if game_sessions[mess.channel.id].player_roles[j] == '4' and game_sessions[mess.channel.id].player_status[j][0] == 0:
                    game_sessions[mess.channel.id].player_status[member][2] = 3
        elif game_sessions[mess.channel.id].player_roles[member] == '12':
            count = 0
            for j in game_sessions[mess.channel.id].player_roles:
                if int(game_sessions[mess.channel.id].player_roles[j]) in [2, 3] and game_sessions[mess.channel.id].player_status[j][0] == 1:
                    count += 1
            if count == 0:
                game_sessions[mess.channel.id].player_status[member][3] = 6
            del count
    for i in range(len(sequence)):
        if type(sequence[i]) == int:
            for j in list(game_sessions[mess.channel.id].player_roles.keys()):
                if int(game_sessions[mess.channel.id].player_roles[j]) == sequence[i]:
                    if game_sessions[mess.channel.id].player_status[j][0] != 0 and game_sessions[mess.channel.id].player_status[j][1] == 0:
                        game_sessions[mess.channel.id].right_to_act = [j]
                        await j.send('⚠️ **ВАШ ХОД** ⚠️')
                        await j.send('Чтобы выбрать цель для вашего ход, напишите `!action` *номер_игрока*')
                    elif game_sessions[mess.channel.id].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    if i != 3:
                        await timer(game_sessions[mess.channel.id].game_settings['time'][4], mess, [j], 3)
                    elif i == 3:
                        game_sessions[mess.channel.id].right_to_chat = game_sessions[mess.channel.id].mafia.copy()
                        await timer(game_sessions[mess.channel.id].game_settings['time'][4], mess, [j], 3)
                        if game_sessions[mess.channel.id].don_phase == 1 and game_sessions[mess.channel.id].player_status[j][0] != 0 and game_sessions[mess.channel.id].player_status[j][1] == 0 and vote_results.count(max(vote_results)) == 1 and sum(vote_results) != 0:
                            game_sessions[mess.channel.id].killed.append(str(vote_results.index(max(vote_results))+1))
                    game_sessions[mess.channel.id].right_to_act.clear()
                    game_sessions[mess.channel.id].right_to_chat.clear()
        elif type(sequence[i]) == list and i == 4:
            game_sessions[mess.channel.id].right_to_chat = game_sessions[mess.channel.id].police.copy()
            for j in list(game_sessions[mess.channel.id].player_roles.keys()):
                if int(game_sessions[mess.channel.id].player_roles[j]) == 4 and game_sessions[mess.channel.id].player_status[j][0] != 0:
                    if game_sessions[mess.channel.id].player_status[j][1] == 0:
                        game_sessions[mess.channel.id].right_to_act = [j]
                        await j.send('⚠️ **ВАШ ХОД** ⚠️')
                        await j.send('Чтобы выбрать цель для вашего ход, напишите `!action` *номер_игрока*')
                    elif game_sessions[mess.channel.id].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    await timer(game_sessions[mess.channel.id].game_settings['time'][4], mess, [j], 3)
                    game_sessions[mess.channel.id].right_to_act.clear()
                    break
                elif int(game_sessions[mess.channel.id].player_roles[j]) == 11 and game_sessions[mess.channel.id].player_status[j][0] != 0:
                    if game_sessions[mess.channel.id].player_status[j][1] == 0:
                        game_sessions[mess.channel.id].right_to_act = [j]
                        await j.send('⚠️ **ВАШ ХОД** ⚠️')
                        await j.send('Чтобы выбрать цель для вашего ход, напишите `!action` *номер_игрока*')
                    elif game_sessions[mess.channel.id].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                    await mess.channel.send('Ход ' + sequence_guild_message[i])
                    await timer(game_sessions[mess.channel.id].game_settings['time'][4], mess, [j], 3)
                    game_sessions[mess.channel.id].right_to_act.clear()
                    break
            game_sessions[mess.channel.id].right_to_chat.clear()
        elif type(sequence[i]) == list and i == 2:
            game_sessions[mess.channel.id].right_to_chat = game_sessions[mess.channel.id].mafia.copy()
            game_sessions[mess.channel.id].right_to_act = []
            game_sessions[mess.channel.id].mafia_vote = []
            for j in list(game_sessions[mess.channel.id].player_roles.keys()):
                if int(game_sessions[mess.channel.id].player_roles[j]) == 9 and game_sessions[mess.channel.id].player_status[j][0] != 0:
                    if game_sessions[mess.channel.id].player_status[j][1] == 0:
                        game_sessions[mess.channel.id].right_to_act.append(j)
                        await j.send('⚠️ **ВАШ ХОД** ⚠️')
                        await j.send('Чтобы выбрать цель для вашего ход, напишите `!action` *номер_игрока*')
                    elif game_sessions[mess.channel.id].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                elif int(game_sessions[mess.channel.id].player_roles[j]) == 12 and game_sessions[mess.channel.id].player_status[j][0] != 0:
                    count = 0
                    for member in list(game_sessions[mess.channel.id].player_roles.keys()):
                        if int(game_sessions[mess.channel.id].player_roles[member]) in [2, 3] and game_sessions[mess.channel.id].player_status[member][0] != 0:
                            count += 1
                    if game_sessions[mess.channel.id].player_status[j][1] == 0 and count == 0:
                        game_sessions[mess.channel.id].right_to_act.append(j)
                        await j.send('⚠️ **ВАШ ХОД** ⚠️')
                        await j.send('Чтобы выбрать цель для вашего ход, напишите `!action` *номер_игрока*')
                    elif game_sessions[mess.channel.id].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
                elif int(game_sessions[mess.channel.id].player_roles[j]) == 2 and game_sessions[mess.channel.id].player_status[j][0] != 0:
                    if game_sessions[mess.channel.id].player_status[j][1] == 0:
                        game_sessions[mess.channel.id].right_to_act.append(j)
                        await j.send('⚠️ **ВАШ ХОД** ⚠️')
                        await j.send('Чтобы выбрать цель для вашего ход, напишите `!action` *номер_игрока*')
                    elif game_sessions[mess.channel.id].player_status[j][1] in [1, 2]:
                        await j.send('Вас лишили хода!')
            k = list(game_sessions[mess.channel.id].player_roles.values())
            if k.count('2')+k.count('9')+k.count('12') != 0:
                await mess.channel.send('Ход ' + sequence_guild_message[i])
                await timer(game_sessions[mess.channel.id].game_settings['time'][5], mess, game_sessions[mess.channel.id].right_to_act, 3)
            game_sessions[mess.channel.id].right_to_act.clear()
            vote_results = []
            for j in range(1, len(game_sessions[mess.channel.id].members)+1):
                vote_results.append(game_sessions[mess.channel.id].mafia_vote.count(str(j)))
            for j in list(game_sessions[mess.channel.id].player_roles.keys()):
                if game_sessions[mess.channel.id].player_roles[j] == '3' and game_sessions[mess.channel.id].player_status[j][0] != 0 and game_sessions[mess.channel.id].player_status[j][1] == 0:
                    game_sessions[mess.channel.id].right_to_act = [j]
                    if sum(vote_results) != 0:
                        for l in range(len(vote_results)):
                            if vote_results[l] != 0:
                                await j.send(str(vote_results[l]) + ' проголосовал(-о) за убийство игрока под номером ' + str(l+1))
                    else:
                        await j.send('Мафия не выбрала ни одной цели для убийства')
                elif game_sessions[mess.channel.id].player_roles[j] == '3' and (game_sessions[mess.channel.id].player_status[j][0] == 0 or game_sessions[mess.channel.id].player_status[j][1] != 0) or list(game_sessions[mess.channel.id].player_roles.values()).count('3') == 0:
                    if sum(vote_results) != 0:
                        k = vote_results.index(max(vote_results))
                        if vote_results.count(max(vote_results)) == 1 and game_sessions[mess.channel.id].player_roles[game_sessions[mess.channel.id].members[k]] != '8' and game_sessions[mess.channel.id].player_status[game_sessions[mess.channel.id].members[k]][1] != 2:
                            game_sessions[mess.channel.id].killed.append(str(k+1))
            game_sessions[mess.channel.id].don_phase = 1
        game_sessions[mess.channel.id].killed = list(set(game_sessions[mess.channel.id].killed))
        game_sessions[mess.channel.id].killed.sort()

    for i in game_sessions[mess.channel.id].killed:
        try:
            game_sessions[mess.channel.id].player_status[game_sessions[mess.channel.id].members[int(i)-1]][0] = 0
        except:
            pass
    game_sessions[mess.channel.id].already = [0 for i in range(len(game_sessions[mess.channel.id].members))]
    ms = await mess.channel.send('Город просыпается ⏰ (Включите камеру и после этого нажмите ⏰, чтобы подтвердить готовность ко дню)')
    await ms.add_reaction('⏰')
    for i in range(len(game_sessions[mess.channel.id].members)):
        try:
            await game_sessions[mess.channel.id].members[i].edit(
                nick=(str(i + 1) + '. ' + str(game_sessions[mess.channel.id].members[i])[:-5]) + ' 😴')
        except:
            pass
    game_sessions[mess.channel.id].right_to_act.clear()
    game_sessions[mess.channel.id].count = 0

    for i in list(game_sessions[mess.channel.id].player_status.values()):
        if i[0] != 0:
            game_sessions[mess.channel.id].count += 1
    if game_sessions[mess.channel.id].count == 0:
        await ms.delete()
        await mess.channel.send('Наступает день 🌇')

async def genclassic(ctx):
    if type(ctx.channel) != discord.channel.DMChannel:
        game_sessions[ctx.channel.id].roles_num = roles_num_b.copy()
        game_sessions[ctx.channel.id].members = ctx.message.author.voice.channel.members
        amount = len(game_sessions[ctx.channel.id].members)
        if amount > 3 and amount < 11:
                game_sessions[ctx.channel.id].roles_num['2'], game_sessions[ctx.channel.id].roles_num['3'], game_sessions[ctx.channel.id].roles_num['4'] = amount//3 - 1, 1, 1
                game_sessions[ctx.channel.id].roles_num['1'] = amount - sum(list(game_sessions[ctx.channel.id].roles_num.values()))
                await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" +
                               "Мирных жителей: " + str(game_sessions[ctx.channel.id].roles_num['1']) + "\n" +
                               "Мафий: " + str(game_sessions[ctx.channel.id].roles_num['2']) + "\n" +
                               "Донов мафии: " + str(game_sessions[ctx.channel.id].roles_num['3']) + "\n" +
                               "Комиссаров: " + str(game_sessions[ctx.channel.id].roles_num['4']))
        else:
            await ctx.send('Классический режим доступен для игры при команде от 3 до 10 игроков')
            del game_sessions[ctx.channel.id]
            return
        await game_initialize(ctx)


@client.command()
async def settings(ctx):
    if ctx.channel.id not in list(game_sessions.keys()):
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
async def sets(ctx):
    if ctx.channel.id not in list(game_sessions.keys()):
        pass
    elif game_sessions[ctx.channel.id].running == False:
        pass
    else:
        return
    x = get_all_sets(ctx.author.id)
    if x == {}:
        await ctx.send('На данный момент вы не сохранили ни одного списка ролей')
        return
    counter = 1
    for i in list(x.keys()):
        text = ''
        for j in list(x[i].keys()):
            if j == '1':
                text += 'Мирный житель' + ': ' + str(x[i][j]) + ', '
            else:
                if j == '12':
                    text += roles_definition[int(j)] + ': ' + str(x[i][j])
                else:
                    text += roles_definition[int(j)] + ': ' + str(x[i][j]) + ', '
        await ctx.send(str(counter) + '. ' + i + ' ( ' + text + ' )')
        counter += 1


@client.command()
async def reset(ctx):
    if ctx.channel.id in list(game_sessions.keys()):
        if game_sessions[ctx.channel.id].running == True:
            return
        try:
            await game_sessions[ctx.channel.id].context.delete()
        except:
            pass
        for member in game_sessions[ctx.channel.id].members:
            try:
                await member.edit(nick=member.name)
            except:
                pass
        del game_sessions[ctx.channel.id]
        await ctx.send('Список обнулен')
    else:
        await ctx.send('Список не задан')


async def add_role(num, ctx, message):
    await pool(ctx, message)
    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    response = await ctx.bot.wait_for('message', check=check)
    try:
        request = response.content
        if request == '!reset':
            return True
        if int(request[:request.find(' ')]) not in [1, 2]:
            if game_sessions[ctx.channel.id].roles_num[request[:request.find(' ')]]+int(request[request.find(' ')+1:]) > 1:
                await ctx.send('Такой персонаж может быть только один')
                if await add_role(num, ctx, message) == True:
                    return True
            else:
                game_sessions[ctx.channel.id].roles_num[request[:request.find(' ')]] += int(request[request.find(' ')+1:])
                if num - int(request[request.find(' ') + 1:]) > 0:
                    if await add_role(num - int(request[request.find(' ') + 1:]), ctx, message) == True:
                        return True
        else:
            if int(request[request.find(' ')+1:]) <= num:
                game_sessions[ctx.channel.id].roles_num[request[:request.find(' ')]] += int(request[request.find(' ')+1:])
                if num - int(request[request.find(' ') + 1:]) > 0:
                    if await add_role(num - int(request[request.find(' ') + 1:]), ctx, message) == True:
                        return True
            else:
                await ctx.send('Количество ролей превышает количество игроков. Попробуйте снова.')
                if await add_role(num, ctx, message) == True:
                    return True
        await pool(ctx, message)
    except:
        if await add_role(num, ctx, message) == True:
            return True


async def create(ctx):
    try:
        x = ctx.message.author.voice.channel
    except AttributeError:
        await ctx.send("Перед началом удостоверьтесь, все ли желающие подключены к Вашему голосовому каналу, в противном случае не все роли смогут выдаться.\nЕсли всё готово, можно приступать к настройке игровой сессии.")
        return
    if game_sessions[ctx.channel.id].game_settings['mode'] == "non-auto" and type(ctx.channel) != discord.channel.DMChannel:
        game_sessions[ctx.channel.id].roles_num = roles_num_b.copy()

        def check(m):
            return m.author.id == ctx.author.id
        game_sessions[ctx.channel.id].members = ctx.message.author.voice.channel.members
        for member in game_sessions[ctx.channel.id].members:
            if member.bot:
                game_sessions[ctx.channel.id].members.remove(member)
        await ctx.send("Выберите ведущего.")
        response = await ctx.bot.wait_for('message', check=check)
        if response.content == '!reset':
            return
        for member in game_sessions[ctx.channel.id].members:
            if member.mentioned_in(response):
                emb = discord.Embed(title="Вас назначили ведущим игры.", colour=discord.Color.darker_grey())
                emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713750207623331880/AATXAJxHckd0XbeQRXnekTtsXFQ0vgyIRvtCrntQeQs900-c-k-c0xffffffff-no-rj-mo.png?width=519&height=519")
                await member.send(embed=emb)
                game_master = member
                game_sessions[ctx.channel.id].members.remove(game_master)
                break
        await ctx.send("Задайте роли. Чтобы добавить роль в список напишите `номер_роли количество`, которое хотите добавить (Пример: комбинация 2 1 добавит одну мафию в список)")
        message = await ctx.send("1. Мирных жителей: " + str(game_sessions[ctx.channel.id].roles_num['1']) + "\n" +
                               "2. Мафий: " + str(game_sessions[ctx.channel.id].roles_num['2']) + "\n" +
                               "3. Донов мафии: " + str(game_sessions[ctx.channel.id].roles_num['3']) + "\n" +
                               "4. Комиссаров: " + str(game_sessions[ctx.channel.id].roles_num['4']) + "\n" +
                               "5. Докторов: " + str(game_sessions[ctx.channel.id].roles_num['5']) + "\n" +
                               "6. Маньяков: " + str(game_sessions[ctx.channel.id].roles_num['6']) + "\n" +
                               "7. Куртизанок: " + str(game_sessions[ctx.channel.id].roles_num['7']) + "\n" +
                               "8. Бессмертных: " + str(game_sessions[ctx.channel.id].roles_num['8']) + "\n" +
                               "9. Двуликих: " + str(game_sessions[ctx.channel.id].roles_num['9']) + "\n" +
                               "10. Воров: " + str(game_sessions[ctx.channel.id].roles_num['10']) + "\n" +
                               "11. Сержантов: " + str(game_sessions[ctx.channel.id].roles_num['11']) + "\n" +
                               "12. Оборотней: " + str(game_sessions[ctx.channel.id].roles_num['12']) + "\n\n" +
                               "Оставшихся мест: " + str(len(game_sessions[ctx.channel.id].members) -
                                                         int(sum(list(game_sessions[ctx.channel.id].roles_num.values())))))
        if await add_role(len(game_sessions[ctx.channel.id].members), ctx, message) == True:
            return
        x = "Начало игры. Роли игроков в игре:\n\n"
        rl = ["Мирных жителей: " + str(game_sessions[ctx.channel.id].roles_num['1']) + "\n",
              "Мафий: " + str(game_sessions[ctx.channel.id].roles_num['2']) + "\n",
              "Донов мафии: " + str(game_sessions[ctx.channel.id].roles_num['3']) + "\n",
              "Комиссаров: " + str(game_sessions[ctx.channel.id].roles_num['4']) + "\n",
              "Докторов: " + str(game_sessions[ctx.channel.id].roles_num['5']) + "\n",
              "Маньяков: " + str(game_sessions[ctx.channel.id].roles_num['6']) + "\n",
              "Куртизанок: " + str(game_sessions[ctx.channel.id].roles_num['7']) + "\n",
              "Бессмертных: " + str(game_sessions[ctx.channel.id].roles_num['8']) + "\n",
              "Двуликих: " + str(game_sessions[ctx.channel.id].roles_num['9']) + "\n",
              "Воров: " + str(game_sessions[ctx.channel.id].roles_num['10']) + "\n",
              "Сержантов: " + str(game_sessions[ctx.channel.id].roles_num['11']) + "\n",
              "Оборотней: " + str(game_sessions[ctx.channel.id].roles_num['12'])]
        for i in range(1, 13):
            if game_sessions[ctx.channel.id].roles_num[str(i)] != 0:
                x += rl[i - 1]
        await ctx.send(x)
        await blank_message(1, ctx.channel)
    elif game_sessions[ctx.channel.id].game_settings['mode'] == 'auto' and type(ctx.channel) != discord.channel.DMChannel:
        game_sessions[ctx.channel.id].roles_num = roles_num_b.copy()
        game_sessions[ctx.channel.id].members = ctx.message.author.voice.channel.members
        for member in game_sessions[ctx.channel.id].members:
            if member.bot:
                game_sessions[ctx.channel.id].members.remove(member)
        await ctx.send("Задайте роли. Чтобы добавить роль в список напишите `номер_роли количество`, которое хотите добавить (Пример: комбинация 2 1 добавит одну мафию в список)")
        message = await ctx.send("1. Мирных жителей: " + str(game_sessions[ctx.channel.id].roles_num['1']) + "\n" +
                                 "2. Мафий: " + str(game_sessions[ctx.channel.id].roles_num['2']) + "\n" +
                                 "3. Донов мафии: " + str(game_sessions[ctx.channel.id].roles_num['3']) + "\n" +
                                 "4. Комиссаров: " + str(game_sessions[ctx.channel.id].roles_num['4']) + "\n" +
                                 "5. Докторов: " + str(game_sessions[ctx.channel.id].roles_num['5']) + "\n" +
                                 "6. Маньяков: " + str(game_sessions[ctx.channel.id].roles_num['6']) + "\n" +
                                 "7. Куртизанок: " + str(game_sessions[ctx.channel.id].roles_num['7']) + "\n" +
                                 "8. Бессмертных: " + str(game_sessions[ctx.channel.id].roles_num['8']) + "\n" +
                                 "9. Двуликих: " + str(game_sessions[ctx.channel.id].roles_num['9']) + "\n" +
                                 "10. Воров: " + str(game_sessions[ctx.channel.id].roles_num['10']) + "\n" +
                                 "11. Сержантов: " + str(game_sessions[ctx.channel.id].roles_num['11']) + "\n" +
                                 "12. Оборотней: " + str(game_sessions[ctx.channel.id].roles_num['12']) + "\n\n" +
                                 "Оставшихся мест: " + str(len(game_sessions[ctx.channel.id].members) -
                                                           int(sum(list(
                                                               game_sessions[ctx.channel.id].roles_num.values())))))
        if await add_role(len(game_sessions[ctx.channel.id].members), ctx, message) == True:
            return
        x = "Начало игры. Роли игроков в игре:\n\n"
        rl = ["Мирных жителей: " + str(game_sessions[ctx.channel.id].roles_num['1']) + "\n",
              "Мафий: " + str(game_sessions[ctx.channel.id].roles_num['2']) + "\n",
              "Донов мафии: " + str(game_sessions[ctx.channel.id].roles_num['3']) + "\n",
              "Комиссаров: " + str(game_sessions[ctx.channel.id].roles_num['4']) + "\n",
              "Докторов: " + str(game_sessions[ctx.channel.id].roles_num['5']) + "\n",
              "Маньяков: " + str(game_sessions[ctx.channel.id].roles_num['6']) + "\n",
              "Куртизанок: " + str(game_sessions[ctx.channel.id].roles_num['7']) + "\n",
              "Бессмертных: " + str(game_sessions[ctx.channel.id].roles_num['8']) + "\n",
              "Двуликих: " + str(game_sessions[ctx.channel.id].roles_num['9']) + "\n",
              "Воров: " + str(game_sessions[ctx.channel.id].roles_num['10']) + "\n",
              "Сержантов: " + str(game_sessions[ctx.channel.id].roles_num['11']) + "\n",
              "Оборотней: " + str(game_sessions[ctx.channel.id].roles_num['12'])]
        for i in range(1, 13):
            if game_sessions[ctx.channel.id].roles_num[str(i)] != 0:
                x += rl[i - 1]
        await ctx.send(x)
        await blank_message(1, ctx.channel)
        await game_initialize(ctx)


async def pool(ctx, message):
    if type(ctx.channel) != discord.channel.DMChannel:
        if ctx.channel.id in list(game_sessions.keys()):
                await message.edit(content="1. Мирных жителей: " + str(game_sessions[ctx.channel.id].roles_num['1']) + "\n" +
                               "2. Мафий: " + str(game_sessions[ctx.channel.id].roles_num['2']) + "\n" +
                               "3. Донов мафии: " + str(game_sessions[ctx.channel.id].roles_num['3']) + "\n" +
                               "4. Комиссаров: " + str(game_sessions[ctx.channel.id].roles_num['4']) + "\n" +
                               "5. Докторов: " + str(game_sessions[ctx.channel.id].roles_num['5']) + "\n" +
                               "6. Маньяков: " + str(game_sessions[ctx.channel.id].roles_num['6']) + "\n" +
                               "7. Куртизанок: " + str(game_sessions[ctx.channel.id].roles_num['7']) + "\n" +
                               "8. Бессмертных: " + str(game_sessions[ctx.channel.id].roles_num['8']) + "\n" +
                               "9. Двуликих: " + str(game_sessions[ctx.channel.id].roles_num['9']) + "\n" +
                               "10. Воров: " + str(game_sessions[ctx.channel.id].roles_num['10']) + "\n" +
                               "11. Сержантов: " + str(game_sessions[ctx.channel.id].roles_num['11']) + "\n" +
                               "12. Оборотней: " + str(game_sessions[ctx.channel.id].roles_num['12']) + "\n\n" +
                               "Оставшихся мест: " + str(len(game_sessions[ctx.channel.id].members) -
                                                         int(sum(list(game_sessions[ctx.channel.id].roles_num.values())))))
        else:
            await ctx.send('Необходимо создать список ролей')


@client.command()
async def save(ctx, name=None):
    if name != None:
        if ctx.channel.id in list(game_sessions.keys()):
            if game_sessions[ctx.channel.id].roles_num != {}:
                x = get_all_sets(ctx.author.id)
                if len(x) >= 5:
                    if name in list(x.keys()):
                        save_set(ctx.author.id, name, game_sessions[ctx.channel.id].roles_num)
                        await ctx.send('Список под названием {} был перезаписан'.format(name))
                    else:
                        await ctx.send('Максимум можно сохранить 5 списков. Напишите название списка, который вы хотите заменить, или `!cancel` для отмены')
                        await sets(ctx)

                        def check(m):
                            return m.author.id == ctx.author.id and m.channel == ctx.channel

                        response = await ctx.bot.wait_for('message', check=check)
                        if response.content == '!cancel':
                            await ctx.send('Отменено')
                            return
                        else:
                            change_set(ctx.author.id, response.content, name, game_sessions[ctx.channel.id].roles_num)
                            await ctx.send('Список {} заменен на список под названием {}'.format(response.content, name))
                else:
                    save_set(ctx.author.id, name, game_sessions[ctx.channel.id].roles_num)
                    await ctx.send('Список сохранен под названием {}'.format(name))
            else:
                await ctx.send('Сохранить список ролей можно только до начала игры')
        else:
            await ctx.send('Необходимо создать список ролей')
    else:
        await ctx.send('Необходимо задать имя списка')


async def user_rename(ctx):
    try:
        for i in range(len(game_sessions[ctx.channel.id].members)):
            try:
                await game_sessions[ctx.channel.id].members[i].edit(
                    nick=(str(i + 1) + '. ' + str(game_sessions[ctx.channel.id].members[i])[:-5]))
            except:
                pass
        for i in list(game_sessions[ctx.channel.id].player_roles.values()):
            if int(i) in [2, 3, 10, 12]:
                game_sessions[ctx.channel.id].black += 1
            elif int(i) == 6:
                game_sessions[ctx.channel.id].maniac += 1
            elif int(i) == 9:
                game_sessions[ctx.channel.id].two_faced += 1
            else:
                game_sessions[ctx.channel.id].red += 1
        game_sessions[ctx.channel.id].player_status = {game_sessions[ctx.channel.id].members[x]: [0 for i in range(6)]
                                                       for x in range(len(game_sessions[ctx.channel.id].members))}
        for i in list(game_sessions[ctx.channel.id].player_roles.keys()):
            await status_maker(i, ctx)
    except:
        await ctx.channel.send('Необходимо сначала задать список ролей для игры.')


async def game_initialize(ctx):
    if type(ctx.channel) != discord.channel.DMChannel:
        for role in game_sessions[ctx.channel.id].roles_num.copy():
            if game_sessions[ctx.channel.id].roles_num[role] == 0:
                if role in game_sessions[ctx.channel.id].roles_num:
                    del game_sessions[ctx.channel.id].roles_num[role]
        if game_sessions[ctx.channel.id].roles_num == {}:
            await ctx.send("Вы не задали роли")
            del game_sessions[ctx.channel.id]
            return
        elif sum(list(game_sessions[ctx.channel.id].roles_num.values())) != len(game_sessions[ctx.channel.id].members):
            await ctx.send('Данный список ролей не подходит для текущего количества игроков')
            del game_sessions[ctx.channel.id]
            return
        else:
            roles_num_list = []
            while game_sessions[ctx.channel.id].roles_num != {}:
                for role in game_sessions[ctx.channel.id].roles_num.copy():
                    if role in game_sessions[ctx.channel.id].roles_num:
                        for i in range(0, game_sessions[ctx.channel.id].roles_num[role]):
                            roles_num_list.append(role)
                        del game_sessions[ctx.channel.id].roles_num[role]
            counter = 1
            for member in game_sessions[ctx.channel.id].members:
                if member.dm_channel == None:
                    x = await member.create_dm()
                    night_ids[x.id] = ctx.channel.id
                else:
                    night_ids[member.dm_channel.id] = ctx.channel.id
                counter += 1
                random.seed(random.randint(0, 100))
                index_of_giving_role = random.randint(0, len(roles_num_list) - 1)
                giving_role = roles_num_list[index_of_giving_role]
                roles_num_list.pop(index_of_giving_role)
                game_sessions[ctx.channel.id].player_roles[member] = giving_role
                emb = discord.Embed(title=roles_description[giving_role][0], colour=discord.Color.darker_grey())
                emb.add_field(name="Описание роли:", value=roles_description[giving_role][1])
                emb.set_image(url=roles_description[giving_role][2])
                await member.send(embed=emb)
        if game_sessions[ctx.channel.id].game_settings['mode'] == 'non-auto':
            del game_sessions[ctx.channel.id]
        else:
                for i in list(game_sessions[ctx.channel.id].player_roles.keys()):
                    try:
                        await i.edit(nick=i.name + ' ❌')
                    except:
                        pass
                game_sessions[ctx.channel.id].vn = 5
                await ctx.send('Описания ролей были отправлены всем в личные сообщения\n\n')
                message = await ctx.send('Подтвердите свою готовность к игре (Нажмите ✅, чтобы подтвердить готовность, нажмите ❌, чтобы отменить готовность)')
                game_sessions[ctx.channel.id].context = message
                await message.add_reaction('✅')
                await message.add_reaction('❌')


@client.command()
async def start(ctx, name=None):
    if ctx.channel.id in list(game_sessions.keys()):
        await ctx.send('В данном канале уже создается список или идет игра')
        return
    if ctx.channel.id not in list(game_sessions.keys()) and name != None:
        new_set = load_set(ctx.author.id, name)
        game_sessions[ctx.channel.id].members = ctx.message.author.voice.channel.members
        if new_set == {}:
            await ctx.send('Такого списка ролей не существует')
            del game_sessions[ctx.channel.id]
            return
        else:
            game_sessions[ctx.channel.id].roles_num = new_set
            del new_set
            game_sessions[ctx.channel.id].game_settings = get_settings(ctx.author.id)
            game_sessions[ctx.channel.id].game_mode = 'custom'
            await game_initialize(ctx)
    elif ctx.channel.id not in list(game_sessions.keys()):
        game_sessions[ctx.channel.id] = Game()
        if ctx.channel.guild.id != 713353831706263573:
            message = await ctx.channel.send(
                'Выберите режим игры и нажмите кнопку для выбора режима. 1 - классика, 2 - свободный')
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
            game_sessions[ctx.channel.id].vn = 6
            game_sessions[ctx.channel.id].right = ctx.author
            game_sessions[ctx.channel.id].context = ctx
        else:
            if ctx.author.voice.channel.user_limit == 10:
                game_sessions[ctx.channel.id].game_settings = {'mode': 'auto', 'mute': 'on',
                                                               'time': [60, 45, 15, 60, 40, 90]}
                await genclassic(ctx)
            else:
                game_sessions[ctx.channel.id].game_mode = 'custom'
                game_sessions[ctx.message.channel.id].game_settings = get_settings(ctx.author.id)
                await create(ctx)


@client.event
async def on_message(mess):
    if mess.author == client.user and mess.guild != None:
        if mess.content == '💠 **ИГРА НАЧАЛАСЬ** 💠':
            await meeting_day(mess)
        if mess.content == 'Наступает день 🌇':
            await day(mess)
        if mess.content == 'Наступает ночь 🌃 (Просьба игрокам с активными ролями перейти в личные сообщения с ботом)':
            await night(mess)
    elif mess.guild == None and mess.author != client.user and night_ids[mess.channel.id] in list(game_sessions.keys()):
        if mess.author in game_sessions[night_ids[mess.channel.id]].members and mess.content[0] != '!' and mess.author in game_sessions[night_ids[mess.channel.id]].right_to_chat:
            await night_echo(mess)
    await client.process_commands(mess)

#---------------------Token-------------------------

token = 'NzEzMzczNTg4ODYxODc4MzQz.XsfK7Q.IigCNgypVztyU5cOg_Bg2tgOYsI'
client.run(token)
