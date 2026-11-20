
import streamlit as st


def render_sidebar(pages):
    with st.sidebar:

        # Brand section
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="brand-mark">S</div>
                <div class="brand-info">
                    <div class="brand-name">SpendWise</div>
                    <div class="brand-caption">PERSONAL FINANCE</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section-label">WORKSPACE</div>',
            unsafe_allow_html=True,
        )

        # Navigation
        selected = st.radio(
            "Navigation",
            options=list(pages.keys()),
            format_func=lambda name: (
                f"{pages[name][0]}   {name}"
            ),
            key="spendwise_navigation",
            label_visibility="collapsed",
        )

        # Sidebar footer
        st.markdown(
            """
            <div class="sidebar-footer">
                <div class="connection-status">
                    <span class="status-dot"></span>
                    <span>Connected to expense API</span>
                </div>
                <div class="sidebar-version">SpendWise · Personal Finance</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected
