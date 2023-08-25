// ページが読み込まれたときの処理
document.addEventListener('DOMContentLoaded', function() {
    const signupShowButton = document.querySelector('.signup-show');
    const signupModal = document.getElementById('signup-modal');
    const closeModalButton = document.getElementById('close-modal');

    // モーダル表示ボタンがクリックされたときの処理
    signupShowButton.addEventListener('click', function() {
        signupModal.style.display = 'block';
    });

    // モーダル閉じるボタンがクリックされたときの処理
    closeModalButton.addEventListener('click', function() {
        signupModal.style.display = 'none';
    });
});

