import os
import time
import requests
import json
from flask_cors import CORS
url = "http://localhost:1337/strains?populate=*"
bearer_token = "a7afa94895905900d62ce7014bf5aca7c452d21e61c6222488b69e9f33819011b991b4e621b77caea7596f56635a83c7a365448a95b649153e854f4cb3420a7f92b45c15e94a4fd81faa492735f696691b2962b0b8df0d962dc694aad320630da912fc67365a64f4b2224315359205be366bda0503d5747deabe19f9a600fb29"

def authenticate_api_bearer_token(url, bearer_token):
    headers = {'Authorization': f'Bearer {bearer_token}'}
    response = requests.get(url, headers=headers)
    return response

def get_rating(entry, key):
    return entry.get(key, {}).get('Rating', 0)

def calculate_weighted_rating(entry, weights):
    attributes = entry.get('attributes', {})
    
    total_rating = 0.0
    total_weight = sum(weights.values()) - 1

    # Calcula el rating total basado en los atributos y pesos dados
    for rating_key in ['Germination', 'BudDensity', 'Yield', 'Power', 'Strenght', 'Truth', 'Resilience']:
        if rating_key == 'Germination':
            # Extrae 'Germination_Rating' desde 'Seed_quality' si estamos tratando con 'Germination'
            Seed_quality = attributes.get('Seed_quality', {})
            germination_rating =Seed_quality.get('Appearance_Seed_Rating', 0)  

            total_rating += germination_rating * weights.get('Germination', 0)
        else:
            # Para otros atributos, procede como antes
            rating_value = attributes.get(rating_key, {}).get('Rating', 0)
            total_rating += rating_value * weights.get(rating_key, 0)
    
    # Incluye las calificaciones de olor y sabor
    smell_flavor = attributes.get('Smell_Flavor', {})
    smell_rating = smell_flavor.get('Smell_Rating', 0)
    flavor_rating = smell_flavor.get('Flavor_Rating', 0)

    total_rating += smell_rating * weights.get('Smell_Rating', 0)
    total_rating += flavor_rating * weights.get('Flavor_Rating', 0)
    
    # Calcula el rating ponderado
    weighted_rating = total_rating / total_weight if total_weight > 0 else 0


    return weighted_rating


def classify_yield(yield_size):
    """Classify the yield size into categories."""
    try:
        yield_size = float(yield_size)  # Ensure Yield_size is a number
    except ValueError:
        return "Unknown"  # Return Unknown if conversion fails

    if yield_size <= 500:
        return "Low Yield"
    elif 500 < yield_size <= 800:
        return "Mid Yield"
    else:
        return "High Yield"

def classify_Brand_promises_fidelity(final_rating):
    try:
        final_rating = float(final_rating)  # Ensure weighted_rating is a number
    except ValueError:
        return "Unknown"  # Return "Unknown" if conversion fails
    
    if final_rating > 70:
        return "Yes"
   
    else:
        return "No"


def fetch_and_process_data(url, bearer_token, weights):
    response = authenticate_api_bearer_token(url, bearer_token)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        for entry in data:
            strain_name = entry['attributes'].get('Strain_name', 'Unknown Strain')
            weighted_rating = calculate_weighted_rating(entry, weights)
            print(f"Strain: {strain_name}, Weighted Rating: {weighted_rating:.2f}")
    else:
        print(f"Error fetching data: {response.status_code}")

# Valores de ponderación individuales para cada característica
weights = {
    'Germination': 1.0,
    'BudDensity': 1.0,
    'Power': 1.0,
    'Strenght': 1.0,
    'Truth': 1.0,
    'Smell_Rating': 1.0,
    'Flavor_Rating': 1.0,
    'Yield': 1.0,
    'Appearance_Seed_Rating': 1.0,
    'Resilience': 1.0,
}


