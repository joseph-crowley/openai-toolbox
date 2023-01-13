$(document).ready(function() {
    $("#conversation-form").submit(function(e) {
        e.preventDefault();
        var message = $("#conversation-input").val();
        var conversation_id = $("#conversation_id").val();
        $("#conversation-input").val("");
        $.ajax({
            type: "POST",
            url: "{% url 'submit_message' %}",
            data: {
                message: message,
                conversation_id: conversation_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                $("#conversation-history").html(response);
            }
        });
    });
    $("#select_conversation").submit(function(e) {
        e.preventDefault();
        var conversation_id = $("#conversation_id").val();
        $.ajax({
            type: "POST",
            url: "{% url 'submit_conversation' %}",
            data: {
                conversation_id: conversation_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                location.reload();
            }
        });
    });
});

