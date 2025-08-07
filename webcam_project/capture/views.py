# capture/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CapturedImageForm
from .models import CapturedImage

import face_recognition
import os
import base64
import io
from PIL import Image
import numpy as np
import pickle
import json

REFERENCE_ENCODING_PATH = 'media/reference_encoding.pkl'

def capture_photo(request):
    if request.method == 'POST':
        form = CapturedImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()

            image_path = image_instance.image.path
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            if not face_locations:
                return render(request, 'capture/capture.html', {
                    'form': form,
                    'error': 'No face detected in the uploaded image.'
                })

            encoding = face_recognition.face_encodings(image)[0]
            with open(REFERENCE_ENCODING_PATH, 'wb') as f:
                pickle.dump(encoding, f)

            return redirect('face_tracking')
    else:
        form = CapturedImageForm()

    return render(request, 'capture/capture.html', {'form': form})

def face_tracking_view(request):
    return render(request, 'capture/track.html')

def face_check_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)

            face_locations = face_recognition.face_locations(image_np)
            if not face_locations:
                return JsonResponse({'message': 'No face detected'})

            current_encoding = face_recognition.face_encodings(image_np)[0]

            if not os.path.exists(REFERENCE_ENCODING_PATH):
                return JsonResponse({'message': 'Reference encoding not found'})

            with open(REFERENCE_ENCODING_PATH, 'rb') as f:
                reference_encoding = pickle.load(f)

            match = face_recognition.compare_faces([reference_encoding], current_encoding)[0]

            if match:
                return JsonResponse({'message': 'Face verified ✅'})
            else:
                return JsonResponse({'message': 'Face does not match ❌'})

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'})

    return JsonResponse({'message': 'Invalid request method'})
