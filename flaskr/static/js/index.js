// var leftBand = document.querySelector('.left-band');
// var search = document.querySelector('.search');
// var chevronLeft = document.querySelector('.left-band').querySelector('.chevron-left');
// var mainPage = document.querySelector('#main-page');

// chevronLeft.addEventListener('click', showMain);


// var scrollFunc = function (e) {
//     e.stopPropagation();
//     var direct = 0;
//     e = e || window.event;
//     if (e.wheelDelta) {  //判断浏览器IE，谷歌滑轮事件             
//         if (e.wheelDelta > 0) { //当滑轮向上滚动时
//             mouseUpScroll();
//         }
//         if (e.wheelDelta < 0) { //当滑轮向下滚动时
//             mouseDownScroll();
//         }
//     } else if (e.detail) {  //Firefox滑轮事件
//         if (e.detail < 0) { //当滑轮向上滚动时
//             mouseUpScroll();
//         }
//         if (e.detail > 0) { //当滑轮向下滚动时
//             mouseDownScroll();
//         }
//     }
//     // ScrollText(direct);
// }
// //给页面绑定滑轮滚动事件
// document.addEventListener('DOMMouseScroll', scrollFunc, false);
// //滚动滑轮触发scrollFunc方法
// window.onmousewheel = document.onmousewheel = scrollFunc;

// var mouseUpScroll = function () {

// }
// var mouseDownScroll = function () {
//     showMain();
// }

// function showMain() {
//     document.removeEventListener('DOMMouseScroll', scrollFunc);
//     window.onmousewheel = document.onmousewheel = null;
//     // 让欢迎页完全消失后再允许页面滚动，避免滚动事件使得主页面也进行了滚动
//     animate(leftBand, -leftBand.offsetWidth,
//         function () { document.body.style.overflow = 'auto'; },
//         true);
//     animate(search, search.parentNode.offsetWidth, fadeIn(mainPage, 15), true);
// }

// function fadeIn(element, speed) {
//     element.style.display = 'block';
//     var speed = speed || 30;
//     var num = 0;
//     var st = setInterval(function () {
//         num++;
//         element.style.opacity = num / 100;
//         if (num == 100) { clearInterval(st); }
//     }, speed);
// }

// function animate(obj, target, callback, hide) {
//     clearInterval(obj.timer);
//     obj.timer = setInterval(function () {
//         // var step = Math.ceil((target - obj.offsetLeft) / 10);
//         var step = (target - obj.offsetLeft) / 10;
//         step = step > 0 ? Math.ceil(step) : Math.floor(step);
//         if (obj.offsetLeft == target) {
//             clearInterval(obj.timer);
//             if (callback) {
//                 callback();
//             }
//             if (hide) {
//                 obj.style.display = 'none';
//             }
//         }
//         obj.style.left = obj.offsetLeft + step + 'px';
//     }, 15);
// }

// dynamically ajust the width of the page
var w = document.querySelectorAll('.w')
var aside = document.querySelector('.aside-nav')
function witdthAjust () {
    var width = document.body.offsetWidth;
    var ajustWidth;
    if (width > 1850) {
        ajustWidth = 1280;
    }
    else {
        ajustWidth = 1020;
    }
    aside.style.left = width * 0.52 + ajustWidth / 2 + 'px';
    // TODO: check the dynamic ajust
    for (var i = 0; i < w.length; i++){
        w[i].style.width = ajustWidth + 'px';
    }
}
witdthAjust();
window.addEventListener("resize", witdthAjust);

var userMenu = document.querySelector('#user-menu')
var loginInfo = document.querySelector('.user-info')
var loginArrow = document.querySelector('#user-menu').querySelector('.arrow-up')
userMenu.addEventListener("mouseenter", showLoginInfo)
userMenu.addEventListener("mouseleave", hideLoginInfo)

function showLoginInfo() {
    loginInfo.style.display = "block";
    loginArrow.style.display = "block";
}

function hideLoginInfo() {
    loginInfo.style.display = "none";
    loginArrow.style.display = "none";
}