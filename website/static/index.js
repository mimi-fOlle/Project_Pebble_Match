document.addEventListener('DOMContentLoaded', function () {
  let button_menu = document.getElementsByClassName('button-menu');
  let btn_about1 = document.getElementsByClassName('btn_about');
  let show_text = document.getElementsByClassName('content-to-show');
  // change front size button 
  for (let index = 0; index < button_menu.length; index++) {
    button_menu[index].onclick = function () {
      for (let j = 0; j < button_menu.length; j++) {
        button_menu[j].classList.remove('scale_button');
      }

      this.classList.toggle('scale_button');

    }
    /* show and hide about content */
    for (let k = 0; k < btn_about1.length; k++) {
      btn_about1[k].onclick = function () {
          console.log(k); 
        let getDatatext = this.getAttribute('data-show')
       /*  console.log(getDatatext); */
        
        let getIdParagrap = document.getElementById(getDatatext);
/*         console.log(getIdParagrap); */
        
    /*     for (let l = 0; l < show_text.length; l++) {
          show_text[l].classList.remove('about-to-show');
        } */
        getIdParagrap.classList.toggle('about-to-show');

      };

    }
  }

}, false);
