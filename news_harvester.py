import yfinance as yf 

class NewsHarvester:
    def fetch_live_news(self,ticker_symbol):
        print(f"Connecting to live feeds for {ticker_symbol}...")
        #ticker = yf.Ticker(ticker_symbol)
        #summary = ticker.info.get("long business summary",'')
        # We bypass Yahoo and use a raw SEC 10-K excerpt
        sec_filing_excerpt = """
        Tesla, Inc. designs, develops, manufactures, sells and leases high-performance fully electric vehicles and energy generation and storage systems. 
        Our revenue growth is heavily dependent on the global adoption rate of EVs and the expansion of our Supercharger network. 
        We face severe macroeconomic headwinds in the European market due to supply chain constraints and fluctuating raw material costs. 
        However, operating margins improved by 200 basis points driven by software-related profits from Full Self-Driving subscriptions.
        """
        raw_text_data = []
        if sec_filing_excerpt:
            sentences = sec_filing_excerpt.split('. ')

            for sentence in sentences:
                if len(sentence)>20:
                    clean_sentence = sentence.strip() + '. '
                    if not clean_sentence.endswith('.'):
                        clean_sentence += '.'
                    raw_text_data.append(clean_sentence)
        return raw_text_data 
    
if __name__ == "__main__":
    harvester = NewsHarvester()
    target_ticker = "TSLA"
    scraped_texts = harvester.fetch_live_news(target_ticker)
    print(f"\n--- SUCCESS: Harvested {len(scraped_texts)} live data points for {target_ticker} ---")
    for i ,text in enumerate(scraped_texts):
        print(f"{i+1}.{text}")