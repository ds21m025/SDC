import pandas as pd
import numpy as np
import datetime
import os

import json
import requests

import streamlit as st
import altair as alt
from vega_datasets import data


# Display container version
# ==============================================================================
container_version = None
if os.path.isfile('./container_version.txt'):
    with open('./container_version.txt') as f:
        container_version = f.readline().strip()
if container_version is None or len(container_version) == 0:
    container_version = "not available"

version_text = st.sidebar.text(f"container version:\n{container_version}\n ")
# ==============================================================================


# Declare progress and status elements
# ==============================================================================
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
# ==============================================================================


# Define ISO country codes (2-letter, 3-letter, and numeric)
# ==============================================================================
country_codes = pd.DataFrame(
    columns=['cc_a3', 'cc_a2', 'cc_num', 'country'], 
    dtype='string',
    data=[('ABW', 'AW', 533, 'Aruba'), ('AFG', 'AF', 4, 'Afghanistan'), ('AGO', 'AO', 24, 'Angola'), ('AIA', 'AI', 660, 'Anguilla'), ('ALB', 'AL', 8, 'Albania'), ('AND', 'AD', 20, 'Andorra'), ('ARE', 'AE', 784, 'United Arab Emirates'), ('ARG', 'AR', 32, 'Argentina'), ('ARM', 'AM', 51, 'Armenia'), ('ASM', 'AS', 16, 'American Samoa'), ('ATG', 'AG', 28, 'Antigua and Barbuda'), ('AUS', 'AU', 36, 'Australia'), ('AUT', 'AT', 40, 'Austria'), ('AZE', 'AZ', 31, 'Azerbaijan'), ('BDI', 'BI', 108, 'Burundi'), ('BEL', 'BE', 56, 'Belgium'), ('BEN', 'BJ', 204, 'Benin'), ('BFA', 'BF', 854, 'Burkina Faso'), ('BGD', 'BD', 50, 'Bangladesh'), ('BGR', 'BG', 100, 'Bulgaria'), ('BHR', 'BH', 48, 'Bahrain'), ('BHS', 'BS', 44, 'Bahamas'), ('BIH', 'BA', 70, 'Bosnia and Herzegovina'), ('BLM', 'BL', 652, 'Saint Barthélemy'), ('BLR', 'BY', 112, 'Belarus'), ('BLZ', 'BZ', 84, 'Belize'), ('BMU', 'BM', 60, 'Bermuda'), ('BOL', 'BO', 68, 'Bolivia (Plurinational State of)'), ('BRA', 'BR', 76, 'Brazil'), ('BRB', 'BB', 52, 'Barbados'), ('BRN', 'BN', 96, 'Brunei Darussalam'), ('BTN', 'BT', 64, 'Bhutan'), ('BWA', 'BW', 72, 'Botswana'), ('CAF', 'CF', 140, 'Central African Republic'), ('CAN', 'CA', 124, 'Canada'), ('CHE', 'CH', 756, 'Switzerland'), ('CHL', 'CL', 152, 'Chile'), ('CHN', 'CN', 156, 'China'), ('CIV', 'CI', 384, "Côte d'Ivoire"), ('CMR', 'CM', 120, 'Cameroon'), ('COD', 'CD', 180, 'Congo, Democratic Republic of the'), ('COG', 'CG', 178, 'Congo'), ('COK', 'CK', 184, 'Cook Islands'), ('COL', 'CO', 170, 'Colombia'), ('COM', 'KM', 174, 'Comoros'), ('CPV', 'CV', 132, 'Cabo Verde'), ('CRI', 'CR', 188, 'Costa Rica'), ('CUB', 'CU', 192, 'Cuba'), ('CUW', 'CW', 531, 'Curaçao'), ('CYM', 'KY', 136, 'Cayman Islands'), ('CYP', 'CY', 196, 'Cyprus'), ('CZE', 'CZ', 203, 'Czechia'), ('DEU', 'DE', 276, 'Germany'), ('DJI', 'DJ', 262, 'Djibouti'), ('DMA', 'DM', 212, 'Dominica'), ('DNK', 'DK', 208, 'Denmark'), ('DOM', 'DO', 214, 'Dominican Republic'), ('DZA', 'DZ', 12, 'Algeria'), ('ECU', 'EC', 218, 'Ecuador'), ('EGY', 'EG', 818, 'Egypt'), ('ERI', 'ER', 232, 'Eritrea'), ('ESP', 'ES', 724, 'Spain'), ('EST', 'EE', 233, 'Estonia'), ('ETH', 'ET', 231, 'Ethiopia'), ('FIN', 'FI', 246, 'Finland'), ('FJI', 'FJ', 242, 'Fiji'), ('FLK', 'FK', 238, 'Falkland Islands (Malvinas)'), ('FRA', 'FR', 250, 'France'), ('FRO', 'FO', 234, 'Faroe Islands'), ('FSM', 'FM', 583, 'Micronesia (Federated States of)'), ('GAB', 'GA', 266, 'Gabon'), ('GBR', 'GB', 826, 'United Kingdom of Great Britain and Northern Ireland'), ('GEO', 'GE', 268, 'Georgia'), ('GGY', 'GG', 831, 'Guernsey'), ('GHA', 'GH', 288, 'Ghana'), ('GIB', 'GI', 292, 'Gibraltar'), ('GIN', 'GN', 324, 'Guinea'), ('GLP', 'GP', 312, 'Guadeloupe'), ('GMB', 'GM', 270, 'Gambia'), ('GNB', 'GW', 624, 'Guinea-Bissau'), ('GNQ', 'GQ', 226, 'Equatorial Guinea'), ('GRC', 'GR', 300, 'Greece'), ('GRD', 'GD', 308, 'Grenada'), ('GRL', 'GL', 304, 'Greenland'), ('GTM', 'GT', 320, 'Guatemala'), ('GUF', 'GF', 254, 'French Guiana'), ('GUM', 'GU', 316, 'Guam'), ('GUY', 'GY', 328, 'Guyana'), ('HND', 'HN', 340, 'Honduras'), ('HRV', 'HR', 191, 'Croatia'), ('HTI', 'HT', 332, 'Haiti'), ('HUN', 'HU', 348, 'Hungary'), ('IDN', 'ID', 360, 'Indonesia'), ('IMN', 'IM', 833, 'Isle of Man'), ('IND', 'IN', 356, 'India'), ('IRL', 'IE', 372, 'Ireland'), ('IRN', 'IR', 364, 'Iran (Islamic Republic of)'), ('IRQ', 'IQ', 368, 'Iraq'), ('ISL', 'IS', 352, 'Iceland'), ('ISR', 'IL', 376, 'Israel'), ('ITA', 'IT', 380, 'Italy'), ('JAM', 'JM', 388, 'Jamaica'), ('JEY', 'JE', 832, 'Jersey'), ('JOR', 'JO', 400, 'Jordan'), ('JPN', 'JP', 392, 'Japan'), ('KAZ', 'KZ', 398, 'Kazakhstan'), ('KEN', 'KE', 404, 'Kenya'), ('KGZ', 'KG', 417, 'Kyrgyzstan'), ('KHM', 'KH', 116, 'Cambodia'), ('KIR', 'KI', 296, 'Kiribati'), ('KNA', 'KN', 659, 'Saint Kitts and Nevis'), ('KOR', 'KR', 410, 'Korea, Republic of'), ('KWT', 'KW', 414, 'Kuwait'), ('LAO', 'LA', 418, "Lao People's Democratic Republic"), ('LBN', 'LB', 422, 'Lebanon'), ('LBR', 'LR', 430, 'Liberia'), ('LBY', 'LY', 434, 'Libya'), ('LCA', 'LC', 662, 'Saint Lucia'), ('LIE', 'LI', 438, 'Liechtenstein'), ('LKA', 'LK', 144, 'Sri Lanka'), ('LSO', 'LS', 426, 'Lesotho'), ('LTU', 'LT', 440, 'Lithuania'), ('LUX', 'LU', 442, 'Luxembourg'), ('LVA', 'LV', 428, 'Latvia'), ('MAF', 'MF', 663, 'Saint Martin (French part)'), ('MAR', 'MA', 504, 'Morocco'), ('MCO', 'MC', 492, 'Monaco'), ('MDA', 'MD', 498, 'Moldova, Republic of'), ('MDG', 'MG', 450, 'Madagascar'), ('MDV', 'MV', 462, 'Maldives'), ('MEX', 'MX', 484, 'Mexico'), ('MHL', 'MH', 584, 'Marshall Islands'), ('MKD', 'MK', 807, 'North Macedonia'), ('MLI', 'ML', 466, 'Mali'), ('MLT', 'MT', 470, 'Malta'), ('MMR', 'MM', 104, 'Myanmar'), ('MNE', 'ME', 499, 'Montenegro'), ('MNG', 'MN', 496, 'Mongolia'), ('MNP', 'MP', 580, 'Northern Mariana Islands'), ('MOZ', 'MZ', 508, 'Mozambique'), ('MRT', 'MR', 478, 'Mauritania'), ('MSR', 'MS', 500, 'Montserrat'), ('MTQ', 'MQ', 474, 'Martinique'), ('MUS', 'MU', 480, 'Mauritius'), ('MWI', 'MW', 454, 'Malawi'), ('MYS', 'MY', 458, 'Malaysia'), ('MYT', 'YT', 175, 'Mayotte'), ('NCL', 'NC', 540, 'New Caledonia'), ('NER', 'NE', 562, 'Niger'), ('NGA', 'NG', 566, 'Nigeria'), ('NIC', 'NI', 558, 'Nicaragua'), ('NIU', 'NU', 570, 'Niue'), ('NLD', 'NL', 528, 'Netherlands'), ('NOR', 'NO', 578, 'Norway'), ('NPL', 'NP', 524, 'Nepal'), ('NRU', 'NR', 520, 'Nauru'), ('NZL', 'NZ', 554, 'New Zealand'), ('OMN', 'OM', 512, 'Oman'), ('PAK', 'PK', 586, 'Pakistan'), ('PAN', 'PA', 591, 'Panama'), ('PCN', 'PN', 612, 'Pitcairn'), ('PER', 'PE', 604, 'Peru'), ('PHL', 'PH', 608, 'Philippines'), ('PLW', 'PW', 585, 'Palau'), ('PNG', 'PG', 598, 'Papua New Guinea'), ('POL', 'PL', 616, 'Poland'), ('PRI', 'PR', 630, 'Puerto Rico'), ('PRK', 'KP', 408, "Korea (Democratic People's Republic of)"), ('PRT', 'PT', 620, 'Portugal'), ('PRY', 'PY', 600, 'Paraguay'), ('PSE', 'PS', 275, 'Palestine, State of'), ('PYF', 'PF', 258, 'French Polynesia'), ('QAT', 'QA', 634, 'Qatar'), ('REU', 'RE', 638, 'Réunion'), ('ROU', 'RO', 642, 'Romania'), ('RUS', 'RU', 643, 'Russian Federation'), ('RWA', 'RW', 646, 'Rwanda'), ('SAU', 'SA', 682, 'Saudi Arabia'), ('SDN', 'SD', 729, 'Sudan'), ('SEN', 'SN', 686, 'Senegal'), ('SGP', 'SG', 702, 'Singapore'), ('SHN', 'SH', 654, 'Saint Helena, Ascension and Tristan da Cunha'), ('SLB', 'SB', 90, 'Solomon Islands'), ('SLE', 'SL', 694, 'Sierra Leone'), ('SLV', 'SV', 222, 'El Salvador'), ('SMR', 'SM', 674, 'San Marino'), ('SOM', 'SO', 706, 'Somalia'), ('SPM', 'PM', 666, 'Saint Pierre and Miquelon'), ('SRB', 'RS', 688, 'Serbia'), ('SSD', 'SS', 728, 'South Sudan'), ('STP', 'ST', 678, 'Sao Tome and Principe'), ('SUR', 'SR', 740, 'Suriname'), ('SVK', 'SK', 703, 'Slovakia'), ('SVN', 'SI', 705, 'Slovenia'), ('SWE', 'SE', 752, 'Sweden'), ('SWZ', 'SZ', 748, 'Eswatini'), ('SXM', 'SX', 534, 'Sint Maarten (Dutch part)'), ('SYC', 'SC', 690, 'Seychelles'), ('SYR', 'SY', 760, 'Syrian Arab Republic'), ('TCA', 'TC', 796, 'Turks and Caicos Islands'), ('TCD', 'TD', 148, 'Chad'), ('TGO', 'TG', 768, 'Togo'), ('THA', 'TH', 764, 'Thailand'), ('TJK', 'TJ', 762, 'Tajikistan'), ('TKL', 'TK', 772, 'Tokelau'), ('TKM', 'TM', 795, 'Turkmenistan'), ('TLS', 'TL', 626, 'Timor-Leste'), ('TON', 'TO', 776, 'Tonga'), ('TTO', 'TT', 780, 'Trinidad and Tobago'), ('TUN', 'TN', 788, 'Tunisia'), ('TUR', 'TR', 792, 'Türkiye'), ('TUV', 'TV', 798, 'Tuvalu'), ('TZA', 'TZ', 834, 'Tanzania, United Republic of'), ('UGA', 'UG', 800, 'Uganda'), ('UKR', 'UA', 804, 'Ukraine'), ('URY', 'UY', 858, 'Uruguay'), ('USA', 'US', 840, 'United States of America'), ('UZB', 'UZ', 860, 'Uzbekistan'), ('VAT', 'VA', 336, 'Holy See'), ('VCT', 'VC', 670, 'Saint Vincent and the Grenadines'), ('VEN', 'VE', 862, 'Venezuela (Bolivarian Republic of)'), ('VGB', 'VG', 92, 'Virgin Islands (British)'), ('VIR', 'VI', 850, 'Virgin Islands (U.S.)'), ('VNM', 'VN', 704, 'Viet Nam'), ('VUT', 'VU', 548, 'Vanuatu'), ('WLF', 'WF', 876, 'Wallis and Futuna'), ('WSM', 'WS', 882, 'Samoa'), ('YEM', 'YE', 887, 'Yemen'), ('ZAF', 'ZA', 710, 'South Africa'), ('ZMB', 'ZM', 894, 'Zambia'), ('ZWE', 'ZW', 716, 'Zimbabwe'), ('TWN', 'TW', 158, 'Taiwan'), ('ESH', 'EH', 732, 'Western Sahara'), ('NAM', 'NA', 516, 'Namibia'), ('ATF', 'TF', 260, 'French Southern Territories'), ('BES', 'BQ', 535, 'Bonaire, Sint Eustatius and Saba')]
)
# ==============================================================================


