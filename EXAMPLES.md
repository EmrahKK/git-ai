# Kullanım Örnekleri ve Senaryolar

Bu döküman, sistemin farklı kullanım senaryolarını ve gerçek dünya örneklerini içerir.

## İçindekiler

- [Temel Kullanım Senaryoları](#temel-kullanım-senaryoları)
- [Dashboard Kullanım Örnekleri](#dashboard-kullanım-örnekleri)
- [Analiz Senaryoları](#analiz-senaryoları)
- [Karşılaştırmalı Analizler](#karşılaştırmalı-analizler)
- [Karar Destek Örnekleri](#karar-destek-örnekleri)

---

## Temel Kullanım Senaryoları

### Senaryo 1: Yeni Ekip Üyesinin Performans Takibi

**Durum**: Ekibe yeni katılan bir geliştirici var, ilk 3 aydaki gelişimini takip etmek istiyorsunuz.

**Dashboard Kullanımı**:

1. **Zaman Aralığını Ayarlayın**
   - Kibana'da zaman filtresi: "Last 90 days"

2. **Geliştirici Filtreleme**
   - Developer filter'dan yeni üyeyi seçin

3. **İzlenecek Metrikler**:

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

**Aksiyonlar**:
- **1. Ay**: Mentörlük, code review, pair programming
- **2. Ay**: Best practice'leri öğretme, AI kullanımı training
- **3. Ay**: Bağımsız çalışmaya geçiş

---

### Senaryo 2: Sprint Retrospective için Veri Analizi

**Durum**: 2 haftalık sprint bitti, retrospective için objective data istiyorsunuz.

**Dashboard Kullanımı**:

1. **Zaman Aralığı**: Last 14 days
2. **Takım Filtresi**: Backend Team

**Analiz Edilecek Metrikler**:

#### Sprint Özet Kartı
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

---

### Senaryo 3: Code Quality İyileştirme Kampanyası

**Durum**: Takımda yüksek Churn/Rework oranı var, iyileştirme planı yapılacak.

**Başlangıç Durumu (Ağustos)**:
```
Churn/Rework: 38%
cefficiency: 0.61
Change Failure Rate: 28%
```

**4 Aylık İyileştirme Planı**:

| Ay | Aksiyon | Hedef Metrik |
|----|---------|-------------|
| **Eylül** | Code review process<br>Pair programming | Churn: <30%<br>cefficiency: >0.65 |
| **Ekim** | Test automation<br>CI/CD pipeline | Failure Rate: <20%<br>Lead Time: <2 gün |
| **Kasım** | AI adoption training<br>Best practices doc | Cursor Score: >65<br>Acceptance: >70% |
| **Aralık** | Refactoring sprints<br>Tech debt reduction | Churn: <20%<br>Refactor: >25% |

**Dashboard Takibi**:
- Her hafta metrik review
- Trend grafikleri ile progress tracking
- Developer bazlı breakdown

**Sonuç (Aralık)**:
```
Churn/Rework: 18% ✅ (38% → 18%)
cefficiency: 0.76 ✅ (0.61 → 0.76)
Change Failure Rate: 12% ✅ (28% → 12%)
Cursor Score: 71 ✅ (52 → 71)
```

---

## Dashboard Kullanım Örnekleri

### Örnek 1: Haftalık Takım Toplantısı

**Senaryo**: Her Pazartesi yapılan team sync meeting.

**Dashboard Flow**:

1. **Overview Panel** (5 dakika)
   - Geçen hafta toplam commit: 87
   - Aktif developer sayısı: 12
   - Toplam deployment: 8
   - AI kullanım ortalaması: %74

2. **Category Distribution** (3 dakika)
   - New Work: %52 ✅
   - Churn: %12 ✅
   - Refactor: %24 ✅
   - Help Others: %12 ✅

3. **DORA Metrics** (5 dakika)
   - Deployment frequency: 8/week (Target: 10)
   - Lead time median: 22 saat ✅
   - Failure rate: %10 ✅

4. **Highlight Developers** (3 dakika)
   - En yüksek productive score: Jane (88)
   - En fazla help others: John (18 commits)
   - En iyi AI usage: Sarah (Cursor Score: 92)

5. **Action Items** (4 dakika)
   - Deployment frequency artırma planı
   - Jane'in best practice'lerini share etme
   - Sarah'ın AI kullanım workshop'u

**Total Duration**: 20 dakika

---

### Örnek 2: Aylık Engineering Review

**Senaryo**: C-level'a aylık rapor sunumu.

**Executive Summary Dashboard**:

```
🎯 October 2024 Engineering Metrics

👥 Team Performance
  - Active Developers: 24
  - Total Commits: 1,248
  - Lines of Code: 89,500
  - Projects Active: 8

📈 Productivity Trends
  - Overall Productivity: 76/100 (↑ 8%)
  - Average cefficiency: 0.74 (↑ 0.05)
  - Commit Quality Score: 82/100 (↑ 4%)

🚀 DORA Metrics (Industry Benchmark)
  - Deployment Frequency: Daily (Elite) ⭐⭐⭐⭐
  - Lead Time: 1.2 days (High) ⭐⭐⭐
  - Change Failure: 11% (Elite) ⭐⭐⭐⭐

🤖 AI Impact
  - Cursor Adoption: 87% of developers
  - Average Acceptance Rate: 73%
  - Estimated Time Saved: 840 hours/month
  - ROI: 320% (vs license cost)

💡 Key Insights
  ✅ AI adoption showing 22% productivity increase
  ✅ DORA metrics in "High Performer" category
  ⚠️ 3 developers need AI training
  🎯 Tech debt reduced by 15%
```

---

### Örnek 3: Performance Review için Veri

**Senaryo**: 6 aylık developer performance review.

**Developer: John Doe**

**Dashboard Filters**:
- Developer: John Doe
- Time Range: Last 180 days
- Compare: Team Average

**Metrik Kartı**:

```
👤 John Doe - Performance Summary (Apr-Oct 2024)

📊 Commit Statistics
  Total Commits: 342 (Team Avg: 298) ✅
  Lines Changed: 28,450 (Team Avg: 24,200) ✅
  Files Modified: 1,240 (Team Avg: 1,100) ✅

📈 Quality Metrics
  cefficiency: 0.79 (Team Avg: 0.74) ⭐
  Commit Impact Avg: 2.1 (Team Avg: 2.0) ✅
  
🎯 Category Distribution
  New Work: 54% (Team: 48%) ⭐
  Refactor: 26% (Team: 24%) ✅
  Help Others: 12% (Team: 15%) ⚠️
  Churn/Rework: 8% (Team: 13%) ⭐⭐

🤖 AI Usage
  Cursor Score: 84 (Team: 72) ⭐⭐
  Acceptance Rate: 81% (Team: 73%) ⭐
  Daily AI Usage: High & Consistent ✅

🚀 DORA Contribution
  Commits in Production: 287/342 (84%)
  Average Lead Time: 16h (Team: 22h) ⭐
  Zero Failure Commits: 98% ⭐

💪 Strengths
  1. Very high code efficiency (0.79)
  2. Excellent AI tool adoption (Score: 84)
  3. Low rework rate (8% vs team 13%)
  4. Fast delivery (16h lead time)

📚 Development Areas
  1. Increase "Help Others" collaboration
  2. Consider mentoring junior developers
  3. Share AI best practices with team

🎯 Overall Rating: 4.5/5 (High Performer)
```

**Visual Dashboard**:
- 6-aylık trend grafikleri
- Takım ile karşılaştırma radar chart
- Kategori evolution timeline

---

## Analiz Senaryoları

### Analiz 1: AI Kullanımının Performansa Etkisi

**Araştırma Sorusu**: "AI kullanan geliştiriciler daha üretken mi?"

**Analiz Adımları**:

1. **Geliştiricileri Gruplama**

```
Grup A (High AI Users): Cursor Score > 75
  - 8 developer
  - Avg commits/day: 4.2
  - Avg cefficiency: 0.78
  - Avg lead time: 18h

Grup B (Low AI Users): Cursor Score < 50
  - 6 developer
  - Avg commits/day: 2.8
  - Avg cefficiency: 0.68
  - Avg lead time: 32h
```

2. **Metrik Karşılaştırması**

| Metrik | High AI | Low AI | Fark |
|--------|---------|--------|------|
| Commits/day | 4.2 | 2.8 | +50% ⬆️ |
| cefficiency | 0.78 | 0.68 | +15% ⬆️ |
| Lead Time | 18h | 32h | -44% ⬆️ |
| Churn Rate | 14% | 26% | -46% ⬆️ |
| New Work % | 52% | 41% | +27% ⬆️ |

3. **İstatistiksel Analiz**

```python
# T-test for significance
from scipy import stats

high_ai_commits = [4.5, 4.1, 4.3, 4.0, 4.8, 3.9, 4.2, 4.4]
low_ai_commits = [3.1, 2.8, 2.6, 3.0, 2.9, 2.5]

t_stat, p_value = stats.ttest_ind(high_ai_commits, low_ai_commits)
# p_value < 0.05 → Statistically significant
```

4. **Sonuç**

✅ **AI kullanımı ile üretkenlik arasında güçlü pozitif korelasyon**

**Öneriler**:
- Tüm ekibe AI training programı
- Best practice sharing sessions
- AI tool adoption incentive

---

### Analiz 2: Sprint Velocity Optimizasyonu

**Problem**: "Sprint'lerde hangi faktörler hızı etkiliyor?"

**Veri Toplama** (Son 6 sprint):

| Sprint | Story Points | Commits | Avg Lead Time | Failure Rate | Velocity |
|--------|-------------|---------|---------------|--------------|----------|
| S37 | 45 | 142 | 28h | 15% | 38 |
| S38 | 48 | 156 | 24h | 12% | 42 |
| S39 | 42 | 138 | 26h | 18% | 35 |
| S40 | 50 | 168 | 20h | 10% | 47 |
| S41 | 52 | 172 | 18h | 8% | 50 |
| S42 | 54 | 178 | 16h | 6% | 53 |

**Korelasyon Analizi**:

```
Velocity vs Lead Time: -0.87 (Strong negative)
Velocity vs Failure Rate: -0.82 (Strong negative)
Velocity vs Commits: +0.94 (Very strong positive)
```

**Bulgular**:
1. **Lead time azaldıkça velocity artıyor** → Hızlı feedback döngüsü önemli
2. **Failure rate azaldıkça velocity artıyor** → Kalite hızı destekliyor
3. **Commit sayısı ile velocity doğru orantılı** → Küçük, sık commit'ler

**Optimizasyon Önerileri**:
- ✅ Deployment pipeline'ı hızlandırın (lead time ↓)
- ✅ Test coverage'ı artırın (failure rate ↓)
- ✅ Atomik commit culture'ı teşvik edin (commits ↑)

---

### Analiz 3: Takımlar Arası Karşılaştırma

**Senaryo**: 3 takım var, hangisi daha iyi perform ediyor?

**Dashboard View**: "Team Comparison"

```
📊 Team Performance Comparison (Q3 2024)

Team A (Backend) - 8 developers
  Avg Productivity Score: 78
  DORA Rating: High Performer ⭐⭐⭐
  Cursor Score: 75
  Churn Rate: 15%
  
Team B (Frontend) - 6 developers
  Avg Productivity Score: 82
  DORA Rating: Elite Performer ⭐⭐⭐⭐
  Cursor Score: 81
  Churn Rate: 11%
  
Team C (Mobile) - 5 developers
  Avg Productivity Score: 68
  DORA Rating: Medium Performer ⭐⭐
  Cursor Score: 58
  Churn Rate: 24%
```

**Detaylı Breakdown**:

| Metrik | Team A | Team B | Team C |
|--------|--------|--------|--------|
| Deployment/Week | 8 | 12 | 4 |
| Lead Time | 22h | 14h | 38h |
| Failure Rate | 12% | 7% | 19% |
| New Work % | 48% | 54% | 42% |
| AI Adoption | 87% | 100% | 60% |

**Analiz**:

**Team B (Best Performer)**:
- ✅ En yüksek AI adoption (%100)
- ✅ En düşük lead time (14h)
- ✅ En sık deployment (12/week)
- ✅ En düşük churn rate (%11)

**Team C (Needs Improvement)**:
- ❌ Düşük AI adoption (%60)
- ❌ Yüksek lead time (38h)
- ❌ Az deployment (4/week)
- ❌ Yüksek churn rate (%24)

**Action Plan for Team C**:
1. **Week 1-2**: AI training workshop (Team B'den birini davet et)
2. **Week 3-4**: CI/CD pipeline optimization
3. **Week 5-8**: Code quality improvement (pairing with Team B)
4. **Week 9-12**: Re-assess and iterate

---

## Karşılaştırmalı Analizler

### Karşılaştırma 1: AI Öncesi vs Sonrası

**Senaryo**: Cursor adoption öncesi (Q1 2024) ve sonrası (Q3 2024) karşılaştırma.

**Q1 2024 (Before AI)**:
```
Average Commits/Developer/Day: 3.2
Average cefficiency: 0.69
Average Lead Time: 32 hours
Churn/Rework Rate: 22%
Deployment Frequency: 6/week
```

**Q3 2024 (After AI)**:
```
Average Commits/Developer/Day: 4.1 (+28%)
Average cefficiency: 0.76 (+10%)
Average Lead Time: 18 hours (-44%)
Churn/Rework Rate: 14% (-36%)
Deployment Frequency: 10/week (+67%)
```

**ROI Hesaplama**:
```
Cost:
  - Cursor licenses: 24 × $20/month = $480/month
  
Benefit:
  - Time saved: ~900 hours/month
  - Hourly rate: $50
  - Value: $45,000/month
  
ROI: (45,000 - 480) / 480 × 100 = 9,275% 🚀
```

---

### Karşılaştırma 2: Junior vs Senior Developers

**Dashboard Filter**: Compare by Seniority

**Junior Developers (0-2 years)**:
```
Avg Commits/Day: 2.8
Avg cefficiency: 0.68
Cursor Score: 72
Churn Rate: 24%
Help Others: 8%

With AI Training (+3 months):
Avg Commits/Day: 3.5 (+25%)
Avg cefficiency: 0.74 (+9%)
Cursor Score: 79 (+10%)
Churn Rate: 18% (-25%)
```

**Senior Developers (5+ years)**:
```
Avg Commits/Day: 4.2
Avg cefficiency: 0.79
Cursor Score: 68
Churn Rate: 12%
Help Others: 22%

With AI Training (+3 months):
Avg Commits/Day: 5.1 (+21%)
Avg cefficiency: 0.82 (+4%)
Cursor Score: 82 (+21%)
Churn Rate: 10% (-17%)
```

**Insight**: 
- Junior'lar AI'dan daha fazla faydalanıyor (churn reduction)
- Senior'lar AI'ı daha hızlı benimsiyor (cursor score improvement)
- Her iki grup da commit sayısında artış

---

## Karar Destek Örnekleri

### Karar 1: Yeni Ekip Üyesi Almak mı, AI Adoption mı?

**Durum**: Capacity artırma ihtiyacı var.

**Seçenek A**: Yeni Junior Developer
```
Cost: $60,000/year
Ramp-up time: 3-6 months
Capacity increase: +15-20% (after ramp-up)
Risk: Recruitment, training, retention
```

**Seçenek B**: AI Tools + Existing Team Training
```
Cost: $15,000/year (licenses + training)
Ramp-up time: 1-2 months
Capacity increase: +25-30% (based on data)
Risk: Adoption resistance, learning curve
```

**Dashboard Data**:
- Current team AI adoption: 65%
- Team with 90%+ adoption: 28% more productive
- Time saved with AI: 180h/month/team

**Karar**: Seçenek B → AI adoption'ı push et
**ROI**: 4x daha iyi, 2x daha hızlı

---

### Karar 2: Hangi Takıma Refactoring Sprint'i Verilmeli?

**Durum**: Q4'te 1 sprint refactoring için ayrılacak.

**Team A Metrics**:
```
Technical Debt Score: 68
Churn Rate: 18%
Refactor %: 22%
Deployment Issues: 12/month
```

**Team B Metrics**:
```
Technical Debt Score: 82
Churn Rate: 28%
Refactor %: 15%
Deployment Issues: 24/month
```

**Dashboard Analysis**: Team B açıkça daha fazla refactoring'e ihtiyaç var.

**Karar**: Team B'ye refactoring sprint
**Expected Outcome**:
- Churn rate: 28% → 18%
- Deployment issues: 24 → 12
- Lead time: -30%

---

## Özet

Bu örnekler, dashboard'un farklı kullanım senaryolarını göstermektedir:

✅ **Individual Performance Tracking**
✅ **Team Productivity Analysis**
✅ **AI Impact Measurement**
✅ **DORA Metrics Monitoring**
✅ **Data-Driven Decision Making**

Dashboard'u bu şekilde kullanarak:
- 📊 Objective data ile kararlar alırsınız
- 🎯 Clear goals ve targets belirlersiniz
- 📈 Continuous improvement sağlarsınız
- 🤖 AI adoption'ı optimize edersiniz
- 👥 Team collaboration'ı artırırsınız

