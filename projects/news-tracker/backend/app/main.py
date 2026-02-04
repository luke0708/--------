from __future__ import annotations

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .auth import ensure_admin_seed
from .database import init_db, engine
from .models import Topic, Source
from .routers import auth, admin, topics, sources, articles, analysis, health
from .services.scheduler import scheduler, schedule_topics

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="新闻追踪")

import os

# ...

origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(topics.router)
app.include_router(sources.router)
app.include_router(articles.router)
app.include_router(analysis.router)


DEFAULT_TOPICS = [
    {
        "name_zh": "特朗普",
        "name_en": "Donald Trump",
        "keywords": "特朗普,川普,Trump,Donald Trump",
        "is_core": True,
    },
    {
        "name_zh": "黄金",
        "name_en": "Gold",
        "keywords": "黄金,金价,Gold,Gold price",
        "is_core": True,
    },
]

DEFAULT_SOURCES = [
    {
        "name": "Yahoo Finance",
        "url": "https://finance.yahoo.com/news/rssindex",
        "lang": "en",
        "priority": 8,
    },
    {
        "name": "Investing.com",
        "url": "https://www.investing.com/rss/news.rss",
        "lang": "en",
        "priority": 7,
    },
    {
        "name": "MarketWatch",
        "url": "http://feeds.marketwatch.com/marketwatch/topstories/",
        "lang": "en",
        "priority": 7,
    },
    {
        "name": "Fox Business",
        "url": "https://moxie.foxbusiness.com/google-publisher/latest.xml",
        "lang": "en",
        "priority": 6,
    },
    {
        "name": "Fortune",
        "url": "https://fortune.com/feed",
        "lang": "en",
        "priority": 6,
    },
#    {
#        "name": "Reuters US",
#        "url": "https://www.reuters.com/world/us/rss",
#        "lang": "en",
#        "priority": 10,
#    },
#    {
#        "name": "Reuters World",
#        "url": "https://www.reuters.com/world/rss",
#        "lang": "en",
#        "priority": 8,
#    },
    {
        "name": "CNBC Top News",
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "lang": "en",
        "priority": 6,
    },
    {
        "name": "BBC US & Canada",
        "url": "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
        "lang": "en",
        "priority": 5,
    },
    {
        "name": "FT中文网",
        "url": "http://www.ftchinese.com/rss/news",
        "lang": "zh",
        "priority": 8,
    },
#    {
#        "name": "联合早报财经",
#        "url": "https://www.zaobao.com.sg/rss/finance",
#        "lang": "zh",
#        "priority": 7,
#    },
#    {
#        "name": "Kitco Gold News",
#        "url": "https://www.kitco.com/rss/category/commodities/gold",
#        "lang": "en",
#        "priority": 10,
#    },
#    {
#        "name": "Kitco Base Metals",
#        "url": "https://www.kitco.com/rss/category/commodities/base-metals",
#        "lang": "en",
#        "priority": 9,
#    },
]


def seed_initial_data() -> None:
    with Session(engine) as session:
        if not session.exec(select(Topic)).first():
            for item in DEFAULT_TOPICS:
                session.add(Topic(**item))
            session.commit()

        if not session.exec(select(Source)).first():
            for item in DEFAULT_SOURCES:
                session.add(Source(**item))
            session.commit()

        ensure_admin_seed(session)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_initial_data()
    schedule_topics()
    if not scheduler.running:
        scheduler.start()


@app.on_event("shutdown")
def on_shutdown() -> None:
    if scheduler.running:
        scheduler.shutdown()
