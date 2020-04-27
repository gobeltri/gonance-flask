import pandas as pd

def normalize_ledger_df(df: pd.DataFrame) -> pd.DataFrame:
	df_out = df
	df_out['Investment Gross'] = df_out['Investment Gross'].str.replace(r"€",'')
	df_out['Investment Gross'] = df_out['Investment Gross'].str.replace(r",",'')
	df_out['Investment Gross'] = df_out['Investment Gross'].astype(float)
	df_out['Value'] = df_out['Value'].str.replace(r"€",'')
	df_out['Value'] = df_out['Value'].str.replace(r",",'')
	df_out['Value'] = df_out['Value'].astype(float)
	df_out['Date'] = pd.to_datetime(df_out['Date'])
	df_out['Year'] = df_out['Date'].dt.year
	df_out['Month'] = df_out['Date'].dt.month
	return (df_out)


def figure_by_group_and_period(df:pd.DataFrame, figure:str, group:str, period:str) -> pd.DataFrame:

	"""
	figures_accepted = ['Investment Gross', 'Shares', 'Fees', 'Tax', 'Investment Netto', 'Value']
	groups_accepted = ['Category #1', 'Category #2', 'Broker', 'Market', 'Product']
	periods_accepted = ['Year', 'Quarter']
	"""

	df_out = df

	df_out = df_out.pivot_table(index=group, columns=period, 
		values=figure, aggfunc='sum')

	if figure == 'Investment Gross':
		df_out['Total Investment'] = df_out.sum(axis=1)

	return df_out



def enhance_historical(df:pd.DataFrame) -> pd.DataFrame:
	df_out = df

	df_out['Allocation'] = df_out['20Q2_value'] / df_out['20Q2_value'].sum(axis=0)
	df_out['Delta Last-Y'] = df_out['20Q2_value'] / df_out['19Q2_value'] - 1
	df_out['Delta Last-Q'] = df_out['20Q2_value'] / df_out['20Q1_value'] - 1

	df_out['Returns'] = df_out['20Q2_value'] - df_out['Total Investment']
	df_out['Returns %'] = df_out['Returns'] / df_out['Total Investment']

	df_out = df_out.fillna(0.0)
	df_out = df_out.reset_index()

	return df_out


def format_historical(df:pd.DataFrame) -> pd.DataFrame:
	df_out = df

	#df_out['Allocation'] = pd.Series([round(val, 2) for val in df_out['Allocation']], index = df_out.index)
	df_out['Allocation'] = pd.Series(["{0:.2f}".format(val * 100) for val in df_out['Allocation']], index = df_out.index)

	df_out['20Q2_value'] = pd.Series([round(val, 2) for val in df_out['20Q2_value']], index = df_out.index)
	df_out['20Q2_value'] = pd.Series(["{0:.2f}".format(val) for val in df_out['20Q2_value']], index = df_out.index)

	df_out['Total Investment'] = pd.Series([round(val, 2) for val in df_out['Total Investment']], index = df_out.index)
	df_out['Total Investment'] = pd.Series(["{0:.2f}".format(val) for val in df_out['Total Investment']], index = df_out.index)

	#df_out['Delta Last-Y'] = pd.Series([round(val, 2) for val in df_out['Delta Last-Y']], index = df_out.index)
	df_out['Delta Last-Y'] = pd.Series(["{0:.2f}".format(val * 100) for val in df_out['Delta Last-Y']], index = df_out.index)

	#df_out['Delta Last-Q'] = pd.Series([round(val, 2) for val in df_out['Delta Last-Q']], index = df_out.index)
	df_out['Delta Last-Q'] = pd.Series(["{0:.2f}".format(val * 100) for val in df_out['Delta Last-Q']], index = df_out.index)

	df_out['Returns'] = pd.Series([round(val, 2) for val in df_out['Returns']], index = df_out.index)
	df_out['Returns'] = pd.Series(["{0:.2f}".format(val) for val in df_out['Returns']], index = df_out.index)

	#df_out['Returns %'] = pd.Series([round(val, 2) for val in df_out['Returns %']], index = df_out.index)
	df_out['Returns %'] = pd.Series(["{0:.2f}".format(val * 100) for val in df_out['Returns %']], index = df_out.index)

	return df_out

