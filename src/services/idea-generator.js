const db = require('../db/database');

class IdeaGenerator {
  constructor(trendAnalyzer) {
    this.analyzer = trendAnalyzer;

    // Türkçe video başlık şablonları
    this.titleTemplates = {
      kisisel_gelisim: [
        '{KONU} - Hayatını Değiştirecek {SAYI} Alışkanlık',
        'Başarılı İnsanların Ortak {SAYI} Özelliği ({KONU})',
        '{KONU} Hakkında Kimsenin Söylemediği Gerçekler',
        'Bu {KONU} Tekniği Hayatımı Değiştirdi (Bilimsel)',
        '{SAYI} Günde {KONU} Nasıl Geliştirilir?',
        '{KONU}: Zenginlerin Sana Söylemediği Sır',
        'Elon Musk\'un {KONU} Stratejisi (Herkes Yapabilir)',
        '{KONU} İçin En Etkili {SAYI} Yöntem (2024)',
        'Neden {KONU} Konusunda Başarısız Oluyorsun?',
        '30 Günde {KONU} Challenge - Sonuçlar İnanılmaz!',
      ],
      finans: [
        'Ayda {PARA} TL Pasif Gelir - {KONU} Yöntemi',
        '{KONU} ile Para Kazanmanın {SAYI} Yolu (Gerçekçi)',
        'Zenginler {KONU} Hakkında Ne Biliyor? (Sır Açıklandı)',
        '{PARA} TL ile {KONU} Yatırımına Başlamak',
        '{KONU} - Finansal Özgürlüğe Giden {SAYI} Adım',
        'Bu {KONU} Hatasını Yapma! (Para Kaybedersin)',
        '{SAYI} Yaşında Emekli Olmanın {KONU} Formülü',
        '{KONU} vs {KONU2}: Hangisi Daha Karlı?',
        'Warren Buffett\'ın {KONU} Stratejisi (Basit Anlatım)',
        '2024\'te {KONU} ile Zengin Olmanın Yol Haritası',
      ],
    };
  }

  // Trend videolardan fikir üret
  generateFromTrends(trendingVideos, count = 10) {
    const ideas = [];

    for (const video of trendingVideos.slice(0, count * 2)) {
      const title = video.title || '';
      const keywords = this._extractKeywords(title);
      const category = this._detectCategory(title);
      const templates = this.titleTemplates[category] || this.titleTemplates.kisisel_gelisim;

      // Her trend video için 1-2 fikir üret
      const template = templates[Math.floor(Math.random() * templates.length)];
      const idea = this._fillTemplate(template, keywords);

      ideas.push({
        title: idea,
        description: this._generateDescription(video, keywords),
        sourceVideoId: video.id,
        sourceChannelId: video.channel_id || video.channelId,
        strategy: this._determineStrategy(video),
        estimatedPotential: this._estimatePotential(video),
        tags: keywords.join(', '),
      });
    }

    // En iyi fikirleri seç ve kaydet
    const topIdeas = ideas.slice(0, count);
    for (const idea of topIdeas) {
      this._saveIdea(idea);
    }

    return topIdeas;
  }

