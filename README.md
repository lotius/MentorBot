# Setting Up A New Copy of MentorBot
## Preparation
To get started running your own copy of MentorBot you will need a few things:
- A discord server that you have administrative or moderator access to (in order to invite the bot to it)
- A computer or server (Windows/Linux) capable of running the Python interpreter.
- Python 3
- PIP (Python package manager)
- An internet connection

## Discord Bot Application Creation
To get started you'll need to navigate to Discord's Developer Application section on their website: [Discord Developer Application](https://discord.com/developers/applications). Log into it with your Discord credentials.

You should be at a page that looks similar to this:

<img width="2531" height="1216" alt="image" src="https://github.com/user-attachments/assets/0ddc7522-f177-4409-9522-996d8fffce6b" />

Click on New Application in the upper-right corner. Give the application a name, such as MentorBot, or whatever you want it to be called. This isn't the bot's name within your server. That comes later. You'll be at a screen that looks like this:

<img width="2500" height="1227" alt="image" src="https://github.com/user-attachments/assets/c9923527-696c-464b-be4c-63608686e378" />

You can fill out a description, add an application icon (I have the Mentor image in place, as you can see), some tags to help identify your application, but they are not required. Next, go to the Installation section on the left, and choose Guild Install on the right:

<img width="2487" height="782" alt="image" src="https://github.com/user-attachments/assets/1c9b9490-f360-40a6-9610-2c01b4c4cd6d" />

Next, head to the Bot tab. We need to grab some values from here to hold onto for later:

<img width="2092" height="1210" alt="image" src="https://github.com/user-attachments/assets/b34c52b8-8e61-412e-8f41-302e69e6c167" />

Notice that you can set a user icon and name for your bot here. Do that now.

Under the section that says TOKEN click the Reset Token button. Copy the value that is generated and store that for later. Do not make this value public to anyone. The token can only be viewed once so make sure to copy it properly, or you will have to do a Reset Token again to get a new one:

<img width="1093" height="148" alt="image" src="https://github.com/user-attachments/assets/1f8b2cb5-2504-4e65-b9fd-1803726fdd48" />

We will reference this BOT_TOKEN value later

Scroll down and turn on the permissions for Presence Intent, Server Members Intent, and Message Content Intent:

<img width="2461" height="866" alt="image" src="https://github.com/user-attachments/assets/a4e066fa-f490-48fe-9342-ff0a726f7b22" />

Presence probably isn't currently needed, but I have future plans for it. Make sure to Save Changes before moving on.

Next, head to the OAuth2 section on the left, and scroll down to OAuth2 URL Generator. Under Scopes, select Bot:

<img width="2261" height="898" alt="image" src="https://github.com/user-attachments/assets/9cc823fc-fb60-4d21-a900-a1ed2c7549a0" />

This will open up another section below that. Scroll down to Bot Permissions, and select Administrator:

<img width="2310" height="1125" alt="image" src="https://github.com/user-attachments/assets/f3987625-cf32-4bb9-81a1-dafb92d447bb" />

Now, the bot probably doesn't need full administrator permissions. If you're uncomfortable with that you'll need to select the individual permissions the bot would need instead. The bot needs to be able to:
- Send Messages
- Send Messages in Threads
- Attach Files
- Embed Links
- View Channels

<img width="927" height="986" alt="image" src="https://github.com/user-attachments/assets/0d07015f-c672-407e-b919-4a705103a0a0" />

Now at the very bottom of the OAuth2 page you will have a URL/link that has been generated in the Generated URL box based on the selections you have made. Copy this link, open up a fresh browser tab, and then paste it in. You'll be taken to a page that looks like this:

<img width="746" height="887" alt="image" src="https://github.com/user-attachments/assets/b43150fc-63ff-4ad8-8ba9-d470fbd2c6a5" />

This is where you will select the server you wish to invite the bot into. Click Continue, verify the permissions, and then Authorize:

<img width="676" height="447" alt="image" src="https://github.com/user-attachments/assets/af0cc44c-b5a5-4381-bef7-b8c449722082" />

If you look in Discord you'll see that your bot is now in your server! However, it is still offline. 

<img width="596" height="387" alt="image" src="https://github.com/user-attachments/assets/a0ef1dc1-6fb3-4786-8eb4-6a5337117034" />

We need to set up our Python environment and actually run the bot for it to log in and respond to user input.

## Setting up Python

