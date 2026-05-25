# Fintech Review Analytics

This repository contains a comprehensive pipeline for analyzing customer reviews of fintech applications for three banks namely Commercial Bank of Ethiopia, Bank of Abyssinia, and Dashen Bank. It first uses google play scraper to scrape raw data from the web and then uses Natural Language Processing (NLP) to extract sentiments, themes, and business insights.

## Project Structure
```text
fintech-review-analytics/
├── .vscode/               # Editor settings
├── .github/workflows/     # CI/CD (Unit tests)
├── data/                  # Data directory (gitignored *.csv)
│   └── processed/         # Raw review data as well as the analyzed data
├── notebooks/             # Exploratory analysis & Demos
├── src/                   # Source code (modular logic)
├── tests/                 # Unit tests
├── scripts/               # Production scripts
└── requirements.txt       # Dependencies
```

## Getting Started
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the data collection and preprocessing:
   ```bash
   python scripts/scrape_reviews.py
   python scripts/preprocess_data.py
   ```

## Task 1: Data Collection and Preprocessing

### Scraping Methodology
- **Library**: `google-play-scraper`
- **Targets**: 
  - Telebirr (`cn.tydic.ethiopay`)
  - CBE Birr (`prod.cbe.birr`)
  - Bank of Abyssinia Apollo (`com.boa.apollo`)
- **Parameters**: Collected all available reviews with `country='et'` and `lang='en'`.
- **Date Range**: 2020-08-06 to 2026-05-13.
- **Fields Collected**: Review text, rating (1–5), review date, bank name, source ("Google Play").

### Preprocessing Steps
1. **Deduplication**: Removed duplicate reviews based on content, bank, and date.
2. **Missing Value Handling**: Dropped rows missing review text or rating.
3. **Date Normalization**: Converted all dates to `YYYY-MM-DD` format.
4. **Export**: Saved cleaned dataset as `data/cleaned_reviews.csv`.

### KPIs Achieved
- **Volume**: 20,781+ reviews collected (Target: 1,200+).
- **Data Quality**: <1% missing data dropped during preprocessing.
- **Organization**: Clean CSV generated with all required columns.

## Key Features
- **Sentiment Analysis**: Comparative analysis using TextBlob, VADER, and DistilBERT.
- **Thematic Mapping**: Rule-based categorization of reviews into business themes (Stability, UX, Features, etc.).
- **Visual Analytics**: Distribution plots and theme-sentiment divergence charts.

## Error Handling & Testing
- Robust data loading with type checking and file existence verification.
- Unit tests for text preprocessing and sentiment logic in the `tests/` directory.
- Automated testing via GitHub Actions.





## 📊 Data Scraping Methodology & Metadata

This component of the pipeline is responsible for extracting public user feedback from the Google Play Store for major Ethiopian banking applications. The collected dataset serves as the foundational raw input for our downstream fintech sentiment analysis model.

### ⚙️ Scraping Methodology

We utilize the `google_play_scraper` library, a lightweight Python package that executes native HTTP requests to the Google Play Store endpoints, bypassing the need for heavy browser automation tools like Selenium or external API keys.

1. **Target Identification:** 
   We map target institutions to their unique Play Store package identifiers:
   * **Commercial Bank of Ethiopia (CBE):** `com.combanketh.mobilebanking`
   * **Bank of Abyssinia (BoA):** `com.boa.boaMobileBanking`
   * **Dashen Bank:** `com.dashen.dashensuperapp`


2. **Extraction Parameters:**
   * **Language (`lang`):** `en` (English)
   * **Location (`country`):** `et` (Ethiopia)
   * **Sorting Strategy:** `Sort.NEWEST` (Ensures the most recent user experiences are prioritized)
   * **Target Volume:** Up to 500 reviews per application to ensure statistical relevance across competing platforms.

3. **Data Pipeline Workflow:**
   The script dynamically loops through each identifier, handles potential 404/network exceptions gracefully without breaking execution, extracts specific schemas, flattens the records, and appends a `bank` origin tag.

---

### 📅 Temporal Scope (Date Range)

* **Collection Date:** May 17, 2026
* **Data Horizon:** The dataset spans from **Feburary 14, 2025** to **May 15, 2026**. 
  *(Note: Because we capped the extraction at a maximum of 500 reviews per bank sorted by `NEWEST`, the exact starting date varies per bank depending on their individual review velocity).*

---

### ⚠️ Technical & Data Limitations

When analyzing or expanding this dataset, keep the following architectural limitations in mind:

* **The 500-Count Threshold:** To optimize script execution and prevent IP throttling, collection is capped at 500 reviews per bank. This creates a data bottleneck for highly active apps (like CBE), capturing only their most recent history, while capturing a much wider historical footprint for banks with lower daily review volumes.
* **Language Filtering Constraints:** The scraping request specifies `lang='en'`. However, the Google Play Store algorithm often includes hybrid reviews (e.g., mixtures of English characters writing Amharic/Afan Oromo phrases, or pure Amharic text if the user's system language overrode the request). A dedicated text-cleaning preprocessing step is required before modeling.
* **Dynamic App ID Volatility:** Financial institutions occasionally rebuild or rebrand their mobile applications (e.g., Dashen Bank migrating from traditional IDs to `com.dashen.dashensuperapp`). Hardcoded identifiers require routine monitoring to avoid `404 NotFound` execution crashes.
* **Anonymized Metadata:** The Play Store API does not provide demographic details, user location history (beyond the global country store filter), or hardware specifications unless explicitly mentioned by the user in the comment text.


## 🧹 Preprocessing Quality Report

To prepare the text for modeling, our cleaning pipeline removes duplicate records, null entries, and extreme outliers (e.g., empty reviews or accidental spam clicks). Below is the diagnostic summary of our processing pipeline across all target applications.

### 📊 Preprocessing Performance Matrix

| Metric | Commercial Bank of Ethiopia | Bank of Abyssinia | Dashen Bank |
| :--- | :---: | :---: | :---: |
| **Raw Volume Collected** | 500 | 500 | 500 |
| **Cleaned Volume** | 500 | 500 | 500 |
| **Dropped Records** | 0 | 0 | 0 |
| **Data Retention %** | 100% | 100% | 100% |
| **Pipeline Quality Tier** | **EXCELLENT** | **EXCELLENT** | **EXCELLENT** |
| **Temporal Span Covered** | *2026-03-03* to *2026-05-15* | *2025-02-14* to *2026-05-14* | *2025-08-14* to *2026-05-14* |

### 🔍 Data Structure & Post-Clean Schema

Following pipeline execution, all records are saved to `data/processed/combined_bank_reviews_clean.csv` enforcing a unified relational layout:

* **`review_id`** *(String)*: Unique transaction hash generated by the Play Store engine.
* **`review`** *(String)*: Normalized user comment content (stripped of double spacing and formatting artifacts).
* **`rating`** *(Integer)*: Scale array ranging from 1 (poor) to 5 (excellent).
* **`date`** *(Timestamp)*: Absolute ISO submission index.
* **`bank`** *(String)*: Categorical label tracking corporate source location.
* **`source`** *(String)*: Origin platform tracking anchor (`Google Play`).

##  Sentiment Analysis & Comparative Pipeline

This module applies three distinct algorithmic approaches—ranging from traditional rule-based lexicon dictionaries to deep learning transformer architectures—to map and evaluate customer sentiment distributions for major Ethiopian banking institutions (**CBE, Bank of Abyssinia, and Dashen Bank**).

### 📊 Sentiment Framework Configurations
To ensure an equitable side-by-side distribution comparison, all framework scores are normalized and mapped onto an identical 3-way distribution spectrum (`POSITIVE`, `NEUTRAL`, `NEGATIVE`) using the following thresholds:

*   **VADER (Valence Aware Dictionary and sEntiment Reasoner):** Captures sentiment strings utilizing a localized baseline lexicon map. Evaluated via the global `compound` metric score using standard benchmarks:
    *   **POSITIVE:** Score $\ge 0.05$
    *   **NEGATIVE:** Score $\le -0.05$
    *   **NEUTRAL:** $-0.05 < \text{Score} < 0.05$
*   **TextBlob:** Parses text records to compute semantic polarity and baseline phrase subjectivity indicators. Thresholded similarly to VADER for structural alignment:
    *   **POSITIVE:** Score $\ge 0.05$
    *   **NEGATIVE:** Score $\le -0.05$
    *   **NEUTRAL:** $-0.05 < \text{Score} < 0.05$
*   **DistilBERT Transformer (`distilbert-base-uncased-finetuned-sst-2-english`):** A context-aware deep learning pipeline model. Since the underlying architecture is natively binary (outputs only binary `POSITIVE`/`NEGATIVE` classes), an implicit **Neutrality Interceptor** is implemented:
    *   If the model's prediction confidence score sits below **70% (`< 0.70`)**, the record is flagged as **NEUTRAL** due to high context ambiguity.
    *   If confidence is $\ge 0.70$, the model's native label assignment is preserved.

---

### 🔍 Architectural Insights & Limitations

During model benchmarking, distinct behavioral traits were observed regarding how the frameworks handle raw, non-filtered app store reviews containing multi-language elements (such as Ge'ez characters or Amharic phrases written in Latin script):

1.  **Lexicon Vulnerability (VADER & TextBlob):** These engines depend strictly on an English word matrix. When analyzing text strings containing localized Amharic idioms or transliterations, they fail to find keyword matches and safely default the review to **NEUTRAL (0.0)**. This generates an artificially high neutral baseline distribution.
2.  **Transformer Overconfidence (DistilBERT):** As a contextual model, DistilBERT attempts to break down foreign character clusters into English sub-tokens. This can result in aggressive classification patterns with misleadingly high confidence scores on text entries it does not natively understand.

---

### 📈 Current Execution Results Matrix


| Bank | Framework | % POSITIVE | % NEUTRAL | % NEGATIVE |
| :--- | :--- | :---: | :---: | :---: |
| **CBE** | VADER | `68.00` | `22.00` | `10.00` |
| | TextBlob | `66.00` | `28.00` | `6.00` |
| | DistilBERT | `67.00` | `3.00` | `30.00` |
| **Abyssinia**| VADER | `53.00` | `29.00` | `18.00` |
| | TextBlob | `54.00` | `34.00` | `12.00` |
| | DistilBERT | `52.00` | `5.00` | `43.00` |
| **Dashen** | VADER | `64.00` | `22.00` | `14.00` |
| | TextBlob | `63.00` | `26.00` | `11.00` |
| | DistilBERT | `63.00` | `3.00` | `34.00` |


##  Sentiment Aggregation & Cross-Validation Metrics

This pipeline stage shifts focus from individual string classification to population-level cross-validation, grouping metrics across independent variables: **Banking Institution** and **User Star Rating (1–5)**. 

### 📐 Metric Aggregation Architecture
By tracking the cross-section of app store star ratings against the algorithmic results, we assess the predictive convergence of rule-based dictionaries versus deep-learning contexts:

1.  **VADER Matrix Correlation:** Quantifies sentiment intensity values against explicit star ratings. Historically, 1-star reviews should tightly converge toward a negative baseline ($\approx -0.6$), whereas 5-star ratings should align with a strong positive ceiling ($\approx +0.7$).
2.  **TextBlob Polar Matrix:** Provides a smooth linear slope mapping sentiment valence. TextBlob calculates explicit semantic phrase metrics, which allow it to establish baseline validations alongside VADER.
3.  **Transformer Sentiment Distribution:** Validates our custom **Neutrality Interceptor** logic. The score vector utilizes a sign-mapping logic: $\text{Label Class} \times \text{Confidence Probability Value}$, mapping deep-learning context perfectly onto a standard $-1.0$ to $+1.0$ comparative chart scale.

---

### 📊 Metric Aggregation Visualizations Template
The workflow automatically stores, aggregates, and outputs three corresponding trend charts inside the notebook directory:
*   `Average VADER Sentiment by Bank and Star Rating`
*   `Average TextBlob Polarity by Bank and Star Rating`
*   `Average Transformer Sentiment by Bank and Star Rating`

##  Thematic Analysis & Business Logic Mapping

This phase moves beyond global sentiment polarity to discover the **root causes** of user satisfaction or frustration by organizing feedback into five business-critical domains.

### 🧩 Methodology
1. **Keyword Discovery:** Utilized `TfidfVectorizer` to extract statistically significant n-grams (unigrams and bigrams) per financial institution. This ensures that our thematic boundary definitions are derived from actual customer vocabulary.
2. **Heuristic Keyword Mapping:** Implemented a robust `THEME_MAP` classifier to bucket incoming text streams into five distinct target pillars:
   * **System Stability:** Backend performance, server connectivity, and application crashes.
   * **Authentication & Access:** Onboarding barriers, OTP generation issues, and login bottlenecks.
   * **User Experience (UX):** Front-end UI aesthetics, navigation fluidness, and interface layout clarity.
   * **Financial Transactions:** Core functional features including mobile money transfers, bill payments, and balance tracking.
   * **Support & Trust:** Human customer service interactions, problem resolution velocity, and platform trust metrics.
3. **Sentiment-Theme Cross-Correlation:** Cross-referenced VADER compound sentiment averages against the assigned themes to isolate functional **Drivers** (positive vectors) from engineering **Pain Points** (negative vectors).

### 📈 Operational Insights Matrix
The workflow outputs a normalized distribution table showing how each bank's feedback is segmented among the five main themes:

| Bank | System Stability | Authentication & Access | User Experience (UX) | Financial Transactions | Support & Trust | General/Other |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CBE** | `0.07%` | `0.01%` | `0.04%` | `0.06%` | `0.04%` | `0.77%` |
| **Abyssinia**| `0.13%` | `0.03%` | `0.02%` | `0.03%` | `0.06%` | `0.73%` |
| **Dashen** | `0.08%` | `0.05%` | `0.09%` | `0.03%` | `0.04%` | `0.70%` |