  // Kendi kanalın en iyi videolarından fikir türet
  generateFromMyTopVideos(channelId, count = 10) {
    const myTopVideos = db.prepare(`
      SELECT * FROM videos
      WHERE channel_id = ?
      ORDER BY view_count DESC
      LIMIT 20
    `).all(channelId);

    if (myTopVideos.length === 0) return [];

    const ideas = [];

    for (const video of myTopVideos) {
      const keywords = this._extractKeywords(video.title);
      const tags = JSON.parse(video.tags || '[]');
      const allKeywords = [...keywords, ...tags.slice(0, 5)];

      // Spin-off fikirleri
      ideas.push({
        title: this._createSpinoff(video.title, 'derinlemesine'),
        description: `"${video.title}" videonuz ${video.view_count.toLocaleString()} izlenme aldı. Bu konuyu daha derinlemesine ele alan bir video yüksek potansiyele sahip.`,
        sourceVideoId: video.id,
        sourceChannelId: channelId,
        strategy: 'spin-off',
        estimatedPotential: 'yüksek',
        tags: allKeywords.join(', '),
      });

      // Serileştirme fikri
      ideas.push({
        title: `${this._extractMainTopic(video.title)} - BÖLÜM 2 (Daha Derine)`,
        description: `Hit videonuzun devamı. İzleyiciler serinin devamını bekliyor olabilir.`,
        sourceVideoId: video.id,
        sourceChannelId: channelId,
        strategy: 'series',
        estimatedPotential: 'yüksek',
        tags: allKeywords.join(', '),
      });

      // Güncellenmiş versiyon
      ideas.push({
        title: `${this._extractMainTopic(video.title)} (GÜNCEL VERSİYON)`,
        description: `Eski hit videonuzun güncellenmiş hali. Zaten ilgi gören bir konunun yeni versiyonu.`,
        sourceVideoId: video.id,
        sourceChannelId: channelId,
        strategy: 'update',
        estimatedPotential: 'orta-yüksek',
        tags: allKeywords.join(', '),
      });
    }

    const topIdeas = ideas.slice(0, count);
    for (const idea of topIdeas) {
      this._saveIdea(idea);
    }

    return topIdeas;
  }

  // Rakip kanallardan ilham al
  generateFromCompetitors(competitorVideos, count = 10) {
    const ideas = [];

    for (const video of competitorVideos) {
      const views = parseInt(video.view_count || video.statistics?.viewCount || 0);
      if (views < 10000) continue; // Sadece başarılı videolardan ilham al

      const keywords = this._extractKeywords(video.title || '');
      const category = this._detectCategory(video.title || '');
      const templates = this.titleTemplates[category] || this.titleTemplates.kisisel_gelisim;

      const template = templates[Math.floor(Math.random() * templates.length)];

      ideas.push({
        title: this._fillTemplate(template, keywords),
        description: `Rakip kanalda "${video.title}" videosu ${views.toLocaleString()} izlenme almış. Benzer konuyu kendi tarzınızda ele alın.`,
        sourceVideoId: video.id,
        sourceChannelId: video.channel_id,
        strategy: 'competitor-inspired',
        estimatedPotential: this._estimatePotentialFromViews(views),
        tags: keywords.join(', '),
      });
    }

    const topIdeas = ideas
      .sort((a, b) => {
        const order = { 'çok yüksek': 4, 'yüksek': 3, 'orta-yüksek': 2, 'orta': 1 };
        return (order[b.estimatedPotential] || 0) - (order[a.estimatedPotential] || 0);
      })
      .slice(0, count);

    for (const idea of topIdeas) {
      this._saveIdea(idea);
    }

    return topIdeas;
  }

  // Kayıtlı fikirleri getir
  getIdeas(status = null, limit = 50) {
    if (status) {
      return db.prepare(`
        SELECT vi.*, v.title as source_title, v.view_count as source_views, v.thumbnail_url
        FROM video_ideas vi
        LEFT JOIN videos v ON vi.source_video_id = v.id
        WHERE vi.status = ?
        ORDER BY vi.created_at DESC
        LIMIT ?
      `).all(status, limit);
    }

    return db.prepare(`
      SELECT vi.*, v.title as source_title, v.view_count as source_views, v.thumbnail_url
      FROM video_ideas vi
      LEFT JOIN videos v ON vi.source_video_id = v.id
      ORDER BY vi.created_at DESC
      LIMIT ?
    `).all(limit);
  }

  // Fikir durumunu güncelle
  updateIdeaStatus(ideaId, status) {
    db.prepare('UPDATE video_ideas SET status = ? WHERE id = ?').run(status, ideaId);
  }

  // --- Yardımcı Metodlar ---

  _extractKeywords(title) {
    const stopWords = new Set([
      'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
      'should', 'may', 'might', 'can', 'shall', 'to', 'of', 'in', 'for',
      'on', 'with', 'at', 'by', 'from', 'and', 'or', 'but', 'not', 'no',
      'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its',
      'our', 'their', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'how',
      'what', 'why', 'when', 'where', 'who', 'which', 'if', 'then', 'so',
      'bir', 'bu', 'şu', 've', 'ile', 'için', 'de', 'da', 'ki', 'ne',
      'nasıl', 'neden', 'çok', 'en', 'daha', 'olan', 'olarak', 'ben', 'sen',
    ]);

    return title
      .replace(/[^\w\sçğıöşüÇĞİÖŞÜ]/g, ' ')
      .split(/\s+/)
      .filter((w) => w.length > 2 && !stopWords.has(w.toLowerCase()))
      .slice(0, 8);
  }

