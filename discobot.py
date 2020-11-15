# -*- coding: utf8 -*-
import discord
from discord.ext import commands
import asyncio
import random
import time as tm

prefix = "!"
client = commands.Bot(command_prefix=prefix)
client.remove_command("help")

roles_num_b = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0,'14':0}
players = 0
tumb=0
time = 10
voted=[]
votes=[]
already=[]
available=[]
guilty={}
checker=0
killed=['-']
vote_choice = ''
mode = 'non-auto'
right = None
roles_num = {}
player_roles = {}

#------------------Bot is online-------------------

@client.event
async def on_ready():
    print("Bot is online.")
    await client.change_presence(status= discord.Status.online)

#-----------------Utility commands------------------

@client.command()
async def unmute(ctx):
    await ctx.author.edit(mute=False)

#-------------------Main body-----------------------

#---------------Additional functions----------------

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
        await time_message.delete()
        await time_message.channel.send('Ваш ход окончен.')
    elif vt==1:
        await mess.channel.send('Кто голосует за игрока  ' + str(member)[:-5]+'?')
        message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
        await message.add_reaction('✅')
        for i in range(time - 1, -1, -1):
            time_break = tm.time()
            while True:
                if tm.time() - time_break > 1.0:
                    time_break = tm.time()
                    try:
                        await message.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
                        break
                    except:
                        pass
        await message.delete()
    else:
        message = await mess.channel.send(str(time // 60) + ':' + str((time % 60) // 10) + str((time % 60) % 10))
        await message.add_reaction('✅')
        await message.add_reaction('⛔')
        for i in range(time - 1, -1, -1):
            time_break = tm.time()
            while True:
                if tm.time() - time_break > 1.0:
                    time_break = tm.time()
                    try:
                        await message.edit(content=str(i // 60) + ':' + str((i % 60) // 10) + str((i % 60) % 10))
                        break
                    except:
                        pass
        await message.delete()

@client.event
async def on_reaction_add(reaction,user):
    global count
    global checker
    if reaction.emoji == '⛔' and user == right and vn==0:
        checker = 1
    elif reaction.emoji == '⛔' and user!=reaction.message.author and vn==3:
        if already[members.index(user)] == 0 and available[members.index(user)] == 1:
            count -= 1
            already[members.index(user)] = 1
    elif reaction.emoji == '✅' and user!=reaction.message.author and vn==1:
        if already[members.index(user)] == 0 and available[members.index(user)] == 1:
            votes[members.index(gl)] += 1
            already[members.index(user)] = 1
    elif reaction.emoji == '✅' and user != reaction.message.author and vn == 2:
        if already[members.index(user)] == 0 and available[members.index(user)] == 1:
            already[members.index(user)] = 1
            guilty[ind] += 1
    elif reaction.emoji == '✅' and user != reaction.message.author and vn == 3:
        if already[members.index(user)] == 0 and available[members.index(user)] == 1:
            already[members.index(user)] = 1
            count += 1

@client.command()
async def vote(ctx,choice):
    try:
        if ctx.author.id == right_to_vote.id:
            global vote_choice
            try:
                choice = int(choice)
            except:
                pass
            global tumb
            if choice > len(members) or choice - 1 < 0:
                await ctx.send('Игрока под номером ' + str(choice) + ' не существует, проголосуйте за другого.')
            elif choice-1 in voted and sum(votes) == 0:
                await ctx.send('Этот игрок уже выставлен на голосование. Выберите другого.')
            elif available[choice-1] == 0:
                await ctx.send('Этот игрок уже убит. Выберите другого.')
            elif len(voted)!=0 and choice-1 not in voted and tumb == 1:
                await ctx.send('Необходимо проголосовать за одного из игроков выставленных на голосовании')
            elif len(guilty)!=0 and choice-1 not in guilty:
                await ctx.send('Необходимо проголосовать за одного из игроков выставленных на голосовании')
            else:
                vote_choice=choice
                await ctx.send('Принято!')
    except:
        pass

#-----------------Main commands---------------------

@client.command()
async def change(ctx):
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
        await ctx.send("1. Мирный житель " + "\n" + "2. Мафия "+ "\n" + "3. Дон мафии " + "\n" + "4. Комиссар " + "\n" + "5. Доктор " + "\n" + "6. Маньяк " + "\n" + "7. Куртизанка " + "\n" + "8. Бессмертный " + "\n" + "9. Двуликий " + "\n" + "10. Некромант " + "\n" + "11. Лунатик " + "\n" + "12. Вор " + "\n" + "13. Сержант " + "\n" + "14. Оборотень")
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
        await ctx.send(
            "1. Мирный житель " + "\n" + "2. Мафия " + "\n" + "3. Дон мафии " + "\n" + "4. Комиссар " + "\n" + "5. Доктор " + "\n" + "6. Маньяк " + "\n" + "7. Куртизанка " + "\n" + "8. Бессмертный " + "\n" + "9. Двуликий " + "\n" + "10. Некромант " + "\n" + "11. Лунатик " + "\n" + "12. Вор " + "\n" + "13. Сержант " + "\n" + "14. Оборотень")
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
    await ctx.send("1. Мирных жителей: " + str(roles_num['1']) + "\n" + "2. Мафий: " + str(roles_num['2']) + "\n" + "3. Донов мафии: " + str(roles_num['3']) + "\n" + "4. Комиссаров: " + str(roles_num['4']) + "\n" + "5. Докторов: " + str(roles_num['5']) + "\n" + "6. Маньяков: " + str(roles_num['6']) + "\n" + "7. Куртизанок: " + str(roles_num['7']) + "\n" + "8. Бессмертных: " + str(roles_num['8']) + "\n" + "9. Двуликих: " + str(roles_num['9']) + "\n" + "10. Некромантов: " + str(roles_num['10']) + "\n" + "11. Лунатиков: " + str(roles_num['11']) + "\n" + "12. Воров: " + str(roles_num['12']) + "\n" + "13. Сержантов: " + str(roles_num['13']) + "\n" + "14. Оборотней: " + str(roles_num['14']) + "\n\n" + "Оставшихся мест: " + str(int(players) - int(roles_num['1']) - int(roles_num['2']) - int(roles_num['3']) - int(roles_num['4']) - int(roles_num['5']) - int(roles_num['6']) - int(roles_num['7']) - int(roles_num['8']) - int(roles_num['9']) - int(roles_num['10']) - int(roles_num['11']) - int(roles_num['12']) - int(roles_num['13']) - int(roles_num['14'])))

@client.command()
async def give(ctx):
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
            counter = 1
            for member in members:
                counter+=1
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
            await ctx.send("Роли были распределены. Удачной игры!")
    else:
        await ctx.send("Количество участников голосового канала и количество указанных игроков не соответствует.")

@client.command()
async def start(ctx):
    if mode == 'non-auto':
        await ctx.send('Эта команда доступна только для режима без ведущего.')
    else:
        try:
            for i in range(len(members)):
                try:
                    await members[i].edit(nick=(str(i+1)+'. '+str(members[i])[:-5]))
                except:
                    pass
            members[0]
            await ctx.send('Игра началась!')
        except:
            await ctx.send('Необходимо сначала задать список ролей для игры.')

@client.event
async def on_message(mess):
    if mess.author == client.user and mess.guild != None:
        if mess.content == 'Игра началась!': # День знакомств
            await mess.channel.send('Начинается день знакомств')
            global already
            already = [0 for i in range(len(members))]
            global time
            global tumb
            global available
            global right
            global checker
            global vn
            vn = 0
            tumb = 0
            available = [1 for i in range(len(members))]
            for member in members:
                right=member
                checker = 0
                await timer(time,mess,member,0)
            await mess.channel.send('Наступает день')
        if mess.content == 'Наступает день':#объявление убитых+выставление на голосование игроков
            await mess.channel.send('Ночью были убиты игроки под номерами: '+ (', ').join(killed))
            #for person in killed:
                #available[int(person)-1] = 0
                #await members[int(person)-1].edit(nick=str(person) + '. ' + str(members[int(person)-1])[:-5] + ' ☠', mute=True)
            await mess.channel.send('Начинается обсуждение и выставление кандидатур на голосование.')
            global voted
            global votes
            global right_to_vote
            voted=[]
            votes = [0 for i in range(len(members))]#колличественные голоса за игроков
            killed.clear()
            global vote_choice
            for i in range(len(available)):
                if available[i] == 1:
                    checker = 0
                    vote_choice = ''
                    member = members[i]
                    right = member
                    right_to_vote=member
                    await timer(time,mess,member,0)
                    if vote_choice == '':
                        pass
                    elif vote_choice-1 not in voted:
                        voted.append(vote_choice-1)
            right_to_vote=None
            if len(voted)==0:
                await mess.channel.send('Было принято решение никого не сажать в тюрьму.')
            else:
                m=[]
                for i in range(len(voted)):
                    m.append(str(voted[i]+1))
                await mess.channel.send('Обвиняются игроки под номерами: ' + (', ').join(m))
                await mess.channel.send('Обвиняемым предоставляется оправдательная речь')
        if mess.content == 'Обвиняемым предоставляется оправдательная речь':
            for i in voted:
                checker=0
                member = members[i]
                right = member
                await timer(time,mess,member,0)
            await mess.channel.send('Начинается голосование')
        if mess.content == 'Начинается голосование':
            tumb = 1
            votes.append(1)
            right = None
            vn=1
            for i in voted:
                member = members[i]
                global gl
                gl = member
                await timer(time,mess,member,1)
            del votes[-1]
            for i in range(len(already)):
                if available[i]==1 and already[i]==0:
                    votes[voted[-1]]+=1
            await mess.channel.send('Голосование окончено')
        if mess.content == 'Голосование окончено':
            if votes.count(max(votes)) == 1:
                guil=votes.index(max(votes))
                vn=0
                right=members[guil]
                checker=0
                await mess.channel.send('Приговоренному дается право произнести последнюю речь.')
                await timer(time,mess,members[guil],0)
                available[guil]=0
                await members[guil].edit(nick=str(guil+1) + '. ' + str(members[guil])[:-5] + ' ☠',mute=True)
                await mess.channel.send(str(members[guil])[:-5] + ' был посажен за решетку!')
            else:
                global guilty
                for i in range(len(votes)):
                    if votes[i] == max(votes):
                        guilty[i+1] = 0
                await mess.channel.send('Обвиняемым '+str(guilty.keys())[11:-2]+' предоставляются дополнительные оправдательные речи.')
                guilty.clear()
                right = None
                vn=0
                for i in range(len(votes)):
                    if votes[i] == max(votes):
                        checker=0
                        guilty[i] = 0
                        member = members[i]
                        right=member
                        await timer(time,mess,member,0)
                await mess.channel.send('Начинается повторное голосование.')
                right = None
                already = [0 for i in range(len(members))]
                for i in range(len(guilty)):
                    vn=2
                    member = members[list(guilty.keys())[i]]
                    global ind
                    ind=list(guilty.keys())[i]
                    await timer(time, mess, member, 1)
                for i in range(len(already)):
                    if available[i] == 1 and already[i] == 0:
                        guilty[list(guilty.keys())[-1]] += 1
                if list(guilty.values()).count(max(guilty.values())) == 1:
                    vn=0
                    for i in range(len(guilty)):
                        if guilty[i] == max(guilty.values()):
                            checker=0
                            right=members[list(guilty.keys())[i]]
                            await mess.channel.send('Приговоренному дается право произнести последнюю речь.')
                            await timer(time, mess, members[list(guilty.keys())[i]], 0)
                            available[i] = 0
                            try:
                                await members[i].edit(nick=str(i + 1) + '. ' + str(members[i])[:-5] + ' ☠',mute=True)
                                await mess.channel.send(str(members[i])[:-5] + ' был посажен за решетку!')
                            except:
                                pass
                            break
                else:
                    for i in list(guilty.keys()):
                        if guilty[i]!=max(guilty.values()):
                            del guilty[i]
                    await mess.channel.send('По-прежнему остались игроки с одинаковым количеством голосов, поэтому принимается решение: выгнать или оставить всех.\n✅ - выгнать, ⛔ - оставить')
                    global count
                    count=0
                    vn=3
                    right=None
                    already = [0 for i in range(len(members))]
                    checker=0
                    await timer(time,mess,member,2)
                    for i in range(len(already)):
                        if available[i]==1 and already[i]==0:
                            count-=1
                    if count>0:
                        await mess.channel.send('Приговоренным дается право произнести последнюю речь.')
                        vn=0
                        for i in list(guilty.keys()):
                            checker=0
                            right=members[list(guilty.keys())[i]]
                            await timer(time, mess, members[list(guilty.keys())[i]], 0)
                            available[i] = 0
                            await members[i].edit(nick=str(i + 1) + '. ' + str(members[i])[:-5] + ' ☠', mute=True)
                            await mess.channel.send(str(members[i])[:-5] + ' был посажен за решетку!')
                    else:
                        await mess.channel.send('Было принято решение никого не сажать в тюрьму.')
    await client.process_commands(mess)

#---------------------Token-------------------------

token = 'NzEzMzczNTg4ODYxODc4MzQz.XsfK7Q.IigCNgypVztyU5cOg_Bg2tgOYsI'
client.run(token)