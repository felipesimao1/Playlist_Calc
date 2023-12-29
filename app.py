from flask import Flask, render_template, request
from pytube import Playlist

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular_tempo_total():
    url_playlist = request.form['url']
    horas_por_dia = float(request.form['horas_por_dia']) if request.form['horas_por_dia'] else 0

    try:
        playlist = Playlist(url_playlist)
        tempo_total = sum([video.length for video in playlist.videos])

        horas_total, minutos_total = divmod(tempo_total, 3600)
        minutos_total, segundos_total = divmod(minutos_total, 60)

        dias_necessarios = tempo_total / (3600 * horas_por_dia) if horas_por_dia > 0 else 0

        resultado = {
            "tempo_total": f"{int(horas_total)}:{int(minutos_total)}:{int(segundos_total)}",
            "dias_necessarios": round(dias_necessarios, 2)
        }
        return render_template('index.html', resultado=resultado, error=None)
    except Exception as e:
        return render_template('index.html', resultado=None, error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
