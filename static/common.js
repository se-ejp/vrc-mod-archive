// common.js

// ログイン状態をチェックしてナビバーを更新
function updateNavbar() {
    const userDisplay = document.getElementById('user-display');
    if (!userDisplay) return;

    const nickname = localStorage.getItem('userNickname');
    const userId = localStorage.getItem('userId');
    const userAvatar = localStorage.getItem('userAvatar'); // 追加：アイコンURLを取得

    if (userId) {
        // アイコン画像がある場合はimgタグ、ない場合は頭文字を表示
        let avatarContent;
        if (userAvatar && userAvatar !== "null" && userAvatar !== "") {
            avatarContent = `<img src="${userAvatar}" style="width:100%; height:100%; object-fit:cover; border-radius:50%;">`;
        } else {
            const initial = (nickname || userId)[0].toUpperCase();
            avatarContent = `<span>${initial}</span>`;
        }

        userDisplay.innerHTML = `
            <div class="user-icon" onclick="toggleMenu(event)" style="overflow:hidden; display:flex; align-items:center; justify-content:center;">
                ${avatarContent}
            </div>
            <div class="dropdown-menu" id="dropdown-menu">
                <div class="menu-header">${nickname || userId} さん</div>
                <div class="dropdown-item" onclick="location.href='profile.html?id=${userId}'">プロフィールを見る</div>
                <div class="dropdown-item" onclick="location.href='unchi.txt'">りゅうちゃんです</div>
                <div class="dropdown-item logout" onclick="logout()">ログアウト</div>
            </div>
        `;
    } else {
        userDisplay.innerHTML = `
            <a href="login.html" style="color:#00f2ff; text-decoration:none; font-size:0.85rem; border:1px solid #00f2ff; padding:5px 12px; border-radius:20px; display:inline-block;">
                <span class="pc-text">ログイン / 新規登録</span>
                <span class="sp-text">ログイン</span>
            </a>
        `;
    }
}

function toggleMenu(event) {
    if(event) event.stopPropagation();
    const menu = document.getElementById('dropdown-menu');
    if (menu) menu.classList.toggle('active');
}

function logout() {
    if(confirm("ログアウトしますか？")) {
        localStorage.clear();
        location.reload();
    }
}

// 背景の高さを調整
function fixBgHeight() {
    const bg = document.querySelector('.bg-fixed');
    if (bg) bg.style.height = (window.screen.height * 1.2) + 'px';
}

// 画面外クリックでメニューを閉じる
window.addEventListener('click', (e) => {
    const menu = document.getElementById('dropdown-menu');
    const container = document.getElementById('user-display');
    if (menu && container && !container.contains(e.target)) {
        if (menu) menu.classList.remove('active');
    }
});

// ページ読み込み時に実行
window.addEventListener('DOMContentLoaded', () => {
    updateNavbar();
    fixBgHeight();
});