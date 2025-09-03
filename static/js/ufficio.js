
document.getElementById('richiestaDataForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Richiesta di data inviata per lavorazione ID: ' + document.getElementById('idLavorazione').value);
});

function filtraMacchina() {
    const filtro = document.getElementById('macchinaFiltro').value;
    alert('Filtro applicato: ' + filtro);
}
