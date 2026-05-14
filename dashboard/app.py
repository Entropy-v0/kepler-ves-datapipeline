import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import statsmodels.api as sm
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Kepler P2P Sentinel",
    page_icon="🛰️",
    layout="wide"
)

# Custom CSS para el look premium original
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="metric-container"] {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    [data-testid="stMetricValue"] { color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_db_engine():
    # Detecta si está en Docker o Local automáticamente
    db_host = os.getenv('DB_HOST', 'db' if os.path.exists('/.dockerenv') else 'localhost')
    
    url_object = URL.create(
        "postgresql",
        username=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASS', 'kepler2004'),
        host=db_host,
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'kepler_db'),
    )
    return create_engine(url_object)

def load_data():
    engine = get_db_engine()
    query = "SELECT * FROM p2p_ads ORDER BY timestamp DESC"
    return pd.read_sql(query, engine)

# --- HEADER ---
st.title("🛰️ Kepler P2P Market Sentinel")
st.markdown("---")

try:
    df = load_data()
    
    if df.empty:
        st.warning("No se encontraron datos en la base de datos.")
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # --- FILA 1: MÉTRICAS (Estilo Original) ---
        col1, col2, col3, col4 = st.columns(4)
        
        avg_price = df['price'].mean()
        min_price = df['price'].min()
        max_price = df['price'].max()
        total_usdt = df['available'].sum() # Usando el campo 'available' que ya tienes
        
        col1.metric("Avg Price (VES)", f"{avg_price:,.2f}")
        col2.metric("Min Price (VES)", f"{min_price:,.2f}")
        col3.metric("Max Price (VES)", f"{max_price:,.2f}")
        col4.metric("Liquidez Total", f"{total_usdt:,.0f} USDT")
        
        st.markdown("### 📈 Market Analysis")
        
        # --- FILA 2: CHARTS (Línea de Tiempo y Barras de Bancos) ---
        c1, c2 = st.columns([2, 1])
        
        with c1:
            fig_corr = px.scatter(
                df, 
                x='available', 
                y='price',
                trendline="ols",
                title="Correlación: Oferta (USDT) vs Precio (VES)",
                labels={'available': 'Stock en Venta (USDT)', 'price': 'Precio (VES)'},
                template="plotly_dark",
                color="success_rate",
                color_continuous_scale="RdYlGn",
                hover_data=['merchant', 'banks']
            )
            
            fig_corr.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Cálculo rápido del coeficiente para mostrar debajo del gráfico
            corr_value = df['price'].corr(df['available'])
            st.write(f"**Coeficiente de Correlación de Pearson:** `{corr_value:.4f}`")
            
        with c2:
            # Bank Distribution Original
            all_banks = df['banks'].str.split(', ').explode()
            bank_counts = all_banks.value_counts().head(10)
            
            fig_banks = px.bar(
                x=bank_counts.index, 
                y=bank_counts.values,
                title="Top Payment Methods",
                labels={'x': 'Bank', 'y': 'Ads Count'},
                template="plotly_dark",
                color_discrete_sequence=["#58a6ff"]
            )
            st.plotly_chart(fig_banks, use_container_width=True)
            
        # --- FILA 3: TABLA ---
        st.markdown("### 📄 Latest Advertisements")
        st.dataframe(
            df[['timestamp', 'merchant', 'price', 'available', 'banks', 'success_rate']], 
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error(f"Error conectando a la base de datos: {e}")

# Footer
st.markdown("---")
st.caption("Kepler Project - Financial Data Science Experiments")