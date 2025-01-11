from flask import Flask, request, jsonify
from services.event_service import combined_search, get_event_image

app = Flask(__name__)

@app.route('/api/events/search', methods=['GET'])
def search_events():
    # Get query parameters
    params = request.args
    keyword = params.get('keyword')
    city = params.get('city')
    state_code = params.get('stateCode')
    start_date = params.get('startDate')
    end_date = params.get('endDate')
    segment = params.get('segment')

    # Perform the search
    result = combined_search(
        keyword=keyword,
        city=city,
        state_code=state_code,
        start_date=start_date,
        end_date=end_date,
        segment=segment,
    )
    return jsonify(result)

@app.route('/api/events/image/<event_id>', methods=['GET'])
def fetch_event_image(event_id):
    # Get event images using event ID
    result = get_event_image(event_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
