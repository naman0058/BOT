import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import   MessageHandler, Filters ,Updater, CommandHandler, ConversationHandler, CallbackContext, CallbackQueryHandler
import mysql.connector
from datetime import datetime
# # Connect to the SQLite database
conn = mysql.connector.connect(
  host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
  user ="doadmin",
  passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
  database="leads",
  port=25060
)
cur = conn.cursor()
# def dbcon():
#     conn = mysql.connector.connect(
#       host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
#       user ="doadmin",
#       passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
#       database="leads",
#       port=25060
#     )
#     cur = conn.cursor()
#     return cur


cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INT AUTO_INCREMENT PRIMARY KEY ,user_key BIGINT , username VARCHAR(255)  , Balance INT NOT NULL DEFAULT 0  )")
cur.execute("CREATE TABLE IF NOT EXISTS jobs(job_id INT AUTO_INCREMENT PRIMARY KEY ,topic VARCHAR(255) DEFAULT NULL,Client VARCHAR(255) DEFAULT NULL, description TEXT DEFAULT NULL, Category VARCHAR(255) DEFAULT NULL, phoneno VARCHAR(255) DEFAULT NULL  )")
cur.execute("CREATE TABLE IF NOT EXISTS leaddata(lead_id INT AUTO_INCREMENT PRIMARY KEY ,job_id INT DEFAULT NULL,user_key BIGINT DEFAULT NULL , date DATETIME DEFAULT NULL)")


# Define a function to handle the /jobs command


# Define a function to handle the /apply command
def start(update, context):
    conn = mysql.connector.connect(
      host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
      user ="doadmin",
      passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
      database="leads",
      port=25060
    )
    cur = conn.cursor()
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
      avl1 = f"SELECT * FROM users WHERE user_key = {user_iid}"
      cur.execute(avl1)
      squr1 = cur.fetchall()[0]
      
      context.bot.send_message(chat_id=user_iid, text=f"Hello {squr1[2].upper()}")
      cur.execute("SELECT * FROM jobs")
      jobs=cur.fetchall()
      yourjob = []
      for y in jobs:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Pick Leads', callback_data=y[0])],])
        context.bot.send_message(chat_id=user_iid, text=f"Title -: {y[1]}\nDescription -: {y[3]}\nContact -: {'X'*(len(y[5])-2)}{y[5][-2:]}\nName -: {y[2]}\nDate -: {y[6]}" , reply_markup=reply_markup)
    else :
      avl2 = f"SELECT * FROM users WHERE user_key = {user_iid}"
      cur.execute(avl2)
      squr = cur.fetchall()[0]
      context.bot.send_message(chat_id=user_iid, text=f"Hello {squr[2].upper()}")
      context.bot.send_message(chat_id=user_iid, text=f"finding your job ...")
      
      cur.execute("SELECT * FROM jobs")
      jobs=cur.fetchall()
      yourjob = []
      for y in jobs:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Pick Leads', callback_data=y[0])],])
        context.bot.send_message(chat_id=user_iid, text=f"Title -: {y[1]}\nDescription -: {y[3]}\nContact -: {'X'*(len(y[5])-2)}{y[5][-2:]}\nName -: {y[2]}\nDate -: {y[6]}" , reply_markup=reply_markup)
    conn.commit()
        
def InlineKeyboardHandler(update: Update, _: CallbackContext):
    
    conn = mysql.connector.connect(
      host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
      user ="doadmin",
      passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
      database="leads",
      port=25060
    )

    cur = conn.cursor()

    user_key = update.callback_query.message.chat_id
    option=update.callback_query.data
    avl1 = f"SELECT * FROM leaddata WHERE job_id = {option} AND user_key = {user_key}"
    cur.execute(avl1)
    lead = cur.fetchall()
    if lead == []:
        avl = f"SELECT * FROM users WHERE user_key = {user_key}"
        cur.execute(avl)

        bal = cur.fetchall()[0][3]
        print(bal)
        # print(update)
        if bal >=25 or bal == None:
            upd="UPDATE users SET Balance = Balance-25 WHERE user_key = %s ;"
            val =tuple([user_key])
            today = datetime.now()
            cur.execute(upd,val)
            exe="INSERT INTO leaddata(job_id, user_key,date) VALUES (%s,%s,%s);"
            val1 =tuple([option,user_key,today])

            cur.execute(exe,val1)
            # conn.commit()
            
            
            job = f"SELECT * FROM jobs WHERE job_id = {option}"
            cur.execute(job)
            y = cur.fetchall()[0]
            
            _.bot.send_message(chat_id=user_key, text=f"Title -: {y[1]}\nDescription -: {y[3]}\nContact -:{y[5]}\nName -:{y[2]}" )
        else:
            
            _.bot.send_message(chat_id=user_key, text=f"hii Your balance is low . Please recharge your account by clicking on below contact ID\n@Namam0058 \nYour Unique ID -: {user_key}" ,)
    
    else:
        job = f"SELECT * FROM jobs WHERE job_id = {option}"
        cur.execute(job)
        y = cur.fetchall()[0]
        
        _.bot.send_message(chat_id=user_key, text=f"Title -: {y[1]}\nDescription -: {y[3]}\nContact -:{y[5]}\nName -:{y[2]}" )
    conn.commit()
    
    
def details(update, context):
    conn = mysql.connector.connect(
      host ='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
      user ="doadmin",
      passwd ="AVNS_y2INtIf0l_w0ZJgiY29",
      database="leads",
      port=25060
    )
    cur = conn.cursor()
    user_iid = update.message.chat_id
    usernamee = update.message.chat.username 
    avl = f"SELECT * FROM users WHERE user_key = {user_iid}"
    cur.execute(avl)
    squr = cur.fetchall()[0]
    context.bot.send_message(chat_id=user_iid, text=f"username {squr[2]} \n user ID:{squr[1]} \n ********\n Balance: {squr[3]}")
    conn.commit()



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
    # 
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
