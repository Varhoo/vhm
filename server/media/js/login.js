(function($) {
$(document).ready(function(){
    $("#id_mojeid_href").click(function(){
        $("#id_row_login").hide();
        $("#id_row_mojeid").show();
        $("form").attr("action","/openid/")
        return false;
    });
});
})(django.jQuery);
