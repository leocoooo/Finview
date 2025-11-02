"""
Graphiques d'analyse et de comparaison du portfolio
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import streamlit as st
from .config import TRANSACTION_COLORS, TRANSACTION_LABELS, AVAILABLE_BENCHMARKS
from .layouts import get_base_layout
from .history import get_portfolio_monthly_history


def create_monthly_transactions_chart(df_history):
    """
    Crée un graphique professionnel des transactions par mois et type
    
    Args:
        df_history: DataFrame contenant l'historique des transactions avec colonnes 'date' et 'type'
    
    Returns:
        go.Figure: Graphique Plotly
    """
    # Prepare data
    df_copy = df_history.copy()
    df_copy['month'] = pd.to_datetime(df_copy['date']).dt.to_period('M').astype(str)
    monthly_transactions = df_copy.groupby(['month', 'type']).size().reset_index(name='count')
    
    # Apply labels
    monthly_transactions['type_label'] = monthly_transactions['type'].map(TRANSACTION_LABELS)
    
    # Create chart
    fig = px.bar(
        monthly_transactions, 
        x='month', 
        y='count', 
        color='type_label',
        title="Transaction Evolution by Month",
        labels={
            'month': 'Month', 
            'count': 'Number of transactions', 
            'type_label': 'Transaction type'
        },
        color_discrete_map={TRANSACTION_LABELS[k]: v for k, v in TRANSACTION_COLORS.items()},
        custom_data=['type_label']
    )
    
    # Customize chart
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#374151'),
        title=dict(
            font=dict(size=18, color='#1f2937', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='#e5e7eb',
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f3f4f6',
            showline=False,
            tickfont=dict(size=11)
        ),
        legend=dict(
            title=dict(text='Transaction type', font=dict(size=12)),
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02,
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            borderwidth=0
        ),
        hovermode='x unified',
        bargap=0.15,
        bargroupgap=0.1
    )
    
    # Improve tooltips
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>Count: %{y}<extra></extra>'
    )
    
    return fig


def create_financial_portfolio_vs_benchmark_chart(portfolio, benchmark_ticker="^FCHI", benchmark_name="CAC40"):
    """
    Graphique comparant le portfolio (sans immobilier) à un benchmark choisi
    
    Args:
        portfolio: Instance de Portfolio
        benchmark_ticker: Le ticker Yahoo Finance (ex: "^FCHI", "^DJI", "^GSPC", "BTC-USD")
        benchmark_name: Le nom à afficher (ex: "CAC40", "Dow Jones", "S&P 500", "Bitcoin")
        
    Returns:
        go.Figure: Graphique Plotly
    """
    df = get_portfolio_monthly_history(portfolio)
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
        return fig

    # Filtrer pour exclure l'immobilier
    dates = df["date"]
    values_no_real_estate = df["value"] - df.get("real_estate_value", 0)

    # Récupérer les données du benchmark
    benchmark_series = None
    try:
        ticker = yf.Ticker(benchmark_ticker)

        # Convertir explicitement en datetime
        start_date = pd.to_datetime(dates.iloc[0])
        end_date = pd.to_datetime(dates.iloc[-1])

        # Ajouter des marges
        start_date = start_date - pd.Timedelta(days=30)
        end_date = end_date + pd.Timedelta(days=1)

        # Récupérer les données
        benchmark_hist = ticker.history(start=start_date, end=end_date)

        # Supprimer la timezone pour éviter les erreurs de comparaison
        if benchmark_hist.index.tz is not None:
            benchmark_hist.index = benchmark_hist.index.tz_localize(None)

        print(f"📥 Lignes reçues: {len(benchmark_hist)}")

        if len(benchmark_hist) > 0:
            # Aligner avec les dates du portfolio
            benchmark_values = []
            for date in dates:
                date_pd = pd.to_datetime(date)
                # Trouver la date la plus proche (avant ou le jour même)
                mask = benchmark_hist.index <= date_pd
                if mask.any():
                    closest_idx = benchmark_hist.index[mask][-1]
                    benchmark_values.append(benchmark_hist.loc[closest_idx, 'Close'])
                else:
                    benchmark_values.append(None)

            benchmark_series = pd.Series(benchmark_values, index=dates)
            # Remplir les valeurs manquantes
            benchmark_series = benchmark_series.ffill().bfill()
        else:
            print("⚠️ Aucune ligne reçue de yfinance")

    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    # Créer le graphique
    fig = go.Figure()

    # Benchmark (axe gauche)
    if benchmark_series is not None and not benchmark_series.empty:
        fig.add_trace(go.Scatter(
            x=dates,
            y=benchmark_series,
            name=benchmark_name,
            line=dict(color='#F59E0B', width=2),
            yaxis='y'
        ))
    else:
        print(f"❌ Pas de trace {benchmark_name}")

    # Portfolio (axe droit)
    fig.add_trace(go.Scatter(
        x=dates,
        y=values_no_real_estate,
        name='Portfolio',
        line=dict(color='#3B82F6', width=3),
        fill='tozeroy',
        fillcolor='rgba(59,130,246,0.1)',
        yaxis='y2'
    ))

    layout = get_base_layout(" ", 400)
    layout.update({
        'xaxis_title': "Date",
        'hovermode': 'x unified',
        'yaxis': dict(
            title=dict(text=f'{benchmark_name}', font=dict(color='#F59E0B')),
            tickfont=dict(color='#F59E0B'),
            side='left'
        ),
        'yaxis2': dict(
            title=dict(text='Financial Portfolio value (€)', font=dict(color='#3B82F6')),
            tickfont=dict(color='#3B82F6'),
            overlaying='y',
            side='right'
        ),
        'legend': dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        'margin': dict(l=60, r=60, t=50, b=40)
    })
    fig.update_layout(**layout)

    return fig


def render_portfolio_comparison(portfolio):
    """
    Interface Streamlit pour afficher la comparaison avec sélection du benchmark
    
    Args:
        portfolio: Instance de Portfolio
    """
    # Selectbox pour choisir le benchmark
    selected_benchmark = st.selectbox(
        "Choosing a comparison benchmark",
        options=list(AVAILABLE_BENCHMARKS.keys()),
        index=0  # CAC 40 par défaut
    )
    
    # Récupérer le ticker correspondant
    ticker = AVAILABLE_BENCHMARKS[selected_benchmark]
    
    # Créer et afficher le graphique
    fig = create_financial_portfolio_vs_benchmark_chart(
        portfolio, 
        benchmark_ticker=ticker,
        benchmark_name=selected_benchmark
    )
    
    st.plotly_chart(fig)
