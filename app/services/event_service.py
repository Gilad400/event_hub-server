import requests

api_key = "rJl9LnZCTj5lHVrGDbdObgTiRRmlnSdk"
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
        params['startDateTime'] = f"{start_date}T00:00:00Z"
    if end_date:
        params['endDateTime'] = f"{end_date}T23:59:59Z"
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