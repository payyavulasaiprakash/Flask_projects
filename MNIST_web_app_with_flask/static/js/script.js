const imageInput = document.getElementById('image-input');
const predictBtn = document.getElementById('predict-btn');
const predictionOutput = document.getElementById('prediction');
const errorOutput = document.getElementById('error');
const imageUploadLabel = document.getElementById('image-upload-label');
const uploadedImage = document.getElementById('uploaded-image');

imageUploadLabel.addEventListener('click', () => {
  imageInput.click();
});

imageInput.addEventListener('change', () => {
  if (imageInput.files.length > 0) {
    predictBtn.disabled = false;
    const file = imageInput.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      uploadedImage.src = reader.result;
      uploadedImage.style.display = 'block';
    };
    reader.readAsDataURL(file);
  } else {
    predictBtn.disabled = true;
    uploadedImage.src = '';
    uploadedImage.style.display = 'none';
  }
});

predictBtn.addEventListener('click', () => {
  const imageFile = imageInput.files[0];
  if (!imageFile) {
    errorOutput.textContent = 'Please select an image file.';
    return;
  }

  const formData = new FormData();
  formData.append('image', imageFile);

  fetch('/predict', {
    method: 'POST',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        predictionOutput.textContent = '';
        errorOutput.textContent = `Error: ${data.error}`;
      } else {
        predictionOutput.textContent = `Predicted digit: ${data.prediction}`;
        errorOutput.textContent = '';
        uploadedImage.src = `data:image/jpg;base64,${data.image_data}`;
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      predictionOutput.textContent = '';
      errorOutput.textContent = 'An error occurred. Please try again.';
    });
});