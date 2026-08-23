# Senrivia Bot Architecture

## Overview
Senrivia is a Telegram bot that tracks influencer trails and metrics.

## Project Structure

- **bot/**: Core bot logic and handlers
  - `app.py`: Main bot application
  - `handlers/`: Command and message handlers
  - `keyboards/`: Telegram keyboard layouts
  - `middlewares/`: Request processing middlewares

- **admin/**: Admin web dashboard
  - `dashboard.py`: Flask web interface

- **database/**: Database layer
  - `mongo.py`: MongoDB operations

- **services/**: Business logic services
  - `analytics.py`: Analytics tracking
  - `trail.py`: Influencer trail management

- **scraper/**: Web scraping utilities
  - `fxtwitter.py`: Twitter/X data scraper

- **workers/**: Background processing
  - `scheduler.py`: Task scheduling

## Technology Stack

- **Framework**: python-telegram-bot
- **Database**: MongoDB
- **Web**: Flask
- **Task Scheduling**: APScheduler
- **API**: FXTwitter API

## Key Features

1. Real-time influencer trail tracking
2. Twitter/X data integration
3. Analytics and metrics
4. Admin dashboard
5. Background job processing
