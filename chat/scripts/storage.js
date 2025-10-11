function saveId(id) {
    localStorage.setItem('id', id);
}

function getId() {
  return localStorage.getItem('id');
}