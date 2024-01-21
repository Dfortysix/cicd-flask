from flask import Flask, jsonify, request,render_template
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def hello():
   return render_template('index.html')

@app.route('/hello/<name>')
def hello_name(name):
   # Load current count
   f = open("count.txt", "r")
   count = int(f.read())
   f.close()
   # Increment the count
   count += 1
   # Overwrite the count
   f = open("count.txt", "w")
   f.write(str(count))
   f.close()

   return render_template('hello.html', name=name, count=count)

if __name__ == '__main__':
   app.run(host ='0.0.0.0', debug = True)