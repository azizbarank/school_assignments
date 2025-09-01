#!/usr/bin/env python3
"""
Extract evaluation results to CSV format for analysis and submission.
"""

import json
import csv
from pathlib import Path

def extract_results_to_csv(json_file_path, csv_file_path):
    """
    Extract evaluation results from JSON to CSV format.
    """
    
    # Load the JSON results
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Prepare CSV data
    csv_data = []
    
    # Add header
    header = [
        'Sentence_ID',
        'Sentence', 
        'Ground_Truth_Entities',
        'Predicted_Entities',
        'True_Positives',
        'False_Positives', 
        'False_Negatives',
        'Precision',
        'Recall',
        'F1_Score',
        'Perfect_Match'
    ]
    
    csv_data.append(header)
    
    # Process each sentence
    for i, result in enumerate(data['detailed_results'], 1):
        row = [
            i,  # Sentence ID
            result['sentence'],
            '; '.join(result['true_entities']),  # Join with semicolon for readability
            '; '.join(result['predicted_entities']),
            result['metrics']['tp'],
            result['metrics']['fp'], 
            result['metrics']['fn'],
            round(result['metrics']['precision'], 3),
            round(result['metrics']['recall'], 3),
            round(result['metrics']['f1'], 3),
            'Yes' if result['metrics']['f1'] == 1.0 else 'No'  # Perfect match indicator
        ]
        csv_data.append(row)
    
    # Write to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    print(f"✅ Results extracted to: {csv_file_path}")
    print(f"📊 Total sentences: {len(data['detailed_results'])}")
    
    # Print summary statistics
    overall = data['overall_metrics']
    print(f"\n📈 Overall Results:")
    print(f"   Precision: {overall['precision']:.3f}")
    print(f"   Recall:    {overall['recall']:.3f}")
    print(f"   F1-Score:  {overall['f1']:.3f}")
    print(f"   True Positives:  {overall['total_tp']}")
    print(f"   False Positives: {overall['total_fp']}")
    print(f"   False Negatives: {overall['total_fn']}")
    
    # Additional statistics
    perfect_matches = sum(1 for result in data['detailed_results'] if result['metrics']['f1'] == 1.0)
    zero_matches = sum(1 for result in data['detailed_results'] if result['metrics']['f1'] == 0.0)
    
    print(f"\n🎯 Performance Breakdown:")
    print(f"   Perfect matches (F1=1.0): {perfect_matches}/{len(data['detailed_results'])} ({perfect_matches/len(data['detailed_results'])*100:.1f}%)")
    print(f"   Zero matches (F1=0.0):    {zero_matches}/{len(data['detailed_results'])} ({zero_matches/len(data['detailed_results'])*100:.1f}%)")
    print(f"   Partial matches:          {len(data['detailed_results']) - perfect_matches - zero_matches}/{len(data['detailed_results'])} ({(len(data['detailed_results']) - perfect_matches - zero_matches)/len(data['detailed_results'])*100:.1f}%)")
    
    return csv_file_path

if __name__ == "__main__":
    json_file = "evaluation_results_100samples.json"
    csv_file = "evaluation_dataset_100sentences.csv"
    
    if Path(json_file).exists():
        extract_results_to_csv(json_file, csv_file)
    else:
        print(f"❌ Error: {json_file} not found!")
        print("Make sure you have run the full evaluation first.")