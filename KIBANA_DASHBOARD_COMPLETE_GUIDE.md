# Kibana Dashboard Kapsamlı Rehber
# AI Destekli Geliştirici Verimlilik Analizi

> Geliştirici performansı ve AI kullanımının yazılım geliştirme süreçlerine etkisini ölçümlemek için tasarlanmış kapsamlı bir analiz ve görselleştirme platformu.

**Son Güncelleme**: Kasım 2025

---

## 📑 İçindekiler

1. [Genel Bakış](#genel-bakış)
2. [Proje Yapısı ve Mimari](#proje-yapısı-ve-mimari)
3. [Hızlı Başlangıç ve Kurulum](#hızlı-başlangıç-ve-kurulum)
4. [Veri Yapıları ve Kategoriler](#veri-yapıları-ve-kategoriler)
5. [Metrikler Rehberi](#metrikler-rehberi)
6. [Dashboard Görselleri](#dashboard-görselleri)
7. [Kullanım Örnekleri ve Senaryolar](#kullanım-örnekleri-ve-senaryolar)
8. [Script'ler ve Veri Toplama](#scriptler-ve-veri-toplama)
9. [Sorun Giderme](#sorun-giderme)

---

## 📊 Genel Bakış

Bu proje, yazılım geliştirme ekiplerinin verimliliğini ve AI araçlarının (özellikle Cursor IDE) bu verimliliğe etkisini analiz etmek için üç temel veri kaynağını kullanmaktadır:

### Veri Kaynakları

- **Git Metrics**: Commit analizi, commit kategorileri, geliştirici verimliliği
- **DORA Metrics**: Deployment frequency, Lead Time, Change Failure Rate metrikleri
- **Cursor Metrics**: AI kullanım istatistikleri, kabul oranları, üretkenlik skorları

### ⚠️ Önemli Not

**Bu analiz ve dashboard, kişi değerlendirme amacı taşımaz; yalnızca proje ve geliştirme sürecindeki gelişim alanlarına dair genel bilgi sağlar.**

### 🎯 Amaç

- Geliştirici üretkenliğini objektif metriklerle ölçümlemek
- AI asistan araçlarının kod kalitesi ve hıza etkisini anlamak
- DORA metriklerini takip ederek sürekli iyileştirme alanlarını belirlemek
- Takım ve proje bazında karşılaştırmalı analizler yapmak

---

## 🏗️ Proje Yapısı ve Mimari

### Mimari Diyagram

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

### Klasör Yapısı

```
.
├── README.md                      # Genel bilgiler
├── DATA_STRUCTURE.md              # Veri yapıları ve kategoriler
├── METRICS_GUIDE.md               # Metriklerin detaylı açıklaması
├── WIDGETS_GUIDE.md               # Dashboard görsel ve açıklamaları
├── EXAMPLES.md                    # Kullanım örnekleri
├── scripts/                       # Veri işleme scriptleri
│   ├── gitstats.py               # Git commit analizi
│   ├── dora-metrics.py           # DORA metrikleri toplama
│   ├── cursor_metrics.py         # Cursor AI kullanım metrikleri
│   ├── requirements.txt          # Python bağımlılıkları
│   ├── users.txt.example         # Kullanıcı eşleştirmeleri örneği
│   ├── teams.txt.example         # Takım tanımlamaları örneği
│   └── README.md                 # Script'ler hakkında bilgi
└── images/                        # Dashboard görselleri
```

---

## 🚀 Hızlı Başlangıç ve Kurulum

### Gereksinimler

- Python 3.8+
- Elasticsearch 7.17.x
- Kibana 7.17.x
- Git repository erişimi
- (Opsiyonel) SQL Server - DORA metrikleri için
- (Opsiyonel) Cursor API erişimi

### 1. Bağımlılıkları Yükleyin

```bash
pip install -r scripts/requirements.txt
```

### 2. Kullanıcı ve Takım Dosyalarını Yapılandırın

**users.txt Formatı**: `UserAlias-CorporateName`
```bash
echo "U12345-John Doe" >> scripts/users.txt
echo "U67890-Jane Smith" >> scripts/users.txt
```

**teams.txt Formatı**: `DeveloperName=TeamName`
```bash
echo "John Doe=Backend Team" >> scripts/teams.txt
echo "Jane Smith=Frontend Team" >> scripts/teams.txt
```

### 3. Git Metriklerini Toplayın

```bash
python scripts/gitstats.py \
  --repo-path /path/to/repo \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password your-password \
  --names-input-file scripts/users.txt
```

### 4. DORA Metriklerini Toplayın (Opsiyonel)

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

### 5. Cursor Metriklerini Toplayın (Opsiyonel)

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

---

## 📦 Veri Yapıları ve Kategoriler

### Git Commit Veri Yapısı

Her commit, aşağıdaki bilgileri içeren bir JSON dökümanı olarak Elasticsearch'e indexlenir:

```json
{
  "sha": "159792db9ef7661c4def3ebde8d26be96bcb2544",
  "author": "John Doe",
  "email": "jdoe@company.com",
  "commit_date": 1721116725,
  "date": "2024-07-16T07:58:45",
  "message": "Citizenship number updated to customerId",
  "project_name": "Neobank",
  "repository_name": "Neobank",
  "total_files_changed": 6,
  "insertions": 12,
  "deletions": 12,
  "category": "Churn/Rework",
  "cefficiency": 0.25,
  "commit_impact": 2.1,
  "files": [
    {
      "insertions": 3,
      "deletions": 3,
      "file": "api/AccountModule.cs",
      "category": "Churn/Rework"
    }
  ]
}
```

### Alan Açıklamaları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `sha` | string | Commit'in benzersiz SHA hash değeri |
| `author` | string | Commit yapan geliştiricinin adı |
| `email` | string | Geliştiricinin e-posta adresi |
| `commit_date` | integer | Unix timestamp (saniye) |
| `date` | string | ISO 8601 format tarih-saat |
| `message` | string | Commit mesajı |
| `project_name` | string | Proje adı |
| `repository_name` | string | Repository adı |
| `total_files_changed` | integer | Değişen dosya sayısı |
| `insertions` | integer | Eklenen satır sayısı |
| `deletions` | integer | Silinen satır sayısı |
| `category` | string | Commit kategorisi (4 kategoriden biri) |
| `cefficiency` | float | Commit verimliliği (0-1 arası) |
| `commit_impact` | float | Commit etkisi skoru |
| `files` | array | Değişen dosyaların detayları |

---

## 📂 Commit Kategorileri

Her commit, yapılan değişikliklerin niteliğine göre 4 kategoriden birine atanır:

### 1. 🔨 Refactor (Yeniden Yapılandırma)

**Tanım**: Mevcut kodun iyileştirilmesi, optimize edilmesi veya temizlenmesi.

**Kriter**:
- Dosyanın son değiştirilme tarihi **3 haftadan eski** olmalı
- Toplam değişiklik (ekleme + silme) **10 satırdan fazla** olmalı

**Ağırlık**: 8 (En yüksek değer)

**Örnek**:
- Eski kod bloklarının temizlenmesi
- Performans optimizasyonları
- Kod standardizasyonu
- Mimari iyileştirmeler

### 2. ✨ New Work (Yeni Çalışma)

**Tanım**: Tamamen yeni özellik veya kod eklenmesi.

**Kriter**:
- Dosya ilk defa oluşturulmuş olmalı, VEYA
- Dosyada sadece ekleme yapılmış, silme olmamalı

**Ağırlık**: 6

**Örnek**:
- Yeni API endpoint'leri
- Yeni servisler veya modüller
- Yeni test dosyaları
- Yeni özellik geliştirmeleri

### 3. 🤝 Help Others (Başkalarına Yardım)

**Tanım**: Başka bir geliştiricinin yazdığı kodu düzeltme veya geliştirme.

**Kriter**:
- Dosyayı en son değiştiren kişi, mevcut commit'i yapandan **farklı** olmalı
- Son değişiklik **3 haftadan yeni** olmalı

**Ağırlık**: 5

**Örnek**:
- Takım arkadaşının kodundaki bug düzeltme
- Code review sonrası düzeltmeler
- Pair programming katkıları
- Acil hotfix'ler

### 4. 🔄 Churn/Rework (Sık Değişiklik/Yeniden Çalışma)

**Tanım**: Kısa süre önce değiştirilen kodun tekrar değiştirilmesi.

**Kriter**:
- Diğer 3 kategoriye girmeyen tüm değişiklikler

**Ağırlık**: 4 (En düşük değer)

**Örnek**:
- Hatalı implementasyon düzeltmeleri
- Gereksinim değişiklikleri
- Eksik kalan işlerin tamamlanması
- Sürekli değişen kodlar (code smell)

### Kategori Dağılımı İdeali

Sağlıklı bir geliştirme sürecinde beklenen kategori dağılımı:

| Kategori | İdeal Oran | Açıklama |
|----------|------------|----------|
| New Work | 40-50% | Ana odak yeni özellikler olmalı |
| Refactor | 20-30% | Düzenli kod iyileştirmeleri |
| Help Others | 10-20% | Takım iş birliği |
| Churn/Rework | <20% | Düşük olmalı (yüksek ise kod kalite problemi olabilir) |

### Commit Kategori Belirleme

Bir commit'in kategorisi, içindeki tüm dosya değişikliklerinin kategorilerine göre **ağırlıklı ortalama** ile belirlenir.

**Hesaplama Adımları**:

1. Her dosya için kategori belirlenir
2. Her kategorinin ağırlıklı puanı hesaplanır
3. En yüksek puana sahip kategori seçilir

**Örnek Hesaplama**:

Bir commit'te 5 dosya değişmiş olsun:

| Dosya | Kategori | Ağırlık |
|-------|----------|---------|
| File1.cs | New Work | 6 |
| File2.cs | New Work | 6 |
| File3.cs | Refactor | 8 |
| File4.cs | Churn/Rework | 4 |
| File5.cs | Churn/Rework | 4 |

**Toplam Skorlar**:
- New Work: 2 × 6 = 12
- Refactor: 1 × 8 = 8
- Churn/Rework: 2 × 4 = 8

**Sonuç**: Commit kategorisi = **New Work**

---

## 🎯 Metrikler Rehberi

### Git Commit Metrikleri

#### 1. Commit Efficiency (cefficiency)

Commit verimliliği, yeni yazılmış kod satırlarının, yeniden yazılan kod satırlarına oranını ölçer.

**Formül**:
```python
if insertions > 0:
    cefficiency = insertions / (insertions + deletions)
else:
    cefficiency = 0
```

**Yorumlama**:
- `1.0`: Sadece yeni kod eklendi (ideal)
- `0.5`: Eşit miktarda ekleme ve silme
- `0.0`: Sadece kod silindi

**İdeal Değer**: > 0.7

#### 2. Commit Impact

Commit'in kod tabanına etkisini ölçer. Logaritmik ölçek kullanır.

**Formül**:
```python
if total_changes > 1:
    commit_impact = log10(total_changes)
else:
    commit_impact = 0
```

**Yorumlama**:
- `< 1`: Küçük değişiklik (< 10 satır)
- `1-2`: Orta seviye değişiklik (10-100 satır)
- `2-3`: Büyük değişiklik (100-1000 satır)
- `> 3`: Çok büyük değişiklik (> 1000 satır)

#### 3. Productive Score

Geliştiricinin genel üretkenlik skoru.

**Formül**:
```python
productive_score = (
    (new_work_percentage * 0.4) +
    (refactor_percentage * 0.3) +
    (help_others_percentage * 0.2) +
    ((1 - churn_percentage) * 0.1)
) * 100
```

---

### DORA Metrikleri

#### 1. Deployment Frequency (Dağıtım Sıklığı)

**Tanım**: Belirli bir zaman diliminde production'a yapılan dağıtım sayısı.

**DORA Seviyeleri**:

| Seviye | Frekans | Durum |
|--------|---------|-------|
| Elite | Günde birden fazla | ⭐⭐⭐⭐ |
| High | Haftada bir - Günde bir | ⭐⭐⭐ |
| Medium | Ayda bir - Haftada bir | ⭐⭐ |
| Low | Ayda birden az | ⭐ |

**İyileştirme Önerileri**:
- ✅ CI/CD pipeline'larını otomatikleştirin
- ✅ Feature flag'leri kullanın
- ✅ Küçük, sık release'ler yapın
- ✅ Deployment risklerini azaltın

#### 2. Lead Time for Changes (Değişiklik Teslim Süresi)

**Tanım**: Kod commit'inden production'a kadar geçen süre.

**Formül**:
```
lead_time = deployment_time - first_commit_time
```

**DORA Seviyeleri**:

| Seviye | Süre | Durum |
|--------|------|-------|
| Elite | < 1 gün | ⭐⭐⭐⭐ |
| High | 1 gün - 1 hafta | ⭐⭐⭐ |
| Medium | 1 hafta - 1 ay | ⭐⭐ |
| Low | 1 ay - 6 ay | ⭐ |

**İyileştirme Önerileri**:
- ✅ Code review süresini kısaltın
- ✅ Test otomasyonunu artırın
- ✅ Deployment sürecini basitleştirin
- ✅ Batch size'ı küçültün

#### 3. Change Failure Rate (Değişiklik Başarısızlık Oranı)

**Tanım**: Production'a yapılan değişikliklerin başarısız olma yüzdesi.

**Formül**:
```
change_failure_rate = (failed_deployments / total_deployments) * 100
```

**DORA Seviyeleri**:

| Seviye | Oran | Durum |
|--------|------|-------|
| Elite | 0% - 15% | ⭐⭐⭐⭐ |
| High | 16% - 30% | ⭐⭐⭐ |
| Medium | 31% - 45% | ⭐⭐ |
| Low | > 45% | ⭐ |

---

### Cursor AI Metrikleri

#### 1. Acceptance Rate (Kabul Oranı)

**Tanım**: AI tarafından önerilen kod parçalarının geliştiriciler tarafından kabul edilme yüzdesi.

**Formül**:
```
acceptance_rate = (acceptances / (acceptances + rejections)) * 100
```

**Yorumlama**:

| Oran | Anlamı | Durum |
|------|--------|-------|
| 80% - 100% | AI önerileri çok değerli | ⭐⭐⭐⭐ |
| 60% - 80% | İyi AI kullanımı | ⭐⭐⭐ |
| 40% - 60% | Orta seviye | ⭐⭐ |
| < 40% | Düşük kalite öneriler | ⭐ |

#### 2. Cursor Score (AI Kullanım Skoru)

**Tanım**: Geliştiricinin AI asistanı ne kadar etkin kullandığını gösteren 0-100 arası kompozit skor.

**Formül**:
```python
cursor_score = (
    acceptance_rate * 0.40 +      # Kabul oranı ağırlığı
    usage_frequency * 0.30 +       # Kullanım sıklığı ağırlığı
    consistency * 0.20 +           # Tutarlılık ağırlığı
    efficiency * 0.10              # Verimlilik ağırlığı
)
```

**Yorumlama**:

| Skor | Seviye | Açıklama |
|------|--------|----------|
| 85 - 100 | 🏆 Master | AI'yı maksimum verimlilikle kullanıyor |
| 70 - 85 | ⭐ Expert | Çok iyi AI kullanımı |
| 55 - 70 | ✅ Good | Standart üstü kullanım |
| 40 - 55 | ⚠️ Average | Gelişme alanı var |
| < 40 | ❌ Poor | AI potansiyeli kullanılmıyor |

---

## 📊 Dashboard Görselleri

Dashboard, 35+ görselleştirme içerir. İşte başlıca görsel kategorileri:

### Git Commit Görselleri (14 adet)

1. **Commit Statistics Details** - Tüm commit'lerin detaylı tablosu
2. **Developer Score & AI Score** - Zaman içindeki performans trendleri
3. **Commit Count & AI Accepted Count** - Aktivite karşılaştırması
4. **Monthly Commit Count by Project** - Proje bazlı aylık aktivite
5. **Top Repositories by Score** - En başarılı repository'ler
6. **Top Projects by Score** - En yüksek kaliteli projeler
7. **Commits Category** - Kategori dağılım grafiği (donut)
8. **Repository Commits** - Repository bazlı commit dağılımı
9. **Project Commits** - Proje bazlı commit dağılımı
10. **Lines Deleted** - Toplam silinen satır sayısı
11. **Lines Added** - Toplam eklenen satır sayısı
12. **Developer Count** - Aktif geliştirici sayısı
13. **Commits Per Hour of Day** - Günlük çalışma pattern'leri
14. **Commit Frequency** - Ortalama commit sıklığı
15. **Commit Efficiency** - Ortalama verimlilik skoru

### Developer Performance Görselleri (9 adet)

16. **Top Developers by AI Score** - AI kullanımında en iyi geliştiriciler
17. **Top Developers by Score** - Genel performans liderleri
18. **Developer Performance Table** - Kapsamlı performans tablosu
19. **Performance Distribution Analysis** - İstatistiksel dağılım histogram'ı
20. **Developer Performance Transition Matrix** - Kategori geçiş matrisi
21. **Performance vs Activity Correlation** - Aktivite-performans korelasyonu
22. **Developer Performance Comparison (AI vs Non-AI)** - AI etkisi karşılaştırması
23. **Developer Performance Flow** - Zaman içinde kategori geçişleri
24. **Developer Performance Matrix: AI Score vs Commit Score** - 4 kadran analizi

### AI Metrikleri Görselleri (3 adet)

25. **AI Acceptance Rate** - Genel kabul oranı metrifiği
26. **File Types: Heavy AI Users vs No AI Users** - Dosya türü bazlı AI kullanımı

### DORA Metrikleri Görselleri (8 adet)

27. **DORA Lead Time Average by Team** - Takım bazlı lead time
28. **DORA Lead Time Average by Product** - Ürün bazlı lead time
29. **DORA Deployment Frequency by Team** - Takım deployment sıklığı
30. **DORA Deployment Frequency by Product** - Ürün deployment sıklığı
31. **DORA Change Failure Rate by Team** - Takım başarısızlık oranı
32. **DORA Change Failure Rate by Product** - Ürün başarısızlık oranı
33. **DORA Metrics Product Performance Chart** - Çok boyutlu bubble chart
34. **DORA Metrics Team Performance Chart** - Takım performans bubble chart

### İleri Analiz Görselleri (2 adet)

35. **AI Impact on Deployment Frequency** - AI etkisi multi-layer analiz
36. **AI Usage vs Lead Time Analysis** - Korelasyon scatter plot

---

## 💼 Kullanım Örnekleri ve Senaryolar

### Senaryo 1: Yeni Ekip Üyesinin Performans Takibi

**Durum**: Ekibe yeni katılan bir geliştirici var, ilk 3 aydaki gelişimini takip etmek istiyorsunuz.

**Dashboard Kullanımı**:

1. Zaman filtresi: "Last 90 days"
2. Developer filter'dan yeni üyeyi seçin
3. İzlenecek Metrikler:

| Metrik | 1. Ay | 2. Ay | 3. Ay | Hedef |
|--------|-------|-------|-------|-------|
| Günlük Commit | 2-3 | 4-5 | 6-8 | 6+ |
| cefficiency | 0.65 | 0.72 | 0.78 | >0.70 |
| Churn/Rework % | 35% | 25% | 18% | <20% |
| Cursor Score | 45 | 62 | 78 | >70 |

**Beklenen Gelişim**:
- ✅ Commit sayısı artmalı
- ✅ Efficiency iyileşmeli
- ✅ Churn/Rework azalmalı
- ✅ AI kullanımı artmalı

### Senaryo 2: Sprint Retrospective için Veri Analizi

**Durum**: 2 haftalık sprint bitti, retrospective için objective data istiyorsunuz.

**Sprint Özet Kartı Örneği**:

```
📊 Sprint 42 Summary (Oct 16 - Oct 30)

Commits: 156
Developers: 8
Total Lines Changed: 12,450
Average cefficiency: 0.74

Category Breakdown:
  New Work: 48% ✅
  Refactor: 22% ✅
  Help Others: 16% ✅
  Churn/Rework: 14% ✅

DORA Metrics:
  Deployments: 12
  Avg Lead Time: 18 hours ⭐
  Failure Rate: 8% ✅

AI Usage:
  Avg Cursor Score: 72
  Acceptance Rate: 76%
```

**Retrospective Soruları**:

✅ **What went well?**
- Lead time 18 saat (hedef: <24 saat)
- Churn/Rework düşük (%14)
- AI kullanımı yüksek

⚠️ **What needs improvement?**
- Deployment sayısı az (12, hedef: 14+)
- New Work oranı biraz düşük (hedef: %50+)

🎯 **Action Items**:
- Daha küçük feature'lar için daha sık deployment
- Refactor işlerini separate sprint'e taşı

### Senaryo 3: AI Kullanımının Performansa Etkisi

**Araştırma Sorusu**: "AI kullanan geliştiriciler daha üretken mi?"

**Analiz**:

Geliştiricileri gruplama:
- **Grup A (High AI Users)**: Cursor Score > 75
- **Grup B (Low AI Users)**: Cursor Score < 50

**Metrik Karşılaştırması**:

| Metrik | High AI | Low AI | Fark |
|--------|---------|--------|------|
| Commits/day | 4.2 | 2.8 | +50% ⬆️ |
| cefficiency | 0.78 | 0.68 | +15% ⬆️ |
| Lead Time | 18h | 32h | -44% ⬆️ |
| Churn Rate | 14% | 26% | -46% ⬆️ |
| New Work % | 52% | 41% | +27% ⬆️ |

**Sonuç**: ✅ AI kullanımı ile üretkenlik arasında güçlü pozitif korelasyon

### Senaryo 4: Haftalık Takım Toplantısı

**Dashboard Flow** (20 dakika):

1. **Overview Panel** (5 dk) - Genel metrikler
2. **Category Distribution** (3 dk) - Commit kategori dağılımı
3. **DORA Metrics** (5 dk) - Deployment, lead time, failure rate
4. **Highlight Developers** (3 dk) - En iyi performanslar
5. **Action Items** (4 dk) - Gelecek hafta planı

---

## 🔧 Script'ler ve Veri Toplama

### Script Çalıştırma Sırası

Verileri toplarken önerilen sıra:

#### 1. Git Metrics (Temel veriler)

```bash
python scripts/gitstats.py \
  --repo-path /path/to/repo \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password password \
  --names-input-file scripts/users.txt \
  --days 30
```

**Çıktı Index**: `git-commits`

#### 2. DORA Metrics (Deployment verileri)

```bash
python scripts/dora-metrics.py \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password password \
  --db-host your-sql-server \
  --db-name your_database \
  --db-username your_user \
  --db-password your_password \
  --teams-file scripts/teams.txt \
  --days 30
```

**Çıktı Index'ler**:
- `dora-deployment-frequency`
- `dora-lead-time`
- `dora-change-failure-rate`

#### 3. Cursor Metrics (AI kullanım verileri)

```bash
python scripts/cursor_metrics.py \
  --cursor-api-url https://api.cursor.com \
  --cursor-username your_username \
  --cursor-password your_password \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password password \
  --users-file scripts/users.txt \
  --days 30
```

**Çıktı Index**: `cursor-metrics`

### Otomatik Çalıştırma

#### Cron Job Örneği (Linux/macOS)

```bash
# Her gün saat 02:00'da çalış
0 2 * * * cd /path/to/scripts && /path/to/venv/bin/python gitstats.py \
  --repo-path /repos/myrepo \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password password \
  --names-input-file users.txt \
  --days 1
```

#### Performans İpuçları

**Büyük Repository'ler için**:

```bash
# Sadece son N gün için çalıştır
python gitstats.py --days 7 ...

# Specific branch için
python gitstats.py --branch main ...
```

**Paralel Çalıştırma**:

```bash
#!/bin/bash
python gitstats.py --repo-path /repos/repo1 ... &
python gitstats.py --repo-path /repos/repo2 ... &
python gitstats.py --repo-path /repos/repo3 ... &
wait
```

---

## 🔍 Sorun Giderme

### Elasticsearch Bağlantı Hatası

```bash
# Elasticsearch'ün çalışıp çalışmadığını kontrol et
curl http://localhost:9200

# Authentication'ı test et
curl -u elastic:password http://localhost:9200/_cluster/health
```

### SQL Server Bağlantı Hatası

```python
# Test connection
import pyodbc
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=your-server;DATABASE=your-db;UID=user;PWD=pass'
)
print(conn)
```

### Cursor API Hatası

```bash
# API erişimini test et
curl -u username:password https://api.cursor.com/health
```

### Hata Ayıklama

**Verbose Mode**:

```bash
python gitstats.py --verbose ...
```

**Log Dosyası**:

```bash
python gitstats.py ... 2>&1 | tee git_stats.log
```

**Dry Run Mode**:

```bash
python gitstats.py --dry-run ...
```

---

## 🔒 Güvenlik Notları

⚠️ **ÖNEMLİ**:

1. **Şifreleri kod içine yazmayın**
   - Environment variables kullanın
   - Secret management tools kullanın

2. **users.txt ve teams.txt dosyalarını paylaşmayın**
   - Bu dosyalar `.gitignore`'da listelenmiştir
   - Örneklerini `.example` uzantılı olarak ekleyin

3. **Log dosyalarını kontrol edin**
   - Sensitive bilgi içerebilirler
   - Production'da log level'i ayarlayın

---

## 📈 Dashboard Kullanma En İyi Pratikleri

### Günlük İnceleme
- [ ] Dün yapılan commit'leri gözden geçir
- [ ] Churn/Rework oranını kontrol et
- [ ] AI acceptance rate'e bak

### Haftalık Review
- [ ] Commit kategori dağılımını incele
- [ ] Lead time trend'ine bak
- [ ] Takım bazında performans karşılaştır
- [ ] Cursor score gelişimini takip et

### Aylık Analiz
- [ ] DORA metriklerini değerlendir
- [ ] Üretkenlik trendlerini incele
- [ ] AI impact'i ölç ve raporla
- [ ] İyileştirme aksiyonlarını planla

---

## 📋 Önemli Metrikler Hızlı Referans

| Metrik | İdeal Değer | Kritik Eşik |
|--------|-------------|-------------|
| cefficiency | > 0.7 | < 0.5 |
| Churn/Rework % | < 20% | > 40% |
| Deployment Frequency | Günlük | < Haftalık |
| Lead Time | < 1 gün | > 1 hafta |
| Change Failure Rate | < 15% | > 30% |
| AI Acceptance Rate | > 70% | < 40% |
| Cursor Score | > 70 | < 40 |

---

## 🎓 Özet

Bu sistem, geliştirici performansını ve AI etkisini ölçümlemek için kapsamlı bir platform sağlar:

✅ **4 Commit Kategorisi**: New Work, Refactor, Help Others, Churn/Rework  
✅ **Verimlilik Metrikleri**: cefficiency, commit_impact  
✅ **DORA Metrikleri**: Deployment frequency, lead time, failure rate  
✅ **AI Metrikleri**: Cursor score, acceptance rate  
✅ **35+ Dashboard Görseli**: Comprehensive analiz ve raporlama  
✅ **Data-Driven Kararlar**: Objektif metriklerle iyileştirme  

---

## 📞 İletişim ve Destek

Sorularınız için repository sahibi ile iletişime geçebilirsiniz.

## 📝 Lisans

Bu proje şirket içi kullanım için tasarlanmıştır.

---

**© 2025 - AI Destekli Geliştirici Verimlilik Analizi Platformu**

