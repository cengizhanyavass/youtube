require('dotenv').config();
const express = require('express');
const path = require('path');
const cron = require('node-cron');

const YouTubeAPI = require('./services/youtube-api');
const TrendAnalyzer = require('./services/trend-analyzer');
const IdeaGenerator = require('./services/idea-generator');
const ChannelDiscovery = require('./services/channel-discovery');
const createApiRouter = require('./routes/api');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// API Key kontrolü
const API_KEY = process.env.YOUTUBE_API_KEY;
if (!API_KEY || API_KEY === 'YOUR_API_KEY_HERE') {
  console.error('╔════════════════════════════════════════════════════════════╗');
  console.error('║  UYARI: YouTube API anahtarı bulunamadı!                  ║');
  console.error('║  .env dosyasına YOUTUBE_API_KEY değerini ekleyin.         ║');
  console.error('║  Rehber için README.md dosyasını okuyun.                  ║');
  console.error('║  Uygulama demo modunda başlatılıyor...                    ║');
  console.error('╚════════════════════════════════════════════════════════════╝');
}

// Servisleri başlat
const youtubeApi = new YouTubeAPI(API_KEY || 'demo');
const trendAnalyzer = new TrendAnalyzer(youtubeApi);
const ideaGenerator = new IdeaGenerator(trendAnalyzer);
const channelDiscovery = new ChannelDiscovery(youtubeApi, trendAnalyzer);

// API routes
app.use('/api', createApiRouter({ youtubeApi, trendAnalyzer, ideaGenerator, channelDiscovery }));

// SPA fallback
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Zamanlanmış görevler (her gün sabah 08:00'de)
cron.schedule('0 8 * * *', async () => {
  console.log('[CRON] Günlük trend toplama başlatıldı...');
  try {
    const trends = await trendAnalyzer.collectTrends('all');
    console.log(`[CRON] ${trends.length} trend video toplandı`);

    const trending = trendAnalyzer.getTopTrending(30);
    const ideas = ideaGenerator.generateFromTrends(trending, 5);
    console.log(`[CRON] ${ideas.length} yeni video fikri üretildi`);
  } catch (err) {
    console.error('[CRON] Hata:', err.message);
  }
});

// Haftalık kanal keşfi (her Pazartesi 09:00)
cron.schedule('0 9 * * 1', async () => {
  console.log('[CRON] Haftalık kanal keşfi başlatıldı...');
  try {
    const channels = await channelDiscovery.discoverNewChannels('all');
    console.log(`[CRON] ${channels.length} yeni kanal keşfedildi`);
  } catch (err) {
    console.error('[CRON] Hata:', err.message);
  }
});

app.listen(PORT, () => {
  console.log('');
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║       🎬 YouTube Büyüme Asistanı - @hillmotivasyon       ║');
  console.log('╠════════════════════════════════════════════════════════════╣');
  console.log(`║  Sunucu: http://localhost:${PORT}                           ║`);
  console.log('║  Niş: Kişisel Gelişim + Finans/Yatırım                   ║');
  console.log('║  Hedef: Global trend analiz (Hindi hariç)                 ║');
  console.log('╚════════════════════════════════════════════════════════════╝');
  console.log('');
});
