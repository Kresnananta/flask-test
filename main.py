from flask import Flask, render_template, request
app = Flask(__name__)

# rute / page masuk utama
@app.route("/")
def main():
    web_title = "Home"
    return render_template('home.html', web_title=web_title)

# page about
@app.route("/about")
def about():
    web_title = "About"
    return render_template('about.html', web_title=web_title)

@app.route("/usia", methods=['GET', 'POST'])
def usia():
    web_title = "Cek Usia"
    usia_anda = None
    # ngambil inputan tiap POST
    if request.method == 'POST':
        # dari name/var input di html
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = 2026
        usia_anda = tahun_sekarang - tahun_lahir
    
    return render_template('usia.html', web_title=web_title, usia_anda=usia_anda)

if __name__ == '__main__':
    app.run()

