# Chartify – Interactive Data Visualization and Analysis Platform

Chartify is a Python-based interactive data visualization and analysis platform developed using Streamlit. It allows users to upload CSV and Excel datasets, explore the data, generate statistical summaries, create interactive visualizations, and obtain AI-based insights.

## Features

- Upload CSV and Excel datasets
- Preview uploaded data
- View dataset overview and basic information
- Identify numerical and categorical columns
- Apply numerical filters
- Check missing values
- Check duplicate rows
- Generate automatic data insights
- Generate summary statistics
- Create interactive visualizations
- Generate AI-based insights using Ollama

## Technologies Used

- **Python** – Application development
- **Streamlit** – Web application interface
- **Pandas** – Data processing and analysis
- **Plotly Express** – Interactive data visualization
- **Requests** – Communication with the local Ollama API
- **Ollama** – Local AI model execution
- **Llama 3.2:1B** – Local language model

## How It Works

1. Upload a CSV or Excel dataset.
2. Chartify reads the dataset using Pandas.
3. The application displays a preview and dataset overview.
4. Numerical and categorical columns are identified.
5. Users can apply numerical filters.
6. The application generates automatic insights and statistical summaries.
7. Users can create interactive charts such as bar charts, line charts, pie charts, scatter plots, and histograms.
8. Ollama generates additional AI-based insights from the dataset summary.

## AI Integration

Chartify uses Ollama to run the Llama 3.2:1B language model locally.

The application communicates with Ollama through its local API:

`http://localhost:11434/api/generate`

Running the model locally reduces dependency on external AI APIs and allows the AI insight feature to operate on the local system.

## Project Structure

```text
Chartify-Data-Visualization/
│
├── app_WITHOUT_AI.py
├── README.md
└── requirements.txt
