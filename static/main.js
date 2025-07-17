// function uploadFiles() {
//   const input = document.getElementById('fileInput');
//   const formData = new FormData();

//   for (let i = 0; i < input.files.length && i < 5; i++) {
//     formData.append(files, input.files[i]);
//   }

//   fetch('/upload', {
//     method: 'POST',
//     body: formData
//   })
//   .then(res => res.json())
//   .then(data => {
//     document.getElementById('result').textContent = JSON.stringify(data, null, 2);
//   })
//   .catch(error => {
//     document.getElementById('result').textContent = '오류 발생: ' + error;
//   });
// }
