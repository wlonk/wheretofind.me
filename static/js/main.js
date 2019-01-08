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

jQuery(document).ready(function($) {
  // Add:
  $(".add-identity").click(function() {
    // Add placeholder
    var placeholder = $(`
  <div class="identity card">
    <div class="card-body">
      <div class="form-group row">
        <label class="col-sm-2 col-form-label name">Name</label>
        <div class="col-sm-10">
          <input type="text" class="form-control name" name="name" readonly placeholder="...">
        </div>
      </div>
      <div class="form-group row">
        <label class="col-sm-2 col-form-label url">URL</label>
        <div class="col-sm-10">
          <input type="text" class="form-control url" name="url" readonly placeholder="...">
        </div>
      </div>
      <button class="btn delete btn-outline-danger float-right">&minus;</button>
    </div>
  </div>
    `);
    $("form.identities .add-identity").before(placeholder);
    // Hit API
    var url = "/api/identities/";
    var data = {
      "name": "example",
      "url": "https://example.com/"
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
        placeholder.find("input").removeAttr("placeholder");
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

  // Change:
  $("form.identities").change(evt => {
    var identity = $(evt.target).parents(".identity");
    var url = `/api/identities/${identity.data("id")}/`;
    var data = {
      "name": identity.find("input[name=name]").val(),
      "url": identity.find("input[name=url]").val(),
    };
    var csrftoken = getCookie('csrftoken');
    fetch(url, {
      method: "PUT",
      body: JSON.stringify(data),
      credentials: "same-origin",
      headers:{
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      }
    }).then()
    .catch();
  });

  // Delete:
  $("form.identities").on("click", ".delete", evt => {
    var identity = $(evt.target).parents(".identity");
    var url = `/api/identities/${identity.data("id")}/`;
    var csrftoken = getCookie('csrftoken');
    fetch(url, {
      method: "DELETE",
      credentials: "same-origin",
      headers:{
        "X-CSRFToken": csrftoken
      }
    }).then(
      () => {
        identity.remove();
      }
    ).catch();
    return false;
  });

  // Suppress form submission:
  $("form.identities").submit(() => false);
});
