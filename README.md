# Senrivia Bot

**Where influencers have a trail**

Senrivia is a comprehensive Telegram bot designed to track and analyze influencer trails across social media platforms, particularly Twitter/X.

## Features

- 📊 Real-time influencer trail tracking
- 🐦 Twitter/X data integration via FXTwitter
- 📈 Advanced analytics and metrics
- 👨‍💼 Admin dashboard for management
- ⏰ Background job processing
- 🗄️ MongoDB data persistence

## Quick Start

### Prerequisites
- Python 3.8+
- MongoDB
- Telegram Bot Token

### Installation

```bash
# Clone the repository
git clone https://github.com/Vickonweb3/Senrevia-.git
cd Senrevia-

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Running the Bot

```bash
python main.py
```

## Project Structure

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Configuration

All configuration is managed through environment variables in `.env` file. See `.env.example` for all available options.

## API Reference

### Commands
- `/start` - Start the bot
- `/settings` - Manage user settings
- `/watchlist` - Manage watchlists
- `/admin` - Admin commands (admin only)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the development team.
