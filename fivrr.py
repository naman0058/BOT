import telegram
import mysql.connector
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='db-mysql-blr1-69812-do-user-12247241-0.b.db.ondigitalocean.com',
    user='doadmin',
    passwd='AVNS_y2INtIf0l_w0ZJgiY29',
    database='leads',
    port=25060
)
cur = conn.cursor()

# Create necessary tables if they don't exist
cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INT AUTO_INCREMENT PRIMARY KEY, user_key BIGINT, username VARCHAR(255), Balance INT NOT NULL DEFAULT 0)")
cur.execute("CREATE TABLE IF NOT EXISTS jobs(job_id INT AUTO_INCREMENT PRIMARY KEY, topic VARCHAR(255) DEFAULT NULL, Client VARCHAR(255) DEFAULT NULL, description TEXT DEFAULT NULL, Category VARCHAR(255) DEFAULT NULL, phoneno VARCHAR(255) DEFAULT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS leaddata(lead_id INT AUTO_INCREMENT PRIMARY KEY, job_id INT DEFAULT NULL, user_key BIGINT DEFAULT NULL, date DATETIME DEFAULT NULL)")


def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    username = update.message.chat.username or update.message.chat.first_name or update.message.chat.last_name
    
    cur.execute("SELECT * FROM users WHERE user_key = %s", (user_id,))
    user = cur.fetchone()
    
    if user is None:
        cur.execute("INSERT INTO users(user_key, username) VALUES (%s, %s)", (user_id, username))
        conn.commit()
        
        context.bot.send_message(chat_id=user_id, text="Welcome to India's first Telegram Bot for finding freelance work with client's contact numbers. Get started by typing /start to get new leads every time.\n\nAs a welcome gift, we are providing 2 free leads for you to get started.")
        
    else:
        context.bot.send_message(chat_id=user_id, text="Welcome back!")
    
    # Get and send the job data for today and yesterday to the user
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    cur.execute("SELECT j.*, (SELECT COUNT(l.lead_id) FROM leaddata l WHERE l.job_id = j.job_id) AS counter FROM jobs j WHERE DATE(date) BETWEEN %s AND %s", (yesterday, today))
    jobs = cur.fetchall()
    
    for job in jobs:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Pick Leads', callback_data=job[0])]])
        context.bot.send_message(chat_id=user_id, text=f"Title: {job[1]}\nDescription: {job[3]}\nContact: {'X'*(len(job[5])-2)}{job[5][-2:]}\nName: {job[2]}\nDate: {job[6]}\nResponsed: {job[7]}", reply_markup=reply_markup)
    
    # Print when a user comes
    print(f"User {user_id} ({username}) has started the bot.")


def inline_keyboard_handler(update: Update, context: CallbackContext):
    user_key = update.callback_query.message.chat_id
    option = update.callback_query.data
    
    cur.execute("SELECT * FROM leaddata WHERE job_id = %s AND user_key = %s", (option, user_key))
    lead = cur.fetchone()
    
    if lead is None:
        cur.execute("SELECT * FROM users WHERE user_key = %s", (user_key,))
        user = cur.fetchone()
        
        if user[3] >= 25 or user[3] is None:
            cur.execute("UPDATE users SET Balance = Balance - 25 WHERE user_key = %s", (user_key,))
            today = datetime.now()
            cur.execute("INSERT INTO leaddata(job_id, user_key, date) VALUES (%s, %s, %s)", (option, user_key, today))
            conn.commit()
            
            cur.execute("SELECT * FROM jobs WHERE job_id = %s", (option,))
            job = cur.fetchone()
            
            context.bot.send_message(chat_id=user_key, text=f"Title: {job[1]}\nDescription: {job[3]}\nContact: {job[5]}\nName: {job[2]}\nDate: {job[6]}")
            
            # Print when a user picks a lead
            print(f"User {user_key} has picked lead {option}.")
        else:
            context.bot.send_message(chat_id=user_key, text=f"Dear valued customer, we would like to inform you that your account balance is currently low. To continue receiving unlimited leads, we recommend recharging your account by selecting one of the following plans:\n\nRs. 100 for one month (https://filemakr.com/monthly-recharge/{user_key})\n\nTo proceed with the recharge, please click on the respective plan. If you have any further inquiries or concerns, please do not hesitate to contact us at @taskTango. Your unique identification number is {user_key}. Thank you for choosing our services.")
    
    else:
        cur.execute("SELECT * FROM jobs WHERE job_id = %s", (option,))
        job = cur.fetchone()
        
        context.bot.send_message(chat_id=user_key, text=f"Title: {job[1]}\nDescription: {job[3]}\nContact: {job[5]}\nName: {job[2]}\nDate: {job[6]}")


def details(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    
    cur.execute("SELECT * FROM users WHERE user_key = %s", (user_id,))
    user = cur.fetchone()
    
    if user is not None:
        context.bot.send_message(chat_id=user_id, text=f"Username: {user[2]}\nUser ID: {user[1]}\nBalance: {user[3]}")
    else:
        context.bot.send_message(chat_id=user_id, text="User details not found.")


# Create a new Telegram bot with the provided token
bot_token = '6224747889:AAE_ox7z8etC0_G8C5owm67Be644-G8htl4'
bot = telegram.Bot(token=bot_token)

# Set up an Updater to handle incoming messages
updater = Updater(token=bot_token, use_context=True)

# Add command and callback handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('details', details))
updater.dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_handler))

# Start the bot
updater.start_polling()
