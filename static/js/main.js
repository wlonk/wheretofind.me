function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(() => {
  // Add:
  $(".add-identity").click(() => {
    // Add placeholder
    var placeholder = $("template#identity").contents('div').clone();
    $("form.identities .add-identity").before(placeholder);
    // Hit API
    var url = "/api/identities/";
    var data = {
      "name": "",
      "url": ""
    };
    var csrftoken = getCookie('csrftoken');
    fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      credentials: "same-origin",
      headers:{
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      }
    }).then(res => res.json()).then(
      // Replace placeholder
      data => {
        placeholder.data("id", data.id);
        placeholder.find("input").removeAttr("readonly");
        placeholder.find("input.name").val(data.name);
        placeholder.find("label.name").attr("for", `name-${data.id}`);
        placeholder.find("input.name").attr("id", `name-${data.id}`);
        placeholder.find("input.url").val(data.url);
        placeholder.find("label.url").attr("for", `url-${data.id}`);
        placeholder.find("input.url").attr("id", `url-${data.id}`);
      }
    );
    return false;
  });

  var savedIdentitiesOrdering = [];

  // Allow reordering identities
  $("form.identities").sortable({
    items: ".identity",
    axis: "y",
    containment: "parent",
    start: evt => {
      var identities = $(evt.target);
      var url = '/api/identities/reorder/';
      savedIdentitiesOrdering = identities.find('.identity').not('.ui-sortable-placeholder');
    },
    stop: evt => {
      var identities = $(evt.target);
      var url = '/api/identities/reorder/';
      var cards = identities.find('.identity');
      var data = $.map(cards, card => $(card).data('id'));
      var csrftoken = getCookie('csrftoken');

      fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        credentials: "same-origin",
        headers:{
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        }
      })
        .catch(() => {
          cards.detach();
          savedIdentitiesOrdering.insertAfter(identities.find('h1'));
        });
    },
  });

  // Change:
  $("form.identities").change(evt => {
    var identity = $(evt.target).parents(".identity");
    var saving = identity.find('.msg-saving');
    var url = `/api/identities/${identity.data("id")}/`;
    var data = {
      "name": identity.find("input[name=name]").val(),
      "url": identity.find("input[name=url]").val(),
    };
    var csrftoken = getCookie('csrftoken');
    saving.removeClass('d-none');
    fetch(url, {
      method: "PUT",
      body: JSON.stringify(data),
      credentials: "same-origin",
      headers:{
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      }
    }).finally(() => saving.addClass('d-none'));
  });

  // Delete:
  $("form.identities").on("click", ".delete", evt => {
    var identity = $(evt.target).parents(".identity");
    var deleting = identity.find('.msg-deleting');
    var inputs = identity.find('input');
    var url = `/api/identities/${identity.data("id")}/`;
    var csrftoken = getCookie('csrftoken');
    inputs.prop('readonly', true);
    deleting.removeClass('d-none');
    fetch(url, {
      method: "DELETE",
      credentials: "same-origin",
      headers:{
        "X-CSRFToken": csrftoken
      }
    }).then(() => {
      identity.remove();
    }).catch(() => {
      inputs.prop('readonly', false);
      deleting.addClass('d-none');
    });
    return false;
  });

  // Suppress form submission:
  $("form.identities").submit(() => false);
});
