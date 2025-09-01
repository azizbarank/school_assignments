#!/usr/bin/env python3
"""
Detailed error analysis for the entity linking evaluation.
"""

import json
from collections import Counter, defaultdict

def analyze_errors(json_file_path):
    """
    Analyze error patterns from evaluation results.
    """
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Collect error examples
    disambiguation_errors = []
    partial_match_errors = []
    complete_miss_errors = []
    hallucination_errors = []
    
    for result in data['detailed_results']:
        sentence = result['sentence']
        true_entities = result['true_entities'] 
        predicted_entities = result['predicted_entities']
        
        # Normalize for comparison
        def normalize(entity):
            return entity.lower().replace('_', ' ')
        
        true_normalized = [normalize(e) for e in true_entities]
        pred_normalized = [normalize(e) for e in predicted_entities]
        
        # Analyze each error type
        for pred in predicted_entities:
            pred_norm = normalize(pred)
            if pred_norm not in true_normalized:
                # Check if it's a disambiguation issue
                if any(pred_norm in true_norm or true_norm in pred_norm for true_norm in true_normalized):
                    disambiguation_errors.append({
                        'sentence': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                        'predicted': pred,
                        'closest_true': [t for t in true_entities if normalize(t) in pred_norm or pred_norm in normalize(t)][0] if any(normalize(t) in pred_norm or pred_norm in normalize(t) for t in true_entities) else 'N/A'
                    })
                else:
                    hallucination_errors.append({
                        'sentence': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                        'predicted': pred,
                        'true_entities': true_entities
                    })
        
        for true in true_entities:
            true_norm = normalize(true)
            if true_norm not in pred_normalized:
                complete_miss_errors.append({
                    'sentence': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                    'missed': true,
                    'predicted_entities': predicted_entities
                })
    
    return {
        'disambiguation_errors': disambiguation_errors[:10],  # Top 10
        'complete_miss_errors': complete_miss_errors[:10],
        'hallucination_errors': hallucination_errors[:10]
    }

if __name__ == "__main__":
    json_file = "evaluation_results_100samples.json"
    
    errors = analyze_errors(json_file)
    
    print("🔍 DETAILED ERROR ANALYSIS")
    print("=" * 60)
    
    print(f"\n🎯 DISAMBIGUATION ERRORS (predicted similar but wrong variant):")
    print(f"Found {len(errors['disambiguation_errors'])} examples:")
    for i, error in enumerate(errors['disambiguation_errors'][:5], 1):
        print(f"  {i}. Predicted: '{error['predicted']}' | True: '{error['closest_true']}'")
        print(f"     Sentence: {error['sentence']}\n")
    
    print(f"\n❌ COMPLETE MISSES (entities not found at all):")  
    print(f"Found {len(errors['complete_miss_errors'])} examples:")
    for i, error in enumerate(errors['complete_miss_errors'][:5], 1):
        print(f"  {i}. Missed: '{error['missed']}'")
        print(f"     Predicted: {error['predicted_entities']}")
        print(f"     Sentence: {error['sentence']}\n")
        
    print(f"\n👻 HALLUCINATIONS (predicted non-existent entities):")
    print(f"Found {len(errors['hallucination_errors'])} examples:")  
    for i, error in enumerate(errors['hallucination_errors'][:5], 1):
        print(f"  {i}. Hallucinated: '{error['predicted']}'")
        print(f"     True entities: {error['true_entities']}")
        print(f"     Sentence: {error['sentence']}\n")