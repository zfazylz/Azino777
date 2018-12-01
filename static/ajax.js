function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

// Setup ajax connections safetly

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
$(function () {
    $("#roller").click(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/game/",
            data: {
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken" ]').val(),
                betValue: $("#betValue").val(),
            },
            success: function (response) {
                $("#userBalance").html('You have ' + response['userBalance']);
                var userBets = ''
                response['userBets'].forEach(function (singleBet) {
                    userBets += '<small id="betCombination">' + singleBet[0][0] + ':' +
                        singleBet[0][1] + ':' +
                        singleBet[0][2] + ':' +
                        singleBet[0][3] + ':' +
                        singleBet[0][4] + ' </small>  <small id="betValue"> ' +
                        singleBet[1] + '</small><small id="betResult"> ' +
                        singleBet[2] + '</small><br>'
                });
                $("#userBets").html(userBets);

                var lastBetCombo = response['userBets'][0][0]
                $("#userBetsLast").html(lastBetCombo[0] + ' : ' +
                    lastBetCombo[1] + ' : ' +
                    lastBetCombo[2] + ' : ' +
                    lastBetCombo[3] + ' : ' +
                    lastBetCombo[4]
                );

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert('Try to reconnect');
            }
        });
    });
});