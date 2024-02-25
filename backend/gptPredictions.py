import openai
import requests

# Set your OpenAI API key
openai.api_key = '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'

#OUT OF USE TILL I GET MORE CREDITS :b



# Function to retrieve solar insolation data from the Flask API
def get_solar_insolation_data():
    # Make a request to the Flask API endpoint
    response1 = requests.post('http://localhost:5000/submit-coordinates',
                              json={'coordinates': [{'lat': 40.7128, 'lng': -74.0060}]})
    # Extract solar insolation data from the response
    solar_insolation_data1 = response1.json()['top_5_results']
    return solar_insolation_data1


# Retrieve solar insolation data from the Flask API
solar_insolation_data = get_solar_insolation_data()

# Define the prompt including the solar insolation data
prompt = f"""
Consider the following points in your response:

1. Based on the provided solar insolation data, measured in watts per square meter (W/m²): {solar_insolation_data}

2. Discuss potential optimization strategies for the solar panel configuration, including considerations such as tilt angle, orientation, and tracking systems, to maximize energy generation efficiency.

3. Evaluate the feasibility and benefits of incorporating energy storage solutions, such as batteries, to store excess energy generated during peak sunlight hours for use during periods of low solar insolation or at night.

4. Estimate the return on investment (ROI) for a solar energy system, taking into account the upfront costs of installation, potential savings on electricity bills, and available incentives or rebates for solar installations.

5. Assess the environmental impact of transitioning to solar energy, including the reduction in carbon emissions and dependence on fossil fuels over the system's lifespan.

6. Discuss the options available for financing a solar energy system, such as solar leases, power purchase agreements (PPAs), or loans, and provide recommendations based on financial situation and preferences.

7. Explore potential energy-efficient measures that can be implemented in conjunction with the solar energy system to further reduce energy consumption and optimize overall energy efficiency in the household.
"""

# Generate a response using the OpenAI API with the "gpt-3.5-turbo" model
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=100  # Limiting the maximum number of words generated
)

# Print the response
print(response.choices[0].text.strip())
