<<<<<<< HEAD

# Import Libraries:
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
st.set_page_config(layout="wide",page_icon="📈")

# Read CSV Dataset:
df = pd.read_csv("cleaned_retail_store_sales.csv", parse_dates = ["Date"])

# Prepare
st.title("Retail Sales Analytics Dashboard")
st.write('Customer insights, product performance, and sales trends—all in one place')
st.divider()
tab1,tab2,tab3,tab4,tab5 = st.tabs(['Customer Behavior','Product Analysis','Sales Trend','Payment Insights','Location Analysis'])

# Sidebar Filters:
st.sidebar.title("Filter Options")

date_range = st.sidebar.multiselect("Select Year:", options= df['Year'].unique(), default=df['Year'].unique())

cat_select = st.sidebar.multiselect("Select Category:", options= df['Category'].unique(), default=df['Category'].unique())

loc_select = st.sidebar.multiselect("Select Location:", options= df['Location'].unique(), default=df['Location'].unique())

# Filters Apply:
df_filtered = df[
    (df['Year'].isin(date_range)) &
    (df['Category'].isin(cat_select)) &
    (df['Location'].isin(loc_select))
]

st.sidebar.title("Summary Statistics")
st.sidebar.metric("Total Revenue",f'${df_filtered['Total Spent'].sum():,.2F}')

st.sidebar.metric("Total Transactions",f'{df['Transaction ID'].size}')

st.sidebar.metric("Unique Customers",f'${df_filtered['Customer ID'].nunique()}')

st.sidebar.metric("Average Transaction Value",f'${df_filtered['Total Spent'].mean()}')

# Customer Behavior - Tab1:
with tab1:
    st.header("Customer Behavior & Segmentation")

    # Q1
    top_cust = df_filtered.groupby('Customer ID')['Total Spent'].sum().nlargest(10)
    fig1 = px.bar(top_cust,title='Top 10 Customers by Spendings', labels={'value':'Total Spent', 'index': 'Customer ID'},text_auto = True)
    st.plotly_chart(fig1)


    col1 , col2 = st.columns(2)
    with col1:
    # Q2:
        avg_cust = df_filtered.groupby(['Customer ID'])['Total Spent'].mean().mean()
        st.metric("Average Transaction Value per Customer", f'${avg_cust:.2f}')

    # Q3:
        repeat_cust= df_filtered['Customer ID'].value_counts().gt(1).sum()
        one_time = df_filtered['Customer ID'].nunique()- repeat_cust
        fig3= px.pie(values=[repeat_cust,one_time], names=['Repeat Customers','One-Time Customers'],title='Customer Frequency')
        st.plotly_chart(fig3)

    # Q4:
        avg_trans = df_filtered['Customer ID'].value_counts().mean()
        st.metric("Average Transaction per Customer",f'{avg_trans:.1f}')


    with col2:
    # Q5:
        category_preference = df_filtered.groupby(['Customer ID', 'Category']).size().unstack().fillna(0)
        st.dataframe(category_preference.idxmax(axis=1).value_counts().rename('Customers by Preferred Category'),use_container_width = True)

    # Q6:
        total_spending = df_filtered.groupby('Customer ID')['Total Spent'].sum()
        spending_bins = pd.qcut(total_spending, q=4 , labels = ['Q1','Q2','Q3','Q4'] )
        fig6 = px.histogram(spending_bins, title='Total Spending Distribution with Quartilies', text_auto = True)
        st.plotly_chart(fig6)

    # Q7:
    purchase_freq = df_filtered.groupby('Customer ID').size().sort_values(ascending=False).head(10)
    fig7 = px.bar(purchase_freq,labels={'value':'Number of Purchases','index':'Customer ID'},title='Top 10 Customer with Purchase Frequency', text_auto = True)
    st.plotly_chart(fig7)

    
    # Q8
    df_filtered['Transaction Date'] = pd.to_datetime(df_filtered['Transaction Date'])
    time_between = df_filtered.groupby('Customer ID')['Transaction Date'].apply(lambda x: x.sort_values().diff().mean().days).mean()
    st.metric('Average Days Between Purchases (Repeat Customers)', f'{time_between:.1f} days')

    # Q9:
    df_sorted = df_filtered.sort_values(['Customer ID','Transaction Date'])
    customer_lifetime = df_sorted.groupby('Customer ID')['Transaction Date'].agg(['min','max'])
    df_sorted = df_filtered.sort_values(['Customer ID', 'Transaction Date'])
    customer_lifetime = df_sorted.groupby('Customer ID')['Transaction Date'].agg(['min', 'max'])
    customer_lifetime['CLV (days)'] = (customer_lifetime['max'] - customer_lifetime['min']).dt.days

    top_clv = customer_lifetime['CLV (days)'].nlargest(10).reset_index()
    fig9 = px.bar(top_clv, x='Customer ID', y='CLV (days)', title='Top 10 Customers by Lifetime (in Days)',text_auto = True)
    st.plotly_chart(fig9)

    # Q10:
    method_preference = df_filtered.groupby(['Customer ID','Location']).size().unstack().fillna(0)
    method_preference['Primary Method'] = method_preference.idxmax(axis=1)
    st.dataframe(method_preference['Primary Method'].value_counts().rename('Customer by Preferred Location'), use_container_width= True)
    
    # Q11:
    total_spending = df_filtered.groupby('Customer ID')['Total Spent'].sum()
    high_spenders = total_spending[total_spending > total_spending.quantile(.9)].index
    payment_method = df_filtered[df_filtered['Customer ID'].isin(high_spenders)]['Payment Method'].value_counts(normalize=True)
    fig11 = px.pie(values=payment_method,title='Payment Methods for top 10% Spenders ',names=payment_method.axes[0],color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig11, use_container_width = True)

    # Q12:
    sorted_spendings = total_spending.sort_values(ascending=False)
    cumlative = sorted_spendings.cumsum() / sorted_spendings.sum() * 100
    result = (cumlative <= 80).sum()
    st.metric('Customers Contributing to 80% of Revenue', result)


