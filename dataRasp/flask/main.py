from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/config', methods=['POST', 'GET'])
def config():
    if request.method == 'POST':
    	ssid = request.form['ssid']
    	password = request.form['pass']
    	email = request.form['email']
		auth = request.form['auth']
    	e = open('/home/pi/config/email.txt', 'w')
    	e.write(email)
    	e.close()

        a = open('/home/pi/config/auth.txt', 'w')
    	a.write(auth)
    	a.close()

    	s = open('/home/pi/config/ssidpass.txt', 'w')
    	s.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    	s.write('update_config=1\n')
    	s.write('country=US\n')
    	s.write('network={\n')
    	s.write('\tssid="{}"\n'.format(ssid))
    	s.write('\tpsk="{}"\n'.format(password))
    	s.write('\tscan_ssid=1\n')
    	s.write('}\n')
    	s.close()
    subprocess.call(
        'sudo cp /home/pi/config/ssidpass.txt /etc/wpa_supplicant/wpa_supplicant.conf', shell=True)
    return render_template('config.html')


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