# Load and cache COVID-19 data from the internet
# ==============================================================================
@st.cache
def load_data():
    status_text.text("Loading data...\n ")

    # Geometry data for world map
    world_map = alt.topo_feature(data.world_110m.url, "countries")
    progress_bar.progress(2)

    # Our World in Data
    status_text.text("Loading data from\nOur World in Data...")
    owid = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    progress_bar.progress(30)

    owid = owid[[
        "iso_code", 
        "date",
        "new_cases_smoothed", 
        "new_deaths_smoothed", 
        "total_cases_per_million", 
        "total_deaths_per_million", 
        "new_tests", 
        "total_tests_per_thousand", 
        "new_people_vaccinated_smoothed", 
        "people_vaccinated", 
        "people_vaccinated_per_hundred", 
        "people_fully_vaccinated_per_hundred", 
        "life_expectancy",
        "human_development_index",
        "population"
    ]]

    owid_cum = owid[['iso_code', 'total_cases_per_million', 'total_deaths_per_million', 'total_tests_per_thousand', 'people_vaccinated_per_hundred', 'life_expectancy', 'human_development_index', 'population']]
    owid_cum = owid_cum.groupby('iso_code').max()    
    owid_cum = pd.merge(owid_cum, country_codes, how='inner', left_on='iso_code', right_on='cc_a3')
    progress_bar.progress(40)

    # WHO
    status_text.text("Loading data from\nWHO...")
    who_cases = pd.read_csv("https://covid19.who.int/WHO-COVID-19-global-data.csv")
    progress_bar.progress(60)
    who_vaccs = pd.read_csv("https://covid19.who.int/who-data/vaccination-data.csv")
    progress_bar.progress(80)

    # Global Health Observatory
    status_text.text("Loading data from\nGlobal Health Observatory...")
    gho_life_expectancy = requests.get("https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=TimeDim eq 2019 and Dim1 eq 'BTSX'")
    gho_life_expectancy = json.loads(gho_life_expectancy.text)
    gho_life_expectancy = [(v['SpatialDim'], v['NumericValue']) for v in gho_life_expectancy['value']]
    gho_life_expectancy = pd.DataFrame(gho_life_expectancy, columns=['cc_a3', 'life_expectancy'])
    progress_bar.progress(100)

    return (world_map, owid, owid_cum, who_cases, who_vaccs, gho_life_expectancy)


