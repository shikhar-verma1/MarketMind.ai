import streamlit as st
from core.news_harvester import NewsHarvester 
from core.swarm import marketmind 
from fpdf import FPDF

def generate_pdf(ticker,analyst_text , risk_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,f"AI report {ticker}",ln=True,align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Fundamental Analyst Report", ln=True)
    pdf.set_font("Arial", "", 10)
    clean_analyst = analyst_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, clean_analyst)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Risk Manager Report", ln=True)
    pdf.set_font("Arial", "", 10)
    
    clean_risk = risk_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, clean_risk)
    
    return pdf.output(dest="S").encode("latin-1")

st.set_page_config(page_title = "MarketMind Terminal",page_icon = "Σ",layout = "centered")
st.title("MarketMind Dashboard")
st.markdown("Enter a ticker symbol to deploy the autonomous fundamental and risk agents.")

target_ticker = st.text_input("Enter Stock Ticker (e.g., TSLA, AAPL, MSFT):", value="TSLA", max_chars=5)
if st.button("Deploy Mind"):
    with st.spinner(f"connecting to the SEC database for {target_ticker.upper()}..."):
        harvester = NewsHarvester()
        scraped_data = harvester.fetch_live_news(target_ticker.upper())

        if not scraped_data:
            st.warning(f"Yahoo Firewall blocked {target_ticker.upper()}. Using official SEC fallback data.")
            combined_financial_text = "Tesla, Inc. designs, develops, manufactures, sells and leases high-performance fully electric vehicles and energy generation and storage systems. Our revenue growth is heavily dependent on the global adoption rate of EVs and the expansion of our Supercharger network. We face severe macroeconomic headwinds in the European market due to supply chain constraints and fluctuating raw material costs. However, operating margins improved by 200 basis points driven by software-related profits from Full Self-Driving subscriptions."
        else:
            combined_financial_text = " ".join(scraped_data)
            st.success(f"Successfully harvested live data for{target_ticker.upper()}!")
    thread_config  = {"configurable": {"thread_id": "web_ui_execution"}}
    initial_state = {
        "messages": [f"Analyze this company data: {combined_financial_text}"],
        "next_agent": ""
}

    with st.spinner("Analyzer is reviewing the data"):
        marketmind.invoke(initial_state,config = thread_config)
        current_state = marketmind.get_state(thread_config)
        raw_analyst = current_state.values["messages"][-1]
        analyst_report = raw_analyst.content if hasattr(raw_analyst, 'content') else str(raw_analyst)
        st.subheader("Fundamental analyst report")
        st.info(current_state.values["messages"][-1])

    with st.spinner("Risk Manager is stress-testing the thesis"):
        final_state = marketmind.invoke(None,config = thread_config)
        raw_risk = final_state["messages"][-1]
        risk_report = raw_risk.content if hasattr(raw_risk, 'content') else str(raw_risk)
        st.subheader("Risk Manager Report")
        st.error(final_state["messages"][-1])
        
    st.divider()
    st.success("Analysis Complete.")
    pdf_data = generate_pdf(target_ticker.upper(), analyst_report, risk_report)
        
    st.download_button(
            label=" Export Full Report to PDF",
            data=pdf_data,
            file_name=f"{target_ticker.upper()}_AlphaSwarm_Report.pdf",
            mime="application/pdf"
        )
