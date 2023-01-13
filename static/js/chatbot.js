$(document).ready(function(){
    $("#message-form").submit(function(event){
        event.preventDefault();
        var message = $("#message-input").val();
        $.ajax({
            type: "POST",
            url: "{% url 'submit_message' %}",
            data: {
                message: message,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(data) {
                var bot_response = data.bot_response;
                $("#conversation").append("<div class='bot-response'>" + bot_response + "</div>");
                $("#message-input").val("");
            }
        });
    });
});

