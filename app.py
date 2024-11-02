from flask import Flask, request, send_file
from rembg import remove,new_session
import io
import os from environ

app = Flask(__name__)
hum_seg_session = new_session(model_name='u2net_human_seg')

@app.route('/api/remove-background', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return {'error': 'No image uploaded'}, 400

        file = request.files['image']
        
        if file.filename == '':
            return {'error': 'No selected file'}, 400
            
        input_image = file.read()
        output_image = remove(input_image,session=hum_seg_session)
        
        output_buffer = io.BytesIO()
        output_buffer.write(output_image)
        output_buffer.seek(0)
        
        return send_file(
            output_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='removed_background.png'
        )
        
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    PORT = environ.get("PORT","5000")
    app.run(host='0.0.0.0', port=int(PORT))
