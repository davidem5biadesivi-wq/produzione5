
document.getElementById('nuovaLavorazioneForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Nuova lavorazione inserita per macchina: ' + document.getElementById('macchina').value);
});
