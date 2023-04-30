# testing.py
import os
import random
import discord
from discord import Embed
import Pet
from datetime import datetime
import time

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

pet = Pet.Pet()
x = -1


intents = discord.Intents.all() #discord.py has changed
intents.members = True # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='t!', intents=intents)





    


@bot.event

async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
            
    print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
    
@bot.command(name='pet')
async def pet_command(ctx):
    if pet.type == -1: 
        await ctx.send("You don't have a pet to show off! Try t!choose to pick your pet :)")
        return
    await ctx.send("Display Pet")

@bot.command(name='RPS')
async def play_game(ctx):

    if pet.type == -1: 
        await ctx.send("You don't have a pet to play with! Try t!choose to pick your pet :)")
        return
    """Play a game of rock-paper-scissors against the user"""

   
    # Get the channel from the context
    channel = ctx.channel

    # Create an embed object with information about a game of rock-paper-scissors
    embed = Embed(
        title="Rock, Paper, Scissors!",
        description="Play a game of rock-paper-scissors against the user",
        color=0xf0f0f0,
    )
    embed.set_thumbnail(
        url="https://media.istockphoto.com/id/1056840214/vector/rock-paper-scissors-vector-illustration.jpg?s=612x612&w=0&k=20&c=6KEBfon5f9BXXhLiu9JfOk6EHsM193SiWMcqDjN1jqM="
    )

    # Send the message with the embed
    await channel.send(content="", tts=False, embed=embed)


    options = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(options)
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in options
    
    await ctx.send("Enter 'rock', 'paper', or 'scissors': ")

    user_choice = await bot.wait_for('message', check=check)
    user_choice = user_choice.content.lower()
    
    await ctx.send("Bot is thinking. . .")
    await ctx.send(f"Bot chooses {bot_choice}")
    
    if user_choice == bot_choice:
        await ctx.send("It's a tie!")
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'paper' and bot_choice == 'rock') or \
         (user_choice == 'scissors' and bot_choice == 'paper'):
        #images\MONTY-HAPPY.png
        file = discord.File("MONTY-HAPPY.png")
        pet.incHappy(5)
        await ctx.send(file=file)
        await ctx.send("You win!")
    else:
        file = discord.File("MONTY-MAD.png")
        pet.decHappy(5)
        await ctx.send(file=file)
        await ctx.send("Bot wins!")
    pet.decEnergy(2)
    pet.decFood(2)
    await kill(ctx)

@bot.command(name='HoL')
async def play_H_L(ctx):

    if pet.type == -1: 
        await ctx.send("You don't have a pet to play with! Try t!choose to pick your pet :)")
        return
    """Play a game of higher or lower against me!!!!!!!\n"""
    """I'm thinking of a number. You guess a number, and I'll tell you if the number is higher or lower, until you guess the number!!\n"""
    """You have 5 tries. Let's play! \n"""



    channel = ctx.channel
    embed = Embed(
        title= "Higher or Lower",
        description= "I'm thinking of a number. You guess a number, and I'll tell you if the number is higher or lower, until you guess the number\n\nYou have 10 tries. Let's play!",
        color= 0x36cb4a,
    )

    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/1101918931222008010/1102120728536567868/Untitled_Artwork.png?width=1024&height=1024"
    )
    await channel.send(content="", tts=False, embed=embed)


    secret_number = random.randint(1, 100)

    counter = 0


    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

    await ctx.send("Guess a number: ")
    user_choice = await bot.wait_for('message', check=check)
    user_input = int(user_choice.content)

    print(secret_number) #FIXME


    while secret_number != user_choice:
        if counter == 5:
            print(pet.happy)
            pet.decHappy(5)
            print(pet.happy)
            file = discord.File("MONTY-MAD.png")
            await ctx.send(file=file)
            await ctx.send("You lose. You should study binary search")
            break
        elif user_input > secret_number:
            await ctx.send("Lower.")
            counter = counter + 1
        elif user_input < secret_number:
            await ctx.send("Higher.")
            counter = counter + 1
        else:
            file = discord.File("MONTY-HAPPY.png")
            print(pet.happy)
            pet.incHappy(5)
            print(pet.happy)
            await ctx.send(file=file)
            congrats = "You little genius. You got! It only took you "
            congrats += str(counter)

            if counter == 1:
                congrats += " try!! What are the odds?"
            else:
                congrats += " tries!"

            await ctx.send(congrats)
            break

        await ctx.send("Guess again: \n")

        user_choice = await bot.wait_for('message', check=check)
        user_input = int(user_choice.content)
    pet.decEnergy(2)
    pet.decFood(2)
    await kill(ctx)
        
@bot.command(name='choose')
async def choose_pet(ctx):
    if pet.type > -1: 
        await ctx.send("You already have a pet!")
        return
    await ctx.send("Please choose between Dog (0) or Axolotl (1)")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()
    user_choice = await bot.wait_for('message', check=check)
    user_input = int(user_choice.content)
    
    pet_name = ""
    if user_input == 0:
        pet_name = "Monty"
    elif user_input == 1:
        user_input == 'Axolotl'
        pet_name = "Frankie"
        
    pet.setName(pet_name)
    pet.setType(user_input)

    
    await ctx.send("Your pet " + pet.name + " says hi!")
    file = discord.File(pet.sprites[pet.type][0])
    await ctx.send(file=file)

    print(pet.status())
    
@bot.command(name='sleep')
async def sleep(ctx):
    if pet.type == -1: 
        await ctx.send("You don't have a pet! Try t!choose to pick your pet :)")
        return
    await ctx.send("Do you want to put your pet to sleep: Y/N")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    user_choice = await bot.wait_for('message', check=check)
    user_input = user_choice.content
    
    if user_input == 'Y':
        sleepRet = pet.putToSleep(1)
        if(sleepRet == -1):
            file = discord.File(pet.sprites[pet.type][2])
            await ctx.send(file=file)
            await ctx.send("Your pet did not want to go to sleep, you silly!")
            
