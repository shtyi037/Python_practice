$(function() {
    $("#uphone").blur(function() {
        if ($(this).val() == " ") {
            $("#uphone_err").html("手機號碼不能為空");
            $("#uphone_err").css("color", "#f00");
        } else {
            $("#uphone_err").html("");
        }
    });
});