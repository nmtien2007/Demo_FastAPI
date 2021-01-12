
// (function ($) {
//     "use strict";


    /*==================================================================
    // [ Focus input ]*/
    // $('.input100').each(function(){
    //     $(this).on('blur', function(){
    //         if($(this).val().trim() != "") {
    //             $(this).addClass('has-val');
    //         }
    //         else {
    //             $(this).removeClass('has-val');
    //         }
    //     })
    // });
  
  
    /*==================================================================
    [ Validate ]*/
    // var input = $('.validate-input .input100');
    //
    // $('.validate-form').on('submit',function(){
    //     var check = true;
    //
    //     for(var i=0; i<input.length; i++) {
    //         if(validate(input[i]) == false){
    //             showValidate(input[i]);
    //             check=false;
    //         }
    //     }
    //
    //     return check;
    // });


    // $('.validate-form .input100').each(function(){
    //     $(this).focus(function(){
    //        hideValidate(this);
    //     });
    // });
    //
    // function validate (input) {
    //     if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
    //         if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
    //             return false;
    //         }
    //     }
    //     else {
    //         if($(input).val().trim() == ''){
    //             return false;
    //         }
    //     }
    // }
    //
    // function showValidate(input) {
    //     var thisAlert = $(input).parent();
    //
    //     $(thisAlert).addClass('alert-validate');
    // }
    //
    // function hideValidate(input) {
    //     var thisAlert = $(input).parent();
    //
    //     $(thisAlert).removeClass('alert-validate');
    // }
    
    /*==================================================================
    // [ Show pass ]*/
    // var showPass = 0;
    // $('.btn-show-pass').on('click', function(){
    //     if(showPass == 0) {
    //         $(this).next('input').attr('type','text');
    //         $(this).find('i').removeClass('zmdi-eye');
    //         $(this).find('i').addClass('zmdi-eye-off');
    //         showPass = 1;
    //     }
    //     else {
    //         $(this).next('input').attr('type','password');
    //         $(this).find('i').addClass('zmdi-eye');
    //         $(this).find('i').removeClass('zmdi-eye-off');
    //         showPass = 0;
    //     }
    //
    // });

//     $('.login100-form-btn').on('click', function(){
//         var username = $('#username').val();
//         var password = $('#pass').val();
//         var client_id = $('#client_id').val();
//         var auth_code = $('#auth_code').val();
//         var data = {"user_name": username, "password": password};
//
//         var dataType = 'json';
//
//         // Set Headers
//         var headers = {
//           "Authorization-Code": auth_code,
//           "Client-Id": client_id
//         };
//
//         // Call Api
//         $.ajax({
//             url: "http://localhost:8001/login",
//             headers: headers,
//             method: "POST",
//             dataType: dataType,
//             data: data,
//             success: function(data){
//               alert(data);
//             }
//         });
//
//     });
//
//
// })(jQuery);