import scraper as sc
import pandas as pd

#Collect job with different job title
jobs = ['Data Scientist', 'Data Analyst', 'Data Engineer',
        'Business Analyst', 'Machine Learning Engineer', 'Data Architect']

for job in jobs:
    df = sc.get_jobs(job, 180, False, 5)
    df.to_csv(f'glassdoor_{job.replace(" ", "_")}.csv', index=False)
