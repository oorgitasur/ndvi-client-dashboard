import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
import plotly.express as px

# =====================================================
# BASIC CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

PROJECT_NAME = "PELI DASPUR STRETCH Multispectral+RGB Crop Health Survey"
CLIENT_NAME = "Client Demo"
SURVEY_DATE = "May 2026"
DATA_TYPE = "Drone-Based Multispectral NDVI Visualization"
ANALYSIS_TYPE = "Visual Crop Vigor Classification"

st.set_page_config(
    page_title="Crop Health Intelligence Dashboard",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# FILE PATHS
# =====================================================

preview_path = BASE_DIR / "data" / "preview" / "ndvi_web.jpg"
classified_path = BASE_DIR / "data" / "processed" / "classified_crop_health.png"
annotated_path = BASE_DIR / "data" / "processed" / "annotated_priority_zones.png"
summary_path = BASE_DIR / "data" / "processed" / "crop_health_summary.csv"
zones_path = BASE_DIR / "data" / "processed" / "priority_scouting_zones.csv"
methodology_path = BASE_DIR / "data" / "processed" / "methodology_note.txt"

if not annotated_path.exists():
    annotated_path = BASE_DIR / "data" / "processed" / "annotated_stress_zones.png"

if not zones_path.exists():
    zones_path = BASE_DIR / "data" / "processed" / "stress_zones.csv"

# =====================================================
# VALIDATION
# =====================================================

required_files = [
    preview_path,
    classified_path,
    annotated_path,
    summary_path,
    zones_path,
]

missing_files = [str(p) for p in required_files if not p.exists()]

if missing_files:
    st.error("Some required files are missing. Please run preprocessing first.")
    st.code("\n".join(missing_files))
    st.stop()

# =====================================================
# LOAD DATA
# =====================================================

summary_df = pd.read_csv(summary_path)

try:
    zones_df = pd.read_csv(zones_path)
except Exception:
    zones_df = pd.DataFrame(
        columns=[
            "Zone",
            "Low Relative Vigor Share (%)",
            "Priority",
            "Recommendation",
        ]
    )


def get_metric_value(class_name):
    row = summary_df.loc[summary_df["Class"] == class_name, "Approx Share (%)"]
    if len(row) == 0:
        return 0.0
    return float(row.iloc[0])


high = get_metric_value("High Vigor")
moderate = get_metric_value("Stable / Moderate Vigor")
low = get_metric_value("Low Relative Vigor")
mixed = get_metric_value("Mixed / Transitional")

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
"""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

.hero-container {
    background: linear-gradient(135deg, #102315 0%, #1f3b22 45%, #3d3515 100%);
    border-radius: 26px;
    padding: 36px 40px;
    margin-bottom: 26px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 18px 40px rgba(0,0,0,0.22);
}

.hero-label {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: rgba(255,255,255,0.13);
    color: #d9f99d;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero-title {
    font-size: 2.9rem;
    line-height: 1.08;
    font-weight: 900;
    color: #ffffff;
    margin: 10px 0 14px 0;
}

.hero-subtitle {
    color: #d1d5db;
    font-size: 1.08rem;
    line-height: 1.55;
    max-width: 920px;
    margin-bottom: 22px;
}

.meta-row {
    margin-top: 18px;
    line-height: 2.6;
}

.meta-pill {
    display: inline-block;
    background: rgba(255,255,255,0.10);
    color: #f9fafb;
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 999px;
    padding: 8px 13px;
    font-size: 0.88rem;
    margin-right: 8px;
    margin-bottom: 8px;
}

.kpi-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 18px 18px;
    min-height: 118px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.14);
}

.kpi-label {
    color: #d1d5db;
    font-size: 0.88rem;
    font-weight: 650;
    margin-bottom: 8px;
}

.kpi-value {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 850;
    margin-bottom: 4px;
}

.kpi-note {
    color: #a7f3d0;
    font-size: 0.78rem;
}

.landing-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
}

.landing-card-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 10px;
}

.landing-card-text {
    color: #d1d5db;
    font-size: 0.96rem;
    line-height: 1.55;
}

.confidence-tag {
    display: inline-block;
    border-radius: 999px;
    padding: 6px 10px;
    background: rgba(250, 204, 21, 0.14);
    color: #fde68a;
    border: 1px solid rgba(250, 204, 21, 0.28);
    font-size: 0.8rem;
    font-weight: 700;
    margin-top: 10px;
}

.soft-divider {
    height: 1px;
    background: rgba(255,255,255,0.10);
    margin: 22px 0;
}

.section-header {
    font-size: 1.45rem;
    font-weight: 750;
    margin-top: 0.5rem;
    margin-bottom: 0.8rem;
}

.insight-box {
    border: 1px solid rgba(120,120,120,0.25);
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 12px;
    background: rgba(255,255,255,0.03);
}

.method-note {
    background: rgba(30, 64, 175, 0.16);
    border-left: 4px solid #60a5fa;
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 10px;
    margin-bottom: 18px;
    color: #dbeafe;
}

.action-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.footer-note {
    font-size: 0.85rem;
    color: #9ca3af;
    margin-top: 2rem;
}

button[kind="secondary"] {
    border-radius: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# PREMIUM HEADER
# =====================================================

hero_html = (
    '<div class="hero-container">'
    '<span class="hero-label">Drone-Based Crop Intelligence</span>'
    '<h1 class="hero-title">Crop Health Intelligence Dashboard</h1>'
    '<p class="hero-subtitle">'
    'A visual NDVI interpretation system for understanding field-level vegetation variability, '
    'identifying monitoring-required zones, and planning targeted ground scouting.'
    '</p>'
    '<div class="meta-row">'
    f'<span class="meta-pill"><b>Project:</b> {PROJECT_NAME}</span>'
    f'<span class="meta-pill"><b>Client:</b> {CLIENT_NAME}</span>'
    f'<span class="meta-pill"><b>Survey:</b> {SURVEY_DATE}</span>'
    '<span class="meta-pill"><b>Data:</b> Rendered NDVI Visualization</span>'
    '<span class="meta-pill"><b>Output:</b> Scouting Priority Map</span>'
    '</div>'
    '</div>'
)

st.markdown(hero_html, unsafe_allow_html=True)

# =====================================================
# KPI CARDS
# =====================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">High Vigor Area</div>
    <div class="kpi-value">{high}%</div>
    <div class="kpi-note">Strong vegetation response</div>
</div>
""",
        unsafe_allow_html=True,
    )

