import discord
import boto3
import sys
import os

TOKEN = os.environ['TOKEN']
SERVER_CHANNEL = int(os.environ['SERVER_CHANNEL'])
AWSAccessKeyId = os.environ['AWS_ACCESS_KEY_ID']
AWSSecretKey = os.environ['AWS_SECRET_KEY']
AWSInstanceID = os.environ['AWS_INSTANCE_ID']

ec2 = boto3.resource('ec2',
        aws_access_key_id = AWSAccessKeyId,
        aws_secret_access_key = AWSSecretKey ,
        region_name ='ap-northeast-1'
)
instance = ec2.Instance(AWSInstanceID)

client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    await client.get_channel(SERVER_CHANNEL).send('bot online.')
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot or message.channel.id != SERVER_CHANNEL:
        #print(message.content)
        return
    if message.content=="!exit":
        exit()
        return
    if message.content=='!start':
        try:
            instance.start()
            instance.wait_until_running()
            await message.channel.send('server online.')
        except:
            await message.channel.send('failed to start instance.')
        return
    if message.content=='!stop':
        instance.stop()
        instance.wait_until_stopped()
        await message.channel.send('server stopped.')
        return
    if message.content.startswith('!'):
        await message.channel.send('WARNING: not a command.')
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
