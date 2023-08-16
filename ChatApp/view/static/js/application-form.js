// /**
//  * 入力エラーチェック
//  */
// function checkInput() {
//   if (
//       application_form.purpose.value == "" ||
//       application_form.name.value == "" ||
//       application_form.email.value == "" ||
//       application_form.phone.value == ""
//   ){
//       //上記条件に一致する場合
//       alert("空欄もしくは未選択の項目があります");    //エラーメッセージを出力
//       return false;    //送信ボタン本来の動作をキャンセルします
//   } else {
//       return true;    //送信ボタン本来の動作を実行します
//   }
// }

/**
 * ページ読み込み時の処理
 */
window.addEventListener('load', () => {
    //施設名の絞り込み検索機能の登録処理（別途記載）を実行
    registerSortFacilityEvent();
    //確認モーダル立ち上げ機能の登録処理（別途記載）を実行
    registerCreateConfirmModalEvent();
    //確認モーダルを閉じる機能の登録処理（別途記載）を実行
    registerCloseConfirmModalEvent();
})

/**
 * 施設名の絞り込み検索機能の登録処理
 */
function registerSortFacilityEvent() {
  //検索ボタンを取得
  const sortButton = document.getElementById("sortButton");
     //検索ボタンクリック時
     sortButton.addEventListener("click", function() {
      sortFacility();    //施設名の絞り込み検索処理（別途記載）を実行
      console.log("検索の実行");    //挙動確認用
    })
}

/**
 * 確認モーダル立ち上げ機能の登録処理
 */
function registerCreateConfirmModalEvent() {
  //フォーム要素を取得
  const form = document.querySelector("#form");
  //確認モーダル要素を取得
  const confirmModal = document.getElementById('confirm-modal');
    //フォーム送信時の処理
    form.addEventListener("submit", function(event) {
      event.preventDefault();    //フォーム送信を一旦キャンセル
      confirmModal.style.display = 'block';    //確認モーダルの立ち上げ
      console.log("確認モーダルの立ち上げ");    //挙動確認用
    })
}

/**
 * 確認モーダル立ち上げ機能の登録処理
 */
function registerCloseConfirmModalEvent() {
  //確認モーダル要素を取得
  const confirmModal = document.getElementById('confirm-modal');
  //確認モーダルを閉じるボタンを取得
  const closeConfirmModalButton = document.getElementById('confirm-modal-close');
  // ボタンがクリック時の処理
    closeConfirmModalButton.addEventListener('click', function() {
      confirmModal.style.display = 'none';   //確認モーダルを閉じる
      console.log("確認モーダルを閉じる");    //挙動確認用
    })
}

/**
 * 施設名の絞り込み検索処理
 */
function sortFacility() {
  const sortKeywordValue = document.getElementById("sortKeyword").value.toUpperCase();    //検索フォームに入力されたキーワードをの値を取得（大文字に揃える）
  const facilityList = document.getElementsByClassName("facilityList");    //選択肢（選択ボタン＋施設名）の要素を取得
  const facilityName = document.getElementsByClassName("facilityName");    //施設名の要素を取得

    for (i = 0; i < facilityList.length; i++) {    //選択肢の要素の個数分繰り返し
      facilityNameValue = facilityName[i].textContent;    //施設名の要素から値を抽出し変数に代入
      if (facilityNameValue.toUpperCase().indexOf(sortKeywordValue) > -1) {    //施設名の値とキーワードの値が不一致でなければ（施設名の値は大文字に揃える）
        facilityList[i].style.display = "";    //選択肢の要素を表示
      } else {
        facilityList[i].style.display = "none";   //その他の場合は選択肢の要素を非表示
      }
    }
}
