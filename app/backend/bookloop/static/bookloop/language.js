/* Book input MVP: translate fixed UI text without changing user-entered book data. */
(function () {
  const storageKey = "bookloop-language";
  const supportedLanguages = ["en", "ko", "fr"];
  const messages = {
    en: {
      languageLabel: "Language",
      languageHelp: "Translate fixed UI text. Your book data stays unchanged.",
      languageEnglish: "English",
      languageKorean: "Korean",
      languageFrench: "French",
      bookManagement: "Book management",
      addBookTitle: "Add a book",
      editBookTitle: "Edit your book",
      bookTitle: "Book title",
      bookTitlePlaceholder: "Enter the book title",
      author: "Author",
      authorPlaceholder: "Enter the author's name",
      addBookSubmit: "Add book",
      saveChangesSubmit: "Save changes",
      cancel: "Cancel",
      myBooksTitle: "My books",
      myBooksIntro: "Manage the books you own and choose whether each one is available to borrow.",
      addBook: "Add a book",
      yourBookListings: "Your book listings",
      book: "Book",
      availability: "Availability",
      actions: "Actions",
      available: "Available",
      unavailable: "Unavailable",
      edit: "Edit",
      makeAvailable: "Make available",
      makeUnavailable: "Make unavailable",
      delete: "Delete",
      noBooks: "You have not added a book yet.",
      errors: {
        "Book title is required.": "Book title is required.",
        "Author is required.": "Author is required.",
        "This book listing does not exist.": "This book listing does not exist.",
        "Only the book owner can manage this listing.": "Only the book owner can manage this listing.",
        "The book listing could not be saved.": "The book listing could not be saved.",
      },
      feedback: {
        "Your book was added.": "Your book was added.",
        "Your book was updated.": "Your book was updated.",
      },
    },
    ko: {
      languageLabel: "언어",
      languageHelp: "고정 UI 문구만 번역합니다. 입력한 책 정보는 그대로 유지됩니다.",
      languageEnglish: "영어",
      languageKorean: "한국어",
      languageFrench: "프랑스어",
      bookManagement: "책 관리",
      addBookTitle: "책 추가",
      editBookTitle: "책 수정",
      bookTitle: "책 제목",
      bookTitlePlaceholder: "책 제목을 입력하세요",
      author: "저자",
      authorPlaceholder: "저자 이름을 입력하세요",
      addBookSubmit: "책 추가",
      saveChangesSubmit: "변경 내용 저장",
      cancel: "취소",
      myBooksTitle: "내 책",
      myBooksIntro: "내가 소유한 책을 관리하고 대여 가능 여부를 선택합니다.",
      addBook: "책 추가",
      yourBookListings: "내 책 목록",
      book: "책",
      availability: "대여 가능 여부",
      actions: "작업",
      available: "대여 가능",
      unavailable: "대여 불가",
      edit: "수정",
      makeAvailable: "대여 가능으로 변경",
      makeUnavailable: "대여 불가로 변경",
      delete: "삭제",
      noBooks: "아직 추가한 책이 없습니다.",
      errors: {
        "Book title is required.": "책 제목을 입력해야 합니다.",
        "Author is required.": "저자를 입력해야 합니다.",
        "This book listing does not exist.": "이 책 목록을 찾을 수 없습니다.",
        "Only the book owner can manage this listing.": "책 소유자만 이 목록을 관리할 수 있습니다.",
        "The book listing could not be saved.": "책 목록을 저장하지 못했습니다.",
      },
      feedback: {
        "Your book was added.": "책이 추가되었습니다.",
        "Your book was updated.": "책 정보가 수정되었습니다.",
      },
    },
    fr: {
      languageLabel: "Langue",
      languageHelp: "Seuls les textes fixes sont traduits. Les données de votre livre restent inchangées.",
      languageEnglish: "Anglais",
      languageKorean: "Coréen",
      languageFrench: "Français",
      bookManagement: "Gestion des livres",
      addBookTitle: "Ajouter un livre",
      editBookTitle: "Modifier votre livre",
      bookTitle: "Titre du livre",
      bookTitlePlaceholder: "Saisissez le titre du livre",
      author: "Auteur",
      authorPlaceholder: "Saisissez le nom de l'auteur",
      addBookSubmit: "Ajouter le livre",
      saveChangesSubmit: "Enregistrer les changements",
      cancel: "Annuler",
      myBooksTitle: "Mes livres",
      myBooksIntro: "Gérez les livres que vous possédez et choisissez s'ils sont disponibles au prêt.",
      addBook: "Ajouter un livre",
      yourBookListings: "Vos livres",
      book: "Livre",
      availability: "Disponibilité",
      actions: "Actions",
      available: "Disponible",
      unavailable: "Indisponible",
      edit: "Modifier",
      makeAvailable: "Rendre disponible",
      makeUnavailable: "Rendre indisponible",
      delete: "Supprimer",
      noBooks: "Vous n'avez pas encore ajouté de livre.",
      errors: {
        "Book title is required.": "Le titre du livre est obligatoire.",
        "Author is required.": "L'auteur est obligatoire.",
        "This book listing does not exist.": "Cette fiche de livre n'existe pas.",
        "Only the book owner can manage this listing.": "Seul le propriétaire du livre peut gérer cette fiche.",
        "The book listing could not be saved.": "La fiche du livre n'a pas pu être enregistrée.",
      },
      feedback: {
        "Your book was added.": "Votre livre a été ajouté.",
        "Your book was updated.": "Votre livre a été modifié.",
      },
    },
  };

  const pageTranslations = {
    en: {
      languageEnglish: "🇬🇧 English",
      languageKorean: "🇰🇷 Korean",
      languageFrench: "🇫🇷 French",
      signedInUser: "Signed-in user",
      bookLoopHome: "BookLoop home",
      productNavigation: "BookLoop product navigation",
      guest: "Guest",
      profile: "Profile",
      logout: "Log out",
      login: "Log in",
      register: "Register",
      books: "Books",
      sentRequests: "Sent requests",
      receivedRequests: "Received requests",
      myBooks: "My books",
      receivedReports: "Received reports",
      myReports: "My reports",
      booksPageTitle: "Books",
      sentRequestsPageTitle: "My Requests",
      receivedRequestsPageTitle: "Requests for My Books",
      reportsPageTitle: "My Reports",
      chooseAvailableBook: "Choose an available book to create a borrowing request.",
      signInBeforeRequest: "Sign in before requesting a book.",
      you: "You",
      borrowingRequestViews: "Borrowing request views",
      ownerArea: "Owner · Area",
      status: "Status",
      action: "Action",
      yourBook: "Your book",
      requested: "Requested",
      request: "Request",
      requestMessageLabel: "Message (optional)",
      requestMessage: "Message",
      requestMessagePlaceholder: "Add a short message for the book owner.",
      requestMessageHelp: "Maximum 500 characters.",
      sendRequest: "Send request",
      loginToRequest: "Log in to request",
      noBooksAvailable: "No books are available yet.",
      viewRequest: "View Request",
      chooseAnotherBook: "Choose another book",
      myBorrowingRequests: "My borrowing requests",
      onlyMyRequests: "Only requests created by this account are shown.",
      requestUpdated: "Request updated",
      noPendingAction: "No pending action",
      noRequestedBook: "You have not requested a book yet.",
      backToBooks: "Back to books",
      requestsForMyBooks: "Requests for my books",
      onlyOwnedRequests: "Only requests for listings owned by this account are shown.",
      decisionSaved: "Decision saved",
      borrowerArea: "Borrower · Area",
      decision: "Decision",
      reviewDecide: "Review & decide",
      confirmReturn: "Confirm return",
      viewStatus: "View status",
      noOneRequested: "No one has requested one of your books yet.",
      viewMyBorrowingRequests: "View my borrowing requests",
      myReports: "My reports",
      onlyMyReports: "Only reports submitted by this account are shown. The status reflects the latest Admin review.",
      report: "Report",
      reportedUser: "Reported user",
      category: "Category",
      created: "Created",
      noSubmittedReport: "You have not submitted a report yet.",
      confirmAction: "Confirm action",
      areYouSure: "Are you sure?",
      statuses: {
        pending: "Pending",
        approved: "Approved",
        rejected: "Rejected",
        cancelled: "Cancelled",
        return_pending: "Return pending",
        returned: "Returned",
      },
    },
    ko: {
      languageEnglish: "🇬🇧 영어",
      languageKorean: "🇰🇷 한국어",
      languageFrench: "🇫🇷 프랑스어",
      signedInUser: "로그인 사용자",
      bookLoopHome: "BookLoop 홈",
      productNavigation: "BookLoop 제품 탐색",
      guest: "게스트",
      profile: "프로필",
      logout: "로그아웃",
      login: "로그인",
      register: "가입",
      books: "책",
      sentRequests: "보낸 요청",
      receivedRequests: "받은 요청",
      myBooks: "내 책",
      receivedReports: "받은 신고",
      myReports: "내 신고",
      booksPageTitle: "책",
      sentRequestsPageTitle: "내 대여 요청",
      receivedRequestsPageTitle: "내 책에 들어온 요청",
      reportsPageTitle: "내 신고",
      chooseAvailableBook: "대여 가능한 책을 선택해 대여 요청을 만드세요.",
      signInBeforeRequest: "책을 요청하기 전에 로그인하세요.",
      you: "나",
      borrowingRequestViews: "대여 요청 보기",
      ownerArea: "소유자 · 지역",
      status: "상태",
      action: "작업",
      yourBook: "내 책",
      requested: "요청됨",
      request: "요청",
      requestMessageLabel: "메시지 (선택)",
      requestMessage: "메시지",
      requestMessagePlaceholder: "책 소유자에게 짧은 메시지를 남겨 보세요.",
      requestMessageHelp: "최대 500자입니다.",
      sendRequest: "요청 보내기",
      loginToRequest: "로그인 후 요청",
      noBooksAvailable: "아직 이용 가능한 책이 없습니다.",
      viewRequest: "요청 보기",
      chooseAnotherBook: "다른 책 선택",
      myBorrowingRequests: "내 대여 요청",
      onlyMyRequests: "이 계정이 만든 요청만 표시됩니다.",
      requestUpdated: "요청이 업데이트되었습니다.",
      noPendingAction: "대기 중인 작업 없음",
      noRequestedBook: "아직 요청한 책이 없습니다.",
      backToBooks: "책 목록으로",
      requestsForMyBooks: "내 책에 들어온 요청",
      onlyOwnedRequests: "이 계정이 소유한 목록의 요청만 표시됩니다.",
      decisionSaved: "결정이 저장되었습니다.",
      borrowerArea: "요청자 · 지역",
      decision: "결정",
      reviewDecide: "검토 및 결정",
      confirmReturn: "반납 확인",
      viewStatus: "상태 보기",
      noOneRequested: "아직 내 책을 요청한 사람이 없습니다.",
      viewMyBorrowingRequests: "내 대여 요청 보기",
      onlyMyReports: "이 계정이 제출한 신고만 표시됩니다. 상태는 최신 관리자 검토를 반영합니다.",
      report: "신고",
      reportedUser: "신고 대상 사용자",
      category: "분류",
      created: "생성일",
      noSubmittedReport: "아직 제출한 신고가 없습니다.",
      confirmAction: "작업 확인",
      areYouSure: "정말 진행할까요?",
      statuses: {
        pending: "대기 중",
        approved: "승인됨",
        rejected: "거절됨",
        cancelled: "취소됨",
        return_pending: "반납 확인 대기",
        returned: "반납 완료",
      },
    },
    fr: {
      languageEnglish: "🇬🇧 Anglais",
      languageKorean: "🇰🇷 Coréen",
      languageFrench: "🇫🇷 Français",
      signedInUser: "Utilisateur connecté",
      bookLoopHome: "Accueil BookLoop",
      productNavigation: "Navigation du produit BookLoop",
      guest: "Invité",
      profile: "Profil",
      logout: "Se déconnecter",
      login: "Se connecter",
      register: "Créer un compte",
      books: "Livres",
      sentRequests: "Demandes envoyées",
      receivedRequests: "Demandes reçues",
      myBooks: "Mes livres",
      receivedReports: "Signalements reçus",
      myReports: "Mes signalements",
      booksPageTitle: "Livres",
      sentRequestsPageTitle: "Mes demandes",
      receivedRequestsPageTitle: "Demandes pour mes livres",
      reportsPageTitle: "Mes signalements",
      chooseAvailableBook: "Choisissez un livre disponible pour créer une demande de prêt.",
      signInBeforeRequest: "Connectez-vous avant de demander un livre.",
      you: "Vous",
      borrowingRequestViews: "Vues des demandes de prêt",
      ownerArea: "Propriétaire · Région",
      status: "Statut",
      action: "Action",
      yourBook: "Votre livre",
      requested: "Demandé",
      request: "Demander",
      requestMessageLabel: "Message (facultatif)",
      requestMessage: "Message",
      requestMessagePlaceholder: "Ajoutez un court message au propriétaire.",
      requestMessageHelp: "500 caractères maximum.",
      sendRequest: "Envoyer la demande",
      loginToRequest: "Connectez-vous pour demander",
      noBooksAvailable: "Aucun livre n'est encore disponible.",
      viewRequest: "Voir la demande",
      chooseAnotherBook: "Choisir un autre livre",
      myBorrowingRequests: "Mes demandes de prêt",
      onlyMyRequests: "Seules les demandes créées par ce compte sont affichées.",
      requestUpdated: "Demande mise à jour",
      noPendingAction: "Aucune action en attente",
      noRequestedBook: "Vous n'avez pas encore demandé de livre.",
      backToBooks: "Retour aux livres",
      requestsForMyBooks: "Demandes pour mes livres",
      onlyOwnedRequests: "Seules les demandes pour les livres de ce compte sont affichées.",
      decisionSaved: "Décision enregistrée",
      borrowerArea: "Emprunteur · Région",
      decision: "Décision",
      reviewDecide: "Examiner et décider",
      confirmReturn: "Confirmer le retour",
      viewStatus: "Voir le statut",
      noOneRequested: "Personne n'a encore demandé un de vos livres.",
      viewMyBorrowingRequests: "Voir mes demandes de prêt",
      onlyMyReports: "Seuls les signalements de ce compte sont affichés. Le statut reflète le dernier examen de l'administrateur.",
      report: "Signalement",
      reportedUser: "Utilisateur signalé",
      category: "Catégorie",
      created: "Créé le",
      noSubmittedReport: "Vous n'avez encore soumis aucun signalement.",
      confirmAction: "Confirmer l'action",
      areYouSure: "Êtes-vous sûr ?",
      statuses: {
        pending: "En attente",
        approved: "Approuvée",
        rejected: "Refusée",
        cancelled: "Annulée",
        return_pending: "Retour en attente",
        returned: "Retournée",
      },
    },
  };

  Object.keys(pageTranslations).forEach(function (language) {
    Object.assign(messages[language], pageTranslations[language]);
  });

  let currentLanguage = "en";

  function getLanguage() {
    const savedLanguage = window.localStorage.getItem(storageKey);
    return supportedLanguages.includes(savedLanguage) ? savedLanguage : "en";
  }

  function translateError(error, language) {
    return messages[language].errors[error] || error;
  }

  function applyLanguage(language) {
    currentLanguage = language;
    const translation = messages[language];
    document.documentElement.lang = language;

    document.querySelectorAll("[data-i18n]").forEach(function (element) {
      const key = element.dataset.i18n;
      if (translation[key]) element.textContent = translation[key];
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (element) {
      const key = element.dataset.i18nPlaceholder;
      if (translation[key]) element.setAttribute("placeholder", translation[key]);
    });

    document.querySelectorAll("[data-i18n-status]").forEach(function (element) {
      const status = element.dataset.i18nStatus;
      if (translation.statuses[status]) element.textContent = translation.statuses[status];
    });

    document.querySelectorAll("[data-i18n-label]").forEach(function (element) {
      const key = element.dataset.i18nLabel;
      if (translation[key]) element.setAttribute("data-label", translation[key]);
    });

    document.querySelectorAll("[data-i18n-aria-label]").forEach(function (element) {
      const key = element.dataset.i18nAriaLabel;
      if (translation[key]) element.setAttribute("aria-label", translation[key]);
    });

    document.querySelectorAll("[data-book-feedback]").forEach(function (element) {
      const feedback = element.dataset.bookFeedback;
      element.textContent = translation.feedback[feedback] || feedback;
    });

    const form = document.querySelector("[data-book-form]");
    if (form) {
      const mode = form.dataset.bookFormMode;
      const title = mode === "edit" ? translation.editBookTitle : translation.addBookTitle;
      const submit = mode === "edit" ? translation.saveChangesSubmit : translation.addBookSubmit;
      document.title = `BookLoop · ${title}`;
      document.querySelector("[data-book-form-title]").textContent = title;
      document.querySelector("[data-book-submit]").textContent = submit;
      const errorElement = document.querySelector("[data-book-form-error]");
      if (errorElement) {
        errorElement.textContent = translateError(errorElement.dataset.bookFormError, language);
      }
    } else {
      const page = document.querySelector("[data-bookloop-page]");
      const titleKey = page && page.dataset.bookloopTitleKey;
      if (titleKey && translation[titleKey]) {
        document.title = `BookLoop · ${translation[titleKey]}`;
      }
    }

    document.querySelectorAll("[data-book-form-field]").forEach(function (field) {
      field.setCustomValidity("");
    });

    document.querySelectorAll("[data-bookloop-language]").forEach(function (select) {
      select.value = language;
    });
    window.localStorage.setItem(storageKey, language);
  }

  function bindRequiredFieldMessages() {
    const requiredFields = {
      title: "Book title is required.",
      author: "Author is required.",
    };
    document.querySelectorAll("[data-book-form-field]").forEach(function (field) {
      field.addEventListener("invalid", function () {
        if (field.validity.valueMissing) {
          field.setCustomValidity(translateError(requiredFields[field.id], currentLanguage));
        }
      });
      field.addEventListener("input", function () {
        field.setCustomValidity("");
      });
    });
  }

  function bindRequestFormCancelButtons() {
    document.querySelectorAll("[data-request-form-cancel]").forEach(function (button) {
      button.addEventListener("click", function () {
        const details = button.closest("details");
        const form = button.closest("form");
        if (form) form.reset();
        if (details) details.open = false;
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-bookloop-language]").forEach(function (select) {
      select.addEventListener("change", function () {
        applyLanguage(select.value);
      });
    });
    bindRequiredFieldMessages();
    bindRequestFormCancelButtons();
    applyLanguage(getLanguage());
  });
})();
