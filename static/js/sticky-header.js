window.onscroll = function() {
    var header = document.querySelector('.index_header');
    var nav = document.querySelector('.navBar');

    var scrollPosition = window.scrollY || document.documentElement.scrollTop;

    if (scrollPosition > header.clientHeight) {
        header.style.position = 'fixed';
        nav.style.top = header.clientHeight + 'px';
    } else {
        header.style.position = 'relative';
        nav.style.top = '0';
    }
};