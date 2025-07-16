import re
import json
from datetime import datetime
from collections import Counter

class SimpleAIEngine:
    def __init__(self):
        # Skills database for matching
        self.skills_database = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask'],
            'databases': ['sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins'],
            'ai_ml': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'],
            'data_analysis': ['data analysis', 'statistics', 'r', 'matlab', 'spark', 'hadoop', 'tableau', 'powerbi'],
            'tools': ['git', 'excel', 'word', 'powerpoint', 'jira', 'confluence']
        }
        
        # Salary ranges by job type and location
        self.salary_ranges = {
            'Full-time': {
                'Bangalore': {'min': 600000, 'max': 2000000},
                'Mumbai': {'min': 700000, 'max': 2200000},
                'Delhi': {'min': 650000, 'max': 2100000},
                'Remote': {'min': 500000, 'max': 1800000},
                'default': {'min': 500000, 'max': 1500000}
            },
            'Part-time': {
                'default': {'min': 200000, 'max': 800000}
            },
            'Contract': {
                'default': {'min': 400000, 'max': 1200000}
            },
            'Internship': {
                'default': {'min': 100000, 'max': 400000}
            }
        }
        
        # Sentiment keywords
        self.positive_words = [
            'exciting', 'innovative', 'dynamic', 'collaborative', 'flexible', 'growth',
            'opportunity', 'challenging', 'rewarding', 'creative', 'fast-paced', 'friendly'
        ]
        
        self.negative_words = [
            'stressful', 'demanding', 'rigid', 'boring', 'repetitive', 'isolated',
            'overwhelming', 'toxic', 'unorganized', 'unclear'
        ]
    
    def extract_skills_from_text(self, text):
        """Extract skills from text using keyword matching"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        # Check each skill category
        for category, skills in self.skills_database.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        return found_skills
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis using keyword counting"""
        if not text:
            return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'neutral'}
        
        text_lower = text.lower()
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'neutral'}
        
        # Calculate polarity (-1 to 1)
        polarity = (positive_count - negative_count) / max(total_words, 1)
        polarity = max(-1, min(1, polarity))  # Clamp between -1 and 1
        
        # Calculate subjectivity (0 to 1)
        subjectivity = (positive_count + negative_count) / max(total_words, 1)
        subjectivity = min(1, subjectivity)
        
        # Determine sentiment
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'sentiment': sentiment
        }
    
    def predict_salary(self, job_features):
        """Predict salary based on job features using simple rules"""
        job_type = job_features.get('job_type', 'Full-time')
        location = job_features.get('location', 'Remote')
        description_length = job_features.get('description_length', 0)
        requirements_length = job_features.get('requirements_length', 0)
        skills_count = job_features.get('skills_count', 0)
        
        # Get base salary range
        if job_type in self.salary_ranges:
            if location in self.salary_ranges[job_type]:
                base_range = self.salary_ranges[job_type][location]
            else:
                base_range = self.salary_ranges[job_type]['default']
        else:
            base_range = self.salary_ranges['Full-time']['default']
        
        # Calculate complexity multiplier
        complexity_score = 0
        if description_length > 500:
            complexity_score += 0.1
        if requirements_length > 200:
            complexity_score += 0.1
        if skills_count > 5:
            complexity_score += 0.2
        
        # Calculate predicted salary
        base_salary = (base_range['min'] + base_range['max']) / 2
        predicted_salary = base_salary * (1 + complexity_score)
        
        return int(predicted_salary)
    
    def get_job_recommendations(self, user_skills, user_preferences, all_jobs, top_n=5):
        """Get personalized job recommendations"""
        if not all_jobs:
            return []
        
        # Parse user skills
        user_skills_list = [skill.strip().lower() for skill in user_skills.split(',')] if user_skills else []
        user_preferences_lower = user_preferences.lower() if user_preferences else ""
        
        job_scores = []
        
        for job in all_jobs:
            score = 0
            
            # Skills matching (40% weight)
            job_skills = job.get('skills', '').lower().split(',') if job.get('skills') else []
            job_skills = [skill.strip() for skill in job_skills]
            
            if job_skills and user_skills_list:
                common_skills = set(job_skills) & set(user_skills_list)
                skills_match = len(common_skills) / max(len(job_skills), len(user_skills_list))
                score += skills_match * 0.4
            
            # Location preference (20% weight)
            if user_preferences_lower and job.get('location'):
                if any(loc in job['location'].lower() for loc in user_preferences_lower.split()):
                    score += 0.2
            
            # Job type preference (20% weight)
            if user_preferences_lower and job.get('job_type'):
                if job['job_type'].lower() in user_preferences_lower:
                    score += 0.2
            
            # Salary attractiveness (20% weight)
            if job.get('salary_min'):
                salary_score = min(job['salary_min'] / 1000000, 1.0)
                score += salary_score * 0.2
            
            job_scores.append({
                'job': job,
                'score': score,
                'skills_match': len(set(job_skills) & set(user_skills_list)) if job_skills and user_skills_list else 0
            })
        
        # Sort by score and return top recommendations
        job_scores.sort(key=lambda x: x['score'], reverse=True)
        return job_scores[:top_n]
    
    def analyze_job_market_trends(self, jobs_data):
        """Analyze job market trends"""
        if not jobs_data:
            return {}
        
        trends = {
            'total_jobs': len(jobs_data),
            'avg_salary': 0,
            'popular_skills': {},
            'job_type_distribution': {},
            'location_distribution': {},
            'salary_ranges': {
                'entry_level': 0,
                'mid_level': 0,
                'senior_level': 0
            }
        }
        
        # Calculate average salary
        salaries = []
        for job in jobs_data:
            if job.get('salary_min') and job.get('salary_max'):
                salaries.append((job['salary_min'] + job['salary_max']) / 2)
        
        if salaries:
            trends['avg_salary'] = int(sum(salaries) / len(salaries))
        
        # Popular skills
        all_skills = []
        for job in jobs_data:
            if job.get('skills'):
                skills = [skill.strip().lower() for skill in job['skills'].split(',')]
                all_skills.extend(skills)
        
        if all_skills:
            skill_counts = Counter(all_skills)
            trends['popular_skills'] = dict(skill_counts.most_common(10))
        
        # Job type distribution
        job_types = [job.get('job_type', 'Unknown') for job in jobs_data]
        job_type_counts = Counter(job_types)
        trends['job_type_distribution'] = dict(job_type_counts)
        
        # Location distribution
        locations = [job.get('location', 'Unknown') for job in jobs_data]
        location_counts = Counter(locations)
        trends['location_distribution'] = dict(location_counts.most_common(10))
        
        # Salary range analysis
        for job in jobs_data:
            if job.get('salary_min'):
                salary = job['salary_min']
                if salary < 500000:
                    trends['salary_ranges']['entry_level'] += 1
                elif salary < 1500000:
                    trends['salary_ranges']['mid_level'] += 1
                else:
                    trends['salary_ranges']['senior_level'] += 1
        
        return trends
    
    def generate_job_insights(self, job_data):
        """Generate insights for a specific job posting"""
        insights = {
            'sentiment': self.analyze_sentiment(job_data.get('description', '')),
            'skills_required': self.extract_skills_from_text(job_data.get('description', '') + ' ' + job_data.get('requirements', '')),
            'complexity_score': 0,
            'market_demand': 'medium'
        }
        
        # Calculate complexity score
        description_length = len(job_data.get('description', ''))
        requirements_length = len(job_data.get('requirements', ''))
        skills_count = len(job_data.get('skills', '').split(',')) if job_data.get('skills') else 0
        
        complexity_score = (description_length * 0.3 + requirements_length * 0.4 + skills_count * 0.3) / 1000
        insights['complexity_score'] = min(complexity_score, 1.0)
        
        # Determine market demand based on salary
        if job_data.get('salary_min'):
            if job_data['salary_min'] > 1000000:
                insights['market_demand'] = 'high'
            elif job_data['salary_min'] < 500000:
                insights['market_demand'] = 'low'
        
        return insights

# Initialize the simplified AI engine
ai_ml_engine = SimpleAIEngine() 