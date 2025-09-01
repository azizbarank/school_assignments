# Entity Linking Evaluation with Azure OpenAI - MultiNERD Dutch

> **Evaluation of Azure OpenAI GPT-4o-mini for entity linking on Dutch Wikipedia titles**

## 🎯 Key Results

| Metric | Score |
|--------|-------|
| **Precision** | **55.4%** (77/139 predictions correct) |
| **Recall** | **57.9%** (77/133 entities found) |
| **F1-Score** | **56.6%** |
| **Perfect Matches** | **39/100** sentences (39%) |
| **Complete Failures** | **38/100** sentences (38%) |
| **Partial Matches** | **23/100** sentences (23%) |

## 📊 Executive Summary

This study evaluates Azure OpenAI's GPT-4o-mini model for linking Dutch named entities to Wikipedia page titles using the MultiNERD dataset. The model achieved moderate performance with an F1-score of 56.6%, correctly identifying 77 out of 133 total entities across 100 randomly sampled sentences.

**Key Findings:**
- **Disambiguation challenges**: Model struggles with Wikipedia disambiguation pages (e.g., "Antwerpen" vs "Antwerpen_(stad)")
- **Strong geographic performance**: High accuracy for well-known cities and countries
- **Person name difficulties**: Issues with historical figures and abbreviated names
- **Consistent partial matches**: 23% of sentences had partial success, indicating promising foundational understanding

## 🔍 Error Analysis

### Main Error Categories

1. **Disambiguation Errors (33% of errors)**
   - Predicted simplified versions instead of specific Wikipedia titles
   - Example: "Antwerpen" instead of "Antwerpen_(stad)"
   - Example: "Astra" instead of "SES_Astra"

2. **Complete Misses (45% of errors)** 
   - Failed to identify entities that were clearly present
   - Often missed when multiple entities appeared in complex sentences
   - Historical figures and technical organizations particularly affected

3. **Hallucinations (22% of errors)**
   - Predicted entities not present in ground truth
   - Generic terms mistaken for specific entities (e.g., "organisatie", "Keizerrijk")
   - Abbreviation confusion (e.g., "C.H. Peters" vs "Cornelis_Peters")

## 📈 Performance Breakdown

### By Match Quality
- **Perfect F1=1.0**: 39 sentences (39%) - Complete success
- **Zero F1=0.0**: 38 sentences (38%) - Complete failure  
- **Partial F1>0.0**: 23 sentences (23%) - Mixed results

### By Entity Complexity
- **Simple geographic names**: ~75% success rate
- **Historical events**: ~65% success rate  
- **Person names with abbreviations**: ~30% success rate
- **Disambiguation pages**: ~25% success rate

## 🛠️ Methodology

### Dataset & Sampling
- **Source**: MultiNERD Dutch development set (`dev_nl.tsv`)
- **Sample**: 100 randomly selected sentences (seed=42)
- **Entities**: Person (PER), Location (LOC), Organization (ORG) only
- **Excluded**: Animals, food, diseases, plants, time expressions

### Evaluation Setup
- **Matching**: Flexible matching (underscores ↔ spaces)
- **Metrics**: Precision, Recall, F1-score per sentence + overall
- **Ground Truth**: Wikipedia page titles from MultiNERD annotations

## 🗂️ Files & Data

### Core Results
- **`evaluation_dataset_100sentences.csv`** - Complete dataset with all 100 sentences, predictions, and metrics
- **`evaluation_results_100samples.json`** - Detailed JSON results with full evaluation data

### Implementation Files
- **`evaluation.py`** - Main evaluation script with Azure OpenAI integration
- **`data.py`** - Data loading and sampling from MultiNERD TSV
- **`openai_test.py`** - API connection testing script
- **`extract_results_to_csv.py`** - Utility to convert JSON results to CSV
- **`error_analysis.py`** - Detailed error pattern analysis

### Configuration
- **`.env`** - Azure OpenAI credentials and configuration
- **`dev_nl.tsv`** - MultiNERD Dutch development dataset

## 🚀 Usage Instructions

### Prerequisites
```bash
pip install openai python-dotenv
```

### Configuration
Create `.env` file with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

### Running the Evaluation
```bash
# Test API connection first
python openai_test.py

# Run full evaluation (interactive - choose 1, 2, or 3 for sample size)
python evaluation.py

# Or run specific sizes directly
echo "1" | python evaluation.py  # 5 sentences
echo "2" | python evaluation.py  # 25 sentences  
echo "3" | python evaluation.py  # 100 sentences
```

### Analyzing Results
```bash
# Extract results to CSV format
python extract_results_to_csv.py

# Perform detailed error analysis
python error_analysis.py
```

### Reproducibility
- Fixed random seed (42) ensures consistent sampling
- Complete parameter documentation
- All intermediate results saved for analysis

---