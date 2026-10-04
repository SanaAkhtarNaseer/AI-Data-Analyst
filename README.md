## 🚀 Live Demo

Try the deployed application here:

**[Launch Analytica Data](https://analytica-data.streamlit.app/)**

# 📊 AI Data Analyst

A portfolio-ready Streamlit application that transforms CSV and Excel datasets into an interactive data analytics dashboard with automated data cleaning, visualization, insights, and export capabilities.

## Features

- Upload CSV and Excel datasets
- Automatically inspect dataset structure
- Detect missing values and duplicate records
- Clean missing values using user-selected strategies
- Remove duplicate records
- Standardize column names
- Automatically detect and parse date columns
- Display dataset summary and descriptive statistics
- Explore data using interactive Plotly visualizations
- Analyze numeric distributions
- Compare numeric metrics across categorical groups
- Choose aggregation methods:
  - Sum
  - Average
  - Median
  - Minimum
  - Maximum
  - Count
- Generate numeric correlation matrices
- Automatically generate analytical insights
- Identify differences between categorical groups
- Detect potential numeric outliers using the IQR method
- Export cleaned datasets as CSV or Excel

## Data Quality & Cleaning

The application provides an interactive data-cleaning workflow.

Users can:

- Review missing values
- Identify duplicate rows
- Select a missing-value treatment strategy
- Remove rows containing missing values
- Fill numeric missing values using the median
- Fill categorical missing values using the mode
- Remove duplicate records
- Continue analysis using the cleaned dataset

This allows the original and processed data to be compared before further analysis.

## Interactive Visual Explorer

The Visual Explorer allows users to dynamically select:

- A numeric metric
- A categorical grouping variable
- An aggregation method

The application automatically generates interactive charts based on these selections.

Additional visualizations include:

- Numeric distributions
- Group comparisons
- Correlation heatmaps

## 💡 Automated Insights

The application automatically analyzes the uploaded dataset and generates deterministic analytical insights.

Depending on the available columns, insights may include:

- Numeric averages
- Highest-performing categorical groups
- Differences between highest and lowest groups
- Strong numeric correlations
- Revenue and profit summaries when relevant fields exist
- Potential outliers detected using the IQR method

The insight engine is designed to work across different types of datasets rather than relying on one predefined business dataset.

> The generated insights are deterministic analytics rather than LLM-generated claims. Important conclusions should always be validated against the original dataset and domain context.

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenPyXL
- xlrd

## Supported File Formats

- CSV (`.csv`)
- Excel (`.xlsx`)
- Excel (`.xls`)

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/SanaAkhtarNaseer/AI-Data-Analyst.git
cd AI-Data-Analyst
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Streamlit application

```bash
streamlit run app.py
```

If the `streamlit` command is not recognized, use:

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## 📦 Requirements

The project uses the following main dependencies:

```text
streamlit>=1.38
pandas>=2.2
numpy>=1.26
plotly>=5.24
openpyxl>=3.1
xlrd>=2.0
```

## 🔄 Application Workflow

```text
Upload Dataset
      ↓
Data Quality Inspection
      ↓
Data Cleaning
      ↓
Dataset Overview
      ↓
Interactive Visual Analysis
      ↓
Automated Insights
      ↓
Export Cleaned Dataset
```

## 🎯 Project Purpose

This project demonstrates practical data science and analytics skills, including:

- Data preprocessing
- Missing-value handling
- Exploratory Data Analysis (EDA)
- Statistical summaries
- Automated analytical reasoning
- Interactive data visualization
- Dashboard development
- Data export workflows

The application is designed as a portfolio project demonstrating how Python-based analytics can turn raw tabular datasets into useful, interactive analytical outputs.

## 💼 Portfolio Description

**AI Data Analyst — Python, Pandas, Plotly & Streamlit**

Developed an interactive data analytics application that automates common data-analysis workflows. Users can upload CSV or Excel datasets, assess data quality, clean missing values and duplicates, explore interactive visualizations, compare categorical groups using multiple aggregation methods, analyze correlations, generate automated data-driven insights, detect potential outliers, and export processed datasets.

**Technologies:** Python, Pandas, NumPy, Plotly, Streamlit, OpenPyXL, xlrd.

## 🔮 Future Development

Potential Version 3 features include:

- Natural-language **Ask Your Data**
- LLM-powered explanations
- Automated PDF analytical reports
- Smarter KPI detection
- Configurable data-cleaning rules
- Forecasting
- Anomaly detection
- Advanced statistical analysis

## ⚠️ Responsible Use

Automated insights are intended to assist exploratory analysis.

Important academic, financial, business, medical, or other high-impact decisions should not be made solely from automatically generated insights. Results should be validated against the original dataset and appropriate domain knowledge.

## 📄 Version

**Version 2.0 — Portfolio Release**

Current Version 2 includes the complete data upload, quality inspection, cleaning, visualization, automated insight, and export workflow.
