import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Load Azure OpenAI configuration
api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')
deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

print(f"Azure OpenAI Configuration:")
print(f"  Endpoint: {endpoint}")
print(f"  Deployment: {deployment_name}")
print(f"  API Version: {api_version}")
print()

def get_entity_links(sentence, model=None):
    """
    Get Wikipedia page titles for named entities in a Dutch sentence using Azure OpenAI API.
    
    Args:
        sentence: Dutch sentence to analyze
        model: Azure deployment name (if None, uses default from environment)
    
    Returns:
        List of predicted Wikipedia page titles
    """
    try:
        # Use deployment name from environment if not provided
        if model is None:
            model = deployment_name
            
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": "Je bent een expert in het herkennen van named entities in Nederlandse tekst. Geef voor elke named entity (persoon, plaats, organisatie) de exacte Wikipedia pagina titel terug."
                },
                {
                    "role": "user",
                    "content": f"Geef de Wikipedia pagina titels voor alle named entities in deze Nederlandse zin: '{sentence}'\n\nGeef alleen de Wikipedia titels terug, gescheiden door komma's. Als er geen entities zijn, antwoord met 'Geen'."
                }
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.lower() in ['geen', 'none', '']:
            return []
        
        # Parse the response to extract individual titles
        titles = [title.strip() for title in result.split(',')]
        return titles
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return []

# Test with example sentences
test_sentences = [
    "Deze uittocht vindt onder andere plaats via Amsterdam, Antwerpen en vooral Rotterdam.",
    "Deze restauratie werd geleid door C.H. Peters, die geadviseerd werd door P.J.H. Cuypers."
]

for sentence in test_sentences:
    print(f"Sentence: {sentence}")
    predicted_titles = get_entity_links(sentence)
    print(f"Predicted entities: {predicted_titles}")
    print()