  _detectCategory(title) {
    const lower = title.toLowerCase();
    const financeKeywords = ['money', 'invest', 'finance', 'income', 'wealth', 'rich',
      'para', 'yatırım', 'finans', 'gelir', 'zengin', 'borsa', 'kripto', 'kazanç'];
    if (financeKeywords.some((k) => lower.includes(k))) return 'finans';
    return 'kisisel_gelisim';
  }

  _fillTemplate(template, keywords) {
    let result = template;
    const topic = keywords[0] || 'Başarı';
    const topic2 = keywords[1] || 'Gelişim';
    const numbers = [3, 5, 7, 10, 15, 21, 30];
    const money = [1000, 5000, 10000, 50000];

    result = result.replace('{KONU}', topic);
    result = result.replace('{KONU2}', topic2);
    result = result.replace('{SAYI}', numbers[Math.floor(Math.random() * numbers.length)]);
    result = result.replace('{PARA}', money[Math.floor(Math.random() * money.length)]);

    return result;
  }

  _generateDescription(video, keywords) {
    const views = parseInt(video.view_count || video.statistics?.viewCount || 0);
    const channel = video.channel_title || video.snippet?.channelTitle || 'bir kanal';
    return `"${channel}" kanalında benzer bir video ${views.toLocaleString()} izlenme almış. ` +
      `Anahtar kelimeler: ${keywords.join(', ')}. Bu konuyu Türk izleyiciye uyarlayın.`;
  }

  _determineStrategy(video) {
    const views = parseInt(video.view_count || video.statistics?.viewCount || 0);
    const published = new Date(video.published_at || video.snippet?.publishedAt);
    const daysSince = (Date.now() - published) / (1000 * 60 * 60 * 24);

    if (daysSince <= 7 && views > 100000) return 'hızlı-trend-yakala';
    if (views > 1000000) return 'kanıtlanmış-konu';
    if (views > 100000) return 'yükselen-trend';
    return 'potansiyel-fırsat';
  }

  _estimatePotential(video) {
    const score = video.trending_score || video.trendingScore || 0;
    if (score > 5000) return 'çok yüksek';
    if (score > 1000) return 'yüksek';
    if (score > 500) return 'orta-yüksek';
    return 'orta';
  }

  _estimatePotentialFromViews(views) {
    if (views > 1000000) return 'çok yüksek';
    if (views > 500000) return 'yüksek';
    if (views > 100000) return 'orta-yüksek';
    return 'orta';
  }

  _createSpinoff(title, angle) {
    const mainTopic = this._extractMainTopic(title);
    const angles = {
      'derinlemesine': `${mainTopic} - Kimsenin Bilmediği Detaylar`,
      'pratik': `${mainTopic} - Pratik Uygulama Rehberi`,
      'hata': `${mainTopic} Yaparken En Sık Yapılan ${Math.floor(Math.random() * 5) + 3} Hata`,
    };
    return angles[angle] || angles['derinlemesine'];
  }

  _extractMainTopic(title) {
    // Parantez, sayı ve gereksiz kısımları temizle
    return title
      .replace(/\(.*?\)/g, '')
      .replace(/\[.*?\]/g, '')
      .replace(/[|!?]/g, '')
      .replace(/\d+/g, '')
      .trim()
      .split(/[-:]/)[0]
      .trim();
  }

  _saveIdea(idea) {
    db.prepare(`
      INSERT INTO video_ideas (title, description, source_video_id, source_channel_id,
        strategy, estimated_potential, tags)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(
      idea.title,
      idea.description,
      idea.sourceVideoId || null,
      idea.sourceChannelId || null,
      idea.strategy,
      idea.estimatedPotential,
      idea.tags
    );
  }
}

module.exports = IdeaGenerator;
