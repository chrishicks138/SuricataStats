from flask import Flask, redirect, url_for, request, render_template
import random

app = Flask(__name__)

first = '| Total                     |'
date = 'Date: '

labels = []

def logParse():
    colors = []
    colorint = {}
    keys = []
    dictvalues = {}
    with open('/var/log/suricata/stats.log') as logfile:
        lines = logfile.readlines()
        for line in lines[::128]:
            if date in line:
                line = line.split(' (up')[0].replace('Date: ', '').replace('-', '').replace(' ', '_')
                if line not in labels:
                    labels.append(line)
            if first in line:
                line = line.replace(first, ':').replace('\n', '').replace(' ', '')
                key  = line.split(':')[0]
                value = int(line.split(':')[1])
                if key not in keys:
                    for x in range(3):
                        colorint[x] = random.randint(0,255)
                    string = "rgba("+str(colorint[0])+","+str(colorint[1])+","+str(colorint[2])+",1)"
                    keys.append(key)
                    colors.append(string)
                try:
                    dictvalues[key].append(value)
                except:
                    dictvalues[key] = []
    return dictvalues, colors

@app.route('/')
def hello_world():
    dictvalues = logParse()
    colors = dictvalues[1]
    dictvalues = dictvalues[0]
    values = list(dictvalues.values())
    legends = list(dictvalues.keys())
    counted = [i for i in range(len(list(dictvalues.keys()))) ]
    data = [ legends, labels, values ]
    return render_template('index.html', colors=colors, data=data, counted=counted)

  
if __name__ == '__main__':
  
    app.run(host="0.0.0.0", port=3001)
