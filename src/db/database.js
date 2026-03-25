const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DATA_DIR = path.join(__dirname, '../../data');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const db = new Database(path.join(DATA_DIR, 'youtube-growth.db'));

// WAL mode for better performance
db.pragma('journal_mode = WAL');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS channels (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    handle TEXT,
    description TEXT,
    subscriber_count INTEGER DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    country TEXT,
    language TEXT,
    category TEXT,
    is_mine INTEGER DEFAULT 0,
    discovered_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
  );

  CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY,
    channel_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    published_at TEXT,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    duration TEXT,
    tags TEXT,
    category_id TEXT,
    thumbnail_url TEXT,
    trending_score REAL DEFAULT 0,
    collected_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (channel_id) REFERENCES channels(id)
  );

  CREATE TABLE IF NOT EXISTS video_ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    source_video_id TEXT,
    source_channel_id TEXT,
    strategy TEXT,
    estimated_potential TEXT,
    tags TEXT,
    status TEXT DEFAULT 'new',
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (source_video_id) REFERENCES videos(id)
  );

  CREATE TABLE IF NOT EXISTS trend_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    category TEXT,
    region TEXT DEFAULT 'TR',
    video_count INTEGER,
    avg_views INTEGER,
    top_video_id TEXT,
    snapshot_date TEXT DEFAULT (date('now'))
  );

  CREATE TABLE IF NOT EXISTS competitor_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT NOT NULL,
    similarity_score REAL DEFAULT 0,
    notes TEXT,
    added_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (channel_id) REFERENCES channels(id)
  );

  CREATE INDEX IF NOT EXISTS idx_videos_channel ON videos(channel_id);
  CREATE INDEX IF NOT EXISTS idx_videos_views ON videos(view_count DESC);
  CREATE INDEX IF NOT EXISTS idx_videos_trending ON videos(trending_score DESC);
  CREATE INDEX IF NOT EXISTS idx_video_ideas_status ON video_ideas(status);
`);

module.exports = db;
