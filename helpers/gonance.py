import pandas as pd

def normalize_ledger_df(df: pd.DataFrame) -> pd.DataFrame:
	df_out = df
	df_out['Investment Gross'] = df_out['Investment Gross'].str.replace(r"€",'')
	df_out['Investment Gross'] = df_out['Investment Gross'].str.replace(r",",'')
	df_out['Value'] = df_out['Value'].str.replace(r"€",'')
	df_out['Value'] = df_out['Value'].str.replace(r",",'')
	df_out['Investment Gross'] = df_out['Investment Gross'].astype(float)
	df_out['Value'] = df_out['Value'].astype(float)
	df_out['Date'] = pd.to_datetime(df_out['Date'])
	df_out['Year'] = df_out['Date'].dt.year
	df_out['Month'] = df_out['Date'].dt.month
	return (df_out)

def investment_by_period(df:pd.DataFrame, index:str, period:str) -> pd.DataFrame:
	df_out = df
	if period == 'year':
		df_out = df_out.pivot_table(index='Product', columns='Year', 
			values='Investment Gross', aggfunc='sum')
		return df_out
	if period == 'quarter':
		df_out = df_out.pivot_table(index='Product', columns=['Quarter'], 
			values='Investment Gross', aggfunc='sum')
		df_out['Total Investment'] = df_out.sum(axis=1)
		return df_out

	else:
		return None

def value_by_period(df:pd.DataFrame, index:str, period:str) -> pd.DataFrame:
	df_out = df
	if period == 'year':
		df_out = df_out.pivot_table(index='Product', columns='Year', 
			values='Value', aggfunc='sum')
		return df_out
	if period == 'quarter':
		df_out = df_out.pivot_table(index='Product', columns=['Quarter'], 
			values='Value', aggfunc='sum')
		return df_out

	else:
		return None

def enhance_historical(df:pd.DataFrame) -> pd.DataFrame:
	df_out = df
	df_out['Returns'] = df_out['20Q2_value'] - df_out['Total Investment']
	df_out['Returns %'] = df_out['Returns'] / df_out['Total Investment']
	return df_out