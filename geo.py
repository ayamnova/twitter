'''
Geo.py
A python script to find the distribution of users and tweets across a region.
The most important method is get_geo which will find a distribution of sentiment across a geographic region and can filter them by country (default) or by state (only within the United State).

Author: Karsten Ladner
Date: 6/29/2018
Modified: 10/02/2018
'''

import sys
import carmen
from afinn import Afinn
from os.path import join as jn
from tweets import get_tweets, get_sentiment
from tweets import save_to_file as save
from tweets import load_values_from_file as load

from constants import PATH, OUT, PROC

# Constants

# A dictionary of countries and their respective three letter country code
COUNTRY_CODES = {
    "Afghanistan": "AFG",
    "Albania": "ALB",
    "Algeria": "DZA",
    "American Samoa": "ASM",
    "Andorra": "AND",
    "Angola": "AGO",
    "Anguilla": "AIA",
    "Antigua and Barbuda": "ATG",
    "Argentina": "ARG",
    "Armenia": "ARM",
    "Aruba": "ABW",
    "Australia": "AUS",
    "Austria": "AUT",
    "Azerbaijan": "AZE",
    "Bahamas": "BHM",
    "Bahrain": "BHR",
    "Bangladesh": "BGD",
    "Barbados": "BRB",
    "Belarus": "BLR",
    "Belgium": "BEL",
    "Belize": "BLZ",
    "Benin": "BEN",
    "Bermuda": "BMU",
    "Bhutan": "BTN",
    "Bolivia": "BOL",
    "Bosnia and Herzegovina": "BIH",
    "Botswana": "BWA",
    "Brazil": "BRA",
    "British Virgin Islands": "VGB",
    "Brunei": "BRN",
    "Bulgaria": "BGR",
    "Burkina Faso": "BFA",
    "Burma": "MMR",
    "Myanmar": "MMR",
    "Burundi": "BDI",
    "Cabo Verde": "CPV",
    "Cambodia": "KHM",
    "Cameroon": "CMR",
    "Canada": "CAN",
    "Cayman Islands": "CYM",
    "Central African Republic": "CAF",
    "Chad": "TCD",
    "Chile": "CHL",
    "China": "CHN",
    "Colombia": "COL",
    "Comoros": "COM",
    "Democratic Republic of the Congo": "COD",
    "Republic of the Congo": "COG",
    "Cook Islands": "COK",
    "Costa Rica": "CRI",
    "Côte d'Ivoire": "CIV",
    "Croatia": "HRV",
    "Cuba": "CUB",
    "Curacao": "CUW",
    "Cyprus": "CYP",
    "Czech Republic": "CZE",
    "Denmark": "DNK",
    "Djibouti": "DJI",
    "Dominica": "DMA",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Equatorial Guinea": "GNQ",
    "Eritrea": "ERI",
    "Estonia": "EST",
    "Ethiopia": "ETH",
    "Falkland Islands (Islas Malvinas)": "FLK",
    "Faroe Islands": "FRO",
    "Fiji": "FJI",
    "Finland": "FIN",
    "France": "FRA",
    "French Polynesia": "PYF",
    "Gabon": "GAB",
    "Gambia": "GMB",
    "Georgia": "GEO",
    "Germany": "DEU",
    "Ghana": "GHA",
    "Gibraltar": "GIB",
    "Greece": "GRC",
    "Greenland": "GRL",
    "Grenada": "GRD",
    "Guam": "GUM",
    "Guatemala": "GTM",
    "Guernsey": "GGY",
    "Guinea-Bissau": "GNB",
    "Guinea": "GIN",
    "Guyana": "GUY",
    "Haiti": "HTI",
    "Honduras": "HND",
    "Hong Kong": "HKG",
    "Hungary": "HUN",
    "Iceland": "ISL",
    "India": "IND",
    "Indonesia": "IDN",
    "Iran": "IRN",
    "Iraq": "IRQ",
    "Ireland": "IRL",
    "Isle of Man": "IMN",
    "Israel": "ISR",
    "Italy": "ITA",
    "Jamaica": "JAM",
    "Japan": "JPN",
    "Jersey": "JEY",
    "Jordan": "JOR",
    "Kazakhstan": "KAZ",
    "Kenya": "KEN",
    "Kiribati": "KIR",
    "North Korea": "PRK",
    "South Korea": "KOR",
    "Kosovo": "KSV",
    "Kuwait": "KWT",
    "Kyrgyzstan": "KGZ",
    "Laos": "LAO",
    "Latvia": "LVA",
    "Lebanon": "LBN",
    "Lesotho": "LSO",
    "Liberia": "LBR",
    "Libya": "LBY",
    "Liechtenstein": "LIE",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Macau": "MAC",
    "Macedonia": "MKD",
    "Madagascar": "MDG",
    "Malawi": "MWI",
    "Malaysia": "MYS",
    "Maldives": "MDV",
    "Mali": "MLI",
    "Malta": "MLT",
    "Marshall Islands": "MHL",
    "Mauritania": "MRT",
    "Mauritius": "MUS",
    "Mexico": "MEX",
    "Micronesia": "FSM",
    "Moldova": "MDA",
    "Monaco": "MCO",
    "Mongolia": "MNG",
    "Montenegro": "MNE",
    "Morocco": "MAR",
    "Mozambique": "MOZ",
    "Namibia": "NAM",
    "Nepal": "NPL",
    "Netherlands": "NLD",
    "New Caledonia": "NCL",
    "New Zealand": "NZL",
    "Nicaragua": "NIC",
    "Nigeria": "NGA",
    "Niger": "NER",
    "Niue": "NIU",
    "Northern Mariana Islands": "MNP",
    "Norway": "NOR",
    "Oman": "OMN",
    "Pakistan": "PAK",
    "Palau": "PLW",
    "Panama": "PAN",
    "Papua New Guinea": "PNG",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Philippines": "PHL",
    "Poland": "POL",
    "Portugal": "PRT",
    "Puerto Rico": "PRI",
    "Qatar": "QAT",
    "Romania": "ROU",
    "Russia": "RUS",
    "Rwanda": "RWA",
    "Saint Kitts and Nevis": "KNA",
    "Saint Lucia": "LCA",
    "Saint Martin": "MAF",
    "Saint Pierre and Miquelon": "SPM",
    "Saint Vincent and the Grenadines": "VCT",
    "Samoa": "WSM",
    "San Marino": "SMR",
    "São Tomé and Príncipe": "STP",
    "Saudi Arabia": "SAU",
    "Senegal": "SEN",
    "Serbia": "SRB",
    "Seychelles": "SYC",
    "Sierra Leone": "SLE",
    "Singapore": "SGP",
    "Sint Maarten": "SXM",
    "Slovakia": "SVK",
    "Slovenia": "SVN",
    "Solomon Islands": "SLB",
    "Somalia": "SOM",
    "South Africa": "ZAF",
    "South Sudan": "SSD",
    "Spain": "ESP",
    "Sri Lanka": "LKA",
    "Sudan": "SDN",
    "Suriname": "SUR",
    "Swaziland": "SWZ",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "Syria": "SYR",
    "Taiwan": "TWN",
    "Tajikistan": "TJK",
    "Tanzania": "TZA",
    "Thailand": "THA",
    "Timor-Leste": "TLS",
    "Togo": "TGO",
    "Tonga": "TON",
    "Trinidad and Tobago": "TTO",
    "Tunisia": "TUN",
    "Turkey": "TUR",
    "Turkmenistan": "TKM",
    "Tuvalu": "TUV",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States": "USA",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",
    "Vanuatu": "VUT",
    "Venezuela": "VEN",
    "Vietnam": "VNM",
    "Virgin Islands": "VGB",
    "West Bank": "WBG",
    "Yemen": "YEM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE"
    }

