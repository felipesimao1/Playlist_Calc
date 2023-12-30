from flask import Flask, render_template, request
from pytube import Playlist

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_total_time():
    # Get playlist URL and daily study hours from the form
    playlist_url = request.form['url']
    hours_per_day = float(request.form['hours_per_day']) if request.form['hours_per_day'] else 0

    try:
        # Retrieve playlist information using pytube
        playlist = Playlist(playlist_url)
        total_time = sum([video.length for video in playlist.videos])

        # Convert total time to hours, minutes, and seconds
        total_hours, remaining_minutes = divmod(total_time, 3600)
        total_minutes, total_seconds = divmod(remaining_minutes, 60)

        # Calculate the number of days required to watch the playlist
        days_required = total_time / (3600 * hours_per_day) if hours_per_day > 0 else 0

        # Prepare the result in a dictionary
        result = {
            "total_time": f"{int(total_hours)}:{int(total_minutes)}:{int(total_seconds)}",
            "days_required": round(days_required, 2)
        }

        # Render the result on the 'index.html' template
        return render_template('index.html', result=result, error=None)
    except Exception as e:
        # Handle exceptions and render an error message on the template
        return render_template('index.html', result=None, error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
