from flask import Flask, request, jsonify

app = Flask(__name__)

# Pricing based on pizza size, toppings, and flavor
pricing = {
    'size': {
        'small': 5,
        'medium': 8,
        'large': 12
    },
    'flavors': {
        'cheese': 2,
        'pepperoni': 3,
        'veggie': 2.5
    },
    'toppings': {
        'olives': 0.5,
        'mushrooms': 0.7,
        'extra_cheese': 1,
        'pepperoni': 1.5
    }
}

def calculate_bill(size, flavor, toppings):
    size_cost = pricing['size'].get(size.lower(), 0)
    flavor_cost = pricing['flavors'].get(flavor.lower(), 0)
    toppings_cost = sum(pricing['toppings'].get(topping.lower(), 0) for topping in toppings)
    
    total_cost = size_cost + flavor_cost + toppings_cost
    return total_cost

@app.route('/calculate_bill', methods=['POST'])
def calculate():
   
    data = request.json
    print(data)

    parameters = data.get('queryResult', {}).get('parameters', {})

    size = parameters.get('size')
    print(size)
    flavor = parameters.get('Pizza_Flavour')
    print(flavor)
    # toppings = parameters.get('topping', [])
    # print(toppings)

    toppings = parameters.get('topping')
    if isinstance(toppings, str):
     toppings = [toppings]  # Convert single string to list
    print(toppings)
    
    if not size or not flavor:
        print("Error")
        return jsonify({"error": "Size and flavor are required"}), 400
        

    total_cost = calculate_bill(size, flavor, toppings)

    if 'no' in toppings:
        toppings = 'no'
    else:
        toppings = ', '.join(toppings)
    
    response = {
        'fulfillmentText': f"The total bill for your {size}  pizza with {toppings} toppings and {flavor} flavor is {total_cost:.2f}."
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True,port=5002)
