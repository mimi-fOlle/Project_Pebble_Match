document.addEventListener('DOMContentLoaded', function(){
     let btn_show_signup = document.getElementById('show_signup');
     let div_show_signup = document.getElementById('signup-content');
     let rule_18 = document.getElementById('ct-accept');

     let checkbox = document.getElementById('flexCheckDefault');
     checkbox.onclick = function() {
          if (checkbox.checked == true) {
               btn_show_signup.style.display="block";
          } else {
               btn_show_signup.style.display="none";
          }
     }

     btn_show_signup.onclick = function() {
          div_show_signup.classList.toggle('signup-content-show');
          rule_18.classList.add('ct-accept-hidden');
          

     }

}, false);