with tab2:
    st.header('Product & Category Analysis')
    
    # Q13:
    cat_revenue = df_filtered.groupby('Category')['Total Spent'].sum().sort_values(ascending=False)
    fig13 = px.bar(cat_revenue, title = 'Revenue Per Category', labels={'value':'Total Revenue','index':'Category'},text_auto = True)
    st.plotly_chart(fig13)

    col1,col2 = st.columns(2)
    with col1:
        # Q14:
        top_selling = df_filtered.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(10)
        fig14 = px.bar(top_selling, title='Top 10 Best-Selling Items', labels={'value':'Sold Quantity','Item':'Product'}, text_auto=True )
        st.plotly_chart(fig14)

        # Q15:
        fig15 = px.scatter(df_filtered,x='Price Per Unit',y='Quantity',title='Unit Price Vs. Sales Volume',trendline='ols')
        st.plotly_chart(fig15, use_container_width = True)

    with col2:
        # Q16:
        seasons_selling = df_filtered.groupby(['Category','Season'])['Quantity'].sum().sort_values(ascending=False).unstack()
        fig16 = px.bar(seasons_selling,title='Selling Per Category Per Season',labels={'value':'Unit Sold'} ,barmode='group',text_auto=True,color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig16, use_container_width = True)
    
        # Q17:
        avg_price_cat = df_filtered.groupby('Category')['Price Per Unit'].mean().sort_values(ascending=False)
        fig17 = px.bar(avg_price_cat, title='Average Price Per Unit',labels={'value':'Average Unit Price'},text_auto=True)
        st.plotly_chart(fig17, use_container_width = True)      

    # Q18:
    avg_qty_loc =df.groupby(['Category','Location'])['Quantity'].sum().sort_values(ascending=False).unstack()
    fig18 = px.bar(avg_qty_loc,text_auto = True, barmode='group',title='Effect of Location on Sales',color_discrete_sequence=px.colors.qualitative.Pastel,labels={'value':'Unit Sold'})
    st.plotly_chart(fig18, use_container_width = True)


