from flask import Flask, redirect, url_for, request, render_template
import random

app = Flask(__name__)

first = '| Total                     |'
date = 'Date: '
listvalues = []
labels = []
colors = []
with open('/var/log/suricata/stats.log') as logfile:
    lines = logfile.readlines()
    keys = [ ]
    dictvalues = {}
    for line in lines[::256]:
        if date in line:
            labels.append(line.split(' (up')[0].replace('Date: ', '').replace('-', '').replace(' ', '_'))
        if first in line:
            line = line.replace(first, ':').replace('\n', '').replace(' ', '')
            key  = line.split(':')[0]
            value = int(line.split(':')[1])
            if key not in keys:
                color = random.randint(0,255)
                color1 = random.randint(0,255)
                color2 = random.randint(0,255)
                string = "rgba("+str(color)+","+str(color1)+","+str(color2)+",1)"
                keys.append(key)
                colors.append(string)
            try:
                dictvalues[key].append(value)
            except:
                dictvalues[key] = []
        listvalues.append(dictvalues)



@app.route('/')
def hello_world():
    values = list(dictvalues.values())
    legends = keys
    counted = [i for i in range(len(keys))]
    data = [ legends, labels, values ]
    return render_template('index.html', colors=colors, data=data, counted=counted)

  
if __name__ == '__main__':
  
    app.run(host="0.0.0.0", port=3001)
