const openPopupBtn = document.getElementById('openPopupBtn');
const closePopupBtn = document.getElementById('closePopupBtn');
const popup = document.getElementById('popup');

openPopupBtn.addEventListener('click', function() {
    popup.style.display = 'flex';
});

closePopupBtn.addEventListener('click', function() {
    popup.style.display = 'none';
});