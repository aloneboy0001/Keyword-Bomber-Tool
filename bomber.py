# Import libraries for HTTP requests and XML parsing
import requests
import httpx
import xml.etree.ElementTree as ET

# Commenting out imports related to AI report generation and OpenAI
# import prompts
# import llm

# LLM_MODEL = "gpt-3.5-turbo-1106"  # No longer needed for AI analysis

# Main function to get keyword data from Google suggestions
async def get_keyword_data(input_keyword, input_country):
    # Get suggestions for the input keyword using Google Autocomplete
    keyword_data = await get_suggestion_keywords_google_optimized(input_keyword, input_country)

    # Commenting out AI report generation as it's no longer needed
    # ai_report = await suggestions_ai_analysis(keyword_data, api_key)

    # Prepare the result without AI analysis
    result = {
        "success": True,
        "message": "Success! Keywords Generated",
        "result": {
            "keyword_data": keyword_data,  # Only returning keyword data now
            # Commenting out AI report from result
            # "ai_report": ai_report,
        },
    }

    return result

# Commenting out the AI analysis function as it is no longer required
# async def suggestions_ai_analysis(keyword_data: str, api_key):
#     # This function was previously used to generate the AI report using OpenAI
#     max_retries = 5
#     for _ in range(max_retries):
#         try:
#             # Get a prompt structure for AI analysis
#             prompt = prompts.suggestion_keywords_analysis.format(KEYWORD_DATA=keyword_data)
#             return await llm.generate_response(prompt, LLM_MODEL, api_key)
#         except Exception as e:
#             print(f"Failed to generate analysis for suggestion keywords. Exception type: {type(e).__name__}, Message: {str(e)}")
#     return ""

# Function to get categorized Google suggestions for the given keyword
async def get_suggestion_keywords_google_optimized(query, countryCode):
    # Define various keyword categories for fetching suggestions
    categories = {
        "Questions": ["who", "what", "where", "when", "why", "how", "are"],
        "Prepositions": ["can", "with", "for"],
        "Alphabit": list("abcdefghijklmnopqrstuvwxyz"),
        "Comparisons": ["vs", "versus", "or"],
        "Intent-Based": ["buy", "review", "price", "best", "top", "how to", "why to"],
        "Time-Related": ["when", "schedule", "deadline", "today", "now", "latest"],
        "Audience-Specific": ["for beginners", "for small businesses", "for students", "for professionals"],
        "Problem-Solving": ["solution", "issue", "error", "troubleshoot", "fix"],
        "Feature-Specific": ["with video", "with images", "analytics", "tools", "with example"],
        "Opinions/Reviews": ["review", "opinion", "rating", "feedback", "testimonial"],
        "Cost-Related": ["price", "cost", "budget", "cheap", "expensive", "value"],
        "Trend-Based": ["trends", "new", "upcoming"]
    }

    # Create a dictionary to store categorized suggestions
    categorized_suggestions = {key: {} for key in categories.keys()}

    # Iterate through each category and fetch suggestions
    for category in categories:
        for keyword in categories[category]:
            try:
                # Generate a modified query for each keyword category
                if category in ["Questions", "Prepositions", "Intent-Based", "Time-Related",
                                "Audience-Specific", "Problem-Solving", "Opinions/Reviews", "Cost-Related", "Trend-Based"]:
                    modified_query = f"{keyword} {query}"
                elif category in ["Alphabit", "Feature-Specific"]:
                    modified_query = f"{query} {keyword}"
                else:
                    modified_query = f"{keyword} {query}"

                # Fetch suggestions asynchronously for the modified query
                category_suggestions = await get_suggestions_for_query_async(modified_query, countryCode)
                categorized_suggestions[category][keyword] = category_suggestions
            except Exception as e:
                print(f"Error in get_suggestion_keywords_google_optimized, {e}")
    
    # Return categorized keyword suggestions
    return categorized_suggestions

# Function to fetch suggestions from Google Autocomplete API asynchronously
async def get_suggestions_for_query_async(query, country):
    async with httpx.AsyncClient() as client:
        try:
            # Make a request to Google's Autocomplete API
            response = await client.get(f"http://google.com/complete/search?output=toolbar&gl={country}&q={query}")
            suggestions = []
            if response.status_code == 200:
                # Parse the XML response and extract suggestions
                root = ET.fromstring(response.content)
                for complete_suggestion in root.findall('CompleteSuggestion'):
                    suggestion_element = complete_suggestion.find('suggestion')
                    if suggestion_element is not None:
                        data = suggestion_element.get('data').lower()
                        suggestions.append(data)
        except Exception as e:
            error = e  # Error handling
        # Return the suggestions
        return suggestions

# Optional non-async version of the Google Autocomplete function
def get_suggestions_for_query(query):
    response = requests.get(f"http://google.com/complete/search?output=toolbar&q={query}")
    suggestions = []
    try:
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for complete_suggestion in root.findall('CompleteSuggestion'):
                suggestion_element = complete_suggestion.find('suggestion')
                if suggestion_element is not None:
                    data = suggestion_element.get('data').lower()
                    suggestions.append(data)
    except Exception as e:
        print(f"keyword_research: get_suggestions_for_query. Exception type: {type(e).__name__}, Message: {str(e)}")
    return suggestions