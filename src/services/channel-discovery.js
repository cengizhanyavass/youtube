const db = require('../db/database');

class ChannelDiscovery {
  constructor(youtubeApi, trendAnalyzer) {
    this.api = youtubeApi;
    this.analyzer = trendAnalyzer;

    // Keşfedilecek kanal kategorileri ve arama terimleri
    this.discoveryQueries = {
      kisisel_gelisim: [
        'personal development channel',
        'self improvement motivation',
        'productivity mindset',
        'stoicism philosophy',
        'life coaching tips',
        'success motivation channel',
        'motivasyon kanalı',
      ],
      finans: [
        'personal finance education',
        'investing for beginners channel',
        'financial freedom tips',
        'passive income strategies',
        'money management channel',
        'finans eğitim kanalı',
      ],
      genel_ilham: [
        'educational content creator',
        'TED talks style',
        'explainer channel',
        'infographic video',
      ],
    };

    // Global bölgeler (Hindistan hariç)
    this.regions = ['US', 'GB', 'DE', 'FR', 'BR', 'ES', 'TR', 'AU', 'CA', 'JP', 'KR', 'NL', 'SE', 'IT'];
  }

  // Yeni kanalları keşfet ve veritabanına kaydet
  async discoverNewChannels(category = 'all', maxPerQuery = 10) {
    const queries = category === 'all'
      ? Object.values(this.discoveryQueries).flat()
      : this.discoveryQueries[category] || [];

    const discovered = [];
    const existingIds = new Set(
      db.prepare('SELECT id FROM channels').all().map((r) => r.id)
    );

    for (const query of queries) {
      // Her sorgu için rastgele 2 bölge seç
      const regions = this.regions.sort(() => Math.random() - 0.5).slice(0, 2);

      for (const region of regions) {
        const channels = await this.api.discoverChannels(query, {
          maxResults: maxPerQuery,
          regionCode: region,
        });

        for (const channel of channels) {
          if (existingIds.has(channel.id)) continue;
          existingIds.add(channel.id);

          const subs = parseInt(channel.statistics?.subscriberCount || 0);
          // En az 1000 abonesi olan kanalları kaydet
          if (subs < 1000) continue;

          this.analyzer.saveChannel(channel, { category });
          discovered.push({
            id: channel.id,
            title: channel.snippet.title,
            subscribers: subs,
            videoCount: parseInt(channel.statistics?.videoCount || 0),
            country: channel.snippet.country || 'N/A',
            region,
          });
        }
      }
    }

    return discovered;
  }

  // Benzer kanal bul (kendi kanalına benzeyen)
  async findSimilarChannels(myChannelId) {
    // Kendi kanalımın bilgilerini al
    const myChannel = db.prepare('SELECT * FROM channels WHERE id = ?').get(myChannelId);
    if (!myChannel) return [];

    const mySubs = myChannel.subscriber_count;

    // Benzer abone sayısına sahip kanalları bul (0.1x - 50x arası)
    const similar = db.prepare(`
      SELECT c.*,
        ABS(CAST(c.subscriber_count AS REAL) / MAX(?, 1) - 1) as size_diff
      FROM channels c
      WHERE c.is_mine = 0
        AND c.subscriber_count >= ?
        AND c.subscriber_count <= ?
      ORDER BY size_diff ASC
      LIMIT 30
    `).all(mySubs, Math.floor(mySubs * 0.1), mySubs * 50);

    // Benzerlik skoru hesapla ve kaydet
    for (const channel of similar) {
      const similarity = this._calculateSimilarity(myChannel, channel);

      db.prepare(`
        INSERT OR REPLACE INTO competitor_channels (channel_id, similarity_score, notes)
        VALUES (?, ?, ?)
      `).run(channel.id, similarity, `Benzer kanal: ${channel.title}`);
    }

    return similar.map((ch) => ({
      ...ch,
      similarity: this._calculateSimilarity(myChannel, ch),
    })).sort((a, b) => b.similarity - a.similarity);
  }

  // Rakip kanalların başarılı videolarını analiz et
  async analyzeCompetitorVideos(limit = 5) {
    const competitors = db.prepare(`
      SELECT cc.*, c.title, c.subscriber_count
      FROM competitor_channels cc
      JOIN channels c ON cc.channel_id = c.id
      ORDER BY cc.similarity_score DESC
      LIMIT ?
    `).all(limit);

    const allVideos = [];

    for (const comp of competitors) {
      const videos = await this.api.getTopVideos(comp.channel_id, 10);

      for (const video of videos) {
        this.analyzer.saveVideo(video, comp.channel_id);
        allVideos.push({
          ...video,
          competitorTitle: comp.title,
          competitorSubs: comp.subscriber_count,
        });
      }
    }

    return allVideos;
  }

  // Keşfedilen kanalları listele
  getDiscoveredChannels(options = {}) {
    const { limit = 50, minSubs = 0, sortBy = 'subscriber_count' } = options;

    const validSorts = ['subscriber_count', 'video_count', 'view_count', 'discovered_at'];
    const sort = validSorts.includes(sortBy) ? sortBy : 'subscriber_count';

    return db.prepare(`
      SELECT c.*, cc.similarity_score
      FROM channels c
      LEFT JOIN competitor_channels cc ON c.id = cc.channel_id
      WHERE c.is_mine = 0 AND c.subscriber_count >= ?
      ORDER BY ${sort} DESC
      LIMIT ?
    `).all(minSubs, limit);
  }

  // Rakip kanalları listele
  getCompetitors(limit = 20) {
    return db.prepare(`
      SELECT cc.*, c.title, c.handle, c.subscriber_count, c.video_count, c.view_count, c.country
      FROM competitor_channels cc
      JOIN channels c ON cc.channel_id = c.id
      ORDER BY cc.similarity_score DESC
      LIMIT ?
    `).all(limit);
  }

  // Benzerlik hesaplama
  _calculateSimilarity(myChannel, otherChannel) {
    let score = 0;

    // Abone sayısı benzerliği (max 30 puan)
    const subRatio = Math.min(myChannel.subscriber_count, otherChannel.subscriber_count) /
      Math.max(myChannel.subscriber_count, otherChannel.subscriber_count, 1);
    score += subRatio * 30;

    // Aynı kategori (20 puan)
    if (myChannel.category && myChannel.category === otherChannel.category) {
      score += 20;
    }

    // Video sayısı benzerliği (max 15 puan)
    const videoRatio = Math.min(myChannel.video_count, otherChannel.video_count) /
      Math.max(myChannel.video_count, otherChannel.video_count, 1);
    score += videoRatio * 15;

    // Aynı dil/ülke (15 puan)
    if (otherChannel.country === myChannel.country) {
      score += 15;
    }

    // Aktif kanal bonusu - video sayısına göre (max 20 puan)
    if (otherChannel.video_count > 50) score += 20;
    else if (otherChannel.video_count > 20) score += 10;
    else score += 5;

    return Math.round(score * 100) / 100;
  }
}

module.exports = ChannelDiscovery;
