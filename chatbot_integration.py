import openai
import json

# Set OpenAI API key
openai.api_key = "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"

# Load JSON data
with open('formatted_data.json', 'r') as f:
    data = json.load(f)

# Define function to call GPT model
def get_ppp_opportunities(project_description):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Replace with a supported engine
            prompt=f"Analyze the potential social impact of the following project and provide a brief summary: {project_description}",
            max_tokens=500,  # Limit the length of the generated content
            temperature=0.7  # Control the randomness of the output
        )
        # Return the generated text result
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        # Error handling
        print(f"API call failed: {str(e)}")
        return None

# Test the function using the first project description from the JSON data
if __name__ == "__main__":
    example_project = data[0]['Project Description']  # Get the first project description
    result = get_ppp_opportunities(example_project)
    if result:
        print("GPT-generated analysis result:")
        print(result)
    else:
        print("Failed to generate result. Please check the error message.")
