from flask import Flask, send_from_directory, jsonify
import random
import requests
import html

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

# API Endpoint for retreiving restaurants participating in the Eat Out To Help Out Scheme
# Requires a postcode
# Returns a list of restaurants in the format of:
# { restaurants: [["name", "address"], ["name", "address"]]}
@app.route("/getRestaurants/<postcode>", methods=["GET"])
def restaurants(postcode):
    postcode = str(postcode)

    # The list of registered restaurants within 5 miles of the specified postcode will be obtained from the government website.
    postcode = postcode.split(' ')
    url = 'https://www.tax.service.gov.uk/eat-out-to-help-out/find-a-restaurant/results?lookup=' + \
        postcode[0] + '+' + postcode[1]

    r = requests.get(url)
    r = r.text

    restaurants = []

    # The script will extract the site's data to obtain the restaurant's name and its corresponding address.
    for line in r.splitlines():
        if '<h3 class="govuk-heading-m"' in line:
            y = line.split('>')[1]
            y = y.split('<')[0]
            y = html.unescape(y)
        if 'govuk-results-address govuk-body' in line:
            x = line.split('>')[1]
            x = x.split('<')[0]
            x = html.unescape(x)
            result = (y, x)
            print(result)
            restaurants.append(result)

    print(len(restaurants))
    return jsonify({'restaurants': restaurants})


if __name__ == "__main__":
    app.run(debug=True)
