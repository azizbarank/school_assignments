#!/usr/bin/env python3
"""
Entity Linking Evaluation for MultiNERD

This script evaluates LLM performance on entity linking using MultiNERD Dutch development data.
We compare predicted Wikipedia page titles from OpenAI GPT models against ground truth annotations.
"""

import csv
import json
import random
import os
from collections import defaultdict
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

def load_multinerd_data(file_path="dev_nl.tsv", max_sentences=100):
    """
    Load MultiNERD data and extract sentences with their Wikipedia page titles.
    
    Args:
        file_path: Path to the TSV file
        max_sentences: Maximum number of sentences to process
    
    Returns:
        List of dictionaries with 'sentence' and 'entities' keys
    """
    def filter_entity_type(tag):
        try:
            entity_class = tag.split('-')[1]
        except:
            entity_class = 'MISSING'
        # Filter out lower-case concepts and years
        return entity_class not in ['ANIM', 'FOOD', 'DIS', 'PLANT', 'TIME']
    
    def detokenize(tokens):
        string = ' '.join(tokens)
        string = string.replace(' - ', '-')  # Engels - Nederlandse
        string = string.replace(' e ', 'e ')  # 19 e eeuw
        return string
    
    annotations = []
    
    with open(file_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        tokens = []
        entities = []
        count = 0
        
        for row in reader:
            if len(row) >= 3:  # Token row
                tokens.append(row[1])  # Add token
                if len(row) > 6 and row[6] and filter_entity_type(row[2]):
                    entities.append(row[6])  # Add Wikipedia title
            else:  # End of sentence
                if entities and count < max_sentences:
                    sentence = detokenize(tokens)
                    annotations.append({
                        'sentence': sentence,
                        'entities': list(set(entities))  # Remove duplicates
                    })
                    count += 1
                
                # Reset for next sentence
                entities = []
                tokens = []
    
    return annotations

def get_random_sample(data, sample_size=100, seed=42):
    """
    Get a random sample of sentences for evaluation.
    """
    random.seed(seed)
    
    if len(data) <= sample_size:
        return data
    
    return random.sample(data, sample_size)

def get_entity_links(sentence, client, deployment_name):
    """
    Get Wikipedia page titles for named entities in a Dutch sentence using Azure OpenAI.
    """
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "Je bent een expert in het herkennen van named entities in Nederlandse tekst. Geef voor elke named entity (persoon, plaats, organisatie) de exacte Wikipedia pagina titel terug."
                },
                {
                    "role": "user",
                    "content": f"Geef de Wikipedia pagina titels voor alle named entities in deze Nederlandse zin: '{sentence}'\n\nGeef alleen de Wikipedia titels terug, gescheiden door komma's. Als er geen entities zijn, antwoord met 'Geen'."
                }
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.lower() in ['geen', 'none', '']:
            return []
        
        # Parse and clean the response
        titles = [title.strip() for title in result.split(',')]
        return [t for t in titles if t]  # Remove empty strings
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return []

def normalize_title(title):
    """
    Normalize Wikipedia titles for comparison.
    Handles underscores vs spaces: "SES_Astra" <-> "SES Astra"
    """
    if not title:
        return ""
    
    # Convert to lowercase and replace underscores with spaces
    normalized = title.lower().replace('_', ' ').strip()
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized

def calculate_metrics(predicted_entities, true_entities):
    """
    Calculate precision, recall, and F1-score for entity linking.
    
    Args:
        predicted_entities: List of predicted Wikipedia titles
        true_entities: List of ground truth Wikipedia titles
    
    Returns:
        Dictionary with precision, recall, f1, tp, fp, fn
    """
    # Normalize titles for comparison
    pred_normalized = set(normalize_title(e) for e in predicted_entities)
    true_normalized = set(normalize_title(e) for e in true_entities)
    
    # Calculate metrics
    tp = len(pred_normalized & true_normalized)  # True positives
    fp = len(pred_normalized - true_normalized)  # False positives  
    fn = len(true_normalized - pred_normalized)  # False negatives
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'precision': precision,
        'recall': recall, 
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'fn': fn
    }

def evaluate_sample(sample_data, client, deployment_name, max_samples=10):
    """
    Evaluate entity linking performance on a sample of sentences.
    
    Args:
        sample_data: List of sentences with ground truth entities
        client: OpenAI client instance
        max_samples: Maximum number of samples to evaluate (for testing)
    
    Returns:
        Dictionary with overall metrics and detailed results
    """
    results = []
    all_metrics = []
    error_analysis = defaultdict(list)
    
    print(f"Evaluating {min(len(sample_data), max_samples)} sentences...\n")
    
    for i, item in enumerate(sample_data[:max_samples]):
        sentence = item['sentence']
        true_entities = item['entities']
        
        print(f"\n[{i+1}] Sentence: {sentence}")
        print(f"Ground truth: {true_entities}")
        
        # Get predictions
        predicted_entities = get_entity_links(sentence, client, deployment_name)
        print(f"Predicted: {predicted_entities}")
        
        # Calculate metrics for this sentence
        metrics = calculate_metrics(predicted_entities, true_entities)
        all_metrics.append(metrics)
        
        print(f"Metrics: P={metrics['precision']:.3f}, R={metrics['recall']:.3f}, F1={metrics['f1']:.3f}")
        
        # Store detailed results
        result = {
            'sentence': sentence,
            'true_entities': true_entities,
            'predicted_entities': predicted_entities,
            'metrics': metrics
        }
        results.append(result)
        
        # Error analysis
        if metrics['fp'] > 0:
            error_analysis['false_positives'].extend([
                e for e in predicted_entities 
                if normalize_title(e) not in set(normalize_title(t) for t in true_entities)
            ])
        
        if metrics['fn'] > 0:
            error_analysis['false_negatives'].extend([
                e for e in true_entities
                if normalize_title(e) not in set(normalize_title(p) for p in predicted_entities) 
            ])
    
    # Calculate overall metrics
    total_tp = sum(m['tp'] for m in all_metrics)
    total_fp = sum(m['fp'] for m in all_metrics) 
    total_fn = sum(m['fn'] for m in all_metrics)
    
    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1 = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0.0
    
    return {
        'overall_metrics': {
            'precision': overall_precision,
            'recall': overall_recall,
            'f1': overall_f1,
            'total_tp': total_tp,
            'total_fp': total_fp, 
            'total_fn': total_fn
        },
        'detailed_results': results,
        'error_analysis': dict(error_analysis)
    }

