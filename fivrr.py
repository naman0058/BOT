import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import   MessageHandler, filters ,Updater, CommandHandler, ConversationHandler, CallbackContext, CallbackQueryHandler
import mysql.connector

# Connect to the SQLite database
conn = mysql.connector.connect(
  host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
  user ="doadmin",
  passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
  database="leads",
  port=25060
)
cur = conn.cursor()
def dbcon():
    conn = mysql.connector.connect(
      host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
      user ="doadmin",
      passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
      database="leads",
      port=25060
    )
    cur = conn.cursor()
    return cur


cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INT AUTO_INCREMENT PRIMARY KEY ,user_key BIGINT , username VARCHAR(255)  , Balance INT NOT NULL DEFAULT 0  )")
cur.execute("CREATE TABLE IF NOT EXISTS jobs(job_id INT AUTO_INCREMENT PRIMARY KEY ,topic VARCHAR(255) DEFAULT NULL,Client VARCHAR(255) DEFAULT NULL, description TEXT DEFAULT NULL, Category VARCHAR(255) DEFAULT NULL, phoneno VARCHAR(255) DEFAULT NULL  )")


# Define a function to handle the /jobs command


# Define a function to handle the /apply command
def start(update, context):
    # Get the user's ID and username
    user_iid = update.message.chat_id
    usernamee = update.message.chat.username 
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    for x in [usernamee,first_name,last_name]:
      print(x)
      if x != None:
        usernamee = x
    print(usernamee)
    avl = f"SELECT * FROM users WHERE user_key = {user_iid}"
    cur.execute(avl)
    squr = cur.fetchall()
    # print(squr)
    if squr ==[]:
      qury =f"INSERT INTO users(user_key, username) VALUES (%s,%s);"
      val = tuple([user_iid, usernamee])
      cur.execute(qury,val)
      context.bot.send_message(chat_id=user_iid, text=f"hello {usernamee} wecome back")
      conn.commit()

    else :
      context.bot.send_message(chat_id=user_iid, text=f"hello {usernamee} wecome back")
      context.bot.send_message(chat_id=user_iid, text=f"finding your job ...")
      
      cur.execute("SELECT * FROM jobs")
      jobs=cur.fetchall()
      yourjob = []
      for y in jobs:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Pick Leads', callback_data=y[0])],])
        context.bot.send_message(chat_id=user_iid, text=f"Title \n{y[1]}\n Description \n {y[3]} \n {'X'*10}{y[5][-2:]} \n {y[2]}" , reply_markup=reply_markup)
        
def InlineKeyboardHandler(update: Update, _: CallbackContext):
    conn = mysql.connector.connect(
      host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
      user ="doadmin",
      passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
      database="leads",
      port=25060
    )
    user_key = update.callback_query.message.chat_id
    avl = f"SELECT * FROM users WHERE user_key = {user_key}"
    cur.execute(avl)
    # conn.commit()

    bal = cur.fetchall()[0][3]
    print(bal)
    # print(update)
    if bal >=25 or bal == None:
      upd="UPDATE users SET Balance = Balance-25 WHERE user_key = %s"
      val =tuple([user_key])

      cur.execute(upd,val)
      conn.commit()
      
      option=update.callback_query.data
      job = f"SELECT * FROM jobs WHERE job_id = {option}"
      cur.execute(job)
      y = cur.fetchall()[0]
      
      _.bot.send_message(chat_id=user_key, text=f"Title \n{y[1]}\n Description \n {y[3]} \n {y[5]} \n {y[2]}" )
    else:
      
      _.bot.send_message(chat_id=user_key, text=f"hii {update.callback_query.message.chat.username} \n Your balance is low. Please recharge your account by clicking on the button below.\n your id : {user_key} \n contect @Naman0058" ,)
    
    
def details(update, context):
    user_iid = update.message.chat_id
    usernamee = update.message.chat.username 
    avl = f"SELECT * FROM users WHERE user_key = {user_iid}"
    cur.execute(avl)
    squr = cur.fetchall()[0]
    context.bot.send_message(chat_id=user_iid, text=f"username {squr[2]} \n user ID:{squr[1]} \n ********\n Balance: {squr[3]}")


# Create a new Telegram bot with the provided token

# def skills(update, context):
#     # Get the skills from the message text
#     skills = ",".join(context.args)
#     user_key = update.message.chat_id
#     username = update.message.from_user.username
#     avl = f"SELECT * FROM users WHERE user_key = {user_key}"
#     cur.execute(avl)
#     squr = cur.fetchall()
#     if squr ==[]:
#       qury =f"INSERT INTO users (user_key, username, JobTitle) VALUES (%s,%s,%s);"
#       val = (user_key, username, skills)
#       cur.execute(qury,val)
#       context.bot.send_message(chat_id=update.message.chat_id, text=f"registration complete")
#     else:
#       context.bot.send_message(chat_id=update.message.chat_id, text=f"you'r already register {username}")

    
    
conn.commit()
    
    # Send the job data to the user

bot = telegram.Bot(token='6224747889:AAE_ox7z8etC0_G8C5owm67Be644-G8htl4')

# Set up an Updater to handle incoming messages
updater = Updater(token='6224747889:AAE_ox7z8etC0_G8C5owm67Be644-G8htl4', use_context=True)



# Add a command handler for the /apply command
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('details', details))

updater.dispatcher.add_handler(CallbackQueryHandler(InlineKeyboardHandler))
# Start the bot
updater.start_polling()
