# Kurulum ve Kullanım Rehberi

Bu rehber, AI-Powered Developer Productivity Analytics sistemini sıfırdan kurmak için gereken tüm adımları detaylı olarak açıklar.

## İçindekiler

- [Sistem Gereksinimleri](#sistem-gereksinimleri)
- [Elasticsearch ve Kibana Kurulumu](#elasticsearch-ve-kibana-kurulumu)
- [Python Ortamı Hazırlama](#python-ortamı-hazırlama)
- [Yapılandırma Dosyaları](#yapılandırma-dosyaları)
- [Veri Toplama Script'lerini Çalıştırma](#veri-toplama-scriptlerini-çalıştırma)
- [Dashboard Import](#dashboard-import)
- [Otomatik Çalıştırma (Cron/Scheduled Tasks)](#otomatik-çalıştırma)
- [Sorun Giderme](#sorun-giderme)

---

## Sistem Gereksinimleri

### Minimum Gereksinimler

- **İşletim Sistemi**: Linux, macOS, veya Windows 10/11
- **Python**: 3.8 veya üzeri
- **RAM**: Minimum 4GB (8GB önerilir)
- **Disk Alanı**: Minimum 10GB boş alan
- **Network**: İnternet bağlantısı (API erişimleri için)

### Yazılım Bağımlılıkları

- Elasticsearch 7.17.x
- Kibana 7.17.x
- Python 3.8+
- Git 2.x
- (Opsiyonel) SQL Server - DORA metrikleri için
- (Opsiyonel) Docker - Containerized deployment için

---

## Elasticsearch ve Kibana Kurulumu

### Yöntem 1: Docker ile Kurulum (Önerilen)

#### 1. Docker Compose Dosyası Oluşturma

`docker-compose.yml` dosyası oluşturun:

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.14
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=your_secure_password
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - elastic

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.14
    container_name: kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=your_secure_password
    depends_on:
      - elasticsearch
    networks:
      - elastic

volumes:
  es_data:
    driver: local

networks:
  elastic:
    driver: bridge
```

#### 2. Container'ları Başlatma

```bash
# Container'ları başlat
docker-compose up -d

# Logları kontrol et
docker-compose logs -f

# Elasticsearch'ün çalıştığını kontrol et
curl -u elastic:your_secure_password http://localhost:9200
```

#### 3. Erişim Kontrolü

- **Elasticsearch**: http://localhost:9200
- **Kibana**: http://localhost:5601
- **Kullanıcı**: elastic
- **Şifre**: your_secure_password

### Yöntem 2: Manuel Kurulum

#### Linux/macOS için

```bash
# Elasticsearch indir
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.14-linux-x86_64.tar.gz
tar -xzf elasticsearch-7.17.14-linux-x86_64.tar.gz
cd elasticsearch-7.17.14/

# Elasticsearch'ü başlat
./bin/elasticsearch

# Yeni terminal'de Kibana indir ve başlat
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.17.14-linux-x86_64.tar.gz
tar -xzf kibana-7.17.14-linux-x86_64.tar.gz
cd kibana-7.17.14/
./bin/kibana
```

#### Windows için

1. [Elasticsearch 7.17.14](https://www.elastic.co/downloads/past-releases/elasticsearch-7-17-14) indirin
2. ZIP dosyasını çıkarın
3. `bin\elasticsearch.bat` çalıştırın
4. [Kibana 7.17.14](https://www.elastic.co/downloads/past-releases/kibana-7-17-14) indirin
5. ZIP dosyasını çıkarın
6. `bin\kibana.bat` çalıştırın

---

## Python Ortamı Hazırlama

### 1. Repository'yi Clone'lama

```bash
git clone <repository-url>
cd git-ai-productivity
```

### 2. Virtual Environment Oluşturma

```bash
# Virtual environment oluştur
python3 -m venv venv

# Activate et (Linux/macOS)
source venv/bin/activate

# Activate et (Windows)
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükleme

```bash
pip install -r scripts/requirements.txt
```

Yüklenen paketler:
- `requests`: HTTP istekleri için
- `elasticsearch`: Elasticsearch client
- `numpy`: Sayısal hesaplamalar
- `scipy`: İstatistiksel hesaplamalar
- `pyodbc`: SQL Server bağlantısı
- `python-dateutil`: Tarih işlemleri
- `reportlab`: PDF raporlama (opsiyonel)

---

## Yapılandırma Dosyaları

### 1. Kullanıcı Eşleştirme Dosyası (`users.txt`)

Bu dosya, Git commit'lerindeki kullanıcı adlarını kurumsal isimlerle eşleştirir.

**Format**:
```
UserAlias-CorporateName
```

**Örnek** (`scripts/users.txt`):
```
U12345-John Doe
U67890-Jane Smith
U11223-Robert Johnson
U44556-Emily Davis
```

**Nasıl Bulunur**:
- Git log'larından: `git log --format='%an' | sort -u`
- Cursor API'den kullanıcı listesini alın
- HR sisteminden çalışan listesi

### 2. Takım Tanımlama Dosyası (`teams.txt`)

Bu dosya, geliştiricileri takımlara atar.

**Format**:
```
DeveloperName=TeamName
```

**Örnek** (`scripts/teams.txt`):
```
John Doe=Backend Team
Jane Smith=Backend Team
Robert Johnson=Frontend Team
Emily Davis=Frontend Team
Michael Brown=DevOps Team
```

### 3. Elasticsearch Bağlantı Bilgileri

**Environment Variables** (Önerilen):

```bash
# .env dosyası oluşturun
cat > .env << EOF
ES_URL=http://localhost:9200
ES_USER=elastic
ES_PASSWORD=your_secure_password
EOF

# Environment variables'ı yükle
export $(cat .env | xargs)
```

### 4. SQL Server Bağlantı (DORA Metrics için)

```bash
# .env dosyasına ekleyin
cat >> .env << EOF
DB_HOST=your-sql-server.database.windows.net
DB_PORT=1433
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
EOF
```

### 5. Cursor API Bağlantı

```bash
# .env dosyasına ekleyin
cat >> .env << EOF
CURSOR_API_URL=https://api.cursor.com
CURSOR_USER=your_cursor_username
CURSOR_PASSWORD=your_cursor_password
EOF
```

---

## Veri Toplama Script'lerini Çalıştırma

### 1. Git Metrics Toplama

#### Tek Repository için

```bash
python scripts/gitstats.py \
  --repo-path /path/to/your/repo \
  --elasticsearch-url $ES_URL \
  --elasticsearch-user $ES_USER \
  --elasticsearch-password $ES_PASSWORD \
  --names-input-file scripts/users.txt \
  --days 90
```

#### Parametreler

| Parametre | Açıklama | Zorunlu | Varsayılan |
|-----------|----------|---------|------------|
| `--repo-path` | Git repository yolu | Evet | - |
| `--elasticsearch-url` | Elasticsearch URL | Evet | - |
| `--elasticsearch-user` | ES kullanıcı adı | Evet | - |
| `--elasticsearch-password` | ES şifresi | Evet | - |
| `--names-input-file` | Kullanıcı eşleştirme dosyası | Evet | - |
| `--days` | Kaç gün geriye git | Hayır | 30 |
| `--index-name` | ES index adı | Hayır | git-commits |

#### Çoklu Repository için Script

```bash
#!/bin/bash
# collect_all_repos.sh

REPOS=(
  "/path/to/repo1"
  "/path/to/repo2"
  "/path/to/repo3"
)

for repo in "${REPOS[@]}"; do
  echo "Processing $repo..."
  python scripts/gitstats.py \
    --repo-path "$repo" \
    --elasticsearch-url $ES_URL \
    --elasticsearch-user $ES_USER \
    --elasticsearch-password $ES_PASSWORD \
    --names-input-file scripts/users.txt \
    --days 90
done
```

Çalıştırma:
```bash
chmod +x collect_all_repos.sh
./collect_all_repos.sh
```

### 2. DORA Metrics Toplama

```bash
python scripts/dora-metrics.py \
  --elasticsearch-url $ES_URL \
  --elasticsearch-user $ES_USER \
  --elasticsearch-password $ES_PASSWORD \
  --db-host $DB_HOST \
  --db-port $DB_PORT \
  --db-name $DB_NAME \
  --db-username $DB_USER \
  --db-password $DB_PASSWORD \
  --teams-file scripts/teams.txt \
  --days 90
```

#### Parametreler

| Parametre | Açıklama | Zorunlu |
|-----------|----------|---------|
| `--elasticsearch-url` | Elasticsearch URL | Evet |
| `--elasticsearch-user` | ES kullanıcı adı | Evet |
| `--elasticsearch-password` | ES şifresi | Evet |
| `--db-host` | SQL Server host | Evet |
| `--db-port` | SQL Server port | Hayır (1433) |
| `--db-name` | Veritabanı adı | Evet |
| `--db-username` | DB kullanıcı adı | Evet |
| `--db-password` | DB şifresi | Evet |
| `--teams-file` | Takım tanımlama dosyası | Evet |
| `--days` | Kaç gün geriye git | Hayır (30) |

#### SQL Server Gereksinimleri

DORA script'i, aşağıdaki tablolara erişim gerektirir:

**Deployment Frequency için**:
```sql
SELECT 
  DeploymentDate,
  ProjectName,
  Environment,
  Version,
  DeveloperName,
  Success
FROM Deployments
WHERE DeploymentDate >= @StartDate
```

**Lead Time için**:
```sql
SELECT 
  CommitSHA,
  CommitDate,
  DeploymentDate,
  DeveloperName,
  ProjectName
FROM CommitDeployments
WHERE CommitDate >= @StartDate
```

**Change Failure Rate için**:
```sql
SELECT 
  DeploymentDate,
  ProjectName,
  Failed,
  Rollback,
  HotfixRequired
FROM DeploymentFailures
WHERE DeploymentDate >= @StartDate
```

### 3. Cursor Metrics Toplama

```bash
python scripts/cursor_metrics.py \
  --cursor-api-url $CURSOR_API_URL \
  --cursor-username $CURSOR_USER \
  --cursor-password $CURSOR_PASSWORD \
  --elasticsearch-url $ES_URL \
  --elasticsearch-user $ES_USER \
  --elasticsearch-password $ES_PASSWORD \
  --users-file scripts/users.txt \
  --days 90
```

#### Parametreler

| Parametre | Açıklama | Zorunlu |
|-----------|----------|---------|
| `--cursor-api-url` | Cursor API base URL | Evet |
| `--cursor-username` | Cursor username | Evet |
| `--cursor-password` | Cursor password | Evet |
| `--elasticsearch-url` | Elasticsearch URL | Evet |
| `--elasticsearch-user` | ES kullanıcı adı | Evet |
| `--elasticsearch-password` | ES şifresi | Evet |
| `--users-file` | Kullanıcı eşleştirme dosyası | Evet |
| `--days` | Kaç gün geriye git | Hayır (30) |

---

## Dashboard Import

### 1. Kibana'ya Erişim

Tarayıcıdan Kibana'ya erişin:
```
http://localhost:5601
```

Giriş bilgileri:
- **Username**: elastic
- **Password**: your_secure_password

### 2. Dashboard Import

1. Sol menüden **Stack Management** → **Saved Objects** seçin
2. Sağ üst köşeden **Import** butonuna tıklayın
3. `dashboard-export.ndjson` dosyasını seçin
4. **Import** butonuna tıklayın

### 3. Index Pattern Kontrolü

Dashboard'un çalışması için aşağıdaki index pattern'leri oluşturun:

1. **Management** → **Index Patterns** → **Create index pattern**

2. Aşağıdaki index pattern'leri oluşturun:

| Index Pattern | Time Field |
|---------------|------------|
| `git-commits*` | `date` |
| `dora-deployment-frequency*` | `deployment_date` |
| `dora-lead-time*` | `commit_date` |
| `cursor-metrics*` | `date` |

### 4. Dashboard'u Görüntüleme

1. Sol menüden **Dashboard** seçin
2. **Git Stats & AI Productivity Dashboard** başlıklı dashboard'u açın
3. Sağ üstten zaman aralığını ayarlayın (örn: Last 90 days)

---

## Otomatik Çalıştırma

### Linux/macOS - Cron Jobs

```bash
# Crontab'ı düzenle
crontab -e

# Her gün saat 02:00'da çalışacak job'lar ekle
# Git metrics - Her gün
0 2 * * * /path/to/venv/bin/python /path/to/scripts/gitstats.py --repo-path /path/to/repo --elasticsearch-url http://localhost:9200 --elasticsearch-user elastic --elasticsearch-password your_password --names-input-file /path/to/scripts/users.txt --days 1

# DORA metrics - Her gün
30 2 * * * /path/to/venv/bin/python /path/to/scripts/dora-metrics.py --elasticsearch-url http://localhost:9200 --elasticsearch-user elastic --elasticsearch-password your_password --db-host your-db-host --db-name your-db --db-username your-user --db-password your-pass --teams-file /path/to/scripts/teams.txt --days 1

# Cursor metrics - Her gün
0 3 * * * /path/to/venv/bin/python /path/to/scripts/cursor_metrics.py --cursor-api-url https://api.cursor.com --cursor-username your-user --cursor-password your-pass --elasticsearch-url http://localhost:9200 --elasticsearch-user elastic --elasticsearch-password your_password --users-file /path/to/scripts/users.txt --days 1
```

### Windows - Task Scheduler

1. **Task Scheduler** açın
2. **Create Basic Task** seçin
3. Task detaylarını doldurun:
   - **Name**: Git Metrics Daily
   - **Trigger**: Daily at 2:00 AM
   - **Action**: Start a program
   - **Program**: `C:\path\to\venv\Scripts\python.exe`
   - **Arguments**: `C:\path\to\scripts\gitstats.py --repo-path C:\path\to\repo ...`

### Docker Container ile Otomatik Çalıştırma

`Dockerfile` oluşturun:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY scripts/ /app/scripts/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Cron job dosyası
COPY crontab /etc/cron.d/metrics-cron
RUN chmod 0644 /etc/cron.d/metrics-cron
RUN crontab /etc/cron.d/metrics-cron

CMD ["cron", "-f"]
```

`crontab` dosyası:
```
0 2 * * * cd /app && python scripts/gitstats.py --repo-path /repos/myrepo --elasticsearch-url http://elasticsearch:9200 --elasticsearch-user elastic --elasticsearch-password ${ES_PASSWORD} --names-input-file scripts/users.txt --days 1
30 2 * * * cd /app && python scripts/dora-metrics.py --elasticsearch-url http://elasticsearch:9200 --elasticsearch-user elastic --elasticsearch-password ${ES_PASSWORD} --db-host ${DB_HOST} --db-name ${DB_NAME} --db-username ${DB_USER} --db-password ${DB_PASSWORD} --teams-file scripts/teams.txt --days 1
0 3 * * * cd /app && python scripts/cursor_metrics.py --cursor-api-url ${CURSOR_API_URL} --cursor-username ${CURSOR_USER} --cursor-password ${CURSOR_PASSWORD} --elasticsearch-url http://elasticsearch:9200 --elasticsearch-user elastic --elasticsearch-password ${ES_PASSWORD} --users-file scripts/users.txt --days 1
```

Build ve run:
```bash
docker build -t metrics-collector .
docker run -d --name metrics-collector \
  --network elastic_elastic \
  -v /path/to/repos:/repos \
  -e ES_PASSWORD=your_password \
  -e DB_HOST=your-db-host \
  -e DB_NAME=your-db \
  -e DB_USER=your-user \
  -e DB_PASSWORD=your-pass \
  -e CURSOR_API_URL=https://api.cursor.com \
  -e CURSOR_USER=your-user \
  -e CURSOR_PASSWORD=your-pass \
  metrics-collector
```

---

## Sorun Giderme

### 1. Elasticsearch Bağlantı Hatası

**Hata**:
```
ConnectionError: [Errno 111] Connection refused
```

**Çözüm**:
```bash
# Elasticsearch'ün çalıştığını kontrol et
curl http://localhost:9200

# Docker ile çalışıyorsa
docker ps | grep elasticsearch

# Log'ları kontrol et
docker logs elasticsearch
```

### 2. Authentication Hatası

**Hata**:
```
AuthenticationException: [401] Unauthorized
```

**Çözüm**:
- Elasticsearch kullanıcı adı ve şifresini kontrol edin
- Security ayarlarını kontrol edin:
```bash
curl -u elastic:password http://localhost:9200/_cluster/health
```

### 3. Index Oluşturma Hatası

**Hata**:
```
RequestError: [400] illegal_argument_exception
```

**Çözüm**:
- Index mapping'lerini kontrol edin
- Mevcut index'i silin ve yeniden oluşturun:
```bash
curl -X DELETE -u elastic:password http://localhost:9200/git-commits
```

### 4. Git Repository Erişim Hatası

**Hata**:
```
fatal: not a git repository
```

**Çözüm**:
- Repository yolunun doğru olduğunu kontrol edin
- Git repository'sinin initialize edildiğinden emin olun:
```bash
cd /path/to/repo
git status
```

### 5. SQL Server Bağlantı Hatası

**Hata**:
```
pyodbc.Error: ('08001', 'Server not found')
```

**Çözüm**:
- SQL Server'ın çalıştığını kontrol edin
- Firewall ayarlarını kontrol edin
- Connection string'i test edin:
```python
import pyodbc
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=your-server;'
    'DATABASE=your-db;'
    'UID=your-user;'
    'PWD=your-password'
)
```

### 6. Cursor API Hatası

**Hata**:
```
HTTPError: 403 Forbidden
```

**Çözüm**:
- API credentials'larını kontrol edin
- API rate limit'e takılmadığınızı kontrol edin
- API endpoint'lerinin aktif olduğunu doğrulayın

### 7. Dashboard Göstermiyor

**Problem**: Dashboard açılıyor ama grafik görünmüyor

**Çözüm**:
1. Index pattern'lerin doğru oluşturulduğunu kontrol edin
2. Kibana'da **Discover** sekmesinden veri olup olmadığını kontrol edin
3. Zaman aralığını genişletin (örn: Last 90 days)
4. Refresh butonuna basın

### 8. Python Bağımlılık Hatası

**Hata**:
```
ModuleNotFoundError: No module named 'elasticsearch'
```

**Çözüm**:
```bash
# Virtual environment'ın aktif olduğundan emin olun
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Requirements'ı yeniden yükleyin
pip install -r scripts/requirements.txt
```

---

## Performans İyileştirmeleri

### 1. Elasticsearch Optimizasyonu

```bash
# Heap size'ı artırın (docker-compose.yml)
ES_JAVA_OPTS=-Xms4g -Xmx4g

# Replica sayısını ayarlayın
curl -X PUT -u elastic:password http://localhost:9200/git-commits/_settings -H 'Content-Type: application/json' -d '
{
  "index": {
    "number_of_replicas": 0
  }
}'
```

### 2. Bulk Insert Optimizasyonu

Script'lerde bulk size'ı ayarlayın:
```python
# gitstats.py içinde
BULK_SIZE = 1000  # Değeri artırın
```

### 3. İndex Lifecycle Management

Eski verileri temizlemek için ILM policy oluşturun:
```bash
curl -X PUT -u elastic:password http://localhost:9200/_ilm/policy/metrics-policy -H 'Content-Type: application/json' -d '
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {}
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}'
```

---

## Güvenlik Önerileri

1. **Şifreleri Environment Variables'da Saklayın**
   - Kod içine şifre yazmayın
   - `.env` dosyasını `.gitignore`'a ekleyin

2. **SSL/TLS Kullanın**
   ```yaml
   # docker-compose.yml
   - xpack.security.http.ssl.enabled=true
   ```

3. **Güçlü Şifreler Kullanın**
   - En az 12 karakter
   - Büyük/küçük harf, rakam, özel karakter

4. **Network İzolasyonu**
   - Elasticsearch'ü public internet'e açmayın
   - VPN veya private network kullanın

5. **Audit Logging Aktifleştirin**
   ```yaml
   - xpack.security.audit.enabled=true
   ```

---

## Bakım ve Monitoring

### Daily Checklist
- [ ] Elasticsearch cluster health kontrol
- [ ] Script çalışma log'larını kontrol et
- [ ] Disk kullanımını kontrol et

### Weekly Checklist
- [ ] Index size'larını kontrol et
- [ ] Performance metriklerini gözden geçir
- [ ] Backup'ların alındığını doğrula

### Monthly Checklist
- [ ] Security güncellemelerini yap
- [ ] Eski index'leri temizle
- [ ] Dashboard'ları optimize et

---

## Yedekleme ve Restore

### Snapshot Repository Oluşturma

```bash
# Snapshot directory oluştur
mkdir -p /var/lib/elasticsearch/backup

# Repository kaydet
curl -X PUT -u elastic:password http://localhost:9200/_snapshot/my_backup -H 'Content-Type: application/json' -d '
{
  "type": "fs",
  "settings": {
    "location": "/var/lib/elasticsearch/backup"
  }
}'
```

### Manuel Snapshot Alma

```bash
curl -X PUT -u elastic:password http://localhost:9200/_snapshot/my_backup/snapshot_1?wait_for_completion=true
```

### Snapshot'tan Restore

```bash
curl -X POST -u elastic:password http://localhost:9200/_snapshot/my_backup/snapshot_1/_restore
```

---

## Destek ve Yardım

Kurulum sırasında sorun yaşarsanız:

1. **Log dosyalarını kontrol edin**
2. **Documentation'ı gözden geçirin**
3. **Issue açın** (eğer GitHub repository public ise)
4. **Elasticsearch/Kibana documentation**: https://www.elastic.co/guide/

---

**Kurulum tamamlandı! 🎉**

Artık dashboard'u kullanmaya hazırsınız. İyi analizler!

