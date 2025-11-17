# Metrikler Rehberi

Bu döküman, dashboard'da kullanılan tüm metrikleri, nasıl hesaplandıklarını ve nasıl yorumlanmaları gerektiğini detaylı olarak açıklar.

## İçindekiler

- [Git Commit Metrikleri](#git-commit-metrikleri)
- [DORA Metrikleri](#dora-metrikleri)
- [Cursor AI Metrikleri](#cursor-ai-metrikleri)
- [Kombine Metrikler](#kombine-metrikler)
- [Metrik Yorumlama Kılavuzu](#metrik-yorumlama-kılavuzu)

---

## Git Commit Metrikleri

### 1. Commit Count (Commit Sayısı)

**Tanım**: Belirli bir zaman diliminde yapılan toplam commit sayısı.

**Nasıl Hesaplanır**:
```
commit_count = total number of commits
```

**Yorumlama**:
- **Yüksek değer**: Aktif geliştirme, sık commit'ler
- **Düşük değer**: Az aktivite veya büyük batch commit'ler
- **İdeal**: Günde 3-8 commit (küçük, anlamlı değişiklikler)

**Dashboard'da Nerede**:
- Commit Count Timeline
- Developer Commit Statistics

---

### 2. Lines of Code Changed (Değişen Kod Satırı)

**Tanım**: Eklenen ve silinen toplam kod satırı.

**Nasıl Hesaplanır**:
```
total_changes = insertions + deletions
```

**Yorumlama**:
- **Yüksek değer**: Büyük refactor'lar veya yeni özellikler
- **Düşük değer**: Küçük bug fix'ler veya ince ayarlar
- **Dikkat**: Çok yüksek değerler atomik olmayan commit'lere işaret edebilir

**İdeal Değerler**:
- Günlük ortalama: 200-800 satır
- Commit başına: 50-200 satır

---

### 3. Commit Efficiency (cefficiency)

**Tanım**: Yeni yazılan kodun toplam değişikliklere oranı. Kodun ne kadarının "yeni" olduğunu gösterir.

**Formül**:
```python
cefficiency = insertions / (insertions + deletions)
```

**Değer Aralığı**: 0.0 - 1.0

**Yorumlama**:
| Değer | Anlamı | Durum |
|-------|--------|-------|
| 0.9 - 1.0 | Çoğunlukla yeni kod | ✅ Mükemmel |
| 0.7 - 0.9 | Dengeli geliştirme | ✅ İyi |
| 0.5 - 0.7 | Çok fazla düzeltme | ⚠️ Dikkat |
| < 0.5 | Yeniden yazma/silme baskın | ❌ Problem |

**Dashboard'da Nerede**:
- Commit Efficiency Trend
- Developer Efficiency Comparison

---

### 4. Commit Impact

**Tanım**: Commit'in kod tabanına etkisini logaritmik ölçekte gösterir.

**Formül**:
```python
commit_impact = log10(insertions + deletions + 1)
```

**Değer Aralığı**: 0.0 - 4.0+

**Yorumlama**:
| Değer | Satır Sayısı | Kategori |
|-------|-------------|----------|
| 0 - 1.0 | 1 - 10 | 🔵 Minimal |
| 1.0 - 2.0 | 10 - 100 | 🟢 Küçük |
| 2.0 - 2.5 | 100 - 300 | 🟡 Orta |
| 2.5 - 3.0 | 300 - 1000 | 🟠 Büyük |
| > 3.0 | 1000+ | 🔴 Çok Büyük |

**Kullanım Senaryoları**:
- Büyük refactor'ları tespit etme
- Riskli deployment'ları belirleme
- Code review önceliklerini belirleme

---

### 5. Commit Kategori Dağılımı

**Tanım**: Commit'lerin 4 kategoriye göre yüzdesel dağılımı.

**Kategoriler ve İdeal Oranlar**:

#### New Work (Yeni Çalışma) - İdeal: %40-50
- **Ne anlama gelir**: Yeni özellik geliştirme
- **Yüksek olması**: ✅ İyi - Ürün büyüyor
- **Düşük olması**: ⚠️ Dikkat - Sadece bakım yapılıyor

#### Refactor (Yeniden Yapılandırma) - İdeal: %20-30
- **Ne anlama gelir**: Kod kalitesi iyileştirmeleri
- **Yüksek olması**: ✅ İyi - Teknik borç azalıyor
- **Düşük olması**: ⚠️ Dikkat - Teknik borç artabilir

#### Help Others (Başkalarına Yardım) - İdeal: %10-20
- **Ne anlama gelir**: Takım işbirliği
- **Yüksek olması**: ✅ İyi - Güçlü takım çalışması
- **Düşük olması**: ⚠️ Dikkat - Silolar oluşuyor olabilir

#### Churn/Rework (Yeniden Çalışma) - İdeal: <%20
- **Ne anlama gelir**: Kısa süre önce yapılan işlerin tekrar edilmesi
- **Yüksek olması**: ❌ Kötü - Kalite veya planlama problemi
- **Düşük olması**: ✅ İyi - İlk seferde doğru yapılıyor

**Dashboard'da Nerede**:
- Commit Category Distribution
- Category Trend Over Time
- Developer Category Breakdown

---

### 6. Files Changed per Commit

**Tanım**: Commit başına değişen ortalama dosya sayısı.

**Formül**:
```
avg_files = total_files_changed / commit_count
```

**İdeal Değer**: 2-5 dosya/commit

**Yorumlama**:
- **1-3 dosya**: ✅ Atomik, odaklanmış değişiklikler
- **4-10 dosya**: ⚠️ Orta seviye, kabul edilebilir
- **>10 dosya**: ❌ Çok geniş kapsamlı, split edilmeli

---

## DORA Metrikleri

### 1. Deployment Frequency (Dağıtım Sıklığı)

**Tanım**: Belirli bir zaman diliminde production'a yapılan dağıtım sayısı.

**Nasıl Hesaplanır**:
```
deployment_frequency = total_deployments / time_period
```

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

**Dashboard'da Nerede**:
- Deployment Frequency Timeline
- Deployment Frequency by Team

---

### 2. Lead Time for Changes (Değişiklik Teslim Süresi)

**Tanım**: Kod commit'inden production'a kadar geçen süre.

**Nasıl Hesaplanır**:
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

**Yorumlama**:
- **Kısa lead time**: Hızlı geri bildirim döngüsü, çevik geliştirme
- **Uzun lead time**: Süreç darboğazları, manuel adımlar, bürokrasi

**İyileştirme Önerileri**:
- ✅ Code review süresini kısaltın
- ✅ Test otomasyonunu artırın
- ✅ Deployment sürecini basitleştirin
- ✅ Batch size'ı küçültün

**Dashboard'da Nerede**:
- Lead Time Distribution
- Average Lead Time by Team
- Lead Time Percentiles (P50, P75, P95)

---

### 3. Change Failure Rate (Değişiklik Başarısızlık Oranı)

**Tanım**: Production'a yapılan değişikliklerin başarısız olma yüzdesi.

**Nasıl Hesaplanır**:
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

**Başarısızlık Kriterleri**:
- Production'da kritik bug
- Rollback gereksinimi
- Hotfix ihtiyacı
- Service disruption

**İyileştirme Önerileri**:
- ✅ Test coverage'ı artırın
- ✅ Staging environment'ı iyileştirin
- ✅ Monitoring ve alerting ekleyin
- ✅ Canary deployment kullanın

**Dashboard'da Nerede**:
- Change Failure Rate Trend
- Failure Rate by Project
- Failed Deployment Details

---

## Cursor AI Metrikleri

### 1. Acceptance Rate (Kabul Oranı)

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

**Düşük Oran Sebepleri**:
- AI context'i yeterince beslenmemiş
- Öneriler projeye uygun değil
- Geliştirici AI'a güvenmiyor
- Kod standartları karmaşık

**Dashboard'da Nerede**:
- AI Acceptance Rate Timeline
- Acceptance Rate by Developer
- Acceptance vs Rejection Comparison

---

### 2. Cursor Score (AI Kullanım Skoru)

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

**Bileşenler**:

1. **Acceptance Rate (40%)**: AI önerilerini kabul etme oranı
2. **Usage Frequency (30%)**: Günlük AI kullanım sıklığı
3. **Consistency (20%)**: Düzenli kullanım tutarlılığı
4. **Efficiency (10%)**: Birim zamanda üretkenlik

**Yorumlama**:

| Skor | Seviye | Açıklama |
|------|--------|----------|
| 85 - 100 | 🏆 Master | AI'yı maksimum verimlilikle kullanıyor |
| 70 - 85 | ⭐ Expert | Çok iyi AI kullanımı |
| 55 - 70 | ✅ Good | Standart üstü kullanım |
| 40 - 55 | ⚠️ Average | Gelişme alanı var |
| < 40 | ❌ Poor | AI potansiyeli kullanılmıyor |

**İyileştirme Önerileri**:
- **Düşük Acceptance**: AI context'ine daha fazla bilgi verin
- **Düşük Frequency**: Daha sık AI önerisi isteyin
- **Düşük Consistency**: Günlük rutin haline getirin
- **Düşük Efficiency**: Önerileri hızlıca değerlendirin

**Dashboard'da Nerede**:
- Cursor Score Ranking
- Score Trend Over Time
- Score Distribution by Team

---

### 3. AI Suggestions per Day

**Tanım**: Günlük alınan ortalama AI önerisi sayısı.

**Formül**:
```
avg_suggestions = total_suggestions / active_days
```

**Yorumlama**:

| Günlük Öneri | Kullanım Seviyesi | Durum |
|--------------|-------------------|-------|
| 100+ | Yoğun kullanım | ⭐⭐⭐⭐ |
| 50-100 | Aktif kullanım | ⭐⭐⭐ |
| 20-50 | Orta seviye | ⭐⭐ |
| < 20 | Düşük kullanım | ⭐ |

**Dashboard'da Nerede**:
- Daily AI Usage Heatmap
- Suggestions Trend

---

### 4. Time Saved with AI

**Tanım**: AI kullanımı sayesinde tasarruf edilen tahmini süre.

**Formül**:
```
time_saved = acceptances * avg_time_per_suggestion
```

**Varsayımlar**:
- Her kabul edilen öneri: ~2 dakika tasarruf
- Komplex öneriler: ~5-10 dakika tasarruf

**Yorumlama**:
- Günlük 50 kabul: ~100 dakika (1.7 saat) tasarruf
- Ayda ~40 saat tasarruf potansiyeli

**Dashboard'da Nerede**:
- Time Saved Calculator
- ROI Analysis

---

## Kombine Metrikler

### 1. Developer Productivity Score

**Tanım**: Git metrikleri ve AI kullanımını birleştiren genel üretkenlik skoru.

**Formül**:
```python
productivity_score = (
    commit_score * 0.30 +          # Commit kalitesi ve miktarı
    category_score * 0.25 +        # Kategori dağılımı
    efficiency_score * 0.20 +      # cefficiency
    cursor_score * 0.25            # AI kullanımı
)
```

**Yorumlama**:
- **80-100**: Elite performer
- **60-80**: High performer
- **40-60**: Average
- **<40**: Needs improvement

---

### 2. AI Impact on Productivity

**Tanım**: AI kullanımının commit kalitesi ve miktarına etkisi.

**Ölçüm Yöntemi**:
- AI kullanımı yüksek vs düşük geliştirici gruplarını karşılaştırma
- Zaman serisi analizi (AI öncesi vs sonrası)

**Metrikler**:
```
impact_ratio = productivity_with_ai / productivity_without_ai
```

**İdeal Değer**: >1.5 (50% üretkenlik artışı)

---

### 3. Code Quality Index

**Tanım**: Commit kategorileri ve DORA metriklerinden türetilen kalite skoru.

**Formül**:
```python
quality_index = (
    (1 - churn_percentage) * 0.35 +      # Düşük rework
    refactor_percentage * 0.25 +          # Düzenli refactor
    (1 - change_failure_rate) * 0.25 +   # Düşük hata oranı
    deployment_frequency_score * 0.15     # Sık deployment
)
```

---

## Metrik Yorumlama Kılavuzu

### Metrik Kombinasyonları ve Anlamları

#### Senaryo 1: Yüksek Commit + Düşük Acceptance Rate
**Durum**: Geliştiric aktif ama AI'dan faydalanmıyor
**Aksiyon**: AI kullanımı eğitimi, pair programming

#### Senaryo 2: Yüksek Churn + Düşük Lead Time
**Durum**: Hızlı ama kalitesiz kod
**Aksiyon**: Code review sürecini güçlendirin, test coverage artırın

#### Senaryo 3: Yüksek Refactor + Düşük New Work
**Durum**: Teknik borç temizliği odaklı
**Aksiyon**: Denge kurun, yeni özellik geliştirmeye zaman ayırın

#### Senaryo 4: Yüksek Cursor Score + Yüksek Productivity
**Durum**: AI başarılı bir şekilde kullanılıyor ✅
**Aksiyon**: Best practice'leri dokümante edin, ekiple paylaşın

---

### Alarm Veren Metrik Kombinasyonları

🚨 **KRİTİK**: Yüksek Change Failure Rate + Yüksek Deployment Frequency
- **Risk**: Kalitesiz hızlı release'ler
- **Aksiyon**: Deployment pipeline'a quality gate ekleyin

🚨 **KRİTİK**: Yüksek Churn + Uzun Lead Time
- **Risk**: Hem kalite hem hız problemi
- **Aksiyon**: Süreç review, eğitim, teknik borç planı

⚠️ **DİKKAT**: Düşük Cursor Score + Yüksek Productivity
- **Risk**: AI potansiyeli kullanılmıyor
- **Aksiyon**: AI training, incentive programları

---

## Dashboard'ları Kullanma En İyi Pratikleri

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

## Özet: Önemli Metrikler Hızlı Referans

| Metrik | İdeal Değer | Kritik Eşik |
|--------|-------------|-------------|
| cefficiency | > 0.7 | < 0.5 |
| Churn/Rework % | < 20% | > 40% |
| Deployment Frequency | Günlük | < Haftalık |
| Lead Time | < 1 gün | > 1 hafta |
| Change Failure Rate | < 15% | > 30% |
| AI Acceptance Rate | > 70% | < 40% |
| Cursor Score | > 70 | < 40 |

Bu metrikleri takip ederek, hem bireysel hem de takım seviyesinde sürekli iyileştirme sağlayabilirsiniz.

