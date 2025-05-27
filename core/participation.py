
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

def describe_participation(df, id_col='subject_id', time_col='visit_month', show_plot=True):
    """
    Summarize participation patterns in a longitudinal dataset.

    Parameters:
    - df: pandas.DataFrame in long format
    - id_col: column name for subject ID
    - time_col: column name for time variable
    - show_plot: whether to display a heatmap of participation, a histogram for the number of measurements per individual, a barplot for the number of subjects per timepoint

    Returns:
    - (Optional) Heatmap, Histogram and BarPlot for participation through time
    - two tables, one for summary statistics and one for timepoint distribution
    """
    visits_per_subject = df.groupby(id_col)[time_col].nunique()
    subjects_per_time = df.groupby(time_col)[id_col].nunique()
    participation_matrix = df.pivot_table(index=id_col, columns=time_col, values=time_col, aggfunc='count')
    participation_matrix = participation_matrix.notnull().astype(int)

    summary = {
        "total_subjects": df[id_col].nunique(),
        "total_time_points": df[time_col].nunique(),
        "avg_visits_per_subject": visits_per_subject.mean(),
        "subjects_per_time_point": subjects_per_time.to_dict(),
        "min_visits_per_subject": visits_per_subject.min(),
        "max_visits_per_subject": visits_per_subject.max()
    }

    if show_plot:
        # Heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(participation_matrix.sort_index(), cmap="Blues", cbar=False, linewidths=.5)
        plt.title("Participation Heatmap (Subjects × Time Points)")
        plt.xlabel("Time Point")
        plt.ylabel("Subject ID")
        plt.show()

        # Histogram: Number of measurements per individual
        plt.figure(figsize=(10, 5))
        sns.histplot(visits_per_subject, bins=range(1, visits_per_subject.max() + 2), kde=False, color='teal')
        plt.title("Distribution of Number of Visits per Subject")
        plt.xlabel("Number of Visits")
        plt.ylabel("Number of Subjects")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Barplot: Number of subjects per time point
        plt.figure(figsize=(10, 5))
        sns.barplot(x=subjects_per_time.index, y=subjects_per_time.values, color='skyblue')
        plt.title("Number of Subjects per Time Point")
        plt.xlabel("Time Point")
        plt.ylabel("Number of Subjects")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    summary_df = pd.DataFrame({
        "Metric": [
            "Total Subjects",
            "Total Time Points",
            "Average Visits per Subject",
            "Min Visits per Subject",
            "Max Visits per Subject"
        ],
        "Value": [
            summary["total_subjects"],
            summary["total_time_points"],
            f"{summary['avg_visits_per_subject']:.2f}",
            summary["min_visits_per_subject"],
            summary["max_visits_per_subject"]
        ]
    })

    # Create clean timepoint distribution table
    timepoint_df = pd.DataFrame(subjects_per_time).reset_index().rename(columns={
        "visit_month": "Time Point",
        "subject_id": "Number of Subjects"
})
    
    # Display clean DataFrame tables without index
    print("\n📊 Participation Summary Table:")
    display(summary_df.style.hide(axis="index"))

    print("\n📊 Number of Subjects per Time Point:")
    display(timepoint_df.style.hide(axis="index"))



def analyze_time_deviation(df, id_col='subject_id', nominal_col='nominal_time', actual_col='actual_time', show_plot=True):
    """
    Analyze and visualize deviations between nominal and actual timepoints.

    Parameters:
    - df: pandas.DataFrame
    - id_col: column name for subject ID
    - nominal_col: column name for nominal visit time
    - actual_col: column name for actual visit time
    - show_plot: whether to generate plots

    Returns:
    - deviation_df: DataFrame with deviation and summary stats
    """
    df = df.copy()
    df["deviation"] = df[actual_col] - df[nominal_col]

    # Global stats
    global_stats = {
        "mean_deviation": round(df["deviation"].mean(), 2),
        "std_deviation": round(df["deviation"].std(), 2),
        "min_deviation": round(df["deviation"].min(), 2),
        "max_deviation": round(df["deviation"].max(), 2)
    }

    # Deviation by nominal timepoint
    per_nominal = df.groupby(nominal_col)["deviation"].agg(['mean', 'std', 'min', 'max']).round(2).reset_index()

    if show_plot:
        plt.figure(figsize=(10, 5))
        sns.histplot(df["deviation"], bins=30, kde=True, color='salmon')
        plt.title("Distribution of Visit Time Deviations")
        plt.xlabel("Deviation (Actual - Nominal Time)")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 5))
        sns.boxplot(x=nominal_col, y="deviation", data=df, palette="Set3")
        plt.title("Deviation Distribution by Nominal Time Point")
        plt.xlabel("Nominal Time Point")
        plt.ylabel("Deviation (months)")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    # Convert global_stats dict to a clean DataFrame
    global_stats_df = pd.DataFrame({
        "Metric": list(global_stats.keys()),
        "Value": [f"{v:.2f}" for v in global_stats.values()]
    })

    # Clean and rename per-nominal table
    per_nominal.columns = ["Nominal Time", "Mean Deviation", "Std Deviation", "Min Deviation", "Max Deviation"]

    print("\n📊 Global Deviation Summary:")
    display(global_stats_df.style.hide(axis="index"))

    print("\n📊 Deviation by Nominal Time Point:")
    display(per_nominal.style.hide(axis="index"))



def summarize_by_structure(df, id_col, structural_vars, outcome_vars=None, show_plot=True):
    """
    Summarizes outcomes stratified by structural variables.

    Parameters:
    - df: pandas.DataFrame
    - id_col: ID column for subjects
    - structural_vars: list of variables to group by (e.g., ['sex', 'center'])
    - outcome_vars: list of outcome variables to summarize (e.g., ['BMI', 'grip_strength'])
    - show_plot: show boxplots if True

    Returns:
    - summary_tables: dictionary of summary tables per structural variable
    """
    if outcome_vars is None:
        outcome_vars = df.select_dtypes(include=[np.number]).columns.difference([id_col] + structural_vars).tolist()

    summary_tables = {}

    for var in structural_vars:
        grouped = df.groupby(var)[outcome_vars].agg(['mean', 'std', 'min', 'max']).round(2)
        grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
        summary_tables[var] = grouped.reset_index()

        print(f"\n📊 Summary by {var}:\n")
        display(summary_tables[var].style.hide(axis="index"))

        if show_plot:
            for outcome in outcome_vars:
                plt.figure(figsize=(8, 5))
                sns.boxplot(data=df, x=var, y=outcome, palette="pastel")
                plt.title(f"{outcome} by {var}")
                plt.grid(True, linestyle='--', alpha=0.6)
                plt.tight_layout()
                plt.show()

    return summary_tables
