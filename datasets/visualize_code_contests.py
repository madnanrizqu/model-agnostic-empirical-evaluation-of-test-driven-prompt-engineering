#!/usr/bin/env python3
"""
Visualization script for the CodeContests dataset.
Generates comprehensive visualizations showing dataset distribution and characteristics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os
from datetime import datetime
import json
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('default')
sns.set_palette("husl")

class CodeContestsVisualizer:
    """Comprehensive visualizer for the CodeContests dataset."""
    
    def __init__(self, csv_path="code_contests.csv"):
        """Initialize the visualizer with dataset path."""
        self.csv_path = csv_path
        self.df = None
        self.output_dir = "code_contests_visualizations"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def load_data(self):
        """Load and preprocess the dataset."""
        print(f"Loading dataset from {self.csv_path}...")
        
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Dataset file not found: {self.csv_path}")
        
        self.df = pd.read_csv(self.csv_path)
        print(f"Dataset loaded successfully!")
        print(f"Shape: {self.df.shape[0]} problems, {self.df.shape[1]} columns")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Preprocess data
        self._preprocess_data()
        
    def _preprocess_data(self):
        """Preprocess the dataset for visualization."""
        # Add description length
        self.df['description_length'] = self.df['description'].str.len()
        
        # Parse cf_tags (convert string representation of list to actual list)
        def safe_parse_tags(tags_str):
            try:
                if pd.isna(tags_str) or tags_str == '[]':
                    return []
                return ast.literal_eval(tags_str)
            except:
                return []
        
        self.df['cf_tags_parsed'] = self.df['cf_tags'].apply(safe_parse_tags)
        self.df['num_tags'] = self.df['cf_tags_parsed'].apply(len)
        
        # Map difficulty to labels
        difficulty_map = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
        self.df['difficulty_label'] = self.df['difficulty'].map(difficulty_map)
        
        # Extract test case counts (from string arrays)
        def count_tests(test_str):
            try:
                if pd.isna(test_str):
                    return 0
                # Parse the numpy array string format
                if 'array([' in test_str:
                    # Count comma-separated items in array
                    return test_str.count(',') + 1 if ',' in test_str else 1
                return 0
            except:
                return 0
        
        self.df['public_tests_count'] = self.df['public_tests'].apply(count_tests)
        self.df['private_tests_count'] = self.df['private_tests'].apply(count_tests)
        self.df['generated_tests_count'] = self.df['generated_tests'].apply(count_tests)
        
        print("Data preprocessing completed!")
        
    def create_difficulty_distribution_viz(self):
        """Create visualizations for difficulty distribution."""
        print("Creating difficulty distribution visualizations...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Bar chart with counts and percentages
        difficulty_counts = self.df['difficulty_label'].value_counts()
        colors = ['#2E8B57', '#FFD700', '#CD5C5C']  # Green, Gold, Red
        
        bars = ax1.bar(difficulty_counts.index, difficulty_counts.values, color=colors)
        ax1.set_title('Problem Distribution by Difficulty Level', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Difficulty Level')
        ax1.set_ylabel('Number of Problems')
        
        # Add count labels on bars
        for bar, count in zip(bars, difficulty_counts.values):
            percentage = (count / len(self.df)) * 100
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                    f'{count}\n({percentage:.1f}%)', 
                    ha='center', va='bottom', fontweight='bold')
        
        # 2. Pie chart
        wedges, texts, autotexts = ax2.pie(difficulty_counts.values, 
                                          labels=difficulty_counts.index,
                                          colors=colors,
                                          autopct='%1.1f%%',
                                          startangle=90)
        ax2.set_title('Difficulty Distribution (Percentage)', fontsize=14, fontweight='bold')
        
        # 3. Horizontal bar with detailed stats
        ax3.barh(difficulty_counts.index, difficulty_counts.values, color=colors)
        ax3.set_title('Detailed Problem Counts by Difficulty', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Number of Problems')
        
        # Add detailed text
        for i, (label, count) in enumerate(difficulty_counts.items()):
            percentage = (count / len(self.df)) * 100
            ax3.text(count + 5, i, f'{count} problems ({percentage:.1f}%)', 
                    va='center', fontweight='bold')
        
        # 4. Summary statistics table
        ax4.axis('tight')
        ax4.axis('off')
        
        summary_data = []
        total_problems = len(self.df)
        for difficulty in ['Easy', 'Medium', 'Hard']:
            count = difficulty_counts.get(difficulty, 0)
            percentage = (count / total_problems) * 100
            summary_data.append([difficulty, count, f'{percentage:.1f}%'])
        
        summary_data.append(['TOTAL', total_problems, '100.0%'])
        
        table = ax4.table(cellText=summary_data,
                         colLabels=['Difficulty', 'Count', 'Percentage'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        ax4.set_title('Summary Statistics', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/difficulty_distribution_{self.timestamp}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_problem_characteristics_viz(self):
        """Create visualizations for problem characteristics."""
        print("Creating problem characteristics visualizations...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Description length distribution
        ax1.hist(self.df['description_length'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Distribution of Problem Description Lengths', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Description Length (characters)')
        ax1.set_ylabel('Number of Problems')
        ax1.axvline(self.df['description_length'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {self.df["description_length"].mean():.0f}')
        ax1.legend()
        
        # 2. Description length by difficulty
        sns.boxplot(data=self.df, x='difficulty_label', y='description_length', ax=ax2)
        ax2.set_title('Description Length by Difficulty Level', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Difficulty Level')
        ax2.set_ylabel('Description Length (characters)')
        
        # 3. Number of tags distribution
        tag_counts = self.df['num_tags'].value_counts().sort_index()
        ax3.bar(tag_counts.index, tag_counts.values, alpha=0.7, color='lightgreen', edgecolor='black')
        ax3.set_title('Distribution of Number of Tags per Problem', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Number of Tags')
        ax3.set_ylabel('Number of Problems')
        
        # 4. CF Rating distribution (if available)
        cf_ratings = self.df['cf_rating'][self.df['cf_rating'] > 0]
        if len(cf_ratings) > 0:
            ax4.hist(cf_ratings, bins=20, alpha=0.7, color='orange', edgecolor='black')
            ax4.set_title('Codeforces Rating Distribution', fontsize=14, fontweight='bold')
            ax4.set_xlabel('CF Rating')
            ax4.set_ylabel('Number of Problems')
        else:
            ax4.text(0.5, 0.5, 'No CF Rating data available', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Codeforces Rating Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/problem_characteristics_{self.timestamp}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_tags_analysis(self):
        """Create visualization for tags analysis."""
        print("Creating tags analysis visualization...")
        
        # Collect all tags
        all_tags = []
        for tags_list in self.df['cf_tags_parsed']:
            all_tags.extend(tags_list)
        
        if not all_tags:
            print("No tags found in dataset")
            return
            
        # Count tag frequencies
        tag_counter = Counter(all_tags)
        top_tags = dict(tag_counter.most_common(15))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 1. Top tags horizontal bar chart
        tags_df = pd.DataFrame(list(top_tags.items()), columns=['Tag', 'Count'])
        sns.barplot(data=tags_df, x='Count', y='Tag', ax=ax1, palette='viridis')
        ax1.set_title('Top 15 Most Common Tags', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Number of Problems')
        
        # Add count labels
        for i, count in enumerate(tags_df['Count']):
            ax1.text(count + 0.5, i, str(count), va='center')
        
        # 2. Tags per difficulty level
        tag_diff_data = []
        for _, row in self.df.iterrows():
            difficulty = row['difficulty_label']
            num_tags = row['num_tags']
            tag_diff_data.append({'Difficulty': difficulty, 'Num_Tags': num_tags})
        
        tag_diff_df = pd.DataFrame(tag_diff_data)
        sns.boxplot(data=tag_diff_df, x='Difficulty', y='Num_Tags', ax=ax2)
        ax2.set_title('Number of Tags by Difficulty Level', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Tags per Problem')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/tags_analysis_{self.timestamp}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_test_cases_analysis(self):
        """Create visualization for test cases analysis."""
        print("Creating test cases analysis...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Public tests distribution
        public_counts = self.df['public_tests_count']
        ax1.hist(public_counts, bins=20, alpha=0.7, color='lightblue', edgecolor='black')
        ax1.set_title('Distribution of Public Test Cases', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Number of Public Test Cases')
        ax1.set_ylabel('Number of Problems')
        ax1.axvline(public_counts.mean(), color='red', linestyle='--', 
                   label=f'Mean: {public_counts.mean():.1f}')
        ax1.legend()
        
        # 2. Test cases by difficulty
        test_data = []
        for _, row in self.df.iterrows():
            test_data.append({
                'Difficulty': row['difficulty_label'],
                'Public': row['public_tests_count'],
                'Private': row['private_tests_count'],
                'Generated': row['generated_tests_count']
            })
        
        test_df = pd.DataFrame(test_data)
        test_df_melted = pd.melt(test_df, 
                                id_vars=['Difficulty'], 
                                value_vars=['Public', 'Private', 'Generated'],
                                var_name='Test_Type', value_name='Count')
        
        sns.boxplot(data=test_df_melted, x='Difficulty', y='Count', hue='Test_Type', ax=ax2)
        ax2.set_title('Test Cases Distribution by Difficulty', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Test Cases')
        
        # 3. Time limits distribution
        time_limits = self.df['time_limit'].dropna()
        if len(time_limits) > 0:
            ax3.hist(time_limits, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
            ax3.set_title('Time Limits Distribution', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Time Limit (seconds)')
            ax3.set_ylabel('Number of Problems')
        else:
            ax3.text(0.5, 0.5, 'No time limit data available', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Time Limits Distribution', fontsize=14, fontweight='bold')
        
        # 4. Memory limits distribution
        memory_limits = self.df['memory_limit_bytes'].dropna()
        if len(memory_limits) > 0:
            # Convert bytes to MB for readability
            memory_limits_mb = memory_limits / (1024 * 1024)
            ax4.hist(memory_limits_mb, bins=20, alpha=0.7, color='orange', edgecolor='black')
            ax4.set_title('Memory Limits Distribution', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Memory Limit (MB)')
            ax4.set_ylabel('Number of Problems')
        else:
            ax4.text(0.5, 0.5, 'No memory limit data available', 
                    ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Memory Limits Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/test_cases_analysis_{self.timestamp}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        print("Generating summary report...")
        
        summary = {
            'dataset_info': {
                'total_problems': len(self.df),
                'total_columns': len(self.df.columns),
                'difficulty_distribution': self.df['difficulty_label'].value_counts().to_dict(),
                'timestamp': self.timestamp
            },
            'problem_characteristics': {
                'avg_description_length': float(self.df['description_length'].mean()),
                'median_description_length': float(self.df['description_length'].median()),
                'min_description_length': int(self.df['description_length'].min()),
                'max_description_length': int(self.df['description_length'].max()),
                'avg_tags_per_problem': float(self.df['num_tags'].mean()),
                'max_tags_per_problem': int(self.df['num_tags'].max())
            },
            'test_cases_stats': {
                'avg_public_tests': float(self.df['public_tests_count'].mean()),
                'avg_private_tests': float(self.df['private_tests_count'].mean()),
                'avg_generated_tests': float(self.df['generated_tests_count'].mean())
            },
            'missing_data': {
                column: int(self.df[column].isna().sum()) 
                for column in self.df.columns 
                if self.df[column].isna().sum() > 0
            }
        }
        
        # Save summary to JSON
        with open(f'{self.output_dir}/dataset_summary_{self.timestamp}.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("DATASET SUMMARY REPORT")
        print("="*60)
        print(f"Total Problems: {summary['dataset_info']['total_problems']}")
        print(f"Total Columns: {summary['dataset_info']['total_columns']}")
        print(f"\nDifficulty Distribution:")
        for diff, count in summary['dataset_info']['difficulty_distribution'].items():
            percentage = (count / summary['dataset_info']['total_problems']) * 100
            print(f"  {diff}: {count} ({percentage:.1f}%)")
        
        print(f"\nProblem Characteristics:")
        print(f"  Average Description Length: {summary['problem_characteristics']['avg_description_length']:.0f} chars")
        print(f"  Description Length Range: {summary['problem_characteristics']['min_description_length']} - {summary['problem_characteristics']['max_description_length']} chars")
        print(f"  Average Tags per Problem: {summary['problem_characteristics']['avg_tags_per_problem']:.1f}")
        
        print(f"\nTest Cases Statistics:")
        print(f"  Average Public Tests: {summary['test_cases_stats']['avg_public_tests']:.1f}")
        print(f"  Average Private Tests: {summary['test_cases_stats']['avg_private_tests']:.1f}")
        print(f"  Average Generated Tests: {summary['test_cases_stats']['avg_generated_tests']:.1f}")
        
        if summary['missing_data']:
            print(f"\nMissing Data:")
            for column, count in summary['missing_data'].items():
                print(f"  {column}: {count} missing values")
        else:
            print(f"\nNo missing data detected!")
        
        return summary
        
    def run_all_visualizations(self):
        """Run all visualization methods."""
        print("Starting comprehensive dataset visualization...")
        print("="*60)
        
        self.load_data()
        
        self.create_difficulty_distribution_viz()
        self.create_problem_characteristics_viz()
        self.create_tags_analysis()
        self.create_test_cases_analysis()
        
        summary = self.generate_summary_report()
        
        print(f"\n" + "="*60)
        print(f"VISUALIZATION COMPLETE!")
        print(f"All visualizations saved to: {self.output_dir}/")
        print(f"Summary report saved as: dataset_summary_{self.timestamp}.json")
        print("="*60)
        
        return summary


def main():
    """Main function to run the visualizer."""
    visualizer = CodeContestsVisualizer()
    
    try:
        summary = visualizer.run_all_visualizations()
        
        print("\nVisualization completed successfully!")
        print(f"Check the '{visualizer.output_dir}' directory for all generated plots and reports.")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure the code_contests.csv file exists in the datasets directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your data and try again.")


if __name__ == "__main__":
    main()