with tab3:
    st.header("Sales Trends & Seasonality")

    #Q19:
    month_trend = df_filtered.groupby(['Year','Month'])['Total Spent'].sum().reset_index()
    month_trend['Year-Month'] = month_trend['Year'].astype(str) + '-' +month_trend['Month'].astype(str).str.zfill(2)
    quarter_trend = df_filtered.groupby(['Year','Quarter'])['Total Spent'].sum().reset_index()
    quarter_trend['Year-Quarter'] = quarter_trend['Year'].astype(str) + '-' + quarter_trend['Quarter'].astype(str).str.zfill(2)
    fig19 = make_subplots(rows = 2, cols= 1, subplot_titles=('Monthly Revenue Trend', 'Quarterly Revenue Trend'))
    fig19.add_trace(go.Scatter(x= month_trend['Year-Month'], y= month_trend['Total Spent'], mode= 'lines+markers'),row=1, col=1)
    fig19.add_trace(go.Scatter(x=quarter_trend['Year-Quarter'], y= quarter_trend['Total Spent'], mode = 'lines+markers'), row=2, col=1)
    fig19.update_layout(height = 800, title_text= 'Revenue Trends')
    st.plotly_chart(fig19, use_container_width = True)

    col1, col2 = st.columns(2)

    with col1:

    # Q20:
        day_trend = df_filtered.groupby('Day')['Total Spent'].sum().sort_values(ascending=False)
        fig20 = px.bar(day_trend,labels={'value':'Total Spent'}, title='Revenue Per Days',text_auto= True)
        st.plotly_chart(fig20, use_container_width = True)

    #Q21:
        daily_art = df_filtered.groupby('Date')['Total Spent'].mean().reset_index()
        fig21 = px.line(daily_art, x='Date', y= 'Total Spent', title='Daily Average Revenue per Transactiom')
        st.plotly_chart(fig21, use_container_width = True)

    with col2:

    # Q22:
        week_trend = df_filtered.groupby(['Year','Week'])['Total Spent'].sum().reset_index()
        week_trend['Year-Week'] = week_trend['Year'].astype(str) + '-W' + week_trend['Week'].astype(str).str.zfill(2)
        fig22 = px.line(week_trend, x='Year-Week', y='Total Spent',title='Weekly Sales Trend')
        st.plotly_chart(fig22, use_container_width = True)

    # Q23:
        daily_sales = df_filtered.groupby('Date')['Total Spent'].sum().reset_index()
        mean_sales = daily_sales['Total Spent'].mean()
        fig23 = px.line(daily_sales, x='Date', y='Total Spent', title='Daily Sales with Outliers').add_hline(y= mean_sales, line_dash = 'dash', line_color ='red')
        st.plotly_chart(fig23, use_container_width = True)

