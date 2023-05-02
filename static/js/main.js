console.clear()
console.error("Alerta! Esta función del navegador está pensada para desarrolladores.");
console.error("No pegues ningún comando, pues se trata de un fraude.");


/*===: HANDLE LOGOUT :===*/
const logoutBtn = document.getElementById("logoutBtn");
const deleteBtn = document.getElementById("logoutBtn");

btnCerrarSesion.addEventListener('click', function() {
    fetch('/logout', {
      method: 'POST'
    })
    .then(response => {
      if (response.ok) {
        window.location.reload();
      }
    })
    .catch(error => {
      console.error(error);
    });
  });