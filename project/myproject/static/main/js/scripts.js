var isLoggedIn = document.cookie.includes("entry=1");
var profileLink = document.getElementById('profileLink');
var loginItem = document.getElementById('loginItem');
var registerItem = document.getElementById('registerItem');
var profileItem = document.getElementById('profileItem');
var logoutItem = document.getElementById('logoutItem');

if (isLoggedIn) {
    var username = getCookieValue('login')
    loginItem.style.display = 'none';
    profileLink.textContent = username;
    registerItem.style.display = 'none';
    profileItem.style.display = 'block';
    logoutItem.style.display = 'block';
} else {
    loginItem.style.display = 'block';
    registerItem.style.display = 'block';
    profileItem.style.display = 'none';
    logoutItem.style.display = 'none';
}

function getCookieValue(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
        return match[2];
    }
    return '';
}