with kpi2:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">Stable / Moderate Area</div>
    <div class="kpi-value">{moderate}%</div>
    <div class="kpi-note">Normal crop variation</div>
</div>
""",
        unsafe_allow_html=True,
    )

with kpi3:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">Monitoring Required</div>
    <div class="kpi-value">{low}%</div>
    <div class="kpi-note">Lower relative vegetation response</div>
</div>
""",
        unsafe_allow_html=True,
    )

with kpi4:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">Priority Scouting Zones</div>
    <div class="kpi-value">{len(zones_df)}</div>
    <div class="kpi-note">Top-ranked visual zones</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# LANDING INSIGHT SECTION
# =====================================================

left_intro, right_intro = st.columns([1.15, 1])

with left_intro:
    st.markdown(
        f"""
<div class="landing-card">
    <div class="landing-card-title">Executive Field Insight</div>
    <div class="landing-card-text">
        The surveyed field shows visible crop vigor variation across multiple blocks.
        Green regions indicate stronger vegetation response, while yellow/orange regions
        indicate areas that should be prioritized for ground verification.
        <br><br>
        The dashboard has identified <b>{len(zones_df)} top priority scouting zones</b>
        from the rendered NDVI visualization. These zones can guide field visits,
        irrigation checks, pest observations, and intervention planning.
    </div>
    <div class="confidence-tag">Decision-support output · Ground verification recommended</div>
</div>
""",
        unsafe_allow_html=True,
    )

with right_intro:
    st.markdown("#### Field Preview")
    st.image(Image.open(preview_path), use_container_width=True)
    st.caption("Rendered NDVI visualization used for visual crop vigor interpretation.")

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)

summary_col1, summary_col2 = st.columns([1.2, 1])

with summary_col1:
    st.markdown(
        f"""
<div class="insight-box">
<b>Key Finding:</b> The field displays non-uniform vegetation response, with a mix of high-vigor,
stable/moderate, and monitoring-required areas.
</div>

<div class="insight-box">
<b>Scouting Priority:</b> {len(zones_df)} priority zones were identified based on visual
low-vigor concentration. These zones should be verified on-ground before making intervention decisions.
</div>

<div class="insight-box">
<b>Operational Value:</b> The dashboard helps convert drone NDVI visualization into a clear
decision-support workflow for farm inspection, scouting, and corrective action planning.
</div>
""",
        unsafe_allow_html=True,
    )

with summary_col2:
    fig_summary = px.bar(
        summary_df,
        x="Class",
        y="Approx Share (%)",
        text="Approx Share (%)",
        title="Crop Vigor Distribution",
    )
    fig_summary.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_summary.update_layout(
        height=380,
        xaxis_title="",
        yaxis_title="Approx Share (%)",
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=40),
    )
    st.plotly_chart(fig_summary, use_container_width=True)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Field Overview",
        "Health Classification",
        "Scouting Priorities",
        "Action Plan",
        "Downloads",
    ]
)

# =====================================================
# TAB 1: FIELD OVERVIEW
# =====================================================

