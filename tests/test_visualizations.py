
import numpy as np
import pandas as pd
import pytest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.wearable_visualization.trajectories import (
    plot_individual_trajectory
)
from src.wearable_visualization.comparisons import (
    plot_participant_comparison
)
from src.wearable_visualization.missingness import (
    plot_missingness_heatmap
)
from src.wearable_visualization.multivariable import (
    plot_multivariable_trajectories
)
from src.wearable_visualization.export import save_figure


def test_individual_trajectory_missingness():
    data = pd.DataFrame({
        "participant_id": ["P001"] * 3,
        "date": pd.date_range("2026-01-01", periods=3),
        "sleep_duration_min": [400, np.nan, 440]
    })

    ax = plot_individual_trajectory(
        data, "P001", "sleep_duration_min"
    )

    values = ax.lines[0].get_ydata()

    assert np.allclose(
        values, [400, np.nan, 440], equal_nan=True
    )

    plt.close(ax.figure)


def test_invalid_participant():
    data = pd.DataFrame({
        "participant_id": ["P001"],
        "date": pd.to_datetime(["2026-01-01"]),
        "sleep_duration_min": [400]
    })

    with pytest.raises(ValueError):
        plot_individual_trajectory(
            data, "P999", "sleep_duration_min"
        )


def test_participant_comparison():
    data = pd.DataFrame({
        "participant_id": [
            "P001", "P001", "P002", "P002"
        ],
        "day": [1, 2, 1, 2],
        "sleep_duration_min": [400, 420, 440, 460]
    })

    ax = plot_participant_comparison(
        data, "sleep_duration_min"
    )

    observed_mean = ax.lines[-1].get_ydata()

    assert np.allclose(observed_mean, [420, 440])

    plt.close(ax.figure)


def test_missingness_heatmap():
    data = pd.DataFrame({
        "participant_id": ["P001", "P001", "P002"],
        "day": [1, 2, 1],
        "sleep_duration_min": [400, np.nan, 440]
    })

    ax = plot_missingness_heatmap(
        data,
        "sleep_duration_min",
        expected_days=[1, 2]
    )

    matrix = np.asarray(ax.images[0].get_array())

    expected = np.array([
        [1, 0],
        [1, 0]
    ])

    assert np.array_equal(matrix, expected)

    plt.close(ax.figure)


def test_multivariable_plot():
    data = pd.DataFrame({
        "participant_id": ["P001"] * 3,
        "day": [1, 2, 3],
        "sleep_duration_min": [400, np.nan, 440],
        "hrv_rmssd_ms": [40, 42, 44],
        "steps": [7000, 8000, 9000]
    })

    fig, axes = plot_multivariable_trajectories(
        data,
        "P001",
        expected_days=[1, 2, 3]
    )

    assert len(axes) == 3

    assert np.allclose(
        axes[0].lines[0].get_ydata(),
        [400, np.nan, 440],
        equal_nan=True
    )

    assert np.allclose(
        axes[1].lines[0].get_ydata(),
        [40, 42, 44]
    )

    assert np.allclose(
        axes[2].lines[0].get_ydata(),
        [7000, 8000, 9000]
    )

    plt.close(fig)


def test_figure_export(tmp_path):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])

    paths = save_figure(
        fig,
        filename="test_figure",
        output_dir=tmp_path,
        formats=("png", "pdf")
    )

    assert len(paths) == 2

    png = tmp_path / "test_figure.png"
    pdf = tmp_path / "test_figure.pdf"

    assert png.is_file()
    assert pdf.is_file()

    assert png.stat().st_size > 0
    assert pdf.stat().st_size > 0

    with png.open("rb") as file:
        assert file.read(8) == bytes([137, 80, 78, 71, 13, 10, 26, 10])

    with pdf.open("rb") as file:
        assert file.read(5) == b"%PDF-"

    plt.close(fig)
