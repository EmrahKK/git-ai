# Veri Yapıları ve Kategoriler

Bu döküman, sistemde kullanılan veri yapılarını, commit kategorilerini ve metriklerin nasıl hesaplandığını detaylı olarak açıklar.

## İçindekiler

- [Git Commit Veri Yapısı](#git-commit-veri-yapısı)
- [Commit Kategorileri](#commit-kategorileri)
- [Commit Kategori Belirleme](#commit-kategori-belirleme)
- [Metrik Hesaplamaları](#metrik-hesaplamaları)
- [DORA Metrics Veri Yapısı](#dora-metrics-veri-yapısı)
- [Cursor Metrics Veri Yapısı](#cursor-metrics-veri-yapısı)

---

## Git Commit Veri Yapısı

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

## Commit Kategorileri

Her commit, yapılan değişikliklerin niteliğine göre 4 kategoriden birine atanır:

### 1. 🔨 Refactor (Yeniden Yapılandırma)

**Tanım**: Mevcut kodun iyileştirilmesi, optimize edilmesi veya temizlenmesi.

**Kriter**:
- Dosyanın son değiştirilme tarihi **3 haftadan eski** olmalı
- Toplam değişiklik (ekleme + silme) **10 satırdan fazla** olmalı

**Ağırlık**: 8 (En yüksek değer)

**Örnek**:
```
- Eski kod bloklarının temizlenmesi
- Performans optimizasyonları
- Kod standardizasyonu
- Mimari iyileştirmeler
```

### 2. ✨ New Work (Yeni Çalışma)

**Tanım**: Tamamen yeni özellik veya kod eklenmesi.

**Kriter**:
- Dosya ilk defa oluşturulmuş olmalı, VEYA
- Dosyada sadece ekleme yapılmış, silme olmamalı

**Ağırlık**: 6

**Örnek**:
```
- Yeni API endpoint'leri
- Yeni servisler veya modüller
- Yeni test dosyaları
- Yeni özellik geliştirmeleri
```

### 3. 🤝 Help Others (Başkalarına Yardım)

**Tanım**: Başka bir geliştiricinin yazdığı kodu düzeltme veya geliştirme.

**Kriter**:
- Dosyayı en son değiştiren kişi, mevcut commit'i yapandan **farklı** olmalı
- Son değişiklik **3 haftadan yeni** olmalı

**Ağırlık**: 5

**Örnek**:
```
- Takım arkadaşının kodundaki bug düzeltme
- Code review sonrası düzeltmeler
- Pair programming katkıları
- Acil hotfix'ler
```

### 4. 🔄 Churn/Rework (Sık Değişiklik/Yeniden Çalışma)

**Tanım**: Kısa süre önce değiştirilen kodun tekrar değiştirilmesi.

**Kriter**:
- Diğer 3 kategoriye girmeyen tüm değişiklikler

**Ağırlık**: 4 (En düşük değer)

**Örnek**:
```
- Hatalı implementasyon düzeltmeleri
- Gereksinim değişiklikleri
- Eksik kalan işlerin tamamlanması
- Sürekli değişen kodlar (code smell)
```

### Kategori Dağılımı İdeali

Sağlıklı bir geliştirme sürecinde beklenen kategori dağılımı:

| Kategori | İdeal Oran | Açıklama |
|----------|------------|----------|
| New Work | 40-50% | Ana odak yeni özellikler olmalı |
| Refactor | 20-30% | Düzenli kod iyileştirmeleri |
| Help Others | 10-20% | Takım iş birliği |
| Churn/Rework | <20% | Düşük olmalı (yüksek ise kod kalite problemi olabilir) |

---

## Commit Kategori Belirleme

Bir commit'in kategorisi, içindeki tüm dosya değişikliklerinin kategorilerine göre **ağırlıklı ortalama** ile belirlenir.

### Hesaplama Adımları

1. **Her dosya için kategori belirlenir**
   ```python
   for file in commit.files:
       file.category = determine_file_category(file)
   ```

2. **Her kategorinin ağırlıklı puanı hesaplanır**
   ```python
   category_scores = {
       'Refactor': count_refactor_files * 8,
       'New Work': count_newwork_files * 6,
       'Help Others': count_helpothers_files * 5,
       'Churn/Rework': count_churn_files * 4
   }
   ```

3. **En yüksek puana sahip kategori seçilir**
   ```python
   commit.category = max(category_scores, key=category_scores.get)
   ```

### Örnek Hesaplama

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

## Metrik Hesaplamaları

### 1. Commit Efficiency (cefficiency)

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

### 2. Commit Impact

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

### 3. Productive Score

Geliştiricinin genel üretkenlik skoru (Cursor metrikleriyle birleştirildiğinde).

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

## DORA Metrics Veri Yapısı

### Deployment Frequency

```json
{
  "deployment_date": "2024-07-16T10:30:00",
  "project": "Neobank",
  "environment": "Production",
  "version": "1.2.3",
  "developer": "John Doe",
  "team": "Backend Team",
  "success": true
}
```

### Lead Time

```json
{
  "commit_sha": "abc123...",
  "commit_date": "2024-07-15T14:20:00",
  "deployment_date": "2024-07-16T10:30:00",
  "lead_time_hours": 20.17,
  "developer": "John Doe",
  "team": "Backend Team",
  "project": "Neobank"
}
```

### Change Failure Rate

```json
{
  "deployment_date": "2024-07-16T10:30:00",
  "project": "Neobank",
  "failed": false,
  "rollback": false,
  "hotfix_required": false,
  "team": "Backend Team"
}
```

---

## Cursor Metrics Veri Yapısı

```json
{
  "date": "2024-07-16",
  "developer": "John Doe",
  "team": "Backend Team",
  "acceptances": 45,
  "rejections": 12,
  "acceptance_rate": 0.79,
  "total_suggestions": 57,
  "cursor_score": 82.5,
  "active_time_minutes": 480,
  "suggestions_per_hour": 7.13
}
```

### Cursor Score Hesaplama

Cursor Score, AI kullanım etkinliğini 0-100 arası bir skorla ölçer.

**Bileşenler**:
- Acceptance Rate (Kabul oranı): %40
- Usage Frequency (Kullanım sıklığı): %30
- Consistency (Tutarlılık): %20
- Efficiency (Verimlilik): %10

**Formül**:
```python
cursor_score = (
    acceptance_rate * 40 +
    normalized_usage * 30 +
    consistency_score * 20 +
    efficiency_score * 10
)
```

**Yorumlama**:
- `80-100`: Mükemmel AI kullanımı
- `60-80`: İyi AI kullanımı
- `40-60`: Orta seviye
- `< 40`: Düşük AI kullanımı

---

## Elasticsearch Index Mapping'leri

### git-commits Index

```json
{
  "mappings": {
    "properties": {
      "sha": { "type": "keyword" },
      "author": { "type": "keyword" },
      "email": { "type": "keyword" },
      "commit_date": { "type": "date", "format": "epoch_second" },
      "date": { "type": "date" },
      "message": { "type": "text" },
      "category": { "type": "keyword" },
      "cefficiency": { "type": "float" },
      "commit_impact": { "type": "float" },
      "insertions": { "type": "integer" },
      "deletions": { "type": "integer" },
      "total_files_changed": { "type": "integer" }
    }
  }
}
```

### cursor-metrics Index

```json
{
  "mappings": {
    "properties": {
      "date": { "type": "date" },
      "developer": { "type": "keyword" },
      "team": { "type": "keyword" },
      "acceptances": { "type": "integer" },
      "rejections": { "type": "integer" },
      "acceptance_rate": { "type": "float" },
      "cursor_score": { "type": "float" }
    }
  }
}
```

---

## Veri Kalitesi ve Doğrulama

### Veri Temizleme

Script'ler, verileri indexlemeden önce aşağıdaki kontrolleri yapar:

1. **Null/Boş değer kontrolü**
2. **Tarih formatı doğrulama**
3. **Geçersiz metrik değerleri (negatif sayılar vb.)**
4. **Duplicate commit kontrolü** (SHA bazlı)
5. **Kullanıcı adı eşleştirme**

### Hata Yönetimi

- Başarısız indexlemeler log'lanır
- Bulk indexleme hataları tekrar denenir
- Geçersiz veriler atlanır ve warning log'u oluşturulur

---

## Özet

Bu veri yapıları ve kategoriler, sistemin temelini oluşturur:

✅ **4 Commit Kategorisi**: New Work, Refactor, Help Others, Churn/Rework
✅ **Ağırlıklı Kategori Belirleme**: Dosya bazlı kategori skorları
✅ **Verimlilik Metrikleri**: cefficiency, commit_impact
✅ **DORA Metrikleri**: Deployment frequency, lead time, failure rate
✅ **AI Metrikleri**: Cursor score, acceptance rate

Bu yapı sayesinde, geliştirici performansı ve AI etkisi objektif olarak ölçümlenebilir.

