import os
import re

from flask import request, url_for, json, Response
# from flask.ext.api import FlaskAPI, exceptions, status
from flask import Flask, jsonify

from Models.SlipData.SlipDataResponse import slip_data_response
from flask_api import status, exceptions
from services.OCRService.OCRService import *

app = Flask(__name__)

# Set up a directory to store uploaded images
UPLOAD_FOLDER = "resource/images/uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the directory if it doesn't exist
# Set a maximum file size to prevent large uploads (e.g., 16 MB)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

notes = {
    0: "do the shopping",
    1: "build the codez",
    2: "paint the door",
}


def note_repr(key):
    return {
        "url": request.host_url.rstrip("/") + url_for("notes_detail", key=key),
        "text": notes[key],
    }


@app.route("/OCR", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400
    # if "image" not in request.data:
    #     return jsonify({"error": "No file part"}), 400
    # if request.files != null:
    #     return jsonify({"error": "No file part"}), 400

    file = request.files["image"]  # Get the file from the POST request

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Validate the file type if needed (e.g., allow only PNG and JPEG)
    allowed_extensions = {"png", "jpg", "jpeg"}
    filename = file.filename.lower()
    extension = filename.rsplit(".", 1)[-1]

    if extension not in allowed_extensions:
        return jsonify({"error": "Invalid file type"}), 400

    # Save the file to the upload directory
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)  # Save the file

    # main()
    # Pattern to match Thai words, English words, or numbers
    pattern = r"[a-zA-Z,-,]+|[\u0E00-\u0E7F]+|\d+"
    pattern1 = r"([a-zA-Z]+|[\u0E00-\u0E7F]+|\d+|\.|-)"
    # file.filename
    txt = prepareimage(file.filename)
    txt_strip = txt.strip(' ')
    txt_split = txt.split('\n')

    res = []
    for sub in txt_split:
        res.append(sub.replace('"', ""))

    res1 = []
    for txt_ele in res:
        if len(txt_ele) != 0:
            # txt_clear = re.findall(pattern1, txt_ele)
            res1.append(txt_ele)
        # if(txt_ele == '"'):
        #  txt_split.remove(' ')

    slip_bank_name = fine_slip_name(file.filename)
    field_value = []
    if slip_bank_name == 'kbank_1':
        if res1 != [] and len(res1) >= 2:
            str_data = "fromacc" + res1[2]
            field_value.append(str_data)
        else:
            str_data = "fromacc" + res1[2]
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 3:
            str_data = "frombank" + res1[3]
            field_value.append(str_data)
        else:
            str_data = "frombank"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 4:
            str_data = "fromaccno" + res1[4]
            field_value.append(str_data)
        else:
            str_data = "fromaccno"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 5:
            str_data = "to" + res1[5]
            field_value.append(str_data)
        else:
            str_data = "to"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 6:
            str_data = "tobank" + res1[6]
            field_value.append(str_data)
        else:
            str_data = "tobank"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 7:
            str_data = "toaccno" + res1[7]
            field_value.append(str_data)
        else:
            str_data = "toaccno"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 10:
            str_data = "transactionno" + res1[10]
            field_value.append(str_data)
        else:
            str_data = "transactionno"
            field_value.append(str_data)
        if res1 != [] and len(res1) > 12:
            str_data = "amount" + res1[12]
            field_value.append(str_data)
        else:
            str_data = "amount"
            field_value.append(str_data)
    elif slip_bank_name == 'kbank_2':
        if res1 != [] and len(res1) >= 2:
            str_data = "from :" + res1[2]
            field_value.append(str_data)
        else:
            str_data = "fromacc :" + res1[2]
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 3:
            str_data = "from bank :" + res1[3]
            field_value.append(str_data)
        else:
            str_data = "from bank :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 4:
            str_data = "from acc no :" + res1[4]
            field_value.append(str_data)
        else:
            str_data = "from acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 4:
            str_data = "to :" + res1[4]
            field_value.append(str_data)
        else:
            str_data = "to :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 5:
            str_data = "to bank :" + res1[5]
            field_value.append(str_data)
        else:
            str_data = "to bank :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 7:
            str_data = "to acc no :" + res1[7]
            field_value.append(str_data)
        else:
            str_data = "to acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 9:
            str_data = "transaction no :" + res1[9]
            field_value.append(str_data)
        else:
            str_data = "transaction no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 11:
            str_data = "amount :" + res1[11]
            field_value.append(str_data)
        else:
            str_data = "amount :"
            field_value.append(str_data)
    elif slip_bank_name == 'kbank_3':
        #promtpay
        if res1 != [] and len(res1) >= 2:
            str_data = "from :" + res1[2]
            field_value.append(str_data)
        else:
            str_data = "from :" + res1[2]
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 3:
            str_data = "from bank :" + res1[3]
            field_value.append(str_data)
        else:
            str_data = "from bank :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 4:
            str_data = "from acc no :" + res1[4]
            field_value.append(str_data)
        else:
            str_data = "from acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 5:
            str_data = "to :" + res1[5]
            field_value.append(str_data)
        else:
            str_data = "to :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 6:
            str_data = "to bank : Promptpay"
            field_value.append(str_data)
        else:
            str_data = "to bank : Promptpay"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 7:
            str_data = "to acc no :" + res1[7]
            field_value.append(str_data)
        else:
            str_data = "to acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 10:
            str_data = "transaction no :" + res1[10]
            field_value.append(str_data)
        else:
            str_data = "transaction no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 12:
            str_data = "amount :" + res1[12]
            field_value.append(str_data)
        else:
            str_data = "amount :"
            field_value.append(str_data)
    elif slip_bank_name == 'kbank_4':
        if res1 != [] and len(res1) >= 2:
            str_data = "from :" + res1[2]
            field_value.append(str_data)
        else:
            str_data = "from :" + res1[2]
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 3:
            str_data = "from bank :" + res1[3]
            field_value.append(str_data)
        else:
            str_data = "from bank :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 4:
            str_data = "from acc no :" + res1[4]
            field_value.append(str_data)
        else:
            str_data = "from acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 5:
            str_data = "to :" + res1[5]
            field_value.append(str_data)
        else:
            str_data = "to :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 6:
            str_data = "to bank :" + res1[6]
            field_value.append(str_data)
        else:
            str_data = "to bank :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 7:
            str_data = "to acc no :" + res1[7]
            field_value.append(str_data)
        else:
            str_data = "to acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 9:
            str_data = "transaction no :" + res1[9]
            field_value.append(str_data)
        else:
            str_data = "transaction no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 11:
            str_data = "amount :" + res1[11]
            field_value.append(str_data)
        else:
            str_data = "amount :"
            field_value.append(str_data)
    elif slip_bank_name == 'scb_1':
        # promptpay
        if res1 != [] and len(res1) >= 3:
            str_data = "from :" + res1[3]
            field_value.append(str_data)
        else:
            str_data = "from :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 0:
            str_data = "from bank : SCB"
            field_value.append(str_data)
        else:
            str_data = "from bank : SCB"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 4:
            str_data = "from acc no :" + res1[4]
            field_value.append(str_data)
        else:
            str_data = "from acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 5:
            str_data = "to :" + res1[5]
            field_value.append(str_data)
        else:
            str_data = "to :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 0:
            str_data = "to bank :"
            field_value.append(str_data)
        else:
            str_data = "to bank :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 6:
            str_data = "to acc no :" + res1[6]
            field_value.append(str_data)
        else:
            str_data = "to acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 2:
            str_data = "transaction no :" + res1[2]
            field_value.append(str_data)
        else:
            str_data = "transaction no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) > 7:
            str_data = "amount :" + res1[7]
            field_value.append(str_data)
        else:
            str_data = "amount :"
            field_value.append(str_data)
    elif slip_bank_name == 'bbl_1':
        if res1 != [] and len(res1) >= 5:
            str_data = "from :" + res1[5]
            field_value.append(str_data)
        else:
            str_data = "from :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 7:
            str_data = "from bank :" + res1[7]
            field_value.append(str_data)
        else:
            str_data = "from bank :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 6:
            str_data = "from acc no :" + res1[6]
            field_value.append(str_data)
        else:
            str_data = "from acc no :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 8:
            str_data = "to :" + res1[8]
            field_value.append(str_data)
        else:
            str_data = "to :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 0:
            str_data = "to bank : Promptpay"
            field_value.append(str_data)
        else:
            str_data = "to bank : Promptpay"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 9:
            str_data = "to acc no :" + res1[9]
            field_value.append(str_data)
        else:
            str_data = "toaccno :"
            field_value.append(str_data)
        if res1 != [] and len(res1) >= 15:
            str_data = "transactionno:" + res1[15]
            field_value.append(str_data)
        else:
            str_data = "transactionno :"
            field_value.append(str_data)
        if res1 != [] and len(res1) > 4:
            str_data = "amount :" + res1[4]
            field_value.append(str_data)
        else:
            str_data = "amount :"
            field_value.append(str_data)
    else:
        field_value = res1

    # slip_data_response.from_dict(field_value)
    n_txt = str(txt_split)

    n_txt = re.findall(pattern1, n_txt)
    # json_string = json.dump(txt, ensure_ascii=False)
    size = len(txt_split)
    data = request.form.get('text')
    # jsonify(txt)
    response = Response(
        response=json.dumps(field_value, ensure_ascii=False),
        status=200,
        mimetype="application/json"  # Sets the content type
    )
    return response
    # return json.dumps(res1 ,ensure_ascii=False)


@app.route("/", methods=["GET", "POST"])
def notes_list():
    """
    List or create notes.
    """
    if request.method == "POST":
        note = str(request.data.get("text", ""))
        idx = max(notes.keys()) + 1
        notes[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]


@app.route("/<int:key>/", methods=["GET", "PUT", "DELETE"])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == "PUT":
        note = str(request.data.get("text", ""))
        notes[key] = note
        return note_repr(key)

    elif request.method == "DELETE":
        notes.pop(key, None)
        return "", status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    app.run(debug=True)