(world_map, owid, owid_cum, who_cases, who_vaccs, gho_life_expectancy) = load_data()

status_text.text("Data fully loaded.\n ")
progress_bar.empty()
# ==============================================================================


# Declare interactive selection elements in sidebar
# ==============================================================================
fig_of_interest = st.sidebar.radio(
    "Figure of interest for world map",
    ("COVID-19 cases", "COVID-19 deaths", "COVID-19 tests", "people vaccinated")
)

country_of_interest = st.sidebar.selectbox(
    "Country of interest for time series",
    list(country_codes['country']),
    index = int(np.where(country_codes['country'] == "Austria")[0][0])
)
# fields are: 'cc_a3', 'cc_a2', 'cc_num', 'country'
country = country_codes.loc[country_codes['country'] == country_of_interest].to_dict('records')[0]

min_date = min(owid[owid['iso_code'] == country['cc_a3']]["date"])
min_date = datetime.date(*[int(d) for d in min_date.split('-')])
max_date = max(owid[owid['iso_code'] == country['cc_a3']]["date"])
max_date = datetime.date(*[int(d) for d in max_date.split('-')])
start_date = st.sidebar.date_input("Start of time series", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End of time series", value=max_date, min_value=min_date, max_value=max_date)

# Streamlit widgets automatically run the script from top to bottom. Since this
# button is not connected to any other logic, it just causes a plain rerun.
st.sidebar.button("Re-run")
# ==============================================================================


# Title of HTML main page
# ==============================================================================
st.title("Interactive COVID-19 Dashboard")


# World chart
# ==============================================================================
if fig_of_interest == "COVID-19 cases":
    world_field = "total_cases_per_million"
    world_title = "Reported COVID-19 cases per million people"

elif fig_of_interest == "COVID-19 deaths":
    world_field = "total_deaths_per_million"
    world_title = "Reported COVID-19 deaths per million people"

elif fig_of_interest == "COVID-19 tests":
    world_field = "total_tests_per_thousand"
    world_title = "Reported COVID-19 tests per thousand people"

elif fig_of_interest == "people vaccinated":
    world_field = "people_vaccinated_per_hundred"
    world_title = "Percentage of vaccincated people"

c1 = st.container()
c1.header(world_title)

world_chart_background = alt.Chart(world_map).mark_geoshape(fill="lightgray", stroke="white")

world_chart_foreground = (
    alt.Chart(world_map)
    .mark_geoshape(stroke="black", strokeWidth=0.15)
    .encode(
        color=alt.Color(
            f"{world_field}:Q", 
            scale=alt.Scale(scheme="lightgreyred"), 
            legend=alt.Legend(title="")
        ),
        tooltip=[
            alt.Tooltip("country:N", title="Country"),
            alt.Tooltip("total_cases_per_million:Q", title="cases per million"),
            alt.Tooltip("total_deaths_per_million:Q", title="deaths per million"),
            alt.Tooltip("total_tests_per_thousand:Q", title="tests per thousand"),            
            alt.Tooltip("people_vaccinated_per_hundred:Q", title="vaccincated people per hundred"),
        ],
    )
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(
            owid_cum, 
            "cc_num", 
            ["total_cases_per_million", "total_deaths_per_million", "total_tests_per_thousand", "people_vaccinated_per_hundred", "country"]
        ),
    )
)

