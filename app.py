import io
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="AI Business Data Analyst", page_icon="📊", layout="wide")

st.title("📊 AI Data Analyst")
st.caption(
    "Upload a CSV or Excel dataset, assess data quality, clean missing values, "
    "explore interactive analytics, and generate automated insights."
)

@st.cache_data
def load_file(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    raise ValueError("Please upload a CSV or Excel file.")

def clean_data(df):
    out = df.copy()
    out.columns = [str(c).strip().replace(" ", "_") for c in out.columns]
    out = out.drop_duplicates()
    # Try parsing date-like columns
    for c in out.columns:
        if "date" in c.lower():
            try:
                out[c] = pd.to_datetime(out[c], errors="coerce")
            except Exception:
                pass
    
    return out

def money(x):
    return f"{x:,.2f}"

def auto_insights(df):
    
    insights = []

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # Make column names easier to read
    def pretty(name):
        return str(name).replace("_", " ")

    # ---------------------------------------------------
    # 1. BASIC NUMERIC INSIGHTS
    # ---------------------------------------------------
    for col in numeric_cols:
        series = df[col].dropna()

        if len(series) > 0:
            insights.append(
                f"Average {pretty(col)} is {series.mean():,.2f}."
            )

    # ---------------------------------------------------
    # 2. BEST AND LOWEST PERFORMING CATEGORIES
    # ---------------------------------------------------
    for num_col in numeric_cols:
        for cat_col in categorical_cols:

            # Ignore ID-like / very high-cardinality columns
            unique_count = df[cat_col].nunique(dropna=True)

            if 2 <= unique_count <= 20:

                grouped = (
                    df.dropna(subset=[cat_col])
                    .groupby(cat_col)[num_col]
                    .mean()
                    .dropna()
                    .sort_values(ascending=False)
                )

                if len(grouped) >= 2:
                    best_category = grouped.index[0]
                    best_value = grouped.iloc[0]

                    worst_category = grouped.index[-1]
                    worst_value = grouped.iloc[-1]

                    insights.append(
                        f"{best_category} has the highest average "
                        f"{pretty(num_col)} at {best_value:,.2f} "
                        f"when compared by {pretty(cat_col)}."
                    )

                    difference = best_value - worst_value

                    insights.append(
                        f"The gap in average {pretty(num_col)} between "
                        f"{best_category} and {worst_category} is "
                        f"{difference:,.2f}."
                    )

    # ---------------------------------------------------
    # 3. STRONG CORRELATIONS
    # ---------------------------------------------------
    if len(numeric_cols) >= 2:

        corr = df[numeric_cols].corr()

        relationships = []

        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):

                col1 = numeric_cols[i]
                col2 = numeric_cols[j]
                value = corr.loc[col1, col2]

                if pd.notna(value) and abs(value) >= 0.5:
                    relationships.append(
                        (abs(value), col1, col2, value)
                    )

        relationships.sort(reverse=True)

        for _, col1, col2, value in relationships[:3]:

            direction = "positive" if value > 0 else "negative"

            insights.append(
                f"{pretty(col1)} and {pretty(col2)} have a strong "
                f"{direction} relationship "
                f"(correlation {value:.2f})."
            )

    # ---------------------------------------------------
    # 4. OUTLIER DETECTION
    # ---------------------------------------------------
    for col in numeric_cols:

        series = df[col].dropna()

        if len(series) > 3:

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1

            if iqr > 0:
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr

                outliers = series[
                    (series < lower) | (series > upper)
                ]

                if len(outliers) > 0:

                    percentage = (
                        len(outliers) / len(series)
                    ) * 100

                    insights.append(
                        f"{pretty(col)} contains {len(outliers)} "
                        f"potential outliers, representing "
                        f"{percentage:.1f}% of its valid observations."
                    )

    # ---------------------------------------------------
    # 5. MISSING-DATA WARNING
    # ---------------------------------------------------
    missing = int(df.isna().sum().sum())

    if missing > 0:
        insights.insert(
            0,
            f"Data-quality warning: {missing} missing value(s) "
            f"remain in the dataset."
        )

    # ---------------------------------------------------
    # RETURN INSIGHTS
    # ---------------------------------------------------
    if not insights:
        return [
            "No strong automatic insight was detected."
        ]

    return insights[:15]
    

with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx","xls"])
    st.title("📊 AI Data Analyst")
st.caption(
    "Upload a CSV or Excel dataset, assess data quality, clean missing values, "
    "explore interactive analytics, and generate automated insights."
)

if uploaded is None:
    st.info("Upload a dataset from the sidebar. The project ZIP also contains a sample business dataset.")
    st.stop()

try:
    raw = load_file(uploaded)
except Exception as e:
    st.error(f"Could not read file: {e}")
    st.stop()

cleaned = clean_data(raw)

# Reset processed data when a new file is uploaded
current_file = uploaded.name

if st.session_state.get("current_file") != current_file:
    st.session_state["current_file"] = current_file
    st.session_state["processed_data"] = cleaned.copy()
    st.session_state["cleaning_applied"] = False

analysis_df = st.session_state["processed_data"]
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📋 Overview",
        "🧹 Data Quality",
        "📊 Visual Explorer",
        "💡 Insights & Export"
    ]
)

