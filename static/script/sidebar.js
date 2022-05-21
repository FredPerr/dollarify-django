var SIDEBAR = null;
var DASHBOARD = null;

window.addEventListener("DOMContentLoaded", (event)=> function(){
    SIDEBAR = document.getElementById('sidebar');
    DASHBOARD = document.getElementById('dashboard');
})

function toggle_sidebar(){

    if (SIDEBAR == null)
        return;

    if(SIDEBAR.style.display == 'none'){
        SIDEBAR.style.width = '200px'
        SIDEBAR.style.display = 'flex'
        DASHBOARD.style.gridTemplateColumns = '200px 1fr'
    } else{
        SIDEBAR.style.width = '0'
        SIDEBAR.style.display = 'none'
        DASHBOARD.style.gridTemplateColumns = '0px 1fr'
    }
}