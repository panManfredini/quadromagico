from flask import Flask, request, jsonify, send_from_directory
import os
import datetime
import uuid
from image_processing import create_thumbnail_from_file, display_image, create_image_from_bytes
from sql import insert_image_sql_record
from threading import Thread
import time

app = Flask(__name__)

DISPLAY_OBJ = {
    "is_displaying" : False,
    "display_error" : "",
    "displaying_th" : None
}

STATIC_DIR = '/home/pan/Documents/quadromagico/quadro-magico-client/dist'
STATIC_DIR_IMAGES = '/home/pan/Documents/quadromagico/images'

class DisplayBusyException(Exception):
    pass

class DisplayErrorException(Exception):
    pass

def submit_display_thread(display_now:str,img_file_path:str,title:str):
    if display_now == "on" and DISPLAY_OBJ['is_displaying']:
            raise DisplayBusyException()
        
    elif display_now == "on" and not DISPLAY_OBJ['is_displaying']:
        DISPLAY_OBJ['displaying_th'] = Thread( target=display_image, args=(img_file_path, title, DISPLAY_OBJ) )
        DISPLAY_OBJ['displaying_th'].start()
        
        time.sleep(0.5) # 500 ms should be enough for a simple error to materialize I hope (the image stuff takes long).
        
        if DISPLAY_OBJ['is_displaying'] == False and DISPLAY_OBJ['display_error'] != "":
            raise DisplayErrorException(DISPLAY_OBJ['display_error'])



# Static files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    file_path = os.path.join(STATIC_DIR, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(STATIC_DIR, path)
    else:
        return 'File not found', 404

@app.route('/images/<path:path>')
def serve_static_images(path):
    file_path = os.path.join(STATIC_DIR_IMAGES, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(STATIC_DIR_IMAGES, path)
    else:
        return 'File not found', 404


# ---------------------  API ------------------------ #

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    '''
    POST PARAMS:
    - image: Binary
    - title: str
    - prompt: str
    - display_now: str  on, off
    '''
    image_file = request.files.get('image')
    title = request.form.get('title') or ""
    prompt = request.form.get('prompt') or ""
    display_now = request.form.get('display_now') or "off"
    display_now = display_now.lower()
    timestamp = datetime.datetime.now() 
    ID = timestamp.strftime('%Y%m%d_ID-') + str(uuid.uuid1())[:8]
    img_filename = f"IMG_{ID}.jpg"
    thb_filename = f"THB_{ID}.jpg"
    img_file_path = os.path.join(STATIC_DIR_IMAGES, img_filename)
    thb_file_path = os.path.join(STATIC_DIR_IMAGES, thb_filename)    
    
    try:        
        img = create_image_from_bytes(image_file)
        img.save(img_file_path,'JPEG')
        thumbnail = create_thumbnail_from_file(img_file_path)
        thumbnail.save(thb_file_path,'JPEG')
        
        insert_image_sql_record(timestamp, thb_file_path, img_file_path, title, prompt)
        submit_display_thread(display_now, img_file_path, title)
        
        return jsonify({'success': 'Image uploaded successfully'})
    except DisplayBusyException:
        return jsonify({'warning': 'Image update successfully, but display is busy. Riprovace.'})
    except DisplayErrorException as e:
        return jsonify({"error":f"Image uploaded correctly but error during display: {e}"})
    except Exception as e:
        return jsonify({'error': f'{e}'}), 500


@app.route('/api/is-displaying', methods=['GET'])
def is_displaying():
    global DISPLAY_OBJ
    if DISPLAY_OBJ['is_displaying'] == True:
        return jsonify({'is_display': True })
    
    elif DISPLAY_OBJ['display_error'] == "":
        return jsonify({'is_display':False, 'success': 'Image displayed successfully'})
    
    else:
        return jsonify({'is_display':False, 'error': f"Image display error: {DISPLAY_OBJ['display_error']}"})



        
if __name__ == '__main__':
    app.run(debug=True)