with tab1:
    st.subheader("Dataset overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", f"{len(analysis_df):,}")
    c2.metric("Columns", len(analysis_df.columns))
    c3.metric(
        "Numeric fields",
        len(analysis_df.select_dtypes(include=np.number).columns)
    )
    c4.metric("Missing Values", int(analysis_df.isna().sum().sum()))

    st.dataframe(
        analysis_df.head(100),
        use_container_width=True
    )

    st.subheader("Descriptive statistics")
    st.dataframe(
        analysis_df.describe(include="all").transpose(),
        use_container_width=True
    )

with tab2:
    if st.session_state.get("cleaning_success"):
        st.success("Cleaning applied successfully.")
        st.session_state["cleaning_success"] = False

    st.subheader("Data Quality & Cleaning")
    st.caption(
    "Review missing values and duplicate records, then clean the dataset before analysis."
)
    q1,q2,q3 = st.columns(3)
    q1.metric("Missing values (raw)", int(raw.isna().sum().sum()))
    q2.metric("Duplicate rows removed", int(raw.duplicated().sum()))
    q3.metric("Rows after cleaning", f"{len(analysis_df):,}")
    quality = pd.DataFrame({
        "column": raw.columns,
        "dtype": [str(raw[c].dtype) for c in raw.columns],
        "missing": [int(raw[c].isna().sum()) for c in raw.columns],
        "unique": [int(raw[c].nunique(dropna=True)) for c in raw.columns],
    })
    st.dataframe(quality, use_container_width=True)
    st.subheader("Missing Value Treatment")

    missing_columns = [
        c for c in cleaned.columns
        if cleaned[c].isna().any()
    ]

    if not missing_columns:
        st.success("No missing values detected.")
    else:
        st.warning(
            f"{int(cleaned.isna().sum().sum())} missing values detected."
        )

        treatments = {}

        for c in missing_columns:
            missing_count = int(cleaned[c].isna().sum())

            st.write(
                f"**{c}** — {missing_count} missing value(s)"
            )
           

            if pd.api.types.is_numeric_dtype(cleaned[c]):
                options = [
                    "Keep missing",
                    "Fill with median",
                    "Fill with mean",
                    "Drop affected rows"
                ]
            else:
                options = [
                    "Keep missing",
                    'Fill with "Unknown"',
                    "Fill with mode",
                    "Drop affected rows"
                ]

            choice = st.selectbox(
                f"Treatment for {c}",
                options,
                key=f"missing_{c}"
            )

            treatments[c] = choice
                
                
        if st.button("Apply Cleaning", type="primary"):
            processed = cleaned.copy()

            for c, choice in treatments.items():

                if choice == "Fill with median":
                    processed[c] = processed[c].fillna(
                        processed[c].median()
                    )

                elif choice == "Fill with mean":
                    processed[c] = processed[c].fillna(
                        processed[c].mean()
                    )

                elif choice == 'Fill with "Unknown"':
                    processed[c] = processed[c].fillna("Unknown")

                elif choice == "Fill with mode":
                    mode = processed[c].mode(dropna=True)

                    if not mode.empty:
                        processed[c] = processed[c].fillna(
                            mode.iloc[0]
                        )

                elif choice == "Drop affected rows":
                    processed = processed.dropna(subset=[c])

            st.session_state["processed_data"] = processed
            st.session_state["cleaning_success"] = True
            st.rerun()

with tab3:
    st.subheader("Interactive visual explorer")
    numeric = analysis_df.select_dtypes(include=np.number).columns.tolist()
    categorical = analysis_df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

    if numeric:
        x = st.selectbox("Numeric metric", numeric)
         
        if categorical:
            group = st.selectbox("Group by", categorical)

            aggregation = st.selectbox(
                "Aggregation",
                ["Sum", "Average", "Median", "Minimum", "Maximum", "Count"]
            )

            grouped = analysis_df.groupby(group, dropna=False)[x]

            if aggregation == "Sum":
                agg = grouped.sum().reset_index()
            elif aggregation == "Average":
                agg = grouped.mean().reset_index()
            elif aggregation == "Median":
                agg = grouped.median().reset_index()
            elif aggregation == "Minimum":
                agg = grouped.min().reset_index()
            elif aggregation == "Maximum":
                agg = grouped.max().reset_index()
            else:
                agg = grouped.count().reset_index()

            agg = agg.sort_values(x, ascending=False).head(20)

            fig = px.bar(
                agg,
                x=group,
                y=x,
                title=f"{aggregation} {x} by {group}"
            )

            st.plotly_chart(fig, use_container_width=True)
        fig2 = px.histogram(analysis_df, x=x, title=f"Distribution of {x}")
        st.plotly_chart(fig2, use_container_width=True)
        if len(numeric) >= 2:
            corr = analysis_df[numeric].corr(numeric_only=True)
            fig3 = px.imshow(corr, text_auto=".2f", title="Numeric correlation matrix")
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No numeric columns were detected.")

with tab4:
    st.subheader("Automated Insights & Export")
    st.caption(
        "Review automatically generated analytical insights and download the cleaned dataset."
    )
    for insight in auto_insights(analysis_df):
        st.success(insight)
    st.caption("These insights are deterministic analytics, not LLM-generated claims. Validate business decisions against the source data.")
    csv = analysis_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download cleaned CSV", csv, "cleaned_data.csv", "text/csv")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        analysis_df.to_excel(writer, index=False, sheet_name="Cleaned Data")
    st.download_button("Download cleaned Excel", buffer.getvalue(), "cleaned_data.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
