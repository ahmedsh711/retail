# 🧼 Retail Sales Data Cleaning & Analysis Dashboard

This project is a **Streamlit web app** designed to explore, clean, and visualize retail store sales data. The dataset contains raw sales data with intentional inconsistencies, making it ideal for demonstrating real-world data cleaning and exploratory data analysis (EDA) workflows.

## 📦 Dataset

- **Name:** Retail Store Sales (Dirty) – for Data Cleaning  
- **Source:** [Kaggle Dataset by Ahmed Mohamed](https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning)
- **Description:** This dataset contains sales data with dirty or inconsistent entries in columns like dates, customer names, totals, and payment methods.

---

## 🔍 Features of the App

- 🧹 Data Cleaning:
  - Handle missing values
  - Standardize columns (e.g., dates, categories)
  - Remove or correct inconsistent formatting
- 📊 Exploratory Data Analysis:
  - Summary statistics
  - Interactive charts (sales over time, top products, etc.)
- 📁 Data Filtering:
  - Filter by customer, product, region, or date

---

## 🗂️ Project Structure

```
retail-streamlit-app/
├── app.py                 # Main Streamlit app script
├── requirements.txt       # Required packages
├── README.md              # Project documentation
├── .gitignore             # Git ignore settings
├── data/
│   └── retail_sales_dirty.csv
├── utils/
│   └── cleaner.py         # (Optional) Functions for cleaning
```

---

## ▶️ How to Run Locally

1. **Clone the Repository**
```bash
git clone https://github.com/ahmedsh711/retail
cd retail-streamlit-app
```

2. **Install the Requirements**
```bash
pip install -r requirements.txt
```

3. **Run the App**
```bash
streamlit run app.py
```

---

## 🌐 Live App

You can view the live hosted app here:  
**🔗 (https://retail.streamlit.app/)**

> Replace the link with your actual Streamlit Cloud deployment URL.

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Matplotlib](https://matplotlib.org/)
- [Scikit-learn](https://scikit-learn.org/) (optional for modeling)

---

## 📌 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

*Created with ❤️ by [Ahmed Al-Shobaki](https://github.com/ahmedsh711)*
"# retail" 