with tab4:
    st.header("Payment Method Insight")

    #Q24:
    popular_payment_methods = df_filtered['Payment Method'].value_counts().reset_index()
    fig24 = px.pie(popular_payment_methods,names=payment_method.axes[0], title='Most Popular Payment Method', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig24, use_container_width = True)

    col1, col2 = st.columns(2)
    
    with col1:
    # Q25:
        fig25 = px.box(df_filtered, x= 'Payment Method', y='Total Spent',title = 'Total Spent Distribution by Payment Method')
        st.plotly_chart(fig25, use_container_width = True)

    # Q26:
        popular_payment_methods = df_filtered[['Payment Method','Location']].value_counts().reset_index()
        fig26 = px.bar(popular_payment_methods, x= 'Payment Method', y= 'count', color= 'Location', barmode='group',title='Payment Method Usage: Online vs In-Store' ,color_discrete_sequence=px.colors.qualitative.Pastel,text_auto=True)
        st.plotly_chart(fig26, use_container_width = True)

    with col2:
    
    # Q27:

        payment_trend = df_filtered.groupby(['Year','Month','Payment Method']).size().reset_index(name='Count')
        payment_trend['Year-Month'] = payment_trend['Year'].astype(str) + '-' + payment_trend['Month'].astype(str).str.zfill(2)
        fig27 = px.line(payment_trend,x='Year-Month', y='Count', color='Payment Method', title='Payment Method Trends Over Time',color_discrete_sequence=px.colors.qualitative.Safe)  
        st.plotly_chart(fig27, use_container_width = True)

    # Q28:
        avg_trans_method = df_filtered.groupby('Payment Method')['Total Spent'].mean()
        fig28 = px.bar(avg_trans_method,title='average transaction value by payment method',labels={'value':'Average Spent'}, text_auto=True)
        st.plotly_chart(fig28, use_container_width = True)

with tab5:
    # Q29:
    avg_location = df_filtered.groupby(['Location'])['Total Spent'].mean()
    fig29 = px.bar(avg_location,text_auto= True, title='Average Spending: Online Vs. Offline',labels={'value':'Average Transaction'})
    st.plotly_chart(fig29, use_container_width = True)

    # Q30:
    location_prefer = df_filtered.groupby(['Category','Location'])['Total Spent'].sum().sort_values(ascending=False).reset_index()
    fig30 = px.bar(location_prefer, x='Category', y= 'Total Spent',color='Location',barmode='group',text_auto=True,title='Category Popularity: Online Vs. Offline',color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig30, use_container_width = True)

    # Q31:
    loc_payment = df.groupby(['Payment Method','Location']).size().unstack()
    fig31 = px.bar(loc_payment,barmode='group',text_auto=True,title='Payment Method: Online Vs. Offline',color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig31, use_container_width = True) 

=======

# Import Libraries:
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
st.set_page_config(layout="wide",page_icon="📈")

# Read CSV Dataset:
df = pd.read_csv(r"C:\00-Shobaki\Data Science\Epsolin AI\Revive\Med_Project\Data\Cleaned\cleaned_retail_store_sales.csv", parse_dates = ["Date"])

# Prepare
st.title("Retail Sales Analytics Dashboard")
st.write('Customer insights, product performance, and sales trends—all in one place')
st.divider()
tab1,tab2,tab3,tab4,tab5 = st.tabs(['Customer Behavior','Product Analysis','Sales Trend','Payment Insights','Location Analysis'])

# Sidebar Filters:
st.sidebar.title("Filter Options")

date_range = st.sidebar.multiselect("Select Year:", options= df['Year'].unique(), default=df['Year'].unique())

cat_select = st.sidebar.multiselect("Select Category:", options= df['Category'].unique(), default=df['Category'].unique())

loc_select = st.sidebar.multiselect("Select Location:", options= df['Location'].unique(), default=df['Location'].unique())

# Filters Apply:
df_filtered = df[
    (df['Year'].isin(date_range)) &
    (df['Category'].isin(cat_select)) &
    (df['Location'].isin(loc_select))
]

st.sidebar.title("Summary Statistics")
st.sidebar.metric("Total Revenue",f'${df_filtered['Total Spent'].sum():,.2F}')

st.sidebar.metric("Total Transactions",f'{df['Transaction ID'].size}')

st.sidebar.metric("Unique Customers",f'${df_filtered['Customer ID'].nunique()}')

st.sidebar.metric("Average Transaction Value",f'${df_filtered['Total Spent'].mean()}')

