import pandas as pd
import streamlit as st
import BirdData
import altair as alt

st.set_page_config(layout='centered')

#load data
birds = BirdData.Data()
data = birds.sightings

#introduction and videos
st.title('San Francisco Wild Parrot Data')
st.divider()
st.header('Introduction', divider=True)
st.markdown("Hello! On this page, you can access and view data about the San Francisco Wild Parrots! The San Francisco Wild Parrots are known for their distinctive green bodies, red colored heads, and loud calls. First making appearances in the 1990s, Psittacara erythrogenys, also known as Cherry-headed conures, are not native to San Francisco and are believed to have originated from Ecuador and Peru [(foundsf.org)](https://www.foundsf.org/index.php?title=Parrots_on_Telegraph_Hill). We'll take a closer look at the sightings of these special parrots in San Francisco." )
vid1, vid2 = st.columns(2)
with vid1:
    st.video('videos/IMG_0812.MOV')
with vid2:
    st.video('videos/IMG_0815.MOV')

#map of all data
st.header('Map of All Sightings', divider=True)
st.markdown('The data used in this project tracks sightings of the parrots around San Francisco between the years 2000 and 2024, with a total of 11,133 unique sightings! The top five locations that the parrots have been spotted most frequently can also be shown.')
#top 5 locations
most_freq = st.checkbox('Show Top 5 Locations')
if most_freq:
    st.map(birds.most_freq_loc(), size=25)
    st.dataframe(birds.most_freq_loc(), hide_index=True, use_container_width=True)
else:
    st.map(data)

#map of sightings per neighborhood
st.header('Sightings Per Neighborhood', divider=True)
st.markdown("We can also find how many times the parrots have been sighted in a given neighborhood, as well as the location they are most seen in that neighborhood. They definitely seem to favor certain neighborhoods, like Aquatic Park and Pacific Heights. Check out how often they are spotted in other neighborhoods by selecting one from the list below!")

neighborhood = st.selectbox('Pick a neighborhood:', birds.print_neighborhoods(), index=None, placeholder='Neighborhood Name')
if neighborhood is not None:
    #statistics
    sight, perc = st.columns(2)
    with sight:
        st.metric('Sightings', birds.no_in_neighborhood(neighborhood).shape[0])
    with perc:
        st.metric('Percentage of All Sightings', f"{birds.percent_of_sightings(neighborhood):.2f}%")
    most_in_neighborhood = birds.most_at_location(neighborhood)
    #top coordinates
    show_most_in_neighborhood = st.checkbox(f'Show Top Locations In {neighborhood}')
    if show_most_in_neighborhood:
        st.map(most_in_neighborhood.head(5), size=10)
    else:
        st.map(birds.no_in_neighborhood(neighborhood), size=10)
    st.dataframe(most_in_neighborhood.drop('Neighborhood', axis=1), hide_index=True, use_container_width=True)

#map and chart of sightings per season
st.header('Sightings Per Season', divider=True)
st.subheader('Season Breakdown')
#dataframe of seasonal sightings
season_df = pd.DataFrame({'Season':['Spring', 'Summer', 'Fall', 'Winter'], 
                          'Sightings': [birds.by_season('spring')[1], birds.by_season('summer')[1], birds.by_season('fall')[1], birds.by_season('winter')[1]],
                          'Percentage': [f"{birds.by_season('spring')[2]:.2f}%", f"{birds.by_season('summer')[2]:.2f}%", f"{birds.by_season('fall')[2]:.2f}%", f"{birds.by_season('winter')[2]:.2f}%"]})
#pie chart of seasonal sightings
season_pie = alt.Chart(season_df).mark_arc(innerRadius=75).encode(
        theta=alt.Theta(field="Sightings", type="quantitative"),
        color=alt.Color(field="Season", type="nominal"))
