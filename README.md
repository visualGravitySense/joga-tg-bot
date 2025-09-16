# 🧘 Yoga Learning Bot

Telegram bot for learning yoga using open data and personalized recommendations.

## 🌟 Features

- 📚 **Yoga Poses Catalog** - over 10 basic poses with detailed descriptions
- 🎯 **Personalized Recommendations** - based on user level
- 📊 **Progress Tracking** - workout statistics and achievements
- 🧘 **Pose of the Day** - daily practice recommendations
- ⚙️ **Profile Settings** - difficulty level selection
- ⭐ **Rating System** - for improving recommendations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Bot Setup

1. Create a bot in Telegram via [@BotFather](https://t.me/BotFather)
2. Get the bot token
3. Create `.env` file based on `.env.example`:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_USER_ID=your_telegram_user_id
```

### 3. Run the Bot

```bash
python bot.py
```

## 📁 Project Structure

```
yoga-bot/
├── bot.py              # Main bot file
├── config.py           # Application configuration
├── database.py         # Database operations
├── yoga_data.py        # Yoga data management
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── data/              # Data directory
├── images/            # Pose images
└── videos/            # Video lessons
```

## 🎯 Functionality

### Main Commands

- `/start` - start working with the bot
- `/help` - command help
- `/settings` - profile settings
- `/progress` - your progress
- `/pose` - random pose
- `/daily` - pose of the day

### Interactive Buttons

- 🧘 **Pose of the Day** - daily recommendation
- 📚 **Poses Catalog** - search by categories
- 📊 **My Progress** - workout statistics
- ⚙️ **Settings** - difficulty level
- 🎯 **Recommendations** - personalized advice

### Pose Categories

- **Standing** - Tadasana, Vrikshasana, Virabhadrasana I
- **Seated** - Padmasana
- **On Knees** - Marjariasana, Balasana
- **Lying** - Bhujangasana, Setu Bandhasana
- **Inversion** - Adho Mukha Svanasana
- **Resting** - Shavasana

## 🗄️ Database

The bot uses SQLite for storage:

- **Users** - profiles and settings
- **Yoga Poses** - catalog with descriptions
- **Sessions** - workout history
- **Progress** - statistics and achievements

## 🔧 Technologies

- **Python 3.8+**
- **aiogram 3.2.0** - modern library for Telegram Bot API
- **SQLite** - lightweight database
- **asyncio** - asynchronous programming

## 📈 Development Plans

- [ ] Kaggle datasets integration
- [ ] Adding pose images
- [ ] Video lessons
- [ ] Workout plans
- [ ] Social features
- [ ] Mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Create a Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

If you have questions or suggestions:

- Create an Issue on GitHub
- Write in Telegram: @your_username

---

**Created with ❤️ for learning yoga**
