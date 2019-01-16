/* * /
$(() => {
  var savedIdentitiesOrdering = [];

  // Allow reordering identities
  $("form.identities").sortable({
    items: ".identity",
    axis: "y",
    containment: "parent",
    start: evt => {
      var identities = $(evt.target);
      var url = "/api/identities/reorder/";
      savedIdentitiesOrdering = identities
        .find(".identity")
        .not(".ui-sortable-placeholder");
    },
    stop: evt => {
      var identities = $(evt.target);
      var url = "/api/identities/reorder/";
      var cards = identities.find(".identity");
      var data = $.map(cards, card => $(card).data("id"));
      var csrftoken = getCookie("csrftoken");

      fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        }
      }).catch(() => {
        cards.detach();
        savedIdentitiesOrdering.insertAfter(identities.find("h1"));
      });
    }
  });
});
/* */
