const confirmDialog = document.querySelector("#bookloop-confirm-dialog");
const confirmDialogMessage = document.querySelector("#confirm-dialog-message");
const confirmDialogSubmit = document.querySelector("#confirm-dialog-submit");

if (confirmDialog && confirmDialogMessage && confirmDialogSubmit) {
  let pendingForm = null;

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (pendingForm === form) {
        pendingForm = null;
        return;
      }

      event.preventDefault();
      pendingForm = form;
      confirmDialogMessage.textContent = form.dataset.confirm;
      confirmDialogSubmit.focus();
      confirmDialog.showModal();
    });
  });

  confirmDialog.addEventListener("close", () => {
    if (confirmDialog.returnValue !== "confirm") {
      pendingForm = null;
      return;
    }

    const form = pendingForm;
    pendingForm = null;
    if (form) {
      form.submit();
    }
  });
}
