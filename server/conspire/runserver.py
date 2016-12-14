from conspire import app

app.secret_key = 'hogehogehoge'
app.config['SESSION_TYPE'] = 'filesystem'
app.run(debug=True)
