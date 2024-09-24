import requests
from opencage.geocoder import OpenCageGeocode
import keplergl

# Function to get news for a city
def get_news(city):
    api_key = '8023a88cf1de42cb84f9d6c0e5d9259f'
    url = f'https://newsapi.org/v2/everything?q={city}&apiKey={api_key}'
    response = requests.get(url)
    return response.json()

# Function to get coordinates for a city
def get_coordinates(city):
    key = '1f50677e3f664c36b68e4c871359fe72'
    geocoder = OpenCageGeocode(key)
    result = geocoder.geocode(city)
    if result:
        return (result[0]['geometry']['lat'], result[0]['geometry']['lng'])
    else:
        return (None, None)

# List of top 100 cities in the world
cities = [
    'London', 'New York', 'Tokyo', 'Paris', 'Singapore', 'Dubai', 'Barcelona', 'Los Angeles', 'Rome', 'Chicago',
    'Toronto', 'San Francisco', 'Madrid', 'Amsterdam', 'Boston', 'Hong Kong', 'Sydney', 'Berlin', 'Melbourne', 'Vienna',
    'Milan', 'Munich', 'Miami', 'Zurich', 'Istanbul', 'Seoul', 'Bangkok', 'Brussels', 'Dublin', 'Lisbon',
    'Stockholm', 'Copenhagen', 'Oslo', 'Helsinki', 'Warsaw', 'Prague', 'Budapest', 'Athens', 'Edinburgh', 'Glasgow',
    'Manchester', 'Birmingham', 'Lyon', 'Marseille', 'Nice', 'Toulouse', 'Nantes', 'Strasbourg', 'Bordeaux', 'Lille',
    'Hamburg', 'Frankfurt', 'Stuttgart', 'Dusseldorf', 'Cologne', 'Dresden', 'Leipzig', 'Hanover', 'Nuremberg', 'Bremen',
    'Krakow', 'Gdansk', 'Wroclaw', 'Poznan', 'Lodz', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Katowice', 'Bialystok',
    'Sofia', 'Bucharest', 'Belgrade', 'Zagreb', 'Ljubljana', 'Bratislava', 'Vilnius', 'Riga', 'Tallinn', 'Tirana',
    'Skopje', 'Sarajevo', 'Podgorica', 'Pristina', 'Chisinau', 'Minsk', 'Kiev', 'Tbilisi', 'Yerevan', 'Baku', 'Dhaka'
]

# Fetch news and coordinates for each city
news_data = {city: get_news(city) for city in cities}
coordinates = {city: get_coordinates(city) for city in cities}

# Format data for Kepler.gl
def format_data(news_data, coordinates):
    features = []
    for city, data in news_data.items():
        lat, lon = coordinates[city]
        if lat is not None and lon is not None:
            if 'articles' in data:
                for article in data['articles']:
                    feature = {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [lon, lat]
                        },
                        'properties': {
                            'title': article['title'],
                            'description': article['description'],
                            'url': article['url']
                        }
                    }
                    features.append(feature)
            else:
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [lon, lat]
                    },
                    'properties': {
                        'title': 'No news',
                        'description': '',
                        'url': ''
                    }
                }
                features.append(feature)
    return {
        'type': 'FeatureCollection',
        'features': features
    }

geojson_data = format_data(news_data, coordinates)

# Create the interactive map
map_1 = keplergl.KeplerGl()
map_1.add_data(data=geojson_data, name='News Headlines')

# Configure the tooltip to display the title
config = {
    'version': 'v1',
    'config': {
        'visState': {
            'layers': [
                {
                    'id': 'news_headlines',
                    'type': 'point',
                    'config': {
                        'dataId': 'News Headlines',
                        'label': 'News Headlines',
                        'columns': {
                            'lat': 'geometry.coordinates[1]',
                            'lng': 'geometry.coordinates[0]',
                            'altitude': None
                        },
                        'isVisible': True,
                        'visConfig': {
                            'radius': 10,
                            'colorRange': {
                                'colors': ['#FF0000']
                            }
                        }
                    }
                }
            ],
            'interactionConfig': {
                'tooltip': {
                    'fieldsToShow': {
                        'News Headlines': ['properties.title', 'properties.description', 'properties.url']
                    },
                    'enabled': True
                }
            }
        }
    }
}

map_1.config = config
map_1.save_to_html(file_name='news_map.html')
