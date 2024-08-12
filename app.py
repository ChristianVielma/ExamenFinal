import requests  
from flask import Flask, render_template, request  

app = Flask(__name__)  

@app.route('/', methods=['GET', 'POST'])  
def index():  
    conversion_result = None  
    last_updated = None  
    if request.method == 'POST':  
        amount = request.form.get('amount')  
        from_currency = request.form.get('from_currency')  
        to_currency = request.form.get('to_currency')  

        try:  
            amount = float(amount)  # Convertir a float  
            conversion_result, last_updated = convert_currency(amount, from_currency, to_currency)  
        except ValueError:  
            conversion_result = "Por favor, ingresa un número válido."  

        # Maneja el caso en que `conversion_result` sea None  
        if conversion_result is None:  
            conversion_result = "Error al hacer la conversión."  

    return render_template('index.html', conversion_result=conversion_result, last_updated=last_updated)  

def convert_currency(amount, from_currency, to_currency):  
    api_key = '5d594ee0fea1e4b4eec9551e'  # Reemplaza 'TU_API_KEY' con tu clave de API  
    url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'  
    response = requests.get(url)  

    if response.status_code != 200:  
        return None, "Error al obtener datos de la API"  

    data = response.json()  
    rate = data['rates'].get(to_currency)  # Usar get para evitar KeyError  
    
    if rate is None:  
        return None, "Moneda a la que se quiere convertir no válida."  
    
    last_updated = data['date']  
    return round(amount * rate, 2), last_updated  

if __name__ == '__main__':  
    app.run(debug=True)