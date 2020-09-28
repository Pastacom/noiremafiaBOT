# -*- coding: utf8 -*-
import discord
from discord.ext import commands
import asyncio
import random

prefix = "!"
client = commands.Bot(command_prefix=prefix)
client.remove_command("help")


@client.command()
async def mute(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.author.edit(mute=True)

@client.command()
async def unmute(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.author.edit(mute=False)



@client.command()
async def timer(ctx):
    await ctx.channel.purge(limit=1)
    minutes = 1
    seconds = 30
    if seconds < 10:
        message = await ctx.send(str(minutes)+':0'+str(seconds))
        await message.add_reaction('⛔')
    else:
        message = await ctx.send(str(minutes)+':'+str(seconds))
        await message.add_reaction('⛔')
    for i in range(1,seconds+1+minutes*60):
        seconds-=1
        if seconds < 0 and minutes > 0:
            minutes-=1
            seconds=59
            new_time = str(minutes) + ':' + str(seconds)
        elif seconds<10:
            new_time = str(minutes) + ':0' + str(seconds)
        else:
            new_time = str(minutes)+':'+str(seconds)
        await message.edit(content=new_time)
        def check(reaction, user):
            return str(reaction.emoji) == '⛔' and user != message.author
        try:
            await client.wait_for('reaction_add', timeout=1, check=check)
            await message.delete()
            await ctx.send('Ваш ход окончен.')
        except asyncio.TimeoutError:
            pass
    await message.delete()
    await ctx.send('Ваш ход окончен.')

async def add_role(num, ctx):
    def check(m):
        return m.author.id == ctx.author.id
    response = await ctx.bot.wait_for('message', check=check)
    try:
        request = response.content
        if int(request[-1])<=num:
            roles_num[request[:len(request)-2]]+=int(request[-1])
        else:
            await ctx.send('Количество ролей превышает количество игроков. Попробуйте снова.')
            await add_role(num, ctx)
    except:
        request='0'
    if num-int(request[-1])>0:
        await add_role(num-int(request[-1]), ctx)

roles_num_b = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0,'14':0}
players = 0
mode = 'non-auto'
roles_num = {}
player_roles = {}

@client.event
async def on_ready():
    print("Bot is online.")
    await client.change_presence(status= discord.Status.online)

@client.command()
async def change_mode(ctx):
    await ctx.channel.purge(limit=1)
    global mode
    global roles_num
    roles_num = roles_num_b.copy()
    if mode == 'non-auto':
        mode = 'auto'
        await ctx.send("Предустановка игры переключена на режим без ведущего.")
    else:
        mode = 'non-auto'
        await ctx.send("Предустановка игры переключена на режим с ведущим.")


@client.command()
async def create(ctx):
    await ctx.channel.purge(limit=1)
    global roles_num
    global members
    global roles_num_b
    global players
    if mode == "non-auto":
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
        await ctx.send("Количество игроков? (Не считать ведущего)")
        success = False
        while success != True:
            response = await ctx.bot.wait_for('message', check=check)
            if int(response.content) > 0:
                success = True
            else:
                await ctx.send("Слишком мало игроков для начала игры. Заново укажите количество")
        await ctx.send("Задайте роли.")
        players = response.content
        await add_role(int(response.content), ctx)
        await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" + "Мирных жителей: " + str(roles_num['1']) + "\n" + "Мафий: " + str(roles_num['2']) + "\n" + "Донов мафии: " + str(roles_num['3']) + "\n" + "Комиссаров: " + str(roles_num['4']) + "\n" + "Докторов: " + str(roles_num['5']) + "\n" + "Маньяков: " + str(roles_num['6']) + "\n" + "Куртизанок: " + str(roles_num['7']) + "\n" + "Бессмертных: " + str(roles_num['8']) + "\n" + "Двуликих: " + str(roles_num['9']) + "\n" + "Некромантов: " + str(roles_num['10']) + "\n" + "Лунатиков: " + str(roles_num['11']) + "\n" + "Воров: " + str(roles_num['12']) + "\n" + "Сержантов: " + str(roles_num['13']) + "\n" + "Оборотней: " + str(roles_num['14']))
    else:
        await ctx.send(
            "Перед началом удостоверьтесь, все ли желающие подключены к Вашему голосовому каналу, в противном случае не все роли смогут выдаться.\nЕсли всё готово, можно приступать к настройке игровой сессии.")
        roles_num = roles_num_b.copy()

        def check(m):
            return m.author.id == ctx.author.id

        members = ctx.message.author.voice.channel.members
        for member in members:
            if member.bot:
                members.remove(member)
        await ctx.send("Количество игроков?")
        success = False
        while success != True:
            response = await ctx.bot.wait_for('message', check=check)
            if int(response.content) > 0:
                success = True
            else:
                await ctx.send("Слишком мало игроков для начала игры. Заново укажите количество")
        await ctx.send("Задайте роли.")
        players = response.content
        await add_role(int(response.content), ctx)
        await ctx.send("Начало игры. Роли игроков в игре:" + "\n\n" + "Мирных жителей: " + str(
            roles_num['1']) + "\n" + "Мафий: " + str(roles_num['2']) + "\n" + "Донов мафии: " + str(
            roles_num['3']) + "\n" + "Комиссаров: " + str(roles_num['4']) + "\n" + "Докторов: " + str(
            roles_num['5']) + "\n" + "Маньяков: " + str(roles_num['6']) + "\n" + "Куртизанок: " + str(
            roles_num['7']) + "\n" + "Бессмертных: " + str(
            roles_num['8']) + "\n" + "Двуликих: " + str(roles_num['9']) + "\n" + "Некромантов: " + str(
            roles_num['10']) + "\n" + "Лунатиков: " + str(roles_num['11']) + "\n" + "Воров: " + str(
            roles_num['12']) + "\n" + "Сержантов: " + str(roles_num['13']) + "\n" + "Оборотней: " + str(
            roles_num['14']))

@client.command()
async def pool(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("1. Мирных жителей: " + str(roles_num['1']) + "\n" + "2. Мафий: " + str(roles_num['2']) + "\n" + "3. Донов мафии: " + str(roles_num['3']) + "\n" + "4. Комиссаров: " + str(roles_num['4']) + "\n" + "5. Докторов: " + str(roles_num['5']) + "\n" + "6. Маньяков: " + str(roles_num['6']) + "\n" + "7. Куртизанок: " + str(roles_num['7']) + "\n" + "8. Бессмертных: " + str(roles_num['8']) + "\n" + "9. Двуликих: " + str(roles_num['9']) + "\n" + "10. Некромантов: " + str(roles_num['10']) + "\n" + "11. Лунатиков: " + str(roles_num['11']) + "\n" + "12. Воров: " + str(roles_num['12']) + "\n" + "13. Сержантов: " + str(roles_num['13']) + "\n" + "14. Оборотней: " + str(roles_num['14']) + "\n\n" + "Оставшихся мест: " + str(int(players) - int(roles_num['1']) - int(roles_num['2']) - int(roles_num['3']) - int(roles_num['4']) - int(roles_num['5']) - int(roles_num['6']) - int(roles_num['7']) - int(roles_num['8']) - int(roles_num['9']) - int(roles_num['10']) - int(roles_num['11']) - int(roles_num['12']) - int(roles_num['13']) - int(roles_num['14'])))

@client.command()
async def give(ctx):
    await ctx.channel.purge(limit=1)
    if len(members) == int(players):
        for role in roles_num.copy():
            if roles_num[role] == 0:
                if role in roles_num:
                    del roles_num[role]
        if roles_num == {}:
            await ctx.send("Вы не задали роли.")
        else:
            roles_num_list = []
            while roles_num != {}:
                for role in roles_num.copy():
                    if role in roles_num:
                        for i in range(0, roles_num[role]):
                            roles_num_list.append(role)
                        del roles_num[role]
            for member in members:
                random.seed(random.randint(0, 100))
                index_of_giving_role = random.randint(0, len(roles_num_list) - 1)
                giving_role = roles_num_list[index_of_giving_role]
                roles_num_list.pop(index_of_giving_role)
                global player_roles
                player_roles[member] = giving_role
                if giving_role == "1":
                    emb = discord.Embed(title="Ваша роль - Мирный житель.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Ваша задача состоит в том, чтобы вычислить представителей мафии и посадить в тюрьму. Сделать это вы можете только на дневном голосовании.")
                    emb.set_image(url="https://w-dog.pw/android-wallpapers/4/15/455401079884056/colton-haynes-guy-men-black-machine-black-and-white.jpg")
                    await member.send(embed=emb)
                elif giving_role == "2":
                    emb = discord.Embed(title="Ваша роль - Мафия.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за черных. Ваша задача - избавиться от всех красных игроков в городе. Ночью вы просыпаетесь вместе с другими представителями мафии. Мафия убивает одного игрока за ночь, выбранного общим решением. Если возникают разногласия, то финальное решение принимается Доном мафии. При смерти Дона, убивается цель, за которую проголосовало большее кол-во игроков.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742967390601277/8011f830f532082c.jpg?width=782&height=519")
                    await member.send(embed=emb)
                elif giving_role == "3":
                    emb = discord.Embed(title="Ваша роль - Дон мафии.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за черных. Ваша задача - избавиться от всех красных игроков в городе и обнаружить комиссара, как можно скорее. Ночью вы просыпаетесь дважды, сначала вместе с другими представителями мафии, затем отдельно. Мафия убивает одного игрока за ночь, выбранного общим решением. Если возникают разногласия, то финальное решение принимается вами. Когда вы проснетесь второй раз вы можете указать на любого игрока, если этот игрок - комиссар, то ведущий даст соответсвующий знак.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742944728907786/f1c3da335e7e8b0f.jpg?width=519&height=519")
                    await member.send(embed=emb)
                elif giving_role == "4":
                    emb = discord.Embed(title="Ваша роль - Комиссар.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за красных. Ваша задача - искать мафиози ночью. Когда вы просыпаетесь, вы можете выбрать любого игрока, если это черный игрок, ведущий даст соответсвующий ответ. При проверке маньяка, ведущий скажет, что он играет за мирных. Результаты проверки известны только вам, но вы всегда можете огласить их днем для всех остальных. Просыпается вместе с сержантом, если таковой есть.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742946112897034/357cb0fc4c2d221d.jpg?width=514&height=519")
                    await member.send(embed=emb)
                elif giving_role == "5":
                    emb = discord.Embed(title="Ваша роль - Доктор.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за красных. Ваша задача - спасать от покушения игроков. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока(включая себя), если его пытались убить этой ночью, то он выживает, благодаря вам. Нельзя лечить одного и того же игрока две ночи подряд.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742942719836250/e5b40f920b837dfb.jpg?width=519&height=519")
                    await member.send(embed=emb)
                elif giving_role == "6":
                    emb = discord.Embed(title="Ваша роль - Маньяк.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете сами за себя. Ваша задача - остаться одному в игре. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока, которого хотите убить. Если вас проверит комиссар, то он получит результат, что вы мирный.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742948600119296/14b400af131ac30e.jpg?width=519&height=519")
                    await member.send(embed=emb)
                elif giving_role == "7":
                    emb = discord.Embed(title="Ваша роль - Куртизанка.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за красных. Ваша задача - спасать красных. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока. Выбранный игрок не может быть убит в эту ночь, но при этом теряет возможность использовать свою способность в эту ночь, если она у него есть. Нельзя выбирать одного и того же игрока две ночи подряд. Погибает, если выбирает ночным клиентом Маньяка. Если мафиози остается один и вы выбираете его, то мафиози не убивают этой ночью.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742947987882094/e70bf7c63c141dda.jpg?width=830&height=519")
                    await member.send(embed=emb)
                elif giving_role == "8":
                    emb = discord.Embed(title="Ваша роль - Бессмертный.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за красных. Ваша задача - принимать удар черных на себя. Ночью вас не могут убить. Единстевнный способ выйти из игры - это дневное голосование, на котором решат посадить вас.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713743623614758942/5f9244fb10cf04ea280eb6b192b9df7a--baron-samedi-skull-art.png?width=357&height=519")
                    await member.send(embed=emb)
                elif giving_role == "9":
                    emb = discord.Embed(title="Ваша роль - Двуликий.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за черных. Ваша задача - найти мафию, как можно скорее. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока. Если этот игрок - мафия, то вы получите право просыпаться вместе с мафией ночью и самостоятельно убивать одну цель независимо от мафии. Если всех мафиози посадят или убьют, до того как вы их найдете, то вы проиграете.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742942061461504/f5012122151c499d.jpg?width=872&height=472")
                    await member.send(embed=emb)
                elif giving_role == "10":
                    emb = discord.Embed(title="Ваша роль - Некромант.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за красных. Ваша задача - выбрать нужного человека и вовремя его воскресить. Пока вы живы, все убитые красные могут голосовать половинками голосов. Кроме того, один раз за игру, раскрывшись, вы можете воскресить любого убитого игрока. После вскрытия – Некромант теряет свой статус, а убитые красные перестают голосовать.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713742956653182986/e036ea12affc331c.jpg?width=470&height=519")
                    await member.send(embed=emb)
                elif giving_role == "11":
                    emb = discord.Embed(title="Ваша роль - Лунатик.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за красных. Ваша задача - выдавать себя за мафиози, как можно дольше. Ночью вы просыпаетесь вместе с мафией и участвуете в голосовании. Вы не должны никому говорить свою роль, и кто является мафией. Если вас убивают ночью мафиози, то они сразу получают право убить еще одного игрока, а вы выходите из игры.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713748761725108284/luna-alone-paren-moon-chiorno-beloe.png?width=830&height=519")
                    await member.send(embed=emb)
                elif giving_role == "12":
                    emb = discord.Embed(title="Ваша роль - Вор.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за черных. Ваша задача - лишать хода важных игроков красной команды. Когда вы просыпаетесь ночью, вы можете выбрать любого игрока. Выбранный игрок теряет возможность использовать свою способность в эту ночь, если она у него есть.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713714731038539796/713745661040001124/14977182341005_1920x1200.png?width=830&height=519")
                    await member.send(embed=emb)
                elif giving_role == "13":
                    emb = discord.Embed(title="Ваша роль - Сержант.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за красных. Ваша задача - помогать комиссару в поиске мафии. Вы просыпаетесь вместе с комиссаром и знаете статусы проверенных им игроков. Вы проверять не можете, но если Комиссара убьют, то вы становитесь Комиссаром.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713714731038539796/713747667217285160/97944_original.png?width=780&height=519")
                    await member.send(embed=emb)
                elif giving_role == "14":
                    emb = discord.Embed(title="Ваша роль - Оборотень.", colour=discord.Color.darker_grey())
                    emb.add_field(name="Описание роли:", value="Вы играете за черных. Ваша задача - избавиться от всех красных игроков в городе. Пока жива мафия, у вас нет никаких способностей, вы просто просыпаетесь вместе с мафией, но в голосовании не участвуете. Проверки комиссара покажут, что вы мирный житель. Когда все мафиози выйдут из игры, то вы сможите просыпаться ночью и убивать игроков.")
                    emb.set_image(url="https://media.discordapp.net/attachments/713363794138628176/713748605139419136/scary_werewolf_head_grinning.png?width=722&height=519")
                    await member.send(embed=emb)
            await ctx.channel.purge(limit=1000)
            await ctx.send("Роли были распределены. Удачной игры!")
    else:
        await ctx.send("Количество участников голосового канала и количество указанных игроков не соответствует.")

token = 'NzEzMzczNTg4ODYxODc4MzQz.XsfK7Q.IigCNgypVztyU5cOg_Bg2tgOYsI'
client.run(token)