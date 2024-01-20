from flask import Flask, render_template, redirect, url_for, session
from flask_discord import DiscordOAuth2Session, requires_authorization
import os

app = Flask(__name__)

app.config['DISCORD_CLIENT_ID'] = os.getenv('CLIENT_ID')
app.config['DISCORD_CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')
app.config['DISCORD_BOT_TOKEN'] = os.getenv('TOKEN')
app.config['DISCORD_REDIRECT_URI'] = os.getenv('REDIRECT_URL')

discord = DiscordOAuth2Session(app)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@discord.route('/login')
def login():
    return discord.create_session()

@discord.route('/callback')
def callback():
    data = discord.callback()
    session['discord_token'] = (data['access_token'], '')
    user = discord.fetch_user()
    # Save user data to database for authentication
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@requires_authorization
def dashboard():
    user = discord.fetch_user()
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
