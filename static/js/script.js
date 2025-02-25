// Basic JS to handle profile image modal display
document.addEventListener('DOMContentLoaded', function () {
  const profileImg = document.getElementById('profilePicture');
  const modal = document.getElementById('profileModal');
  const modalImg = document.getElementById('modalProfileImage');
  const closeBtn = document.querySelector('.modal .close');

  if(profileImg) {
    profileImg.addEventListener('click', function() {
      modal.style.display = 'block';
      modalImg.src = this.src;
    });
  }

  if(closeBtn) {
    closeBtn.addEventListener('click', function() {
      modal.style.display = 'none';
    });
  }
});
