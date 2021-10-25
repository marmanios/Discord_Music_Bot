import discord
import ast
from discord.ext import commands
from discord.utils import get
import datetime
from random import randint
import pickle

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '-', case_insensitive=True, intents=intents)

class user():
    def __init__(self,  user_id, birthday):
        self.id = user_id
        self.bday = birthday

users = [] 
black_list = [] # This isnt being saved.... will be gone w restart


# Import the birthday data
with open('UserDataBirthday.txt', "rb") as fp:
    users = pickle.load(fp)


# Start of code
bot = commands.Bot(command_prefix="!", case_insensitive=True)


# ----------------------Only helper function in this whole program-----------------------------
def getBday(msg):
    bday = []
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    #Get month
    for x in range(len(months)):
        if months[x] in msg:
            bday.append(x+1)
            break

    #Get day
    day = [int(word) for word in msg.split() if word.isdigit()]
    if day[0] > 0 and day[0] < 32:
        bday.append(day[0])        
    return bday

# ---------------------------------------------------------------------------------------------
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# -----------------------------------------------------Part that runs on every message-----------------------------------------------------------------------------------------
@client.event
async def on_message(message):
    global users

    # ------------- Basic routine checks -------------------
    if message.author == client.user:
        return

    #Fahd
    if message.author.id == 276588536034230273:
        number_rand = randint(1,20)
        if number_rand == 5:
            await message.channel.send('Shut up paki')

    #Glenn
    if message.author.id == 67876039660933120:
        number_rand = randint(1,20)
        if number_rand == 5:
            await message.channel.send('Shut up indian')
    # ------------------------------------------------------


    msg = message.content

    # Useless code
    if msg.startswith('$hello'):
        await message.channel.send('Hey {}'.format(message.author.display_name.split(' ')[0]))

    # Easter egg   
    elif msg.startswith('-my server now'): 
        role_id = 546807045513281597
        role = get(message.guild.roles, id=role_id)
        await message.delete()  # To ensure no tracks left behind
        await message.author.add_roles(role)
        if message.author.dm_channel is None:
            print("im making a private dm channel to a lucky person")
            await message.author.create_dm()
        await message.author.dm_channel.send("You have now ascended!") # Change it so say whatever (dm to the person who calls this function)
        await message.author.dm_channel.send("Tell anyone about this and I'm taking it away")

    # Wipe the data  
    elif msg.startswith('-wipebirthdays') and (message.author.id == 359358562771664897 or message.author.id == 202255919965274112):
        for x in users:
            if x.id != 359358562771664897:
                pass
            
            else:
                users = [x]
                with open('UserDataBirthday.txt', "wb") as fp:
                    pickle.dump(users, fp)
                break                   


    # ------------------------------------------------------------- Handling Blacklist ------------------------------------------------------------------------------
    elif msg.startswith('-blacklist') and (message.author.id == 359358562771664897 or message.author.id == 202255919965274112):
        black_list.append(msg.split(' ')[1])
        print('Blacklisted ' + str(msg.split(' ')[1]))
        await message.channel.send('BANNED :Black: ')
        
    elif msg.startswith('-unblacklist') and (message.author.id == 359358562771664897 or message.author.id == 202255919965274112):
        black_list.remove(msg.split(' ')[1])
        print('Removed ' + str(msg.split(' ')[1]))
        await message.channel.send('UNBANNED :LETSGOOO:')
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------


    # ------------------------------------------------------------- Handling setting the birthdays ------------------------------------------------------------------
    elif msg.startswith('-setbirthdayfor') and (get(message.guild.roles, id=815087380243283999) in message.author.roles) and not(message.author.id in black_list):
        print("existing users: ", end="")
        print(users)
        
        guild = client.guilds[0]
        userId = None
        for member in guild.members:
            if str(member.id) in msg:
                userId = member.id
                msg = msg.replace(str(userId),'')
        bday = getBday(msg.lower())        
        if len(bday) == 2 and userId != None:            
            dupe = False
            for x in range(len(users)):
                if users[x].id == userId:
                    users[x].bday = bday 
                    dupe = True
                    print("You already here")
                    await message.channel.send('User Force overrided')
                    break
                
            if dupe == False:  
                users.append(user(userId, bday))
                print(message.author , bday)
                print("You new dw")
                await message.channel.send('New User Force Added')
    
        elif userId == None:
            await message.channel.send('user not found')
            
        else:
            print("Error with birthday")
            await message.channel.send('Are you fucking retarded?????')
            await message.channel.send('How hard is it to write ur fucking birthday {}'.format(message.author.display_name.split(' ')[0]))

        with open('UserDataBirthday.txt', "wb") as fp:
            pickle.dump(users, fp)

    # Second function
    elif msg.startswith('-setbirthday') and not(message.author.id in black_list):
        print("Existing users: ", end="")
        print(users)
        bday = getBday(msg.lower())
        if len(bday) == 2 and bday[1] < 32:
            userId = message.author.id
            dupe = False
            for x in range(len(users)):
                if users[x].id == userId:
                    users[x].bday = bday 
                    dupe = True
                    print("You already here")
                    break
                
            if dupe == False:  
                users.append(user(userId, bday))
                print(message.author , bday)
                print("You new dw")
                
        else:
            print("Error with birthday")
            await message.channel.send('Are you fucking retarded?????')
            await message.channel.send('How hard is it to write ur fucking birthday {}'.format(message.author.display_name.split(' ')[0]))

        with open('UserDataBirthday.txt', "wb") as fp:
            pickle.dump(users, fp)

    elif msg.startswith('-setb'):
        await message.channel.send('Do you not know how to fucking spell birthday???')
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------


   # -------------------------------------------------Handling displaying the information ---------------------------------------------------------------------------
    elif msg.startswith('-ListOfBirthdays') and (get(message.guild.roles, id=815087380243283999) in message.author.roles) and not(message.author.id in black_list):
        for x in users:
            name = await message.guild.fetch_member(x.id)
            name = name.display_name
            monthnum = str(int(x.bday[0]))
            datetime_object = datetime.datetime.strptime(monthnum, "%m")
            month_name = datetime_object.strftime("%b")
            msg = (str(name) + ': '+ str(month_name)+ ' ' + str(x.bday[1]))
            if message.author.dm_channel is None:
                await message.author.create_dm()
                
            await message.author.dm_channel.send(msg)
            
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    #elif msg.lower().startswith('fuck omar') or msg.lower().startswith('fuck maged'): <--------------- a questionable piece of code
        #await message.author.kick()

    else:
        # Do birthday thing ..... I still need to change the structure of the whole program since its inefficient af
        todayMonth = datetime.datetime.now().month
        todayDay = datetime.datetime.now().day
        role = get(message.guild.roles, id = 597445659703902239)
        # looping through all users with a set birthday
        for person in users:
            bday = person.bday
            print(bday)
            day = bday[1]
            month = bday[0]
            member_to_give = await message.guild.fetch_member(person.id)

            # Adding the role
            if day == todayDay and month == todayMonth:
                print("its your birthday!")
                # Give him the role 597445659703902239
                await member_to_give.add_roles(role)

            # Removing the role
            else:
                await member_to_give.remove_roles(role)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        

client.run("ODM4NjE2MjY0NjA3Mzk5OTU2.YI9sQg.gFAlsm-VIecvqjshz7PyHNhsDmU")
