from bs4 import BeautifulSoup
import requests
import datetime
import time

request = requests.get('https://www.ivoox.com/podcast-tak-tak-duken-podcast_fg_f1154471_filtro_1.xml')
feed = BeautifulSoup(request.text, 'html.parser')

itunes_duration_elements = feed.find_all('itunes:duration')

total_seconds = 0

try:
    time.strptime(itunes_duration_elements[0].string, '%H:%M:%S')
    time_format = '%H:%M:%S'
except Exception:
    print('Probando otro metodo de parseo...')
    if itunes_duration_elements[0].find('.') != -1:
        time_format = 'seconds.number'
    else:
        time_format = 'seconds'

for element in itunes_duration_elements:
    if time_format == 'seconds':
        total_seconds = total_seconds + int(element.text)
    elif time_format == 'seconds.number':
        total_seconds = total_seconds + int(element.text.split('.')[0])
    else:
        episode_time = time.strptime(element.string, time_format)
        total_seconds = total_seconds + int(((episode_time.tm_hour * 60) * 60)) + int((episode_time.tm_min * 60)) + int(
            episode_time.tm_sec)


time_object = datetime.timedelta(seconds=total_seconds)
avg_duration = datetime.timedelta(seconds=(total_seconds / len(itunes_duration_elements)))

print('El podcast dura un total de:')
print(str(total_seconds) + ' segundos')
print('O')
print(time_object)
print('La duracion promedio de un episodeo es de: ' + str(avg_duration))



