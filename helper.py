import numpy as np

def fetch_mdeal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending = True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x



def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years,country
def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if specified
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals by athlete and get the top 15
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Rename columns

    # Merge with the original dataframe to get additional details
    result = medal_counts.head(15).merge(df, on='Name', how='left')

    # Select and rename columns, and drop duplicates
    result = result[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return result


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return  final_df


def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index = 'Sport',columns = 'Year',values = 'Medal',aggfunc = 'count').fillna(0)
    return pt


def most_successful_country(df, country):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if specified

    temp_df = temp_df[temp_df['region'] == country]

    # Count medals by athlete and get the top 15
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Rename columns

    # Merge with the original dataframe to get additional details
    result = medal_counts.head(10).merge(df, on='Name', how='left')

    # Select and rename columns, and drop duplicates
    result = result[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return result


def weight_v_height(df,sport):
    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    ath_df['Medal'].fillna('NO Medal', inplace=True)
    if sport != 'Overall':
     temp_df = ath_df[ath_df['Sport'] == sport]
     return temp_df
    else:
        return ath_df


def men_v_women(df):
    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    men = ath_df[ath_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = ath_df[ath_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': "Male", 'Name_y': "Female"}, inplace=True)
    final.fillna(0, inplace=True)
    return final