# A dictionary of GPS coordinates retrieved originally from a Google list and modified
COUNTRY_COORD = {
    "Andorra": (42.546245, 1.601554),
    "United Arab Emirates": (23.424076, 53.847818),
    "Afghanistan": (33.93911, 67.709953),
    "Antigua and Barbuda": (17.060816, -61.796428),
    "Anguilla": (18.220554, -63.068615),
    "Albania": (41.153332, 20.168331),
    "Armenia": (40.069099, 45.038189),
    "Netherlands Antilles": (12.226079, -69.060087),
    "Angola": (-11.202692, 17.873887),
    "Antarctica": (-75.250973, -0.071389),
    "Argentina": (-38.416097, -63.616672),
    "American Samoa": (-14.270972, -170.132217),
    "Austria": (47.516231, 14.550072),
    "Australia": (-25.274398, 133.775136),
    "Aruba": (12.52111, -69.968338),
    "Azerbaijan": (40.143105, 47.576927),
    "Bosnia and Herzegovina": (43.915886, 17.679076),
    "Barbados": (13.193887, -59.543198),
    "Bangladesh": (23.684994, 90.356331),
    "Belgium": (50.503887, 4.469936),
    "Burkina Faso": (12.238333, -1.561593),
    "Bulgaria": (42.733883, 25.48583),
    "Bahrain": (25.930414, 50.637772),
    "Burundi": (-3.373056, 29.918886),
    "Benin": (9.30769, 2.315834),
    "Bermuda": (32.321384, -64.75737),
    "Brunei": (4.535277, 114.727669),
    "Bolivia": (-16.290154, -63.588653),
    "Brazil": (-14.235004, -51.92528),
    "Bahamas": (25.03428, -77.39628),
    "The Bahamas": (25.03428, -77.39628),
    "Bhutan": (27.514162, 90.433601),
    "Bouvet Island": (-54.423199, 3.413194),
    "Botswana": (-22.328474, 24.684866),
    "Belarus": (53.709807, 27.953389),
    "Belize": (17.189877, -88.49765),
    "Canada": (56.130366, -106.346771),
    "Cabo Verde": (15.062148, -23.602730),
    "Curacao": (12.182255, -68.973617),
    "Cocos [Keeling] Islands": (-12.164165, 96.870956),
    "Congo [DRC]": (-4.038333, 21.758664),
    "Democratic Republic of the Congo": (-4.038333, 21.758664),
    "Central African Republic": (6.611111, 20.939444),
    "Congo [Republic]": (-0.228021, 15.827659),
    "Republic of the Congo": (-0.228021, 15.827659),
    "Switzerland": (46.818188, 8.227512),
    "Côte d'Ivoire": (7.539989, -5.54708),
    "Cook Islands": (-21.236736, -159.777671),
    "Chile": (-35.675147, -71.542969),
    "Cameroon": (7.369722, 12.354722),
    "China": (35.86166, 104.195397),
    "Colombia": (4.570868, -74.297333),
    "Costa Rica": (9.748917, -83.753428),
    "Cuba": (21.521757, -77.781167),
    "Cape Verde": (16.002082, -24.013197),
    "Christmas Island": (-10.447525, 105.690449),
    "Cyprus": (35.126413, 33.429859),
    "Czech Republic": (49.817492, 15.472962),
    "Germany": (51.165691, 10.451526),
    "Djibouti": (11.825138, 42.590275),
    "Denmark": (56.26392, 9.501785),
    "Dominica": (15.414999, -61.370976),
    "Dominican Republic": (18.735693, -70.162651),
    "Algeria": (28.033886, 1.659626),
    "Ecuador": (-1.831239, -78.183406),
    "Estonia": (58.595272, 25.013607),
    "Egypt": (26.820553, 30.802498),
    "Western Sahara": (24.215527, -12.885834),
    "Eritrea": (15.179384, 39.782334),
    "Spain": (40.463667, -3.74922),
    "Ethiopia": (9.145, 40.489673),
    "Finland": (61.92411, 25.748151),
    "Fiji": (-16.578193, 179.414413),
    "Falkland Islands [Islas Malvinas]": (-51.796253, -59.523613),
    "Falkland Islands (Islas Malvinas)": (-51.796253, -59.523613),
    "Micronesia": (7.425554, 150.550812),
    "Federated States of Micronesia": (7.425554, 150.550812),
    "Faroe Islands": (61.892635, -6.911806),
    "France": (46.227638, 2.213749),
    "Gabon": (-0.803689, 11.609444),
    "United Kingdom": (55.378051, -3.435973),
    "Grenada": (12.262776, -61.604171),
    "Georgia": (42.315407, 43.356892),
    "French Guiana": (3.933889, -53.125782),
    "Guernsey": (49.465691, -2.585278),
    "Ghana": (7.946527, -1.023194),
    "Gibraltar": (36.137741, -5.345374),
    "Greenland": (71.706936, -42.604303),
    "Gambia": (13.443182, -15.310139),
    "The Gambia": (13.443182, -15.310139),
    "Guinea": (9.945587, -9.696645),
    "Guadeloupe": (16.995971, -62.067641),
    "Equatorial Guinea": (1.650801, 10.267895),
    "Greece": (39.074208, 21.824312),
    "South Georgia and the South Sandwich Islands": (-54.429579, -36.587909),
    "Guatemala": (15.783471, -90.230759),
    "Guam": (13.444304, 144.793731),
    "Guinea-Bissau": (11.803749, -15.180413),
    "Guyana": (4.860416, -58.93018),
    "Gaza Strip": (31.354676, 34.308825),
    "Hong Kong": (22.396428, 114.109497),
    "Heard Island and McDonald Islands": (-53.08181, 73.504158),
    "Honduras": (15.199999, -86.241905),
    "Croatia": (45.1, 15.2),
    "Haiti": (18.971187, -72.285215),
    "Hungary": (47.162494, 19.503304),
    "Indonesia": (-0.789275, 113.921327),
    "Ireland": (53.41291, -8.24389),
    "Israel": (31.046051, 34.851612),
    "Isle of Man": (54.236107, -4.548056),
    "India": (20.593684, 78.96288),
    "British Indian Ocean Territory": (-6.343194, 71.876519),
    "Iraq": (33.223191, 43.679291),
    "Iran": (32.427908, 53.688046),
    "Iceland": (64.963051, -19.020835),
    "Italy": (41.87194, 12.56738),
    "Ivory Coast": (7.870761, -5.553105),
    "Jersey": (49.214439, -2.13125),
    "Jamaica": (18.109581, -77.297508),
    "Jordan": (30.585164, 36.238414),
    "Japan": (36.204824, 138.252924),
    "Kenya": (-0.023559, 37.906193),
    "Kyrgyzstan": (41.20438, 74.766098),
    "Cambodia": (12.565679, 104.990963),
    "Kiribati": (-3.370417, -168.734039),
    "Comoros": (-11.875001, 43.872219),
    "Saint Kitts and Nevis": (17.357822, -62.782998),
    "North Korea": (40.339852, 127.510093),
    "South Korea": (35.907757, 127.766922),
    "Kuwait": (29.31166, 47.481766),
    "Cayman Islands": (19.513469, -80.566956),
    "Kazakhstan": (48.019573, 66.923684),
    "Laos": (19.85627, 102.495496),
    "Lebanon": (33.854721, 35.862285),
    "Saint Lucia": (13.909444, -60.978893),
    "Liechtenstein": (47.166, 9.555373),
    "Sri Lanka": (7.873054, 80.771797),
    "Liberia": (6.428055, -9.429499),
    "Lesotho": (-29.609988, 28.233608),
    "Lithuania": (55.169438, 23.881275),
    "Republic of Lithuania": (55.169438, 23.881275),
    "Luxembourg": (49.815273, 6.129583),
    "Latvia": (56.879635, 24.603189),
    "Republic of Latvia": (56.879635, 24.603189),
    "Libya": (26.3351, 17.228331),
    "Morocco": (31.791702, -7.09262),
    "Monaco": (43.750298, 7.412841),
    "Moldova": (47.411631, 28.369885),
    "Montenegro": (42.708678, 19.37439),
    "Madagascar": (-18.766947, 46.869107),
    "Marshall Islands": (7.131474, 171.184478),
    "Macedonia [FYROM]": (41.608635, 21.745275),
    "Macedonia": (41.608635, 21.745275),
    "Mali": (17.570692, -3.996166),
    "Myanmar [Burma]": (21.913965, 95.956223),
    "Burma": (21.913965, 95.956223),
    "Mongolia": (46.862496, 103.846656),
    "Macau": (22.198745, 113.543873),
    "Northern Mariana Islands": (17.33083, 145.38469),
    "Martinique": (14.641528, -61.024174),
    "Mauritania": (21.00789, -10.940835),
    "Montserrat": (16.742498, -62.187366),
    "Malta": (35.937496, 14.375416),
    "Mauritius": (-20.348404, 57.552152),
    "Maldives": (3.202778, 73.22068),
    "Malawi": (-13.254308, 34.301525),
    "Mexico": (23.634501, -102.552784),
    "Malaysia": (4.210484, 101.975766),
    "Mozambique": (-18.665695, 35.529562),
    "Myanmar": (21.941131, 96.081266),
    "Namibia": (-22.95764, 18.49041),
    "New Caledonia": (-20.904305, 165.618042),
    "Niger": (17.607789, 8.081666),
    "Norfolk Island": (-29.040835, 167.954712),
    "Nigeria": (9.081999, 8.675277),
    "Nicaragua": (12.865416, -85.207229),
    "Netherlands": (52.132633, 5.291266),
    "The Netherlands": (52.132633, 5.291266),
    "Norway": (60.472024, 8.468946),
    "Nepal": (28.394857, 84.124008),
    "Nauru": (-0.522778, 166.931503),
    "Niue": (-19.054445, -169.867233),
    "New Zealand": (-40.900557, 174.885971),
    "Oman": (21.512583, 55.923255),
    "Panama": (8.537981, -80.782127),
    "Peru": (-9.189967, -75.015152),
    "French Polynesia": (-17.679742, -149.406843),
    "Papua New Guinea": (-6.314993, 143.95555),
    "Philippines": (12.879721, 121.774017),
    "Pakistan": (30.375321, 69.345116),
    "Poland": (51.919438, 19.145136),
    "Saint Pierre and Miquelon": (46.941936, -56.27111),
    "Pitcairn Islands": (-24.703615, -127.439308),
    "Puerto Rico": (18.220833, -66.590149),
    "Palestinian Territories": (31.952162, 35.233154),
    "Portugal": (39.399872, -8.224454),
    "Palau": (7.51498, 134.58252),
    "Paraguay": (-23.442503, -58.443832),
    "Qatar": (25.354826, 51.183884),
    "Réunion": (-21.115141, 55.536384),
    "Romania": (45.943161, 24.96676),
    "Serbia": (44.016521, 21.005859),
    "Russia": (61.52401, 105.318756),
    "Rwanda": (-1.940278, 29.873888),
    "Saudi Arabia": (23.885942, 45.079162),
    "Solomon Islands": (-9.64571, 160.156194),
    "Seychelles": (-4.679574, 55.491977),
    "Sudan": (12.862807, 30.217636),
    "South Sudan": (7.270041, 29.870007),
    "Sweden": (60.128161, 18.643501),
    "Singapore": (1.352083, 103.819836),
    "Saint Helena": (-24.143474, -10.030696),
    "Slovenia": (46.151241, 14.995463),
    "Svalbard and Jan Mayen": (77.553604, 23.670272),
    "Slovakia": (48.669026, 19.699024),
    "Sierra Leone": (8.460555, -11.779889),
    "San Marino": (43.94236, 12.457777),
    "Saint Martin": (18.066721, -63.051606),
    "Sint Maarten": (18.036314, -63.065967),
    "Senegal": (14.497401, -14.452362),
    "Somalia": (5.152149, 46.199616),
    "St. Lucia": (13.844800, -61.005031),
    "Suriname": (3.919305, -56.027783),
    "São Tomé and Príncipe": (0.18636, 6.613081),
    "El Salvador": (13.794185, -88.89653),
    "Syria": (34.802075, 38.996815),
    "Swaziland": (-26.522503, 31.465866),
    "Turks and Caicos Islands": (21.694025, -71.797928),
    "Chad": (15.454166, 18.732207),
    "French Southern Territories": (-49.280366, 69.348557),
    "Togo": (8.619543, 0.824782),
    "Thailand": (15.870032, 100.992541),
    "Tajikistan": (38.861034, 71.276093),
    "Tokelau": (-8.967363, -171.855881),
    "Timor-Leste": (-8.874217, 125.727539),
    "Turkmenistan": (38.969719, 59.556278),
    "Tunisia": (33.886917, 9.537499),
    "Tonga": (-21.178986, -175.198242),
    "Turkey": (38.963745, 35.243322),
    "Trinidad and Tobago": (10.691803, -61.222503),
    "Tuvalu": (-7.109535, 177.64933),
    "Taiwan": (23.69781, 120.960515),
    "Tanzania": (-6.369028, 34.888822),
    "Ukraine": (48.379433, 31.16558),
    "Uganda": (1.373333, 32.290275),
    "United States": (37.09024, -95.712891),
    "Uruguay": (-32.522779, -55.765835),
    "Uzbekistan": (41.377491, 64.585262),
    "Vatican City": (41.902916, 12.453389),
    "Saint Vincent and the Grenadines": (12.984305, -61.287228),
    "Venezuela": (6.42375, -66.58973),
    "British Virgin Islands": (18.420695,  -64.639968),
    "U.S. Virgin Islands": (18.335765, -64.896335),
    "Virgin Islands": (18.335765, -64.896335),
    "Vietnam": (14.058324, 108.277199),
    "Vanuatu": (-15.376706, 166.959158),
    "Wallis and Futuna": (-13.768752, -177.156097),
    "Samoa": (-13.759029, -172.104629),
    "Kosovo": (42.602636, 20.902977),
    "Yemen": (15.552727, 48.516388),
    "Mayotte": (-12.8275, 45.166244),
    "South Africa": (-30.559482, 22.937506),
    "West Bank": (32.069553, 35.270941),
    "Zimbabwe": (-22.328474, 24.684866),
    "Zambia": (-13.133897, 27.849332)}

