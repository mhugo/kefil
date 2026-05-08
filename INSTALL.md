# Installation instructions

1. Create a Python virtual environment
```
$ python -m venv venv
```

3. Activate it

```
$ source venv/bin/activate
```

4. Install required packages

```
$ pip install flask escpos
```

4. Launch the web application

```
$ python app.py
```

This should display something like:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 647-156-878
```

Now point a browser to http://127.0.0.1:5000 and you should see the application

5. (Optional) Autostart

Have a look at [start.sh](start.sh) and adapt it to your needs
