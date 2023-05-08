function filtrarTabla() {
  let input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("buscador");
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName("table")[0];
  tr = table.getElementsByTagName("tr");

  // Agrega una variable para contar los registros visibles
  let visibleRows = 0;

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
        visibleRows++;
      } else {
        tr[i].style.display = "none";
      }
    }
  }

  // Muestra u oculta el mensaje 'Registros no encontrados' según el número de registros visibles
  const noResultsElement = document.getElementById('no-results');
  if (visibleRows === 0) {
    noResultsElement.style.display = 'block';
  } else {
    noResultsElement.style.display = 'none';
  }
}


console.log("wena")