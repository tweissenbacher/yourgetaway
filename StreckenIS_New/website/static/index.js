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
    window.location.href = "/all_trainstations";
  });
}
function deleteSection(sectionId) {
  fetch("/delete-section", {
    method: "POST",
    body: JSON.stringify({ sectionId: sectionId }),
  }).then((_res) => {
    window.location.href = "/all_sections";
  });
}
function deleteRoute(routeId) {
  fetch("/delete-route", {
    method: "POST",
    body: JSON.stringify({ routeId: routeId }),
  }).then((_res) => {
    window.location.href = "/all_routes";
  });
}
function deleteWarning(warningId) {
  fetch("/delete-warning", {
    method: "POST",
    body: JSON.stringify({ warningId: warningId }),
  }).then((_res) => {
    window.location.href = "/all_warnings";
  });
}
function deleteUser(userId) {
  fetch("/delete-user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/all_users";
  });
}