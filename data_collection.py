import scraper as sc
import pandas as pd

df = sc.get_jobs('data science', 35, False, 3)
df.to_csv('glassdoor_jobs.csv', index=False)
