import streamlit as st


def render_machine_card():

    with st.container(border=True):

        col1, col2 = st.columns([5, 1])

        with col1:

            st.subheader("Machine L-213")

            st.caption("Type L")

        with col2:

            st.warning("21.7 %")

        a, b, c = st.columns(3)

        a.metric(
            "Torque",
            "43.7 Nm"
        )

        b.metric(
            "Tool Wear",
            "217 min"
        )

        c.metric(
            "RPM",
            "1355"
        )

        st.markdown("### Top Risk Factors")

        x, y, z = st.columns(3)

        with x:

            st.error("↑ Torque")

        with y:

            st.error("↑ Tool Wear")

        with z:

            st.success("↓ Power")
