import os

from groq import Groq
from dotenv import load_dotenv
from flask import Flask, render_template, request
from datetime import datetime
from bs4 import BeautifulSoup
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

def ai_call(year):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user", 
                    "content": f"berikan saya fakta menarik tentang tahun {year} dalam 2-3 kalimat",
                }
            ],
            model="llama-3.1-8b-instant",
            stream=False
        )

        ai_output = chat_completion.choices[0].message.content
        return ai_output
    except Exception:
        return "Error, gagal mendapatkan data dari AI."

def filtering_news(media_name):
    class_name = ""
    element_name = ""

    if media_name == "bbc":
        element_name = "h2"
        class_name = "sc-feaf8701-3 eQumHa"
    elif media_name == "kompas":
        element_name = "h1"
        class_name = "hlTitle"
    elif media_name == "idntimes":
        element_name = "h1"
        class_name = "css-x8taim"

    return [element_name, class_name]


def scraping_news(media_name, url):
    response = requests.get(url)
    element = BeautifulSoup(response.content, 'html.parser')
    filter = filtering_news(media_name)
    element_name, class_name = filter[0], filter[1]

    headline = element.find(element_name, class_=class_name)
    return headline.text

@app.route('/')
def main():
    bbc = scraping_news("bbc", "https://www.bbc.com/news")
    kompas = scraping_news("kompas", "https://www.kompas.com/")
    idntimes = scraping_news("idntimes", "https://www.idntimes.com/")
    return render_template('index.html', bbc=bbc, kompas=kompas, idntimes=idntimes)

@app.route('/usia', methods=['GET', 'POST'])
def cek_usia():
    if request.method == 'POST':
        # Ambil data dari form
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir

        ai_output = ai_call(tahun_lahir)
        #print(ai_output)

        return render_template('cek_usia.html', usia=usia, tahun_lahir=tahun_lahir, ai_output=ai_output)
    return render_template('cek_usia.html', usia= None)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
