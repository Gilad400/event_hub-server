import requests

api_key = "my_api_key"
url = "https://app.ticketmaster.com/discovery/v2/events.json"


def search_by_keyword(keyword):
    """Search events by keyword"""
    params = {
        'apikey': api_key,
        'keyword': keyword
    }
    return _make_request(params)

def search_by_id(id):
    """Search events by id"""
    params = {
        'apikey': api_key,
        'id': id
    }
    return _make_request(params)

def combined_search(keyword=None, city=None, state_code=None, 
                    start_date=None, end_date=None, segment=None):
    """Combine multiple search criteria"""
    params = {'apikey': api_key}
        
    if keyword:
        params['keyword'] = keyword
    if city:
        params['city'] = city
    if state_code:
        params['stateCode'] = state_code
    if start_date:
        params['startDateTime'] = start_date
    if end_date:
        params['endDateTime'] = end_date
    if segment:
        params['segmentName'] = segment
           
    return _make_request(params)
    
def get_event_image(event_id):
    response = search_by_id(event_id)
    #look inside the jason response
    embedded = response.get('_embedded', {})
    events = embedded.get('events', [])
    if events:
        event = events[0]
        images = event.get("images", [])
    if len(images) != 0:
        #return images[0].get("url", "No image URL found.")
        #get list of images
        return [image.get("url", "No image URL found.") for image in images] 
    
    return "No images available for this event."

def _make_request(params):
    """Make the API request and handle the response"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

#testing
if __name__ == "__main__":
    # Search for events using combined search
    search_results = combined_search(
        keyword="football"
    )
    
    # Extract the first event's ID (if available)
    events = search_results.get("_embedded", {}).get("events", [])
    if events:
        first_event_id = events[0].get("id")
        print("First Event ID:", first_event_id)
        
        # Fetch and display event details by ID
        if first_event_id:
            #event_details = search_by_id(first_event_id)
            #print("Event Details:", event_details)
            
            # Fetch and display the event's image
            image_url = get_event_image(first_event_id)
            print("Event Image URL:", image_url)
        else:
            print("No valid event ID found.")
    else:
        print("No events found.")
    