# A dictionary of US states and their respecitve two letter code
STATE_CODES = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY"
        }

# A dictionary of US states and their GPS coordiantes
STATE_COORD = {
        "Alabama": (32.361538, -86.279118),
        "Alaska": (58.301935, -134.419740),
        "Arizona": (33.448457, -112.073844),
        "Arkansas": (34.736009, -92.331122),
        "California": (38.555605, -121.468926),
        "Colorado": (39.7391667, -104.984167),
        "Connecticut": (41.767, -72.677),
        "Delaware": (39.161921, -75.526755),
        "Florida": (30.4518, -84.27277),
        "Georgia": (33.76, -84.39),
        "Hawaii": (21.30895, -157.826182),
        "Idaho": (43.613739, -116.237651),
        "Illinois": (39.783250, -89.650373),
        "Indiana": (39.790942, -86.147685),
        "Iowa": (41.590939, -93.620866),
        "Kansas": (39.04, -95.69),
        "Kentucky": (38.197274, -84.86311),
        "Louisiana": (30.45809, -91.140229),
        "Maine": (44.323535, -69.765261),
        "Maryland": (38.972945, -76.501157),
        "Massachusetts": (42.2352, -71.0275),
        "Michigan": (42.7335, -84.5467),
        "Minnesota": (44.95, -93.094),
        "Mississippi": (32.320, -90.207),
        "Missouri": (38.572954, -92.189283),
        "Montana": (46.595805, -112.027031),
        "Nebraska": (40.809868, -96.675345),
        "Nevada": (39.160949, -119.753877),
        "New Hampshire": (43.220093, -71.549127),
        "New Jersey": (40.221741, -74.756138),
        "New Mexico": (35.667231, -105.964575),
        "New York": (42.659829, -73.781339),
        "North Carolina": (35.771, -78.638),
        "North Dakota": (48.813343, -100.779004),
        "Ohio": (39.962245, -83.000647),
        "Oklahoma": (35.482309, -97.534994),
        "Oregon": (44.931109, -123.029159),
        "Pennsylvania": (40.269789, -76.875613),
        "Rhode Island": (41.82355, -71.422132),
        "South Carolina": (34.000, -81.035),
        "South Dakota": (44.367966, -100.336378),
        "Tennessee": (36.165, -86.784),
        "Texas": (30.266667, -97.75),
        "Utah": (40.7547, -111.892622),
        "Vermont": (44.26639, -72.57194),
        "Virginia": (37.54, -77.46),
        "Washington": (47.042418, -122.893077),
        "West Virginia": (38.349497, -81.633294),
        "Wisconsin": (43.074722, -89.384444),
        "Wyoming": (41.145548, -104.802042)
        }