world_chart = (
    (world_chart_background + world_chart_foreground)
    .configure_view(strokeWidth=0)
    .properties(width=710, height=400)
    .project("naturalEarth1")
)
st.altair_chart(world_chart)
# ==============================================================================


# Detailed charts for country of interest
# ==============================================================================
c2 = st.container()
c2.header(f"Details for {country['country']}")

# country filter for owid dataframe
filter = (owid['iso_code'] == country['cc_a3']) & (owid['date'] >= str(start_date)) & (owid['date'] <= str(end_date))
owid_filter = owid[filter]
# Prepare vaccination percentages
owid_vacc = owid_filter[['date']][(owid_filter['people_vaccinated_per_hundred'] >= 0) & (owid_filter['people_fully_vaccinated_per_hundred'] >= 0)]
owid_vacc['fully vaccinated'] = owid_filter['people_fully_vaccinated_per_hundred']
owid_vacc['partly vaccinated'] = owid_filter['people_vaccinated_per_hundred'] - owid_filter['people_fully_vaccinated_per_hundred']
owid_vacc['not vaccinated'] = 100 - owid_filter['people_vaccinated_per_hundred']

col1, col2 = st.columns(2)
with col1:
    st.subheader("Daily COVID-19 cases")
    st.line_chart(owid_filter, x='date', y='new_cases_smoothed')    
with col2:
    st.subheader("Daily COVID-19 deaths")
    st.line_chart(owid_filter, x='date', y='new_deaths_smoothed')

c3 = st.container()
st.subheader("Percentage of vaccinated people")
st.area_chart(owid_vacc, x='date', y=['fully vaccinated', 'partly vaccinated', 'not vaccinated'])
    