#seasonal sightings columns
season_df_col, season_chart_col = st.columns(2, vertical_alignment='center')
season_df_col.dataframe(season_df.sort_values('Sightings', ascending=False), hide_index=True, use_container_width=True)
season_chart_col.altair_chart(season_pie, use_container_width=True)
st.markdown("As shown above, there are slight variations in how often the parrots are spotted based on time of year. For the purposes of this project, we'll look at how often they're seen per season. According to the data, the spring months are when the parrots are most sighted and winter is when they're spotted the least.")

st.subheader('Mapping Season Sightings')
st.markdown('We can also map the amount of sightings per season to better visualize the differences. Make sure to look at the table below the map to see how the neighborhoods change.')
st.markdown("If you look closely, you'll notice that no matter the season, the parrots are always seen the most in the Aquatic Park neighborhood and the Pacific Heights neighborhood. However, there is a quite a bit variance with the other neighborhoods throughout the seasons. Pick a season below to check it out!")
season_list = st.selectbox('Pick a Season to View Map:', options=('Spring', 'Summer', 'Fall', 'Winter'), index=None, placeholder='Select a season...')
if season_list is not None:
    season_sightings = birds.by_season(season_list)[0]
    st.map(season_sightings)
    season_neighborhoods = pd.DataFrame(season_sightings.drop(['latitude', 'longitude'], axis=1).groupby('Neighborhood').sum())
    st.dataframe(season_neighborhoods.sort_values('Sighting Count', ascending=False), use_container_width=True)

st.header('Amount of Sightings Over Time', divider=True)
st.markdown("The data that's used for this project is pulled from several databases using research-grade observations. By looking at the graph below, it's clear that there's been in an upward trend of research-grade observations of the San Francisco parrots in recent years, especially during the years of the COVID-19 pandemic. Despite them being in San Francisco since the 1990's, not many observations of the parrots were recorded prior to 2010. Hopefully, interest in the parrots continues to grow!")
#area chart
date_df = pd.DataFrame(data).astype({'year':'str'})
sightings_over_time = date_df.drop(['day','month', 'latitude', 'longitude', 'geometry'], axis=1).groupby('year').count()
st.area_chart(sightings_over_time, x_label='Year', y_label='Amount of Sightings', color=(173, 214, 255, 0.68))

st.markdown("The amount of sightings per year can be found and mapped as well. If you go through the years, you can see that the sightings were often very few and scattered throughout the city in the early 2000s. As the amount of sightings has risen, they have been particularly concentrated around the Aquatic Park neighborhood and Pacific Heights neighborhood. Other notable concentrations of sightings are in Telegraph Hill, Corona Heights, the Financial District, the Presidio and Golden Gate Park")
st.markdown('Select a year below to see a map of the sightings for that year!')
year_sightings = st.selectbox('Pick a year:', options=sightings_over_time.index.to_list(), index=None, placeholder='Select year...')

#map of sightings per year
if year_sightings is not None:
    sightings_by_year = date_df.groupby('year')
    st.map(sightings_by_year.get_group(year_sightings), size=50)

    in_year = pd.DataFrame(sightings_by_year.get_group(year_sightings).drop(['day','month', 'latitude', 'longitude', 'geometry'], axis=1))
    st.dataframe(pd.DataFrame(in_year.value_counts()).
                 reset_index()[['name','count']].
                 rename(columns={'name': 'Neighborhood', 'count': 'Sighting Count'}),
                 hide_index=True,
                 use_container_width=True)

st.header('Conclusion', divider=True)
st.markdown("Thanks for taking the time to check out my project! This started as a way to help my partner find the local parrots because she had never seen them in her entire time living in the Bay Area. I figured that if I could find out where they spend most of their time, I could just bring her to them. What started as just a fun tool to show my partner something she's been looking for since she was a kid ended up being my first data visualization project. I hope you learned a little more about these birds than you did before!")

st.subheader('Sources')
st.write("GBIF.org (16 April 2024) GBIF Occurrence Download https://doi.org/10.15468/dl.ch87pw")
st.write('https://www.foundsf.org/index.php?title=Parrots_on_Telegraph_Hill')