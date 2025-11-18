# AI Destekli Geliştirici Verimlilik Analizi

Geliştirici performansı ve AI kullanımının yazılım geliştirme süreçlerine etkisini ölçümlemek için tasarlanmış kapsamlı bir analiz ve görselleştirme platformu.

## 📊 Genel Bakış

Bu proje, yazılım geliştirme ekiplerinin verimliliğini ve AI araçlarının (özellikle Cursor IDE) bu verimliliğe etkisini analiz etmek için üç temel veri kaynağını kullanmaktadır:

- **Git Metrics**: Commit analizi, commit kategorileri, geliştirici verimliliği
- **DORA Metrics**: Deployment frequency, Lead Time, Change Failure Rate metrikleri
- **Cursor Metrics**: AI kullanım istatistikleri, kabul oranları, üretkenlik skorları

## ⚠️ Önemli Not

**Bu analiz ve dashboard, kişi değerlendirme amacı taşımaz; yalnızca proje ve geliştirme sürecindeki gelişim alanlarına dair genel bilgi sağlar.**

## 🎯 Amaç

- Geliştirici üretkenliğini objektif metriklerle ölçümlemek
- AI asistan araçlarının kod kalitesi ve hıza etkisini anlamak
- DORA metriklerini takip ederek sürekli iyileştirme alanlarını belirlemek
- Takım ve proje bazında karşılaştırmalı analizler yapmak

## 🏗️ Mimari

```
┌─────────────────┐
│   Git Repos     │──┐
└─────────────────┘  │
                     │    ┌──────────────┐
┌─────────────────┐  ├───▶│   Scripts    │──┐
│   SQL Server    │──┘    └──────────────┘  │
└─────────────────┘                         │    ┌────────────────┐
                                            ├───▶│ Elasticsearch  │
┌─────────────────┐       ┌──────────────┐ │    └────────────────┘
│  Cursor API     │──────▶│   Scripts    │─┘            │
└─────────────────┘       └──────────────┘              │
                                                         ▼
                                                ┌────────────────┐
                                                │     Kibana     │
                                                │   Dashboard    │
                                                └────────────────┘
```

## 📁 Proje Yapısı

```
.
├── README.md                      # Bu dosya
├── DATA_STRUCTURE.md         # Veri yapıları ve kategoriler
├── METRICS_GUIDE.md          # Metriklerin detaylı açıklaması
├── WIDGETS_GUIDE.md          # Dasboard görsel ve açıklamaları
├── scripts/                       # Veri işleme scriptleri
│   ├── gitstats.py               # Git commit analizi
│   ├── dora-metrics.py           # DORA metrikleri toplama
│   ├── cursor_metrics.py         # Cursor AI kullanım metrikleri
│   ├── requirements.txt          # Python bağımlılıkları
│   ├── users.txt                 # Kullanıcı eşleştirmeleri
│   └── teams.txt                 # Takım tanımlamaları
└── images/                    # Dasboard görselleri
```

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- Elasticsearch 7.17.x
- Kibana 7.17.x
- Git repository erişimi
- (Opsiyonel) SQL Server - DORA metrikleri için
- (Opsiyonel) Cursor API erişimi

### Kurulum

1. **Bağımlılıkları yükleyin:**
```bash
pip install -r scripts/requirements.txt
```

2. **Kullanıcı ve takım dosyalarını yapılandırın:**
```bash
# scripts/users.txt - Format: UserAlias-CorporateName
echo "U12345-John Doe" >> scripts/users.txt

# scripts/teams.txt - Format: DeveloperName=TeamName
echo "John Doe=Backend Team" >> scripts/teams.txt
```

3. **Git metriklerini toplayın:**
```bash
python scripts/gitstats.py \
  --repo-path /path/to/repo \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password your-password \
  --names-input-file scripts/users.txt
```

4. **DORA metriklerini toplayın (opsiyonel):**
```bash
python scripts/dora-metrics.py \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password your-password \
  --db-host your-sql-server \
  --db-name your-database \
  --db-username your-username \
  --db-password your-password \
  --teams-file scripts/teams.txt
```

5. **Cursor metriklerini toplayın (opsiyonel):**
```bash
python scripts/cursor_metrics.py \
  --cursor-api-url https://api.cursor.com \
  --cursor-username your-username \
  --cursor-password your-password \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password your-password \
  --users-file scripts/users.txt
```


## 📈 Dashboard Bileşenleri

### Git Metrics
- Commit kategorileri (New Work, Refactor, Churn/Rework, Help Others)
- Geliştirici verimliliği (cefficiency)
- Kod etkisi (commit impact)
- Günlük/haftalık commit trendleri

### DORA Metrics
- **Deployment Frequency**: Dağıtım sıklığı
- **Lead Time**: Commit'ten production'a kadar geçen süre
- **Change Failure Rate**: Başarısız deployment oranı

### Cursor AI Metrics
- AI öneri kabul oranları
- Günlük AI kullanım istatistikleri
- Cursor Score (AI kullanım etkinliği)
- Geliştirici başına AI etkisi

Detaylı metrik açıklamaları için [Metrics Guide](METRICS_GUIDE.md) dökümanına bakınız.

## 📊 Veri Yapıları

Her veri kaynağı Elasticsearch'te ayrı indexlerde saklanır:

- `git-commits`: Git commit verileri
- `dora-deployment-frequency`: Deployment sıklığı verileri
- `dora-lead-time`: Lead time verileri
- `cursor-metrics`: AI kullanım metrikleri

Detaylı veri yapıları için [Data Structure Guide](DATA_STRUCTURE.md) dökümanına bakınız.

## 🔍 Dashboard Görselleri

Dashboard, 30'dan fazla görselleştirme içerir. Tüm görsellerin detaylı açıklamaları [Widgets Guide](WIDGETS_GUIDE.md) dosyasında mevcuttur.

## 🤝 Katkıda Bulunma

Bu proje açık kaynak değildir ancak içerik ve yapı hakkında önerileriniz için issue açabilirsiniz.

## 📝 Lisans

Bu proje şirket içi kullanım için tasarlanmıştır.

## 📧 İletişim

Sorularınız için repository sahibi ile iletişime geçebilirsiniz.

---

**Son Güncelleme**: Kasım 2025
