from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import requests

app = Flask(__name__)

# Load Dataset
car = pd.read_csv("Cleaned_Car_data.csv")

# Load Model
model = pickle.load(open("LinearRegressionModel.pkl", "rb"))

# Pexels API Key
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"


@app.route("/")
def index():

    companies = sorted(car["company"].dropna().unique())
    car_models = sorted(car["name"].dropna().unique())
    years = sorted(car["year"].dropna().unique(), reverse=True)
    fuel_types = sorted(car["fuel_type"].dropna().unique())

    # JavaScript ke liye data
    car_data = car[["company", "name"]].drop_duplicates().to_dict(orient="records")

    return render_template(
        "index.html",
        companies=companies,
        car_models=car_models,
        years=years,
        fuel_types=fuel_types,
        car_data=car_data
    )


@app.route("/predict", methods=["POST"])
def predict():

    company = request.form.get("company")
    car_model = request.form.get("car_model")
    year = int(request.form.get("year"))
    fuel_type = request.form.get("fuel_type")
    kms_driven = int(request.form.get("kilo_driven"))

    input_df = pd.DataFrame(
        [[car_model, company, year, kms_driven, fuel_type]],
        columns=[
            "name",
            "company",
            "year",
            "kms_driven",
            "fuel_type"
        ]
    )

    prediction = model.predict(input_df)

    return str(round(prediction[0], 2))


@app.route("/get_image")
def get_image():

    model_name = request.args.get("model")

    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": model_name + " car",
        "per_page": 1
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    image_url = ""

    if "photos" in data and len(data["photos"]) > 0:
        image_url = data["photos"][0]["src"]["large"]

    return jsonify({
        "image": image_url
    })


if __name__ == "__main__":
    app.run(debug=True)