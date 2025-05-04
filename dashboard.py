import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import uuid

def render_dashboard():
    """
    Render the dashboard with user reports and metrics
    """
    if not st.session_state.reports:
        st.info("Você ainda não gerou nenhum relatório. Gere seu primeiro relatório na aba 'Gerar Novo Relatório'.")
        return
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Relatórios", len(st.session_state.reports))
    with col2:
        # Count report types
        report_types = {}
        for report in st.session_state.reports:
            report_type = report['report_type_display']
            report_types[report_type] = report_types.get(report_type, 0) + 1
        
        most_common_type = max(report_types.items(), key=lambda x: x[1])[0]
        st.metric("Tipo mais comum", most_common_type)
    with col3:
        # Get the date of the most recent report
        most_recent_date = max([report['generated_date'] for report in st.session_state.reports])
        st.metric("Relatório mais recente", most_recent_date)
    
    # Display reports by type chart
    report_type_df = pd.DataFrame({
        'Tipo': list(report_types.keys()),
        'Quantidade': list(report_types.values())
    })
    
    st.subheader("Relatórios por Tipo")
    fig = px.pie(
        report_type_df, 
        values='Quantidade', 
        names='Tipo', 
        color_discrete_sequence=px.colors.sequential.Blues
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display reports table
    st.subheader("Seus Relatórios")
    
    # Create a dataframe with report details
    reports_data = []
    for report in st.session_state.reports:
        reports_data.append({
            'ID': report['id'],
            'Título': report['title'],
            'Tipo': report['report_type_display'],
            'Data de Geração': report['generated_date']
        })
    
    reports_df = pd.DataFrame(reports_data)
    
    # Display as a table with view buttons
    for i, row in reports_df.iterrows():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.write(f"**{row['Título']}**")
        with col2:
            st.write(row['Tipo'])
        with col3:
            st.write(row['Data de Geração'])
        with col4:
            if st.button("Visualizar", key=f"view_{row['ID']}"):
                # Find the report in the session state
                for report in st.session_state.reports:
                    if report['id'] == row['ID']:
                        # Set the current page to report view and store the report ID
                        st.session_state.current_report = report
                        st.session_state.current_page = "report"
                        st.rerun()
