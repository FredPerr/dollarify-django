window.onclick = function(event){
    if (!event.target.matches('.dropdown-toggle')){
        var dropdowns = document.getElementsByClassName('dropdown-menu')
        var i;
        for(i = 0; i < dropdowns.length; i++){
            var dropdown = dropdowns[i];
            if (dropdown.classList.contains('show')){
                dropdown.classList.remove('show')
            }
        }
    }
};

function expand_dropdown_menu(id){
    document.getElementById(id).classList.toggle('show');
}