@bot.command(name='status')
async def status(ctx):
    if pet.type == -1: 
        await ctx.send("You don't have a pet! Try t!choose to pick your pet :)")
        return
    if(pet.sleeping):
        file = discord.File(pet.sprites[pet.type][4])
        await ctx.send(file=file)
        await ctx.send(pet.name + " is sleeping")
    else:
        await ctx.send("Happy Level: " + str(pet.happy))
        await ctx.send("Energy Level: " + str(pet.energy))
        await ctx.send("Food Level: " + str(pet.food))
        if pet.status() == 3:
            file = discord.File(pet.sprites[pet.type][0])
            await ctx.send(file=file)
            await ctx.send(pet.name + " is happy!")
        elif pet.status() == 2:
            file = discord.File(pet.sprites[pet.type][1])
            await ctx.send(file=file)
            await ctx.send(pet.name + " is tired")
            await ctx.send(pet.name + " needs to take a nap!")
            
        elif pet.status() == 1:
            file = discord.File(pet.sprites[pet.type][2])
            await ctx.send(file=file)
            await ctx.send(pet.name + " is hungry!")
            await ctx.send("You should feed " + pet.name + "!")
        else:
            file = discord.File(pet.sprites[pet.type][1])
            await ctx.send(file=file)
            await ctx.send(pet.name + " is sad")
            await ctx.send(pet.name + " wants to play with you!")
    
@bot.event
async def kill(ctx):
    if pet.happy == 0 or pet.energy == 0 or pet.food == 0:
        pet.type = -1
        await ctx.send(pet.name + " died! :(")
        if pet.happy == 0:
            await ctx.send("They died from saddness!")
        elif pet.food == 0:
            await ctx.send("They starved!")
        elif pet.energy == 0:
            await ctx.send("They died of exhaustion!")
        #FIXME insert dieded image

# @bot.command(name='dieded')
# async def dieded(ctx):
#     pet.happy = 0
#     await kill(ctx)
        


# Define the slot machine emojis
emojis = ["🍒", "🍊", "🍋"]

# Define the slot machine command

@bot.command(name='slots')
async def play_slots(ctx):
    channel = ctx.channel
    embed = Embed(
        title= "Slot Machine",
        description= "Step right up and spin the reels of fortune in our thrilling slot machine game, where every spin could lead to dazzling non-stop excitement!",
        color=0x100361,
    )

    embed.set_thumbnail(
        url="https://www.shutterstock.com/image-vector/slot-machine-cartoon-character-illustration-600w-2169481853.jpg"
    )
    await channel.send(content="", tts=False, embed=embed)
    
    emojis = [":smile:", ":heart:", ":star:", ":moneybag:", ":apple:", ":pineapple:", ":lemon:", ":cherries:", ":grapes:", ":watermelon:"]
    slot1 = random.choice(emojis)
    slot2 = random.choice(emojis)
    slot3 = random.choice(emojis)
    embed = discord.Embed(title="Slot Machine", color=0x100361)
    
    # Check if all three slots match
    # result_embed = discord.Embed(title="Slot Machine", color=0x100361)

    if slot1 == slot2 == slot3:
        # message = f"JACKPOT! 🎉🎉🎉"
        pet.incHappy(15)
        file = discord.File(pet.sprites[pet.type][3])
        result_embed = discord.Embed(title="Congratulations!", value=f"{slot1} {slot2} {slot3} \n\nJACKPOT! 🎉🎉🎉", inline=False)
        await ctx.send(file=file, embed=embed)
    else:
        # message = f"Sorry, better luck next time 😔"
        pet.decHappy(5)
        file = discord.File(pet.sprites[pet.type][1])
        embed.add_field(name="Result", value=f"{slot1} {slot2} {slot3} \n\nSorry, better luck next time 😔", inline=False)
        await ctx.send(file=file, embed=embed)
        #  embed=result_embed
        
    # Send the slot machine message to the Discord channel
    pet.decEnergy(3)
    pet.decFood(2)
    # await ctx.send(message)
    await kill(ctx)

@bot.command(name='nap')
async def nap(ctx):
    if pet.type == -1: 
        await ctx.send("You don't have a pet! Try t!choose to pick your pet :)")
        return
    pet.nap()
    await ctx.send(pet.name + " is taking a quick nap!")
    file = discord.File(pet.sprites[pet.type][4])
    await ctx.send(file=file)

@bot.command(name='feed')
async def feedChoice(ctx):
    if pet.type == -1: 
        await ctx.send("You don't have a pet to feed! Try t!choose to pick your pet :)")
        return
    """Choose what to feed your Pet!"""
    options = ['Donut','Burger']
    comp_choice = random.choice(options)

    if comp_choice == 'Donut':
        await ctx.send("Your Pet is Craving Something Sweet\nWould you like to feed it a Burger or Donut")
    else: 
        await ctx.send("Your Pet is Craving Something Savory\nWould you like to feed it a Burger or Donut")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content in options

    user_choice = await bot.wait_for('message', check=check)

    if user_choice.content not in options:
        await ctx.send("Invalid choice! Try again.")
    

    if user_choice.content == comp_choice:
        await ctx.send("You made your pet Happy!")
        pet.incFood(6)
        
        file = discord.file(pet.sprites[pet.type][3])

        await ctx.send(file=file)
        
    else:
        await ctx.send("Uh-oh, wrong choice")
        pet.decHappy(3)
        file = discord.file(pet.sprites[pet.type][2])
        await ctx.send(file=file)
    await kill(ctx)

bot.run(TOKEN)