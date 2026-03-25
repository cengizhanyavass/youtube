const express = require('express');
const router = express.Router();

module.exports = function createApiRouter(services) {
  const { youtubeApi, trendAnalyzer, ideaGenerator, channelDiscovery } = services;

  // === DASHBOARD ===
  router.get('/dashboard', (req, res) => {
    try {
      const db = require('../db/database');
      const stats = {
        totalChannels: db.prepare('SELECT COUNT(*) as c FROM channels').get().c,
        totalVideos: db.prepare('SELECT COUNT(*) as c FROM videos').get().c,
        totalIdeas: db.prepare('SELECT COUNT(*) as c FROM video_ideas').get().c,
        newIdeas: db.prepare("SELECT COUNT(*) as c FROM video_ideas WHERE status = 'new'").get().c,
        topTrending: trendAnalyzer.getTopTrending(5),
        recentIdeas: ideaGenerator.getIdeas(null, 5),
        quota: youtubeApi.getQuotaStatus(),
      };
      res.json(stats);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  // === KANAL ===
  router.post('/channel/setup', async (req, res) => {
    try {
      const handle = req.body.handle || '@hillmotivasyon';
      const channel = await youtubeApi.getChannelByHandle(handle);
      if (!channel) return res.status(404).json({ error: 'Kanal bulunamadı' });

      trendAnalyzer.saveChannel(channel, { isMine: true, category: 'egitim' });

      // Kanalın videolarını da topla
      const videos = await youtubeApi.getChannelVideos(channel.id, 50);
      for (const v of videos) {
        trendAnalyzer.saveVideo(v, channel.id);
      }

      res.json({
        message: 'Kanal başarıyla kuruldu!',
        channel: {
          id: channel.id,
          title: channel.snippet.title,
          subscribers: channel.statistics.subscriberCount,
          videos: videos.length,
        },
      });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  router.get('/channel/my', (req, res) => {
    const db = require('../db/database');
    const channel = db.prepare('SELECT * FROM channels WHERE is_mine = 1').get();
    if (!channel) return res.status(404).json({ error: 'Kanal henüz kurulmadı. POST /api/channel/setup kullanın.' });
    res.json(channel);
  });

  router.get('/channel/my/top-videos', (req, res) => {
    const db = require('../db/database');
    const channel = db.prepare('SELECT * FROM channels WHERE is_mine = 1').get();
    if (!channel) return res.status(404).json({ error: 'Kanal henüz kurulmadı' });

    const limit = parseInt(req.query.limit) || 20;
    const videos = db.prepare(`
      SELECT * FROM videos WHERE channel_id = ? ORDER BY view_count DESC LIMIT ?
    `).all(channel.id, limit);
    res.json(videos);
  });

  // === TREND ANALİZ ===
  router.post('/trends/collect', async (req, res) => {
    try {
      const category = req.body.category || 'all';
      res.json({ message: 'Trend toplama başlatıldı...', status: 'started' });

      // Arka planda topla
      trendAnalyzer.collectTrends(category).then((results) => {
        console.log(`[TREND] ${results.length} trend video toplandı`);
      });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  router.get('/trends/top', (req, res) => {
    const limit = parseInt(req.query.limit) || 20;
    const trending = trendAnalyzer.getTopTrending(limit);
    res.json(trending);
  });

  router.get('/trends/fastest', (req, res) => {
    const limit = parseInt(req.query.limit) || 15;
    const fastest = trendAnalyzer.getFastestGrowing(limit);
    res.json(fastest);
  });

  // === VİDEO FİKİRLERİ ===
  router.post('/ideas/generate', async (req, res) => {
    try {
      const { source = 'trends', count = 10 } = req.body;
      let ideas = [];

      if (source === 'trends') {
        const trending = trendAnalyzer.getTopTrending(30);
        ideas = ideaGenerator.generateFromTrends(trending, count);
      } else if (source === 'my-videos') {
        const db = require('../db/database');
        const channel = db.prepare('SELECT * FROM channels WHERE is_mine = 1').get();
        if (!channel) return res.status(404).json({ error: 'Önce kanalınızı kurun' });
        ideas = ideaGenerator.generateFromMyTopVideos(channel.id, count);
      } else if (source === 'competitors') {
        const db = require('../db/database');
        const compVideos = db.prepare(`
          SELECT v.* FROM videos v
          JOIN competitor_channels cc ON v.channel_id = cc.channel_id
          ORDER BY v.view_count DESC LIMIT 50
        `).all();
        ideas = ideaGenerator.generateFromCompetitors(compVideos, count);
      }

      res.json({ count: ideas.length, ideas });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  router.get('/ideas', (req, res) => {
    const status = req.query.status || null;
    const limit = parseInt(req.query.limit) || 50;
    const ideas = ideaGenerator.getIdeas(status, limit);
    res.json(ideas);
  });

  router.patch('/ideas/:id/status', (req, res) => {
    const { status } = req.body;
    if (!['new', 'saved', 'planned', 'done', 'dismissed'].includes(status)) {
      return res.status(400).json({ error: 'Geçersiz durum' });
    }
    ideaGenerator.updateIdeaStatus(req.params.id, status);
    res.json({ message: 'Güncellendi' });
  });

  // === KANAL KEŞİF ===
  router.post('/discover/channels', async (req, res) => {
    try {
      const category = req.body.category || 'all';
      const channels = await channelDiscovery.discoverNewChannels(category);
      res.json({ discovered: channels.length, channels });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  router.post('/discover/similar', async (req, res) => {
    try {
      const db = require('../db/database');
      const myChannel = db.prepare('SELECT * FROM channels WHERE is_mine = 1').get();
      if (!myChannel) return res.status(404).json({ error: 'Önce kanalınızı kurun' });

      const similar = await channelDiscovery.findSimilarChannels(myChannel.id);
      res.json(similar);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  router.post('/discover/analyze-competitors', async (req, res) => {
    try {
      const limit = parseInt(req.body.limit) || 5;
      const videos = await channelDiscovery.analyzeCompetitorVideos(limit);
      res.json({ analyzed: videos.length, message: 'Rakip videolar analiz edildi' });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  router.get('/discover/channels', (req, res) => {
    const options = {
      limit: parseInt(req.query.limit) || 50,
      minSubs: parseInt(req.query.minSubs) || 0,
      sortBy: req.query.sortBy || 'subscriber_count',
    };
    res.json(channelDiscovery.getDiscoveredChannels(options));
  });

  router.get('/discover/competitors', (req, res) => {
    const limit = parseInt(req.query.limit) || 20;
    res.json(channelDiscovery.getCompetitors(limit));
  });

  // === KOTA ===
  router.get('/quota', (req, res) => {
    res.json(youtubeApi.getQuotaStatus());
  });

  return router;
};
