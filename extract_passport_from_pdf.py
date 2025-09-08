#!/usr/bin/env python3
if len(approx) == 4:
pts = approx.reshape(4,2).astype('float32')
(x,y,w,h) = cv2.boundingRect(pts)
if w == 0 or h == 0:
continue
ar_ok = aspect_ratio_ok(w, h)
if not ar_ok and area < page_area * 0.05:
continue
warped = four_point_transform(orig, pts)
if warped.shape[0] < warped.shape[1]:
warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)
candidates.append((area, warped))
candidates = sorted(candidates, key=lambda x: x[0], reverse=True)
crops = [c[1] for c in candidates]
return crops




@app.route('/upload', methods=['POST'])
def upload_pdf():
if 'file' not in request.files:
return jsonify({'error': 'no file uploaded (use form field "file")'}), 400
f = request.files['file']
if f.filename == '':
return jsonify({'error': 'empty filename'}), 400
with TemporaryDirectory() as td:
in_path = Path(td) / 'input.pdf'
f.save(str(in_path))
images = convert_from_path(str(in_path), dpi=DPI)
saved = []
for i, pil_page in enumerate(images, start=1):
page_img = convert_pdf_page_to_cv2_image(pil_page)
crops = find_passport_candidates(page_img)
for j, crop in enumerate(crops, start=1):
out_name = f'page_{i:03d}_passport_{j:02d}.jpg'
rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
im = Image.fromarray(rgb)
buf = io.BytesIO()
im.save(buf, format='JPEG', quality=95)
buf.seek(0)
saved.append((out_name, buf.read()))
if not saved:
return jsonify({'error': 'no passport-like region detected'}), 404
# if one image -> return directly
if len(saved) == 1:
name, data = saved[0]
return send_file(io.BytesIO(data), mimetype='image/jpeg', as_attachment=True, download_name=name)
# else return a zip
zip_buf = io.BytesIO()
with zipfile.ZipFile(zip_buf, 'w') as zf:
for name, data in saved:
zf.writestr(name, data)
zip_buf.seek(0)
return send_file(zip_buf, mimetype='application/zip', as_attachment=True, download_name='passports.zip')




if __name__ == '__main__':
port = int(os.environ.get('PORT', 8000))
app.run(host='0.0.0.0', port=port)
