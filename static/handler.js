document.getElementById('upload-form').addEventListener('submit', function(e) {
        var imageFile = document.getElementById('imageFile');
        var videoFile = document.getElementById('videoFile');
        var formAction = '';

        if (imageFile.files.length > 0) {
            formAction = detectImageUrl;
        } else if (videoFile.files.length > 0) {
            formAction = detectVideoUrl;
        } else {
            e.preventDefault();
            return false;
        }

        // Встановлення action для форми і продовження відправлення
        this.action = formAction;
    });

     document.addEventListener("DOMContentLoaded", function() {
      // Відслідковування змін у полі введення файлу
      document.getElementById('imageFile').addEventListener('change', function(event) {
        var fileName = event.target.files[0].name; // Отримання імені файлу
        var nextSibling = event.target.nextElementSibling; // Отримання мітки
        nextSibling.innerText = fileName; // Оновлення тексту мітки

        // Оновлення стану кнопки
        var submitButton = document.getElementById('submit-button');
        if (event.target.files.length > 0) {
          submitButton.removeAttribute('disabled'); // Активація кнопки
        } else {
          submitButton.setAttribute('disabled', 'disabled'); // Деактивація кнопки
        }
      });
    });

    document.addEventListener("DOMContentLoaded", function() {
      // Відслідковування змін у полі введення файлу відео
      document.getElementById('videoFile').addEventListener('change', function(event) {
        var fileName = event.target.files[0].name; // Отримання імені файлу
        var nextSibling = event.target.nextElementSibling; // Отримання мітки
        nextSibling.innerText = fileName; // Оновлення тексту мітки

        // Оновлення стану кнопки відправки для відео
        var submitButton = document.getElementById('submit-video-button');
        if (event.target.files.length > 0) {
          submitButton.removeAttribute('disabled'); // Активація кнопки
        } else {
          submitButton.setAttribute('disabled', 'disabled'); // Деактивація кнопки
        }
      });
    });
