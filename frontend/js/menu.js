fetch('../templates/menu.html')
  .then(response => response.text())
  .then(html => {
    document.getElementById('menu-container').innerHTML = html;
  });