# pyIDA

**pyIDA** is a Python package for Initial Data Analysis (IDA) in longitudinal studies, built in alignment with the [STRATOS framework](http://stratos-initiative.org).

It provides reproducible, visual, and tabular summaries for screening data quality, participation patterns, and time irregularities in longitudinal datasets — especially useful for cohort studies, clinical follow-ups, and EHR-based research.

---

## 📦 Modules Implemented So Far

### ✅ 1. `describe_participation()`

Summarizes how individuals participate across time in longitudinal studies.

- **Inputs**: Long-format DataFrame with:
  - `subject_id`: unique ID per individual
  - `time_point`: time or visit index
- **Outputs**:
  - Number of subjects per time point
  - Number of visits per subject
  - Clean summary tables
  - Heatmap of participation matrix (Subjects × Time)
  - Histogram of visits per subject
  - Bar chart of subjects per time point

#### Example Usage

```python
from core.participation import describe_participation

summary = describe_participation(
    df,
    id_col='subject_id',
    time_col='visit_month',
    show_plot=True  # default is True
)
```

### ✅ 2. `analyze_time_deviation()`

Analyzes the deviation between **nominal** (planned) and **actual** visit times.

- **Inputs**: Long-format DataFrame with:
  - `subject_id`: unique ID per individual
  - `nominal_time`: planned time of visit (e.g., months since baseline)
  - `actual_time`: observed time of visit (e.g., real measurement date in months)

- **Outputs**:
  - A `deviation` column: `actual_time - nominal_time`
  - **Global summary table** with mean, std, min, max deviation
  - **Grouped summary** of deviation by nominal time point
  - **Histogram** of time deviations
  - **Boxplot** of deviations across visit time points

> 🧼 Beautiful tables are always shown with hidden index.  
> 🧪 To avoid Jupyter showing duplicated output when assigning return values, use `;` or `_ = analyze_time_deviation(...)`.

#### Example Usage

```python
from core.time_metrics import analyze_time_deviation

deviation_df, global_stats_df, per_nominal_df = analyze_time_deviation(
    df,
    id_col='subject_id',
    nominal_col='nominal_time',
    actual_col='actual_time',
    show_plot=True  # plots + tables shown
)
```

### ✅ 3. `summarize_by_structure()`

Summarizes key outcome variables (e.g., BMI, grip strength) stratified by one or more **structural variables** such as `sex`, `center`, or `age_group`.

- **Inputs**: Long-format DataFrame with:
  - `subject_id`: unique ID per individual
  - One or more structural variables (e.g., `sex`, `center`)
  - One or more numeric outcome variables (e.g., `BMI`, `grip_strength`)
- **Outputs**:
  - Clean summary tables (mean, std, min, max) for each group
  - Boxplots of outcomes stratified by group
  - Summary statistics for each structural variable listed separately

> 🧼 Tables are displayed beautifully with hidden index.  
> 🔍 Automatically handles multiple grouping and outcome variables.

#### Example Usage

```python
from core.structural_vars import summarize_by_structure

summary_tables = summarize_by_structure(
    df,
    id_col='subject_id',
    structural_vars=['sex', 'center'],
    outcome_vars=['grip_strength', 'BMI'],
    show_plot=True  # plots + tables shown
)
```