def retrieve_location(tweet):
    '''Retrieve the location of a tweet.

    Args:
        tweet: a tweet object

    Returns:
        None if a location is not found
        or
        a location with the attributes: country, city, state, county, latitude,
        and longitude accessed using dot notation.

        For example:
            t.city will access the city of the location
    '''

    # initialize the location engine
    r = carmen.get_resolver()
    r.load_locations()
    # get the location
    loc = r.resolve_tweet(tweet)
    # return the location
    if loc is not None:
        return(loc[1])
    else:
        return(None)


def get_state(loc):
    '''Return the state of the location.
    Args:
        loc: a carmen location
    Returns:
        (str) the state of the location
        if a state is not found, returns None
    '''

    try:
        return(loc.state)
    except AttributeError:
        return(None)


def get_city(loc):
    '''Return the city of the location.
    Args:
        loc: a carmen location
    Returns:
        (str) the city of the location
        if a city is not found, returns None
    '''

    try:
        return(loc.city)
    except AttributeError:
        return(None)


def is_valid_country(loc, ctry):
    '''Return whether the location's country is equal with the other country.
    Args:
        loc: a carmen location
        ctry: (string) country to compare the location with
    Returns:
        bool
    '''

    if loc.country == ctry:
        return(True)
    else:
        return(False)