with tab1:
    st.markdown(
        '<div class="section-header">Original NDVI Visualization Map</div>',
        unsafe_allow_html=True,
    )

    st.image(Image.open(preview_path), use_container_width=True)

    st.caption(
        "Green regions represent stronger relative vegetation vigor. "
        "Yellow/orange regions represent lower relative vegetation response requiring field observation."
    )

    st.markdown(
        """
<div class="method-note">
<b>Interpretation:</b> This map is a rendered NDVI visualization. It is suitable for visual crop vigor
interpretation and scouting prioritization. Exact NDVI value calculations require raw single-band NDVI data.
</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================
# TAB 2: HEALTH CLASSIFICATION
# =====================================================

with tab2:
    left, right = st.columns([1.35, 1])

    with left:
        st.markdown(
            '<div class="section-header">Classified Crop Health Map</div>',
            unsafe_allow_html=True,
        )
        st.image(Image.open(classified_path), use_container_width=True)
        st.caption(
            "This map simplifies the rendered NDVI visualization into crop vigor categories."
        )

    with right:
        st.markdown(
            '<div class="section-header">Crop Vigor Share</div>',
            unsafe_allow_html=True,
        )

        fig = px.pie(
            summary_df,
            values="Approx Share (%)",
            names="Class",
            hole=0.45,
            title="Visual Crop Health Share",
        )
        fig.update_layout(height=420, margin=dict(l=10, r=10, t=60, b=10))
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(summary_df, use_container_width=True, hide_index=True)

# =====================================================
# TAB 3: SCOUTING PRIORITIES
# =====================================================

with tab3:
    st.markdown(
        '<div class="section-header">Priority Scouting Zone Map</div>',
        unsafe_allow_html=True,
    )

    st.image(Image.open(annotated_path), use_container_width=True)

    st.caption(
        "The marked zones are the top visual low-vigor concentration areas. "
        "They should be used for field scouting and ground verification."
    )

    st.markdown(
        '<div class="section-header">Zone-Wise Scouting Table</div>',
        unsafe_allow_html=True,
    )

    if len(zones_df) > 0:
        st.dataframe(zones_df, use_container_width=True, hide_index=True)
    else:
        st.success(
            "No major priority scouting zones were detected using the current visual threshold."
        )

# =====================================================
# TAB 4: ACTION PLAN
# =====================================================

with tab4:
    st.markdown(
        '<div class="section-header">AI-Assisted Agronomic Interpretation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
Based on the rendered NDVI visualization, the field shows the following relative crop vigor distribution:

- **High vigor area:** {high}%
- **Stable / moderate vigor area:** {moderate}%
- **Monitoring required / low relative vigor area:** {low}%
- **Mixed / transitional area:** {mixed}%

### Priority Observations

The yellow/orange-toned regions should be considered **monitoring-required zones**.
These areas may indicate lower vegetation response due to irrigation variation, nutrient imbalance,
pest pressure, disease symptoms, soil variation, or crop-stage differences.
"""
    )

    st.markdown("### Suggested Field Action")

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        st.markdown(
            """
<div class="action-card">
<b>1. Ground Verification</b><br>
Visit the top priority scouting zones marked on the map and verify actual crop condition.
</div>

<div class="action-card">
<b>2. Irrigation Check</b><br>
Check soil moisture, water distribution, drainage issues, and irrigation uniformity.
</div>

<div class="action-card">
<b>3. Crop Stand Observation</b><br>
Inspect plant density, crop stage variation, yellowing, wilting, or patchy growth.
</div>
""",
            unsafe_allow_html=True,
        )

    with action_col2:
        st.markdown(
            """
<div class="action-card">
<b>4. Pest / Disease Inspection</b><br>
Observe leaf symptoms, pest pressure, disease patterns, and localized damage.
</div>

<div class="action-card">
<b>5. Nutrient Assessment</b><br>
Compare visual symptoms with nutrient deficiency patterns and soil history.
</div>

<div class="action-card">
<b>6. Follow-Up Survey</b><br>
Conduct a second drone survey after corrective action to monitor improvement.
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("### Next Upgrade Recommendation")

    st.markdown(
        """
For advanced reporting, the system can further support:

- Raw single-band NDVI GeoTIFF integration
- Field boundary-based area calculation
- RGB orthomosaic overlay
- Flight metadata and GSD-based reporting
- Time-series crop health comparison
- Prescription and intervention mapping
"""
    )

# =====================================================
# TAB 5: DOWNLOADS
# =====================================================

with tab5:
    st.markdown(
        '<div class="section-header">Download Dashboard Outputs</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "These outputs can be shared with the field team, client, or agronomist for review and follow-up planning."
    )

    download_files = [
        ("Crop Health Summary CSV", summary_path),
        ("Priority Scouting Zones CSV", zones_path),
        ("Classified Crop Health Map", classified_path),
        ("Annotated Priority Zones Map", annotated_path),
        ("NDVI Web Preview", preview_path),
    ]

    if methodology_path.exists():
        download_files.append(("Methodology Note", methodology_path))

    for label, path in download_files:
        with open(path, "rb") as f:
            st.download_button(
                label=f"Download {label}",
                data=f,
                file_name=path.name,
                mime="application/octet-stream",
            )

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
<div class="footer-note">
Generated from drone-based rendered NDVI visualization data.
Outputs are designed for visual interpretation, scouting prioritization, and client demo reporting.
</div>
""",
    unsafe_allow_html=True,
)