def create_enriched_json(data, weights):
    enriched_data = []  # Lista para almacenar los datos enriquecidos
    for entry in data:
        strain_id = entry.get('id', '')
        strain_name = entry['attributes'].get('Strain_name', 'Unknown Strain')
        strain_Description = entry['attributes'].get('Strain_Description', 'Unknown Description')
        weighted_rating = calculate_weighted_rating(entry, weights)
        image_data = entry['attributes'].get('strain_image', {}).get('data', None)
        if image_data:
             image_info = image_data.get('attributes', {})
        else:    
            image_info = {}
       #data prejason
        strain_characteristics = entry['attributes'].get('Strains_Characterisitics', {})
        seed_bank = strain_characteristics.get('SeedBank', 'Unknown SeedBank')
        Species = strain_characteristics.get('Species', 'Unknown SeedBank')
        Type = strain_characteristics.get('Type', 'Unknown SeedBank')
        Flowering_Time = entry['attributes'].get('Flowering_Time', ' ')
        Germination_Appearance = entry['attributes'].get('Germination', {})
        Germination_Appearance_Rating = Germination_Appearance.get('Rating',' ')
        Appearance_Seed = entry['attributes'].get('Seed_quality', {})
        Appearance_Seed_Rating = Appearance_Seed.get('Appearance_Seed_Rating',' ')
        BudDensity = entry['attributes'].get('BudDensity', {})
        BudDensity_Rating = BudDensity.get('Rating',' ')
        Yield = entry['attributes'].get('Yield', {})
        Yield_Rating = Yield.get('Rating',' ')
        Yield_Size = Yield.get('Size_grams',' ')
        yield_category = classify_yield(Yield_Size)
        Power = entry['attributes'].get('BudDensity', {})
        Power_Rating = Power.get('Rating',' ')
        Strenght = entry['attributes'].get('Strenght',{})
        Strenght_Rating= Strenght.get('Rating',' ')
        Truth = entry['attributes'].get('Truth',{})
        Truth_Rating = Truth.get('Rating',' ')
        Smell_Flavor = entry['attributes'].get('Smell_Flavor',{})
        Smell_Rating = Smell_Flavor.get('Smell_Rating',' ')
        Flavor_Rating = Smell_Flavor.get('Flavor_Rating',' ')
        Resilience= entry['attributes'].get('Resilience',{})
        Resilience_Rating = Resilience.get('Rating',' ')
        Cannabinoid_Profile =entry['attributes'].get('Cannabinoid_Profile',{})
        THC_Percentage = None
        if Cannabinoid_Profile is not None:
         if isinstance(Cannabinoid_Profile, dict):
          THC_Percentage = Cannabinoid_Profile.get('THC_Percentege', ' ')
          
          CBD_Percentege = None
        if Cannabinoid_Profile is not None:
         if isinstance(Cannabinoid_Profile, dict):
          CBD_Percentege = Cannabinoid_Profile.get('CBD_Percentege', ' ')

         Brand_promises_fidelity = classify_Brand_promises_fidelity(weighted_rating)
         Plant_health = entry['attributes'].get('Plant_health',{})
         Have_Virus = Plant_health.get('Have_Virus',' ')

        Youtube_Video = entry['attributes'].get('Youtube_Video')
        if Youtube_Video is None:
             Youtube_Video = ' '

         

        # Json Gen
        enriched_entry = {
            'Strain':{
            'Strain_Id': strain_id,
            'Strain_Name': strain_name,   
            'Strain_Description':strain_Description,
             'Seed_Bank': seed_bank,
             'Flowering_Time':Flowering_Time,
            'Species': Species,
            'Youtube_video':Youtube_Video,
            'Type': Type,
              'Image': {
                'name': image_info.get('name', ''),
                'alternativeText': image_info.get('alternativeText', ''),
                'caption': image_info.get('caption', ''),
                'width': image_info.get('width', 0),
                'height': image_info.get('height', 0),
                'url': image_info.get('url', ''),
            },
             'Bud_Density_Rating': BudDensity_Rating,
           'Yield': {
                'Yield_Rating': Yield_Rating,
                'Yiled_Size':Yield_Size,
                'Yield_Size': yield_category
            },
            'Seed_quality':{
               'Germination_Rating': Germination_Appearance_Rating,
                'Appearance_Seed_Rating': Appearance_Seed_Rating
            },
            'Power_Rating': Power_Rating,
            'Strenght_Rating': Strenght_Rating,
            'Truth_Rating': Truth_Rating,
             'Smell_flavor':{
                'Smell_Rating': Smell_Rating,
                'Flavor_Rating': Flavor_Rating
            },
            'Cannabinoid_Profile':{
                'THC_Percentage':THC_Percentage,
                'CBD_Percentege':CBD_Percentege
            },
           'Plant_Health':{
                 'Have_Virus': Have_Virus
            },
            'Brand_promises_fidelity': Brand_promises_fidelity,
            'Resilience_Rating':Resilience_Rating,
            'Weighted_Rating': weighted_rating,
        }
        }
        enriched_data.append(enriched_entry)
    # Convierte la lista de datos enriquecidos a JSON
    return json.dumps(enriched_data, indent=4)

# Modifica la función fetch_and_process_data para incluir la creación del nuevo JSON
def fetch_and_process_data(url, bearer_token, weights):
    response = authenticate_api_bearer_token(url, bearer_token)
    if response.status_code == 200:
        data = response.json().get('data', [])
        enriched_json = create_enriched_json(data, weights)  # Use the function to create enriched JSON
        return enriched_json  # Return the JSON string
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


# from flask import Flask, jsonify

from flask import Flask, jsonify, request, abort
import requests
import json

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# Your existing functions here (authenticate_api_bearer_token, calculate_weighted_rating, create_enriched_json)



def fetch_and_process_data(url, bearer_token, weights):
    # Your modified fetch_and_process_data function that returns JSON data
    response = authenticate_api_bearer_token(url, bearer_token)
    if response.status_code == 200:
        data = response.json().get('data', [])
        enriched_json = create_enriched_json(data, weights)  # Generate enriched JSON
        return enriched_json
    else:
        print(f"Error fetching data: {response.status_code}")
        return None
    
expected_bearer_token = "6e5O5ZwgTC9CRRdzTc2CEYsxfnDDohQI4au31KUzCNmxPUWC2Q"
@app.route('/')
def data():
  # Check if Authorization header is present
    if 'Authorization' not in request.headers:
        abort(401)  # Unauthorized if no Authorization header is provided

    # Extract the bearer token from the Authorization header
    auth_header = request.headers['Authorization']
    _, token = auth_header.split(' ')  # Split the Authorization header to get the token

    # Verify the bearer token
    if token != expected_bearer_token:
        abort(403)  # Forbidden if the provided token is not valid

    # Proceed with fetching and processing data if the token is valid
    enriched_json = fetch_and_process_data(url, bearer_token, weights)  # Assuming this returns a JSON string
    if enriched_json:
        # Convert JSON string back to a Python dict for jsonify to work
        data = json.loads(enriched_json)
        return jsonify(data)
    else:
        return "Failed to fetch data", 500

if __name__ == '__main__':
    app.run(debug=True)









# Asegúrate de que el ciclo principal sigue intacto
if __name__ == "__main__":
    while True:
        fetch_and_process_data(url, bearer_token, weights)
        time.sleep(10)  # Espera 10 segundos antes de la próxima actualización

