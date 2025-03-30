"""
Search-related tools for the travel planning application.
This module contains functions for web searches, Wikipedia searches, and web browsing.
"""

import os
import json
import requests
from typing import Union, List, Dict, Any, Optional, Literal
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def serper_search(
    query: Union[str, List[str]],
    search_type: Literal["search", "news", "images", "shopping"] = "search",
    num_results: Optional[int] = 10,
    date_range: Optional[Literal["h", "d", "w", "m", "y"]] = None,
    location: Optional[str] = None
) -> Union[str, List[str]]:
    """
    Perform a search using the Serper API and format the results.

    Args:
        query (Union[str, List[str]]): The search query or a list of search queries.
        search_type (Literal["search", "news", "images", "shopping"]): The type of search to perform.
        num_results (Optional[int]): Number of results to return (default: 10).
        date_range (Optional[Literal["h", "d", "w", "m", "y"]]): Date range for results
                                                                (h: hour, d: day, w: week, m: month, y: year).
        location (Optional[str]): Specific location for the search.

    Returns:
        Union[str, List[str]]: A formatted string or list of formatted strings containing the search results.

    Raises:
        ValueError: If the API key is not set or if there's an error with the API call.
        requests.RequestException: If there's an error with the HTTP request.
    """
    # Load environment variables
    load_dotenv()

    # Get API key from environment variable
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY environment variable is not set")

    # Define the base URL
    BASE_URL = "https://google.serper.dev"

    # Construct the URL based on the search type
    url = f"{BASE_URL}/{search_type}"

    # Convert query to list if it's a string
    queries = [query] if isinstance(query, str) else query

    results_list = []

    for single_query in queries:
        # Prepare the payload
        payload = {
            "q": single_query,
            "gl": "us",
            "hl": "en",
        }

        # Add num_results to payload if provided
        if num_results is not None:
            payload["num"] = num_results

        # Add optional parameters if provided
        if date_range:
            payload["tbs"] = f"qdr:{date_range}"
        if location:
            payload["location"] = location

        # Prepare headers
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        try:
            # Make the API call
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            results = response.json()

            # Format the results
            formatted_results = ""

            if "organic" in results:
                formatted_results += "Organic Results:\n"
                for i, result in enumerate(results["organic"], 1):
                    formatted_results += f"{i}. {result.get('title', 'No Title')}\n"
                    formatted_results += f"   URL: {result.get('link', 'No Link')}\n"
                    formatted_results += f"   Snippet: {result.get('snippet', 'No Snippet')}\n\n"

            if "news" in results:
                formatted_results += "News Results:\n"
                for i, news in enumerate(results["news"], 1):
                    formatted_results += f"{i}. {news.get('title', 'No Title')}\n"
                    formatted_results += f"   Source: {news.get('source', 'No Source')}\n"
                    formatted_results += f"   URL: {news.get('link', 'No Link')}\n"
                    formatted_results += f"   Date: {news.get('date', 'No Date')}\n"
                    formatted_results += f"   Snippet: {news.get('snippet', 'No Snippet')}\n"
                    formatted_results += f"   Image URL: {news.get('imageUrl', 'No Image URL')}\n\n"

            if "images" in results:
                formatted_results += "Image Results:\n"
                for i, image in enumerate(results["images"], 1):
                    formatted_results += f"{i}. {image.get('title', 'No Title')}\n"
                    formatted_results += f"   URL: {image.get('link', 'No Link')}\n"
                    formatted_results += f"   Source: {image.get('source', 'No Source')}\n\n"

            if "shopping" in results:
                formatted_results += "Shopping Results:\n"
                for i, item in enumerate(results["shopping"], 1):
                    formatted_results += f"{i}. {item.get('title', 'No Title')}\n"
                    formatted_results += f"   Price: {item.get('price', 'No Price')}\n"
                    formatted_results += f"   URL: {item.get('link', 'No Link')}\n\n"

            results_list.append(formatted_results.strip())

        except requests.RequestException as e:
            results_list.append(f"Error making request to Serper API for query '{single_query}': {str(e)}")
        except json.JSONDecodeError:
            results_list.append(f"Error decoding JSON response from Serper API for query '{single_query}'")

    return results_list[0] if len(results_list) == 1 else results_list


