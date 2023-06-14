from flask import Flask, request, jsonify
from datetime import datetime
import requests

current_orders = [31313,]

def dateConvert(isoDate):
    dt = datetime.fromisoformat(isoDate.replace("Z", "+00:00"))
    frt_date = dt.strftime("%A, %B %d %Y")
    human_date_time = f"{frt_date}"
    return human_date_time

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    order_id = data["queryResult"]["parameters"]["number"]
    api_url = "https://orderstatusapi-dot-organization-project-311520.uc.r.appspot.com/api/getOrderStatus"

    sendReq = {"orderId": order_id}
    response = requests.post(api_url, data=sendReq)
    
    try:
        if response.status_code == 200:
            order_id = int(order_id)
            if order_id in current_orders:
                date_data = response.json()
                ship_date = date_data.get("shipmentDate")
                if ship_date:
                    ship_date = dateConvert(ship_date)
                    fullfillment_reply = f"Your order {order_id} is scheduled to arrive on {ship_date}."
                else:
                    fullfillment_reply = f"Unable to determine shipment date for order {order_id}."
            else: 
                fullfillment_reply = f"Your order {order_id} is not valid!"
        else:
            fullfillment_reply = "Sorry, there was an error processing the request."
    except Exception as e:
        fullfillment_reply = "An error occurred while processing the request."
        print(f"Error: {str(e)}")

    return jsonify({"fulfillmentText": fullfillment_reply})

if __name__ == "__main__":
    app.run(debug=True)