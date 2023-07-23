import scraper as sc
import pandas as pd

df = sc.get_jobs('data scientist', 1000, False, 15)
df.to_csv('glassdoor_jobs.csv', index=False)