def find_location(tweet, ctry=None, by_state=False, by_city=False):
    '''Find the correct location based on filters.

    Args:
        tweet: the tweet to locate
        ctry: (string) the country to find the distribution within. If nothing,
            is passed, it will not filter the tweets by country and will get a
            global distribution by country.
        by_state: (bool) if True, it will return a distribution by state within
            the country passed by the ctry argument. Default: False
        by_city: (bool) if True, it will return a distribution by city within
            the country passed by the ctry argument. Default: False
    Returns:
        if a location is found, a string
        else: None
    '''

    # find the tweet's location
    loc = retrieve_location(tweet)
    # avoid unlocated tweets
    if loc is not None:
        # find the geo distribution within a country
        if is_valid_country(loc, ctry):
            # filter by state: return the state
            if by_state:
                return(get_state(loc))
            # filter by city: return the city
            elif by_city:
                return(get_city(loc))
            # filter by country: return the country
            else:
                return(loc.country)
        # not filtering by country
        else:
            # filter by state globally: return the state
            if by_state:
                return(get_state(loc))
            # filter by city globally: return the city
            elif by_city:
                return(get_city(loc))
            # filter by country globally: return the country
            else:
                return(loc.country)
    # a location was not found
    else:
        return(None)


def get_geo(tweets, ctry=None, by_state=False, by_city=False):
    '''Find the sentiment distribution for a region.

    A method to find the sentiment distribution across a geographic region in
    a list of tweets. It uses the carmen engine to determine location and the
    afinn engine to determine the sentimentality of the tweet's text.

    Args:
        tweets: (list) a list of tweets
        ctry: (string) the country to find the distribution within. If nothing,
            is passed, it will not filter the tweets by country and will get a
            global distribution by country.
        by_state: (bool) if True, it will return a distribution by state within
            the country passed by the ctry argument. Default: False
        by_city: (bool) if True, it will return a distribution by city within
            the country passed by the ctry argument. Default: False

    Returns:
        dict: of the form
            'places': {
                    'total': (int) the number of tweets originating in that
                        place
                    'users': (set) the set of usernames of users who tweeted
                    'sent': (dict) a dictionary of tweet sentiment information
                        'neg': (int) the number of tweets with a negative 
                            sentiment score
                        'pos': (int) the number of tweets with a positive
                            sentiment score
                        'neut': (int) the number of tweets with a neutral
                            sentiment score
                    }
            'filt': (int) the number of tweets that which were not able to be 
                located
    '''
    d = {
            'places': dict(),
            'filt': 0
            }

    # look through all the tweets and try to find their location
    for t in tweets:
        loc = find_location(t, ctry=ctry, by_state=by_state, by_city=by_city)

        # if no location was found, skip tweet
        if loc is None:
            d['filt'] += 1
            continue
        else:
            # calculate the sentiment of the tweet text
            print(len([t]))
            sent = get_sentiment([t])[0]

            # if this is a new location instantiate a new dictionary with
            # default values
            if loc not in d['places'].keys():
                d['places'][loc] = {
                    'total': 1,
                    'users': {t['user']['screen_name']},
                    'sent': {
                        'total': sent,
                        'neg': 0,
                        'pos': 0,
                        'neut': 0
                        }
                    }
            # we are looking at a location that has already been added so
            # update the appropriate values
            else:
                d['places'][loc]['total'] += 1
                d['places'][loc]['users'].add(t['user']['screen_name'])

            # Increment correct sentiment category
            if sent < 0:
                d['places'][loc]['sent']['neg'] += 1
            elif sent == 0:
                d['places'][loc]['sent']['neut'] += 1
            elif sent > 0:
                d['places'][loc]['sent']['pos'] += 1

    # return dictionary
    return d


