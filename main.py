import os

from groq import Groq
from dotenv import load_dotenv
from flask import Flask, render_template, request
from datetime import datetime

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


@app.route('/')
def main():
    return render_template('index.html')

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
    app.run(host='0.0.0.0')
