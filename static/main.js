document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach(el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');

      });
    });
  }

});

var theme = document.querySelector("#theme-link");

let mode;
mode = localStorage.getItem('mode');
if (mode === 'light'){
  lightMode();
}else{
  darkMode(); 
}
function checkmode(){
  if (mode === 'light'){
    darkMode();
  }else{
    lightMode(); 
  }

}


function darkMode() {
  theme.href = "/static/css/cyborg.css";
  document.getElementById("darkmodebtn").innerHTML = "Light Mode ";
  localStorage.setItem('mode', 'dark');
  mode = localStorage.getItem('mode');
}

function lightMode() {
  theme.href = "/static/css/bulma.css";
  document.getElementById("darkmodebtn").innerHTML = "Dark Mode ";
  localStorage.setItem('mode', 'light');
  mode = localStorage.getItem('mode');
}
