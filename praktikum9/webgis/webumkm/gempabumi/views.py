import json
import urllib.request
from datetime import datetime
from django.shortcuts import render

def gempaterkini(request):
    url = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
    daftar_gempa = []
    error_msg = None

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_data = json.loads(response.read().decode('utf-8'))
            gempa_list = raw_data.get('Infogempa', {}).get('gempa', [])[:15]

            for idx, item in enumerate(gempa_list, start=1):
                coords = item.get('Coordinates', '0,0').split(',')
                lat = float(coords[0].strip())
                lon = float(coords[1].strip())
                mag = float(item.get('Magnitude', 0))
                kedalaman_str = item.get('Kedalaman', '0 km')
                kedalaman_km = float(kedalaman_str.replace('km', '').strip())

                daftar_gempa.append({
                    'no': idx,
                    'tanggal': item.get('Tanggal', ''),
                    'jam': item.get('Jam', ''),
                    'lat': lat,
                    'lon': lon,
                    'magnitude': mag,
                    'kedalaman_str': kedalaman_str,
                    'kedalaman_km': kedalaman_km,
                    'wilayah': item.get('Wilayah', ''),
                    'potensi': item.get('Potensi', ''),
                })
    except Exception as e:
        error_msg = f"Gagal mengambil data BMKG: {str(e)}"

    context = {
        'daftar_gempa': daftar_gempa,
        'gempa_json': json.dumps(daftar_gempa),
        'waktu_update': datetime.now().strftime("%H.%M.%S"),
        'error_msg': error_msg,
    }
    return render(request, 'gempabumi/gempaterkini.html', context)