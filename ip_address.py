import requests

# response = requests.get("http://ip-api.com/json/24.48.0.1").json()
# print(response)
# print(response['lat'])
# print(response['lon'])


# {"query": "167.71.3.72"},
#         {"query": "206.189.198.234"},
#         {"query": "157.230.75.212"},
def get_ip_address():
    response = requests.post("http://ip-api.com/batch", json=[
        {"query": "208.80.152.201"},


    ]).json()
    for ipinfo in response:
        lat=ipinfo['lat']
        lon=ipinfo['lon']
        return [lat,lon]
    #
    # / *setInterval(() = > {
    #     fetch("/get_accident_probability")
    #
    #         .then(res= > res.json())
    # .then(data= > {
    #     console.log(data.accident_prob)
    # const
    # threshold = 0.95; // set
    # your
    # threshold
    # here
    # console.log(data.accident_prob < threshold)
    # if (data.accident_prob < threshold)
    # {
    #
    #     document.getElementById("alert-button1").display = "visible"
    #
    # } else {
    #
    #     document.getElementById("alert-button1").display = "none";
    #
    # }
    #
    # });
    # }, 1000); * /