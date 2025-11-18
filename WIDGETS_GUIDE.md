# Dashboard Görselleri Rehberi

Bu döküman, Kibana dashboard'unda bulunan tüm görsellerin (widget'ların) detaylı açıklamalarını içerir. Her görsel için veri kaynağı, metrikler ve kullanım amacı belirtilmiştir.

---

## İçindekiler

- [Git Commit Görselleri](#git-commit-görselleri)
- [Developer Performance Görselleri](#developer-performance-görselleri)
- [AI Metrikleri Görselleri](#ai-metrikleri-görselleri)
- [DORA Metrikleri Görselleri](#dora-metrikleri-görselleri)
- [İleri Analiz Görselleri](#i̇leri-analiz-görselleri)
---

## Git Commit Görselleri

### 1. Commit Statistics Details (Data Table)

![Commit Statistics Details](/images/commit-statistics-details.png)

**Tür:** Veri Tablosu  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Tüm commit'lerin detaylı bilgilerini tablo formatında gösterir.

**Sütunlar:**
- **Commit SHA:** Commit'in benzersiz kimliği
- **Date:** Commit tarihi
- **Project:** Projenin adı
- **Repository:** Repository adı
- **Message:** Commit mesajı
- **Author:** Commit'i yapan geliştirici
- **Category:** Commit kategorisi (New Work, Refactor, Churn/Rework, Help Others)
- **Files Changed:** Değiştirilen dosya sayısı
- **Insertions:** Eklenen satır sayısı
- **Deletions:** Silinen satır sayısı

**Kullanım Amacı:**
- Commit'lerin detaylı incelenmesi
- Belirli commit'leri filtreleme ve arama
- Raw data analizi

---

### 2. Developer Score & AI Score (Line Chart)

![Developer Score & AI Score](/images/developer-score-ai-score.png)

**Tür:** Çizgi Grafik  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** Geliştiricilerin hesaplanan performans skoru ile AI kullanım skorlarının zaman içindeki değişimini gösterir.

**Metrikler:**
- **Developer Score (Mavi Çizgi):** Karmaşık formülle hesaplanan geliştirici performans skoru
- **AI Score (Kırmızı Çizgi):** Cursor AI kullanım effectiveness skoru

**Kullanım Amacı:**
- Performans trendlerini takip etmek
- AI kullanımının performansa etkisini görmek
- Zaman içindeki gelişimi analiz etmek

---

### 3. Commit Count & AI Accepted Count (Line Chart)

![Commit Count & AI Accepted Count](/images/commit-count-and-ai-accepted-count.png)

**Tür:** Çizgi Grafik  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** Günlük commit sayısı ile kabul edilen AI önerilerinin karşılaştırılması.

**Metrikler:**
- **Commit Count (Mavi Çizgi):** Günlük commit sayısı
- **AI Accepted Count (Turuncu Çizgi):** Kabul edilen AI önerilerinin sayısı

**Kullanım Amacı:**
- Aktivite seviyelerini izlemek
- AI kullanımı ile commit aktivitesi arasındaki ilişkiyi görmek
- Günlük produktivite pattern'lerini analiz etmek

---

### 4. Monthly Commit Count by Project (Stacked Bar Chart)

![Monthly Commit Count by Project](/images/monthly-commit-count-by-project.png)

**Tür:** Yığın Bar Grafik  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Aylık bazda projelerin commit sayılarını yığın halinde gösterir.

**Metrikler:**
- **X Ekseni:** Aylar
- **Y Ekseni:** Commit sayısı
- **Renk Kodları:** Her proje için farklı renk

**Kullanım Amacı:**
- Proje aktivitelerini aylık takip etmek
- Proje bazlı kaynak dağılımını görmek
- Zaman içinde proje yoğunluklarını karşılaştırmak

---

### 5. Top Repositories by Score (Horizontal Bar Chart)

![Top Repositories by Score](/images/top-repositories-by-score.png)

**Tür:** Yatay Bar Grafik  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Repository'leri hesaplanan performans skoruna göre sıralar.

**Metrikler:**
- **Y Ekseni:** Repository adları
- **X Ekseni:** Hesaplanan performans skoru
- **Sıralama:** Skoruna göre azalan sırada

**Kullanım Amacı:**
- En başarılı repository'leri belirlemek
- Repository bazlı performans karşılaştırması
- Best practice'leri paylaşmak için hedef repository'leri seçmek

---

### 6. Top Projects by Score (Horizontal Bar Chart)

![Top Projects by Score](/images/top-projects-by-score.png)

**Tür:** Yatay Bar Grafik  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Projeleri hesaplanan performans skoruna göre sıralar.

**Metrikler:**
- **Y Ekseni:** Proje adları
- **X Ekseni:** Hesaplanan performans skoru
- **Sıralama:** Skora göre azalan sırada

**Kullanım Amacı:**
- En yüksek kaliteli projeleri belirlemek
- Proje bazlı karşılaştırma yapmak
- Kaynak tahsisi için veri sağlamak

---

### 7. Commits Category (Donut Chart)

![Commits Category](/images/commits-category.png)

**Tür:** Halka Grafik  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Commit'lerin kategori bazında dağılımını gösterir.

**Kategoriler:**
- **New Work:** Yeni özellik geliştirme
- **Refactor:** Kod iyileştirme ve yeniden yapılandırma
- **Churn/Rework:** Hatalı kod düzeltmeleri ve tekrar çalışma
- **Help Others:** Diğer geliştiricilere yardım

**Kullanım Amacı:**
- Geliştirme aktivitelerinin dağılımını anlamak
- Sağlıklı bir kategori dengesi olup olmadığını kontrol etmek
- Yüksek churn oranlarını tespit etmek

---

### 8. Repository Commits (Donut Chart)

![Repository Commits](/images/repository-commits.png)

**Tür:** Halka Grafik  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Commit'lerin repository bazında dağılımını gösterir.

**Metrikler:**
- **Değer:** Repository başına commit sayısı
- **Kategoriler:** Repository adları
- **Görünüm:** Yüzdelik dilimler

**Kullanım Amacı:**
- Hangi repository'lerin daha aktif olduğunu görmek
- Repository bazlı workload dağılımını analiz etmek

---

### 9. Project Commits (Donut Chart)

![Project Commits](/images/project-commits.png)

**Tür:** Halka Grafik  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Commit'lerin proje bazında dağılımını gösterir.

**Metrikler:**
- **Değer:** Proje başına commit sayısı
- **Kategoriler:** Proje adları
- **Görünüm:** Yüzdelik dilimler

**Kullanım Amacı:**
- Proje bazlı aktivite seviyelerini karşılaştırmak
- Kaynak dağılımını görselleştirmek

---

### 10. Lines Deleted (Metric)

![Lines Deleted](/images/lines-deleted.png)

**Tür:** Metrik (Tek Sayı)  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Toplam silinen kod satırı sayısını gösterir.

**Metrikler:**
- **Değer:** Tüm commit'lerdeki toplam silinen satır sayısı (deletions)
- **Renk:** Turuncu tonunda (#e48f7d)

**Kullanım Amacı:**
- Kod temizleme aktivitelerini takip etmek
- Refactoring yoğunluğunu ölçmek

---

### 11. Lines Added (Metric)

![Lines Added](/images/lines-added.png)

**Tür:** Metrik (Tek Sayı)  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Toplam eklenen kod satırı sayısını gösterir.

**Metrikler:**
- **Değer:** Tüm commit'lerdeki toplam eklenen satır sayısı (insertions)
- **Renk:** Yeşil tonunda

**Kullanım Amacı:**
- Yeni kod yazma miktarını takip etmek
- Productivity indicator olarak kullanmak

---

### 12. Developer Count (Metric)

![Developer Count](/images/developer-count.png)

**Tür:** Metrik (Tek Sayı)  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Aktif geliştirici sayısının toplam benzersiz sayısını gösterir.

**Metrikler:**
- **Değer:** Unique developer count (author.keyword field'ından)
- **Renk:** Yeşil tonunda (#71be83)

**Kullanım Amacı:**
- Ekip büyüklüğünü izlemek
- Aktif contributor sayısını takip etmek

---

### 13. Commits Per Hour of Day (Heat Map)

![Commits Per Hour of Day](/images/commits-per-hour-of-day.png)

**Tür:** Isı Haritası  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Günün saatlerine göre commit yoğunluğunu renk derecelendirmesi ile gösterir.

**Metrikler:**
- **X Ekseni:** Saat aralıkları (00-23 formatında)
- **Renk Yoğunluğu:** Commit sayısına göre yeşil tonlaması
- **Değer:** Her saat dilimindeki toplam commit sayısı

**Görsel Özellikler:**
- 24 saat dilimi için dikdörtgen bloklar
- Yeşil renk skalası (açık yeşilden koyu yeşile)
- Interactive tooltip ile saat ve commit sayısı
- Minimal tasarım ile net görsellik

**Kullanım Amacı:**
- En yoğun çalışma saatlerini belirlemek
- Ekip çalışma pattern'lerini anlamak
- Deployment timing stratejileri için insight

---

### 14. Commit Frequency (Metric)

![Commit Frequency](/images/commit-frequency.png)

**Tür:** Metrik (Duration)  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Ortalama commit sıklığını saat bazında hesaplayarak gösterir.

**Hesaplama Formülü:**
```
Commit Frequency = (time_range / 1000) / (commit_count + 1) / 1200
```

**Metrikler:**
- **Değer:** Saat cinsinden ortalama commit aralığı
- **Format:** Duration formatında gösterim (örn: 2.5 saat)
- **Renk:** Mor tonunda (#b0b2f4)

**Kullanım Amacı:**
- Commit yapma sıklığını izlemek
- Çok seyrek veya çok sık commit pattern'lerini tespit etmek

---

### 15. Commit Efficiency (Metric)

![Commit Efficiency](/images/commit-efficiency.png)

**Tür:** Metrik (Decimal Number)  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Ortalama commit verimliliği skorunu gösterir.

**Metrikler:**
- **Değer:** Ortalama efficiency skoru (cefficiency field'ından)
- **Format:** Ondalık sayı formatında (1 digit precision)
- **Renk:** Turuncu tonunda (#E48F7D)

**Efficiency Skoru Nedir:**
- Commit'in kod değişiklik kalitesini ölçen metrik
- Insertion/deletion oranı, dosya sayısı ve impact faktörlerine dayalı
- Yüksek değer = daha verimli kod değişiklikleri

**Kullanım Amacı:**
- Kod kalitesini takip etmek
- Verimlilik trendlerini izlemek

---

## Developer Performance Görselleri

### 16. Top Developers by AI Score (Donut Chart)

![Top Developers by AI Score](/images/top-developers-by-ai-score.png)

**Tür:** Halka Grafik  
**Veri Kaynağı:** `cursor-metrics` index

**Açıklama:** Geliştiricileri AI kullanım skorlarına göre gösterir.

**Metrikler:**
- **Değer:** Ortalama AI skoru
- **Kategoriler:** Geliştirici adları
- **Görünüm:** Yüzdelik dilimlerde

**Kullanım Amacı:**
- AI toollarını en etkin kullanan geliştiricileri belirlemek
- Geliştirici AI adoption seviyelerini karşılaştırmak
- AI eğitimi ve coaching ihtiyaçlarını tespit etmek

---

### 17. Top Developers by Score (Donut Chart)

![Top Developers by Score](/images/top-developers-by-score.png)

**Tür:** Halka Grafik  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Geliştiricileri hesaplanan genel performans skorlarına göre gösterir.

**Metrikler:**
- **Değer:** Hesaplanan geliştirici performans skoru
- **Kategoriler:** Geliştirici adları
- **Görünüm:** Yüzdelik dilimlerde

**Kullanım Amacı:**
- Top performer'ları belirlemek
- Performans dağılımını görmek
- Recognition ve best practice sharing için

---

### 18. Developer Performance Table

![Developer Performance Table](/images/developer-performance-table.png)

**Tür:** Veri Tablosu  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** Geliştiricilerin kapsamlı performans metriklerini tablo halinde gösterir.

**Sütunlar:**
- **Developer:** Geliştirici adı
- **Score:** Hesaplanan genel performans skoru
- **AI Score:** Cursor AI kullanım etkinlik skoru
- **Commits:** Toplam commit sayısı
- **Commit Impact:** Ortalama commit impact değeri
- **Commit Efficiency:** Ortalama commit efficiency değeri
- **Commit Frequency:** Commit sıklık oranı (saat cinsinden)
- **New Work:** Yeni iş kategorisindeki commit yüzdesi
- **Refactor:** Refactor kategorisindeki commit yüzdesi
- **Help Others:** Yardım kategorisindeki commit yüzdesi
- **Churn/Rework:** Churn/Rework kategorisindeki commit yüzdesi

**Kullanım Amacı:**
- Detaylı developer performance analizi
- Kıyaslama ve benchmarking
- Performance review için veri sağlamak

---

### 19. Performance Distribution Analysis (Histogram)

![Performance Distribution Analysis](/images/performance-distribution-analysis.png)

**Tür:** Histogram (Dual Panel)  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** Geliştirici performans skorlarının istatistiksel dağılımını histogram ile gösterir.

**Özellikler:**
- **Çift Panel Layout:** Commit Score ve AI Score ayrı ayrı analiz
- **Histogram Bars:** Her performans aralığındaki geliştirici sayısı
- **Team Average Lines:** Ortalama performans çizgileri
- **Kategorik Renklendirme:**
  - High Performer (Yeşil)
  - Good Performer (Mavi)
  - Average Performer (Turuncu)
  - Developing Skills (Kırmızı)

**Kullanım Amacı:**
- Performans dağılımının normal olup olmadığını görmek
- Outlier'ları tespit etmek
- Ekip average'ını görmek

---

### 20. Developer Performance Transition Matrix

![Developer Performance Transition Matrix](/images/developer-performance-transition-matrix.png)

**Tür:** Transition Matrix (Heat Map)  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Geliştiricilerin aylık performans kategorileri arasındaki geçişlerini matrix formatında gösterir.

**Matrix Boyutları:**
- **Y Ekseni:** Previous Period (Önceki dönem kategorisi)
- **X Ekseni:** Current Period (Mevcut dönem kategorisi)
- **Renk Yoğunluğu:** Geçiş olasılık yüzdesi
- **Metin Etiketleri:** Yüzde ve geliştirici sayısı

**Performans Kategorileri:**
- High Performer (Yüksek Performans)
- Good Performer (İyi Performans)
- Moderate Performer (Orta Performans)
- Developing Skills (Gelişmekte)

**Kullanım Amacı:**
- Kariyer gelişimini takip etmek
- Performance improvement rate'lerini ölçmek
- Retention risk belirlemek

---

### 21. Performance vs Activity Correlation - Efficiency Sweet Spots

![Performance vs Activity Correlation - Efficiency Sweet Spots](/images/performance-vs-activity-correlation-efficiency-sweet-spots.png)

**Tür:** Scatter Plot  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** Geliştirici aktivite seviyesi ile performans arasındaki korelasyonu gösterir ve optimal efficiency noktalarını belirginleştirir.

**Eksen Tanımları:**
- **X Ekseni:** Total Activity Score (Logaritmik skala)
- **Y Ekseni:** Overall Performance Score
- **Renk Kodları:** Efficiency kategorilerine göre
- **Nokta Boyutu:** Average daily commits'e göre

**Efficiency Kategorileri:**
- High Efficiency (Yüksek Verimlilik)
- Good Efficiency (İyi Verimlilik)
- Moderate Efficiency (Orta Verimlilik)
- Low Activity (Düşük Aktivite)
- High Activity, Low Performance (Yüksek Aktivite, Düşük Performans)

**İleri Özellikler:**
- Logarithmic scaling for activity
- Trend lines ve correlation indicators
- Interactive tooltips
- Efficiency sweet spot highlighting

**Kullanım Amacı:**
- Optimal çalışma pattern'lerini belirlemek
- Aktivite ile kalite arasındaki dengeyi görmek
- Overwork veya underwork durumlarını tespit etmek

---

### 22. Developer Performance Comparison (AI vs Non-AI)

![Developer Performance Comparison](/images/developer-performance-comparison.png)

**Tür:** Grouped Bar Chart  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** AI kullanan ve AI kullanmayan geliştiriciler arasında performans metriklerini karşılaştırır.

**Karşılaştırılan Metrikler:**
- **Code Efficiency:** Ortalama kod verimliliği skorları
- **Commit Impact:** Ortalama commit etki skorları
- **Avg Insertions:** Ortalama eklenen satır sayısı
- **Avg Deletions:** Ortalama silinen satır sayısı

**Geliştirici Kategorileri:**
- **AI User (Mavi):** Cursor AI'ı aktif kullanan geliştiriciler (totalAccepts > 0)
- **Non-AI User (Kırmızı):** AI kullanmayan veya minimum kullanan geliştiriciler

**Görsel Özellikler:**
- Grouped bar chart layout
- Side-by-side comparison için her metrik için çift bar
- Hover interactivity ve değer etiketleri

**Kullanım Amacı:**
- AI impact'ini ölçmek
- ROI hesaplaması için veri
- AI adoption'ı teşvik etmek

---

### 23. Developer Performance Flow - Category Transitions Over Time

![Developer Performance Flow - Category Transitions Over Time](/images/developer-performance-flow-category-transitions-over-time.png)

**Tür:** Flow Diagram (Sankey-like)  
**Veri Kaynağı:** `git-stats` index

**Açıklama:** Geliştiricilerin performans kategorileri arasındaki geçişlerini zaman içinde flow diagram formatında görselleştirir.

**Flow Kategorileri:**
- **High Performer (Yeşil):** Yüksek performans seviyesi (≥50 skor)
- **Good Performer (Mavi):** İyi performans seviyesi (30-49 skor)
- **Moderate Performer (Turuncu):** Orta performans seviyesi (15-29 skor)
- **Developing Skills (Kırmızı):** Gelişmekte olan beceriler (>0-14 skor)

**Görsel Özellikler:**
- **Previous Period (Sol Taraf):** Önceki dönemdeki performans kategorileri
- **Current Period (Sağ Taraf):** Mevcut dönemdeki performans kategorileri
- **Flow Lines:** Kategoriler arası geçişleri gösteren eğriler
- **Line Thickness:** Geçiş yapan geliştirici sayısına göre değişken kalınlık
- **Hover Tooltips:** Her akış için detaylı geçiş bilgileri

**Kullanım Amacı:**
- Geliştirici kariyer yolculuğunu takip etmek
- Performance improvement pattern'lerini analiz etmek
- Retention risk ve success story'leri belirlemek
- Team development stratejilerini şekillendirmek
- Coaching effectiveness'ını ölçmek

---

### 24. Developer Performance Matrix: AI Score vs Commit Score

![Developer Performance Matrix: AI Score vs Commit Score](/images/developer-performance-matrix-ai-score-vs-commit-score.png)

**Tür:** Scatter Plot (Quadrant Analysis)  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** Geliştiricileri AI skoru ve Commit skoru bazında 4 farklı performans profiline ayıran scatter plot matrisi.

**Performans Kadranları:**
- **AI + Git Champions (Yeşil):** Hem AI hem Commit skoru ≥50
- **AI Specialists (Mavi):** AI skoru ≥50, Commit skoru <50
- **Git Masters (Sarı):** Commit skoru ≥50, AI skoru <50
- **Developing Skills (Kırmızı):** Her iki skor da <50

**Görsel Elementleri:**
- **X Ekseni:** AI Score (Cursor Score) 0-100 aralığı
- **Y Ekseni:** Commit Score 0-100 aralığı
- **Nokta Rengi:** Performans kadranına göre
- **Nokta Boyutu:** Total commits sayısına göre (sqrt scale)
- **Grid Lines:** 50 referans çizgileri (kesikli)
- **Quadrant Labels:** Her kadranın köşesinde etiket

**Kullanım Amacı:**
- Geliştiricileri profile'lara ayırmak
- Strength ve development area'larını belirlemek
- Targeted coaching stratejileri oluşturmak

---

## AI Metrikleri Görselleri

### 25. AI Acceptance Rate (Metric)

![AI Acceptance Rate](/images/ai-acceptance-rate.png)

**Tür:** Metrik (Percentage)  
**Veri Kaynağı:** `cursor-metrics` index

**Açıklama:** AI önerilerinin kabul edilme oranını yüzdelik değer olarak gösterir.

**Hesaplama Formülü:**
```
AI Acceptance Rate = (sum(totalAccepts) / sum(totalApplies)) × 100
```

**Metrikler:**
- **Değer:** Yüzdelik format ile gösterim (1 decimal precision)
- **Renk:** Pembe tonunda (#D36086)
- **Format:** Percentage formatında display

**Formül Bileşenleri:**
- **totalAccepts:** Kabul edilen AI önerilerinin toplam sayısı
- **totalApplies:** Uygulanan AI önerilerinin toplam sayısı

**Kullanım Amacı:**
- AI tool effectiveness'ını ölçmek
- Kullanıcı memnuniyetini indirect ölçmek
- AI model quality'yi track etmek

---

### 26. File Types: Heavy AI Users vs No AI Users

![File Types: Heavy AI Users vs No AI Users](/images/file-types-heavy-ai-users-vs-no-ai-users.png)

**Tür:** Grouped Bar Chart  
**Veri Kaynağı:** `git-stats` ve `cursor-metrics` index

**Açıklama:** AI'ı yoğun kullanan geliştiriciler ile hiç AI kullanmayan geliştiriciler arasında dosya türü bazında kod değişiklik pattern'lerini karşılaştırır.

**Geliştirici Kategorileri:**
- **Heavy AI User (Yeşil):** Total AI aktivitesi >20 (totalAccepts + totalApplies)
- **No AI User (Kırmızı):** AI aktivitesi sıfır veya minimal

**Analiz Edilen Dosya Türleri:**
- C# (.cs), JavaScript (.js), TypeScript (.ts)
- Python (.py), JSON (.json), HTML (.html)
- CSS (.css), XML (.xml), Markdown (.md)
- Other (Diğer dosya türleri)

**Görsel Özellikler:**
- Grouped bar chart layout
- Her dosya türü için yan yana karşılaştırma
- Hover tooltips ile detaylı değişiklik sayıları
- Filtered data (minimum 500 toplam değişiklik)

**Kullanım Amacı:**
- Hangi dosya türlerinde AI daha çok kullanıldığını görmek
- AI adoption pattern'lerini anlamak
- Technology stack bazlı AI effectiveness

---

## DORA Metrikleri Görselleri

### 27. DORA Lead Time Average by Team

![DORA Lead Time Average by Team](/images/dora-lead-time-average-by-team.png)

**Tür:** Bar Chart (Performance Level Colored)  
**Veri Kaynağı:** `dora-lead-time` index

**Açıklama:** Takım bazında ortalama DORA Lead Time metriklerini saat cinsinden görselleştirir. DORA (DevOps Research and Assessment) Lead Time, kod commit'inden production deployment'a kadar geçen süreyi ölçer.

**Özellikler:**
- **X Ekseni:** Team adları (45 derece döndürülmüş etiketler)
- **Y Ekseni:** Average Lead Time (Saat)
- **Renk Kodlaması (Performance Level):**
  - **Yeşil (#2ca02c):** Elite (< 6 saat)
  - **Turuncu (#ff7f0e):** High (6-12 saat)
  - **Kırmızı (#d62728):** Medium (12-24 saat)
  - **Koyu Kırmızı (#8b0000):** Low (> 24 saat)

**Tooltip Bilgileri:**
- Team adı
- Average Lead Time (saat ve gün cinsinden)
- Total Deployments sayısı
- Performance Level (Elite/High/Medium/Low)

**Kullanım Amacı:**
- Takım bazlı delivery speed'i karşılaştırmak
- Bottleneck'leri tespit etmek
- DORA benchmark'larına göre değerlendirme

---

### 28. DORA Lead Time Average by Product

![DORA Lead Time Average by Product](/images/dora-lead-time-average-by-product.png)

**Tür:** Bar Chart (Performance Level Colored)  
**Veri Kaynağı:** `dora-lead-time` index

**Açıklama:** Ürün bazında ortalama DORA Lead Time metriklerini saat cinsinden görselleştirir. Multi-product deployment'lar için ürünler ayrıştırılarak analiz edilir.

**Özellikler:**
- **X Ekseni:** Product adları (45 derece döndürülmüş etiketler)
- **Y Ekseni:** Average Lead Time (Saat)
- **Renk Kodlaması:** Elite/High/Medium/Low performance levels

**Veri İşleme:**
- Product field'ı comma-separated değerler için split edilir
- Her ürün individual olarak işlenir (flatten transformation)
- Boş ve "non" değerler filtrelenir

**Kullanım Amacı:**
- Ürün bazlı delivery performance
- Product complexity assessment
- Release planning için insight

---

### 29. DORA Deployment Frequency by Team

![DORA Deployment Frequency by Team](/images/dora-deployment-frequency-by-team.png)

**Tür:** Bar Chart (Performance Level Colored)  
**Veri Kaynağı:** `dora-deployment-frequency` index

**Açıklama:** Takım bazında DORA Deployment Frequency metriklerini görselleştirir. Her takımın belirli bir zaman periyodundaki toplam deployment sayısını analiz eder.

**Özellikler:**
- **X Ekseni:** Team adları
- **Y Ekseni:** Deployment Count
- **Renk Kodlaması (Performance Level):**
  - **Yeşil (#2ca02c):** Elite (>90 deployment/month)
  - **Turuncu (#ff7f0e):** High (51-90 deployment)
  - **Kırmızı (#d62728):** Medium (11-50 deployment)
  - **Koyu Kırmızı (#8b0000):** Low (≤10 deployment)

**Tooltip Bilgileri:**
- Team adı
- Deployment Count
- Percentage (toplam deployment'lara göre)
- Performance Level

**DORA Benchmark Kategorileri:**
- **Elite:** Günde birden fazla deployment
- **High:** Haftada bir ile ayda bir arası
- **Medium:** Ayda bir ile 6 ayda bir arası
- **Low:** 6 aydan daha seyrek

**Kullanım Amacı:**
- Deployment maturity seviyesini ölçmek
- CI/CD effectiveness'ını değerlendirmek
- DevOps transformation progress tracking

---

### 30. DORA Deployment Frequency by Product

![DORA Deployment Frequency by Product](/images/dora-deployment-frequency-by-product.png)

**Tür:** Bar Chart (Performance Level Colored)  
**Veri Kaynağı:** `dora-deployment-frequency` index

**Açıklama:** Ürün bazında DORA Deployment Frequency metriklerini görselleştirir. Multi-product release'ler için ürünler ayrıştırılarak individual deployment frequency analizi yapılır.

**Özellikler:**
- **X Ekseni:** Product adları
- **Y Ekseni:** Deployment Count
- **Renk Kodlaması:** Performance levels

**Veri İşleme:**
- Product field'ı comma-separated için split
- Her ürün individual olarak aggregate
- "non" product'lar filtrelenir

**Kullanım Amacı:**
- Product release rhythm analizi
- Technology stack comparison
- Release strategy optimization

---

### 31. DORA Change Failure Rate by Team

![DORA Change Failure Rate by Team](/images/dora-change-failure-rate-by-team.png)

**Tür:** Bar Chart (Performance Level Colored)  
**Veri Kaynağı:** `dora-deployment-frequency` index

**Açıklama:** Takım bazında DORA Change Failure Rate metriklerini görselleştirir. Change Failure Rate, deployment'ların ne kadarının hata nedeniyle geri alındığını veya hotfix gerektirdiğini ölçer.

**Özellikler:**
- **X Ekseni:** Team adları
- **Y Ekseni:** Change Failure Rate (Yüzde)
- **Renk Kodlaması (Performance Level):**
  - **Yeşil (#2ca02c):** Elite (< 10% failure rate)
  - **Turuncu (#ff7f0e):** High (10-20% failure rate)
  - **Kırmızı (#d62728):** Medium (20-30% failure rate)
  - **Koyu Kırmızı (#8b0000):** Low (> 30% failure rate)

**Hesaplama Formülü:**
```
Change Failure Rate = (1 - ((Total Deployments - Hotfix Deployments) / Total Deployments)) × 100
```

**Tooltip Bilgileri:**
- Team adı
- Change Failure Rate (yüzde)
- Total Deployments
- Hotfix Deployments
- Success Rate

**DORA Benchmark Kategorileri:**
- **Elite:** %10'dan az failure rate
- **High:** %10-20 arası
- **Medium:** %20-30 arası
- **Low:** %30'dan fazla

**Kullanım Amacı:**
- Code quality ve testing effectiveness'ı ölçmek
- Production stability tracking
- Risk assessment

---

### 32. DORA Change Failure Rate by Product

![DORA Change Failure Rate by Product](/images/dora-change-failure-rate-by-product.png)

**Tür:** Bar Chart (Performance Level Colored)  
**Veri Kaynağı:** `dora-deployment-frequency` index

**Açıklama:** Ürün bazında DORA Change Failure Rate metriklerini görselleştirir. Multi-product deployment'lar için ürünler ayrıştırılarak individual failure rate analizi yapılır.

**Özellikler:**
- **X Ekseni:** Product adları
- **Y Ekseni:** Change Failure Rate (Yüzde)
- **Renk Kodlaması:** Performance levels

**Hesaplama Formülü:**
```
Change Failure Rate = (1 - ((Total Deployments - Hotfix Deployments) / Total Deployments)) × 100
```

**Kullanım Amacı:**
- Product quality comparison
- Technical debt assessment
- Testing strategy evaluation

---

### 33. DORA Metrics Product Performance Chart (Bubble Chart)

![DORA Metrics Product Performance Chart](/images/dora-metrics-product-performance-chart.png)

**Tür:** Bubble Chart (Multi-Dimensional)  
**Veri Kaynağı:** `dora-deployment-frequency` ve `dora-lead-time` index

**Açıklama:** Ürün bazında DORA metriklerini çok boyutlu bubble chart formatında görselleştirir. Bu gelişmiş analiz, deployment frequency, lead time ve change failure rate'i aynı grafikte göstererek ürün performansının holistic değerlendirmesini sağlar.

**Bubble Chart Boyutları:**
- **X Ekseni:** Deployment Frequency (günlük, logaritmik skala)
- **Y Ekseni:** Change Lead Time (saat cinsinden, logaritmik skala - ters)
- **Bubble Boyutu:** Change Failure Rate (büyük bubble = yüksek failure rate)
- **Renk Kodlaması:** DORA Performance Level

**Performance Level Kategorileri:**
- **Elite (Yeşil #10b981):** Deploy/Day ≥1, Lead Time ≤24h, Failure Rate ≤5%
- **High (Mavi #3b82f6):** Deploy/Day ≥0.14, Lead Time ≤168h, Failure Rate ≤10%
- **Medium (Sarı #f59e0b):** Deploy/Day ≥0.03, Lead Time ≤720h, Failure Rate ≤15%
- **Low (Kırmızı #ef4444):** Diğer tüm durumlar

**Gelişmiş Özellikler:**
- Logaritmik skalalar: Geniş value range'leri için optimal görsellik
- Dual data source join: Deployment ve Lead Time verilerinin birleştirilmesi
- Dynamic date range: Time span'e göre otomatik normalizasyon
- Interactive hover: Detaylı tooltip bilgileri

**Tooltip Bilgileri:**
- Product adı
- Deployments per Day
- Total Deployments
- Average Lead Time (hours)
- Median Lead Time (hours)
- Change Failure Rate (%)
- Hotfix Deployments
- Performance Level

**Kullanım Amacı:**
- Ürün performansını holistic değerlendirme
- Multi-dimensional comparison
- Strategic planning için insight
- Investment decision support

---

### 34. DORA Metrics Team Performance Chart (Bubble Chart)

![DORA Metrics Team Performance Chart](/images/dora-metrics-team-performance-chart.png)

**Tür:** Bubble Chart (Multi-Dimensional)  
**Veri Kaynağı:** `dora-deployment-frequency` ve `dora-lead-time` index

**Açıklama:** Takım bazında DORA metriklerini çok boyutlu bubble chart formatında görselleştirir. Bu analiz, takımların deployment maturity'sini ve DevOps capability'sini comprehensive şekilde değerlendirmeyi sağlar.

**Bubble Chart Boyutları:**
- **X Ekseni:** Deployment Frequency (günlük, logaritmik skala)
- **Y Ekseni:** Change Lead Time (saat cinsinden, logaritmik skala - ters)
- **Bubble Boyutu:** Change Failure Rate
- **Renk Kodlaması:** DORA Performance Level

**Performance Level Kategorileri:**
- Elite, High, Medium, Low (Product chart ile aynı kriterler)

**Teknik Özellikler:**
- Logaritmik scale optimization
- Cross-index data join
- Dynamic normalization
- Interactive selection

**Tooltip Bilgileri:**
- Team adı
- Deployments per Day
- Average Lead Time
- Median Lead Time
- Change Failure Rate
- Performance Level

**Kullanım Amacı:**
- Takımlar arası DevOps maturity comparison
- Coaching ve training prioritization
- Best practice sharing identification
- Process improvement roadmap planning
- DevOps transformation success measurement

---

## İleri Analiz Görselleri

### 35. AI Impact on Deployment Frequency

![AI Impact on Deployment Frequency](/images/ai-impact-on-deployment-frequency.png)

**Tür:** Multi-Layer Line Chart with Area Background  
**Veri Kaynağı:** `dora-deployment-frequency`, `cursor-usage`, `cursor-usage-events` index

**Açıklama:** AI kullanımının deployment frekansı üzerindeki etkisini haftalık bazda çok katmanlı görselleştirme ile analiz eder. AI metrikleri ile deployment frekans metrikleri arasındaki korelasyonu ortaya çıkarmayı hedefler.

**Görsel Katmanları:**
1. **Background Area Layer (Açık Mavi):** Total AI Activity değerlerini arkaplan olarak gösterir
2. **Active AI Users Line (Koyu Mavi):** Haftalık aktif AI kullanıcı sayısı (Scale: 0-120)
3. **Active Projects Line (Mor):** Deployment yapılan proje sayısı (Scale: 0-40)
4. **AI Activity per User Line (Turuncu):** Kullanıcı başına AI aktivite yoğunluğu (Scale: 0-100)

**Tooltip Detayları:**
- Week (YYYY-MM-DD)
- Active AI Users
- AI Accepts
- Chat Requests
- Composer Requests
- Avg Cursor Score
- Active Projects
- Hotfixes

**Hesaplama Formülleri:**
```
total_ai_activity = total_accepts + total_chat_requests + total_composer_requests
ai_activity_per_user = total_ai_activity / active_users (if > 0)
```

**Kullanım Amacı:**
- AI kullanımı ile deployment sıklığı arasındaki korelasyonu görmek
- AI adoption'ın business impact'ini ölçmek
- ROI hesaplaması için veri
- AI tool investment justification

---

### 36. AI Usage vs Lead Time Analysis

![AI Usage vs Lead Time Analysis](/images/ai-usage-vs-lead-time-analysis.png)

**Tür:** Scatter Plot with Regression Line  
**Veri Kaynağı:** `dora-lead-time` ve `cursor-usage` index

**Açıklama:** Geliştirici bazında AI kullanım etkinliği ile DORA Lead Time metrikleri arasındaki korelasyonu dağılım grafiği ile analiz eder. Regresyon çizgisi ile trend eğilimi gösterilir.

**Görsel Elementleri:**
1. **Scatter Points:**
   - **X Ekseni:** Average Cursor Score (AI Usage) - 0-60 aralığı
   - **Y Ekseni:** Average Lead Time (Days) - 0-10 gün aralığı
   - **Nokta Boyutu:** Total Accepts değerine göre (50-400 px range)
2. **Regression Line:**
   - Kırmızı trend çizgisi
   - AI kullanımı ile lead time arasındaki ilişki

**Veri Filtreleme:**
- Sadece cursor_score > 0 olan developer'lar
- Lead time > 0 olan kayıtlar
- Minimum 300 developer analizi

**Tooltip İçeriği:**
- Developer adı
- Cursor Score (1 decimal)
- Lead Time (Days) (3 decimal precision)
- Total Accepts (1 decimal)
- Total Records

**Kullanım Amacı:**
- AI kullanımının delivery speed'e etkisini ölçmek
- Negative correlation'u göstermek (AI ↑, Lead Time ↓)
- Individual developer level'da AI effectiveness
- Training ve adoption strategy için data-driven decision

---

## Metrik Kartları ve KPI'lar

Dashboard'da ayrıca aşağıdaki tek sayı metrik kartları da bulunmaktadır:

- **Total Commits:** Toplam commit sayısı
- **Total Files Changed:** Toplam değişen dosya sayısı
- **Average Commit Impact:** Ortalama commit impact skoru
- **Commit Count:** Filtre edilmiş commit sayısı
- **AI Total Accepts:** Toplam kabul edilen AI önerileri
- **AI Total Applies:** Toplam uygulanan AI önerileri
- **Average Cursor Score:** Ortalama AI kullanım skoru
- **Active Developers:** Aktif geliştirici sayısı

Bu metrik kartları dashboard'un üst kısmında KPI overview sağlar ve filtrelere göre dinamik olarak güncellenir.

---

## Görsel Yerleştirme ve Dashboard Layout

Dashboard, görselleri mantıksal gruplara ayırarak organize eder:

### Üst Bölüm - KPI Overview
- Metrik kartları (8-10 adet)
- Hızlı özet bilgiler

### İkinci Bölüm - Trend Analizi
- Zaman serisi grafikleri
- Line chart'lar
- Aktivite trendleri

### Üçüncü Bölüm - Dağılım ve Kompozisyon
- Donut chart'lar
- Category breakdowns
- Distribution görselleri

### Dördüncü Bölüm - Developer Performance
- Performance table
- Comparison chart'ları
- Ranking görselleri

### Beşinci Bölüm - DORA Metrikleri
- DORA bar chart'ları
- Bubble chart'lar
- Team/Product comparison

### Altıncı Bölüm - İleri Analiz
- Correlation analysis
- Flow diagram'lar
- Transition matrices
- Scatter plot'lar

### Alt Bölüm - Detaylı Tablolar
- Commit statistics details
- Raw data tables
- Drill-down için

---

## Filtreleme ve Interactivity

Dashboard, tüm görseller için ortak filtreler sunar:

- **Time Range:** Tarih aralığı seçimi (Dashboard üst bar)
- **Developer:** Geliştirici adına göre filtreleme
- **Project:** Proje bazlı filtreleme
- **Repository:** Repository bazlı filtreleme
- **Team:** Takım bazlı filtreleme
- **Category:** Commit kategorisi filtreleme
- **Performance Level:** DORA performance level filtreleme

Filtreler, tüm görsellere otomatik olarak uygulanır ve real-time güncelleme sağlar.

---

## Özet

Bu dashboard, **35+ görsel** ile kapsamlı bir geliştirici üretkenlik ve AI etki analizi sağlar:

- ✅ **Git Metrikleri:** 14 görsel
- ✅ **Developer Performance:** 9 görsel
- ✅ **AI Metrikleri:** 3 görsel
- ✅ **DORA Metrikleri:** 8 görsel
- ✅ **İleri Analiz:** 2 görsel

Her görsel, specific business question'a cevap vermek ve actionable insight sağlamak için tasarlanmıştır.

**Dashboard kullanım senaryoları için** [EXAMPLES.md](EXAMPLES.md) dökümanına bakınız.
**Metriklerin detaylı açıklaması için** [METRICS_GUIDE.md](METRICS_GUIDE.md) dökümanına bakınız.

