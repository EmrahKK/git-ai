# Data Collection Scripts

Bu klasör, Elasticsearch'e veri göndermek için kullanılan Python script'lerini içerir.

## Script'ler

### 1. `gitstats.py`
Git commit'lerini analiz eder ve Elasticsearch'e indexler.

**Özellikler**:
- Commit kategorilerini belirler (New Work, Refactor, Help Others, Churn/Rework)
- Commit efficiency (cefficiency) hesaplar
- Commit impact skoru hesaplar
- Dosya bazlı kategori analizi yapar

**Kullanım**:
```bash
python gitstats.py \
  --repo-path /path/to/repo \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password your_password \
  --names-input-file users.txt \
  --days 30
```

**Çıktı Index**: `git-commits`

---

### 2. `dora-metrics.py`
DORA metriklerini SQL Server'dan alır ve Elasticsearch'e indexler.

**Özellikler**:
- Deployment Frequency hesaplar
- Lead Time for Changes hesaplar
- Change Failure Rate hesaplar
- Takım bilgilerini enrichment yapar

**Kullanım**:
```bash
python dora-metrics.py \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password your_password \
  --db-host your-sql-server \
  --db-name your_database \
  --db-username your_user \
  --db-password your_password \
  --teams-file teams.txt \
  --days 30
```

**Çıktı Index'ler**:
- `dora-deployment-frequency`
- `dora-lead-time`
- `dora-change-failure-rate`

---

### 3. `cursor_metrics.py`
Cursor API'den AI kullanım metriklerini alır ve Elasticsearch'e indexler.

**Özellikler**:
- AI suggestion acceptance/rejection sayıları
- Cursor Score hesaplama
- Günlük kullanım istatistikleri
- Kullanıcı eşleştirme

**Kullanım**:
```bash
python cursor_metrics.py \
  --cursor-api-url https://api.cursor.com \
  --cursor-username your_username \
  --cursor-password your_password \
  --elasticsearch-url http://localhost:9200 \
  --elasticsearch-user elastic \
  --elasticsearch-password your_password \
  --users-file users.txt \
  --days 30
```

**Çıktı Index**: `cursor-metrics`

---

## Yapılandırma Dosyaları

### `users.txt`
Kullanıcı ID'lerini gerçek isimlere eşleştirir.

**Format**:
```
UserAlias-CorporateName
```

**Örnek**:
```
U12345-John Doe
U67890-Jane Smith
```

**Nerede Kullanılır**:
- `gitstats.py`: Git commit author'larını eşleştirme
- `cursor_metrics.py`: Cursor kullanıcılarını eşleştirme

---

### `teams.txt`
Geliştiricileri takımlara atar.

**Format**:
```
DeveloperName=TeamName
```

**Örnek**:
```
John Doe=Backend Team
Jane Smith=Frontend Team
```

**Nerede Kullanılır**:
- `dora-metrics.py`: DORA metriklerine takım bilgisi ekleme

---

## Bağımlılıklar

### `requirements.txt`
Tüm Python bağımlılıklarını içerir.

**Kurulum**:
```bash
pip install -r requirements.txt
```

**Paketler**:
- `requests`: HTTP client
- `elasticsearch`: Elasticsearch Python client
- `numpy`: Sayısal hesaplamalar
- `scipy`: İstatistiksel işlemler
- `pyodbc`: SQL Server bağlantısı
- `python-dateutil`: Tarih-saat işlemleri
- `reportlab`: Raporlama (opsiyonel)

---

## Script Çalıştırma Sırası

Verileri toplarken önerilen sıra:

1. **Git Metrics** (Temel veriler)
```bash
python gitstats.py ...
```

2. **DORA Metrics** (Deployment verileri)
```bash
python dora-metrics.py ...
```

3. **Cursor Metrics** (AI kullanım verileri)
```bash
python cursor_metrics.py ...
```

---

## Hata Ayıklama

### Verbose Mode

Script'leri `--verbose` veya `-v` flag'i ile çalıştırarak detaylı log görebilirsiniz:

```bash
python gitstats.py --verbose ...
```

### Log Dosyası

Log'ları dosyaya kaydetmek için:

```bash
python gitstats.py ... 2>&1 | tee git_stats.log
```

### Dry Run Mode

Bazı script'ler `--dry-run` modunu destekler (veri indexlemeden sadece analiz yapar):

```bash
python gitstats.py --dry-run ...
```

---

## Otomatik Çalıştırma

### Cron Job Örneği (Linux/macOS)

```bash
# Her gün saat 02:00'da çalış
0 2 * * * cd /path/to/scripts && /path/to/venv/bin/python gitstats.py --repo-path /repos/myrepo --elasticsearch-url http://localhost:9200 --elasticsearch-user elastic --elasticsearch-password password --names-input-file users.txt --days 1
```

### Task Scheduler (Windows)

Windows Task Scheduler'da günlük task oluşturun:
- **Program**: `C:\path\to\venv\Scripts\python.exe`
- **Arguments**: `C:\path\to\scripts\gitstats.py --repo-path ...`
- **Trigger**: Daily at 2:00 AM

---

## Performans İpuçları

### Büyük Repository'ler için

```bash
# Sadece son N gün için çalıştır
python gitstats.py --days 7 ...

# Specific branch için
python gitstats.py --branch main ...
```

### Bulk Size Ayarlama

Script içindeki `BULK_SIZE` değişkenini artırın (varsayılan: 500):

```python
# gitstats.py içinde
BULK_SIZE = 1000  # Daha hızlı indexleme
```

### Paralel Çalıştırma

Birden fazla repository için paralel çalıştırma:

```bash
#!/bin/bash
python gitstats.py --repo-path /repos/repo1 ... &
python gitstats.py --repo-path /repos/repo2 ... &
python gitstats.py --repo-path /repos/repo3 ... &
wait
```

---

## Güvenlik Notları

⚠️ **ÖNEMLİ**:

1. **Şifreleri kod içine yazmayın**
   - Environment variables kullanın
   - Secret management tools kullanın

2. **users.txt ve teams.txt dosyalarını paylaşmayın**
   - Bu dosyalar `.gitignore`'da listelenmiştir
   - Örneklerini `users.txt.example` olarak ekleyin

3. **Log dosyalarını kontrol edin**
   - Sensitive bilgi içerebilirler
   - Production'da log level'i ayarlayın

---

## Sorun Giderme

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

---

## Daha Fazla Bilgi

Detaylı kurulum ve kullanım bilgileri için ana dökümanları inceleyin:

- [Setup Guide](../repository/SETUP_GUIDE.md)
- [Data Structure](../repository/DATA_STRUCTURE.md)
- [Metrics Guide](../repository/METRICS_GUIDE.md)