def save_geo(dat, filt, none, fout):
    data = {
            "data": dat,
            "num_filtered": filt,
            "nolocation": none
            }
    save(data, fout)


def load_geo(fin):
    d = load(fin)
    return(d['data'], d['num_filtered'], d['nolocation'])


def to_CSV(out, data, by_state=False):
    codes = dict()
    coord = dict()

    print("Saving Country CSV File")
    total_pos_tweets = 0
    for loc in data:
        total_pos_tweets += data[loc]['sent']['pos']

    # Determine whether it's by-state or by-country
    if by_state is False:
        # organize them by country, so use the country dictionary
        codes = COUNTRY_CODES
        coord = COUNTRY_COORD
    else:
        # organize them by state, so use the state dictionary
        codes = STATE_CODES
        coord = STATE_COORD

    # Write a comma-separated file
    with open(out, 'w') as fout:
        fout.write("Place,Code,Sentiment,Users,Lat,Lon,Count\n")
        for c in codes:
            if data.get(c) is not None:
                s = data["sent"]["pos"] / total_pos_tweets
                u = len(data[c]["users"])
                t = data[c]["sent"]["pos"] \
                    + data[c]["sent"]["neg"] \
                    + data[c]["sent"]["neut"]
            else:
                s = 0
                u = 0
                t = 0
            try:
                fout.write("{0},{1},{2},{3},{4},{5},{6}\n".format(
                    c, codes[c], s, u, coord[c][0], coord[c][1], t
                    ))
            except KeyError:
                    print("Missing key {0}".format(c))
        fout.close()
        print("Finished writing CSV file")


if __name__ == '__main__':
    tw = get_tweets(['./data/25crisis/'])
    tweets, filt = tw
    g = get_geo(tweets)
    print(g['places'])

    # Save the geo data to a .dat file
    print("Saving Country Geo .dat File")
    save_geo(g["places"], filt, g["filt"], jn(PROC, "geo-cn.dat"))

    # Save the geo data to a CSV
    print("Saving Country CSV File")
    to_CSV(jn(PROC, "geo-cn.csv"), g["places"])
