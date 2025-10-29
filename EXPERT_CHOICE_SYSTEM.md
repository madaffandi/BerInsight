# Expert Choice System - Multi-Criteria Decision Analysis (MCDA)

## Overview
BerInsight menggunakan **Expert Choice Algorithm** berbasis Multi-Criteria Decision Analysis (MCDA) untuk memprioritaskan insights dan memberikan rekomendasi actionable kepada tim yang tepat.

## Algoritma Scoring

### Kriteria & Bobot (Total 100%)

1. **Sentiment Analysis (30%)**
   - Negative: 90/100
   - Neutral: 50/100
   - Positive: 20/100
   - Rationale: Negative sentiment memerlukan perhatian segera

2. **Urgency (25%)**
   - Berdasarkan keyword detection: urgent, critical, issue, problem, error, failed, broken, crash, bug, security
   - Score = min(keyword_matches × 20, 100)
   - Rationale: Issue urgent harus diprioritaskan

3. **Engagement (20%)**
   - Berdasarkan word count dan content richness
   - Score = min((word_count / 50) × 100, 100)
   - Rationale: Content yang lebih detail menunjukkan tingkat engagement lebih tinggi

4. **Recency (15%)**
   - Score = max(100 - (days_since_published × 2), 0)
   - Decreases 2 points per day
   - Rationale: Insights terbaru lebih relevan

5. **Business Impact (10%)**
   - Berdasarkan keyword: system, security, data, customer, revenue, user, feature, integration, performance
   - Score = min(keyword_matches × 15, 100)
   - Rationale: Impact terhadap business metrics penting

### Formula Weighted Sum
```
Expert Score = (
  Sentiment × 0.30 +
  Urgency × 0.25 +
  Engagement × 0.20 +
  Recency × 0.15 +
  Impact × 0.10
)
```

## Prioritization Levels

| Expert Score | Priority | Action Required |
|--------------|----------|-----------------|
| 70-100       | High     | Immediate attention needed |
| 40-69        | Medium   | Review and plan action |
| 0-39         | Low      | Monitor and track |

## Team Assignment

Insights secara otomatis di-assign ke tim berdasarkan:

1. **Product Team**: Product mentions (BRImo, Card, Qlola, Loan, etc.)
2. **Engineering Team**: Technical keywords (bug, error, crash, performance)
3. **Marketing Team**: Social media channels (Instagram, Twitter, Facebook, YouTube)
4. **Customer Support Team**: Support-related keywords (help, service, support)

## Implementation Benefits

✅ **Objektif & Konsisten**: Menggunakan weighted scoring yang transparan
✅ **Multi-Dimensional**: Mempertimbangkan 5 aspek berbeda
✅ **Actionable**: Langsung memberikan rekomendasi tim dan action items
✅ **Scalable**: Dapat handle volume insights yang besar
✅ **Transparent**: Score breakdown tersedia untuk setiap insight

## Visualisasi di Dashboard

Setiap insight di halaman "Call to Action" menampilkan:
- 📊 **Expert Score Badge** (0-100)
- 🎯 **Score Breakdown** (5 kriteria detail)
- 🏷️ **Priority Label** (High/Medium/Low)
- 👥 **Recommended Team**
- ✅ **Action Items**

## Referensi
Sistem ini terinspirasi dari metodologi Expert Choice® dan Analytic Hierarchy Process (AHP) yang dikembangkan oleh Thomas L. Saaty untuk decision making kompleks.

---
**Last Updated**: October 30, 2025
**Version**: 1.0.0