# Customer Behavior - Tab1:
with tab1:
    st.header("Customer Behavior & Segmentation")

    # Q1
    top_cust = df_filtered.groupby('Customer ID')['Total Spent'].sum().nlargest(10)
    fig1 = px.bar(top_cust,title='Top 10 Customers by Spendings', labels={'value':'Total Spent', 'index': 'Customer ID'},text_auto = True)
    st.plotly_chart(fig1)


    col1 , col2 = st.columns(2)
    with col1:
    # Q2:
        avg_cust = df_filtered.groupby(['Customer ID'])['Total Spent'].mean().mean()
        st.metric("Average Transaction Value per Customer", f'${avg_cust:.2f}')

    # Q3:
        repeat_cust= df_filtered['Customer ID'].value_counts().gt(1).sum()
        one_time = df_filtered['Customer ID'].nunique()- repeat_cust
        fig3= px.pie(values=[repeat_cust,one_time], names=['Repeat Customers','One-Time Customers'],title='Customer Frequency')
        st.plotly_chart(fig3)

    # Q4:
        avg_trans = df_filtered['Customer ID'].value_counts().mean()
        st.metric("Average Transaction per Customer",f'{avg_trans:.1f}')


    with col2:
    # Q5:
        category_preference = df_filtered.groupby(['Customer ID', 'Category']).size().unstack().fillna(0)
        st.dataframe(category_preference.idxmax(axis=1).value_counts().rename('Customers by Preferred Category'),use_container_width = True)

    # Q6:
        total_spending = df_filtered.groupby('Customer ID')['Total Spent'].sum()
        spending_bins = pd.qcut(total_spending, q=4 , labels = ['Q1','Q2','Q3','Q4'] )
        fig6 = px.histogram(spending_bins, title='Total Spending Distribution with Quartilies', text_auto = True)
        st.plotly_chart(fig6)

    # Q7:
    purchase_freq = df_filtered.groupby('Customer ID').size().sort_values(ascending=False).head(10)
    fig7 = px.bar(purchase_freq,labels={'value':'Number of Purchases','index':'Customer ID'},title='Top 10 Customer with Purchase Frequency', text_auto = True)
    st.plotly_chart(fig7)

    
    # Q8
    df_filtered['Transaction Date'] = pd.to_datetime(df_filtered['Transaction Date'])
    time_between = df_filtered.groupby('Customer ID')['Transaction Date'].apply(lambda x: x.sort_values().diff().mean().days).mean()
    st.metric('Average Days Between Purchases (Repeat Customers)', f'{time_between:.1f} days')

    # Q9:
    df_sorted = df_filtered.sort_values(['Customer ID','Transaction Date'])
    customer_lifetime = df_sorted.groupby('Customer ID')['Transaction Date'].agg(['min','max'])
    df_sorted = df_filtered.sort_values(['Customer ID', 'Transaction Date'])
    customer_lifetime = df_sorted.groupby('Customer ID')['Transaction Date'].agg(['min', 'max'])
    customer_lifetime['CLV (days)'] = (customer_lifetime['max'] - customer_lifetime['min']).dt.days

    top_clv = customer_lifetime['CLV (days)'].nlargest(10).reset_index()
    fig9 = px.bar(top_clv, x='Customer ID', y='CLV (days)', title='Top 10 Customers by Lifetime (in Days)',text_auto = True)
    st.plotly_chart(fig9)

    # Q10:
    method_preference = df_filtered.groupby(['Customer ID','Location']).size().unstack().fillna(0)
    method_preference['Primary Method'] = method_preference.idxmax(axis=1)
    st.dataframe(method_preference['Primary Method'].value_counts().rename('Customer by Preferred Location'), use_container_width= True)
    
    # Q11:
    total_spending = df_filtered.groupby('Customer ID')['Total Spent'].sum()
    high_spenders = total_spending[total_spending > total_spending.quantile(.9)].index
    payment_method = df_filtered[df_filtered['Customer ID'].isin(high_spenders)]['Payment Method'].value_counts(normalize=True)
    fig11 = px.pie(values=payment_method,title='Payment Methods for top 10% Spenders ',names=payment_method.axes[0],color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig11, use_container_width = True)

    # Q12:
    sorted_spendings = total_spending.sort_values(ascending=False)
    cumlative = sorted_spendings.cumsum() / sorted_spendings.sum() * 100
    result = (cumlative <= 80).sum()
    st.metric('Customers Contributing to 80% of Revenue', result)


