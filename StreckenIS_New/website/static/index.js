function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function deleteTrainstation(trainstationId) {
  fetch("/delete-trainstation", {
    method: "POST",
    body: JSON.stringify({ trainstationId: trainstationId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}