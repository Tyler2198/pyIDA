
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
        plt.figure(figsize=(12, 8))
        sns.heatmap(participation_matrix.sort_index(), cmap="Blues", cbar=False, linewidths=.5)
        plt.title("Participation Heatmap (Subjects × Time Points)")
        plt.xlabel("Time Point")
        plt.ylabel("Subject ID")
        plt.show()

    return summary
