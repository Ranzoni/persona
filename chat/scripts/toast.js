let toastsAmount = 0;

function showToast(message) {
  const $toast = document.createElement('div');
  $toast.id = `toast-${++toastsAmount}`;
  $toast.className = 'toast';
  const $toastMessage = document.createElement('div');
  $toastMessage.class = 'toast-message';
  $toast.appendChild($toastMessage);
  $toastMessage.textContent = message;

  document.body.appendChild($toast);
  
  $toast.classList.add('show');

  
  setTimeout(() => {
    hideToast(toastsAmount);

    setTimeout(() => {
        $toast.remove();
        toastsAmount--;
    });
  }, 5000);
}

function hideToast(toastIdx) {
  const $toast = document.getElementById(`toast-${toastIdx}`);
  $toast.classList.remove('show');
}
