window.onclick = function(event){
    if (!event.target.matches('.dropdown-button')){
        var dropdowns = document.getElementsByClassName('dropdown-content')
        var i;
        for(i = 0; i < dropdowns.length; i++){
            var dropdown = dropdowns[i];
            if (dropdown.classList.contains('dropdown-content-visible')){
                dropdown.classList.remove('dropdown-content-visible')
            }
        }
    }
};