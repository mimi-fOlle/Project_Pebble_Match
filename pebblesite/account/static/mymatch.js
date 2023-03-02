document.addEventListener('DOMContentLoaded', function(){
     let btnSendPebble = document.getElementsByClassName('sendPebble');
     let pebbleSendMatch = document.getElementById('sendPebble');
     let pebbleCongra = document.getElementById('sendPebble1');
     for (let index = 0; index < btnSendPebble.length; index++) {
          btnSendPebble[index].onclick = function () {
                 pebbleSendMatch.classList.toggle('pebbleHide');
                 pebbleCongra.classList.remove('pebbleHide')

          }

     }
     
   
}, false);

window.onload = choosePic;

var myPix = new Array("/static/images/1.jpg",
"/static/images/2.jpg",
"/static/images/3.jpg",
"/static/images/4.jpg",
"/static/images/5.jpg",
"/static/images/6.jpg",
"/static/images/7.jpg",
"/static/images/8.jpg",
"/static/images/9.jpg",
"/static/images/10.jpg",);

function choosePic() {
	randomNum = Math.floor((Math.random() * myPix.length));
	document.getElementById("myPicture").src = myPix[randomNum];
} 
