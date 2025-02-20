import os
import pandas as pd
from flask import Flask, render_template, request, send_file
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

def executar_robo(origem, destino):
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Iniciar o ChromeDriver
    service = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=service, options=chrome_options)

    navegador.get('https://www.transvias.com.br')
    origem_input = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'OrigemDescricao')))

    origem_input.send_keys(origem)
    time.sleep(2)
    destino_input = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'DestinoDescricao')))
    destino_input.send_keys(destino)
    destino_input.send_keys(Keys.TAB)
    time.sleep(2)
    ActionChains(navegador).send_keys(Keys.ENTER).perform()

    SCROLL_PAUSE_TIME = 0.5
    last_height = navegador.execute_script('return document.body.scrollHeight')
    while True:
        navegador.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = navegador.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(1)

    email = []
    elements = navegador.find_elements('xpath', "//span[@title='E-mail']/a")
    for element in elements:
        email.append(element.text)
    navegador.quit()

    # Gerar arquivo Excel com os emails
    if email:
        # Nome do arquivo baseado na origem e destino
        nome_arquivo = f"{origem}_para_{destino}.xlsx"
        nome_arquivo = nome_arquivo.replace(" ", "_")  # Substituir espaços por _ no nome do arquivo
        df = pd.DataFrame(email, columns=["Email"])
        file_path = os.path.join(os.getcwd(), nome_arquivo)
        df.to_excel(file_path, index=False, engine='openpyxl')

    return email, file_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        origem = request.form["origem"]
        destino = request.form["destino"]
        resultado, file_path = executar_robo(origem, destino)
        # Se gerou o arquivo, enviar o link para download
        if resultado:
            return send_file(file_path, as_attachment=True)

        return render_template("index.html", resultado="Nenhum email encontrado")
    
    return render_template("index.html", resultado=None)

if __name__ == "__main__":
    app.run(debug=True)
