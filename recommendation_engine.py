import requests

def get_recommendation(city, predicted_bill, devices_info):
    prompt = f"""
    My electricity bill for this month in {city} is ₹{predicted_bill:.2f}.
    I use the following devices: {devices_info}.
    Suggest 3 personalized and practical tips to reduce electricity usage.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return "Could not generate recommendation. Try again later."
    except requests.exceptions.RequestException:
        return "Ollama API is not running or could not be reached."
