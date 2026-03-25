const { google } = require('googleapis');
const db = require('../db/database');

class YouTubeAPI {
  constructor(apiKey) {
    this.youtube = google.youtube({
      version: 'v3',
      auth: apiKey,
    });
    this.quotaUsed = 0;
    this.dailyQuotaLimit = 10000; // Free tier limit
  }

  _trackQuota(cost) {
    this.quotaUsed += cost;
    if (this.quotaUsed > this.dailyQuotaLimit * 0.9) {
      console.warn(`[UYARI] API kotası %90'ı aştı: ${this.quotaUsed}/${this.dailyQuotaLimit}`);
    }
  }

  // Kanal ID'sini handle'dan bul
  async getChannelByHandle(handle) {
    try {
      const res = await this.youtube.channels.list({
        part: 'snippet,statistics,contentDetails',
        forHandle: handle.replace('@', ''),
      });
      this._trackQuota(1);
      if (res.data.items && res.data.items.length > 0) {
        return res.data.items[0];
      }
      return null;
    } catch (err) {
      console.error('Kanal bulunamadı:', err.message);
      return null;
    }
  }

  // Kanal ID ile bilgi al
  async getChannelById(channelId) {
    try {
      const res = await this.youtube.channels.list({
        part: 'snippet,statistics,contentDetails',
        id: channelId,
      });
      this._trackQuota(1);
      return res.data.items?.[0] || null;
    } catch (err) {
      console.error('Kanal bilgisi alınamadı:', err.message);
      return null;
    }
  }

  // Kanalın videolarını al
  async getChannelVideos(channelId, maxResults = 50) {
    try {
      const res = await this.youtube.search.list({
        part: 'snippet',
        channelId,
        maxResults: Math.min(maxResults, 50),
        order: 'date',
        type: 'video',
      });
      this._trackQuota(100);

      if (!res.data.items) return [];

      // Get video details (views, likes etc.)
      const videoIds = res.data.items.map((v) => v.id.videoId).join(',');
      const details = await this.youtube.videos.list({
        part: 'statistics,contentDetails,snippet',
        id: videoIds,
      });
      this._trackQuota(1);

      return details.data.items || [];
    } catch (err) {
      console.error('Videolar alınamadı:', err.message);
      return [];
    }
  }

  // Kanalın en çok izlenen videolarını al
  async getTopVideos(channelId, maxResults = 20) {
    try {
      const res = await this.youtube.search.list({
        part: 'snippet',
        channelId,
        maxResults: Math.min(maxResults, 50),
        order: 'viewCount',
        type: 'video',
      });
      this._trackQuota(100);

      if (!res.data.items) return [];

      const videoIds = res.data.items.map((v) => v.id.videoId).join(',');
      const details = await this.youtube.videos.list({
        part: 'statistics,contentDetails,snippet',
        id: videoIds,
      });
      this._trackQuota(1);

      return details.data.items || [];
    } catch (err) {
      console.error('Top videolar alınamadı:', err.message);
      return [];
    }
  }

  // Kategoriye göre trend videoları ara (Hindi hariç)
  async searchTrendingVideos(query, options = {}) {
    const {
      maxResults = 25,
      regionCode = 'US',
      publishedAfter = null,
      relevanceLanguage = null,
    } = options;

    try {
      const params = {
        part: 'snippet',
        q: query,
        maxResults: Math.min(maxResults, 50),
        order: 'viewCount',
        type: 'video',
        regionCode,
        videoDuration: 'medium', // 4-20 min videos
      };

      if (publishedAfter) params.publishedAfter = publishedAfter;
      if (relevanceLanguage) params.relevanceLanguage = relevanceLanguage;

      const res = await this.youtube.search.list(params);
      this._trackQuota(100);

      if (!res.data.items) return [];

      const videoIds = res.data.items.map((v) => v.id.videoId).join(',');
      const details = await this.youtube.videos.list({
        part: 'statistics,contentDetails,snippet',
        id: videoIds,
      });
      this._trackQuota(1);

      // Filter out Hindi content
      const filtered = (details.data.items || []).filter((v) => {
        const lang = v.snippet.defaultAudioLanguage || v.snippet.defaultLanguage || '';
        const title = v.snippet.title || '';
        // Exclude Hindi (hi) language videos
        if (lang.startsWith('hi')) return false;
        // Basic Hindi script detection
        if (/[\u0900-\u097F]/.test(title)) return false;
        return true;
      });

      return filtered;
    } catch (err) {
      console.error('Trend arama hatası:', err.message);
      return [];
    }
  }

  // Belirli bir kategoride popüler kanalları keşfet
  async discoverChannels(query, options = {}) {
    const { maxResults = 15, regionCode = 'US' } = options;

    try {
      const res = await this.youtube.search.list({
        part: 'snippet',
        q: query,
        maxResults,
        type: 'channel',
        order: 'relevance',
        regionCode,
      });
      this._trackQuota(100);

      if (!res.data.items) return [];

      const channelIds = res.data.items.map((c) => c.snippet.channelId).join(',');
      const details = await this.youtube.channels.list({
        part: 'snippet,statistics',
        id: channelIds,
      });
      this._trackQuota(1);

      // Filter out Hindi channels
      const filtered = (details.data.items || []).filter((ch) => {
        const country = ch.snippet.country || '';
        const lang = ch.snippet.defaultLanguage || '';
        if (lang.startsWith('hi') || country === 'IN') return false;
        if (/[\u0900-\u097F]/.test(ch.snippet.title)) return false;
        return true;
      });

      return filtered;
    } catch (err) {
      console.error('Kanal keşif hatası:', err.message);
      return [];
    }
  }

  // Popüler/trending videoları al (bölgeye göre)
  async getTrendingVideos(regionCode = 'US', categoryId = '27') {
    // 27 = Education
    try {
      const res = await this.youtube.videos.list({
        part: 'snippet,statistics,contentDetails',
        chart: 'mostPopular',
        regionCode,
        videoCategoryId: categoryId,
        maxResults: 25,
      });
      this._trackQuota(1);

      const filtered = (res.data.items || []).filter((v) => {
        const lang = v.snippet.defaultAudioLanguage || v.snippet.defaultLanguage || '';
        if (lang.startsWith('hi')) return false;
        if (/[\u0900-\u097F]/.test(v.snippet.title)) return false;
        return true;
      });

      return filtered;
    } catch (err) {
      console.error('Trending hatası:', err.message);
      return [];
    }
  }

  // Kota durumunu kontrol et
  getQuotaStatus() {
    return {
      used: this.quotaUsed,
      limit: this.dailyQuotaLimit,
      remaining: this.dailyQuotaLimit - this.quotaUsed,
      percentage: Math.round((this.quotaUsed / this.dailyQuotaLimit) * 100),
    };
  }
}

module.exports = YouTubeAPI;
