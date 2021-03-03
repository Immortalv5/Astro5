function openMenu(){
  document.querySelector(".menu").style.width = "250px";
  document.querySelector(".menu").style.visibility = "visible";
  document.querySelector('.move').style.left = "250px";
  document.querySelector('.leftmove').style.right = "250px";
}

function closeMenu(){
document.querySelector(".menu").style.width = "0px";
document.querySelector(".menu").style.visibility = "hidden";
document.querySelector('.move').style.left = "0px";
document.querySelector('.leftmove').style.right = "0px";
}

document.querySelector("#open_menu").addEventListener('click', openMenu);
document.querySelector("#main").addEventListener('click', closeMenu);