with tab2:
    st.header('Product & Category Analysis')
    
    # Q13:
    cat_revenue = df_filtered.groupby('Category')['Total Spent'].sum().sort_values(ascending=False)
    fig13 = px.bar(cat_revenue, title = 'Revenue Per Category', labels={'value':'Total Revenue','index':'Category'},text_auto = True)
    st.plotly_chart(fig13)

    col1,col2 = st.columns(2)
    with col1:
        # Q14:
        top_selling = df_filtered.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(10)
        fig14 = px.bar(top_selling, title='Top 10 Best-Selling Items', labels={'value':'Sold Quantity','Item':'Product'}, text_auto=True )
        st.plotly_chart(fig14)

        # Q15:
        fig15 = px.scatter(df_filtered,x='Price Per Unit',y='Quantity',title='Unit Price Vs. Sales Volume',trendline='ols')
        st.plotly_chart(fig15, use_container_width = True)

    with col2:
        # Q16:
        seasons_selling = df_filtered.groupby(['Category','Season'])['Quantity'].sum().sort_values(ascending=False).unstack()
        fig16 = px.bar(seasons_selling,title='Selling Per Category Per Season',labels={'value':'Unit Sold'} ,barmode='group',text_auto=True,color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig16, use_container_width = True)
    
        # Q17:
        avg_price_cat = df_filtered.groupby('Category')['Price Per Unit'].mean().sort_values(ascending=False)
        fig17 = px.bar(avg_price_cat, title='Average Price Per Unit',labels={'value':'Average Unit Price'},text_auto=True)
        st.plotly_chart(fig17, use_container_width = True)      

    # Q18:
    avg_qty_loc =df.groupby(['Category','Location'])['Quantity'].sum().sort_values(ascending=False).unstack()
    fig18 = px.bar(avg_qty_loc,text_auto = True, barmode='group',title='Effect of Location on Sales',color_discrete_sequence=px.colors.qualitative.Pastel,labels={'value':'Unit Sold'})
    st.plotly_chart(fig18, use_container_width = True)


with tab3:
    st.header("Sales Trends & Seasonality")

    #Q19:
    month_trend = df_filtered.groupby(['Year','Month'])['Total Spent'].sum().reset_index()
    month_trend['Year-Month'] = month_trend['Year'].astype(str) + '-' +month_trend['Month'].astype(str).str.zfill(2)
    quarter_trend = df_filtered.groupby(['Year','Quarter'])['Total Spent'].sum().reset_index()
    quarter_trend['Year-Quarter'] = quarter_trend['Year'].astype(str) + '-' + quarter_trend['Quarter'].astype(str).str.zfill(2)
    fig19 = make_subplots(rows = 2, cols= 1, subplot_titles=('Monthly Revenue Trend', 'Quarterly Revenue Trend'))
    fig19.add_trace(go.Scatter(x= month_trend['Year-Month'], y= month_trend['Total Spent'], mode= 'lines+markers'),row=1, col=1)
    fig19.add_trace(go.Scatter(x=quarter_trend['Year-Quarter'], y= quarter_trend['Total Spent'], mode = 'lines+markers'), row=2, col=1)
    fig19.update_layout(height = 800, title_text= 'Revenue Trends')
    st.plotly_chart(fig19, use_container_width = True)

    col1, col2 = st.columns(2)

    with col1:

    # Q20:
        day_trend = df_filtered.groupby('Day')['Total Spent'].sum().sort_values(ascending=False)
        fig20 = px.bar(day_trend,labels={'value':'Total Spent'}, title='Revenue Per Days',text_auto= True)
        st.plotly_chart(fig20, use_container_width = True)

    #Q21:
        daily_art = df_filtered.groupby('Date')['Total Spent'].mean().reset_index()
        fig21 = px.line(daily_art, x='Date', y= 'Total Spent', title='Daily Average Revenue per Transactiom')
        st.plotly_chart(fig21, use_container_width = True)

    with col2:

    # Q22:
        week_trend = df_filtered.groupby(['Year','Week'])['Total Spent'].sum().reset_index()
        week_trend['Year-Week'] = week_trend['Year'].astype(str) + '-W' + week_trend['Week'].astype(str).str.zfill(2)
        fig22 = px.line(week_trend, x='Year-Week', y='Total Spent',title='Weekly Sales Trend')
        st.plotly_chart(fig22, use_container_width = True)

    # Q23:
        daily_sales = df_filtered.groupby('Date')['Total Spent'].sum().reset_index()
        mean_sales = daily_sales['Total Spent'].mean()
        fig23 = px.line(daily_sales, x='Date', y='Total Spent', title='Daily Sales with Outliers').add_hline(y= mean_sales, line_dash = 'dash', line_color ='red')
        st.plotly_chart(fig23, use_container_width = True)

