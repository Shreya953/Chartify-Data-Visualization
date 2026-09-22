import streamlit as st
import pandas as pd
import plotly.express as px
import requests


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Chartify",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("📊 Chartify")

st.sidebar.write(
    "Interactive Data Visualization Platform"
)

st.sidebar.divider()

st.sidebar.subheader("🎛️ Dashboard Controls")

st.sidebar.info(
    "Upload a dataset and use the controls to explore your data."
)


# -----------------------------------
# WEBSITE HEADER
# -----------------------------------

st.title("📊 Chartify")

st.caption(
    "Interactive Data Visualization & Analysis Platform"
)

st.write(
    "Upload your dataset, explore key statistics, discover automatic "
    "insights, and create interactive visualizations — all in one place."
)

st.divider()


# -----------------------------------
# DATASET UPLOAD
# -----------------------------------

st.subheader("📁 Upload your Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)


# -----------------------------------
# PROCESS DATASET
# -----------------------------------

if uploaded_file is not None:

    # -----------------------------------
    # READ DATASET
    # -----------------------------------

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:

        st.error(
            f"Error while reading the dataset: {e}"
        )

        st.stop()


    # -----------------------------------
    # SUCCESS MESSAGE
    # -----------------------------------

    st.success("Dataset uploaded successfully! 🎉")


    # -----------------------------------
    # COLUMN CLASSIFICATION
    # -----------------------------------

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()


    # -----------------------------------
    # INTERACTIVE DATA FILTER
    # -----------------------------------

    st.sidebar.subheader("🔍 Data Filter")

    filtered_df = df.copy()

    if len(numerical_columns) > 0:

        filter_column = st.sidebar.selectbox(
            "Choose a numerical column to filter",
            numerical_columns
        )

        column_data = df[filter_column].dropna()

        if len(column_data) > 0:

            min_value = float(column_data.min())
            max_value = float(column_data.max())

            if min_value < max_value:

                selected_range = st.sidebar.slider(
                    f"Select range for {filter_column}",
                    min_value=min_value,
                    max_value=max_value,
                    value=(min_value, max_value)
                )

                filtered_df = df[
                    (df[filter_column] >= selected_range[0]) &
                    (df[filter_column] <= selected_range[1])
                ]

            else:

                st.sidebar.info(
                    f"{filter_column} contains only one value."
                )


    # -----------------------------------
    # DATASET PREVIEW
    # -----------------------------------

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


    # -----------------------------------
    # DATASET OVERVIEW
    # -----------------------------------

    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📄 Rows",
            filtered_df.shape[0]
        )

    with col2:

        st.metric(
            "📊 Columns",
            filtered_df.shape[1]
        )

    with col3:

        st.metric(
            "⚠️ Missing Values",
            filtered_df.isnull().sum().sum()
        )

    st.divider()


    # -----------------------------------
    # AVAILABLE COLUMNS
    # -----------------------------------

    st.subheader("📋 Available Columns")

    st.write(
        list(filtered_df.columns)
    )


    # -----------------------------------
    # COLUMN CLASSIFICATION DISPLAY
    # -----------------------------------

    st.subheader("🔍 Column Classification")

    col1, col2 = st.columns(2)

    with col1:

        st.write("🔢 Numerical Columns")
        st.write(numerical_columns)

    with col2:

        st.write("📝 Categorical/Text Columns")
        st.write(categorical_columns)


    # -----------------------------------
    # AUTOMATIC DATA INSIGHTS
    # -----------------------------------

    st.subheader("🤖 Automatic Data Insights")

    st.info(
        f"📊 This dataset contains "
        f"{filtered_df.shape[0]} rows and "
        f"{filtered_df.shape[1]} columns."
    )

    st.info(
        f"🔢 The dataset contains "
        f"{len(numerical_columns)} numerical columns "
        f"and {len(categorical_columns)} "
        f"categorical/text columns."
    )


    # -----------------------------------
    # MISSING VALUES
    # -----------------------------------

    missing_values = filtered_df.isnull().sum().sum()

    if missing_values == 0:

        st.success(
            "✅ Great! No missing values were found in the dataset."
        )

    else:

        st.warning(
            f"⚠️ The dataset contains "
            f"{missing_values} missing values."
        )


    # -----------------------------------
    # MISSING VALUES INSIGHT
    # -----------------------------------

    column_missing = filtered_df.isnull().sum()

    highest_missing_column = column_missing.idxmax()
    highest_missing_count = column_missing.max()

    if highest_missing_count > 0:

        st.warning(
            f"⚠️ **{highest_missing_column}** has the highest number "
            f"of missing values: **{highest_missing_count}**."
        )

    else:

        st.success(
            "✅ No individual column contains missing values."
        )


    # -----------------------------------
    # DUPLICATE ROWS
    # -----------------------------------

    duplicate_rows = filtered_df.duplicated().sum()

    if duplicate_rows == 0:

        st.success(
            "✅ No duplicate rows were found in the dataset."
        )

    else:

        st.warning(
            f"⚠️ The dataset contains "
            f"{duplicate_rows} duplicate rows."
        )


    # -----------------------------------
    # SMART NUMERICAL INSIGHT
    # -----------------------------------

    if len(numerical_columns) > 0:

        column_averages = (
            filtered_df[numerical_columns]
            .mean()
            .dropna()
        )

        if len(column_averages) > 0:

            highest_average_column = (
                column_averages.idxmax()
            )

            highest_average_value = (
                column_averages.max()
            )

            st.info(
                f"🏆 **{highest_average_column}** has the highest "
                f"average value of "
                f"**{highest_average_value:,.2f}** "
                f"among the numerical columns."
            )


    # -----------------------------------
    # AI-POWERED DATA INSIGHTS - OLLAMA
    # -----------------------------------

    st.subheader("🤖 AI-Powered Data Insights")

    if "ai_insights" not in st.session_state:
        st.session_state.ai_insights = None

    if st.button("✨ Generate AI Insights"):

        with st.spinner("🤖 AI is analyzing your dataset locally..."):

            try:

                data_summary = f"""
Dataset Shape: {filtered_df.shape}

Column Names:
{list(filtered_df.columns)}

Numerical Summary:
{filtered_df[numerical_columns].describe().to_string() if numerical_columns else "No numerical columns available"}

Categorical Columns:
{categorical_columns}

Missing Values:
{filtered_df.isnull().sum().to_string()}
"""

                prompt = f"""
You are a helpful data analyst.

Analyze the following dataset summary and provide clear,
useful insights for a student-level data analytics project.

Give:

1. Overall dataset observations
2. Important numerical insights
3. Interesting patterns or trends
4. Data quality observations
5. Useful recommendations

Keep the response concise, easy to understand, and professional.

Dataset Summary:
{data_summary}
"""

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3.2:1b",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                st.session_state.ai_insights = result["response"]

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Ollama is not running. Please open Ollama "
                    "and try again."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "❌ The local AI is taking too long to respond. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    f"❌ Local AI analysis could not be completed: {e}"
                )


    # Display saved AI insights
    if st.session_state.ai_insights:

        st.success("✅ AI Analysis Completed Locally!")

        st.markdown("### 🤖 AI Insights")

        st.write(st.session_state.ai_insights)


    # -----------------------------------
    # NUMERICAL SUMMARY STATISTICS
    # -----------------------------------

    st.subheader("📊 Numerical Summary Statistics")

    if len(numerical_columns) > 0:

        summary_df = (
            filtered_df[numerical_columns]
            .describe()
            .T
        )

        summary_df["Median"] = (
            filtered_df[numerical_columns]
            .median()
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

    else:

        st.info(
            "No numerical columns are available "
            "for summary statistics."
        )


    # -----------------------------------
    # DATA VISUALIZATION
    # -----------------------------------

    st.subheader("📊 Data Visualization")

    chart_type = st.selectbox(
        "Choose a Visualization",
        [
            "Bar Chart",
            "Line Chart",
            "Pie Chart",
            "Scatter Plot",
            "Histogram"
        ]
    )


    # -----------------------------------
    # BAR CHART
    # -----------------------------------

    if chart_type == "Bar Chart":

        if len(numerical_columns) > 0:

            y_axis = st.selectbox(
                "Choose Numerical Column",
                numerical_columns,
                key="bar_y"
            )

            chart_data = (
                filtered_df[[y_axis]]
                .head(20)
                .copy()
            )

            chart_data["Row"] = (
                range(1, len(chart_data) + 1)
            )

            fig = px.bar(
                chart_data,
                x="Row",
                y=y_axis,
                title=f"{y_axis} - First 20 Records"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No numerical columns are available "
                "for the Bar Chart."
            )


    # -----------------------------------
    # LINE CHART
    # -----------------------------------

    elif chart_type == "Line Chart":

        if len(numerical_columns) > 0:

            y_axis = st.selectbox(
                "Choose Numerical Column",
                numerical_columns,
                key="line_y"
            )

            chart_data = (
                filtered_df[[y_axis]]
                .copy()
            )

            chart_data["Row"] = (
                range(1, len(chart_data) + 1)
            )

            fig = px.line(
                chart_data,
                x="Row",
                y=y_axis,
                title=f"{y_axis} Trend"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No numerical columns are available "
                "for the Line Chart."
            )


    # -----------------------------------
    # PIE CHART
    # -----------------------------------

    elif chart_type == "Pie Chart":

        pie_columns = [
            column
            for column in numerical_columns
            if "id" not in column.lower()
        ]

        if len(pie_columns) > 0:

            selected_metrics = st.multiselect(
                "Choose Numerical Metrics",
                pie_columns,
                default=pie_columns[:3],
                key="pie_metrics"
            )

            if len(selected_metrics) > 0:

                metric_values = []

                for column in selected_metrics:

                    metric_values.append(
                        filtered_df[column].sum()
                    )

                pie_data = pd.DataFrame({
                    "Metric": selected_metrics,
                    "Value": metric_values
                })

                fig = px.pie(
                    pie_data,
                    names="Metric",
                    values="Value",
                    title="Distribution of Selected Metrics",
                    hole=0.25
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "Please select at least one metric."
                )

        else:

            st.warning(
                "No suitable numerical columns are available."
            )


    # -----------------------------------
    # SCATTER PLOT
    # -----------------------------------

    elif chart_type == "Scatter Plot":

        if len(numerical_columns) >= 2:

            x_axis = st.selectbox(
                "Choose X-axis",
                numerical_columns,
                key="scatter_x"
            )

            y_axis = st.selectbox(
                "Choose Y-axis",
                numerical_columns,
                index=1,
                key="scatter_y"
            )

            fig = px.scatter(
                filtered_df,
                x=x_axis,
                y=y_axis,
                title=f"{y_axis} vs {x_axis}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "Scatter Plot requires at least "
                "two numerical columns."
            )


    # -----------------------------------
    # HISTOGRAM
    # -----------------------------------

    elif chart_type == "Histogram":

        if len(numerical_columns) > 0:

            column = st.selectbox(
                "Choose Numerical Column",
                numerical_columns,
                key="histogram_column"
            )

            fig = px.histogram(
                filtered_df,
                x=column,
                title=f"Distribution of {column}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No numerical columns are available "
                "for the Histogram."
            )


# -----------------------------------
# NO DATASET UPLOADED
# -----------------------------------

else:

    st.info(
        "👆 Upload a CSV or Excel dataset "
        "to start exploring your data!"
    )