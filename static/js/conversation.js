$(document).ready(function() {
    $("#submit-form").submit(function(e) {
        e.preventDefault();
        var message = $("#message").val();
        $("#message").val("");
        $.ajax({
            type: "POST",
            url: "{% url 'submit_message' %}",
            data: {
                message: message,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
            }
        });
    });
});