def print_evaluation_report(results):
    """
    Print a comprehensive evaluation report.
    """
    overall = results['overall_metrics']
    
    print("=" * 60)
    print("ENTITY LINKING EVALUATION REPORT")
    print("=" * 60)
    
    print(f"\n📊 OVERALL METRICS:")
    print(f"  Precision: {overall['precision']:.3f} ({overall['total_tp']}/{overall['total_tp'] + overall['total_fp']})")
    print(f"  Recall:    {overall['recall']:.3f} ({overall['total_tp']}/{overall['total_tp'] + overall['total_fn']})")
    print(f"  F1-Score:  {overall['f1']:.3f}")
    
    print(f"\n📈 COUNTS:")
    print(f"  True Positives:  {overall['total_tp']}")
    print(f"  False Positives: {overall['total_fp']}")
    print(f"  False Negatives: {overall['total_fn']}")
    
    # Error analysis
    errors = results['error_analysis']
    if errors:
        print(f"\n🔍 ERROR ANALYSIS:")
        
        if 'false_positives' in errors:
            fp_unique = list(set(errors['false_positives']))
            print(f"  Most common false positives ({len(fp_unique)} unique):")
            for fp in fp_unique[:10]:  # Show top 10
                print(f"    - {fp}")
        
        if 'false_negatives' in errors:
            fn_unique = list(set(errors['false_negatives']))
            print(f"  Most common false negatives ({len(fn_unique)} unique):")
            for fn in fn_unique[:10]:  # Show top 10
                print(f"    - {fn}")
    
    print(f"\n" + "=" * 60)

def main():
    """
    Main evaluation function.
    """
    # Load Azure OpenAI configuration
    load_dotenv()
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION')
    deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    
    if not all([api_key, endpoint, api_version, deployment_name]):
        print("Error: Missing Azure OpenAI configuration in .env file")
        print("Required: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME")
        return
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    
    print(f"Azure OpenAI Configuration:")
    print(f"  Endpoint: {endpoint}")
    print(f"  Deployment: {deployment_name}")
    print(f"  API Version: {api_version}")
    print()
    
    # Load the data
    print("Loading MultiNERD data...")
    data = load_multinerd_data()
    print(f"Loaded {len(data)} sentences with entities")
    
    if data:
        print(f"\nExample:")
        print(f"Sentence: {data[0]['sentence']}")
        print(f"Entities: {data[0]['entities']}")
    
    # Get sample for evaluation
    sample_data = get_random_sample(data, sample_size=100)
    print(f"\nSample size: {len(sample_data)}")
    
    # Test metrics function
    print("\n" + "="*40)
    print("TESTING METRICS CALCULATION")
    print("="*40)
    test_pred = ["Amsterdam", "Rotterdam", "New_York"]
    test_true = ["Amsterdam", "Rotterdam", "Antwerpen"]
    test_metrics = calculate_metrics(test_pred, test_true)
    print(f"Test prediction: {test_pred}")
    print(f"Test ground truth: {test_true}")
    print(f"Test metrics: {test_metrics}")
    
    # Ask user for evaluation size
    print("\n" + "="*40)
    print("EVALUATION OPTIONS")
    print("="*40)
    print("Choose evaluation size:")
    print("1. Small test (5 sentences) - Quick test, minimal API calls")
    print("2. Medium test (25 sentences) - Moderate evaluation")
    print("3. Full evaluation (100 sentences) - Complete evaluation, ~100 API calls")
    
    while True:
        choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        if choice == '1':
            max_samples = 5
            break
        elif choice == '2':
            max_samples = 25
            break
        elif choice == '3':
            max_samples = 100
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    # Run evaluation
    print(f"\nStarting evaluation with {max_samples} sentences...")
    print("This will make OpenAI API calls. Please wait...")
    
    evaluation_results = evaluate_sample(sample_data, client, deployment_name, max_samples=max_samples)
    
    # Print the report
    print_evaluation_report(evaluation_results)
    
    # Save results to file
    output_file = f'evaluation_results_{max_samples}samples.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary for assignment report
    overall = evaluation_results['overall_metrics']
    print(f"\n" + "="*40)
    print("SUMMARY FOR ASSIGNMENT REPORT")
    print("="*40)
    print(f"Evaluation Size: {max_samples} sentences")
    print(f"Precision: {overall['precision']:.3f}")
    print(f"Recall: {overall['recall']:.3f}")  
    print(f"F1-Score: {overall['f1']:.3f}")
    print(f"True Positives: {overall['total_tp']}")
    print(f"False Positives: {overall['total_fp']}")
    print(f"False Negatives: {overall['total_fn']}")

if __name__ == "__main__":
    main()