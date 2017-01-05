$('#submit_btn').addClass('disabled');
    
    $("#input_login").change(function () {
      var username = $(this).val();
      
      if (username.length == 0)
        {
           $('.info_login').text("");
            $('#username_block').removeClass('has-error')
                                .remoteClass('has-success')          
        }
      else
        {
        $.ajax({
          url: "/validate/username/",
          data: {
            'username': username
          },
          dataType: 'json',
          
          success: function (data) {
            $('#info_login').text(data['info']);
            
            if (data.is_okey){
              $('#info_login').removeClass('info_error_text')
                              .addClass('info_ok_text');
              $('#username_block').removeClass('has-error')
                                  .addClass('has-success')
              $('#submit_btn').addClass('active').removeClass('disabled');
            }
            
            else{
              $('#info_login').removeClass('info_ok_text')
                               .addClass('info_error_text');
              $('#username_block').removeClass('has-success')
                                  .addClass('has-error')
              $('#submit_btn').addClass('disabled').removeClass('active');
            }
          }
        });
       }
    });


  $("#input_pass2, #input_pass").change(function () {
    
      var pass2 = $('#input_pass2').val();
      var pass1 = $('#input_pass').val();
    
      if (pass1 == pass2 && pass1.length > 4){
        
        $('.password_block').removeClass('has-error')
                            .addClass('has-success');
        $('#info_pass').text("Паролі співпадають");
        $('#info_pass').removeClass('info_error_text')
                        .addClass('info_ok_text');
      }
      else if (pass2.length < 5 || pass1.length < 5){
        
        $('.password_block').removeClass('has-success').addClass('has-error');     
        $('#info_pass').text("Пароль недостатньо довгий");
        $('#info_pass').removeClass('info_ok_text').addClass('info_error_text');                        
      }
      else if (pass1 != pass2){
        
        $('.password_block').removeClass('has-success').addClass('has-error');     
        $('#info_pass').text("Паролі не співпадають");
        $('#info_pass').removeClass('info_ok_text').addClass('info_error_text');                              
      }
    else{
        $('.password_block').removeClass('has-success').addClass('has-error');     
        $('#info_pass').text("Невідома помилка");
        $('#info_pass').removeClass('info_ok_text').addClass('info_error_text'); 
    }
    
  });
    
