import pandas as pd
from datetime import datetime

class ExcelWriter:
    def save_to_excel(self, transactions: list, output_path: str):
        try:
            df = pd.DataFrame(transactions)
            if df.empty:
                print("Warning: No transactions found")
                return
            # Convert date strings to proper Excel date format (DD/MM/YYYY)
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
            # Visual date grouping: blank out repeated dates
            df['Date'] = df['Date'].mask(df['Date'].eq(df['Date'].shift()))
            # Clean up amounts (remove ₹ symbol and convert to numeric)
            df['Amount_Numeric'] = pd.to_numeric(df['Amount'].str.replace('₹', '').str.replace(',', ''), errors='coerce').fillna(0)
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Transactions', index=False)
                self._create_summary_sheet(df, writer)
                self._create_category_sheet(df, writer)
        except Exception as e:
            print(f"Error in save_to_excel: {e}")
            print(f"Transactions data: {transactions}")
            raise

    def _create_summary_sheet(self, df: pd.DataFrame, writer):
        # Use only non-null dates for min/max
        date_min = df['Date'].dropna().min().strftime('%d/%m/%Y') if not df['Date'].dropna().empty else "N/A"
        date_max = df['Date'].dropna().max().strftime('%d/%m/%Y') if not df['Date'].dropna().empty else "N/A"
        summary_data = {
            'Metric': [
                'Total Transactions',
                'Total Amount',
                'Average Transaction',
                'Date Range',
                'Unique Categories',
                'Unique Merchants'
            ],
            'Value': [
                len(df),
                f"₹{df['Amount_Numeric'].sum():,.2f}",
                f"₹{df['Amount_Numeric'].mean():,.2f}",
                f"{date_min} to {date_max}",
                df['Category'].nunique(),
                df['Merchant'].nunique()
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

    def _create_category_sheet(self, df: pd.DataFrame, writer):
        category_stats = df.groupby('Category').agg({
            'Amount_Numeric': ['sum', 'count', 'mean']
        }).round(2)
        category_stats.columns = ['Total Amount', 'Transaction Count', 'Average Amount']
        category_stats = category_stats.sort_values('Total Amount', ascending=False)
        total_amount = df['Amount_Numeric'].sum()
        category_stats['Percentage'] = (category_stats['Total Amount'] / total_amount * 100).round(1)
        category_stats.to_excel(writer, sheet_name='Category Breakdown') 