def wikipedia_search_articles(query: str, num_results: int = 10) -> List[Dict[str, str]]:
    """
    Search for Wikipedia articles based on a given query.

    Args:
        query (str): The search query string.
        num_results (int, optional): The maximum number of search results to return. Defaults to 10.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing detailed information about each search result.
        Each dictionary includes:
            - 'title': The title of the article.
            - 'fullurl': The full URL of the article on Wikipedia.
            - 'snippet': A brief extract or snippet from the article.

    Raises:
        requests.exceptions.RequestException: If there's an error fetching search results from the Wikipedia API.
        KeyError, ValueError: If there's an error parsing the API response.
    """
    print(f"Searching articles for query: {query}")
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": num_results,
        "format": "json",
        "origin": "*"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        search_results = data["query"]["search"]

        # Fetch additional details for each search result
        detailed_results = []
        for result in search_results:
            page_id = result['pageid']
            detailed_params = {
                "action": "query",
                "pageids": page_id,
                "prop": "info|extracts|pageimages",
                "inprop": "url",
                "exintro": "",
                "explaintext": "",
                "pithumbsize": "250",
                "format": "json",
                "origin": "*"
            }
            detailed_response = requests.get(base_url, params=detailed_params)
            detailed_response.raise_for_status()
            detailed_data = detailed_response.json()
            page_data = detailed_data["query"]["pages"][str(page_id)]

            detailed_result = {
                "title": page_data.get("title"),
                "fullurl": page_data.get("fullurl"),
                "snippet": page_data.get("extract", "")
            }
            detailed_results.append(detailed_result)

        return detailed_results
    except requests.exceptions.RequestException as e:
        print(f"Error searching articles: {e}")
        return []
    except (KeyError, ValueError) as e:
        print(f"Error parsing response: {e}")
        return []


def wikipedia_search_images(query: str, limit: int = 20, thumb_size: int = 250) -> str:
    """
    Search for images on Wikimedia Commons based on a given query.

    Args:
        query (str): The search query for finding images.
        limit (int, optional): The maximum number of image results to return. Defaults to 20.
        thumb_size (int, optional): The desired size of the thumbnail in pixels. Defaults to 250.

    Returns:
        str: A formatted string containing information about the found images.

    Raises:
        requests.exceptions.RequestException: If there's an error in the HTTP request.
        KeyError, ValueError: If there's an error parsing the API response.
    """
    print(f"Searching images for query: {query}")
    base_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": f"intitle:{query}",
        "gsrlimit": limit,
        "prop": "pageimages|info",
        "pithumbsize": thumb_size,
        "inprop": "url",
        "format": "json",
        "origin": "*"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Check if 'query' and 'pages' exist in the response
        if 'query' not in data or 'pages' not in data['query']:
            return "No images found for your query."
            
        pages = data["query"]["pages"]
        image_results = []
        
        for page_id, page_data in pages.items():
            # Check if we have a thumbnail available
            if 'thumbnail' in page_data and 'source' in page_data['thumbnail']:
                image_info = {
                    "title": page_data["title"],
                    "url": page_data["fullurl"],
                    "thumbnail": page_data['thumbnail']['source']
                }
                image_results.append(image_info)

        # Format the output
        formatted_results = []
        separator = "-" * 30  # Create a separator line
        
        if not image_results:
            return "No images with thumbnails found for your query."
            
        for i, image in enumerate(image_results, 1):
            formatted_image = f"\nImage {i}:\n"
            formatted_image += f"  Title: {image['title']}\n"
            formatted_image += f"  URL: {image['url']}\n"
            formatted_image += f"  Thumbnail: {image['thumbnail']}\n"
            formatted_image += f"{separator}"
            formatted_results.append(formatted_image)

        return "".join(formatted_results)

    except requests.exceptions.RequestException as e:
        print(f"Error searching images: {e}")
        return f"Error occurred while searching for images: {str(e)}"
    except (KeyError, ValueError) as e:
        print(f"Error parsing response: {e}")
        return f"Error occurred while parsing the response: {str(e)}"


def browse_webpage(url: str) -> str:
    """
    Fetches content from a webpage and extracts relevant information.

    Args:
        url (str): The URL to browse

    Returns:
        str: The extracted content from the webpage
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', 'iframe', 'nav', 'footer']):
            script_or_style.decompose()
        
        # Try to find the main content using common selectors
        main_content = None
        
        # Look for common content container elements
        content_selectors = [
            'main', 'article', '.content', '#content', '.main-content', 
            '.article', '.post', '.entry', '.blog-post'
        ]
        
        for selector in content_selectors:
            if selector.startswith('.') or selector.startswith('#'):
                content = soup.select_one(selector)
            else:
                content = soup.find(selector)
                
            if content:
                main_content = content
                break
        
        # If we found main content, extract text from that
        if main_content:
            # Get text while preserving some structure
            paragraphs = main_content.find_all('p')
            if paragraphs:
                extracted_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
            else:
                extracted_text = main_content.get_text(separator='\n\n', strip=True)
        else:
            # Extract from body if main content not identified
            extracted_text = soup.body.get_text(separator='\n\n', strip=True)
        
        # Clean up the text
        lines = (line.strip() for line in extracted_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        extracted_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit length of extracted text to prevent very large outputs
        max_length = 8000
        if len(extracted_text) > max_length:
            extracted_text = extracted_text[:max_length] + "...\n[Content truncated due to length]"
            
        return f"Content from {url}:\n\n{extracted_text}"
    
    except requests.exceptions.RequestException as e:
        return f"Error browsing webpage {url}: {str(e)}"
    except Exception as e:
        return f"Error extracting content from {url}: {str(e)}"