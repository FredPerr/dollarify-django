window.onclick = function(event){
    if (!event.target.matches('.dropdown-toggle'))
        closeAllDropdowns();
};

function closeAllDropdowns(except=null){
    var dropdowns = document.getElementsByClassName('dropdown-menu')
    var i;
    for(i = 0; i < dropdowns.length; i++){
        var dropdown = dropdowns[i];
        if (except != null && dropdown.id == except)
            continue;
        if (dropdown.classList.contains('show')){
            dropdown.classList.remove('show');
        }
    }
}

function toggle_dropdown_menu(id){
    closeAllDropdowns(id)
    document.getElementById(id).classList.toggle('show');
}