from App import app
import os 

if __name__ == 'main':
    porta =int(os.getenv('PORT'),'5000')
    app.run(host='0.0.0.0',port=porta)