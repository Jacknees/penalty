$('#sign').submit(function() {
    var form = $(this);
    
    $.post(form.attr('action'), form.serialize(), function(retorno) {
        
        var iName = $('#aunome').val();
        var iPass = $('#ausenha').val();
        if (iName == '' || iPass == '') {

        } else{
            $('#btnlogin').addClass("disabled");
            $('#btnlogin').text("Aguarde...");
            $.ajax({
                url : "/autentica/",
                type : "POST",
                data : { 
                    username : iName,
                    password : iPass,
                     },

                success : function(json) {
                    if (json == true) {
                        parent.window.document.location.href = '/';
                    } else {
                        $('#aunome, #ausenha').addClass("is-invalid");
                        $('#btnlogin').removeClass("disabled");
                        $('#btnlogin').text("Entrar");                        
                    }            
                },

                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                   $('#btnlogin').removeClass("disabled");
                   $('#btnlogin').text("Entrar");

                }
            }); 
        }
    });
    return false;
});


$('#register').submit(function() {
    var form = $(this);
    $.post(form.attr('action'), form.serialize(), function(retorno) {
        
        var iName = $('#nomer').val();
        var iUser = $('#userr').val();
        var iEmail = $('#emailr').val();
        var iSenha = $('#passwordr').val();
        var iReSenha = $('#repasswordr').val();

        if (iName == '' || iEmail == '' || iSenha == '' || iUser == '' || iSenha == '' || iReSenha == '') {
            alert("Complete todos os campos!");
        } 
        else if (iSenha != iReSenha){
            alert("Senhas não conferem!");
        }
        else{
            $('#btnregister').addClass("disabled");
            $('#btnregister').text("Aguarde...");
            $.ajax({
                url : "/registra/",
                type : "POST",
                data : { 
                    name: iName,
                    username : iUser,
                    email : iEmail,
                    password : iSenha,
                     },

                success : function(json) {
                    console.log("Resultado do processamento: "+json);
                    if (json == true) {
                        parent.window.document.location.href = '/';
                    } else {
                        alert("Tente com dados diferentes!");
                        $('#btnregister').removeClass("disabled");
                        $('#btnregister').text("Registrar-se!");                        
                    }            
                },

                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                   alert("Comportamento inesperado. Contacte o matenedor do projeto.");
                    $('#btnregister').removeClass("disabled");
                    $('#btnregister').text("Registrar-se!");

                }
            }); 
        }
    });
    return false;
});


function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
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

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });