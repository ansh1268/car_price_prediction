// ==========================
// Dynamic Model Dropdown
// ==========================

function updateModels() {

    const company = document.getElementById("company").value;
    const modelSelect = document.getElementById("car_model");

    modelSelect.innerHTML = "";

    const models = [...new Set(
        carData
        .filter(car => car.company === company)
        .map(car => car.name)
    )];

    models.forEach(model => {

        const option = document.createElement("option");

        option.value = model;
        option.textContent = model;

        modelSelect.appendChild(option);

    });

    // First model ki image automatically load karo
    loadCarImage();

}



// ==========================
// Load Car Image
// ==========================

function loadCarImage() {

    const model = document.getElementById("car_model").value;

    fetch("/get_image?model=" + encodeURIComponent(model))

    .then(response => response.json())

    .then(data => {

        if(data.image){

            document.getElementById("carImage").src = data.image;

        }

        else{

            document.getElementById("carImage").src =
            "https://via.placeholder.com/500x250?text=No+Image";

        }

    })

    .catch(error=>{

        console.log(error);

    });

}



// ==========================
// Company Change
// ==========================

document.getElementById("company").addEventListener("change",function(){

    updateModels();

});



// ==========================
// Model Change
// ==========================

document.getElementById("car_model").addEventListener("change",function(){

    loadCarImage();

});



// ==========================
// Prediction
// ==========================

document.getElementById("predictForm").addEventListener("submit",function(e){

    e.preventDefault();

    let formData=new FormData(this);

    fetch("/predict",{

        method:"POST",
        body:formData

    })

    .then(response=>response.text())

    .then(price=>{

        document.getElementById("prediction").innerHTML=
        "💰 Predicted Price : ₹ "+Number(price).toLocaleString('en-IN');

    });

});

window.onload=function(){

    updateModels();

}