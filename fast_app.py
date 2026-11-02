
import streamlit as st
import pandas as pd
import io

from scraper_fast import scrape_member_list, scrape_all_addresses


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="BNI Member Directory Scraper",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("📊 BNI Member Directory Scraper")

st.subheader("Mumbai North East Chapter")

st.write(
    "Fetch member details, view the directory, "
    "and download the records in Excel format."
)

st.divider()


# ==========================================
# START SCRAPING
# ==========================================

if st.button("🚀 Start Scraping", type="primary"):

    try:

        with st.spinner(
            "Fetching member details and addresses. "
            "Please wait..."
        ):

            # Fetch member list
            members = scrape_member_list()

            if members:

                # Fetch addresses using Selenium
                members = scrape_all_addresses(members)

                # Create DataFrame
                df = pd.DataFrame(members)

                # Select columns for display and Excel
                df = df[
                    [
                        "Member Name",
                        "Company",
                        "Profession/Specialty",
                        "Phone",
                        "Address",
                        "Profile URL"
                    ]
                ]

                # Generate Excel in memory
                excel_buffer = io.BytesIO()

                df.to_excel(
                    excel_buffer,
                    index=False,
                    engine="openpyxl"
                )

                excel_buffer.seek(0)

                # Save results in Streamlit session
                st.session_state["members_df"] = df

                st.session_state["excel_file"] = (
                    excel_buffer.getvalue()
                )

                st.success(
                    "Scraping completed successfully!"
                )

            else:

                st.warning(
                    "No member records were found."
                )

    except Exception as error:

        st.error(
            f"Something went wrong: {error}"
        )


# ==========================================
# DISPLAY SCRAPED DATA
# ==========================================

if "members_df" in st.session_state:

    df = st.session_state["members_df"]

    st.divider()

    st.subheader("📋 Scraped Member Details")

    # Metrics
    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="Total Members",
            value=len(df)
        )

    with col2:

        addresses_found = (
            df["Address"] != "Not Available"
        ).sum()

        st.metric(
            label="Addresses Retrieved",
            value=int(addresses_found)
        )

    # Search functionality
    search_query = st.text_input(
        "🔍 Search by Member Name or Company"
    )

    if search_query:

        filtered_df = df[
            df["Member Name"].str.contains(
                search_query,
                case=False,
                na=False
            )
            |
            df["Company"].str.contains(
                search_query,
                case=False,
                na=False
            )
        ]

    else:

        filtered_df = df

    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # Excel download button
    st.download_button(
        label="📥 Download Excel File",
        data=st.session_state["excel_file"],
        file_name="BNI_Mumbai_North_East_Members.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        type="primary"
    )


else:

    st.info(
        "Click 'Start Scraping' to fetch the member information."
    )


# ==========================================
# FOOTER
# ==========================================



st.divider()

st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 15px;
                justify-content: center;">
        <img src="https://github.com/pillailakshmi099-ops.png"
             width="75"
             style="border-radius: 50%;">
        <div>
            <h4 style="margin: 0;">Lakshmi Prasanth Pillai</h4>
            <p style="margin: 2px 0;">@pillailakshmi099-ops</p>
            <a href="https://github.com/pillailakshmi099-ops/bni-member-scraper.git"
               target="_blank">Visit GitHub Repository ↗</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
