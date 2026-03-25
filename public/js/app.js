const app = {
  // API çağrısı yardımcısı
  async api(method, endpoint, body = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);

    try {
      const res = await fetch(`/api${endpoint}`, opts);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Bir hata olustu');
      return data;
    } catch (err) {
      this.toast(err.message, 'error');
      throw err;
    }
  },

  // Sayfa navigasyonu
  init() {
    document.querySelectorAll('.nav-item').forEach((item) => {
      item.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach((i) => i.classList.remove('active'));
        document.querySelectorAll('.page').forEach((p) => p.classList.remove('active'));
        item.classList.add('active');
        document.getElementById(`page-${item.dataset.page}`).classList.add('active');
        this.onPageLoad(item.dataset.page);
      });
    });

    this.loadDashboard();
  },

  onPageLoad(page) {
    switch (page) {
      case 'dashboard': this.loadDashboard(); break;
      case 'trends': this.loadTrends(); break;
      case 'ideas': this.loadIdeas(); break;
      case 'discover': this.loadChannels(); break;
      case 'my-channel': this.loadMyChannel(); break;
    }
  },

  // === DASHBOARD ===
  async loadDashboard() {
    try {
      const data = await this.api('GET', '/dashboard');

      document.getElementById('stat-channels').textContent = data.totalChannels;
      document.getElementById('stat-videos').textContent = data.totalVideos;
      document.getElementById('stat-ideas').textContent = data.totalIdeas;
      document.getElementById('stat-new-ideas').textContent = data.newIdeas;

      // Trending videolar
      const trendingEl = document.getElementById('dashboard-trending');
      if (data.topTrending && data.topTrending.length > 0) {
        trendingEl.innerHTML = data.topTrending.map((v) => this.renderVideoItem(v)).join('');
      }

      // Son fikirler
      const ideasEl = document.getElementById('dashboard-ideas');
      if (data.recentIdeas && data.recentIdeas.length > 0) {
        ideasEl.innerHTML = data.recentIdeas.map((i) => this.renderIdeaItem(i)).join('');
      }

      // Kota
      this.updateQuota(data.quota);
    } catch (e) {
      // Dashboard yüklenemedi - sorun yok
    }
  },

  // === KANAL KURULUMU ===
  async setupChannel() {
    this.showLoading('Kanal bilgileri aliniyor...');
    try {
      const data = await this.api('POST', '/channel/setup', {
        handle: '@hillmotivasyon',
      });
      this.toast(`Kanal kuruldu! ${data.channel.videos} video yuklendi.`, 'success');
      this.loadDashboard();
    } catch (e) {
      // Hata zaten toast ile gösterildi
    }
    this.hideLoading();
  },

  // === TREND TOPLAMA ===
  async collectTrends() {
    this.showLoading('Trendler toplanıyor... Bu islem biraz zaman alabilir.');
    try {
      await this.api('POST', '/trends/collect', { category: 'all' });
      this.toast('Trend toplama baslatildi! Arka planda devam ediyor.', 'info');
      // Birkaç saniye bekleyip yükle
      setTimeout(() => this.loadTrends(), 3000);
    } catch (e) {
      // Hata toast ile gösterildi
    }
    this.hideLoading();
  },

  async loadTrends() {
    const filter = document.getElementById('trend-filter')?.value || 'top';
    const endpoint = filter === 'fastest' ? '/trends/fastest' : '/trends/top';

    try {
      const data = await this.api('GET', endpoint);
      const container = document.getElementById('trends-list');

      if (data && data.length > 0) {
        container.innerHTML = data.map((v) => this.renderVideoCard(v)).join('');
      } else {
        container.innerHTML = '<p class="empty-state">Henuz trend verisi yok. "Trend Topla" butonuna basin.</p>';
      }
    } catch (e) {
      // Hata
    }
  },

  // === VIDEO FIKIRLERI ===
  async generateIdeas(source) {
    this.showLoading(`${source} kaynagindan fikirler uretiliyor...`);
    try {
      const data = await this.api('POST', '/ideas/generate', { source, count: 15 });
      this.toast(`${data.count} yeni video fikri uretildi!`, 'success');
      this.loadIdeas();
    } catch (e) {
      // Hata
    }
    this.hideLoading();
  },

  async loadIdeas() {
    const status = document.getElementById('idea-filter')?.value || '';
    const endpoint = status ? `/ideas?status=${status}` : '/ideas';

    try {
      const data = await this.api('GET', endpoint);
      const container = document.getElementById('ideas-list');

      if (data && data.length > 0) {
        container.innerHTML = data.map((i) => this.renderIdeaCard(i)).join('');
      } else {
        container.innerHTML = '<p class="empty-state">Henuz video fikri uretilmedi.</p>';
      }
    } catch (e) {
      // Hata
    }
  },

  async updateIdeaStatus(id, status) {
    try {
      await this.api('PATCH', `/ideas/${id}/status`, { status });
      this.toast('Fikir durumu guncellendi', 'success');
      this.loadIdeas();
    } catch (e) {
      // Hata
    }
  },

  // === KANAL KESFI ===
  async discoverChannels() {
    this.showLoading('Global kanallar kesfediliyor... (Hindi kanallar filtreleniyor)');
    try {
      const data = await this.api('POST', '/discover/channels', { category: 'all' });
      this.toast(`${data.discovered} yeni kanal kesfedildi!`, 'success');
      this.loadChannels();
    } catch (e) {
      // Hata
    }
    this.hideLoading();
  },

  async findSimilar() {
    this.showLoading('Benzer kanallar araniyor...');
    try {
      await this.api('POST', '/discover/similar');
      this.toast('Benzer kanallar bulundu!', 'success');
      this.loadCompetitors();
    } catch (e) {
      // Hata
    }
    this.hideLoading();
  },

  async analyzeCompetitors() {
    this.showLoading('Rakip kanallar analiz ediliyor...');
    try {
      const data = await this.api('POST', '/discover/analyze-competitors', { limit: 5 });
      this.toast(`${data.analyzed} rakip video analiz edildi!`, 'success');
    } catch (e) {
      // Hata
    }
    this.hideLoading();
  },

  async loadChannels() {
    try {
      const data = await this.api('GET', '/discover/channels');
      const container = document.getElementById('channels-list');

      if (data && data.length > 0) {
        container.innerHTML = data.map((ch) => this.renderChannelCard(ch)).join('');
      }
    } catch (e) {
      // Hata
    }
  },

  async loadCompetitors() {
    try {
      const data = await this.api('GET', '/discover/competitors');
      const container = document.getElementById('competitors-list');

      if (data && data.length > 0) {
        container.innerHTML = data.map((ch) => this.renderChannelCard(ch, true)).join('');
      }
    } catch (e) {
      // Hata
    }
  },

  // === KANALIM ===
  async loadMyChannel() {
    try {
      const channel = await this.api('GET', '/channel/my');
      const el = document.getElementById('my-channel-info');
      el.innerHTML = `
        <h3>${channel.title}</h3>
        <p style="color:var(--text-secondary);margin-bottom:15px">${channel.description || ''}</p>
        <div class="my-channel-details">
          <div class="my-channel-stat">
            <div class="number">${this.formatNumber(channel.subscriber_count)}</div>
            <div class="label">Abone</div>
          </div>
          <div class="my-channel-stat">
            <div class="number">${this.formatNumber(channel.view_count)}</div>
            <div class="label">Toplam Izlenme</div>
          </div>
          <div class="my-channel-stat">
            <div class="number">${channel.video_count}</div>
            <div class="label">Video</div>
          </div>
        </div>
      `;

      // Top videolar
      const videos = await this.api('GET', '/channel/my/top-videos?limit=10');
      const videosEl = document.getElementById('my-top-videos');
      if (videos && videos.length > 0) {
        videosEl.innerHTML = videos.map((v) => this.renderVideoItem(v)).join('');
      } else {
        videosEl.innerHTML = '<p class="empty-state">Video bulunamadi.</p>';
      }
    } catch (e) {
      // Kanal kurulmamış
    }
  },

  // === RENDER FONKSIYONLARI ===

  renderVideoCard(v) {
    const views = this.formatNumber(v.view_count || 0);
    const score = v.trending_score || 0;
    const thumb = v.thumbnail_url || '';
    const title = this.escapeHtml(v.title || '');
    const channel = this.escapeHtml(v.channel_title || '');

    return `
      <div class="video-card">
        ${thumb ? `<img class="video-card-thumb" src="${thumb}" alt="" loading="lazy">` : '<div class="video-card-thumb"></div>'}
        <div class="video-card-body">
          <div class="video-card-title">${title}</div>
          <div class="video-card-meta">
            <span>${channel}</span>
            <span>${views} izlenme</span>
          </div>
          <span class="video-card-score">Skor: ${Math.round(score)}</span>
        </div>
      </div>
    `;
  },

  renderVideoItem(v) {
    const views = this.formatNumber(v.view_count || 0);
    const thumb = v.thumbnail_url || '';
    const title = this.escapeHtml(v.title || '');

    return `
      <div class="video-item">
        ${thumb ? `<img class="video-item-thumb" src="${thumb}" alt="" loading="lazy">` : '<div class="video-item-thumb"></div>'}
        <div class="video-item-info">
          <div class="video-item-title">${title}</div>
          <div class="video-item-meta">${views} izlenme</div>
        </div>
      </div>
    `;
  },

  renderIdeaCard(idea) {
    const potential = idea.estimated_potential || 'orta';
    const potentialClass = potential.includes('yuksek') || potential.includes('yüksek')
      ? (potential.includes('cok') || potential.includes('çok') ? 'very-high' : 'high')
      : 'medium';

    return `
      <div class="idea-card">
        <div class="idea-card-title">${this.escapeHtml(idea.title)}</div>
        <div class="idea-card-desc">${this.escapeHtml(idea.description || '')}</div>
        <div class="idea-card-footer">
          <div>
            <span class="idea-tag">${this.escapeHtml(idea.strategy || '')}</span>
            <span class="idea-potential ${potentialClass}">${potential}</span>
          </div>
          <div class="idea-actions">
            <button class="btn btn-sm btn-success" onclick="app.updateIdeaStatus(${idea.id}, 'saved')">Kaydet</button>
            <button class="btn btn-sm btn-info" onclick="app.updateIdeaStatus(${idea.id}, 'planned')">Planla</button>
            <button class="btn btn-sm btn-danger" onclick="app.updateIdeaStatus(${idea.id}, 'dismissed')">Sil</button>
          </div>
        </div>
      </div>
    `;
  },

  renderIdeaItem(idea) {
    return `
      <div class="video-item">
        <div class="video-item-info">
          <div class="video-item-title" style="color:var(--accent-yellow)">${this.escapeHtml(idea.title)}</div>
          <div class="video-item-meta">${this.escapeHtml(idea.strategy || '')} - ${idea.estimated_potential || ''}</div>
        </div>
      </div>
    `;
  },

  renderChannelCard(ch, isCompetitor = false) {
    const initial = (ch.title || '?')[0].toUpperCase();
    const subs = this.formatNumber(ch.subscriber_count || 0);
    const videos = ch.video_count || 0;
    const score = ch.similarity_score ? Math.round(ch.similarity_score) : null;

    return `
      <div class="channel-card">
        <div class="channel-avatar">${initial}</div>
        <div class="channel-info">
          <div class="channel-name">${this.escapeHtml(ch.title || '')}</div>
          <div class="channel-stats">${subs} abone - ${videos} video ${ch.country ? '- ' + ch.country : ''}</div>
        </div>
        ${score !== null ? `<span class="channel-score">%${score}</span>` : ''}
      </div>
    `;
  },

  // === TAB YONETIMI ===
  switchTab(tabEl, section) {
    const parent = tabEl.closest('.page');
    parent.querySelectorAll('.tab').forEach((t) => t.classList.remove('active'));
    parent.querySelectorAll('.tab-content').forEach((c) => c.classList.remove('active'));
    tabEl.classList.add('active');
    document.getElementById(`${section}-${tabEl.dataset.tab}`).classList.add('active');

    if (tabEl.dataset.tab === 'competitors') this.loadCompetitors();
  },

  // === YARDIMCI FONKSIYONLAR ===

  formatNumber(n) {
    n = parseInt(n) || 0;
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
    return n.toString();
  },

  escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  },

  updateQuota(quota) {
    if (!quota) return;
    const el = document.getElementById('quota-info');
    el.querySelector('span').textContent = `API Kotasi: ${quota.percentage}%`;
    el.querySelector('.quota-fill').style.width = `${quota.percentage}%`;
    if (quota.percentage > 80) {
      el.querySelector('.quota-fill').style.background = 'var(--accent)';
    }
  },

  showLoading(text) {
    document.getElementById('loading-text').textContent = text || 'Yukleniyor...';
    document.getElementById('loading').style.display = 'flex';
  },

  hideLoading() {
    document.getElementById('loading').style.display = 'none';
  },

  toast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  },
};

// Başlat
document.addEventListener('DOMContentLoaded', () => app.init());
