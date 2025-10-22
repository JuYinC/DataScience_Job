# Data Science Jobs Salary Estimator: Overview

- Created a tool that estimates data science salaries (MAE ~ $27.6K) with the info of the job
- Scraped over 1000 job descriptions from glassdoor using python and selenium
- Engineered features from the text of each job description to quantify the value companies put on python, excel, sql, aws, spark, tableau, and machine learning.
- Optimized Linear, Lasso, Ridge Regression, Gradient Boosting, Decision Tree, and Random Forest Regressors using GridSearchCV to reach the best model.
- Built a client-facing web application with Flask featuring an interactive UI for salary predictions

## Code and Resources Used

Python Version: 3.12 (also compatible with 3.9+)

Packages: pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle

Scikit-learn Version: 1.7.2

For Web Framework Requirements: Use virtual environment (venv) and install packages as needed

[Project Reference](https://github.com/PlayingNumbers/ds_salary_proj)

[Scraper Github](https://github.com/arapfaik/scraping-glassdoor-selenium)

[EDA](https://www.kaggle.com/code/davidbroberts/data-science-job-posting-on-glassdoor-eda)

[Flask Productionization](https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2)

## Web Scraping

Scrape 1080 job postings from glassdoor.com. With each job, we got the following:

- Job title
- Salary Estimate
- Job Description
- Rating
- Company
- Location
- Company Size
- Company Founded Date
- Type of Ownership
- Industry
- Sector
- Revenue

## Data Cleaning

After scraping the data, It's time to clean it up so that it was usable for our model. I made the following changes and created the following variables:

- Removed duplicates and rows without salary
- Parsed numeric data out of salary
- Made columns for employer provided salary and hourly wages
- Transformed founded date into age of company
- Replaced -1 to Unknown in certain columns
  - Size
  - Type of ownership
  - Industry
  - Sector
  - Revenue
- Parsed rating out of company text
- Made a new column for company state
- Column for simplified job title and Seniority
- Made columns for if different skills were listed in the job description:
  - Python
  - Excel
  - SQL
  - Tableau
  - AWS
  - Spark
  - Machine Learning
- Column for description length

## EDA

I analyzed the data to uncover salary with differnt variables. Belows are a few highlights.

![Heat map of correlation](images/corr.png "Heat map of correlation")
![Salary by Job Title and Experience](images/salary_jobs.png "Salary by Job Title and Experience")
![Salary by State](images/salary_state.png "Salary by State")
![Word Cloud](./images/wordcloud.png "Word Cloud")

## Model Building

Transformed the categorical variables into dummy variables, and split the data into train and tests sets with a test size of 20%.

Tried different models and evaluated them using Mean Absolute Error(MAE) and Root Mean Square Error(RMSE)

### Modols Evaluated

- Linear Regression
- Lasso Regression
- Ridge Regression
- Decision Tree
- Random Forest
- Gradient Boosting

## Model Performance

Among all the models, Random Forest model and Gradient Boosting have better performance, and Random Forest is slightly better.

- **Random Forest** MAE: 27.59 RMSE: 54.03

- **Gradient Boosting** MAE: 29.77 RMSE: 56.91

## Productionization

Built a Flask web application with both API endpoints and an interactive web interface:

### Web UI
- Modern, responsive web interface at `http://127.0.0.1:5000/`
- Interactive form for inputting job details (company rating, age, skills, etc.)
- Real-time salary predictions displayed in the browser
- Beautiful gradient design with user-friendly experience

### API Endpoints
- `/predict` - POST endpoint for raw 165-feature array predictions
- `/predict_simple` - POST endpoint for simplified form data (automatically encodes features)

### Running the Application

1. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install flask numpy pandas scikit-learn
   ```

3. **Retrain the model (optional):**
   ```bash
   python retrain_model.py
   ```

4. **Run the Flask app:**
   ```bash
   cd FlaskAPI
   python app.py
   ```

5. **Access the web interface:**
   Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
DataScience_Job/
├── FlaskAPI/
│   ├── app.py                 # Flask application with web UI and API
│   ├── models/
│   │   └── model_file.p      # Trained Random Forest model
│   ├── templates/
│   │   └── index.html        # Web interface
│   ├── data_input.py         # Sample input data
│   └── request.py            # API testing script
├── retrain_model.py          # Script to retrain model with current sklearn version
├── data_cleaning.ipynb       # Data cleaning pipeline
├── eda.ipynb                 # Exploratory data analysis
├── model_building.ipynb      # Model training and evaluation
├── data_cleaned.csv          # Cleaned dataset
└── README.md
```

## Conclusion

Both the Random Forest and Gradient Boosting models demonstrated satisfactory performance in predicting average salaries. The Random Forest model was chosen for deployment due to slightly better performance. The web application provides an accessible interface for users to get salary estimates based on job characteristics, making the model insights available to non-technical users.
