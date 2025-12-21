import streamlit as st
from com.powerball.main.utility.common_utilities import CommonUtilities


def get_dates_for_column(key_id, min_d, max_d, global_state):
    """
    Helper to determine date range based on global override or local slider.
    global_state is a tuple: (is_override_active, global_start, global_end)
    """
    is_global, g_start, g_end = global_state

    if is_global:
        return g_start, g_end

    st.write(f"**Filter for {key_id}:**")
    slider = st.slider(
        f"Range ({key_id})",
        min_value=min_d,
        max_value=max_d,
        value=(min_d, max_d),
        key=key_id
    )
    return slider[0], slider[1]

def render_chart_in_column(column_obj, title, data, GeneratorClass,
                           min_d, max_d, global_state,
                           figsize, plot_kwargs):
    """
    Generic function to render a single chart inside a Streamlit column.

    :param column_obj: The st.column object to render into.
    :param title: The header text for this column.
    :param data: The raw input data.
    :param GeneratorClass: The class to instantiate (e.g. FrequencyChartGenerator).
    :param min_d/max_d: Config limits.
    :param global_state: Tuple (override_bool, start, end).
    :param figsize: Tuple (width, height).
    :param plot_kwargs: Dictionary of arguments for the .plot() method (e.g. {'type': 'main'}).
    """
    with column_obj:
        st.subheader(title)

        # 1. Handle Slider Logic
        # We use the title as the unique key for the slider
        start, end = get_dates_for_column(title, min_d, max_d, global_state)

        # 2. Instantiate the Chart Generator
        gen = GeneratorClass(
            data,
            start_date=start.strftime("%m-%d-%Y"),
            end_date=end.strftime("%m-%d-%Y"),
            chart_name=title
        )

        # 3. Generate Plot (Unpacking specific kwargs like 'type' or 'position_index')
        fig = gen.plot(figsize=figsize, **plot_kwargs)

        # 4. Render
        st.pyplot(fig, use_container_width=True, dpi=CommonUtilities.get_chart_dpi())
