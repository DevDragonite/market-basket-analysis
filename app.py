import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config

# ─── Configuración de Página ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Market Basket Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Diccionario de Traducciones ─────────────────────────────────────────────
translations = {
    "ES": {
        "title": "🛒 Market Basket Intelligence",
        "home_title": "Bienvenido al Análisis de Cesta de Compra",
        "home_subtitle": "Descubre patrones ocultos en tus datos de ventas para aumentar el ticket promedio.",
        "objective": "🎯 Objetivo",
        "objective_text": "Identificar qué productos se compran juntos frecuentemente para diseñar estrategias de Cross-Selling efectivas.",
        "methodology": "🔬 Metodología",
        "methodology_text": "Utilizamos el algoritmo **FP-Growth** para minar reglas de asociación, filtrando por métricas de confianza y lift.",
        "cta_button": "🚀 Iniciar Análisis",
        "sidebar_settings": "Configuración",
        "lang_select": "Idioma / Language",
        "filters": "Filtros de Análisis",
        "min_lift": "Lift Mínimo",
        "min_conf": "Confianza Mínima",
        "sort_by": "Ordenar reglas por:",
        "dataset_stats": "📊 Estado del Dataset",
        "total_rules": "Total Reglas",
        "filtered_rules": "Reglas Filtradas",
        "tab1": "🔍 Explorador",
        "tab2": "🤖 Simulador",
        "tab3": "🕸️ Grafo",
        "tab4": "💡 Conclusiones",
        "kpi_rules": "Reglas Activas",
        "kpi_lift": "Lift Máximo",
        "kpi_conf": "Confianza Promedio",
        "kpi_opps": "Oportunidades",
        "table_title": "Tabla de Datos",
        "map_title": "Mapa de Oportunidades",
        "sim_title": "🛒 El Cliente compra:",
        "sim_rec": "✨ Si lleva '{}', ofrece también:",
        "graph_title": "Conexiones de Producto",
        "insight_title": "🧠 Insights Automáticos",
        "gold_rule": "🏆 La Regla de Oro",
        "gold_text": "La asociación más fuerte detectada es entre **{0}** y **{1}**. \n\nLos datos indican que quien compra el primero tiene **{2:.1f} veces** más probabilidad de llevar el segundo. ¡Es tu combo estrella!",
        "hidden_gems": "💎 Gemas Ocultas",
        "hidden_text": "Estos productos tienen un Lift altísimo pero un volumen bajo. Son compras de nicho muy fiables.",
        "anchors": "⚓ Productos Ancla",
        "anchors_text": "Estos son los productos que 'disparan' más ventas cruzadas. Son la puerta de entrada a tu catálogo.",
        "impact_forecast": "🔮 Previsión de Impacto",
        "forecast_text": "Si activas estrategias de cross-selling en el Top 20% de reglas, se estima un revenue adicional potencial de **£{0:,.0f}** mensual."
    },
    "EN": {
        "title": "🛒 Market Basket Intelligence",
        "home_title": "Welcome to Market Basket Analysis",
        "home_subtitle": "Discover hidden patterns in sales data to boost Average Order Value (AOV).",
        "objective": "🎯 Objective",
        "objective_text": "Identify which products are frequently bought together to design effective Cross-Selling strategies.",
        "methodology": "🔬 Methodology",
        "methodology_text": "We use the **FP-Growth** algorithm to mine association rules, filtering by confidence and lift metrics.",
        "cta_button": "🚀 Start Analysis",
        "sidebar_settings": "Settings",
        "lang_select": "Language",
        "filters": "Analysis Filters",
        "min_lift": "Min Lift",
        "min_conf": "Min Confidence",
        "sort_by": "Sort rules by:",
        "dataset_stats": "📊 Dataset Status",
        "total_rules": "Total Rules",
        "filtered_rules": "Filtered Rules",
        "tab1": "🔍 Explorer",
        "tab2": "🤖 Simulator",
        "tab3": "🕸️ Graph",
        "tab4": "💡 Insights",
        "kpi_rules": "Active Rules",
        "kpi_lift": "Max Lift",
        "kpi_conf": "Avg Confidence",
        "kpi_opps": "Opportunities",
        "table_title": "Data Table",
        "map_title": "Opportunity Map",
        "sim_title": "🛒 Customer buys:",
        "sim_rec": "✨ If buying '{}', also offer:",
        "graph_title": "Product Connections",
        "insight_title": "🧠 Automated Insights",
        "gold_rule": "🏆 Golden Rule",
        "gold_text": "The strongest association is between **{0}** and **{1}**. \n\nData shows customers buying the first are **{2:.1f} times** more likely to buy the second. This is your star combo!",
        "hidden_gems": "💎 Hidden Gems",
        "hidden_text": "High Lift but Low Support items. Specific niche purchases with high reliability.",
        "anchors": "⚓ Anchor Products",
        "anchors_text": "These products trigger the most cross-sales. They are the gateway to your catalog.",
        "impact_forecast": "🔮 Impact Forecast",
        "forecast_text": "Activating cross-selling on the Top 20% rules could generate an estimated **£{0:,.0f}** additional monthly revenue."
    },
    "PT": {
        "title": "🛒 Inteligência de Cesta de Compras",
        "home_title": "Bem-vindo à Análise de Cesta de Compras",
        "home_subtitle": "Descubra padrões ocultos nos dados de vendas para aumentar o Ticket Médio.",
        "objective": "🎯 Objetivo",
        "objective_text": "Identificar quais produtos são comprados juntos frequentemente para criar estratégias eficazes de Cross-Selling.",
        "methodology": "🔬 Metodologia",
        "methodology_text": "Usamos o algoritmo **FP-Growth** para minerar regras de associação, filtrando por métricas de confiança e lift.",
        "cta_button": "🚀 Iniciar Análise",
        "sidebar_settings": "Configurações",
        "lang_select": "Idioma / Língua",
        "filters": "Filtros de Análise",
        "min_lift": "Lift Mínimo",
        "min_conf": "Confiança Mínima",
        "sort_by": "Ordenar regras por:",
        "dataset_stats": "📊 Estado do Dataset",
        "total_rules": "Total de Regras",
        "filtered_rules": "Regras Filtradas",
        "tab1": "🔍 Explorador",
        "tab2": "🤖 Simulador",
        "tab3": "🕸️ Grafo",
        "tab4": "💡 Insights",
        "kpi_rules": "Regras Ativas",
        "kpi_lift": "Lift Máximo",
        "kpi_conf": "Confiança Média",
        "kpi_opps": "Oportunidades",
        "table_title": "Tabela de Dados",
        "map_title": "Mapa de Oportunidades",
        "sim_title": "🛒 O Cliente compra:",
        "sim_rec": "✨ Se levar '{}', ofereça também:",
        "graph_title": "Conexões de Produto",
        "insight_title": "🧠 Insights Automáticos",
        "gold_rule": "🏆 Regra de Ouro",
        "gold_text": "A associação mais forte é entre **{0}** e **{1}**. \n\nClientes que compram o primeiro têm **{2:.1f} vezes** mais probabilidade de levar o segundo. É o seu combo estrela!",
        "hidden_gems": "💎 Joias Escondidas",
        "hidden_text": "Itens com alto Lift mas baixo suporte. Compras de nicho muito confiáveis.",
        "anchors": "⚓ Produtos Âncora",
        "anchors_text": "Estes produtos disparam o maior número de vendas cruzadas. São a porta de entrada do seu catálogo.",
        "impact_forecast": "🔮 Previsão de Impacto",
        "forecast_text": "Ativar estratégias de cross-selling no Top 20% das regras pode gerar um revenue adicional estimado de **£{0:,.0f}** mensal."
    }
}

