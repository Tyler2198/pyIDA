
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
    - show_plot: whether to display a heatmap of participation

    Returns:
    - summary: dict with basic stats
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
