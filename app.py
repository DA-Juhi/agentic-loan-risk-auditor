import pandas as pd
import os

def run_agentic_audit(file_path):
    print("🚀 [Conquer AI Auditor] Initializing pipeline...")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found. Please place the dataset in this folder.")
        return

    # Ingest Portfolio Data
    df = pd.read_csv(file_path)
    print(f"📊 Successfully ingested {len(df):,} portfolio records.")

    # 1. Baseline Financial Analytics
    total_disbursed = float(df['loan_amount'].sum())
    total_collected = float(df['total_payment'].sum())
    net_portfolio_profit = total_collected - total_disbursed

    # 2. Legacy Process Failure Telemetry (Human-Verified Portfolio Breakdown)
    verified_mask = df['verification_status'] == 'Verified'
    charged_off_mask = df['loan_status'] == 'Charged Off'
    
    legacy_verified_defaults = int(df[verified_mask & charged_off_mask].shape[0])
    legacy_capital_loss = float(df[verified_mask & charged_off_mask]['loan_amount'].sum())

    # 3. Autonomous AI Risk Agent Decision Engine Matrix
    # Vectorized policy check matching the identified human blind spots
    high_leverage_risk = (df['Loan-to-Income Ratio'] > 0.25) & (df['dti'] > 0.14)
    debt_overload_risk = df['dti'] > 0.22
    installment_strain_risk = (df['Installment-to-Income'] > 10.0) & (df['int_rate'] > 0.15)

    # Flag records matching our automated criteria
    df['ai_action'] = 'Approve'
    df.loc[high_leverage_risk, 'ai_action'] = 'Deny (High Leverage)'
    df.loc[debt_overload_risk & (df['ai_action'] == 'Approve'), 'ai_action'] = 'Deny (Debt Overload)'
    df.loc[installment_strain_risk & (df['ai_action'] == 'Approve'), 'ai_action'] = 'Deny (Installment Strain)'

    # 4. Simulation & Impact Metrics Calculation
    ai_denied_mask = df['ai_action'].str.startswith('Deny')
    ai_intercepted_defaults = int(df[ai_denied_mask & charged_off_mask].shape[0])
    capital_protected = float(df[ai_denied_mask & charged_off_mask]['loan_amount'].sum())
    
    # Calculate operational optimization percentage
    efficiency_gain = (ai_intercepted_defaults / legacy_verified_defaults) * 100 if legacy_verified_defaults > 0 else 0

    print("⚡ Simulation complete. Generating UI payloads...")

    # Compile data into JSON strings to inject dynamically into the dashboard
    metrics = {
        "portfolio_size": f"{len(df):,}",
        "net_profit": f"${net_portfolio_profit:,.2f}",
        "legacy_loss": f"${legacy_capital_loss:,.2f}",
        "capital_saved": f"${capital_protected:,.2f}",
        "intercepted_count": f"{ai_intercepted_defaults:,}",
        "efficiency_gain": f"{efficiency_gain:.1f}%"
    }

    generate_dashboard(metrics)

def generate_dashboard(metrics):
    template_path = os.path.join(os.path.dirname(__file__), 'template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    for key, value in metrics.items():
        html = html.replace(f'{{{{{key}}}}}', value)

    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✨ Production dashboard file successfully generated: [dashboard.html]")

if __name__ == "__main__":
    run_agentic_audit('Finance_loan_dataset.csv')