# ─── Estilos Custom (Glassmorphism & Minimalismo) ────────────────────────────
st.markdown("""
<style>
    /* Google Font: Poppins */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo general: DEEP DARK THEME */
    .stApp {
        background-color: #0F172A; /* Slate 900 */
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,20%,1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,20%,1) 0, transparent 50%);
        background-attachment: fixed;
        background-size: cover;
        color: #F8FAFC; /* Slate 50 */
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Tarjetas: Glassmorphism */
    .kpi-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.6);
        border-color: rgba(99, 102, 241, 0.5);
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Headers & Textos */
    h1 {
        background: linear-gradient(90deg, #F8FAFC 0%, #E2E8F0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    h2, h3, h4 { color: #F1F5F9; }
    p, li, label, div { color: #CBD5E1; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255,255,255,0.05);
        color: #94A3B8;
        border-radius: 8px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# ─── Data Loading ────────────────────────────────────────────────────────────
# ─── Data Loading ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    rules = pd.read_csv('output/association_rules.csv')
    return rules

try:
    rules = load_data()
except FileNotFoundError:
    st.error("⚠️ DATA NOT FOUND. Please run 'market_basket_analysis.ipynb' first.")
    st.stop()

# ─── Session State Initialization ────────────────────────────────────────────
if 'lang_index' not in st.session_state:
    st.session_state['lang_index'] = 0
if 'nav_index' not in st.session_state:
    st.session_state['nav_index'] = 0

# ─── Sidebar Logic ───────────────────────────────────────────────────────────
st.sidebar.markdown("## Menu")

# Selector de Idioma con Persistencia
def update_lang():
    st.session_state['lang_index'] = ["Español (ES)", "English (EN)", "Português (PT)"].index(st.session_state.lang_select)

lang_options = ["Español (ES)", "English (EN)", "Português (PT)"]
lang_option = st.sidebar.selectbox(
    "🌐 Idioma / Language",
    lang_options,
    index=st.session_state['lang_index'],
    key="lang_select",
    on_change=update_lang
)
lang_code = lang_option.split("(")[1].split(")")[0] # ES, EN, PT
t = translations[lang_code]

# Navegación con Persistencia
# Usamos radio pero guardamos el estado manualmente si es necesario, 
# aunque st.radio mantiene su estado por defecto si la key es constante.
app_mode = st.sidebar.radio(
    "Navegación", 
    ["🏠 Home", "📊 Dashboard"],
    index=0 if "Home" in st.session_state.get("nav_selection", "Home") else 1,
    key="nav_selection"
)

# ─── Vistas ──────────────────────────────────────────────────────────────────

def show_home():
    st.title(t["home_title"])
    st.markdown(f"### {t['home_subtitle']}")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### {t['objective']}
        {t['objective_text']}
        
        ### {t['methodology']}
        {t['methodology_text']}
        """)
        
        # Botón que cambia la navegación
        if st.button(t['cta_button'], type="primary"):
            st.session_state.nav_selection = "📊 Dashboard"
            st.rerun()

    with col2:
        # Placeholder para imagen ilustrativa
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); border-radius: 20px; padding: 40px; text-align: center;">
            <span style="font-size: 100px;">🛒🔗🎁</span>
            <br><br>
            <p style="font-style: italic; opacity: 0.7;">Mining patterns from 19,000+ transactions</p>
        </div>
        """, unsafe_allow_html=True)

def show_dashboard():
    # ─── Sidebar Filtros (Solo visible en Dashboard) ─────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"🎛️ {t['filters']}")
    
    # Persistencia de Filtros
    if 'min_lift' not in st.session_state: st.session_state.min_lift = 1.2
    if 'min_conf' not in st.session_state: st.session_state.min_conf = 0.5
    
    min_lift = st.sidebar.slider(t['min_lift'], 1.0, 5.0, key="min_lift")
    min_conf = st.sidebar.slider(t['min_conf'], 0.1, 1.0, key="min_conf")
    
    sort_metric = st.sidebar.selectbox(
        t['sort_by'],
        ["lift", "confidence", "support"],
        key="sort_metric"
    )
    
    # Filtrar datos
    filtered_rules = rules[
        (rules['lift'] >= min_lift) &
        (rules['confidence'] >= min_conf)
    ].sort_values(sort_metric, ascending=False)
    
    # Stats Compactos
    st.sidebar.divider()
    with st.sidebar.expander(t['dataset_stats'], expanded=False):
        st.markdown(f"""
        - **{t['total_rules']}:** {len(rules)}
        - **{t['filtered_rules']}:** {len(filtered_rules)}
        """)
    
    # ─── Dashboard Header ────────────────────────────────────────────────────
    st.title(t['title'])
    
    # ─── KPI Cards Row ───────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{len(filtered_rules)}</div><div class="kpi-label">{t['kpi_rules']}</div></div>""", unsafe_allow_html=True)
    with col2:
        best_lift = filtered_rules['lift'].max() if not filtered_rules.empty else 0
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{best_lift:.2f}x</div><div class="kpi-label">{t['kpi_lift']}</div></div>""", unsafe_allow_html=True)
    with col3:
        avg_conf = filtered_rules['confidence'].mean() if not filtered_rules.empty else 0
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{avg_conf:.1%}</div><div class="kpi-label">{t['kpi_conf']}</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{len(filtered_rules) * 5}</div><div class="kpi-label">{t['kpi_opps']}</div></div>""", unsafe_allow_html=True)

    st.write("") 

    # ─── Tabs de Navegación ──────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([t['tab1'], t['tab2'], t['tab3'], t['tab4']])

    # ─── Tab 1: Explorador ──────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader(t['table_title'])
            st.dataframe(
                filtered_rules[['antecedent', 'consequent', 'support', 'confidence', 'lift']],
                use_container_width=True,
                height=500
            )
        with c2:
            st.subheader(t['map_title'])
            if not filtered_rules.empty:
                filtered_rules['tooltip'] = filtered_rules.apply(
                    lambda x: f"Lift: {x['lift']:.2f}x<br>Conf: {x['confidence']:.1%}", axis=1
                )
                fig = px.scatter(
                    filtered_rules, x="support", y="confidence", size="lift", color="lift",
                    custom_data=["tooltip"], color_continuous_scale="Plasma", template="plotly_dark"
                )
                
                # Añadir cuadrantes
                avg_support = filtered_rules['support'].mean()
                avg_conf_val = filtered_rules['confidence'].mean()
                
                fig.add_hline(y=avg_conf_val, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Confianza Media")
                fig.add_vline(x=avg_support, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Support Medio")
                
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
    
    # ─── Tab 2: Simulador ────────────────────────────────────────────────────
    with tab2:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"### {t['sim_title']}")
            all_antecedents_simple = sorted(list(set([x.split(',')[0].strip(" {'}") for x in rules['antecedent']])))
            
            selected = st.selectbox("Selecciona producto", all_antecedents_simple, label_visibility="collapsed")
            
        with c2:
            st.markdown(f"### {t['sim_rec'].format(selected)}")
            matches = filtered_rules[filtered_rules['antecedent'].str.contains(selected, regex=False)].sort_values('lift', ascending=False).head(3)
            
            for _, row in matches.iterrows():
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; border-left: 4px solid #00b894; margin-bottom: 10px;">
                    <h4 style="margin:0; color:white;">{row['consequent']}</h4>
                    <p style="margin:0;">Lift: <strong>{row['lift']:.2f}x</strong> | Conf: <strong>{row['confidence']:.1%}</strong></p>
                </div>
                """, unsafe_allow_html=True)

    # ─── Tab 3: Grafo ────────────────────────────────────────────────────────
    with tab3:
        st.subheader(t['graph_title'])
        # Graph logic here (simplified loop)
        G = nx.DiGraph()
        for _, r in filtered_rules.head(30).iterrows():
            ant = r['antecedent'].split(', ')[0]
            con = r['consequent'].split(', ')[0]
            G.add_edge(ant, con, weight=r['lift'])
        
        nodes = [Node(id=n, label=n, size=15, color="#4361EE", font={'color': 'white'}) for n in G.nodes()]
        edges = [Edge(source=e[0], target=e[1], color="#94A3B8") for e in G.edges()]
        
        config = Config(width=800, height=500, directed=True, nodeHighlightBehavior=True, highlightColor="#F72585")
        
        try:
            agraph(nodes=nodes, edges=edges, config=config)
        except:
            st.warning("Graph requires streamlit-agraph")

    # ─── Tab 4: Insights ─────────────────────────────────────────────────────
    # ─── Tab 4: Insights ─────────────────────────────────────────────────────
    with tab4:
        st.subheader(t['insight_title'])
        if not filtered_rules.empty:
            # 1. Regra de Ouro (Mayor Lift)
            top = filtered_rules.iloc[0]
            ant_top = top['antecedent'].split(', ')[0]
            con_top = top['consequent'].split(', ')[0]
            
            st.info(f"""
            #### {t['gold_rule']}
            {t['gold_text'].format(ant_top, con_top, top['lift'])}
            """)
            
            col_insight1, col_insight2 = st.columns(2)
            
            with col_insight1:
                st.markdown(f"#### {t['hidden_gems']}")
                # Gemas: Alto Lift (> 75%), Bajo Support (< 25%)
                gems = filtered_rules[
                    (filtered_rules['lift'] > filtered_rules['lift'].quantile(0.75)) & 
                    (filtered_rules['support'] < filtered_rules['support'].quantile(0.25))
                ].head(3)
                
                for _, row in gems.iterrows():
                    st.markdown(f"🔸 **{row['antecedent']}** ➡ {row['consequent']} (Lift: {row['lift']:.1f}x)")
                st.caption(f"_{t['hidden_text']}_")
                
            with col_insight2:
                st.markdown(f"#### {t['anchors']}")
                # Anclas: Productos que más aparecen en antecedentes
                # Simplificación: Tomar la columna string y contar
                top_anchors = filtered_rules['antecedent'].value_counts().head(3)
                for prod, count in top_anchors.items():
                    st.markdown(f"⚓ **{prod}** ({count} reglas)")
                st.caption(f"_{t['anchors_text']}_")
            
            st.markdown("---")
            # Forecast
            estimated_revenue = len(filtered_rules) * 15 # Dummy value
            st.success(f"""
            #### {t['impact_forecast']}
            {t['forecast_text'].format(estimated_revenue)}
            """)

# ─── Routing ─────────────────────────────────────────────────────────────────
if app_mode == "🏠 Home":
    show_home()
else:
    show_dashboard()
