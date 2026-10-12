
import pandas as pd
import matplotlib.pyplot as plt

from .trajectories import VARIABLE_LABELS


def plot_multivariable_trajectories(
    df,
    participant_id,
    variables=None,
    participant_col="participant_id",
    day_col="day",
    expected_days=None,
    figsize=(10, 8)
):
    """
    Plot multiple longitudinal variables for one participant.

    Each variable has its own y-axis, while all panels share
    the same study-day x-axis.

    Missing observations remain gaps.
    """

    if variables is None:
        variables = [
            "sleep_duration_min",
            "hrv_rmssd_ms",
            "steps"
        ]

    if not variables:
        raise ValueError("At least one variable is required.")

    required = [participant_col, day_col] + variables

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    participant_data = df.loc[
        df[participant_col] == participant_id
    ].copy()

    if participant_data.empty:
        raise ValueError(
            f"Participant {participant_id} not found."
        )

    if participant_data[day_col].duplicated().any():
        raise ValueError(
            "Duplicate study days detected for participant."
        )

    if expected_days is None:
        days = sorted(
            participant_data[day_col].dropna().unique()
        )
    else:
        days = list(expected_days)

    if not days:
        raise ValueError("No study days available.")

    fig, axes = plt.subplots(
        nrows=len(variables),
        ncols=1,
        figsize=figsize,
        sharex=True,
        squeeze=False
    )

    axes = axes.flatten()

    for ax, variable in zip(axes, variables):

        values = (
            participant_data
            .set_index(day_col)[variable]
            .reindex(days)
        )

        ax.plot(
            days,
            values,
            marker="o",
            linewidth=1.5,
            markersize=4
        )

        ax.set_ylabel(
            VARIABLE_LABELS.get(variable, variable)
        )

        ax.grid(alpha=0.25)

    axes[-1].set_xlabel("Study day")
    axes[-1].set_xticks(days)

    fig.suptitle(
        f"Longitudinal wearable measurements: {participant_id}"
    )

    fig.tight_layout()

    return fig, axes
