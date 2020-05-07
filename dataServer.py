from flask import Flask, request, jsonify, render_template
from PIL import Image
app = Flask(__name__)


# each camera will send images at certain time intervals as
# POST requests that will be handled as below.
# The server will write the image to the directory and add the image name
# along with the timestamp to a global queue.

buffer = []

@app.route('/send', methods=['POST'])
def writeFile():
    global buffer

    #save file
    file = request.files['file']
    filename = file.filename
    file.save('images/'+filename)

    if len(buffer) <= 4:
        buffer.append(filename)
    else:
        f = open("globalQueue.txt", "a+")
        f.write(','.join(buffer))
        f.close()

        buffer = []
    print(buffer)


    return jsonify({"state":1})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port= 5000,debug=True)
