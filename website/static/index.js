document.addEventListener('DOMContentLoaded', function(){
     let button_menu = document.getElementsByClassName('button');
     let showcontent = document.getElementsByClassName('card')
     // change front size button 
     for (let index = 0; index < button_menu.length; index++) {
          button_menu[index].onclick = function() {
          for (let j = 0; j < button_menu.length; j++) {
               button_menu[j].classList.remove('scale_button');       
          }

          this.classList.toggle('scale_button');

          // show tag content

          let tagcontent = this.getAttribute('data-show');
          let showtag = document.getElementById(tagcontent);
          for (let k = 0; k < showcontent.length; k++) {
               showcontent[k].classList.remove('card_show');
               
          }
          showtag.classList.toggle('card_show')
           }     
     }

}, false);
