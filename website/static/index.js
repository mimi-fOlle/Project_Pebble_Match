document.addEventListener('DOMContentLoaded', function(){
     let button_menu = document.getElementsByClassName('button');
     // change front size button 
     for (let index = 0; index < button_menu.length; index++) {
          button_menu[index].onclick = function() {
          for (let j = 0; j < button_menu.length; j++) {
               button_menu[j].classList.remove('scale_button');       
          }

          this.classList.toggle('scale_button');
          console.log('hello');
          
     }
}

}, false);
