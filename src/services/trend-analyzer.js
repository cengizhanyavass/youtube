const db = require('../db/database');

class TrendAnalyzer {
  constructor(youtubeApi) {
    this.api = youtubeApi;

    // @hillmotivasyon için özel arama terimleri
    this.searchQueries = {
      'kisisel_gelisim': [
        'personal development tips',
        'self improvement motivation',
        'productivity hacks',
        'morning routine successful',
        'mindset growth',
        'habits of successful people',
        'stoicism life advice',
        'discipline motivation',
        'how to change your life',
        'self development',
        'kişisel gelişim',
        'motivasyon',
        'başarı sırları',
        'özgüven geliştirme',
      ],
      'finans': [
        'passive income ideas',
        'financial freedom',
        'money management tips',
        'investing for beginners',
        'side hustle ideas',
        'how to save money',
        'wealth building strategies',
        'financial literacy',
        'para kazanma yolları',
        'yatırım tavsiyeleri',
        'finansal özgürlük',
        'borsa yatırım',
      ],
    };

    // Birden fazla bölgede arama (Hindi hariç)
    this.regions = ['US', 'GB', 'TR', 'DE', 'BR', 'FR', 'ES', 'JP', 'KR', 'AU'];
  }

  // Video'nun trending skorunu hesapla
  calculateTrendingScore(video) {
    const views = parseInt(video.statistics?.viewCount || 0);
    const likes = parseInt(video.statistics?.likeCount || 0);
    const comments = parseInt(video.statistics?.commentCount || 0);

    const publishedAt = new Date(video.snippet.publishedAt);
    const now = new Date();
    const daysSincePublished = (now - publishedAt) / (1000 * 60 * 60 * 24);

    // Günlük ortalama izlenme
    const dailyViews = daysSincePublished > 0 ? views / daysSincePublished : views;

    // Engagement oranı
    const engagement = views > 0 ? ((likes + comments * 2) / views) * 100 : 0;

    // Yenilik bonusu (son 7 gün içinde yayınlananlara bonus)
    const recencyBonus = daysSincePublished <= 7 ? 2.0 : daysSincePublished <= 30 ? 1.5 : 1.0;

    // Trending skoru = günlük izlenme * engagement * yenilik bonusu
    const score = (dailyViews * 0.4 + engagement * 1000 * 0.3 + (likes / Math.max(daysSincePublished, 1)) * 0.3) * recencyBonus;

    return Math.round(score * 100) / 100;
  }

  // Videoyu veritabanına kaydet
  saveVideo(video, channelId) {
    const stmt = db.prepare(`
      INSERT OR REPLACE INTO videos (id, channel_id, title, description, published_at,
        view_count, like_count, comment_count, duration, tags, category_id, thumbnail_url, trending_score)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    const trendingScore = this.calculateTrendingScore(video);

    stmt.run(
      video.id,
      channelId || video.snippet.channelId,
      video.snippet.title,
      video.snippet.description?.substring(0, 500) || '',
      video.snippet.publishedAt,
      parseInt(video.statistics?.viewCount || 0),
      parseInt(video.statistics?.likeCount || 0),
      parseInt(video.statistics?.commentCount || 0),
      video.contentDetails?.duration || '',
      JSON.stringify(video.snippet.tags || []),
      video.snippet.categoryId || '',
      video.snippet.thumbnails?.high?.url || video.snippet.thumbnails?.default?.url || '',
      trendingScore
    );

    return trendingScore;
  }

  // Kanalı veritabanına kaydet
  saveChannel(channel, options = {}) {
    const stmt = db.prepare(`
      INSERT OR REPLACE INTO channels (id, title, handle, description, subscriber_count,
        video_count, view_count, country, language, category, is_mine, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    `);

    stmt.run(
      channel.id,
      channel.snippet.title,
      channel.snippet.customUrl || '',
      channel.snippet.description?.substring(0, 500) || '',
      parseInt(channel.statistics?.subscriberCount || 0),
      parseInt(channel.statistics?.videoCount || 0),
      parseInt(channel.statistics?.viewCount || 0),
      channel.snippet.country || '',
      channel.snippet.defaultLanguage || '',
      options.category || '',
      options.isMine ? 1 : 0
    );
  }

  // Trend videoları topla ve analiz et
  async collectTrends(category = 'all') {
    const queries = category === 'all'
      ? [...this.searchQueries.kisisel_gelisim, ...this.searchQueries.finans]
      : this.searchQueries[category] || [];

    const results = [];
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    for (const query of queries) {
      // Farklı bölgelerde ara (kota tasarrufu için 3 bölge)
      const selectedRegions = this.regions.sort(() => Math.random() - 0.5).slice(0, 3);

      for (const region of selectedRegions) {
        const videos = await this.api.searchTrendingVideos(query, {
          regionCode: region,
          maxResults: 10,
          publishedAfter: thirtyDaysAgo.toISOString(),
        });

        for (const video of videos) {
          const score = this.saveVideo(video, video.snippet.channelId);
          results.push({
            id: video.id,
            title: video.snippet.title,
            channelTitle: video.snippet.channelTitle,
            views: parseInt(video.statistics?.viewCount || 0),
            trendingScore: score,
            query,
            region,
          });
        }
      }
    }

    // Skora göre sırala
    results.sort((a, b) => b.trendingScore - a.trendingScore);
    return results;
  }

  // En yüksek trending skorlu videoları getir
  getTopTrending(limit = 20) {
    return db.prepare(`
      SELECT v.*, c.title as channel_title, c.subscriber_count
      FROM videos v
      LEFT JOIN channels c ON v.channel_id = c.id
      ORDER BY v.trending_score DESC
      LIMIT ?
    `).all(limit);
  }

  // Son 7 günde en hızlı büyüyen videoları bul
  getFastestGrowing(limit = 15) {
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    return db.prepare(`
      SELECT v.*, c.title as channel_title,
        CAST(v.view_count AS REAL) / MAX(1, julianday('now') - julianday(v.published_at)) as daily_views
      FROM videos v
      LEFT JOIN channels c ON v.channel_id = c.id
      WHERE v.published_at >= ?
      ORDER BY daily_views DESC
      LIMIT ?
    `).all(sevenDaysAgo.toISOString(), limit);
  }

  // Belirli bir anahtar kelimenin trend durumunu kaydet
  saveTrendSnapshot(keyword, category, videos) {
    const avgViews = videos.length > 0
      ? Math.round(videos.reduce((sum, v) => sum + parseInt(v.statistics?.viewCount || 0), 0) / videos.length)
      : 0;

    const topVideo = videos.sort((a, b) =>
      parseInt(b.statistics?.viewCount || 0) - parseInt(a.statistics?.viewCount || 0)
    )[0];

    db.prepare(`
      INSERT INTO trend_snapshots (keyword, category, video_count, avg_views, top_video_id)
      VALUES (?, ?, ?, ?, ?)
    `).run(keyword, category, videos.length, avgViews, topVideo?.id || null);
  }
}

module.exports = TrendAnalyzer;
