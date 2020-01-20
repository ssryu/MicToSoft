onload = function(){

    // smooth-scroll有効化
    const scroll = new SmoothScroll('a[href*="#"]');


    document.getElementById('menu-trigger').onclick = function(){
        document.getElementById('menu-trigger').classList.toggle('active')
        document.getElementById('top-menu').classList.toggle('active')
    }


};