with tab4:
    st.header("Payment Method Insight")

    #Q24:
    popular_payment_methods = df_filtered['Payment Method'].value_counts().reset_index()
    fig24 = px.pie(popular_payment_methods,names=payment_method.axes[0], title='Most Popular Payment Method', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig24, use_container_width = True)

    col1, col2 = st.columns(2)
    
    with col1:
    # Q25:
        fig25 = px.box(df_filtered, x= 'Payment Method', y='Total Spent',title = 'Total Spent Distribution by Payment Method')
        st.plotly_chart(fig25, use_container_width = True)

    # Q26:
        popular_payment_methods = df_filtered[['Payment Method','Location']].value_counts().reset_index()
        fig26 = px.bar(popular_payment_methods, x= 'Payment Method', y= 'count', color= 'Location', barmode='group',title='Payment Method Usage: Online vs In-Store' ,color_discrete_sequence=px.colors.qualitative.Pastel,text_auto=True)
        st.plotly_chart(fig26, use_container_width = True)

    with col2:
    
    # Q27:

        payment_trend = df_filtered.groupby(['Year','Month','Payment Method']).size().reset_index(name='Count')
        payment_trend['Year-Month'] = payment_trend['Year'].astype(str) + '-' + payment_trend['Month'].astype(str).str.zfill(2)
        fig27 = px.line(payment_trend,x='Year-Month', y='Count', color='Payment Method', title='Payment Method Trends Over Time',color_discrete_sequence=px.colors.qualitative.Safe)  
        st.plotly_chart(fig27, use_container_width = True)

    # Q28:
        avg_trans_method = df_filtered.groupby('Payment Method')['Total Spent'].mean()
        fig28 = px.bar(avg_trans_method,title='average transaction value by payment method',labels={'value':'Average Spent'}, text_auto=True)
        st.plotly_chart(fig28, use_container_width = True)

with tab5:
    # Q29:
    avg_location = df_filtered.groupby(['Location'])['Total Spent'].mean()
    fig29 = px.bar(avg_location,text_auto= True, title='Average Spending: Online Vs. Offline',labels={'value':'Average Transaction'})
    st.plotly_chart(fig29, use_container_width = True)

    # Q30:
    location_prefer = df_filtered.groupby(['Category','Location'])['Total Spent'].sum().sort_values(ascending=False).reset_index()
    fig30 = px.bar(location_prefer, x='Category', y= 'Total Spent',color='Location',barmode='group',text_auto=True,title='Category Popularity: Online Vs. Offline',color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig30, use_container_width = True)

    # Q31:
    loc_payment = df.groupby(['Payment Method','Location']).size().unstack()
    fig31 = px.bar(loc_payment,barmode='group',text_auto=True,title='Payment Method: Online Vs. Offline',color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig31, use_container_width = True) 

>>>>>>> 0820cc7 (Initial commit for Streamlit app)
