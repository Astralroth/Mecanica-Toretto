function filtrarTabla() {
  let nombreInput, precioInput, table, tr, tdNombre, tdPrecio, i, nombreValue, precioValue;
  nombreInput = document.getElementById("buscador");
  precioInput = document.getElementById("filtro-precio");
  table = document.getElementsByTagName("table")[0];
  tr = table.getElementsByTagName("tr");

  // Agrega una variable para contar los registros visibles
  let visibleRows = 0;

  for (i = 0; i < tr.length; i++) {
    tdNombre = tr[i].getElementsByTagName("td")[0];
    tdPrecio = tr[i].getElementsByTagName("td")[2];

    if (tdNombre && tdPrecio) {
      nombreValue = tdNombre.textContent || tdNombre.innerText;
      precioValue = tdPrecio.textContent || tdPrecio.innerText;

      const nombreFilter = nombreInput.value.trim().toUpperCase();
      const precioFilter = precioInput.value.trim();

      // Aplica el filtro del nombre
      const nombreMatch = nombreFilter === '' || nombreValue.toUpperCase().indexOf(nombreFilter) > -1;

      // Aplica el filtro del precio
      const precioMatch = precioFilter === '' || parseFloat(precioValue.replace('$', '')) <= parseFloat(precioFilter);

      if (nombreMatch && precioMatch) {
        tr[i].style.display = "";
        visibleRows++;
      } else {
        tr[i].style.display = "none";
      }
    }
  }

  // Muestra u oculta el mensaje 'Registros no encontrados' según el número de registros visibles
  const noResultsElement = document.getElementById("no-results");
  if (visibleRows === 0) {
    noResultsElement.style.display = "block";
  } else {
    noResultsElement.style.display = "none";
  }
}

